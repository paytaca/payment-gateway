from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from PaymentGateway.models import User, Order, Storefront, TotalSalesByMonth, TotalSales
from bch_api.serializers import UserSerializer, StorefrontSerializer, OrdersSerializer, TotalSalesByMonthSerializer

'''Kanan pagtesting han pasa pasa chuchu'''
# from .serializers import TotalSalesSerializer
# from PaymentGateway.forms import TestForm
# from django.http import JsonResponse

# Create your views here.


User = get_user_model()

class StorefrontApiView(APIView):
    def get(self, request):
        storefront = Storefront.objects.all()
        serializer = StorefrontSerializer(storefront, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrdersApiView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        # todos = Todo.objects.filter(user = request.user.id)
        # todos = Order.objects.filter(user = str(request.user))
        orders = Order.objects.all()
        # serializer = TodoSerializer(todos, many=True)
        serializer = OrdersSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrdersTotalSalesByMonthApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # def get_object(self, todo_id):
    #     '''
    #     Helper method to get the object with given todo_id, and user_id
    #     '''
    #     try:
    #         # return Todo.objects.get(id=todo_id, user = user_id)
    #         return TotalSalesByMonth.objects.get(total_sale=1)
    #     except TotalSalesByMonth.DoesNotExist:
    #         return None

    # 3. Retrieve
    def get(self, request, *args, **kwargs):
        # '''
        # Retrieves the Todo with given todo_id
        # '''
        # todo_instance = self.get_object(todo_id)
        # if not todo_instance:
        #     return Response(
        #         {"res": "Object with order id does not exists"},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )

        # serializer = TotalSalesByMonthSerializer(todo_instance)
        
        todos = TotalSalesByMonth.objects.all()
        serializer = TotalSalesByMonthSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserApiView(APIView):
    def get(self, request):
        '''
        List all the todo items for given requested user
        '''
        # todos = Todo.objects.filter(user = request.user.id)
        # todos = Order.objects.filter(user = str(request.user))
        todos = User.objects.all()
        # serializer = TodoSerializer(todos, many=True)
        serializer = UserSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

''' kanan pagtesting han pasa pasa chuchu '''
    
# class TestView(APIView):
#     def get(self, request):
#         total = Test.objects.all()
#         serializer = TestSerializer(total, many=True)

#         return Response(serializer.data)
    
# class CreateTestView(APIView):
#     """ Create Test Table """
#     def post (self, request):
#         form = TestForm(request.data)

#         if form.is_valid():
#             test = form.save(commit=False)
#             test.save()

#             return Response({'status': 'New test added'})
#         else:
#             return Response({'status': 'errors', 'errors': form.errors})