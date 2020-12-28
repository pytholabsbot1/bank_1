
from django.http import HttpResponseRedirect
from django.shortcuts import render
from employee.models import *
from employee.forms import *
import pdfkit
from itertools import zip_longest
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from itertools import chain
import datetime as dt

def AgentCollection(request,tp):

    tp = request.tp_
    from_date = request.POST.get("from_date")
    to_date = request.POST.get("to_date")

    search_val = request.POST.get("search_val")
    filter_val = request.POST.get("filter_val")
    all_ = request.POST.get("all_") == "on"
    audit = request.POST.get("audit") == "on"

    print(filter_val)

    if(tp=='dp'):
        #processing them into statements -for agentwise deposit collection
        if (all_):
            collections = collection_deposit.objects.all() 
        else:
            collections = employee_interview.objects.get(nomination_number = search_val).collection_deposit_set.all()       
        
        f_ = f",deposit__category__id='{filter_val}'" if(filter_val) else ""
        filter_ = f".filter(payment_received_date__range=['{from_date}','{to_date}'] {f_} )"                 
        audit_fields = ', deposit__db = True )'
        display_fields = ('bill_no','deposit__society_account_number','person__first_name' , 'person__last_name','person__area','payment_received_date','payment_received','deposit__category__name')
        title = 'Deposit Collections'

    else:
            #processing them into statements -for clientwise finance collection
        if(all_):
            collections = collection_finance.objects.all()
        else:
            collections = employee_interview.objects.get(nomination_number = search_val).collection_finance_set.all()        
        
        f_ = f",finance__finance__loan_type__id='{filter_val}'" if(filter_val) else ""
        filter_ = f".filter(loan_emi_received_date__range=['{from_date}','{to_date}'] {f_} )" 
        audit_fields = ', finance__db = True )'
        display_fields = ('bill_no','finance__finance__loan_account_number','person__first_name' , 'person__last_name','person__area','loan_emi_received_date','loan_emi_received','penalty')
        title = 'Finance Collections'


    #if audit is true so show only audit
    filter_ = filter_[:-1] + audit_fields if(audit) else filter_

    rows = eval(f"collections{filter_}.values_list{display_fields}")

    #add to fuckin context
    context = {'headers':display_fields}
    context['rows'] = rows
    context['title'] = title
    print(context['rows'])
    
    #get the table html
    rendered_report = render(request,"employee/table.html",context)
    context['table'] = rendered_report.content.decode('utf-8')
    return context
        

def dividendreport(request):
    f_year = dt.datetime.strptime(request.POST.get("financial_year"),"%Y-%m-%d")
    p = request.POST.get("percentage")
    audit = request.POST.get("audit") == "on"

    display_fields = ('nomination_number' , 'entry_date' ,"first_name" , "last_name" , "father_name" , "mobile_number_1" , "sharing_amount" , "no_of_shares" )

    rows_ =  client.objects.filter(entry_date__range = (f_year , f_year + relativedelta(years=1)) , status=True).values_list(*display_fields)
    rows = [i + ( i[-2] * round(float(p)/100 ,2 ) , )  for i in rows_]

    context = {'headers':[i.replace('_'," ").capitalize() for i in display_fields] + ["Dividend Amt"]}
    context['rows'] = rows
    context['title'] = 'Dividend Report'

    #get the table html
    rendered_report = render(request,"employee/table.html",context)
    context['table'] = rendered_report.content.decode('utf-8')
    return context


def ClientCollection(request):

    tp = request.tp_
    from_date = request.POST.get("from_date")
    to_date = request.POST.get("to_date")
    search_val = request.POST.get("search_val")
    all_ = request.POST.get("all_")
    audit = request.POST.get("audit") == "on"

    if(tp=='dp'):
        #processing them into statements -for agentwise deposit collection
        if (all_):
            collections = collection_deposit.objects.all() 
        else:
            collections = client.objects.get(nomination_number = search_val).collection_deposit_set.all()       
        filter_ = f".filter(payment_received_date__range=['{from_date}','{to_date}'])"                 
        display_fields = ('bill_no','deposit__society_account_number','person__first_name' , 'person__last_name' ,'person__area','payment_received_date','payment_received','deposit__category__name')

    else:
            #processing them into statements -for clientwise deposit collection
        if(all_):
            collections = collection_finance.objects.all()
        else:
            collections = client.objects.get(nomination_number = search_val).collection_finance_set.all()        
        
        filter_ = f".filter(loan_emi_received_date__range=['{from_date}','{to_date}'])" 
        display_fields = ('bill_no','finance__finance__loan_account_number','person__first_name', 'person__last_name' ,'person__area','loan_emi_received_date','loan_emi_received','penalty')

    #if audit is true so show only audit
    filter_ = filter_[:-1] + ', db=True )'if(audit) else filter_

    rows = eval(f"collections{filter_}.values_list{display_fields}")

    #add to fuckin context
    context = {'headers':[i.replace('deposit',"").replace('person',"").replace('finance',"").replace('__',"").replace('_'," ") for i in display_fields]}
    context['rows'] = rows
    context['title'] = 'Client Wise Collections'
    print(context['rows'])
    
    #get the table html
    rendered_report = render(request,"employee/table.html",context)
    context['table'] = rendered_report.content.decode('utf-8')
    return context


# Procedure

# Get list of all fields needed
# Pick best block to fit loan in 
# Headers Shit
# Return shit



def ledger(request):
    from_date = request.POST.get("from_date")
    to_date = request.POST.get("to_date")
    search_val = request.POST.get("nom_num")
    audit = request.POST.get("audit") == "on"
    ledger_for = request.POST.get("Ledger_for")
    print(ledger_for)

    person_fields = ('first_name' , 'last_name','father_name' ,'area','mobile_number_1','current_address')

    ##Loan and Soicety
    if(ledger_for == "Society"):  
        display_fields = ('person__nomination_number','society_account_number','account_opening_date','account_opening_amount','category__name','maturity_date' ,'maturity_amount','scheme__duration','scheme__duration_type' ) 
        if(search_val):
            collections = client.objects.get(nomination_number = search_val).deposits_table_set.all()      
            person_details = eval(f'client.objects.filter(nomination_number = search_val).values_list{person_fields}')[0]
            table_head = ' '.join(person_details[:2]) + '<br>'.join( [str(i) for i in person_details[2:]] )
        else:
            collections = deposits_table.objects.all()
            table_head = "Showing All Deposits"

        filter_ = f".filter(account_opening_date__range=['{from_date}','{to_date}'])"                 
        #if audit is true so show only audit
        filter_ = filter_[:-1] + ', db=True )'if(audit) else filter_

        rows = eval(f"collections{filter_}.values_list{display_fields}")
        m = {}
        for dp_set in rows:
            dp = deposits_table.objects.filter(society_account_number=dp_set[0])
            if(dp and dp.withdrawl_entry_set.all()):
                withdrawls_ = dp.withdrawl_entry_set.all()
                withrawl = withdrawls_[0]
                m[dp_set] = (f'WD : {withrawl.amount_withdrawl_date}' , f'WA : {withrawl.amount_withdrawl}' , f'BL : {dp.balance}' , f'IN : {dp.interest_collected}', "TP: CASH")
            else:
                m[dp_set] = []

        # print(rows)
        #add to fuckin context
        context = {'headers':[i.replace('deposit',"").replace('scheme',"").replace('person',"").replace('finance',"").replace('__',"").replace('_'," ") for i in display_fields]}
    
    else:
        display_fields = ('finance__person__nomination_number','finance__loan_account_number','loan_start_date','total','finance__loan_type__name' ) 
        if(search_val):
            collections = approved_finance_table.objects.filter(finance__person__nomination_number=search_val)       
            person_details = eval(f'client.objects.filter(nomination_number = search_val).values_list{person_fields}')[0]
            table_head = ' '.join(person_details[:2]) + '<br>'.join( [str(i) for i in person_details[2:]] )
        else:
            collections = approved_finance_table.objects.all()
            table_head = "Showing All Finances"

        filter_ = f".filter(loan_start_date__range=['{from_date}','{to_date}'])"                 
        #if audit is true so show only audit
        filter_ = filter_[:-1] + ', db=True )'if(audit) else filter_

        rows = eval(f"collections{filter_}.values_list{display_fields}")
        m = {}
        for fc_set in rows:
            fc = approved_finance_table.objects.filter(finance__loan_account_number=fc_set[1])
            if(len(fc) and fc[0].collection_finance_set.last() ):
                dp= fc[0].collection_finance_set.last()
                dp = deposits
                m[fc_set] = (f'DD : {dp.loan_emi_received_date}' , f'DA : {dp.loan_emi_received}' , f'P : {dp.penalty}' )
            else:
                m[fc_set] = []

        # print(rows)
        #add to fuckin context
        context = {'headers':["Nomination Number","Finance Account" , "Start Date" , "Total Amount" , "Loan Type"]}
    
    
    
    context['ledger'] = m
    context['title'] = table_head
    # print(context['rows'])
    
    #get the table html
    rendered_report = render(request,"employee/table.html",context)
    context['table'] = rendered_report.content.decode('utf-8')
    return context


def cash_report(request):
    from_date = request.POST.get("from_date")
    to_date = request.POST.get("to_date")
    audit = request.POST.get("audit") == "on"

    context = {'headers':['Date','V.No','Ttile' ,"Head" , '10','20','50','100','200','500','2000','Amount' , 'Date','V.No','Ttile' ,"Head" ,'10','20','50','100','200','500','2000','Amount' ]}
    vouchers = Voucher.objects.filter(date__range=[from_date, to_date]).order_by('id')
    if(audit):
        vouchers = vouchers.filter(db=True)

    vcs = {}

    if(vouchers):
        for dt in vouchers.values_list("date",flat=True).distinct():
            closing = vouchers.filter(date=dt).last().updated_cash
            #vcs[unique_date] = [cr_vouchers_of_date] , [dr_vouchers_of_date]
            v_  = vouchers.filter(date=dt).values_list("date","voucher_number","title",'head__value','n_10','n_20','n_50','n_100','n_200','n_500','n_2000','amount')
        
            c_ = v_.filter(transact_type="Cr").exclude(voucher_type="Contra")
    
            d_ = v_.filter(transact_type="Dr").exclude(voucher_type="Contra")
            d_contra = v_.filter(transact_type="Cr",voucher_type="Contra")
            d_ = d_ | d_contra
            # conact the rows of cr and dr if theres no dr
            concat = [x + y for x, y in zip_longest(c_, d_, fillvalue= (tuple([ '-' for i in range(12) ])) ) ]
            
            d_tots = [sum([vchr[i] for vchr in c_]) for i in range(4,12)]
            c_tots = [sum([vchr[i] for vchr in d_]) for i in range(4,12)]

            print(d_tots , c_tots)
            vcs[dt] = {"rows" : concat , "d_tots" : d_tots , "c_tots" : c_tots,"closing": closing}


        context['cash_transact'] = vcs
        context['title'] = ' <p style="float:left;">IN (Reciepts)</p> <p style="float:right;">OUT (Payments)</p>'
        context['Opening'] = ( [getattr(vouchers.first(),i ) for i  in ('curr_n_10','curr_n_20','curr_n_50','curr_n_100','curr_n_200','curr_n_500','curr_n_2000','curr_cash') ] , vouchers.first().date)

 
        #get the table html
        rendered_report = render(request,"employee/table.html",context)
        context['table'] = rendered_report.content.decode('utf-8')
        context['heading'] = 'CASH Report'

    
    return context


def cashbook(request):
    from_date = request.POST.get("from_date")
    to_date = request.POST.get("to_date")
    audit = request.POST.get("audit") == "on"

    context = {'headers':['Date' , 'V.No', "Title" ,'Head','SHead' , 'Amount', "Cheque" ,"Narration" , 'Date' , 'V.No', "Title" ,'Head' ,'SHead' ,'Amount', "Cheque" ,"Narration"]}

    vouchers = Voucher.objects.filter(date__range=[from_date, to_date]).order_by('id')
    if(audit):
        vouchers = vouchers.filter(db=True)
        
    vcs = {}

    if(vouchers):
        for dt in vouchers.values_list("date",flat=True).distinct():
            
            #vcs[unique_date] = [cr_vouchers_of_date] , [dr_vouchers_of_date]
            v_  = vouchers.filter(date=dt).values_list("date","voucher_number","title",'head__value', 'sub_head__value','amount',"cheque_details__cheque_number",'remarks')
            
            closing = vouchers.filter(date=dt).last().updated_cash
            c_ = v_.filter(transact_type="Cr").exclude(voucher_type="Contra")
            # c_contra = v_.filter(transact_type="Dr",voucher_type="Contra")
            # c_ = c_ | c_contra

            d_ = v_.filter(transact_type="Dr").exclude(voucher_type="Contra")
            d_contra = v_.filter(transact_type="Cr",voucher_type="Contra")
            d_ = d_ | d_contra
            # conact the rows of cr and dr if theres no dr
            concat = [x + y for x, y in zip_longest(c_, d_, fillvalue= (tuple([ '-' for i in range(8) ])) ) ]

            vcs[dt] = {"rows" : concat , "c_total": sum(c_.values_list('amount',flat=True)) ,"d_total": sum(d_.values_list('amount',flat=True)) ,"closing": closing} 
            
        vcs = sorted(vcs.items())
        print(dict(vcs))
        # records = [cr_vouchers[i] + dr_vouchers[i]  for i in range(max( len(cr_vouchers), len(dr_vouchers) ))]

        context['cashbook'] = vcs
        context['title'] = ' <p style="float:left;">Cr. (Reciepts)</p> <p style="float:right;">Dr. (Payments)</p>'

 
        #get the table html
        rendered_report = render(request,"employee/table.html",context)
        context['table'] = rendered_report.content.decode('utf-8')
        context['heading'] = 'CASH Report'

    else:
        context['heading'] = 'No Entries'

    return context


def bankTransactions(request):
    from_date = request.POST.get("from_date")
    to_date = request.POST.get("to_date")
    audit = request.POST.get("audit") == "on"

    vouchers = Voucher.objects.filter(date__range=[from_date, to_date],voucher_type="Contra").order_by('id')
    if(audit):
        vouchers = vouchers.filter(db=True)

    vcs = {}

    if(vouchers):
        for dt in vouchers.values_list("date",flat=True).distinct():
            
            #vcs[unique_date] = [cr_vouchers_of_date] , [dr_vouchers_of_date]
            v_  = vouchers.filter(date=dt).values_list("date","voucher_number","title",'head__value', 'sub_head__value','amount',"cheque_details__cheque_number",'remarks')
            
            closing = vouchers.filter(date=dt).last().updated_bank
            c_ = v_.filter(transact_type="Cr")
            d_ = v_.filter(transact_type="Dr")

            # conact the rows of cr and dr if theres no dr
            concat = [x + y for x, y in zip_longest(c_, d_, fillvalue= (tuple([ '-' for i in range(8) ])) ) ]

            vcs[dt] = {"rows" : concat , "c_total": sum(c_.values_list('amount',flat=True)) ,"d_total": sum(d_.values_list('amount',flat=True)) ,"closing": closing} 
            
        vcs = sorted(vcs.items())
        print(dict(vcs))
        # records = [cr_vouchers[i] + dr_vouchers[i]  for i in range(max( len(cr_vouchers), len(dr_vouchers) ))]

        context = {'headers':['Date' , 'V.No', "Title" ,'Head','SHead' , 'Amount', "Cheque" ,"Narration" , 'Date' , 'V.No', "Title" ,'Head' ,'SHead' ,'Amount', "Cheque" ,"Narration"]}
        context['cashbook'] = vcs
        context['Opening'] = (vouchers.first().curr_bank , vouchers.first().date)
        context['title'] = ' <p style="float:left;">Bank IN</p> <p style="float:right;">Bank OUT</p>'
        
        #get the table html
        rendered_report = render(request,"employee/table.html",context)
        context['table'] = rendered_report.content.decode('utf-8')
        context['heading'] = 'Bank Report'
    
    else:
        context = {}
    
    return context


def withdrawls(request):
    print(request.POST)
    from_date = request.POST.get("from_date")
    to_date = request.POST.get("to_date")
    acc_num = request.POST.get("search")
    audit = request.POST.get("audit") == "on"

    mature_withdraws = withdrawl_entry.objects.filter(amount_withdrawl_date__range=[from_date, to_date])
    if(acc_num):
        mature_withdraws = mature_withdraws.filter(society_account__person__nomination_number=acc_num)
    if(audit):
        mature_withdraws = mature_withdraws.filter(society_account__db=True)

    #add remaining balance field
    records = mature_withdraws.values_list("society_account__society_account_number","society_account__person__first_name",'society_account__category','amount_withdrawl_date','amount_withdrawl','society_account__balance',"rest_amount")
    context = {'headers':["Client A/C No","Client Name","Category",	"Withdrawal Date",	"Withdrawal Amount",	"Total DeptAmount","Balance"]}
    context['rows'] = records
    context['title'] = 'Withdrawl Details'

    #get the table html
    rendered_report = render(request,"employee/table.html",context)
    context['table'] = rendered_report.content.decode('utf-8')
    context['heading'] = 'Withdrawl Details'
    return context


def loans(request):
    from_date = request.POST.get("from_date")
    to_date = request.POST.get("to_date")
    acc_num = request.POST.get("search")
    audit = request.POST.get("audit") == "on"
    print(acc_num)

    finances = approved_finance_table.objects.filter(loan_start_date__range=[from_date, to_date])
    if(acc_num):
        finances = finances.filter(finance__person__nomination_number=acc_num)
    if(audit):
        finances = finances.filter(finance__db=True)
    
    records = finances.values_list("finance__loan_account_number","finance__person__first_name",'finance__person__father_name','loan_start_date','loan_end_date','sanctioned_amount','total_intrest_amount','discount')
    context = {'headers':["Client A/C No","Client Name","Fathers Name","StartDate","EndDate","Amount","Interest","Discount"]}
    context['rows'] = records
    context['title'] = ' Loan Details'
    
    #get the table html
    rendered_report = render(request,"employee/table.html",context)
    context['table'] = rendered_report.content.decode('utf-8')
    context['heading'] = 'CASH Report'
    return context


def maturity(request):
    from_date = request.POST.get("from_date")
    to_date = request.POST.get("to_date")
    acc_num = request.POST.get("search")
    audit = request.POST.get("audit") == "on"

    mature_withdraws = withdrawl_entry.objects.filter(amount_withdrawl_date__range=[from_date, to_date],category="Maturity")
    if(acc_num):
        mature_withdraws = mature_withdraws.filter(society_account__person__nomination_number=acc_num)
    if(audit):
        mature_withdraws = mature_withdraws.filter(society_account__db=True)

    records = mature_withdraws.values_list("society_account__society_account_number","society_account__person__first_name",'available_amount','intrest_amount','deduction_amount','society_account__maturity_amount','society_account__maturity_date','paymode','cheque_no')
    # records = [cr_vouchers[i] + dr_vouchers[i]  for i in range(max( len(cr_vouchers), len(dr_vouchers) ))]

    context = {'headers':["Client A/C No","Client Name","NetBalance","Interest"	,"Deduction","MaturityAmount","Maturity Date","PayMode","ChqNo"]}
    context['rows'] = records
    context['title'] = ' Maturity Details'
    
    #get the table html
    rendered_report = render(request,"employee/table.html",context)
    context['table'] = rendered_report.content.decode('utf-8')
    context['heading'] = 'Maturity Report'
    return context


def emp_report(request):
    ''' Report fo Employee Collections'''
    from_date = request.POST.get("from_date")
    to_date = request.POST.get("to_date")
    tp = request.POST.get("filter_val")
    context = {'headers':['bill no','Account no.' , 'Name' ,'Area' ,'Payment', 'Date' , 'Type']}
    
    e = employee_interview.objects.get(nomination_number= request.user.username)
    if(tp=="Deposits"):
	    collections = [ [dp.bill_no , dp.deposit.society_account_number , " ".join([dp.deposit.person.first_name, dp.deposit.person.last_name]) , dp.deposit.person.area ,round(dp.payment_received , 1), dp.payment_received_date ,'Deposit'] for dp in e.employee_interview.collection_deposit_set.filter(payment_received_date=timezone.now())]
    else:
	    collections = [ [fc.bill_no , ' '.join([fc.finance.finance.person.first_name , fc.finance.finance.person.last_name]) , fc.finance.finance.person.area , round(fc.loan_emi_received ,1) , fc.loan_emi_received_date , 'Finance'] for fc in e.employee_interview.collection_finance_set.filter(loan_emi_received_date=timezone.now())]

   
    context['rows'] = collections 
    rendered_report =  render(request,"employee/table.html",context)

    context['table'] = rendered_report.content.decode('utf-8')
    context['heading'] = 'Employee Collections'
    context['off_explore'] = 1
    return context


##New Ones >>>>>>>>>>>>>>>>>>>>>>>

def emi_due(request):
    from_date = request.POST.get("from_date")
    to_date = request.POST.get("to_date")
    acc_num = request.POST.get("search")
    audit = request.POST.get("audit") == "on"
    print(acc_num)
    display_fields = ('finance__loan_account_number' , 'finance__person__first_name' ,'finance__person__last_name' , 'loan_start_date' ,'loan_end_date' , 'sanctioned_amount' ,'loan_duration' ,'emi_amount' ,'duration_type' ,'recieved' , 'finance__agent_name__nomination_number','finance__person__mobile_number_1')
    
    finances = approved_finance_table.objects.all().values_list(*display_fields)
    if(acc_num):
        finances = finances.filter(finance__person__nomination_number=acc_num).values_list(*display_fields)
    rows = []
    for finance in finances:
        t_delta = relativedelta(timezone.now().date(),finance[3])
        timespan = getattr(t_delta , finance[8])

        installments_left  = finance[6] // timespan if(timespan) else 0
        total_due = finance[7] * installments_left
        
        rows.append(finance + (installments_left , total_due ))

    context = {'headers':("Loan Acc." , 'First Name' ,"Last Name" ,"Loan Start Date" ,"Loan End Date" , "Finance Amt" , "Duration" , "EMI Amt" , "Duration Type" , "Recieved" , "agent" , "Mobile" ,"Installments Left" ,"Total Due")}
    context['rows'] = rows 
    rendered_report =  render(request,"employee/table.html",context)

    context['table'] = rendered_report.content.decode('utf-8')
    context['heading'] = 'EMI Due Report'
    return context


def document_dispatch(request):
    from_date = request.POST.get("from_date")
    to_date = request.POST.get("to_date")
    acc_num = request.POST.get("search")

    display_fields = ('cli__loan_account_number','name','status','Submit_date','remarks')
    if(acc_num):
        documents  = finance_table.objects.get(loan_account_number=acc_num).documents_set.all().values_list(*display_fields)
    else:
        documents = Documents.objects.all().values_list(*display_fields)

    context = {'headers':("Document Name" , "Loan ACC" , 'Status' , "Submit Date" ,"Remarks")}
    context['rows'] = documents
    rendered_report =  render(request,"employee/table.html",context)

    context['table'] = rendered_report.content.decode('utf-8')
    context['heading'] = 'Document dispatch Report'
    return context


def daily_report_fc(request):

    from_date = request.POST.get("from_date")
    to_date = request.POST.get("to_date")
    acc_num = request.POST.get("search")

    rows = []

    accounts = approved_finance_table.objects.filter(loan_start_date__range=[from_date , to_date])
    if(acc_num):
        accounts = accounts.filter(finance__agent_name__nomination_number=acc_num)
    

    for acc in accounts:
        name = acc.finance.person.first_name + " " + acc.finance.person.last_name
        rows.append( (acc.finance.loan_account_number , name , acc.finance.person.area, acc.recieved, "0", "0" ) )

    context = {'headers':("Acc Num" , "Name" , 'Area' , "Recieved" ,"D1 __" , "D2__")}
    context['rows'] = rows
    rendered_report =  render(request,"employee/table.html",context)

    context['table'] = rendered_report.content.decode('utf-8')
    context['heading'] = 'Daily Finance Print Report'
    return context

def daily_report_dp(request):

    from_date = request.POST.get("from_date")
    to_date = request.POST.get("to_date")
    acc_num = request.POST.get("acc_num")

    rows = []
    
    accounts =  deposits_table.objects.filter(account_opening_date__range=[from_date ,to_date])
    if(acc_num):
        accounts = accounts.filter(agent_name__nomination_number = acc_num)

    for acc in accounts:
        name = acc.person.first_name + " " + acc.person.last_name
        rows.append( (acc.society_account_number , name , acc.person.area, acc.balance, "0", "0" ) )

    context = {'headers':("Acc Num" , "Name" , 'Area' , "Balance" ,"D1 __" , "D2__")}
    context['rows'] = rows
    rendered_report =  render(request,"employee/table.html",context)

    context['table'] = rendered_report.content.decode('utf-8')
    context['heading'] = 'Daily Deposit Print Report'
    return context


def daily_cash(request):
    print(request.POST)
    from_date = request.POST.get("from_date")
    to_date = request.POST.get("to_date")
    emp = request.POST.get("search")
    rows = []
    cash_collections = cash_collection.objects.filter(date__range=[from_date ,to_date])
    if emp:
        e = employee_interview.objects.get(nomination_number=emp)
        cash_collections = cash_collections.filter(employee=e)
    for c in cash_collections:
        payment_string = ""
        if c.n_10:payment_string += "<li>" + str(c.n_10) + " * 10 = " + str(c.n_10 * 10) + "</li>"
        if c.n_20:payment_string += "<li>" + str(c.n_20) + " * 20 = " + str(c.n_20 * 20) + "</li>"
        if c.n_50:payment_string += "<li>" + str(c.n_50) + " * 50 = " + str(c.n_50 * 50) + "</li>"
        if c.n_100:payment_string += "<li>" + str(c.n_100) + " * 100 = " + str(c.n_100 * 100) + "</li>"
        if c.n_200:payment_string += "<li>" + str(c.n_200) + " * 200 = " + str(c.n_200 * 200) + "</li>"
        if c.n_500:payment_string += "<li>" + str(c.n_500) + " * 500 = " + str(c.n_500 * 500) + "</li>"
        if c.n_2000:payment_string += "<li>" + str(c.n_2000) + " * 2000 = " + str(c.n_2000 * 2000) + "</li>"
        payment_string = "<ul>" + payment_string + "</ul>"
        rows.append((c.date, emp, c.total_society_deposit, c.total_loan_deposit, c.tot_reciept, c.total_loan_deposit + c.total_society_deposit,"",payment_string))
    context = {'headers':("Date","Employee" , "Society Total" , 'Loan Total' , "Reciepts", "Total", "Payment Details", "Currency Details")}
    context['rows'] = rows
    rendered_report =  render(request,"employee/table.html",context)
    context['table'] = rendered_report.content.decode('utf-8')
    context['heading'] = 'Daily cash submit report'
    return context

def upcoming_maturity(request):
    print(request.POST)
    from_date = request.POST.get("from_date")
    to_date = request.POST.get("to_date")
    accounts = deposits_table.objects.filter(maturity_date__range=[from_date ,to_date])
    rows = []
    for a in accounts:
        rows.append((a.person.first_name+" "+a.person.last_name, a.society_account_number, a.balance, a.account_opening_date, a.account_opening_amount, a.person.mobile_number_1, a.interest_collected, a.maturity_amount,a.maturity_interest))
    context = {'headers': ("Client Name", "Account Number", "Balance", "Account Opening Date","Account Opening Amount","Mobile Number", "Interest Collected", "Maturity Amount", "Maturity Interest")}
    context['rows'] = rows
    rendered_report =  render(request,"employee/table.html",context)
    context['table'] = rendered_report.content.decode('utf-8')
    context['heading'] = 'Upcoming Maturity report'
    return context

def account_status(request):
    status = request.POST.get("status")
    actype = request.POST.get("account_type")
    rows = []
    if actype:
        if actype=="DEPOSIT":
            accounts = deposits_table.objects.filter(status=status)
            for a in accounts:
                try: 
                    last_dep = str(a.collection_deposit_set.last().created_time) + " - " + str(a.collection_deposit_set.last().payment_received)
                except:
                    last_dep = 'No collections'
                try:
                    last_with = str(a.withdrawl_entry_set.last().created_time) + " - " + str(a.withdrawl_entry_set.last().amount_withdrawl)
                except:
                    last_with = 'no withdrawls'
                rows.append((a.person.first_name+" "+a.person.last_name, a.society_account_number, a.balance, a.account_opening_date, a.account_opening_amount, a.person.mobile_number_1, a.interest_collected, last_dep, last_with ))
                context = {'headers': ("Client Name", "Account Number", "Balance", "Account Opening Date","Account Opening Amount","Mobile Number", "Interest Collected","Last Deposit", "Last withdrawl")}
        if actype=="LOAN":
            accounts = approved_finance_table.objects.filter(status=status)
            for a in accounts:
                try: 
                    last_col = str(a.collection_finance_set.last().created_time) + " - " + str(a.collection_finance_set.last().loan_emi_received)
                except:
                    last_col = 'No collections'
                rows.append((a.finance.person.first_name+" "+a.finance.person.last_name, a.finance.loan_account_number, a.recieved, a.loan_start_date, a.total, a.finance.person.mobile_number_1, a.total_intrest_amount, last_col))
                context = {'headers': ("Client Name", "Account Number", "Recieved", "Loan Start Date","Loan Total","Mobile Number", "Interest Amount","Last EMI")}
        else:
            deps = deposits_table.objects.filter(status=status)
            loans = approved_finance_table.objects.filter(status=status)
            accounts = list(chain(deps, loans))
        context['rows'] = rows
        rendered_report =  render(request,"employee/table.html",context)
        context['table'] = rendered_report.content.decode('utf-8')
        context['heading'] = 'Account Status Report'
        return context

def mycashreport(request):
    from_date = request.POST.get("from_date")
    to_date = request.POST.get("to_date")
    audit = request.POST.get("audit") == "on"
    rows = []
    e = employee_interview.objects.get(nomination_number=request.user)
    cash_collections = cash_collection.objects.filter(date__range=[from_date ,to_date], employee=e)
    for c in cash_collections:
        payment_string = ""
        if c.c_1:payment_string += "<li>C " + str(c.c_1) + " * 1 = " + str(c.c_1 * 1) + "</li>"
        if c.c_2:payment_string += "<li>C " + str(c.c_2) + " * 2 = " + str(c.c_2 * 2) + "</li>"
        if c.c_5:payment_string += "<li>C " + str(c.c_5) + " * 5 = " + str(c.c_5 * 5) + "</li>"
        if c.c_10:payment_string += "<li>C " + str(c.c_10) + " * 10 = " + str(c.c_10 * 10) + "</li>"
        if c.n_10:payment_string += "<li>" + str(c.n_10) + " * 10 = " + str(c.n_10 * 10) + "</li>"
        if c.n_20:payment_string += "<li>" + str(c.n_20) + " * 20 = " + str(c.n_20 * 20) + "</li>"
        if c.n_50:payment_string += "<li>" + str(c.n_50) + " * 50 = " + str(c.n_50 * 50) + "</li>"
        if c.n_100:payment_string += "<li>" + str(c.n_100) + " * 100 = " + str(c.n_100 * 100) + "</li>"
        if c.n_200:payment_string += "<li>" + str(c.n_200) + " * 200 = " + str(c.n_200 * 200) + "</li>"
        if c.n_500:payment_string += "<li>" + str(c.n_500) + " * 500 = " + str(c.n_500 * 500) + "</li>"
        if c.n_2000:payment_string += "<li>" + str(c.n_2000) + " * 2000 = " + str(c.n_2000 * 2000) + "</li>"
        payment_string = "<ul>" + payment_string + "</ul>"
        rows.append((c.date, "SELF", c.total_society_deposit, c.total_loan_deposit, c.tot_reciept, c.total_loan_deposit + c.total_society_deposit,"",payment_string))
    context = {'headers':("Date","Employee" , "Society Total" , 'Loan Total' , "Reciepts", "Total", "Payment Details", "Currency Details")}
    context['rows'] = rows
    rendered_report =  render(request,"employee/table.html",context)
    context['table'] = rendered_report.content.decode('utf-8')
    context['heading'] = 'My cash submit report'
    return context
# @login_required
def report(request,report_type):
    context = {}
    
    if("maturity"==report_type):
        form_ = MajorReport
    elif("loans"==report_type):
        form_ = MajorReport
    elif("withdrawls"==report_type):
        form_ = MajorReport
    elif("emi_due"==report_type):
        form_ = MajorReport
    elif("daily_report_dp" == report_type):
        form_ = MajorReport

    elif("daily_report_fc" == report_type):
        form_ = MajorReport

    elif("document_dispatch"==report_type):
        form_ = MajorReport

    elif("ClientCollection" in report_type):
        form_ = ClientCollectionReport
        report_type , request.tp_ = report_type.split("_")    

    elif("AgentCollection" in report_type):
        form_ = AgentCollectionReport
        report_type , request.tp_ = report_type.split("_")

    elif("ledger"==report_type):
        form_ = Ledger
    elif("cashbook"==report_type):
        form_ = CashBook
    elif("cash_report"==report_type):
        form_ = CashBook
    elif("bankTransactions"==report_type):
        form_ = CashBook

    elif("emp_report"==report_type):
        form_ = EmpReport
    
    elif("daily_cash"==report_type):
        form_ = DailyCash
    
    elif("upcoming_maturity"==report_type):
        form_ = UpcomingMaturity
    
    elif("account_status"==report_type):
        form_ = AccountStatus
    
    elif("mycashreport"==report_type):
        form_ = CashBook

    elif("dividendreport"==report_type):
        form_ = DividendReport

    if request.method == 'POST':
        form = form_(request.POST)
        if form.is_valid():
            context  = eval(f"{report_type}")(request)
    else:
        form = form_()

    context['heading'] = report_type
    context['form'] = form   

    return render(request, 'employee/report.html', context=context)





def client_report(request):
    context = {}
    if request.method == 'POST':
        form = ClientReport(request.POST)
        if form.is_valid():
 
            acc_num = request.POST.get("acc_num")
            key = request.POST.get("secure_key")
            
            if("26" == acc_num[:2]):
                acc = approved_finance_table.objects.get(finance__loan_account_number = acc_num)  

                secured = acc.secure_key == key

                display_fields = ('bill_no','loan_emi_received_date','loan_emi_received','penalty')       
                values = eval( f'acc.collection_finance_set.values_list{display_fields}')

                head_fields = ('person__nomination_number','person__first_name','person__last_name','person__area','person__mobile_number_1','loan_start_date','loan_end_date')
                head = eval( f'approved_finance_table.objects.filter(finance__loan_account_number = acc_num).values_list{head_fields}')
                
                print(head)
                meta_title = '<br>'.join([f'{el.replace("person__","").replace("_"," ")} : {head[0][i]}'  for i , el in enumerate(head_fields)])

            else:
                acc = deposits_table.objects.get(society_account_number = acc_num)
                
                secured = acc.secure_key == key

                display_fields = ('bill_no','payment_received_date','payment_received')
                values = eval( f'acc.collection_deposit_set.values_list{display_fields}')

                head_fields = ('person__nomination_number','person__first_name','person__last_name','person__area','person__mobile_number_1','account_opening_date','category__name')
                head = eval( f'deposits_table.objects.filter(society_account_number = acc_num).values_list{head_fields}')
                
                print(head)
                meta_title = '<br>'.join([f'{el.replace("person__","").replace("_"," ")} : {head[0][i]}'  for i , el in enumerate(head_fields)])

            if(secured):
                context = {'headers':display_fields}
                context['records'] = values
                context['p_img'] = acc.person.photograph.url
                context["off_explore"] = 1
                
                context['title'] = f''' 
                <p style="text-transform: none;">
                {meta_title} </p>
                '''
                
                #get the table html
                rendered_report = render(request,"employee/table.html",context)
                context['table'] = rendered_report.content.decode('utf-8')
            else:
                context['table'] = '<div style="color:red;"> Credentials Are wrong </div>'
   
    else:
        form = ClientReport()

    context['heading'] = 'Client Report'
    context['form'] = form   

    return render(request, 'employee/report.html', context=context)

def get_data_point(header, amount):
    data = {'header': header, 'amount': amount}
    return data


def profitloss_report(request):
    context={}
    if request.method == "POST":
        from_date = request.POST.get("from")
        to_date = request.POST.get("to")

        deposits = deposits_table.objects.filter(account_opening_date__range=[from_date ,to_date])
        print(deposits)

        print(from_date, to_date)
    return render(request, 'employee/plreport.html', context)

def balance_sheet(request):
    context={}
    if request.method == "POST":
        from_date = request.POST.get("from")
        to_date = request.POST.get("to")

        deposits = deposits_table.objects.filter(account_opening_date__range=[from_date ,to_date])
        print(deposits)

        print(from_date, to_date)
    return render(request, 'employee/balancesheet.html', context)



def expenditure(request):
    context={}
    if request.method == "POST":
        from_date = request.POST.get("from")
        to_date = request.POST.get("to")
        clients = client.objects.filter(entry_date__range=[from_date ,to_date])
        fcs = collection_finance.objects.filter(loan_emi_received_date__range=[from_date ,to_date])
        dcs = collection_deposit.objects.filter(payment_received_date__range=[from_date ,to_date])
        deposits = deposits_table.objects.filter(status="ACTIVE")
        data_left = []
        data_right = []
        daily_fcs = fcs.filter(finance__emi_type="Daily")
        month_fcs = fcs.filter(finance__emi_type="Monthly")
        qtr_fcs = fcs.filter(finance__emi_type="Quaterly")
        ot_fcs = fcs.filter(finance__emi_type="OneTime")
        dds_dcs = dcs.filter(deposit__category__name="DD")
        fd_dcs = dcs.filter(deposit__category__name="FD")
        ca_dp = deposits.filter(category__name="CA")
        sharing = get_data_point('Sharing Amount', sum([ c.sharing_amount for c in clients ]))
        daily_fc_total = get_data_point('Daily Finance Collection', sum([ fc.loan_emi_received for fc in daily_fcs ]))
        month_fc_total = get_data_point('Monthly Finance Collection', sum([ fc.loan_emi_received for fc in month_fcs ]))
        qtr_fc_total = get_data_point('Quaterly Finance Collection', sum([ fc.loan_emi_received for fc in qtr_fcs ]))
        ot_fc_total = get_data_point('OneTime Finance Collection', sum([ fc.loan_emi_received for fc in ot_fcs ]))
        dds_dc_total = get_data_point('DDS Collection', sum([ dc.payment_received for dc in dds_dcs ]))
        fd_dc_total = get_data_point('FD Collection', sum([dc.payment_received for dc in fd_dcs]))
        ca_balance_total = get_data_point('Current Account Balance', sum([dp.balance for dp in ca_dp]))
        data_left.append(sharing)
        data_left.append(daily_fc_total)
        data_left.append(month_fc_total)
        data_left.append(qtr_fc_total)
        data_left.append(ot_fc_total)
        data_left.append(dds_dc_total)
        data_left.append(fd_dc_total)
        data_left.append(ca_balance_total)

        ######Data right

        loans = approved_finance_table.objects.filter(loan_start_date__range=[from_date ,to_date])
        dd_loans = loans.filter(emi_type="Daily")
        mn_loans = loans.filter(emi_type="Monthly")

        context = {'income': data_left, 'expense': data_right, 'from_date': from_date, 'to_date': to_date}
        print(from_date, to_date)
    return render(request, 'employee/expenditure.html', context)