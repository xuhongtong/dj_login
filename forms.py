from django import forms   #导入forms模块
from captcha.fields import CaptchaField   #导入验证码功能模块

class UserForm(forms.Form):   #所有表单类都需要继承forms.Form
    '''
定义form子标签<input>子元素的name属性变量，这里定义的是name=username和name=password的变量
label就是label标签，max_length为设置该变量可以输入的最大字符
widget为设置input的类型，这里的passwordinput为type='password',添加属性使用attrs={}以字典键值对的形式，这里增加了class和placeholder属性
'''
    username=forms.CharField(label='用户名',max_length=64,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'用户名'}))
    password=forms.CharField(label='密码',max_length=512,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'密码'}))
    captcha=CaptchaField(label='验证码')   #添加验证码表单字段


class RegisterForm(forms.Form):
    gender=(
        ('male',"男"),
        ('female',"女"),
    )

    username=forms.CharField(label='用户名',max_length=64,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'用户名'}))
    password1=forms.CharField(label='密码',max_length=512,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'密码'}))
    password2 = forms.CharField(label='密码', max_length=512,widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '密码'}))
    email=forms.EmailField(label='邮箱',widget=forms.EmailInput(attrs={'class':'form-control'}))
    sex=forms.ChoiceField(label='性别',choices=gender)
    captcha = CaptchaField(label='验证码')


