from django.shortcuts import render, redirect
from django.http import HttpResponse
from Store.models.customer import Customer
from django.contrib.auth.hashers import make_password
from django.views import View



# Signup Class
class Signup(View):

    def get(self, request):
        return render(request, 'signup.html')

    # Signup New Costumer
    def post(self, request):
        post = request.POST
        first_name = post.get('firstname')
        last_name = post.get('lastname')
        phone = post.get('phone')
        email = post.get('email')
        password = post.get('password')

        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None
        customer = Customer(first_name=first_name,
                            last_name=last_name,
                            phone=phone,
                            email=email,
                            password=password)

        error_message = self.signup_validate(customer)

        # Saving
        if not error_message:
            print(first_name, last_name, phone, email, password)
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('homepage')

        else:
            data = {
                'error': error_message,
                'values': value
            }
        return render(request, 'signup.html', data)

    # Signup Validate
    def signup_validate(self, customer):
        error_message = None

        if not customer.first_name:
            error_message = 'First Name Required..'
        elif not customer.last_name:
            error_message = 'Last Name Required..'
        elif not customer.phone:
            error_message = 'Mobile Number Required..'
        elif len(customer.phone) < 10 or len(customer.phone) > 10:
            error_message = 'Not a valid Mobile Number..'
        elif not customer.email:
            error_message = 'Email Required..'
        elif not customer.password:
            error_message = 'Password Required..'
        elif len(customer.password) < 6:
            error_message = 'Password should be atleast 6 characters..'
        elif customer.isExists():
            error_message = 'Email address already used..'

        return error_message
