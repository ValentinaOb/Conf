from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.http import FileResponse, Http404, HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Work, UploadWorkForm, User_Data, UploadUserDataForm, Review_Work, User_Role, Review_Work
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import update_session_auth_hash
import os
from django.contrib import auth
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.admin.views.decorators import staff_member_required
from collections import namedtuple
from itertools import chain
from collections import defaultdict


works_rev = namedtuple('Three', ['category', 'title', 'authors','file','file_size','uploaded_at','status', 'users','send_at','work_id'])

@staff_member_required
def admin_home(request):

    #usernames of reviewers
    reviewers_id = User_Role.objects.filter(user_role='reviewer')  
    user_ids = reviewers_id.values_list('user_id', flat=True)  
    reviewers = User.objects.filter(id__in=user_ids)  


    '''rev_works_id = Review_Work.objects.all()
    rev_works_ids = rev_works_id.values_list('user_id', flat=True)  
    
    rev_works = User.objects.filter(id__in=rev_works_ids) '''
    
    #
    #rev_works_id = Review_Work.objects.all()
    '''rev_works_ids = rev_works_id.values_list('user_id', flat=True)  


    #users_dict = {user.id: user for user in User.objects.filter(id__in=[x for x in rev_works_id if x is not None])}  
    #rev_works = [users_dict.get(uid, None) for uid in rev_works_id]
    rev_works = User.objects.filter(id__in=rev_works_ids).exclude(None)'''

    '''rev_works_id = Review_Work.objects.values('send_at', 'users').annotate(
    category=Value(None, output_field=TextField()), 
    title=Value(None, output_field=CharField()), 
    authors=Value(None, output_field=TextField()), 
    file=Value(None, output_field=FileField()), 
    file_size=Value(None, output_field=IntegerField()), 
    uploaded_at=Value(None, output_field=DateTimeField()),
    status=Value(None, output_field=CharField()),
    source=Value('Review_Work', output_field=CharField()))

    works = Work.objects.values('category', 'title', 'authors','file','file_size','uploaded_at','status').annotate(
    send_at=Value(None, output_field=DateTimeField()), 
    users=Value(None, output_field=TextField()),
    source=Value('Work', output_field=CharField())  # Додаємо джерело
    )
    works_rev_union = works.union(rev_works_id)
    print('R: ',works_rev_union)'''

    #works_rev_join = Work.objects.select_related('review_work').values('category', 'title', 'authors','file','file_size','uploaded_at','status' 'review_work__users','review_work__send_at')
    #works_rev_join = Review_Work.objects.select_related('work').all() 


    '''
    queryset = Review_Work.objects.select_related('work').all()
    
    works_rev_join = [works_rev(obj.work.category, obj.work.title, obj.work.authors, obj.work.file, 
                            obj.work.file_size, obj.work.uploaded_at, obj.work.status, obj.user, obj.send_at, obj.work_id) for obj in queryset]'''

    #
    '''
    rev_works_ids = list(rev_works_id.values_list('users', flat=True))  
    processed_ids = []

    print('A: ',rev_works_ids)
    for i in rev_works_id:        
        if i.users is None:
            processed_ids.append(None)  # Залишаємо None
        elif isinstance(i.users, str) and i.users.startswith("[") and i.users.endswith("]"):
            i.users = i.users[1:-1]  # Прибираємо квадратні дужки
            number_list = i.users.split(",")  # Розбиваємо по комі
            for num in number_list:
                num = num.strip()  # Видаляємо пробіли
                if num.isdigit():  # Перевіряємо, чи це число
                    processed_ids.append(int(num))
                else:
                    processed_ids.append(None)  # Якщо це список, додаємо всі елементи списку
        else:
            processed_ids.append(i.users)  # Якщо це одиночне число, додаємо його як є
    print('F: ',processed_ids)

    data_dict = {obj.id: obj.username for obj in User.objects.filter(id__in=[x for x in processed_ids if x is not None])}
    #rev_works = [data_dict.get(i, None) for i in processed_ids]
    rev_works = []

    for item in rev_works_ids:
        if item is None:
            rev_works.append(None)
        elif item.startswith("[") and item.endswith("]"):
            numbers = item[1:-1].split(", ")
            rev_works.append([data_dict.get(int(num), None) for num in numbers])
        else:
            rev_works.append(data_dict.get(int(item), None))
            
    #rev_works_list = [data_dict.get(aid, None) for aid in rev_works_ids]
    #rev_works = zip(rev_works_id, rev_works_list) 
    
    print(data_dict)
    print(rev_works)
    print('I: ',type(rev_works))'''
    
    '''for i in rev_works_ids:
        print('I: ',i)
        if i ==None:
            i="-"'''
    #
    '''queryset=Review_Work.objects.select_related('user').prefetch_related(
    'user__work_set',  
    'user__user_data_set').all()
    works_rev_join = [works_rev(obj.user.work_set.category, obj.user.work_set.title, obj.user.work_set.authors, obj.user.work_set.file, 
                            obj.user.work_set.file_size, obj.user.work_set.uploaded_at, obj.user.work_set.status, obj.user, obj.send_at, obj.work_id,obj.user.user_data_set.lastname) for obj in queryset]
    '''
    '''work = Work.objects.select_related('user').values('category', 'title','authors','file','file_size','uploaded_at','status','user')
    user_data = User_Data.objects.select_related('user').values('lastname')
    review_work = Review_Work.objects.select_related('user').values('send_at', 'work_id')

    works_rev_join = list(chain(work, user_data, review_work))'''
    
    #   3 TABLES
    work = Work.objects.select_related('user')  # Отримуємо всі `Two` з `One`
    reviewers_data = User_Data.objects.filter(user_id__in=user_ids)  
    review_work = Review_Work.objects.all()

    # Створюємо словник для швидкого доступу до three і four за one_id
    user_data_dict = {i.user_id: i.lastname for i in reviewers_data}
    review_work_dict = {i.work_id: i.send_at for i in review_work}
    #print('d ',user_data_dict)


    # 
    data = User.objects.values('work__id')

    one_data = Review_Work.objects.values('work_id', 'user_id')
    # Створюємо словник book_id: [lastnames]
    books_authors = defaultdict(list)
    for entry in one_data:
        book_id = entry['work_id']
        author_id = entry['user_id']
        books_authors[book_id].append(user_data_dict.get(author_id))

    # Перетворюємо defaultdict у звичайний словник
    books_authors = dict(books_authors)
    print('L ',books_authors)

    '''# Групуємо дані у словник
    books_authors = defaultdict(list)
    for item in data:
        print('r ',item['work__id'])
        books_authors[item['work__id']].append(user_data_dict)

    #
    books_authors = dict(books_authors)

    print('D ',books_authors)'''

    # Формуємо список об'єктів для шаблону
    works_rev_join = []
    for i in work:
        works_rev_join.append({
            'id':i.id,
            'category': i.category, 
            'title': i.title,
            'authors': i.authors,
            'file': i.file,
            'file_size': i.file_size,
            'uploaded_at': i.uploaded_at,
            'status':i.status,
            'user':i.user,

            #'lastname': user_data_dict.get(i.user_id, ""),
            'send_at': review_work_dict.get(i.user_id, ""),
            'lastname': books_authors.get(i.id, [])
        })
    
    '''queryset=Review_Work.objects.select_related('user').prefetch_related(
    'user__work_set',  
    'user__user_data_set').all()
    works_rev_join = [works_rev(obj.work.category, obj.work.title, obj.work.authors, obj.work.file, 
                            obj.work.file_size, obj.work.uploaded_at, obj.work.status, obj.user, obj.send_at, obj.work_id) for obj in queryset]'''
    for i in works_rev_join:
        print(i)
    
    return render(request, 'base/adm-upload.html', {'reviewers': reviewers,'works_rev_join': works_rev_join,'books_authors': books_authors})

def to_review(request, id):
    edit_element = Work.objects.get(id=id)
    works=Work.objects.all()
    
    if request.method == "POST":
        works=Work.objects.get(title=request.POST['title'])
        #reviewers=User.objects.get(username=request.POST.getlist('reviewer'))

        '''Review_Work.objects.create(
            work=works,
            user=reviewer
        )'''
        #review_work.user=reviewer
        rev_names=request.POST.getlist('reviewer')
        print('re ',rev_names)
        
        for i in rev_names:
            print(i)
            reviewer =User.objects.get(id=i)
            Review_Work.objects.create(
                work=works,
                user=reviewer
            )
            
        '''rev_ids=[]
        rev_objs=[]
        for i in rev_names:
            rev_objs.append(User.objects.get(username=i))
        for i in rev_objs:
            rev_ids.append(i.id)
        review_work.users=(rev_ids)
        review_work.save()'''

        messages.success(request, works.title +' - Successfully submitted for review')
        #messages.success(request, works.title +' - '+ str(rev_names))
        return redirect('admin_home')
    
    '''works=Work.objects.all()
    reviewers_id = User_Role.objects.filter(user_role='reviewer')  
    user_ids = reviewers_id.values_list('user_id', flat=True)  
    reviewers = User.objects.filter(id__in=user_ids)  
    rev_works_id = Review_Work.objects
    rev_works_ids = rev_works_id.values_list('user_id', flat=True)  
    rev_works = User.objects.filter(id__in=rev_works_ids) '''
    print('E: ',edit_element.title)

    #return redirect('admin_home')
    reviewers_id = User_Role.objects.filter(user_role='reviewer')  
    user_ids = reviewers_id.values_list('user_id', flat=True)  
    reviewers = User_Data.objects.filter(user_id__in=user_ids) 
    print('L: ',user_ids, '\nJ ',reviewers)

    '''rev_works_id = Review_Work.objects.all()
    rev_works_ids = rev_works_id.values_list('users', flat=True)  
    rev_works = User.objects.filter(id__in=rev_works_ids) 
    print(rev_works_ids)
    print('D: ',rev_works)'''
    '''queryset = Review_Work.objects.select_related('work').all()
    
    works_rev_join = [works_rev(obj.work.category, obj.work.title, obj.work.authors, obj.work.file, 
                            obj.work.file_size, obj.work.uploaded_at, obj.work.status, obj.user, obj.send_at, obj.work_id) for obj in queryset]
    '''

    
    #       Previous Version !!!
    '''queryset=Review_Work.objects.select_related('user').prefetch_related(
    'user__work_set',  
    'user__user_data_set').all()
    works_rev_join = [works_rev(obj.work.category, obj.work.title, obj.work.authors, obj.work.file, 
                            obj.work.file_size, obj.work.uploaded_at, obj.work.status, obj.user, obj.send_at, obj.work_id,obj.user_data.lastname) for obj in queryset]'''
    
    work = Work.objects.select_related('user')  # Отримуємо всі `Two` з `One`
    user_data = User_Data.objects.all()
    review_work = Review_Work.objects.all()

    # Створюємо словник для швидкого доступу до three і four за one_id
    user_data_dict = {i.user_id: i.lastname for i in user_data}
    review_work_dict = {i.user_id: i.send_at for i in review_work}

    # Формуємо список об'єктів для шаблону
    works_rev_join = []
    for i in work:
        works_rev_join.append({
            'id':i.id,
            'category': i.category, 
            'title': i.title,
            'authors': i.authors,
            'file': i.file,
            'file_size': i.file_size,
            'uploaded_at': i.uploaded_at,
            'status':i.status,
            'user':i.user,

            'lastname': user_data_dict.get(i.user_id, ""),
            'send_at': review_work_dict.get(i.user_id, ""),
        })
    
    return render(request, 'base/adm-upload.html', {'reviewers': reviewers,'works_rev_join': works_rev_join,'edit_element': edit_element})

def status_change(request, id):
    edit_element = Work.objects.get(id=id)
    
    if request.method == "POST":
        works=Work.objects.get(title=request.POST['title'])
        if request.POST['status'] == 'accept':
            accept_work()
        else:
            refuse_work()

        return redirect('admin_home')
    
    reviewers_id = User_Role.objects.filter(user_role='reviewer')  
    user_ids = reviewers_id.values_list('user_id', flat=True)  
    reviewers = User.objects.filter(id__in=user_ids)  

    queryset = Review_Work.objects.select_related('work').all()
    
    works_rev_join = [works_rev(obj.work.category, obj.work.title, obj.work.authors, obj.work.file, 
                            obj.work.file_size, obj.work.uploaded_at, obj.work.status, obj.users, obj.send_at, obj.id) for obj in queryset]

    return render(request, 'base/adm-upload.html', {'reviewers': reviewers,'works_rev_join': works_rev_join,'edit_element': edit_element})



def reviewer_home(request):
    queryset = Review_Work.objects.select_related('work').all()
    work_ids_list=[]
    
    works_rev_join = [works_rev(obj.work.category, obj.work.title, obj.work.authors, obj.work.file, 
                            obj.work.file_size, obj.work.uploaded_at, obj.work.status, obj.user, obj.send_at, obj.work_id) for obj in queryset]
    for i in works_rev_join:
        if i.users is not None:
            num_list=i.users[1:-1].split(", ") 
            for j in num_list:
                if int(j)==request.user.id:
                    work_ids_list.append(i.title)

    #reviewer_tasks=Work.objects.filter(title__in = work_ids_list)
    reviewer_list=Work.objects.only('id').filter(title__in = work_ids_list)
    queryset=Review_Work.objects.select_related('work').filter(work_id__in = reviewer_list)
    reviewer_tasks = [works_rev(obj.work.category, obj.work.title, obj.work.authors, obj.work.file, 
                            obj.work.file_size, obj.work.uploaded_at, obj.work.status, obj.user, obj.send_at, obj.work_id) for obj in queryset]

    '''reviewers_id=Review_Work.objects.values_list('users', flat=True)
    print(reviewers_id)
    
    authors_ids_list=[]
    for i in reviewers_id:
        if i is None:
            authors_ids_list.append(None)
        elif isinstance(i, str):
            i= i[1:-1]
            number_list = i.split(", ")
            for num in number_list:
                num = num.strip()
                authors_ids_list.append(num)
        else:
            authors_ids_list.append(i)  # Якщо це одиночне число, додаємо його як є
        print(i)
        print('L; ',authors_ids_list)
        
    print('JL ', authors_ids_list)
    work_for_review=Review_Work.objects.values_list('work_id', flat=True).filter(user_id=request.user.id)'''
    #reviewer_tasks=Review_Work.objects.values_list('send_at', flat=True).filter(work_id=work_for_review)
    '''
    queryset = Review_Work.objects.select_related('work').filter(id__in=work_for_review)
    
    reviewer_tasks = [works_rev(obj.work.category, obj.work.title, obj.work.authors, obj.work.file, 
                            obj.work.file_size, obj.work.uploaded_at, obj.work.status, obj.users, obj.send_at) for obj in queryset]

    
    print(reviewer_tasks.values_list('send_at', flat=True)) '''
    
    return render(request, 'base/reviewer_home.html', {'reviewer_tasks':reviewer_tasks})


def review_status(request,id):
    review_element= Work.objects.get(id=id)
    
    if request.method == "POST":
        works=Work.objects.get(title=request.POST['title'])
        work_status=User.objects.get(username=request.POST['work_status'])

        review_work=Work.objects.get(work=works)
        review_work.status=work_status
        review_work.save()

        feedback=request.POST['feedback']

        messages.success(request, works.title +' - '+ review_work.status)
        print(works,review_work.status)
        return redirect('reviewer_home')
    
    queryset = Review_Work.objects.select_related('work').all()
    work_ids_list=[]
    
    works_rev_join = [works_rev(obj.work.category, obj.work.title, obj.work.authors, obj.work.file, 
                            obj.work.file_size, obj.work.uploaded_at, obj.work.status, obj.user, obj.send_at, obj.id) for obj in queryset]
    for i in works_rev_join:
        if i.users is not None:
            num_list=i.users[1:-1].split(", ") 
            for j in num_list:
                if int(j)==request.user.id:
                    work_ids_list.append(i.title)
    reviewer_list=Work.objects.only('id').filter(title__in = work_ids_list)
    queryset=Review_Work.objects.select_related('work').filter(work_id__in = reviewer_list)
    reviewer_tasks = [works_rev(obj.work.category, obj.work.title, obj.work.authors, obj.work.file, 
                        obj.work.file_size, obj.work.uploaded_at, obj.work.status, obj.users, obj.send_at, obj.work_id) for obj in queryset]
   
    return render(request, 'base/reviewer_home.html', {'reviewer_tasks': reviewer_tasks,'review_element': review_element})

def review_file(request,id):
    '''rewiew_element = Work.objects.get(id=id)
    url = rewiew_element.file.path
    filename = os.path.basename(url)
    response = StreamingHttpResponse(streaming_content=url)
    response['Content-Disposition'] = f'attachement; filename="{filename}"'

    return response'''
    rewiew_element = Work.objects.get(id=id)
    url = rewiew_element.file.path
    try:
        return FileResponse(open(url, 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()


@csrf_exempt
def home(request):
    '''if request.user.is_superuser:
        return redirect('admin_view')'''
    
    print(request.user)
    user_data=User_Data.objects.get(user=request.user)
    #return render(request, "base/home.html", {'user_data': user_data})

    works=Work.objects.all().filter(user=request.user)
    return render(request, "base/home.html", {'form': UploadWorkForm, 'works': works, 'user_data': user_data})

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
    
    try:
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

            messages.success(request, request.user.username+', Update Changes')

            reviewers_id = User_Role.objects.filter(user_role='reviewer')  
            user_ids = reviewers_id.values_list('user_id', flat=True)  
            reviewers = User.objects.filter(id__in=user_ids)
        
            if request.user.is_superuser:
                return redirect('admin_home')
            elif request.user in reviewers:
                return redirect('reviewer_home')

            return redirect('home')

        '''form = UploadUserDataForm(request.user, request.POST)
            if form.is_valid():
                print("Valid")
                form.save()'''
    except Exception as e:
        messages.error(request, "Error: ",repr(e))

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
    try:
        #print("ID: ",request.user.id)
        if request.user.is_superuser:
            user_data=User_Data.objects
            return render(request, "base/upload.html", {'user_data': user_data})
    
        if request.method == "POST":
            works = Work.objects.create(
                    category=request.POST['category'],
                    title=request.POST['title'],
                    authors=request.POST['authors'],
                    file=request.FILES['file'],
                    file_size=request.FILES['file'].size,
                    status='sent',
                    user=request.user
            )
            messages.success(request, 'Upload '+request.POST['title'])
            #Review_Work.objects.create(work=works)
            '''form = UploadWorkForm(request.POST, request.FILES) # , request.user, request.FILES.size       as 'file_size')
        print("W:", work)
        if form.is_valid():
            print("Valid")
            form.save()'''
            
            

    except IntegrityError:
            messages.error(request, "Error: There is a work with this title")
    '''except Exception as e:
        messages.error(request, "Error: ",repr(e))'''
        
    works=Work.objects.all().filter(user=request.user)
    user_data=User_Data.objects.get(user=request.user)


        
    #return render(request, "base/upload.html", {'form': UploadWorkForm, 'works': works, 'user_data': user_data})          #base/upload.html
    #return render(request, 'base/home.html', {'form': UploadWorkForm, 'works': works, 'user_data': user_data})          #base/upload.html
    return redirect('home')

def update(request, id):
    try:
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
            messages.success(request, 'Update '+ obj.title)

            #return redirect('upload')
            return redirect('home')
        
    except Exception as e:
        messages.error(request, "Error: ",repr(e))

    #return render(request, 'base/upload.html', {'edit_element': edit_element, 'works': works})
    return render(request, 'base/home.html', {'edit_element': edit_element, 'works': works})
    #return redirect('home')

def delete(request, id):
    try:
        obj = Work.objects.get(id=id)
        messages.success(request, 'Delete '+obj.title)
        obj.delete()
        os.remove(str(obj.file.path))
        print("Yes!")
    except Exception as e:
        messages.error(request, "Error: ",repr(e))
    #return redirect('upload') 
    return redirect('home') 
        



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
    print('Y')
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        
        #if <button type="submit" id="form-submit-btn" name ="register">Sign Up</button>    do
        #if "register" in request.POST:  # Registration
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "This username is already taken.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Registration successful!")
            user = authenticate(request, username=email, password=password)
            user_data = User_Data.objects.create(user=user, lastname=username)

            user_role = User_Role.objects.create(user=user,user_role='user')
            user_data.save()
            user_role.save()

            login(request, user)
            return redirect('home')
                
    return render(request, "base/sign.html")

def log(request):
    print('L')
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()

        user = authenticate(request, username=email, password=password)  # Login using email
        print('l: ',user)

        reviewers_id = User_Role.objects.filter(user_role='reviewer')  
        user_ids = reviewers_id.values_list('user_id', flat=True)  
        reviewers = User.objects.filter(id__in=user_ids)
        
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_home')
            elif user in reviewers:
                return redirect('reviewer_home')

            
            messages.success(request, "Successfully logged in!")
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password!")
                
    return render(request, "base/login.html")


def logout(request):
    auth.logout(request)
    messages.success(request,"Logout")
    return redirect('base')


