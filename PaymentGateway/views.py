# # from django.shortcuts import render
# # from django.http import JsonResponse
# # from .models import Order
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status, permissions
# from django.contrib.auth import get_user_model
# from django.shortcuts import get_object_or_404
# # from bch_api.models import Todo
# from .models import User, Order, Storefront, TotalSalesByMonth
# from bch_api.serializers import TodoSerializer, TestSerializer, TotalSalesByMonthSerializer
# # Create your views here.

# # def order_list(request):
# #     orders = Order.objects.all()
# #     data = [{
# #         'order_id': Order.order_id,
# #         'customer_name': Order.customer_name,
# #         'status': Order.status,
# #         'total': Order.total,
# #         'created_at': Order.created_at,
# #         'updated_at': Order.updated_at
# #     } for Order in orders]

# #     return JsonResponse(data, safe = False)

# User = get_user_model()

# class TestApiView(APIView):
#     # permission_classes = [permissions.IsAuthenticated]
    
#     def get(self, request, *args, **kwargs):
#         '''
#         List all the todo items for given requested user
#         '''
#         # todos = Todo.objects.filter(user = request.user.id)
#         # todos = Order.objects.filter(user = str(request.user))
#         todos = Order.objects.all()
#         # serializer = TodoSerializer(todos, many=True)
#         serializer = TestSerializer(todos, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

# class TestTotalSalesByMonthApiView(APIView):
#     # add permission to check if user is authenticated
#     # permission_classes = [permissions.IsAuthenticated]

#     # def get_object(self, todo_id):
#     #     '''
#     #     Helper method to get the object with given todo_id, and user_id
#     #     '''
#     #     try:
#     #         # return Todo.objects.get(id=todo_id, user = user_id)
#     #         return TotalSalesByMonth.objects.get(total_sale=1)
#     #     except TotalSalesByMonth.DoesNotExist:
#     #         return None

#     # 3. Retrieve
#     def get(self, request, *args, **kwargs):
#         # '''
#         # Retrieves the Todo with given todo_id
#         # '''
#         # todo_instance = self.get_object(todo_id)
#         # if not todo_instance:
#         #     return Response(
#         #         {"res": "Object with order id does not exists"},
#         #         status=status.HTTP_400_BAD_REQUEST
#         #     )

#         # serializer = TotalSalesByMonthSerializer(todo_instance)
        
#         todos = TotalSalesByMonth.objects.all()
#         serializer = TotalSalesByMonthSerializer(todos, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
