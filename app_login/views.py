from django.shortcuts import render     #导入render方法，用于渲染html文件，以字典形式传输内容至html页面通过模板进行渲染
from django.shortcuts import redirect  #导入重定向方法
from app_login.models import User       #导入用户信息表
import forms   #导入forms表单
from app_login.models import Confirm    #导入验证码表
import datetime     #导入时间方法
import hashlib      #导入hash加密方法
from django.conf import settings  #导入配置文件
from django.core.mail import EmailMultiAlternatives   #导入邮件发送方法



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
        if login_form.is_valid():     #这个就是用于验证输入表单内容的合法性（包括是否为空、去开头空格等）
            username=login_form.cleaned_data['username']      #cleaned_data会将input标签中的变量和值作为以字典的一个元素形式表现出来
            password=login_form.cleaned_data['password']
        # user = User(username, password)         #添加到User表中
        # user.save()                             #存储到数据库中
            #把数据库中该条记录保存到t_username变量中
            t_username=User.objects.get(name=username)
            # t_password=User.objects.get(password=password)   #获取数据库中的密码信息（这里是hash了）
            # print(t_password)
            if not user_confirm:        #判断该用户是否通过邮箱验证，验证通过了，该表会有一条记录
                message='该用户还未通过邮件确认！'
                return render(request,'login/login.html',{'message':message})
            if not t_username.name:       #判断该用户的账号是否在数据库中有对应的数据
                # return HttpResponse('用户名不存在')
                message='用户名不存在'
            elif t_username.password==hash_code(password):    #将输入的密码取hash值和数据库中的的密码hash值进行匹配
                request.session['is_login']=True     #写入用户状态和数据
                # request.session['user_id']=t_username.id
                request.session['user_name']=username
                return redirect('/index/')
            elif not t_username.password:       #判断该用户的密码是否在数据库中有对应的数据
                # return HttpResponse('密码不存在')
                message='密码不存在'
        return render(request,template_name='login/login.html',context={"message":message,"login_form":login_form})   #将message信息通过模板传递到网页
    login_form=forms.UserForm()         #保留输入的错误字段
    return render(request,template_name='login/login.html',context={"login_form":login_form},content_type='text/html')


#邮箱注册验证功能

def make_confirm(user):
    now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    code=hash_code(user.name,now)
    Confirm.objects.create(code=code,user=user,)
    return code

#hash加密功能

def hash_code(s,salt='app_login'):
    h=hashlib.sha256()      #通过构造函数获得一个hash对象
    s+=salt                 #加盐
    h.update(s.encode())    #使用hash对象的update方法添加消息
    return h.hexdigest()    #获得16进制str类型的消息摘要


#邮件发送注册功能，通过接收的邮件激活账号

def send_email(email,code):
    subject='主题'
    text_content='纯文本：内容'
    html_content='''
                    <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>www.login.com</a>，\
                    这是一个登陆注册系统学习项目</p>
                    <p>请点击站点链接完成注册确认！</p>
                    <p>此链接有效期为{}天！</p>
                    '''.format('127.0.0.1:8000', code, settings.CONFIRM_DAY)
    msg=EmailMultiAlternatives(subject,text_content,settings.EMAIL_HOST_USER,[email])
    msg.attach_alternative(html_content,'text/html')
    msg.send()


#注册方法，渲染相应的网页请求，接收表单数据，保存至数据库中，并做注册合法性等逻辑处理
def register(request):
    if request.session.get('is_login'):     #如果是登陆状态就跳转至主页(先登出才能注册）
        return redirect('/index/')
    if request.method=='POST':             #没有登陆就提交post类型的表单数据
        message = '请检查填写的内容！'  # 这个是用于提示输入有误的反馈变量
        register_form=forms.RegisterForm(request.POST)      #把注册的form表单存储到register_form变量中
        if register_form.is_valid():            #如果注册的内容合法，就继续下面的内容
            #获取web页面输入框输入的信息
            username=register_form.cleaned_data['username']         #获取输入框用户名中填写的信息
            password1=register_form.cleaned_data['password1']       #获取输入框密码中填写的信息
            password2=register_form.cleaned_data['password2']       #获取输入框确认密码中填写的信息
            email=register_form.cleaned_data['email']               #获取输入框邮箱中填写的信息
            sex=register_form.cleaned_data['sex']                   #获取输入框密码中选择的性别信息
            #判断输入的两次密码是否一致
            if password1!=password2:        #如果两次输入的密码不一致
                message='两次密码输入不一致'     #提示输入不一致
                return render(request,'login/register.html',{'message':message,'register_form':register_form})  #提交表单后检测两次密码输入不一致，会重新进入登陆界面，同时提示密码不一致，并保留填写的错误信息
            else:
                user=User.objects.filter(name=username)         #输入的密码一致，就在数据库中查询是否有输入框中所输入的用户名对应的值，并把查询的结果保存至变量中
                if user:        #这里判断查询是否有数据（也就是存在该列）
                    message='用户名已存在，请重新输入'      #已经存在就表明已经注册了该信息，把该提示信息以变量的形式保存到message中
                    return render(request,'login/register.html',{'message':message,'register_form':register_form})  #这里把该提示信息以字典的形式传入到网页中，并把写入的错误信息也保留
                get_email=User.objects.filter(email=email)      #上面都不满足就添加（用户名不存在、两次输入密码一致）
                if get_email:
                    message='邮箱已被注册，请更换邮箱注册！'
                    return render(request,'login/register.html',{'message':message,'register_form':register_form})

                #没问题就进行注册（用户名不存在、两次密码一致、邮箱未注册）
                new_user=User()
                new_user.name=username
                new_user.password=hash_code(password1)      #进行hash加密
                new_user.email=email
                new_user.sex=sex
                new_user.save()         #保存到表中

                code=make_confirm(new_user)
                send_email(email,code)
                message='请前往注册邮箱，进行邮件确认！'
                return render(request,'login/confirm.html',{'register_form':register_form,'message':message})
                # return redirect('/login/')      #注册完成后跳转到登陆页面
        return render(request,'login/register.html',{'register_form':register_form,'message':message})  #有不合法信息就跳转到这个页面，包括验证码校验
    register_form=forms.RegisterForm()      #保留输入的错误字段
    return render(request,'login/register.html',{'register_form':register_form})  #这里用于传递输入过的错误信息到界面，不满足post请求就返回注册页面



#点击邮件中接收到的请求后跳转确认页面，处理该逻辑，跳转邮件确认页面
def user_confirm(request):
    code=request.GET.get('code')
    message=''
    try:
        confirm=Confirm.objects.get(code=code)
    except:
        message='无效的确认请求！'
        return render(request,'login/confirm.html',{'message':message})

    c_time=confirm.date
    now=datetime.datetime.now()
    if now>c_time+datetime.timedelta(settings.CONFIRM_DAY):
        confirm.user.delete()
        message='邮件过期！请重新注册！'
        return render(request,'login/confirm.html',{'message':message})

    else:
        confirm.user.is_conformed=True
        confirm.user.save()
        confirm.delete()
        message='感谢确认，请使用账号登录！'
        return render(request,'login/confirm.html',{'message':message})
    # return render(request,'login/register.html')    #未登陆就
        # 跳转到注册页面



#登出功能函数，渲染主页中判断未登陆的页面内容，显示至网页中
def logout(request):
    if not request.session.get('is_login'):   #如果登陆状态为未登陆
        return redirect('/index/')              #就跳转至主页（也就是依然停留在当前页面）
    request.session.flush()             #清除session记录
    return redirect('/index/')          #返回主页