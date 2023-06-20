# ECommerce_Dev

E-Commerce assignment details:

I developed an ecommerce site.
I used django REST to implement the features.
The system can see the categories and products info.
It ca add new category and product details
Users can register, login and add products to the cart.
The cart is posted for submission with ‘pending’ status.
The requirements file is in the ‘requirements.txt’ file.
Install the requirements file to run the project.
I also used GraphQL to get the product data only. It is new to me but I understand it. I think I can implement the entire project in GraphQl if given time.
At last I tried to implement a payment gateway to the project. I used Stripe. Unfortunately I couldn’t test this.
github: https://github.com/FarabiAkash/ECommerce_Dev



API REQUESTS

POST
http://127.0.0.1:8000/api-user/register/
Request body:
{
    "email": "alfa3@gmail.com",
    "username": "alfa3",
    "password": "12345"
}

POST
http://127.0.0.1:8000/api-user/login/
Request body:
{
    "username": "alfa3",
    "password": "12345"
}

POST
http://127.0.0.1:8000/api-user/logout/

GET // POST
http://127.0.0.1:8000/api-shop/products/

GET // POST
http://127.0.0.1:8000/api-shop/categories/

POST
http://127.0.0.1:8000/api-cart/items/create/
Request body:
{
    "cart": 1,
    "product": 3,
    "quantity": 2
}

POST
http://127.0.0.1:8000/api-cart/create/

GET
http://127.0.0.1:8000/api-orders/<int:cart_id>/


