import uuid
from django.db import models
  
class Users(models.Model):
    my_id = models.AutoField(primary_key=True)
    mobile = models.CharField(max_length=255,null=True,blank = True,unique=True)
    email = models.EmailField(max_length=255,null=True,blank = True)
    name = models.CharField(max_length=255,null=True,blank = True)
    password = models.CharField(max_length=255,null=True,blank = True)

    class Meta:
        db_table='register'
  
    def __str__(self) -> str:
        return self.name

class Posts(models.Model):
    u_id = models.IntegerField()
    my_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255,null=True,blank = True)
    desc = models.CharField(max_length=255,null=True,blank = True)
    image = models.ImageField(upload_to='Media/')
    

    class Meta:
        db_table='posts'
  
    def __str__(self) -> str:
        return self.name


