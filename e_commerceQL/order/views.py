from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate

from rest_framework import viewsets


from .serializers import *
from .models import *

from django.conf import settings
from django.http import JsonResponse
import stripe
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json




class UserRegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response(serializer.errors, status=400)


class UserLoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Invalid credentials'}, status=401)


class UserLogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=204)



class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)



    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            category = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


        
class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class CartCreateView(APIView):
    def post(self, request):
        cart = Cart.objects.create(user=request.user)
        serializer = CartSerializer(cart)
        order = Order.objects.create(cart=cart)
        order.save()
        return Response(serializer.data)






class CartItemCreateView(APIView):
    def post(self, request):
        serializer = CartItemSerializer(data=request.data)
        if serializer.is_valid():
            cart_item = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class OrderView(APIView):
    def get(self, request, cart_id):
        cart = Cart.objects.get(id=cart_id)
        cartitems= CartItem.objects.filter(cart=cart)
        order = Order.objects.filter(cart__id=cart_id).first()
        result={}
        order_id=order.id
        order_date=order.order_date
        total_amount=0
        cartitems= CartItem.objects.filter(cart=order.cart)
        items=[]
        for item in cartitems:
        	temp={}
        	temp['product_name']=item.product.name
        	temp['product_price']= item.product.price
        	temp['quantity']= item.quantity
        	total_amount=total_amount+(item.quantity*item.product.price)
        	result['order_id'] = order.id
        	result['order_date'] = order.order_date
        	result['total_amount'] = total_amount
        	items.append(temp)
        result['items']=items
        serializer = OrderSerializer(order)
        return Response(result)




    def post(self, request, cart_id):

        print(cart_id)
        return Response({'msg':'done'}, status=400)


def create_payment_intent(request):
    # Retrieve the amount from the request data
    amount = request.data.get('amount')

    try:
        # Create a payment intent
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',  # Specify the currency
            payment_method_types=['card']  # Specify the accepted payment method types
        )

        # Return the client secret of the payment intent
        return JsonResponse({'client_secret': intent.client_secret})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



# views.py


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Process the event
    if event.type == 'payment_intent.succeeded':
        print('Handle successful payment event')
        # Access event data using event.data object

    # Handle other event types as needed

    return HttpResponse(status=200)
