from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
# Create your views here.
from app_login.models import User
import forms   #导入forms表单

def index(request):
    return render(request, 'login/index.html')


def login(request):
    if request.session.get('is_login'):     #不允许重复登陆
        return redirect("/index/")
    if request.method=="POST":   #提交表单后，满足请求为post就执行下面的内容
        message = '所有字段都必须填写'
        login_form=forms.UserForm(request.POST)    #获取每个input标签
        # username = request.POST.get('username')       #获取表单中输入的用户名和密码
        # password = request.POST.get('password')
        # print(username,password)
        # if username and password :    #用户名和密码都不为空
        #     username=username.strip()  #清除用户名前后的空格
        if login_form.is_valid():     #这个就是用于验证输入表单内容的合法性
            username=login_form.cleaned_data['username']      #cleaned_data会将input标签中的变量和值作为以字典的一个元素形式表现出来
            password=login_form.cleaned_data['password']
        # user = User(username, password)         #添加到User表中
        # user.save()                             #存储到数据库中
            #查询数据库中是否存在该用户名和密码
            t_username=User.objects.filter(name=username)
            print(t_username)
            t_password=User.objects.filter(password=password)
            if t_username and t_password:
                request.session['is_login']=True     #写入用户状态和数据
                # request.session['user_id']=t_username.id
                request.session['user_name']=username
                return redirect('/index/')
            elif not t_username:
                # return HttpResponse('用户名不存在')
                message='用户名不存在'
            elif not t_password:
                # return HttpResponse('密码不存在')
                message='密码不存在'
        return render(request,'login/login.html',{"message":message,"login_form":login_form})   #将message信息通过模板传递到网页
    login_form=forms.UserForm()         #保留输入的错误字段
    return render(request,'login/login.html',{"login_form":login_form})



def register(request):
    if request.session.get('is_login'):     #如果是登陆状态就跳转至主页
        return redirect('/index/')
    if request.method=='POST':             #提交post类型的表单数据
        register_form=forms.RegisterForm(request.POST)      #把注册的form表单存储到register_form变量中
        message='请检查填写的内容！'             #这个是用于提示输入有误的反馈变量
        if register_form.is_valid():            #如果注册的内容合法，就继续下面的内容
            #获取web页面输入框输入的信息
            username=register_form.cleaned_data['username']
            password1=register_form.cleaned_data['password1']
            password2=register_form.cleaned_data['password2']
            email=register_form.cleaned_data['email']
            print(email)
            sex=register_form.cleaned_data['sex']
            #判断输入的两次密码是否一致
            if password1!=password2:        #如果两次输入的密码不一致
                message='两次密码输入不一致'     #提示输入不一致
                return render(request,'login/register.html',{'message':message,'register_form':register_form})
            else:
                user=User.objects.filter(name=username)
                if user:
                    message='用户名已存在，请重新输入'
                    return render(request,'login/register.html',{'message':message,'register_form':register_form})
                get_email=User.objects.filter(email=email)
                if get_email:
                    message='邮箱已被注册，请更换邮箱注册！'
                    return render(request,'login/register.html',{'message':message,'register_form':register_form})

                #没问题就进行注册
                new_user=User()
                new_user.name=username
                new_user.password=password1
                print(email)
                new_user.email=email
                print(new_user.email)
                new_user.sex=sex
                new_user.save()         #保存到表中
                return redirect('/login/')      #注册完成后跳转到登陆页面
    register_form=forms.RegisterForm()      #保留输入的错误字段
    return render(request,'login/register.html',{'register_form':register_form})  #这里用于传递输入过的错误信息到界面



    # return render(request,'login/register.html')    #未登陆就跳转到注册页面

def logout(request):
    if not request.session.get('is_login'):   #如果登陆状态为未登陆
        return redirect('/index/')              #就跳转至主页（也就是依然停留在当前页面）
    request.session.flush()             #清除session记录
    return redirect('/index/')          #返回主页