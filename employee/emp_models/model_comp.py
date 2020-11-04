from django.db import models
from django.utils import timezone
from django.db.models import CharField
from django.contrib.auth.models import User
import random, string
from django.http import Http404
from django.core.validators import RegexValidator
from django import forms
from django.contrib import admin
from cropperjs.models import CropperImageField

alphanumeric = RegexValidator(r'[A-Za-z0-9]+', 'Only alphanumeric characters are allowed.')


SCHEME_DURATION_TYPE_CHOICES = [
("years", ("years")),
("months", ("months")),
("days", ("days")) 
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
("Quaterly", ("Quaterly")),
("Quaterly", ("Quaterly")),
("Test", ("Test")),
]

FINANCE_TYPE_CHOICES = [
("Car Loan", ("Car Loan")),
("Home Loan", ("Home Loan")),
("Morgage", ("Morgage")) 
]


# def rand_int():
#     l = 10
#     return int(''.join([random.choice(string.digits) for i in range(l)]))

# def rand_string(t,l):
#     if(t=='int'):
#         return int(''.join([random.choice(string.digits) for i in range(l)]))
#     else:
#         return ''.join([random.choice(string.ascii_letters) for i in range(l)])

# def nom_num():
#     len_c = str(len(client.objects.all()))
#     num= "SCC" + ("0"*(4-len_c)) + len_c
#     return num



# def emp_num():
#     len_e = str(len(employee_interview.objects.all()))
#     num= "EMP" + ("0"*(4-len_e)) + len_e
#     return num


class Gaurantor(models.Model):    
    name = models.CharField(max_length = 100, null=True, )
    father_name = models.CharField(max_length = 100, null=True, )
    address = models.CharField(max_length = 500, null=True, )
    photograph = CropperImageField(upload_to='users/images')
    ID_documents = models.FileField(upload_to ='docs/')
    contact = models.CharField(max_length = 10, )

    no_finance = models.IntegerField(default=0)
    expected_amount = models.IntegerField(default=0)
    max_amount = models.IntegerField(default=0)

    #to make two fileds as couple 
    class Meta:
        unique_together = ('name', 'contact','father_name')

    def image_tag(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.photograph))

    def clean(self):
        if self.expected_amount:
            expected = self.expected_amount
            maximum = self.max_amount
            if expected > maximum:
                print("TEST")
                # pass
            else:
                raise forms.ValidationError({'expected_amount': ['Expected amount should be less the maximum amount'],'max_amount': ['Expected amount should be less the maximum amount']})
        if len(self.contact) != 10:
            raise forms.ValidationError({'contact': ["Please enter a valid contact number"]})

class Balance(models.Model):
    cash = models.FloatField(null = True, blank =True, default= 0.0)
    bank = models.FloatField(null = True, blank =True, default= 0.0)
    # Notes Details
    n_10 = models.IntegerField(default=0)
    n_20 = models.IntegerField(default=0)
    n_50 = models.IntegerField(default=0)
    n_100 = models.IntegerField(default=0)
    n_200 = models.IntegerField(default=0)
    n_500 = models.IntegerField(default=0)
    n_2000 = models.IntegerField(default=0)

    c_1 = models.IntegerField(default=0)
    c_2 = models.IntegerField(default=0)
    c_5 = models.IntegerField(default=0)
    c_10 = models.IntegerField(default=0)

#  ------------- model for providing facillity of adding bank choices according to their need
class Bank_Choice(models.Model):
    bank_choice = models.CharField(max_length=100,unique=True) 
    def __str__(self):
        return self.bank_choice

#  ------------- model for providing facillity of adding branch choices according to their need
class Branch_Choice(models.Model):
    branch_choice = models.CharField(max_length=100,unique=True) 
    def __str__(self):
        return self.branch_choice

#  ------------- model for providing facillity of adding scheme choices according to their need
class Scheme(models.Model):

    types = [
    ("Years", ("Years")),
    ("Months", ("Months")),
    ("Days", ("Days")) 
    ]

    name = models.CharField(max_length=100,unique=True , validators=[alphanumeric], help_text="Only one word allowed .. ex - FD_new , RD_monsoon") 
    duration = models.IntegerField(blank =True,null = True)
    duration_type = models.CharField(max_length=100,null = True,choices= [("years", ("years")),
    ("months", ("months")),
    ("days", ("days")) 
    ],default="years")

    interest_rate = models.FloatField(null=True, blank =True, default= 0.0)
    created_time = models.TimeField(default=timezone.now)
    per_day_roi = models.FloatField(null=True, blank =True, default= 0.0)

    def save(self, *args, **kwargs):

        self.name = '_'.join(self.name.split(" "))
        self.interest_rate = self.interest_rate 
        self.per_day_roi = self.interest_rate / 36500

        super(Scheme, self).save(*args, **kwargs)
        
    def __str__(self):
        return '{} {} {} {}%'.format(self.name , self.duration, self.duration_type, self.interest_rate )

class FinanceChoice(models.Model):
    name = models.CharField(max_length=100,unique=True) 
    amount = models.FloatField(null=True, blank =True, default= 0.0)
    created_time = models.TimeField(default=timezone.now)
    def __str__(self):
        return self.name

class DepositChoice(models.Model):
    name = models.CharField(max_length=100,unique=True) 
    emi_type = models.CharField(max_length=100,null = True,choices=[
    ("days", ("days")),
    ("months", ("months")),
    ("one time", ("one time"))],default="one time")
    amount = models.FloatField(null=True, blank =True, default= 0.0)
    created_time = models.TimeField(default=timezone.now)
    
    def __str__(self):
        return self.name

#  ------------- model for providing facillity of adding city choices according to their need
class City_Choice(models.Model):
    city_choice = models.CharField(max_length=100,unique=True) 
    def __str__(self):
        return self.city_choice

#  ------------- model for providing facillity of adding state choices according to their need
class State_Choice(models.Model):
    state_choice = models.CharField(max_length=100,unique=True) 
    def __str__(self):
        return self.state_choice

#  ------------- model for providing facillity of adding district choices according to their need
class District_Choice(models.Model):
    district_choice = models.CharField(max_length=100,unique=True) 
    def __str__(self):
        return self.district_choice

#  ------------- model for providing facillity of adding country choices according to their need
class Country_Choice(models.Model):
    country_choice = models.CharField(max_length=100,unique=True) 
    def __str__(self):
        return self.country_choice
#  ------------- model for providing facillity of adding relation choices according to their need
class Relation_Choice(models.Model):
    relation_choice = models.CharField(max_length=100,unique=True) 
    def __str__(self):
        return self.relation_choice

#  ------------- model for providing facillity of adding id proof choices according to their need
class Id_Type_Choice(models.Model):
    id_type_choice = models.CharField(max_length=100,unique=True) 
    def __str__(self):
        return self.id_type_choice

#------------------------- voucher head ------------------------------
class Head(models.Model):
    value = models.CharField(max_length=100,unique=True) 
    def __str__(self):
        return self.value

#------------------------- voucher sub head ------------------------------
class Sub_Head(models.Model):
    value = models.CharField(max_length=100,unique=True) 
    def __str__(self):
        return self.value



class Basic_Details(models.Model):
    #Basic details component

    GENDER_CHOICES = [
    ("Male", ("Male")),
    ("Female", ("Female")),
    ("Other", ("Other"))
    ]
    
    #basic info
    entry_date = models.DateField(default=timezone.now)
    created_time = models.DateField(default=timezone.now)
    # account holder info 

    first_name = models.CharField(max_length=100,null = True)
    last_name = models.CharField(max_length=100,null = True)
    age = models.IntegerField(null = True)
    gender = models.CharField(max_length=10,null = True,choices=GENDER_CHOICES,default="Male")
    father_name = models.CharField(max_length= 100, null=True  )
    mother_name = models.CharField(max_length= 100, null=True , blank =True)
    date_of_birth = models.DateField(blank=True,null = True)
    # account holder address info
    current_address = models.CharField(max_length = 1000, null=True )
    village = models.CharField(max_length = 100, null=True, )
    area = models.CharField(max_length = 100, null=True, )
    
    city = models.ForeignKey(City_Choice,null = True, to_field='city_choice',related_name='client_city_choice',on_delete=models.CASCADE, default='DAUSA')
    district = models.ForeignKey(District_Choice,null = True, to_field='district_choice',related_name='client_district_choice',on_delete=models.CASCADE, )
    state = models.ForeignKey(State_Choice,null = True, to_field='state_choice',related_name='client_state_choice',on_delete=models.CASCADE, default='RAJASTHAN')
    pincode = models.IntegerField(blank = True , null = True)
    country = models.ForeignKey(Country_Choice ,null = True, to_field='country_choice',related_name='client_country_choice',on_delete=models.CASCADE, default='INDIA')
      
    email_id = models.EmailField(max_length = 100 , null =True, blank = True)
    permanent_address = models.CharField(max_length = 1000, null=True )
    mobile_number_1 = models.CharField(max_length = 10, null=True )
    mobile_number_2 = models.CharField(max_length = 10, null=True, blank =True)
    landline_number = models.CharField(max_length = 15, null=True, blank =True)

    photograph = CropperImageField(upload_to='users/images')
    signature = CropperImageField(upload_to='users/images')
    thumb_impression = CropperImageField(upload_to='users/images',null=True,blank=True)

        # id proof component
    id_type = models.ForeignKey(Id_Type_Choice ,null=True, to_field='id_type_choice',related_name='client_id_type_choice',on_delete=models.CASCADE )
    id_number = models.CharField(max_length = 20, null=True)
    id_photograph1 = CropperImageField(upload_to='users/images') 
    id_photograph2 = CropperImageField(upload_to='users/images', null=True,blank=True) 
    id_photograph3 = CropperImageField(upload_to='users/images', null=True,blank=True) 
    id_photograph4 = CropperImageField(upload_to='users/images', null=True,blank=True) 
    
    class Meta:
        unique_together = ('last_name', 'father_name','id_number', 'first_name', 'village')

        # Cut this hsit
    def clean(self):
        if self.age > 100:
            raise forms.ValidationError({'age': ["Please enter a valid age"]})
    def save(self, *args, **kwargs):
        self.first_name = self.first_name.title() 
        self.last_name = self.last_name.title() if(self.last_name) else self.last_name
        self.father_name = self.father_name.title() if(self.father_name) else self.father_name
        self.mother_name = self.mother_name.title() if(self.mother_name) else self.mother_name
        self.current_address = self.current_address.title() if(self.current_address) else self.current_address 
        self.village = self.village.title() if(self.village) else self.village
        self.permanent_address = self.permanent_address.title() if(self.permanent_address) else self.permanent_address
        self.area = self.area.title() if(self.area) else self.area
        
        super(Basic_Details, self).save(*args, **kwargs)
    
    
    
    

class LoggedInUser(models.Model):
    user = models.OneToOneField(User, related_name='logged_in_user', on_delete=models.CASCADE)
    # Session keys are 32 characters long
    session_key = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return self.user.username