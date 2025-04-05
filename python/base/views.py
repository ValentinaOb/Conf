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
from django.core.mail import send_mail
from datetime import datetime

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
    one_data = Review_Work.objects.values('work_id', 'user_id')
    # Створюємо словник work_id: [lastnames]
    works_authors = defaultdict(list)
    for entry in one_data:
        work_id = entry['work_id']
        author_id = entry['user_id']
        works_authors[work_id].append(user_data_dict.get(author_id))

    # Перетворюємо defaultdict у звичайний словник
    works_authors = dict(works_authors)

    '''# Групуємо дані у словник
    works_authors = defaultdict(list)
    for item in data:
        print('r ',item['work__id'])
        works_authors[item['work__id']].append(user_data_dict)

    #
    works_authors = dict(works_authors)

    print('D ',works_authors)'''

    # Формуємо список об'єктів для шаблону
    works_rev_join = []
    available_status=[]
    available_email_status=[]
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
            'email_status':i.email_status,

            #'lastname': user_data_dict.get(i.user_id, ""),
            'send_at': review_work_dict.get(i.user_id, ""),
            'lastname': works_authors.get(i.id, [])
        })
        available_status.append(i.status)
        available_email_status.append(i.email_status)
    available_status=set(available_status)
    available_email_status=set(available_email_status)
    

    # Отримуємо тип, за яким фільтруємо
    work_status = request.GET.get("filter", "")
    selected_email_status = request.GET.get("email_status", "")
    user_role = request.GET.get("role_filter", "")

    # Визначаємо, чи сортуємо за зростанням чи спаданням
    sort_order = request.GET.get("order", "asc")  # За замовчуванням - зростання
    reverse = sort_order == "desc"

    if selected_email_status:
        works_rev_join = [item for item in works_rev_join if item["email_status"] == selected_email_status]

    # Фільтрація за типом
    if work_status:
        works_rev_join = [item for item in works_rev_join if item["status"] == work_status]

    # Сортування за датою
    works_rev_join.sort(key=lambda x: x["uploaded_at"], reverse=reverse)


    #user role
    users_roles= User_Data.objects.values('user_id','firstname','lastname','job','user__user_role__user_role','user__username')
    if user_role:
        users_roles = [item for item in users_roles if item["user__user_role__user_role"] == user_role]

    '''work_status = request.GET.get('filter')
    if work_status:
        works_rev_join = [item for item in works_rev_join if item['status'] == work_status]
    print('j ',works_rev_join)

    sort_param = request.GET.get("sort")
    if sort_param == "date":
        works_rev_join = sorted(works_rev_join, key=lambda x: x["send_at"], reverse=True)'''

    '''queryset=Review_Work.objects.select_related('user').prefetch_related(
    'user__work_set',  
    'user__user_data_set').all()
    works_rev_join = [works_rev(obj.work.category, obj.work.title, obj.work.authors, obj.work.file, 
                            obj.work.file_size, obj.work.uploaded_at, obj.work.status, obj.user, obj.send_at, obj.work_id) for obj in queryset]'''
    
    return render(request, 'base/adm-upload.html', {'reviewers': reviewers,'works_rev_join': works_rev_join,'works_authors': works_authors,
                                                    'available_status':available_status,"work_status": work_status,"selected_order": sort_order, 
                                                    'available_email_status':available_email_status,'selected_email_status':selected_email_status,
                                                    'users_roles':users_roles})

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
    available_status=[]
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
            'email_status':i.email_status,

            'lastname': user_data_dict.get(i.user_id, ""),
            'send_at': review_work_dict.get(i.user_id, ""),
        })
        available_status.append(i.status)
        available_email_status.append(i.email_status)
    available_status=set(available_status)
    available_email_status=set(available_email_status)
    

    # Отримуємо тип, за яким фільтруємо
    work_status = request.GET.get("filter", "")
    selected_email_status = request.GET.get("email_status", "")
    user_role = request.GET.get("role_filter", "")

    # Визначаємо, чи сортуємо за зростанням чи спаданням
    sort_order = request.GET.get("order", "asc")  # За замовчуванням - зростання
    reverse = sort_order == "desc"

    if selected_email_status:
        works_rev_join = [item for item in works_rev_join if item["email_status"] == selected_email_status]

    # Фільтрація за типом
    if work_status:
        works_rev_join = [item for item in works_rev_join if item["status"] == work_status]

    # Сортування за датою
    works_rev_join.sort(key=lambda x: x["uploaded_at"], reverse=reverse)


    users_roles= User_Data.objects.values('user_id','firstname','lastname','job','user__user_role__user_role','user__username')
    if user_role:
        users_roles = [item for item in users_roles if item["user__user_role__user_role"] == user_role]
        
    return render(request, 'base/adm-upload.html', {'reviewers': reviewers,'works_rev_join': works_rev_join,'edit_element': edit_element,
                                                    'available_status': available_status,"work_status": work_status,"selected_order": sort_order,
                                                    'available_email_status':available_email_status,'selected_email_status':selected_email_status,
                                                    'users_roles':users_roles})
#
'''def status_change(request, id):
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
'''
def email_send(request):
    if 'email' in request.POST:
        selected_works = request.POST.getlist('selected_works')
        new_status = request.POST.get('work_status')

        if not selected_works:
            return redirect('admin_home')

        users_works =Work.objects.select_related('user').values('id','title','status', 'user__username', 'user__email').filter(id__in=selected_works)
        print(users_works)
        users_names=[]
        for user_work in users_works:
            works= Work.objects.filter(id = user_work['id'])
            current_work=Review_Work.objects.values('description').filter(work_id=user_work['id'])
            users_names.append(user_work['user__username']+'. ')
            print('h ',current_work, type(current_work))
            for work in works:
                work.status=new_status
                work.email_status='submitted'
                work.save()

            descriptions = "\n".join(i['description'] for i in current_work if i['description'] is not None)

            subject = f"Status Update - {user_work['title']}"
            if new_status=='finalise':
                message=f"Dear {user_work['user__username']}, \n\nYour work '{user_work['title']}' has been "+new_status+"."
                if len(descriptions)!=0:
                    message+="\nFeedbacks: \n"+descriptions
                message+="\n\nPlease, after finalising the work, do not send a new one, but edit this one. Thank you.\n\nSincerely, Administration"
            else:
                message=f"Dear {user_work['user__username']}, \n\nYour work '{user_work['title']}' has been "+new_status +"."
                if len(descriptions)!=0:
                    message+="\nFeedbacks: \n"+descriptions
                message+="\n\nSincerely, Administration"
            
            recipient_email = user_work['user__email']

            send_mail(subject, message, 'your_email@gmail.com', [recipient_email])

            messages.info(request, f"Selected work have been marked as {new_status} and {users_names} have been notified")
            return redirect('admin_home')
    
    elif 'description'in request.POST:
        selected_works = request.POST.getlist('selected_works')
        users_works =Review_Work.objects.select_related('work').values('work__title','status','description','user__user_data__lastname').filter(work_id__in=selected_works)

        if not selected_works:
            return redirect('admin_home')
        
        reviewers_id = User_Role.objects.filter(user_role='reviewer')  
        user_ids = reviewers_id.values_list('user_id', flat=True)  
        reviewers = User.objects.filter(id__in=user_ids)
        work = Work.objects.select_related('user')  
        reviewers_data = User_Data.objects.filter(user_id__in=user_ids)  
        review_work = Review_Work.objects.all()
        user_data_dict = {i.user_id: i.lastname for i in reviewers_data}
        review_work_dict = {i.work_id: i.send_at for i in review_work}

        one_data = Review_Work.objects.values('work_id', 'user_id')
        works_authors = defaultdict(list)
        for entry in one_data:
            work_id = entry['work_id']
            author_id = entry['user_id']
            works_authors[work_id].append(user_data_dict.get(author_id))

        works_authors = dict(works_authors)
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

                'send_at': review_work_dict.get(i.user_id, ""),
                'lastname': works_authors.get(i.id, [])
            })
        
        
        return render(request, 'base/adm-upload.html', {'reviewers': reviewers,'works_rev_join': works_rev_join,'users_works': users_works})
    return redirect('admin_home')

def assign_role(request):
    selected_users = request.POST.getlist('selected_users')
    new_role = request.POST.get('user_role')

    users =User_Role.objects.filter(user_id__in=selected_users)
    for user in users:
        user.user_role=new_role
        user.save()
    return redirect ('admin_home')


def reviewer_home(request):
    #   3 TABLES
    work_id_for_review=[Review_Work.objects.values('work_id').filter(user_id=request.user.id)]  
    work=Work.objects.select_related('user').filter(id__in=work_id_for_review)
    reviewers_data = User_Data.objects.filter(user_id=request.user.id)  
    review_work = Review_Work.objects.filter(user_id=request.user.id)  

    user_data_dict = {i.user_id: i.lastname for i in reviewers_data}
    review_work_dict = {i.work_id: i.send_at for i in review_work}    
    review_work_status_dict = {i.work_id: i.status for i in review_work} 
    
    one_data = Review_Work.objects.values('work_id', 'user_id')
    works_authors = defaultdict(list)
    for entry in one_data:
        work_id = entry['work_id']
        author_id = entry['user_id']
        works_authors[work_id].append(user_data_dict.get(author_id))

    works_authors = dict(works_authors)
    reviewer_tasks = []
    available_status=[]
    for i in work:
        reviewer_tasks.append({
            'id':i.id,
            'category': i.category, 
            'title': i.title,
            'authors': i.authors,
            'file': i.file,
            'file_size': i.file_size,
            'uploaded_at': i.uploaded_at,
            'user':i.user,

            #'lastname': user_data_dict.get(i.user_id, ""),
            'send_at': review_work_dict.get(i.id, ""),
            'lastname': works_authors.get(i.id, []),
            'status': review_work_status_dict.get(i.id, ""),
        })
        
        available_status.append(review_work_status_dict.get(i.id, ""))# Отримуємо унікальні типи для фільтра
    available_status=set(available_status)
    
    
    # Отримуємо тип, за яким фільтруємо
    work_status = request.GET.get("filter", "")

    # Визначаємо, чи сортуємо за зростанням чи спаданням
    sort_order = request.GET.get("order", "asc")  # За замовчуванням - зростання
    reverse = sort_order == "desc"

    # Фільтрація за типом
    if work_status:
        reviewer_tasks = [item for item in reviewer_tasks if item["status"] == work_status]

    # Сортування за датою
    reviewer_tasks.sort(key=lambda x: x["uploaded_at"], reverse=reverse)

    
    '''queryset = Review_Work.objects.select_related('work').all()
    work_ids_list=[]
    
    works_rev_join = [works_rev(obj.work.category, obj.work.title, obj.work.authors, obj.work.file, 
                            obj.work.file_size, obj.work.uploaded_at, obj.work.status, obj.user, obj.send_at, obj.work_id) for obj in queryset]
    print(works_rev_join)
    for i in works_rev_join:    
        if i.users is not None:
            num_list=i.users[1:-1].split(", ") 
            for j in num_list:
                if int(j)==request.user.id:
                    work_ids_list.append(i.title)'''

    #reviewer_tasks=Work.objects.filter(title__in = work_ids_list)
    '''reviewer_list=Work.objects.only('id').filter(title__in = work_ids_list)
    queryset=Review_Work.objects.select_related('work').filter(work_id__in = reviewer_list)
    reviewer_tasks = [works_rev(obj.work.category, obj.work.title, obj.work.authors, obj.work.file, 
                            obj.work.file_size, obj.work.uploaded_at, obj.work.status, obj.user, obj.send_at, obj.work_id) for obj in queryset]'''

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
    
    return render(request, 'base/reviewer_home.html', {'reviewer_tasks':reviewer_tasks,'available_status':available_status,
                                                    "work_status": work_status,"selected_order": sort_order})

def work_status_check(id):
    status_check=Review_Work.objects.values('status').order_by('user_id').filter(work_id=id)
    status_list=[]
    for i in status_check:
        status_list.append(i['status'])
    print('Y ', status_list)
    work= Work.objects.get(id=id)
    if all(i == 'accept' for i in status_list):    
        work.status='accept'
        work.save()
    if 'refuse' in status_list:
        work.status='refuse'
        work.save()
    if 'finalise' in status_list:
        work.status='finalise'
        work.save()        


def review_status(request,id):
    review_element= Work.objects.get(id=id)
    
    if request.method == "POST":
        #works=Work.objects.get(title=request.POST['title'], user_id=request.user.id)

        review_work=Review_Work.objects.get(work_id=id, user_id=request.user.id)
        review_work.status=request.POST['work_status']
        review_work.description=request.POST['feedback']
        review_work.save()
        work_status_check(id)

        messages.success(request, request.POST['title'] +' - '+ review_work.status)
        return redirect('reviewer_home')
    
    '''queryset = Review_Work.objects.select_related('work').all()
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
                        obj.work.file_size, obj.work.uploaded_at, obj.work.status, obj.users, obj.send_at, obj.work_id) for obj in queryset]'''
    #   3 TABLES
    work_id_for_review=[Review_Work.objects.values('work_id').filter(user_id=request.user.id)]  
    work=Work.objects.select_related('user').filter(id__in=work_id_for_review)
    reviewers_data = User_Data.objects.filter(user_id=request.user.id)  
    review_work = Review_Work.objects.filter(user_id=request.user.id)  

    user_data_dict = {i.user_id: i.lastname for i in reviewers_data}
    review_work_dict = {i.work_id: i.send_at for i in review_work}   
    review_work_status_dict = {i.work_id: i.status for i in review_work} 
    
    one_data = Review_Work.objects.values('work_id', 'user_id')
    works_authors = defaultdict(list)
    for entry in one_data:
        work_id = entry['work_id']
        author_id = entry['user_id']
        works_authors[work_id].append(user_data_dict.get(author_id))

    works_authors = dict(works_authors)
    reviewer_tasks = []
    available_status=[]
    for i in work:
        reviewer_tasks.append({
            'id':i.id,
            'category': i.category, 
            'title': i.title,
            'authors': i.authors,
            'file': i.file,
            'file_size': i.file_size,
            'uploaded_at': i.uploaded_at,
            'user':i.user,

            #'lastname': user_data_dict.get(i.user_id, ""),
            'status': review_work_status_dict.get(i.id, ""),
            'send_at': review_work_dict.get(i.id, ""),
            'lastname': works_authors.get(i.id, [])
        })
        available_status.append(review_work_status_dict.get(i.id, ""))# Отримуємо унікальні типи для фільтра
    available_status=set(available_status)
   
    # Отримуємо тип, за яким фільтруємо
    work_status = request.GET.get("filter", "")

    # Визначаємо, чи сортуємо за зростанням чи спаданням
    sort_order = request.GET.get("order", "asc")  # За замовчуванням - зростання
    reverse = sort_order == "desc"

    # Фільтрація за типом
    if work_status:
        reviewer_tasks = [item for item in reviewer_tasks if item["status"] == work_status]

    # Сортування за датою
    reviewer_tasks.sort(key=lambda x: x["uploaded_at"], reverse=reverse)

    return render(request, 'base/reviewer_home.html', {'reviewer_tasks': reviewer_tasks,'review_element': review_element,
                                                       'available_status':available_status, "work_status": work_status,"selected_order": sort_order})

def review_file(request,id):
    '''rewiew_element = Work.objects.get(id=id)
    url = rewiew_element.file.path
    filename = os.path.basename(url)
    response = StreamingHttpResponse(streaming_content=url)
    response['Content-Disposition'] = f'attachement; filename="{filename}"'

    return response'''
    rewiew_element = Work.objects.get(id=id)
    print('j ',rewiew_element.file.path)
    url = rewiew_element.file.path
    try:
        rewiew_element.status='review'
        rewiew_element.save()
        response = FileResponse(open(url, 'rb'), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{rewiew_element.title}"'
        #return FileResponse(open(url, 'rb'), content_type='application/pdf')
        return response
    except FileNotFoundError:
        raise Http404()

def view_description(request):    
    if request.POST:
        selected_works = request.POST.getlist('selected_works')
        print('k ', selected_works)
        users_works =Review_Work.objects.select_related('work').values('work__title','status','description').filter(work_id__in=selected_works, user_id=request.user.id)
        print('h ',users_works)

        if not selected_works:
            return redirect('reviewer_home')
            
        work_id_for_review=[Review_Work.objects.values('work_id').filter(user_id=request.user.id)]  
        work=Work.objects.select_related('user').filter(id__in=work_id_for_review)
        reviewers_data = User_Data.objects.filter(user_id=request.user.id)  
        review_work = Review_Work.objects.filter(user_id=request.user.id)  

        user_data_dict = {i.user_id: i.lastname for i in reviewers_data}
        review_work_dict = {i.work_id: i.send_at for i in review_work}    
        review_work_status_dict = {i.work_id: i.status for i in review_work} 
        
        one_data = Review_Work.objects.values('work_id', 'user_id')
        works_authors = defaultdict(list)
        for entry in one_data:
            work_id = entry['work_id']
            author_id = entry['user_id']
            works_authors[work_id].append(user_data_dict.get(author_id))

        works_authors = dict(works_authors)
        reviewer_tasks = []
        available_status=[]
        for i in work:
            reviewer_tasks.append({
                'id':i.id,
                'category': i.category, 
                'title': i.title,
                'authors': i.authors,
                'file': i.file,
                'file_size': i.file_size,
                'uploaded_at': i.uploaded_at,
                'user':i.user,

                #'lastname': user_data_dict.get(i.user_id, ""),
                'send_at': review_work_dict.get(i.id, ""),
                'lastname': works_authors.get(i.id, []),
                'status': review_work_status_dict.get(i.id, ""),
            })
            available_status.append(review_work_status_dict.get(i.id, ""))# Отримуємо унікальні типи для фільтра
        available_status=set(available_status)
    
            # Отримуємо тип, за яким фільтруємо
        work_status = request.GET.get("filter", "")

        # Визначаємо, чи сортуємо за зростанням чи спаданням
        sort_order = request.GET.get("order", "asc")  # За замовчуванням - зростання
        reverse = sort_order == "desc"

        # Фільтрація за типом
        if work_status:
            reviewer_tasks = [item for item in reviewer_tasks if item["status"] == work_status]

        # Сортування за датою
        reviewer_tasks.sort(key=lambda x: x["uploaded_at"], reverse=reverse)
        
        return render(request, 'base/reviewer_home.html', {'reviewer_tasks':reviewer_tasks, 'users_works': users_works,
                                                           'available_status':available_status, "work_status": work_status,"selected_order": sort_order})

    return redirect('reviewer_home')



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
    if request.user.is_superuser:
        selected_users = request.POST.getlist('selected_users')
        if not selected_users:
            return redirect('admin_home')
        
        usernames=[]
        for i in selected_users:
            users = User.objects.filter(id=i.id)
            users_data = User_Data.objects.filter(id=i.id)
            works = Work.objects.all().filter(user=i)
            users_role=User_Role.objects.filter(id=i.id)
            
            usernames.append(users.username+'. ')
        
            if len(works)!=0:
                for j in works:
                    review_works = Review_Work.objects.all().filter(work_id=j.id)
                    for k in review_works:
                        k.delete()
                    os.remove(str(j.file.path))
                    j.delete()
            for r in users_role:
                r.delete()
            for d in users_data:
                d.delete()
            for user in users:
                user.delete()
        messages.success(request, 'Deactivate '+usernames)
        return redirect('admin_home')
    
    else:
        user = User.objects.get(id=request.user.id)
        user_data = User_Data.objects.get(id=request.user.id)
        works = Work.objects.all().filter(user=request.user)
        user_role=User_Role.objects.get(id=request.user.id)
        
        if len(works)!=0:
            for j in works:
                review_works = Review_Work.objects.all().filter(work_id=j.id)
                for k in review_works:
                    k.delete()
                os.remove(str(j.file.path))
                j.delete()
        user.delete()
        user_role.delete()
        user_data.delete()
    
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
            # Забороняємо користувачу редагувати, якщо робота вже на перевірці
            if obj.status=='review':
                return redirect('home')

            file = request.FILES.get('file', edit_element.file)
            print(file)
            category = request.POST.get('category', edit_element.category)
            title = request.POST.get('title', edit_element.title)
            authors = request.POST.get('authors', edit_element.authors)
        
            obj.category = category
            obj.file = file
            obj.title = title
            obj.authors = authors
            obj.email_status='unsubmitted'
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


