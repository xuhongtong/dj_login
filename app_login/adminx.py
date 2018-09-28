import xadmin
from .models import User
# class Useradmin():
#     list_display=['name','email',]
xadmin.site.register(User)