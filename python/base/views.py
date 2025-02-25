from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Work, UploadWorkForm, User_Data, UploadUserDataForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import update_session_auth_hash
import os
from django.contrib import auth
from django.contrib.auth.forms import PasswordChangeForm
import phonenumbers
from phonenumber_field.phonenumber import PhoneNumber
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_view(request):
    return render(request, 'adm-upload.html')

@csrf_exempt
def home(request):
    if request.user.is_superuser:
        return render(request, "base/adm-upload.html", {'user_data': user_data})
    
    print(request.user)
    user_data=User_Data.objects.get(user=request.user)
    return render(request, "base/home.html", {'user_data': user_data})

def user_profile(request):
    print(request.user)
    works=Work.objects.all().filter(user=request.user)
    user_data=User_Data.objects.get(user=request.user)
    print(user_data.avatar)
    print(user_data.firstname)
    return render(request, "base/user_profile.html", {'works': works, 'user_data': user_data})

def edit_profile(request):
    user_data=User_Data.objects.get(user=request.user)
    print(request.FILES.get('avatar'))    #default delete

    if request.method == "POST":
        User_Data.objects.get(user=request.user).delete()
        '''user_data.firstname=request.POST.get('firstname',''),
        user_data.lastname=request.POST.get('lastname',''),
        user_data.phone = PhoneNumber.from_string(request.POST.get("phone", "").strip(), region='US')
        user_data.avatar=request.FILES.get('avatar'),
        user_data.country=request.POST.get('country'),
        user_data.language=request.POST.get('language'),
        user_data.user=request.user
        print(user_data.firstname,user_data.lastname, user_data.phone)
        user_data.save()'''
        User_Data.objects.create(
            firstname=request.POST['firstname'],
            lastname=request.POST['lastname'],
            phone=request.POST['phone'],
            job=request.POST['job'],
            avatar=request.FILES.get('avatar'),
            country=request.POST['country'],
            language=request.POST['language'],
            user=request.user
        )
        print(request.FILES.get('avatar'))

        if request.POST['email'] !=request.user.email :
            obj = User.objects.get(id=request.user.id)
            obj.email=request.POST['email']
            obj.save()
        if request.POST['username']:
            obj = User.objects.get(id=request.user.id)
            obj.username=request.POST['username']
            obj.save()

        return redirect('home')

    '''form = UploadUserDataForm(request.user, request.POST)
        if form.is_valid():
            print("Valid")
            form.save()'''

    return render(request,"base/edit_profile.html",{'user_data':user_data, 'form': UploadUserDataForm})

@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        #print(form.is_valid)

        if form.is_valid():
            form.save()  # Save new password
            update_session_auth_hash(request, form.user)  # Keep user logged in
            messages.success(request, "✅ Password changed successfully!")
            return redirect("edit_profile")  
        else:
            messages.error(request, "❌ Current password is incorrect or new passwords do not match.")
            print("Form errors:", form.errors)

    return render(request,"base/change_password.html")

'''def forgot_pswd(request):
    if request.method == "POST":
        print("N")                      #!!!!!!!!!!!
        return redirect("sign")  
    return render(request,"base/forgot_password.html")
'''

def deactivate_account(request):
    print(request.user)
    obj = User.objects.get(id=request.user.id)
    works = Work.objects.all().filter(user=request.user)
    if len(works)!=0:
        os.remove(str(works.file.path))
        works.delete()
    obj.delete()
    return redirect('base')

def upload(request): 
    #print("ID: ",request.user.id)
    if request.user.is_superuser:
        user_data=User_Data.objects
        return render(request, "base/upload.html", {'user_data': user_data})
    
    if request.method == "POST":
        Work.objects.create(
                category=request.POST['category'],
                title=request.POST['title'],
                authors=request.POST['authors'],
                file=request.FILES['file'],
                file_size=request.FILES['file'].size,
                status='sent',
                user=request.user
        )
        '''form = UploadWorkForm(request.POST, request.FILES) # , request.user, request.FILES.size       as 'file_size')
        print("W:", work)
        if form.is_valid():
            print("Valid")
            form.save()'''

    works=Work.objects.all().filter(user=request.user)
    user_data=User_Data.objects.get(user=request.user)
    
    return render(request, "base/upload.html", {'form': UploadWorkForm, 'works': works, 'user_data': user_data})          #base/upload.html

def update(request, id):
    edit_element = Work.objects.get(id=id)
    works=Work.objects.all().filter(user=request.user)
    obj = Work.objects.get(id=id)
    print("hee")

    if "updaterecord" in request.POST:
        file = request.FILES.get('file', edit_element.file)
        print(file)
        category = request.POST.get('category', edit_element.category)
        title = request.POST.get('title', edit_element.title)
        authors = request.POST.get('authors', edit_element.authors)
        
        obj.category = category
        obj.file = file
        obj.title = title
        obj.authors = authors
        obj.save()
        return redirect('upload')

    return render(request, 'base/upload.html', {'edit_element': edit_element, 'works': works})

def delete(request, id):
    obj = Work.objects.get(id=id)
    obj.delete()
    os.remove(str(obj.file.path))
    print("Yes!")
    return redirect('upload') 
        



@csrf_exempt

def base(request):
    context={}
    return render(request, 'base/index.html', context)

def about(request):
    if not request.user.is_anonymous:
        user_data=User_Data.objects.get(user=request.user)
        return render(request, 'base/about-us.html', {'user_data': user_data})
    
    return render(request, 'base/about-us.html')
    

def contact(request):
    if not request.user.is_anonymous:
        user_data=User_Data.objects.get(user=request.user)
        return render(request, 'base/contact.html', {'user_data': user_data})
    
    return render(request, 'base/contact.html')

def schedule(request):
    if not request.user.is_anonymous:
        user_data=User_Data.objects.get(user=request.user)
        return render(request, 'base/schedule.html', {'user_data': user_data})
    
    return render(request, 'base/schedule.html')

def committee(request):
    if not request.user.is_anonymous:
        user_data=User_Data.objects.get(user=request.user)
        return render(request, 'base/committee.html', {'user_data': user_data})
    
    return render(request, 'base/committee.html')


def sign(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        if "register" in request.POST:  # Registration
            if User.objects.filter(email=email).exists():
                messages.error(request, "An account with this email already exists.")
            elif User.objects.filter(username=username).exists():
                messages.error(request, "This username is already taken.")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, "Registration successful! Please log in.")
                user = authenticate(request, username=email, password=password)
                user_data = User_Data.objects.create(user=user)
                user_data.save()

                login(request, user)
                return redirect('home')

        elif "login" in request.POST:  # Login
            user = authenticate(request, username=email, password=password)  # Login using email
            if user is not None:
                login(request, user)
                messages.success(request, "Successfully logged in!")
                return redirect('home')
            else:
                messages.error(request, "Invalid email or password!")
                
    return render(request, "base/sign.html")

def logout(request):
    auth.logout(request)
    messages.success(request,"Logout")
    return redirect('base')


