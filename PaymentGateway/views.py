import base64
import requests
import cashaddress
from pywallet.utils import Wallet
from base58 import b58decode_check, b58encode_check
import watchtower
from datetime import datetime
from decimal import Decimal

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.status import HTTP_400_BAD_REQUEST
# from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from django.contrib.auth import authenticate, login
from django.conf import settings
from django.http import JsonResponse
# from django.contrib.auth.decorators import permission_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import Permission
from django.contrib.auth.hashers import check_password 
from django.shortcuts import get_object_or_404

from woocommerce import API
from .models import Order, Storefront, Account, Product, OrderItem, TotalSales, TotalSalesYesterday, TotalSalesByMonth, TotalSalesByYear
from .forms import UserForm, WalletForm
from bch_api.serializers import UserSerializer, ListUsersSerializer, TotalSalesSerializer, TotalSalesYesterdaySerializer, TotalSalesByMonthSerializer, TotalSalesByYearSerializer
from PaymentGateway.serializers import GetOrderSerializer, TotalBCHSerializer, ProcessOrderSerializer

# ------------------------------------------------------------------------------
# ACCOUNT/USER
# ------------------------------------------------------------------------------

@api_view(['GET'])
def user_info(request):
    # Get the token from the request headers or query params
    token_key = request.META.get('HTTP_AUTHORIZATION', '').split('Token ')[-1] or \
                request.GET.get('token')

    if token_key:
        # Use the token to retrieve the member instance
        account = Account.get_account_from_token(token_key)

        if account:
            # Return the member's info in a JSON response
            user = Account.objects.get(email=account.email)
            account = user
            
            response_data = {
                'id': str(account.user_id),
                'full_name': account.full_name,
                'email': account.email,
                'username': account.username,
                'xpub_key': account.xpub_key,
                'wallet_hash': account.wallet_hash,
                'created_at': account.created_at,
            }
            return JsonResponse(response_data)
            # return JsonResponse(user)

    # Token is invalid or missing
    return JsonResponse({'error': 'Invalid or missing token.'}, status=HTTP_400_BAD_REQUEST)

class UserApiView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Account.objects.all()
    
    # user = authenticate(username='john', password='secret')
    
    def get(self, request):
        # todos = Todo.objects.filter(user = request.user.id)
        # todos = Order.objects.filter(user = str(request.user))
        get_users = Account.objects.all()
        # serializer = TodoSerializer(todos, many=True)
        serializer = ListUsersSerializer(get_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SignUpAPIView(APIView):
    permission_classes = [AllowAny]
    
    @csrf_exempt
    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')
        
        user_email = Account.objects.filter(email=email).first()
        user_username = Account.objects.filter(username=username).first()
        if user_email:
            return Response({'status': 'errors', 'errors': {'email': 'Email already exists'}})
        elif user_username:
            return Response({'status': 'errors', 'errors': {'username': 'Username already exists'}})
        else:
            form = UserForm(request.data)
            if form.is_valid():
                save_form = form.save(commit=False)
                save_form.save()
                
                token = Token.objects.create(user=save_form.auth_user)
                
                return Response({'token': token.key, 'status': 'New User added', 'status': 'success'})
            else:
                return Response({'status': 'errors', 'errors': form.errors})
        
        
class LoginAPIView(APIView):
    # permission_classes = [IsAuthenticated]  # Add this line to require authentication
    permission_classes = [AllowAny]
    
    # @csrf_exempt
    # def get(self, request):
    #     csrf_token = request.COOKIES.get('csrftoken')
    #     if not csrf_token:
    #         csrf_token = settings.CSRF_COOKIE
    #     return Response({'csrf_token': csrf_token})
        
    
    @csrf_exempt
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = authenticate(username=email, password=password)
        
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            # login(request, user)
            user = Account.objects.get(email=email)
            full_name = user.full_name
            return Response({'token': token.key, 'full_name': full_name , 'status': 'success'})
        else:
            return Response({'status': 'error', 'message': 'Invalid email or password'})
        
class EditAccountAPIView(APIView):
    @csrf_exempt
    def post(self, request):
        return Response({'test': 'test'})
        
class WalletAPIView(APIView):
    # permission_classes = [IsAuthenticated]  # Add this line to require authentication
    authentication_classes = [TokenAuthentication]
    # permission_classes = [AllowAny]
    
    @csrf_exempt
    def post(self, request):
        user = request.user
        form = WalletForm(request.data, instance=user)
        
        if form.is_valid():
            save_form = form.save(commit=False)
            save_form.save()
            
            return Response({'status': 'success', 'status': 'Paytaca Wallet updated'})
        else:
            return Response({'status': 'errors', 'errors': form.errors})
        
# ------------------------------------------------------------------------------
# ORDERS
# ------------------------------------------------------------------------------

class GetOrderAPIView(APIView):
    def post(self, request):
        # extract order details from the request
        serializer = GetOrderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        order_id = serializer.validated_data['order_id']
        store_url = serializer.validated_data['store_url']
        
        # check if the store_url exists in Storefront model
        storefront = get_object_or_404(Storefront, store_url=store_url)
        
        # create the order only if the storefront exists using WooCommerceAPI
        wcapi = API(
            url=storefront.store_url,
            consumer_key=storefront.key,
            consumer_secret=storefront.secret,
            version="wc/v3",
            verify_ssl=False,
        )

        # get the order using the order_id and the WooCommerceAPI
        response = wcapi.get(f"orders/{order_id}")  
        if response.status_code != 200:
            return Response('Invalid order ID', status=status.HTTP_400_BAD_REQUEST)

        order_data = response.json()

        # get BCH exchange rate using CoinGecko API
        bch_rate = None
        try:
            response = requests.get("https://api.coingecko.com/api/v3/simple/price", params={"ids": "bitcoin-cash", "vs_currencies": order_data['currency'].lower()})
            response.raise_for_status()
            bch_rate = response.json()["bitcoin-cash"][order_data['currency'].lower()]
        except (requests.exceptions.RequestException, KeyError):
            pass

        # convert total to BCH
        total_bch = Decimal(order_data['total'])
        if bch_rate is not None:
            total_bch /= Decimal(bch_rate)

        # save the order in the Order model
        order = Order(
            store=storefront,
            order_id=order_data['id'],
            customer_name=order_data['billing']['first_name'] + ' ' + order_data['billing']['last_name'],
            status=order_data['status'],
            total=order_data['total'],
            total_bch=total_bch,
            payment_method=order_data['payment_method'],
            created_at=order_data['date_created_gmt'],
            updated_at=order_data['date_modified_gmt']
        )
        order.save()

        # get the products from the order and save them in the database
        for item in order_data['line_items']:
            product_id = item['product_id']
            product = Product.objects.filter(store=storefront, product_id=product_id).first()
            if product is None:
                product_data = wcapi.get(f"products/{product_id}").json()
                product = Product(
                    store=storefront,
                    product_id=product_id,
                    name=product_data['name'],
                    price=Decimal(product_data['price']),
                )
                product.save()
            quantity = item['quantity']
            OrderItem.objects.create(
                order=order,
                product=product,
                store=storefront,
                quantity=quantity,
                price=Decimal(item['price']),
            )

        return Response('Order saved successfully', status=status.HTTP_201_CREATED)

class TotalBCHAPIView(APIView):
    def post(self, request):
        # get the order ID and storefront URL from the POST request
        serializer = TotalBCHSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        order_id = serializer.validated_data['order_id']
        store_url = serializer.validated_data['store_url']

        # get the order and storefront using the order ID and storefront URL
        storefront = get_object_or_404(Storefront, store_url=store_url)
        order = get_object_or_404(Order, store=storefront, order_id=order_id)

        # get the total BCH based on the total amount of the order
        total_bch = order.total_bch

        # generate a new BCH address for the order using the associated user of the storefront
        owner = storefront.account
        new_bch_address = self.generate_address(
            project_id = "964e97eb-b88c-4562-ae18-c45c90756db7",
            wallet_hash = owner.wallet_hash,
            xpub_key = owner.xpub_key,
            index = order.order_id,
            webhook_url=""
        )

        # return the total BCH in a JSON response
        return Response({'total_bch': total_bch, 'bch_address': new_bch_address}, status=status.HTTP_200_OK)

    def generate_address(self, project_id, wallet_hash, xpub_key, index, webhook_url):
        wallet_obj = Wallet.deserialize(
            xpub_key,
            network='BCH'
        )
        child_wallet = wallet_obj.get_child_for_path('0')
        new_address = child_wallet.create_new_address_for_user(index)
        bitpay_addr = new_address.to_address()
        legacy = b58encode_check(b'\x00' + b58decode_check(bitpay_addr)[1:])
        addr_obj = cashaddress.convert.Address.from_string(legacy)
        cash_addr = addr_obj.cash_address()

        data = {
            'addresses': {
                'receiving': cash_addr
            },
            'address_index': index,
            'project_id': project_id,
            'wallet_hash': wallet_hash,
            'webhook_url': webhook_url
        }

        result = watchtower.subscribe(**data)

        if result['success']:
            print("Cash Address: ", cash_addr)
            return cash_addr
        else:
            return None
        
class ProcessOrderAPIView(APIView):
    def post(self, request):
        # Get the order ID, store URL, and total recieved from the request body
        serializer = ProcessOrderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        order_id = serializer.validated_data['order_id']
        store_url = serializer.validated_data['store_url']
        total_received = serializer.validated_data['total_received']

        print(total_received)
        # Get the order from the database using the order ID and store URL
        order = get_object_or_404(Order, order_id=order_id, store=store_url)

        try:
            # Update the status of the order
            order.status = 'completed'
            order.updated_at = datetime.now()
            order.total_received = total_received
            order.save()

            # Mark the order as completed in WooCommerce using the REST API
            # Get the storefront associated with the order
            storefront = get_object_or_404(Storefront, store_url=store_url)
            # Get the WooCommerce credentials from the storefront model
            wc_url = f'{storefront.store_url}/wp-json/wc/v3/orders/{order_id}'
            wc_key = storefront.key
            wc_secret = storefront.secret

            headers = {
                'Authorization': 'Basic ' + base64.b64encode(f"{wc_key}:{wc_secret}".encode('utf-8')).decode('utf-8'),
                'Content-Type': 'application/json'
            }

            data = {
                'status': 'completed'
            }

            response = requests.put(wc_url, headers=headers, json=data, verify=False)

            # Return a JSON response indicating success or failure
            if response.ok:
                return Response({'success': True})
            else:
                return Response({'success': False, 'error': response.reason})

        except Exception as e:
            return Response({'success': False, 'error': str(e)})
   
# ------------------------------------------------------------------------------
# TOTAL SALES
# ------------------------------------------------------------------------------   

class TotalSalesAPIView(APIView):
    def get(self, request):
        get_total_sales = TotalSales.objects.all()
        serializer = TotalSalesSerializer(get_total_sales, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class TotalSalesYesterdayAPIView(APIView):
    def get(self, request):
        get_total_sales_yesterday = TotalSalesYesterday.objects.all()
        serializer = TotalSalesYesterdaySerializer(get_total_sales_yesterday, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class TotalSalesByMonthAPIView(APIView):
    def get(self, request):
        get_total_sales_by_month = TotalSalesByMonth.objects.all()
        serializer = TotalSalesByMonthSerializer(get_total_sales_by_month, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class TotalSalesByYearAPIView(APIView):
    def get(self, request):
        get_total_sales_by_year = TotalSalesByYear.objects.all()
        serializer = TotalSalesByYearSerializer(get_total_sales_by_year, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)