from django.db import models
import datetime
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import DateField

class User(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email=models.EmailField()

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    phone_number = models.CharField(max_length=10)
    address=models.TextField(default="")
    profile=models.FileField(default="")
    def __str__(self):
        return self.user.username

class Validity_pack(models.Model):
    name=models.CharField(max_length=100)
    price=models.IntegerField(default=5000)

    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    acc=models.ForeignKey(Validity_pack,on_delete=models.CASCADE,default=3)
    phone_number = models.CharField(max_length=10)
    address=models.TextField(default="")
    profile=models.FileField(default="")
    license=models.BigIntegerField(default=0)
    created_on=models.DateTimeField(auto_now_add=True)
    valid_till=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username


class Category(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    def __str__(self):
        return self.name
    def get_all_categories():
        return Category.objects.all()

class Product(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=100)
    price=models.IntegerField(default=0)
    category=models.ForeignKey(Category, on_delete=models.CASCADE,default=1)
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE)
    description=models.CharField(max_length=300 , default=' ')
    image=models.ImageField(upload_to='tiffin/images/uploads/')

    @staticmethod   
    def get_all_products():
        return Product.objects.all()

    @staticmethod   
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category = category_id);
        else:
            return Product.get_all_products();

class Feedback(models.Model):
    name=models.CharField(max_length=50)
    email=models.EmailField()
    phone_number=models.CharField(max_length=10)
    messege=models.TextField()
    created_on=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['created_on']

class FeedBackStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class NotificationStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()




from django.db.models.signals import post_save
from django.dispatch import receiver

#@receiver(post_save,sender=Employee)
#def create_user_profile(instance,created,**kwargs):
 #   if created:
 #           Employee.objects.create(user=instance,address="")

#@receiver(post_save,sender=Customer)
#def save_user_profile(instance,**kwargs):
 #       instance.customer.save()

#@receiver(post_save,sender=Employee)
#def save_vender_account(instance,**kwargs):
 #       instance.employee.save()






