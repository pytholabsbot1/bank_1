from datetime import date, timedelta
from django.contrib import admin
from employee.models import *
from django.http import HttpResponseRedirect
# from django.contrib.auth.models import Permission
from django.utils.safestring import mark_safe
from django.contrib import messages
import base64

# components part

def custom_titled_filter(title):
    class Wrapper(admin.FieldListFilter):
        def _new_(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title
            return instance
    return Wrapper


fields_basic = (('nomination_number','entry_date'),('first_name','last_name'),('father_name', 'mother_name'),('current_address','permanent_address'),('village','area'),('age','gender','date_of_birth'),
               ('district','state','country'),('city','pincode','email_id'),('mobile_number_1','mobile_number_2','landline_number'),
               ('photograph','signature','thumb_impression'))

fields_id = (('id_type','id_number'),('id_photograph1','id_photograph2'),('id_photograph3','id_photograph4'))

class GaurantorAdmin(admin.ModelAdmin):

    readonly_fields = ('no_finance',)

    search_fields = ('name',)
    list_display = ('name',"father_name","contact","address",'no_finance',"expected_amount","max_amount")
    
    class Media:
        css = {
        'all': ('employee/styles.css',)
         }
        js = (
            "employee/jquery.js",
            'employee/client.js',
        )

class RedirectHome(admin.ModelAdmin):

    'Redirect all admin forms to homepage after redirect'
    def response_post_save_add(self, request, obj):
        """This makes the response after adding go to another apps changelist for some model"""
        # super(EmployeeInterview, self).response_post_save_change(request, obj)
        return HttpResponseRedirect('/bank')

 
class AutoFillAgent(admin.ModelAdmin):
    class Media:
        js = (
            "https://code.jquery.com/jquery-3.4.1.min.js",
            'employee/m1.js',
            'employee/client.js'   # app static folder
        )


class SchemeAdmin(admin.ModelAdmin):
    readonly_fields = ('per_day_roi',)


class DPChoiceAdmin(admin.ModelAdmin):
    readonly_fields = ('amount',)

class FCChoiceAdmin(admin.ModelAdmin):
    readonly_fields = ('amount',)

# components part //////////////////////////


# ___________________________________________________
# Main Tables
# ___________________________________________________

# Custom Deposit_collection Amdin Models
class collection_depositAdmin(admin.ModelAdmin):

    exclude = ('agent_name','person')
    search_fields = ('deposit__society_account_number',)
    list_display = ('bill_no','sc_num','payment_received_date',"created_time",'payment_received',)
    readonly_fields = ("bill_no","payment_received_date")
    
    def response_post_save_add(self, request, obj):
        
        pmt_recieved = round(obj.payment_received ,3 )
        obj.agent_name = employee_interview.objects.get(nomination_number=request.user.username)
        client = obj.deposit.person
        obj.latest_intrest = round(obj.latest_intrest , 3)
        obj.person = client
        obj.save()

        #update in employee records
        e = employee_interview.objects.get(nomination_number=request.user.username)   
        e.deposit_coll += pmt_recieved
        e.save()

        #update the deposit balance
        d = deposits_table.objects.get(id= obj.deposit.id)
        d.interest_collected = obj.latest_intrest
        d.balance =  d.balance+pmt_recieved
        d.save()
        print(d.balance ,'saved' , obj.payment_received)

        #update for admin insights in category
        c = DepositChoice.objects.get(id=obj.deposit.category.id)
        c.amount += pmt_recieved
        c.save()

        if (d.status == "DEACTIVE" or d.status=="HOLD"):
            if (d.balance > 0):
                d.status == "ACTIVE"
                d.save()
                print("THE ACCOUNT HAS BEEN ACTIVATED AGAIN")

        return HttpResponseRedirect('/bank')

    class Media:
        js = (
            "employee/jquery.js",
            'employee/qr.js',   # app static folder
            'employee/deposit_collection2.js'
        )



    raw_id_fields = ("deposit",'agent_name',)
    


# Custom Finance_collection Amdin Models
class collection_financeAdmin(admin.ModelAdmin):
    raw_id_fields = ("finance",)
    exclude = ('agent_name','person')
    search_fields = ('finance__finance__loan_account_number',)
    list_display = ('bill_no','finance','loan_emi_received_date',"created_time",'loan_emi_received','penalty')

    # def response_pre_save_add(self, request, obj):
    #     print("OUT")
    #     if(obj.finance.emi_amount != obj.loan_emi_received):
    #         print("TEST")
    #         return HttpResponse("EMI AMOUNT IS WRONG")

    def response_post_save_add(self, request, obj):

        # < -- For limiting the Emi Amount -->        
        # if(obj.finance.emi_amount != obj.loan_emi_received):
        #     return HttpResponse("EMI AMOUNT IS WRONG")

        obj.agent_name = employee_interview.objects.get(nomination_number=request.user.username)
        client = obj.finance.finance.person
        obj.person = client
        obj.save()
        
        emi_recieved = round(obj.loan_emi_received ,2)
        print(request.user.username)
        e = employee_interview.objects.get(nomination_number=request.user.username)
        e.finance_coll += emi_recieved
        e.save()

        c = FinanceChoice.objects.get(id=obj.finance.finance.loan_type.id)
        c.amount += emi_recieved
        c.save()

        fc = approved_finance_table.objects.get(id=obj.finance.id)
        fc.recieved += emi_recieved
        fc.save()

        if fc.recieved>=fc.total:
            fc.status = "DEACTIVE"
            fc.save()
            return HttpResponseRedirect('/bank/transit/noc/'+ obj.finance.finance.loan_account_number)

        if not (fc.finance.emi_type == "Daily"):
            return HttpResponseRedirect('/bank/transit/financecollection/'+ str(obj.id))
        else:
            return HttpResponseRedirect('/bank/')
            

    class Media:
        js = (
            "employee/jquery.js",
            'employee/qr.js',   # app static folder
            'employee/deposit_collection2.js'
        )


class PaymentInline(admin.StackedInline):
    model = emp_payments
    extra = 0

class Collection_Cashier(admin.ModelAdmin):
    inlines = [PaymentInline,]
    exclude = ('employee',)
    search_fields = ('bill_number',)
    list_display = ('bill_number',"created_time",'date','employee','total_society_deposit','total_loan_deposit','total_cash_collection','approved')
    readonly_fields = ("bill_number" ,)
    def get_form(self, request, obj=None, **kwargs):
        
        m_fields = ('bill_number','date') 
        
        if request.user.has_perm('change_cash_collection'):
            m_fields = m_fields + ('approved',)

        #Field Groups
        self.fieldsets = (
            (None, {
            'fields': m_fields
            }),
            ('Reciepts', {
                'fields': ('total_society_deposit','total_loan_deposit','total_cash_collection','remarks',)
            }),
            ('Cash', {
            'fields': (('n_10','n_20','n_50','n_100'),
                        ('n_200','n_500','n_2000'),)
            }),
            ('Coins', {
                'fields': ('c_1','c_2','c_5','c_10')
            }),
        )

        return super(Collection_Cashier, self).get_form(request, obj, **kwargs)


    def response_post_save_add(self, request, obj):
        obj.tot_payment = sum([i[0] for i in obj.emp_payments_set.all().values_list('amount')])
        obj.tot_reciept = obj.total_society_deposit + obj.total_loan_deposit
        obj.employee = employee_interview.objects.get(nomination_number=request.user.username)

        obj.save()
        return HttpResponseRedirect('/bank/')

    def response_post_save_change(self, request, obj):
        obj.tot_payment = sum([i[0] for i in obj.emp_payments_set.all().values_list('amount')])
        obj.tot_reciept = obj.total_society_deposit + obj.total_loan_deposit
        obj.save()
        
        return HttpResponseRedirect('/bank/transit/cash_col/'+ str(obj.bill_number))
    
    def get_changeform_initial_data(self, request):
        print("---->> ",request.GET)
        e = employee_interview.objects.filter(nomination_number=request.user.username)
        if(e):
            emp = e.first()
            d_ = emp.collection_deposit_set.filter(payment_received_date=timezone.now()).values_list('payment_received')  
            f_ = emp.collection_finance_set.filter(loan_emi_received_date=timezone.now()).values_list('loan_emi_received')


            l1 = emp.collection_deposit_set.values_list('payment_received_date',flat=True) 
            l2 = emp.collection_finance_set.values_list('loan_emi_received_date',flat=True)
            colls = emp.cash_collection_set.all().values_list('date',flat=True)

            dp_dates = list(l1) +list(l2)
            f1_ = list(filter((timezone.now().date()).__ne__, dp_dates))
            rest_dates = [i for i in f1_ if(i not in colls)]
            d = list(colls)
            strings = [date_obj.strftime('%Y-%m-%d') for date_obj in rest_dates]
            strings = list(dict.fromkeys(strings))
            ul_list = ""
            for s in strings:
                message = 'id_date='+ s
                message_bytes = message.encode('ascii')
                base64_bytes = base64.b64encode(message_bytes)
                base64_message = base64_bytes.decode('ascii')
                li = '<li class="warning" style="width: 25%; margin: 0; line-height: 80%; border-bottom: 0.4px solid #eeb80f"><a href="/admin/employee/cash_collection/add#'+ base64_message +'">' + s + '</a></li>'
                ul_list += li
            # ul_list = '<ul>' + ul_list + '</ul>'

            if(ul_list):
                print("ye")
                messages.error(request, mark_safe(f'You Havent Submitted for Dates {ul_list}'))
            else:
                print("neaaa")
            return {'total_loan_deposit': sum([i[0] for i in f_]) ,'total_society_deposit' : sum([i[0] for i in d_]), "remarks" : "None", "total_cash_collection": (sum([i[0] for i in f_])+sum([i[0] for i in d_]))}

    class Media:
        js = (
            "employee/jquery.js",
            "employee/cash_col.js",
        )



# Custom Finance_collection Amdin Models
class withdrawl(admin.ModelAdmin):
    
    raw_id_fields = ("society_account",)
    search_fields = ('bill_no','society_account__society_account_number')
    list_display = ('bill_no','society_account','amount_withdrawl_date',"created_time",'category','paymode')
    readonly_fields = ('image_tag','sign_tag','bill_no','amount_withdrawl_date')

    def get_changeform_initial_data(self, request):
        print("---->> ",request.GET)

        if(request.GET):
            dp =  deposits_table.objects.get(society_account_number = request.GET['num'])
            k_ = {'society_account':dp.id , 
            "holder_name" : f'{dp.person.first_name} {dp.person.last_name}' ,
            'available_amount': dp.balance , 
            'intrest_amount' : dp.interest_collected,}
            return k_


    def response_post_save_add(self, request, obj):
        sc = deposits_table.objects.get(id=obj.society_account.id)
        if(obj.category=="Maturity"):     
            
            sc.status = "DEACTIVE"
            sc.save()

            return HttpResponseRedirect('/bank/transit/withdrawl/'+ str(obj.bill_no))
        if (obj.category=="withdraw"):
            print("WITHDRAW")
            print(sc.balance)
            if (sc.balance <= 0):
                # sc = deposits_table.objects.get(id=obj.society_account.id)
                sc.status = "DEACTIVE"
                sc.save()
                print("ACCOUNT DEACTIVATED BECAUSE OF ZERO BALANCE")
                return HttpResponseRedirect('/bank')
            
            return HttpResponseRedirect('/bank')

    class Media:
        js = (
            "employee/jquery.js",
            "employee/load_pics.js",
            "employee/withdrawl.js"
        )

     #Field Groups
    fieldsets = (
        ("Info", {
           'fields': ('image_tag','sign_tag','bill_no','amount_withdrawl_date','category','society_account')
        }),
        ('Details', {
            'fields': ('holder_name','available_amount','amount_withdrawl',
                    'intrest_amount','deduction_amount',('paymode','cheque_no'))
        }),
         ('Cash', {
           'fields': (('n_10','n_20','n_50','n_200'),
                    ('n_100','n_500','n_2000'),'remarks',)
        }),

        ('Coins', {
           'fields': ('c_1','c_2','c_5','c_10')
        }),
    )


# ---------------------------- VOUCHERS SECTION


class ChequeInline(admin.StackedInline):
    model = Cheque_details
    extra = 0

class ParticularsInline(admin.StackedInline):
    model = VoucherParticulars
    extra = 1

class HeadInline(admin.StackedInline):
    model = VoucherHead
    extra = 2

class VoucherAdmin(admin.ModelAdmin):
    inlines = [ParticularsInline ,ChequeInline ]
    readonly_fields = ("date",)
    list_display = ('voucher_number' , 'account_number', 'date',"created_time" ,'voucher_type' ,'title','amount','transact_type')
    

    
    def get_changeform_initial_data(self, request):
        print("---->> ",request.GET)
        b = Balance.objects.all()[0]
        return {"curr_cash":b.cash , "curr_bank": b.bank}

    class Media:
        js = (
            "employee/voucher.js",
        )
    def get_form(self, request, obj=None, **kwargs):
        
        v_head = ('voucher_number' ,'updated_cash' , 'updated_bank') if( request.user.is_superuser ) else ()

        #Field Groups
        self.fieldsets = (
            (None, {
            'fields': v_head + ('date','transact_type','db','voucher_type',('curr_cash','curr_bank'),'title',('head','sub_head'),'amount','remarks')
            }),
            ("Cash Info",{
                'fields': (('n_10','n_20','n_50','n_200'),
                        ('n_100','n_500','n_2000'),)
            }),
            ('Coins', {
            'fields': ('c_1','c_2','c_5','c_10')
            }),
        )
        

        return super(VoucherAdmin, self).get_form(request, obj, **kwargs)


class UploadAdmin(admin.ModelAdmin):
    search_fields = ['id_num',]
    list_display = ['id_num',"created_time",'TYPE','date', 'type_other']
    readonly_fields = ('date',)

    class Media:
        js = (
            "employee/uploaddoc.js",
        )
