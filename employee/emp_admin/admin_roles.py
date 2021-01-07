from django.contrib import admin
from employee.models import *
from django.http import HttpResponseRedirect
import datetime
from dateutil.relativedelta import relativedelta
from .admin_comp import *
from PIL import Image
from django import forms

# Components
class DocumentInline(admin.StackedInline):
    readonly_fields = ("Submit_date",)

    model = Documents
    extra = 1

# class GaurantorInline(admin.StackedInline):
#     model = Gaurantor
#     extra = 0
    
# ///Components

class ClientAdmin(AutoFillAgent):
    readonly_fields = ("nomination_number","entry_date")

    def response_post_save_add(self, request, obj):
        #create thumbnail of the profile pic
        image = Image.open(obj.photograph.url[1:])
        image = image.resize((200,200), Image.ANTIALIAS)
        image.save(obj.photograph.url[1:], "png")

        print('saved image')

        obj.agent_name = employee_interview.objects.get(nomination_number=request.user.username)
        obj.save()

        return HttpResponseRedirect('/bank/transit/client/'+obj.nomination_number)
        

    # Search Fields in list view
    search_fields = ('nomination_number','first_name','last_name','mobile_number_1','area',)

    list_display = ('image_tag','entry_date','nomination_number','branch','first_name','last_name','father_name','mobile_number_1','area')


    # Fields to be shown in forms
    fields1 = (('account_nominee_name','nominee_relation',),
                ('nomination_fees','sharing_amount','no_of_shares'),'remarks',)

    guardian_fields = ('minor_checkbox',('guardian_name','guardian_address',),'guardian_relation',)
    
    #Field Groups
    fieldsets = (
        ('Personal Details', {
           'fields': fields_basic
        }),
        ('Id Details', {
           'fields': fields_id,
        }),
        ('Guardian Details', {
            'fields': guardian_fields,
            # 'classes': ['collapse in',]
        }),
        ('Other Details', {
            'fields': fields1,
        }),
    )
    class Media:
        js = (
            # "employee/jquery.js",
            'employee/guardian.js',   # app static folder
        )
        css = {
        'all': ('employee/styles.css',)
         }

    
    
class EmployeeJoining(RedirectHome):

    def get_person(self, obj):
        return  obj.employee.first_name 

    def response_post_save_add(self, request, obj):
        return HttpResponseRedirect('/bank/transit/id_card/'+obj.employee.nomination_number)

    def response_post_save_change(self, request, obj):
         return HttpResponseRedirect('/bank/transit/id_card/'+obj.employee.nomination_number)
    
    raw_id_fields = ("employee",)

    search_fields = ('employee__nomination_number','employee__first_name',)
    


class EmployeeInterview(RedirectHome):

    table_fields = (('interview_date'),)
    readonly_fields = ('nomination_number',)

    def response_post_save_add(self, request, obj):
        #create thumbnail of the profile pic
        image = Image.open(obj.photograph.url[1:])
        image = image.resize((200,200), Image.ANTIALIAS)
        image.save(obj.photograph.url[1:], "png")

        return HttpResponseRedirect('/bank')

    def response_post_save_change(self, request, obj):
        # Delete the user is status is false
        if(not obj.status):         
            try:
                u = User.objects.get(username = obj.nomination_number)
                u.delete()
            except:
                pass

        return HttpResponseRedirect('/bank')

    

    referal_fields = (('referal_name','referal_father'),('referal_mobile_number','referal_address'),('referal_photograph','referal_signature','ref_id_1','ref_id_2'),)

    document_fields = (('upload_id_1','upload_id_2'),('upload_bank_passbook','upload_cheque','upload_stamp_paper'),)
   # fields = fields_basic + table_fields

    fieldsets = (
        ('Personal Details', {
           'fields': fields_basic +  table_fields 
        }),
        ('Referal Details', {
            'fields': referal_fields,
        }),
        ('Documents Upload',{
            'fields':document_fields,
        }),
    )

    search_fields = ('nomination_number','first_name','last_name','mobile_number_1','area',)

    list_display = ('image_tag',"created_time",'entry_date','nomination_number','first_name','last_name','mobile_number_1','area','joined')
    
    class Media:
        js = (
            "employee/jquery.js",
            'employee/client.js',
        )
        css = {
        'all': ('employee/styles.css',)
         }
    
 



# Custom Finance Admin Models
class FinanceTable(AutoFillAgent):

    readonly_fields = ('loan_account_number','agent_name',)

    inlines = [DocumentInline,]

    def response_post_save_add(self, request, obj):
        g = Gaurantor.objects.get(id=obj.gaurantor.id)
        g.no_finance += 1
        g.max_amount += obj.expected_amount
        g.save()
        obj.agent_name = employee_interview.objects.get(nomination_number=request.user.username)
        obj.save()
        # print(obj.Documents)
        return HttpResponseRedirect('/bank/')


    def get_person(self, obj):
        return  obj.person.first_name + ' ' + str(obj.person.last_name)

    def get_img(self, obj):
        return obj.person.image_tag()
    get_person.short_description = 'Client'


     # Search Fields in list view
    search_fields = ('loan_account_number','person__first_name',)
    list_display = ('get_img','applied_date',"created_time",'loan_account_number','expected_amount','get_person','category',)


    # Fields to be shown in forms
    table_fields = ('person',('loan_account_number'),('demanded_amount','loan_duration'),
                    ('duration_type','emi_type'),'loan_type',
                    ('stamp_photograph','cheque_photograph'),
                    ('category'),('expected_date','expected_amount'),
                    )
    guarantor_field = (('guarantor_name','guarantor_photograph'),('guarantor_address','guarantor_relation'),'guarantor_signature','agent_name')

    raw_id_fields = ("person","gaurantor")

   
    #Field Groups for form view
    fieldsets = (
        ('Details', {
           'fields': table_fields
        }),
        ('guarantor Details', {
            'fields': ('gaurantor','agent_name',)
        }),
    )
    
    class Media:
        js = (
            "employee/jquery.js",
            'employee/finance_table.js',
        )
        css = {
        'all': ('employee/styles.css',)
         }

class DocumentAdmin(admin.ModelAdmin):
    def response_post_save_change(self, request, obj):
        if obj.status == 'Dispatched':
            return HttpResponseRedirect('/bank/transit/document/' + str(obj.id))
        return HttpResponse("SUCCESS")
#Approved finance Table
class ApprovedFinanceAdmin(admin.ModelAdmin):

    def get_person(self, obj):
        return  obj.finance.person.first_name + ' ' + obj.finance.person.last_name

    def get_img(self,obj):
        return obj.finance.person.image_tag()

    def loan_acc(self,obj):
        return obj.finance.loan_account_number

    get_person.short_description = 'Client'

     # On Save 
    def response_post_save_add(self, request, obj):
        
        f = finance_table.objects.get(id=obj.finance.id)
        f.approved = True
        f.save()
        
        return HttpResponseRedirect('/bank/transit/fc/'+str(obj.finance.loan_account_number))
       

     # Search Fields in list view
    search_fields = ('finance__loan_account_number',)

    list_display = ('get_img',"created_time",'loan_start_date','loan_acc','sanctioned_amount','loan_end_date')

    raw_id_fields = ("finance",)
    readonly_fields = ('loan_start_date',)
     #Field Groups
    fieldsets = (
        (None, {
           'fields': ('finance','status','db',)
        }),
        ('Bank Details', {
            'fields': (('client_bank_account_number','client_bank'),('ifsc_code','cheque_number'),)
        }),
         ('Loan Details', {
           'fields': (('loan_start_date'),'sanctioned_amount',
                    ('loan_duration','duration_type','emi_type'),'roi','discount',)
        }),
         ("Others", {
           'fields': ('counter_number','remarks',)
        }),

    )

    class Media:
        js = (
            "employee/jquery.js",
            'employee/finance.js'
        )
        css = {
             'all': ('employee/animate.min.css',)
        }

# Custom Deposit Amdin Models
class DepositTable(RedirectHome , AutoFillAgent):

    readonly_fields = ('society_account_number','agent_name','account_opening_date') 

    def get_person(self, obj):
        return  obj.person.first_name + ' ' + str(obj.person.last_name)
    
    def get_img(self,obj):
        return obj.person.image_tag()
     # On Save 
    def response_post_save_add(self, request, obj):
        obj.agent_name = employee_interview.objects.get(nomination_number=request.user.username)
        obj.save()

        #Cretae collection for the opening amount
        data = {'deposit' : obj,
                'bill_no' : len(collection_deposit.objects.all())+1,
                'agent_name' : obj.agent_name,
                'person' : obj.person,
                'payment_received' : obj.account_opening_amount,
                'previous_balance' : 0,
                'latest_intrest' : 0,
                }  
        collection_deposit(**data).save()

        if(obj.category.name=="FD"):
            return HttpResponseRedirect('/bank/transit/dpFD/'+str(obj.society_account_number))
        else:
            return HttpResponseRedirect('/bank/transit/dp/'+str(obj.society_account_number))
       


    #  Search Fields in list view
    
    search_fields = ('society_account_number',)
    list_display = ('get_img',"created_time",'society_account_number','get_person','balance','account_opening_date','category','status','interest_collected')
    # Fields to be shown in forms

    raw_id_fields = ("person",)

     #Field Groups
    fieldsets = (
        (None, {
           'fields': ('person','society_account_number','status','db')
        }),
        ('Bank Details', {
            'fields': ('client_bank_account_number','client_bank','ifsc_code',
                    ('account_opening_date','account_opening_amount'))
        }),
         ('other details', {
           'fields': ('scheme','maturity_date','category',
                    ('counter_number'),'agent_name','remarks',)
        }),
    )
    class Media:
        js = (
            'employee/deposit.js',
        )