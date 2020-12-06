from django.shortcuts import render, redirect
from django.http import HttpResponse
from Store.models.product import Product
from Store.models.category import Category
from Store.models.customer import Customer
from Store.models.customer import Customer
from django.contrib.auth.hashers import make_password, check_password
from django.views import View
#print(make_password('1234'))
#print(check_password('12345','pbkdf2_sha256$216000$2fVqbDqzoIro$A1/JRtrK3nudXkLApmVJXcOJgOHXcjVarO22EL+/pW4='))

# Create your views here.

class Index(View):
    
    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        print(product)
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity :
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1                    
                else:
                      cart[product] = quantity + 1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print( request.session['cart'])
        return redirect('homepage')

    # Display products based on CategoryID
    def get(self, request):
        #print(request.session.get('first_name'))
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}

        products = None
        categories = Category.get_all_categories()
        categoryId = request.GET.get('category')
        if categoryId:
            products = Product.get_all_products_by_categoryid(categoryId)
        else:
            products = Product.get_all_products()
        data = {}
        data['products'] = products
        data['categories'] = categories
        print('You Are : ', Customer.first_name)
        #print('You Are : ', request.session['cart'])
        print('You Are : ', request.session.get('email'))
      #  print('You Are : ', request.session.user)
        return render(request, 'index.html', data)






