import xadmin
from .models import User
from .models import Confirm
# class Useradmin():
#     list_display=['name','email',]
xadmin.site.register(User)          #将用户表注册到xadmin后台
xadmin.site.register(Confirm)        #将用户确认表注册到xadmin后台