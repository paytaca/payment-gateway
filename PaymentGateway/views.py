# from django.shortcuts import render
# from django.http import JsonResponse
# from .models import Order
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
# from bch_api.models import Todo
from .models import User, Order, Storefront
from bch_api.serializers import TodoSerializer, TestSerializer
# Create your views here.

# def order_list(request):
#     orders = Order.objects.all()
#     data = [{
#         'order_id': Order.order_id,
#         'customer_name': Order.customer_name,
#         'status': Order.status,
#         'total': Order.total,
#         'created_at': Order.created_at,
#         'updated_at': Order.updated_at
#     } for Order in orders]

#     return JsonResponse(data, safe = False)

User = get_user_model()

class TestApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        # todos = Todo.objects.filter(user = request.user.id)
        # todos = Order.objects.filter(user = str(request.user))
        todos = Order.objects.all()
        # serializer = TodoSerializer(todos, many=True)
        serializer = TestSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request):
        user = request.user
        storefront = Storefront.objects.get(user=user)
        order_data = request.data.copy()
        order_data['user'] = user.id
        order_data['store'] = storefront.store_url
        serializer = TestSerializer(data=order_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, order_id):
        order = get_object_or_404(Order, user=request.user, order_id=order_id)
        serializer = TestSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, order_id):
        order = get_object_or_404(Order, user=request.user, order_id=order_id)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TestDetailApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, todo_id, user_id):
        '''
        Helper method to get the object with given todo_id, and user_id
        '''
        try:
            # return Todo.objects.get(id=todo_id, user = user_id)
            return Order.objects.get(order_id=todo_id, user = user_id)
        except Order.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, todo_id, *args, **kwargs):
        '''
        Retrieves the Todo with given todo_id
        '''
        todo_instance = self.get_object(todo_id, 0)
        if not todo_instance:
            return Response(
                {"res": "Object with order id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = TodoSerializer(todo_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, todo_id, *args, **kwargs):
        '''
        Updates the todo item with given todo_id if exists
        '''
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'task': request.data.get('task'), 
            'completed': request.data.get('completed'), 
            'user': request.user.id
        }
        serializer = TodoSerializer(instance = todo_instance, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, todo_id, *args, **kwargs):
        '''
        Deletes the todo item with given todo_id if exists
        '''
        todo_instance = self.get_object(todo_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        todo_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )
