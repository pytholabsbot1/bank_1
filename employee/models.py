from django.db import models
from django.utils import timezone
from django.db.models import CharField
import copy , datetime
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.http import HttpResponse,HttpResponseRedirect
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from num2words import num2words 
from employee.emp_models.model_comp import *
from employee.emp_models.model_roles import *
from cropperjs.models import CropperImageField


def get_deposit_billnum():
    objs = len(collection_deposit.objects.all())+1
    return objs

def get_finance_billnum():
    objs = len(collection_finance.objects.all())+1
    return objs

def get_cashcol_billnum():
    objs = len(cash_collection.objects.all())+1
    return objs

def get_withdrawl_billnum():
    objs = len(withdrawl_entry.objects.all())+1
    return objs

def dp_code():
    dt = ''.join(str(datetime.datetime.now().date()).split('-'))[2:]
    ds = str(len(deposits_table.objects.filter(account_opening_date=timezone.now()))+1)
    l_d = "0"* (2-len(ds)) + ds
    dp_ = '19' + dt + l_d
    return(dp_)


def fc_code():
    dt = ''.join(str(datetime.datetime.now().date()).split('-'))[2:]
    print(dt)
    fc = str(len(finance_table.objects.filter(applied_date=timezone.now()))+1)
    print(fc)
    l_d = "0"* (2-len(fc)) + fc
    fc_ = '26' + dt + l_d
    return(fc_)

def rand_int():
    l = 12
    return int(''.join([random.choice(string.digits) for i in range(l)]))



#----------------------------- wants to apply for loan  -------------------------------------
#-------------------------------- new finance --------------------------------------------------
class finance_table(models.Model):
    EMI_TYPE_CHOICES = [
    ("Daily", ("Daily")),
    ("Monthly", ("Monthly")),
    ("Quaterly", ("Quaterly")),
    ("OneTime", ("OneTime")),
    ]
    person = models.ForeignKey(client ,null = True ,on_delete=models.CASCADE )
    
    loan_account_number = models.CharField(max_length=500,null = True, unique=True,default=fc_code)
    demanded_amount = models.FloatField(null=True, default= 0.0)
    loan_duration = models.IntegerField(null = True, )
    duration_type = models.CharField(max_length=100,null = True,choices=SCHEME_DURATION_TYPE_CHOICES,default="Years")
    emi_type = models.CharField(max_length=100,null = True,choices=EMI_TYPE_CHOICES)
    applied_date = models.DateField(default=timezone.now)

    gaurantor = models.ForeignKey(Gaurantor , null=True, on_delete=models.CASCADE)

    stamp_photograph = CropperImageField(upload_to='users/images')
    cheque_photograph = CropperImageField(upload_to='users/images')

    # agent data
    category = models.CharField(max_length=100,null = True,choices=FINANCE_TYPE_CHOICES,default="Loan")
    loan_type = models.ForeignKey(FinanceChoice,null=True,on_delete=models.CASCADE)
    
    agent_name = models.ForeignKey(employee_interview,null=True,on_delete=models.CASCADE)

    approved =  models.BooleanField(default=False)
    expected_date = models.DateField(null = True)
    expected_amount = models.FloatField(null = True)

    remarks = models.TextField(null=True,blank=True)
    created_time = models.TimeField(default=timezone.now)

    def image_tag(self):
        print(self.photograph)
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.photograph))

    def __str__(self):
        return self.person.first_name + " Account Number " + str(self.loan_account_number)

    def clean(self, *args, **kwargs):
        if self.expected_date:
            time_difference = self.expected_date - timezone.now().date()
            if (time_difference.days < 1):
                raise forms.ValidationError({'expected_date': ["Cannot enter a past date. Please enter a future date.",]})
        else:
            raise forms.ValidationError({'expected_date': ["This field is required",]})
        if self.demanded_amount < 1000:
            raise forms.ValidationError({'demanded_amount': ["The demanded amount is too low."]})
        if self.demanded_amount > 9999999:
            raise forms.ValidationError({'demanded_amount': ["The demanded amount is too large."]})
        if self.expected_amount > self.demanded_amount:
            raise forms.ValidationError({'expected_amount': ["Expected amount cannot be greater than demanded amount"]})
        
        if self.gaurantor:
            if self.gaurantor.expected_amount > (self.gaurantor.max_amount):
                raise forms.ValidationError({'gaurantor': ["Gaurantor exceeds the total amount authorized. Please contact admin"]})

        if self.person:
            print(self)
            loans = finance_table.objects.all()
            for loan in loans:
                if loan.person == self.person:
                    if loan == self:
                        # continue
                        apps = loan.approved_finance_table_set.all()
                        if apps:
                            for app in apps:
                                if app.status == 'ACTIVE':
                                    raise forms.ValidationError({'person': ["Gaurantor exceeds the total amount authorized. Please contact admin"]})
                                    break
                        else:
                            raise forms.ValidationError({'person': ["Loan application exists, but has not been approved. Please contact admin."]})
        super(finance_table, self).save(*args, **kwargs)
    # class Meta:
    #     unique_together = ('person', 'date',)
        
#------------------------- whose loan is approved by admin -----------------------------


class approved_finance_table(models.Model):
    EMI_TYPE_CHOICES = [
    ("Daily", ("Daily")),
    ("Monthly", ("Monthly")),
    ("Quaterly", ("Quaterly")),
    ("OneTime", ("OneTime")),
    ]
   
    finance = models.ForeignKey(finance_table ,null = True, unique=True,on_delete=models.CASCADE)
    secure_key = models.CharField(max_length=12, null=True,default= rand_int )
    client_bank_account_number = models.CharField(max_length=20,null = True, )
    client_bank = models.ForeignKey(Bank_Choice, to_field='bank_choice',related_name='finance_approval_bank_choice',on_delete=models.CASCADE,null = True)
    ifsc_code = models.CharField(max_length=20,null = True,  default='IFSC')
    cheque_number = models.CharField(max_length=200,null = True,)
    
    loan_start_date = models.DateField(default = timezone.now )
    loan_end_date = models.DateField(default = timezone.now )
    
    status = models.CharField(max_length=100,choices= [("ACTIVE", ("ACTIVE")),
    ("DEACTIVE", ("DEACTIVE")),
    ("SUSPENDED", ("SUSPENDED")),
    ("HOLD", ("HOLD")),
    ("DEAD", ("DEAD")),
    ],default="ACTIVE")

    db = models.BooleanField(default=True)

    sanctioned_amount = models.FloatField(null=True,)
    total_intrest_amount = models.FloatField(null=True, default= 0.0)
    
    emi_delta = models.CharField(max_length=50,null = True, blank =True)
    loan_duration = models.IntegerField(null = True)
    duration_type = models.CharField(max_length=100,null = True,choices= [
    ("years", ("years")),
    ("months", ("months")),
    ("days", ("days")) 
    ],default="years")
    
    #Flat ROI
    roi = models.IntegerField(null = True )
    no_of_emi = models.IntegerField(null = True , blank =True)
    
    emi_type = models.CharField(max_length=100,null = True,choices=EMI_TYPE_CHOICES,default="Years")
    
    emi_amount = models.FloatField(null=True, blank =True, default= 0.0)
    discount =  models.FloatField(null=True, blank =True, default= 0.0)
    
    #agent_name = models.CharField(max_length= 100,blank =True, null= True)
    counter_number = models.IntegerField(null= True,)
    remarks = models.TextField(null=True,blank=True)

    #for keeping track of total
    recieved = models.FloatField(null=True, blank =True, default= 0.0)
    total = models.FloatField(null=True, blank =True, default= 0.0)
    created_time = models.TimeField(default=timezone.now)
    
    def __str__(self):
        return self.finance.person.first_name + " Nomination Number " + str(self.finance.person.nomination_number)

    def clean(self):
        ##validations
        if not self.id:
            print(self.id)
            if self.sanctioned_amount > self.finance.expected_amount:
                raise forms.ValidationError("Sanctioned amount is larger than expected amount")

            if self.finance:
                all_loans = approved_finance_table.objects.filter(finance__person=self.finance.person, status = "ACTIVE")
                if len(all_loans)>=1:
                    raise forms.ValidationError("The client already has an active loan")

                
    def save(self, *args, **kwargs):
        
        #computing the emi , etc to store on creation
        d_ = self.loan_duration
        dtype_ = self.duration_type
        start_date = datetime.datetime.now()
        
        self.person = self.finance.person
        #compute end date of loan
        k_ = {dtype_:+d_}
        end_date = start_date.date() + relativedelta(**k_)
        
        # compute total amount with discount decuctions
        self.total_intrest_amount = round( (self.sanctioned_amount * (self.roi/100)) ,3)
        emi =  self.total_intrest_amount + self.sanctioned_amount - self.discount
        
        #calculate no. of emi according to type
        print(self.emi_type , start_date.date() , end_date  ,(end_date - start_date.date()).days)
        if(self.emi_type=="Daily"):
            self.no_of_emi = (end_date - start_date.date()).days
            self.emi_delta = '1 days'

        elif(self.emi_type=="Monthly"):
            self.no_of_emi = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
            self.emi_delta = '1 months'

        elif(self.emi_type=="Quaterly"):
            months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
            self.no_of_emi = months // 3
            self.emi_delta = '3 months'

        else:
            self.no_of_emi = 1
            self.emi_delta = 'None'

        print('----> ',self.no_of_emi)
        #compute emi 
        self.emi_amount = round ( emi / self.no_of_emi , 3)
        
        self.total = emi
        #update approved status
        fc = finance_table.objects.get(loan_account_number = self.finance.loan_account_number)
        fc.approved = True
        fc.save()

        gar = self.finance.gaurantor
        amount = gar.max_amount
        gar.max_amount = amount + self.sanctioned_amount
        gar.save()

        super(approved_finance_table, self).save(*args, **kwargs)
        

#---------------------- wants to deposit money for the first time --------------------------
# -------------------------------- new deposit ----------------------------------------
class deposits_table(models.Model):

    person = models.ForeignKey(client ,null = True ,on_delete=models.CASCADE)

    secure_key = models.CharField(max_length=12, null=True,default= rand_int , blank=True)
    society_account_number = models.CharField(max_length=500,null = True, blank =True , unique=True, default=dp_code)
    client_bank_account_number = models.CharField(max_length=500,null = True, blank =True)
    client_bank = models.ForeignKey(Bank_Choice, to_field='bank_choice',related_name='deposit_bank_choice',on_delete=models.CASCADE , blank = True,null = True)
    ifsc_code = models.CharField(max_length=20,null = True, blank =True)
    account_opening_date = models.DateTimeField(default=timezone.now)
    account_opening_amount = models.FloatField(null=True, default= 0.0)
    
    scheme = models.ForeignKey(Scheme,null = True,on_delete=models.CASCADE)

    interest_collected = models.FloatField(null=True, blank =True, default= 0.0)
    maturity_interest = models.FloatField(null=True, blank =True, default= 0.0)

    status = models.CharField(max_length=100,choices= [("ACTIVE", ("ACTIVE")),
    ("DEACTIVE", ("DEACTIVE")),
    ("HOLD", ("HOLD")),
    ("DEAD", ("DEAD")),
    ("SUSPENDED", ("SUSPENDED")) 
    ],default="ACTIVE")

    db = models.BooleanField(default=True)

    balance = models.FloatField(null=True, blank =True, default= 0.0)

    maturity_date = models.DateField(null=True , blank=True)
    maturity_amount = models.FloatField(null=True, blank =True, default= 0.0)
    # agent data
    category = models.ForeignKey(DepositChoice,null = True,on_delete=models.CASCADE)
    #employee_name = models.CharField(max_length= 100,blank =True, null= True)
    agent_name = models.ForeignKey(employee_interview,null=True,on_delete=models.CASCADE)
    counter_number = models.IntegerField( null=True)
    
    remarks = models.TextField(null=True,blank=True)
    created_time = models.TimeField(default=timezone.now)

    def __str__(self):
        return self.society_account_number

    def clean(self):
          ##validations
        if(self.client_bank_account_number):
            if(self.client_bank and self.ifsc_code):
                pass
            else:
                raise forms.ValidationError("Please Enter All Bank Details")

        if(self.account_opening_amount<10):
            raise forms.ValidationError("Please Raise Account Opening Amount")

        if self.person:
            deps = deposits_table.objects.all()
            for dep in deps:
                if dep.person == self.person:
                    if dep == self:
                        continue
                    if dep.status == 'ACTIVE':
                        raise forms.ValidationError({'person': ["Account already active with the same client. Please contact admin"]})
                        break
        ##validations <<<<<


    def save(self, *args, **kwargs):
        if(self.pk is None):
            obj = self
            op_m = self.account_opening_amount - 0
            
            # print('saving')
            obj.balance = op_m
            #is it a deposit account ?
            if(obj.scheme.duration):
                #computing the emi , etc to store on creation
                d_ = obj.scheme.duration
                dtype_ = obj.scheme.duration_type
                start_date = datetime.datetime.now()
                
                #compute end date of loan
                k_ = {dtype_:+d_}
                end_date = start_date.date() + relativedelta(**k_)
                
                # compute total amount with discount deductions
                interest = round( (obj.account_opening_amount * (obj.scheme.per_day_roi * (end_date-start_date.date()).days)) ,3)
                obj.maturity_interest = interest
                obj.maturity_amount =  interest + obj.account_opening_amount
                
                if(obj.category.name=="FD"):
                    obj.interest_collected = interest
        if self.status == "DEACTIVE":
            if self.balance > 0:
                self.status = "ACTIVE"
                print("ACCOUNT ACTIVATED")
        

        super(deposits_table, self).save(*args, **kwargs)

        
    

#---------------- for collection of finance emi ------------------------------------------
#---------------- for collection of finance emi ------------------------------------------
#---------------- for collection of finance emi ------------------------------------------

# collect finance

class collection_finance(models.Model):
    Loan_category =(
        ("Loan",("Loan")),
    )

    finance = models.ForeignKey(approved_finance_table ,null = True, on_delete=models.CASCADE , blank = True)

    bill_no  = models.IntegerField(null = True , blank= False , default=get_finance_billnum)
    loan_emi_received_date = models.DateTimeField(default=timezone.now)
   
    agent_name = models.ForeignKey(employee_interview,null=True,on_delete=models.CASCADE , blank = True)
    person= models.ForeignKey(client,null=True,on_delete=models.CASCADE , blank = True)
    
    loan_emi_received = models.FloatField(null=True,blank =True)
    penalty = models.FloatField(null=True,blank =True, default=0)
    
    remarks = models.TextField(null=True, default="By Cash")
    created_time = models.TimeField(default=timezone.now)

    def __str__(self):
        return self.finance.finance.person.first_name + " Nomination Number " + str(self.finance.finance.person.nomination_number)

    def save(self, *args, **kwargs):
        print(self.finance.recieved , self.finance.total)
        if(self.finance.recieved>=self.finance.total):
            raise  forms.ValidationError("Exccedingt the Total amount to be taken ")
        elif(self.finance.status == "DEACTIVE"):
            raise  forms.ValidationError("Laon Account is Dormant Unable to add Collections")
        
        super(collection_finance, self).save(*args, **kwargs)

#collect deposit 

class collection_deposit(models.Model):

    deposit = models.ForeignKey(deposits_table ,null = True, on_delete=models.CASCADE)

    bill_no = models.IntegerField(null = True , default=get_deposit_billnum)
    payment_received_date = models.DateTimeField(default = timezone.now ,null=True)
        
    agent_name =models.ForeignKey(employee_interview,null=True,on_delete=models.CASCADE)
    person= models.ForeignKey(client,null=True,on_delete=models.CASCADE , blank = True)
  
    payment_received = models.FloatField(null=True,)
    previous_balance = models.FloatField(null=True,blank =True)
    latest_intrest = models.FloatField(null=True,blank =True)
    remarks = models.TextField(null=True, default="By Cash")
    created_time = models.TimeField(default=timezone.now)

    def sc_num(self):
        return self.deposit.society_account_number
    
    def __str__(self):
        return self.deposit.person.first_name + " Nomination Number " + str(self.deposit.person.nomination_number)
    
    def clean(self):
        if self.payment_received:
            if self.payment_received < 10:
                raise forms.ValidationError({'payment_received': ['Amount too low.']})
        if (not (self.previous_balance or self.latest_intrest)) and (not self.previous_balance == 0 and not self.latest_intrest == 0):
            print(not (self.previous_balance or self.latest_intrest))
            print(type(self.previous_balance), self.latest_intrest)
            raise forms.ValidationError({'previous_balance': ['Please load the details using the button on the top.']})
        if self.previous_balance or self.latest_intrest:
            print(self.previous_balance, self.latest_intrest, self.deposit.balance, self.deposit.interest_collected)
            if (self.previous_balance != self.deposit.balance):
                raise forms.ValidationError({'previous_balance': ['Please Verify the details or press the load again button again.']})
    # def save(self, *args, **kwargs):
    #     print(request.user)
    #     super(collection_deposit, self).save(*args, **kwargs)
#---------------- for collection of finance or deposit emi ///------------------------------------------
#---------------- for collection of finance emi //------------------------------------------


#-=withdraw money 

class withdrawl_entry(models.Model):
    PAYMODE = (
        ("CASH",("CASH")),
        ("CHEQUE",("CHEQUE")),
    )
    TYPE = (
        ("Maturity",("Maturity")),
        ("Prematurity",("Prematurity")),
        ("closed",("closed")),
        ("withdraw",("withdraw"))
    )
    bill_no = models.IntegerField(default = get_withdrawl_billnum , unique=True)
    amount_withdrawl_date = models.DateTimeField(default = timezone.now)
    
    category = models.CharField(max_length=100, choices=TYPE)
    society_account = models.ForeignKey(deposits_table,null=True,on_delete=models.CASCADE)
    holder_name = models.CharField(max_length=100,null = True,blank =True)
    
    available_amount = models.FloatField(null=True)
    #manual
    amount_withdrawl = models.FloatField(null=True)
    intrest_amount = models.FloatField(null=True, default = 0)

    deduction_amount = models.FloatField(null=True,blank =True, default = 0)
    rest_amount = models.FloatField(null=True,blank =True, default = 0)
    #cheque / cash
    paymode = models.CharField(max_length=100, choices=PAYMODE)
    
    cheque_no = models.CharField(max_length=200,null = True, blank =True )
    created_time = models.TimeField(default=timezone.now)
    # maturity_amount = models.FloatField(null=True,blank =True, default = 0)
    
    agent = models.ForeignKey(employee_interview,null=True,on_delete=models.SET_NULL)
    
    def image_tag(self):
        print(self)
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.society_account.person.photograph))
    
    def sign_tag(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.society_account.person.signature))
    
    
    image_tag.short_description = 'Photo'
    sign_tag.short_description = 'Sign'


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
    
    remarks = models.TextField(null=True, blank = True)

    def clean(self):

        if(self.paymode == "CASH"):
            notes = [i.strip() for i in 'n_10, n_20 , n_50, n_100 , n_200 , n_500,n_2000 ,c_1 , c_2 , c_5, c_10'.split(',')]
            #check if the total notes amount == entered amount            
            total_amt = sum([int(n.split('_')[1]) * getattr(self,n) for n in notes]) != ((self.amount_withdrawl + self.intrest_amount)-self.deduction_amount)
            if(total_amt):
                raise forms.ValidationError("Notes doesn add up to the amount entered")
        else:
            if(not self.cheque_no):
                raise forms.ValidationError("Give Cheque No.")

        if self.amount_withdrawl:
            if self.amount_withdrawl<10:
                raise forms.ValidationError({'amount_withdrawl': ['Withdrawl amount too low.']})
        if self.society_account and self.category == "withdraw":
            if (self.society_account.balance - self.amount_withdrawl) < 5000:
                raise forms.ValidationError({'amount_withdrawl': ['Withdrawl amount is larger than balance. Minimum Balance is Rs. 5000']})
        elif self.society_account:
            if not (self.society_account.balance == self.amount_withdrawl):
                raise forms.ValidationError({'amount_withdrawl': ['Please withdraw all amount']})


    def save(self, *args, **kwargs):

        av_amt = self.society_account.balance
       
        self.rest_amount = av_amt - self.amount_withdrawl
        super(withdrawl_entry, self).save(*args, **kwargs)

        sc = deposits_table.objects.get(id=self.society_account.id)
        sc.balance = self.rest_amount
        sc.save()

    
    # def __str__(self):
    #     return "Bill Number :" + str(self.bill_no) + " Name :" + self.holder_name 



#------------------------------------  Vouchers ---------------------------------

class Voucher(models.Model):
    TRANSACT_TYPE =(
        ("Cr",("Cr")),
        ("Dr",("Dr"))
    )

    VOUCHER_TYPE =(
        ("Payment",("Payment")),
        ("Journal",("Journal")),
        ("Contra",("Contra")),
        ("Reciept",("Reciept"))
    )

    voucher_number = models.CharField(max_length=9,unique=True)
    date = models.DateTimeField(default = timezone.now)
    
    db = models.BooleanField(default=True)
    custom_num = models.BooleanField(default=False)
     
    transact_type = models.CharField(max_length=50,choices=TRANSACT_TYPE,default="Cr")
    voucher_type = models.CharField(max_length=50,choices=VOUCHER_TYPE,default="Journal")

    title = models.CharField(max_length=50,default="")
    account_number = models.CharField(max_length=100, null=False, blank=True)

    head = models.ForeignKey(Head , on_delete=models.CASCADE)
    sub_head = models.ForeignKey(Sub_Head , on_delete=models.CASCADE)
    
    amount = models.FloatField(null=False)

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

    curr_n_10 = models.IntegerField(default=0)
    curr_n_20 = models.IntegerField(default=0)
    curr_n_50 = models.IntegerField(default=0)
    curr_n_100 = models.IntegerField(default=0)
    curr_n_200 = models.IntegerField(default=0)
    curr_n_500 = models.IntegerField(default=0)
    curr_n_2000 = models.IntegerField(default=0)

    curr_c_1 = models.IntegerField(default=0)
    curr_c_2 = models.IntegerField(default=0)
    curr_c_5 = models.IntegerField(default=0)
    curr_c_10 = models.IntegerField(default=0)

    curr_cash = models.FloatField(null=False,blank=True)
    curr_bank = models.FloatField(null=False,blank=True)
    updated_cash = models.FloatField(null=False,blank=True)
    updated_bank = models.FloatField(null=False,blank=True)

    remarks = models.TextField(default="By Cash")
    created_time = models.TimeField(default=timezone.now)

    def clean(self):
        
        b = Balance.objects.all()[0]
        self.curr_bank = b.bank
        self.curr_cash =  b.cash
        
        notes = [i.strip() for i in 'n_10, n_20 , n_50, n_100 , n_200 , n_500,n_2000 ,c_1 , c_2 , c_5, c_10'.split(',')]

        cr = self.transact_type=="Cr" 

        if(not self.pk):
            
            v_num = str(len(Voucher.objects.filter(voucher_type = self.voucher_type).all()) + 1)
            v_num = self.voucher_type[0] + "0"*(5-len(v_num)) + v_num 

            self.voucher_number = self.voucher_number if(self.custom_num) else v_num

            #validations

            if(self.voucher_type!="Contra"):
                b.cash += self.amount if(cr) else -self.amount

                for n in notes:
                    setattr(self, f"curr_{n}" , eval(f"b.{n}"))
                    setattr(b,n, eval(f"b.{n}+self.{n} if(cr) else b.{n}-self.{n}") )
                    

                #check if the total notes amount == entered amount            
                total_amt = sum([int(n.split('_')[1]) * getattr(self,n) for n in notes]) != self.amount
                if(total_amt):
                    raise forms.ValidationError("Notes doesn add up to the amount entered")
                
            
                #if we are debiting
                if(not cr):
                    #check cash notes are avaliable in quota
                    available_check = False in [getattr(self,n)<=getattr(b,n) for n in notes]
                    if(available_check):
                        raise forms.ValidationError("Cash Quota is not available ")

                    #check if available cash >= amount
                    transact_posible = b.cash >= self.amount
                    if(available_check):
                        raise forms.ValidationError("Cash Balance is not available")

                

            else:
                if(cr):
                    b.cash -= self.amount
                    b.bank += self.amount

                    for n in notes:
                       setattr(b,n, eval(f"b.{n} - self.{n}")) 

                    #check if the total notes amount == entered amount            
                    total_amt = sum([int(n.split('_')[1]) * getattr(self,n) for n in notes]) != self.amount
                    if(total_amt):
                        raise forms.ValidationError("Notes doesn add up to the amount entered : {total_amt}")
                    
                    #check cash notes are avaliable in quota
                    available_check = False in [getattr(self,n)<=getattr(b,n) for n in notes]
                    if(available_check):
                        raise forms.ValidationError("Cash Quota is not available" )

                    #check if available cash >= amount
                    transact_posible = b.cash >= self.amount
                    if(available_check):
                        raise forms.ValidationError("Cash Balance is not available")


                    
                else:
                    if(b.bank>=self.amount):
                        b.bank -= self.amount
                    else:
                        raise forms.ValidationError("Bank Doesnt have enough balance ..")

            b.save()

            self.updated_cash = b.cash
            self.updated_bank = b.bank
        
        #IF Updating existing voucher
        else:

            old_version = Voucher.objects.get(id = self.pk)
            diff_amt = self.amount - old_version.amount 
            p_vchrs = Voucher.objects.filter(id__gt = self.pk) 

            note_diff = [ getattr(self,n) - getattr(old_version,n) for n in notes]
            for i, n_diff in enumerate(note_diff):
                exec( f"b.{notes[i]} += {n_diff}" )

            if(self.voucher_type=="Contra"):
                if(cr):
                    self.updated_bank += diff_amt
                    self.updated_cash -= diff_amt
                    b.cash -= diff_amt
                    b.bank += diff_amt

                    for v in p_vchrs:
                        exec(f"v.curr_cash -= diff_amt")
                        exec(f"v.updated_cash -= diff_amt")
                        exec(f"v.curr_bank += diff_amt")
                        exec(f"v.updated_bank += diff_amt")
                        v.save()

                else:
                    self.updated_bank -= diff_amt
                    self.updated_cash += diff_amt
                    b.cash += diff_amt
                    b.bank -= diff_amt

                    for v in p_vchrs:
                        exec(f"v.curr_cash += diff_amt")
                        exec(f"v.updated_cash += diff_amt")
                        exec(f"v.curr_bank -= diff_amt")
                        exec(f"v.updated_bank -= diff_amt")
                        v.save()
                
            else:
                if(cr):
                    self.updated_cash += diff_amt
                    b.cash += diff_amt

                    for v in p_vchrs:
                        exec(f"v.curr_cash += diff_amt")
                        exec(f"v.updated_cash += diff_amt")
                        v.save()

                else:
                    self.updated_cash -= diff_amt
                    b.cash -= diff_amt

                    for v in p_vchrs:
                        exec(f"v.curr_cash -= diff_amt")
                        exec(f"v.updated_cash -= diff_amt")
                        v.save()
            
            b.save()

        # super(Voucher, self).save(*args, **kwargs)



    def __str__(self):
        return str(self.voucher_number)


#COMPONENTS

#fcash Details Section
class Cheque_details(models.Model):
    bank = models.ForeignKey(Bank_Choice, to_field='bank_choice',related_name='receript_bank_choice',on_delete=models.CASCADE,null = True)
    branch = models.ForeignKey(Branch_Choice, to_field='branch_choice',related_name='receipt_branch_choice',on_delete=models.CASCADE,null = True)
    cheque_number= models.CharField(max_length=20,null=False,blank =True)
    cheque_date = models.DateTimeField(null=False,blank=True)
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE,null = True)
    created_time = models.TimeField(default=timezone.now)

    def __str__(self):
        return self.cheque_number    

#Cash Details Section
class cash_notes(models.Model):
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE,null = True)

     # Notes Details
    _10 = models.IntegerField(default=0)
    _20 = models.IntegerField(default=0)
    _50 = models.IntegerField(default=0)
    _100 = models.IntegerField(default=0)
    _200 = models.IntegerField(default=0)
    _500 = models.IntegerField(default=0)
    _2000 = models.IntegerField(default=0)

#Particulars Section
class VoucherParticulars(models.Model):
    name = models.CharField(max_length=200,null=False,blank= True)
    amount = models.IntegerField(default=0)
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE,null = True)
    created_time = models.TimeField(default=timezone.now)
    def __str__(self):
        return self.name    


#Heads Section
class VoucherHead(models.Model):
    head = models.CharField(max_length=200,null=False,blank= True)
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE,null = True)

    def __str__(self):
        return self.head

#$$$$$ COMPONENTS ///////////



#---cash collection by cashier
class cash_collection(models.Model):
    bill_number = models.IntegerField(default = get_cashcol_billnum, null = True , unique=True)
    date = models.DateTimeField(default=timezone.now)
    
    employee = models.ForeignKey(employee_interview,null=True,blank=True,on_delete=models.CASCADE)
    
    total_society_deposit =  models.FloatField(null = True , blank= True)
    total_loan_deposit =  models.FloatField(null = True , blank= True)
    
    tot_reciept = models.IntegerField(default = 0, null = True , blank= True)
    tot_payment = models.IntegerField(default = 0, null = True , blank= True)
    total_cash_collection = models.IntegerField(default = 0, null = True , blank= True)
    
    approved = models.BooleanField(default=False)
    remarks = models.TextField(null=True, blank=True)
    created_time = models.TimeField(default=timezone.now)

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

    class Meta:
        unique_together = ('employee', 'date',)
        

    def clean(self):
        if(self.total_society_deposit or self.total_loan_deposit):
            notes = [i.strip() for i in 'n_10, n_20 , n_50, n_100 , n_200 , n_500,n_2000 ,c_1 , c_2 , c_5, c_10'.split(',')]
            #check if the total notes amount == entered amount            
            total_amt = sum([int(n.split('_')[1]) * getattr(self,n) for n in notes]) != (self.total_cash_collection)
            if(total_amt):
                raise forms.ValidationError({'total_loan_deposit': ['Notes dont add up to the amount']})
        
        # if self.PaymentInline:
        #     print(self.inlines.name)
        #     raise forms.ValidationError({'total_loan_deposit': ['Yea totally']})
        # else:
        #     print("OFFO")
        
class emp_payments(models.Model):
    name = models.CharField(max_length=100) 
    TYPE = models.CharField(max_length=100,choices = ( ("Society Payment",("Society Payment")), ("Loan Payment",("Loan Payment")) , ("Expense",("Expense")) , ("Other",("Other")) ) )
    amount = models.IntegerField(default=0)
    cash_col = models.ForeignKey(cash_collection ,null=True,on_delete=models.CASCADE , blank =True)


class UploadDocs(models.Model):
    
    id_num = models.CharField(max_length=100, help_text="""
    Hint :<br><br>
    Nomination Certificate : Nomination Number <br>
    Cash Collection : Employee Nomination Number<br>
    Diary : Society / Loan Account number<br>
    Maturity : Society Account number<br>
    Loan NOC : Loan Account Number  <br>
    FD Bond : Society ACC no.<br>
    Other : for ther documents<br><br>
    """)
    doc = models.FileField(upload_to ='docs/') 
    TYPE = models.CharField(max_length=100,choices = ( 
    ("Nomination Certificate",("Nomination Certificate")),
    ("Cash Collection",("Cash Collection")) , 
    ("Loan NOC",("Loan NOC")) , 
    ("Maturity",("Maturity")),
    ("FD Bond",("FD Bond")),
    ("Loan Diary",("Loan Diary")), 
    ("Society Diary",("Society Diary")), 
    ("Loan Monthly / Onetime Reciept",("Loan Monthly / Onetime Reciept")), 
    ("Other",("Other")),
    ))
    type_other = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    created_time = models.TimeField(default=timezone.now)

    def clean(self):

        if self.TYPE == "Other":
            if not self.type_other:
                raise forms.ValidationError('Please provide other document type details.')

    def save(self, *args, **kwargs):
        
        f = finance_table.objects.filter(loan_account_number=self.id_num).exists()
        d = deposits_table.objects.filter(society_account_number =self.id_num).exists()
        e = employee_interview.objects.filter(nomination_number =self.id_num).exists()
        c =  client.objects.filter(nomination_number =self.id_num).exists()

        if(f or d or e or c):
            super(UploadDocs, self).save(*args, **kwargs)

        else:
            raise forms.ValidationError("ID not Recognized")

    def __str__(self):
        return self.id_num

    

# Component
class Documents(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100 , choices=(
        ("Recieved","Recieved"),
        ("Dispatched","Dispatched")
    ), default='Recieved')

    Submit_date = models.DateTimeField(default=timezone.now)
    remarks  = models.TextField(default="None")
    created_time = models.DateTimeField(default=timezone.now)
    
    cli = models.ForeignKey(finance_table, on_delete=models.CASCADE,null = True)

    def save(self, *args, **kwargs):
        # print("DOC SAVE")
        super(Documents, self).save(*args, **kwargs)
        # return HttpResponseRedirect('/bank/transit/document/' + self.cli.person.nomination_number)

# class CounterAndTime(models.Model):
#     timestamp = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
#     total_prints = models.IntegerField(default=0, null=False)
#     documentprintcounter = models.ForeignKey('DocumentPrintCounter', on_delete=models.CASCADE, null=True)

# class DocumentPrintCounter(models.Model):
#     document_name = models.CharField(max_length=200, null=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)

class DocumentPrint(models.Model):
    doc_name = models.CharField(max_length=200, null=True)
    doc_for = models.CharField(max_length=200, null=True)
    printed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)

