from django.shortcuts import render, redirect
from . import models
from . import form
# Create your views here.
def index(request):
    if not request.session.get('is_login',None):
        return redirect('/index/')
    return render(request, 'login/index.html')


def login(request):
    if request.session.get('is_login',None):
        return redirect('/index/')
    if request.method == 'POST':
        login_form = form.UserForm(request.POST)
        message = '请假查填写的内容'
        if login_form.is_valid():
            try:
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = models.User.objects.get(name=username)
                print(user)
            except Exception as e:
                message = '用户不存在'
                return render(request, 'login/login.html',{'message':message})
            if password == user.password:
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/index/')
            else:
                message = '密码不正确'
                return render(request, 'login/login.html',locals())
        else:
            return render(request,'login/login.html',locals())
    login_form = form.UserForm()
    return render(request, 'login/login.html',locals())


def logout(request):
    if not request.session.get('is_login',None):
        return redirect('/login/')
    request.session.flush()
    return redirect('/login/')


def register(request):
    if request.method == 'POST':
        register_form = form.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')

            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'login/register.html', locals())

                new_user = models.User()
                new_user.name = username
                new_user.password = password1
                new_user.email = email
                new_user.sex = sex
                new_user.save()

                return redirect('/login/')
        else:
            return render(request, 'login/register.html', locals())
    register_form = form.RegisterForm()
    return render(request, 'login/register.html',locals())
