from django.shortcuts import render, redirect , HttpResponseRedirect
from django.http import HttpResponse
from Store.models.customer import Customer
from django.contrib.auth.hashers import check_password
from django.views import View


# Login Class
class Login(View):
    return_url = None
    def get(self,request):
      #  request.session['cart'] = {}
        Login.return_url = request.GET.get('return_url')
        return render(request, 'login.html')

    def post(self,request):
        # Login verification
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('first_name')
        customer = Customer.get_customer_by_email(email)
        print(request.POST)

        error_message = None
        if customer:
            request.session['customer'] = customer.id
            request.session['email'] = customer.email
            flag = check_password(password, customer.password)
            if flag:
                request.session['cart'] = {}
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('homepage')
            else:
                error_message = 'Email or Password Invalid..!'
        else:
            error_message = 'Email or Password Invalid..!'
        return render(request, 'login.html', {'error': error_message})

#Logout function
def logout(request):
    request.session.clear()
    request.session['cart'] = {}
    return redirect('login')