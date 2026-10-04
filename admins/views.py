from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from admins.models import RegisterUserTable
import os

# Create your views here.


#---------------------------------------------------------------------------------------------------------------

def AdminHomePage(request):
    return render(request, 'admins/AdminHome.html')

#-----------------------------------------------------------------------------------------------------------

def MainBasePage(request):
    return render(request, 'base/base.html')

#----------------------------------------------------------------------------

def AdminLogin(request):
    if request.method == 'POST':
        usrid = request.POST.get('username')
        pswd = request.POST.get('password')
        print("User ID is = ", usrid)
        if usrid == os.getenv('ADMIN_USERNAME') and pswd == os.getenv('ADMIN_PASSWORD'):
            return render(request, 'admins/AdminHome.html')
        else:
            messages.success(request, 'Please Check Your Login Details')
    return render(request, 'admins/login.html')

#----------------------------------------------------------------------------

def UserLoginPage(request):
    if request.method =='POST':
        username = request.POST['username']
        pswd = request.POST['password']
        try:
             user = RegisterUserTable.objects.get(username=username, password=pswd)
             if user.is_active:
                 return redirect('user-home')
             else:
                 messages.error(request, 'Your Account is not Activate, Please Activate and Try again.')
        except RegisterUserTable.DoesNotExist:
            messages.error(request, 'Invalid username or password.')         
    return render(request, 'users/login.html')

#-----------------------------------------------------------------------------

def RegisterUserPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        pswd = request.POST['password']
        address = request.POST['address']

        if RegisterUserTable.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif RegisterUserTable.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
        else:
            users = RegisterUserTable.objects.create(
                username=username,
                email=email,
                password=pswd,
                address=address,
            )
            users.save()
            messages.success(request, 'User Registered Successfully.')

        return redirect('user-register')  

    return render(request, 'users/register.html')

#--------------------------------------------------------------------------------

def ViewUsersPage(request):
    users = RegisterUserTable.objects.all()
    return render(request, 'admins/viewusers.html',{'users':users})

#---------------------------------------------------------------------------------


def UserActivateFunction(request, pk):
    user = get_object_or_404(RegisterUserTable, id=pk)
    user.is_active = True
    user.save()      
    return redirect(ViewUsersPage)

# ---------------------------------------------------------------------------------

def UserDeactivateFunction(request, pk):
    user = get_object_or_404(RegisterUserTable, id=pk)
    user.is_active = False
    user.save()      
    return redirect(ViewUsersPage)

#------------------------------------------------------------------------------------------