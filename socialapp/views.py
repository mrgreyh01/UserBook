from django.shortcuts import render,redirect

from socialapp.models import Users
from django.db import connection

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.utils import DatabaseError,IntegrityError
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Users,Posts
from .serializers import UserSerializer
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib import messages
from validate_email import validate_email
from rest_framework import serializers 

# Create your views here.

def home(request):
    if request.session.has_key('Username'):
        return redirect('/api/dash')
    return render(request, 'home.html')

def login(request):
    if request.session.has_key('Username'):
        return redirect('/api/dash')
    return render(request,'login.html')


def auth(request):
    # if request.session.has_key('Username'):
    #     return redirect('/api/dash')
    if request.method == 'POST':
        u_name = request.POST["mobile"]
        u_pswd = request.POST["password"]

        found=Users.objects.filter(mobile=u_name,password=u_pswd).exists()
        usr = Users.objects.get(mobile=u_name)



        if found==True:
            # userobj = Users.objects.get(mobile=u_name)
            # print("Hello My Name is ",userobj)
            request.session['Username'] = u_name
            request.session['id'] = usr.my_id
            request.session['name'] = usr.name


            # print("The Name of the user : ",usr.name )


            # request.session['Name'] = userobj
            return redirect('/api/dash')
        else:
            messages.error(request,'username or password is incorrect')
            return redirect('/api/login')
    else:
        return redirect('/api/login')


    # check_if_user_exists = Users.objects.filter(mobile=u_name).exists()

    # if check_if_user_exists:

    #     user = authenticate(request, username=u_name, password=u_pswd)

    #     if user is not None:
    #         request.session['Username'] = u_name
    #         return redirect('/api/dash')
    #     else:
    #         # return JsonResponse({"Warning":"Password is incorrect"})
    #         messages.error(request,'username or password is incorrect')
    #         return redirect('/api/login')

    # else:
    #     # return redirect('/api/login')
    #     return JsonResponse({"error":"err"})

def posts(request):
    return render(request,"post.html")

def logout(request):
    request.session.flush();
    return redirect('/api/login');

def feed(request):
    id = request.session['id'];
    post = Posts.objects.exclude(u_id=id)
    # print(post.desc);
    return render(request,"feed.html",{'post':post})

def register(request):
    if request.session.has_key('Username'):
        return redirect('/api/dash')
    return render(request,"signup.html")

@api_view(['POST'])
def createUser(request):

    serializer =  UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return redirect('/api/login')

    print(serializer.errors)
    return redirect('/api/signup')
    
    # if request.method == 'POST':
    #     name = request.POST.get('name')
    #     mobile = request.POST.get('mobile')
    #     email = request.POST.get('email')
    #     password = request.POST.get('password')

    #     print("Name: ",name)
        
    #     # try:
    #     #     user = Users.objects.get(mobile=mobile)
    #     #     print("User: ",user)
    #     #     return JsonResponse({'status': 'error', 'message': 'User already exists'})
    #     # except IntegrityError:
    #     #     user = Users.objects.create(name=name, mobile=mobile, email=email, password=password)
    #     #     user.save()
    #     #     return JsonResponse({'status': 'success', 'message': 'User created successfully'})
    #     Users(mobile = mobile, email = email, password = password,name = name, ).save()
    #     return JsonResponse({'foo': 'bar'})


    # else:
    #     return JsonResponse({'error': 'err'})


def dash(request):
    uid = request.session['id']
    name = request.session['name']
    print("The ID of the user : ",uid )

    return render(request,'dash.html',{'name':name})

def myprofile(request):
    uid = request.session['id']
    user = Users.objects.get(my_id=uid)

    return render(request,"myprofile.html",{'user':user})

def profile(request):
    return render(request, 'profile.html')

def post(request):
    return render(request, 'post.html')

@csrf_exempt
def search(request):
    data = request.POST['data']
    is_valid = validate_email(data)

    if data.isdigit():
        # res = Users.objects.filter(mobile=data)
        with connection.cursor() as cursor:
            cursor.execute('select name from register where mobile=%s',[data]);
            tbldata = dictfetchall(cursor);
            print("Under digit",tbldata)
        return JsonResponse(tbldata,safe=False)
    elif is_valid:
        with connection.cursor() as cursor:
            cursor.execute('select name from register where email=%s',[data]);
            tbldata = dictfetchall(cursor);
            print("under email",tbldata)

        return JsonResponse(tbldata,safe=False)

    else:
        # with connection.cursor() as cursor:
            # cursor.execute('select name from register where name like %s',[data]);
            # tbldata = dictfetchall(cursor);
            # print("under name",tbldata)
        
        # SomeModel_json = UserSerializer(Users.objects.filter(name__icontains=data))
        # m_data = {"name": SomeModel_json}

        tbldata = Users.objects.filter(name__icontains=data).values('name')
        # m_data = {"name": list(tbldata)}
        m_data = list(tbldata)
        
        return JsonResponse(m_data,safe=False)


# @csrf_exempt
def create_post(request):
    # mobile = request.session['Username'];
    # cursor = connection.cursor()
    # cursor.execute("SELECT my_id,name FROM register WHERE mobile = %s",[mobile])
    # # cursor.execute("SELECT my_id,name FROM register WHERE mobile = 7869503474")

    # tbldata = dictfetchall(cursor)

    # for data in tbldata:
    #     u_id = data['my_id']
    #     name = data['name']

    u_id = request.session['id']
    name = request.session['name']
    
    desc = request.POST['desc']
    # img = request.FILES.getlist('uploadFromPC')
    img = request.FILES['uploadFromPC']


    print(desc);

    try:
        Posts(u_id=u_id,name=name,desc=desc,image=img).save()
    except:
        return redirect("/api/posts")

    return redirect("/api/vposts")

def view_post(request):
    id = request.session['id']
    list = Posts.objects.filter(u_id=id).first()
    print("List:",list)
    if list is not None:
        post = Posts.objects.filter(u_id=id)

        if post is not None:
            print("I am under view post ...")
            return render(request,'myposts.html',{'post':post})
    
        else:
            return JsonResponse({"Error":"err"})

    else:
        return HttpResponse("No posts exists")

def edit_post(request,pk):
    post = Posts.objects.get(my_id=pk)
    return render(request,"update-post.html",{'post':post}) 

def update_post(request):
    # id = request.session['id']
    myid = request.POST['my_id']
    desc = request.POST['desc']
    img = request.FILES['uploadFromPC']

    print(desc);

    post = Posts.objects.get(my_id=myid)

    post.desc = desc
    post.image = img

    try:
        post.save()
    except:
        return redirect("/api/upost")

    return redirect("/api/vpost")

    # Posts.objects.filter(pk=some_value).update(field1='some value')

def delete_post(request,pk):
    try:
        Posts.objects.get(pk=pk).delete()
    except:
        return HttpResponse("Post is not deleted!!")

    return redirect("/api/vpost")


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

# def auth(request):
    
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']
       
#         # if email == ''


#     else:
#         return render(request, 'login.html')