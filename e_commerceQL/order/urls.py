from rest_framework import routers, serializers, viewsets
from graphene_django.views import GraphQLView
from django.urls import path, include
from order.schema import schema
from .views import *



router = routers.DefaultRouter()
# router.register('product-list', ProductListView, 'product-list')


urlpatterns = [
	path('', include(router.urls)),

	path("graphql", GraphQLView.as_view(graphiql=True, schema=schema)),

	path('api-user/register/', UserRegistrationAPIView.as_view(), name='api-register'),
    path('api-user/login/', UserLoginAPIView.as_view(), name='api-login'),
    path('api-user/logout/', UserLogoutAPIView.as_view(), name='api-logout'),


    path('api-shop/categories/', CategoryListView.as_view(), name='category-list'),
    path('api-shop/products/', ProductListView.as_view(), name='product-list'),


    path('api-cart/create/', CartCreateView.as_view(), name='cart-create'),
    path('api-cart/items/create/', CartItemCreateView.as_view(), name='cart-item-create'),

    path('api-orders/<int:cart_id>/', OrderView.as_view(), name='order-view'),
    path('stripe/webhook/', stripe_webhook, name='stripe-webhook'),

]