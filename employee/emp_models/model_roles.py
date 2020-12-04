from django.db import models
from django.utils import timezone
from django.db.models import CharField
from django.contrib.auth.models import User, Group
from employee.emp_models.model_comp  import *
# from employee.emp_admin.admin_comp  import *
from django.utils.safestring import  mark_safe
from django.shortcuts import redirect
import random
from django import forms
from django.http import Http404
from cropperjs.models import CropperImageField

SCHEME_DURATION_TYPE_CHOICES = [
("Years", ("Years")),
("Months", ("Months")),
("Days", ("Days")) 
]
GENDER_CHOICES = [
("Male", ("Male")),
("Female", ("Female")),
("Other", ("Other"))

]
ID_CHOICES = [
("Yes", ("Yes")),
("No", ("No"))

]
AGENT_CATEGORY_CHOICES = [
("Society", ("Society")),
("Finance", ("Finance"))
]
EMI_TYPE_CHOICES = [
("Daily", ("Daily")),
("Monthly", ("Monthly")),
("Quaterly", ("Quaterly")) 
]

FINANCE_TYPE_CHOICES = [
("Loan", ("Loan")),
("Credit", ("Creit")),
("Morgage", ("Morgage")) 
]


def nom_num():
    len_c = str(len(client.objects.all())+1)
    num= "SCC" + ("0"*(4-len(len_c))) + len_c
    return num

def emp_num():
    len_e = str(len(employee_interview.objects.all())+1)
    num= "EMP" + ("0"*(4-len(len_e))) + len_e
    return num

def rand_int():
    l = 12
    return int(''.join([random.choice(string.digits) for i in range(l)]))


class employee_interview(Basic_Details):

    nomination_number = models.CharField(max_length=10, primary_key= True, unique=True,default= emp_num,help_text="Employee ID")
    interview_date = models.DateField(default=timezone.now)

    joined = models.BooleanField(default=False)

    referal_name = models.CharField(max_length= 100,blank =True, null= True)
    referal_father = models.CharField(max_length= 100,blank =True, null= True)
    referal_mobile_number = models.CharField(max_length= 100, null = True ,blank =True)
    referal_address = models.CharField(max_length=1000, null=True, blank=True)
    referal_photograph = CropperImageField(upload_to='users/images', null=True,blank=True)
    referal_signature = CropperImageField(upload_to='users/images', null=True,blank=True)
    ref_id_1 = CropperImageField(upload_to='users/images', null=True,blank=True)
    ref_id_2 = CropperImageField(upload_to='users/images', null=True,blank=True)

    account_nominee_name = models.CharField(max_length= 100,blank =True, null= True)
    account_nominee_contact = models.CharField(max_length= 10,blank =True, null= True)


    finance_coll = models.IntegerField( default=0)
    deposit_coll = models.IntegerField( default =0)

    upload_id_1 = CropperImageField(upload_to='users/images', null=True,blank=True)
    upload_id_2 = CropperImageField(upload_to='users/images', null=True,blank=True)
    upload_bank_passbook = CropperImageField(upload_to='users/images', null=True,blank=True)
    upload_cheque = CropperImageField(upload_to='users/images', null=True,blank=True)
    upload_stamp_paper = CropperImageField(upload_to='users/images', null=True,blank=True)

    def image_tag(self):
        print(self.photograph)
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.photograph))
        # return ('<img src="/media/%s" width="50" height="50" />' % (self.photograph))

    image_tag.short_description = 'Image'

    def __str__(self):
        return self.first_name




class client(Basic_Details):

    nomination_number = models.CharField(max_length=10,primary_key= True, unique=True,default= nom_num)
# --------------------------account holder info ----------------------------
    account_nominee_name = models.CharField(max_length= 100,null= True)
    nominee_relation = models.ForeignKey(Relation_Choice , to_field='relation_choice',related_name='client_relation_choice',on_delete=models.CASCADE , blank=True, null=True)
    status =  models.BooleanField(default=True)

 # --------------------------guardian data----------------------------
    minor_checkbox = models.BooleanField(default=False)
    guardian_name = models.CharField(max_length= 100,blank =True, null= True)
    guardian_relation = models.ForeignKey(Relation_Choice ,null = True, to_field='relation_choice',related_name='client_relation2_choice',on_delete=models.CASCADE , blank=True)
    guardian_address   = models.CharField(max_length = 1000, null=True, blank =True)

    # --------------------------agent data----------------------------
    category = models.CharField(max_length=10,null = True,choices=AGENT_CATEGORY_CHOICES,default="Society")
    agent_name = models.ForeignKey(employee_interview , on_delete=models.SET_NULL , null=True)
    nomination_fees = models.FloatField(null = True,  default= 0.0)
    sharing_amount = models.FloatField(null = True,  default= 0.0)
    no_of_shares = models.IntegerField(default=0)

    remarks = models.TextField(null=True,blank=True)

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.photograph))
        
    image_tag.short_description = 'Image'

    def clean(self):
        if (self.age):
            if(self.age<10):
                raise forms.ValidationError({'age':["Age is too small"]})
        else:
            raise forms.ValidationError("Please Enter Age")

        if(self.minor_checkbox):
            if(self.guardian_name and self.guardian_address and self.guardian_relation):
                pass
            else:
                raise forms.ValidationError("Please enter Gaurdian Details")
        
        if(self.nomination_fees<10 or self.sharing_amount<100 or self.no_of_shares<1):
            raise forms.ValidationError("Fees or shares are not sufficient")

        if(self.nominee_relation):
            pass
        else:
            raise forms.ValidationError("Please specify nominee relation")
        
        if (self.mobile_number_1):
            if len(self.mobile_number_1) != 10:
                raise forms.ValidationError({'mobile_number_1':["Please Enter valid mobile number"]})
        else:
            raise forms.ValidationError({'mobile_number_1':["Please Enter mobile number"]})
        
    def __str__(self):
        return self.first_name + " Nomination Number " + str(self.nomination_number)
    class Meta:
        unique_together = ('nomination_number', 'account_nominee_name',)

class employee_joining(models.Model):
    employee = models.OneToOneField(employee_interview ,null = True, on_delete=models.CASCADE , blank=True)
    designation = models.CharField(max_length= 100,blank =True, null= True)
    joining_date = models.DateField(default=timezone.now)
    salary = models.FloatField(null=True,blank =True)
    bonus = models.FloatField(default=0)
    deduction = models.FloatField(default=0)
    total = models.FloatField(null=True,blank =True)

    def save(self, *args, **kwargs):
        print(self.employee.first_name)
        if(not self.pk):
            user , _ = User.objects.get_or_create(username=self.employee.nomination_number ,is_staff=1 , first_name=self.employee.first_name , last_name= self.employee.last_name)
            user.groups.set([Group.objects.get(id=1)])
            user.set_password('sidhi123')
            user.save()
            print('user created')

            e = employee_interview.objects.get(nomination_number=self.employee.nomination_number )
            e.joined  = True
            e.save()
        else:
            print('user created')
        
        super(employee_joining, self).save(*args, **kwargs)
    


    def __str__(self):
        return self.employee.nomination_number + " " + self.employee.first_name

    

