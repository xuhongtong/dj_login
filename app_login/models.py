from django.db import models

# Create your models here.
class User(models.Model):
    gender=(
        ('mal',"男"),
        ('female',"女")
    )
    name=models.CharField(max_length=64,unique=True)
    password=models.CharField(max_length=512)
    email=models.EmailField(unique=True)
    date=models.DateTimeField(auto_now_add=True)
    sex=models.CharField(max_length=4,choices=gender,default='男')  #choices用于页面上的选择框标签，需要先提供一个二维的二元元组，第一个元素表示存在数据库内真实的值，第二个表示页面上显示的具体内容

    def __str__(self):
        return self.name    #这个是用于管理后台查看用户信息的，没有就会使用user_object显示

    class Meta:
        db_table='t_user'   #自定义创建的表名
        verbose_name='用户'   #管理后台显示的模型名称
        verbose_name_plural='用户'    #verbose_name的复数形式

