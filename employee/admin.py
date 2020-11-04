from django.contrib import admin
from .models import *
from django.http import HttpResponseRedirect


from employee.emp_admin.admin_comp import *
from employee.emp_admin.admin_roles import * 

admin.site.site_header = "Siddhi Site"
admin.site.site_url = '/bank'


# -----------------------------------Register your models here.--------------------------------------------------------------------

admin.site.register(client,ClientAdmin)                 # Database client model is used for storing credentials of client who wants 
admin.site.register(employee_interview,EmployeeInterview)
admin.site.register(employee_joining,EmployeeJoining)                                           # deposit or take loan from organisation ( client creation form )
admin.site.register(Balance) 
                                            
admin.site.register(Bank_Choice)            # model for adding bank choices 
admin.site.register(Branch_Choice)          # model for adding bank choices 
admin.site.register(Scheme,SchemeAdmin)          # model for adding scheme choices 

admin.site.register(City_Choice)            # model for adding city choices 
admin.site.register(State_Choice)           # model for adding state choices 
admin.site.register(District_Choice)        # model for adding district choices 
admin.site.register(Country_Choice)         # model for adding country choices 
admin.site.register(Relation_Choice)        # model for adding relation choices 
admin.site.register(Id_Type_Choice)         # model for adding id type choices
admin.site.register(UploadDocs,UploadAdmin)   

admin.site.register(finance_table,FinanceTable)
admin.site.register(deposits_table,DepositTable)
admin.site.register(collection_finance , collection_financeAdmin)
admin.site.register(approved_finance_table,ApprovedFinanceAdmin)
admin.site.register(withdrawl_entry,withdrawl)
admin.site.register(cash_collection, Collection_Cashier)
admin.site.register(emp_payments)
admin.site.register(collection_deposit , collection_depositAdmin)

admin.site.register(Gaurantor,GaurantorAdmin)
admin.site.register(Voucher, VoucherAdmin)
admin.site.register(FinanceChoice , FCChoiceAdmin)
admin.site.register(DepositChoice, DPChoiceAdmin)
admin.site.register(Head)
admin.site.register(Sub_Head)
admin.site.register(Documents,DocumentAdmin)

#######DocumentCounter
# admin.site.register(CounterAndTime)
admin.site.register(DocumentPrint)