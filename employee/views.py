from django.shortcuts import render
from .models import *
import random
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from dateutil import parser
from dateutil.relativedelta import relativedelta
#import custom views
from employee.emp_views.view_comp import *
from employee.emp_views.view_reports import *
from employee.emp_views.view_reciepts import *
import json
from datetime import date, timedelta
from datetime import datetime as dtime
import base64
from django.contrib import messages
from employee.forms import *
from django.db.models import F
import calendar

# ___________________________________________________
# Main Views
# ___________________________________________________

# ######### FOR CRON JOB #############
# from datetime import date
# from employee.models import *

# def deposit_status_check():
# 	accounts = deposits_table.objects.all()
# 	for account in accounts:
# 		deposits = collection_deposit.objects.filter(deposit=account).order_by('created_time')
# 		latest_deposit = deposits[len(deposits)-1]
# 		last_day_difference = (latest_deposit.payment_received_date - date.today()).days
# 		#if the last deposit was made more than ten days ago
# 		if last_day_difference >= 10:
# 			account.status = "HOLD"
# 			account.save()
# 			print("THE ACCOUNT IS NOW PUT ON HOLD!")
# 		else:
# 			if account.status != "ACTIVE":
# 				account.status == "ACTIVE"
# 				account.save()
# 				print("THE ACCOUNT IS NOW ACTIVE!")
# #####################################
# deposit_status_check()

@login_required()
def index(request): 
	context={}
	
	date_ = parser.parse("2015-04-01") 

	if ("admin" in request.user.username or "cashier" in request.user.username) :
		#fetching details of clients console who had applied for loan and deposits 
		# try:
		loan_data = finance_table.objects.filter(approved=False).values_list('loan_account_number','person__first_name','person__last_name','person__area','expected_date','expected_amount','person__mobile_number_1','applied_date', 'id')
		context_loan_data = []
		for x in loan_data:
			if x[4] <= date.today():
				# print(x)
				message = "id_finance=" + str(x[8])
				message_bytes = message.encode('ascii')
				base64_bytes = base64.b64encode(message_bytes)
				base64_message = base64_bytes.decode('ascii')
				d = list(x)
				d.append(base64_message)
				# d = tuple(list(x).append(base64_message))
				context_loan_data.append(d)
		# loan_data = finance_table.objects.all().order_by('-id')[:4].values_list('loan_account_number','person__first_name','person__last_name','expected_date','expected_amount','person__mobile_number_1','applied_date')

		context['loan_data']= context_loan_data
		# context['loan_data'] = tuple(list(context['loan_data'][]))
		dp_data = deposits_table.objects.filter(maturity_date = timezone.now() , status="ACTIVE").values_list('society_account_number','person__first_name','person__last_name','person__area','person__mobile_number_1','account_opening_date','category__name','maturity_interest','maturity_amount','id','person__photograph','person__signature')
		# print(dp_data)
		context['dp_data']= dp_data
		
		col_data = cash_collection.objects.filter(date=timezone.now()).values_list('employee__first_name','employee__last_name','total_society_deposit','total_loan_deposit','id','approved')
		context['col_data']= col_data
		print(col_data , dp_data)
		# except Exception as exp:
		# 	print('---------------------- ',exp)
		# 	pass
		


		#Balance
		balance = Balance.objects.all()[0]
		context['balance'] = balance
		context['cash'] = round(balance.cash ,2)
		context['bank'] =  round(balance.bank , 2)

		# For admin Console
		if("admin" in request.user.username):

			#admin has extar elements
			dp_insights = {i.name : round(i.amount,2) for i in DepositChoice.objects.all()}
			fc_insights = {i.name : round(i.amount ,2) for i in FinanceChoice.objects.all()}

			print(dp_insights)
			context['dp_amounts'] = dp_insights
			context['fc_amounts'] = fc_insights

			# for getting info of all loggedin users 
			active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
			user_id_list = []
			for session in active_sessions:
				data = session.get_decoded()
				user_id_list.append(data.get('_auth_user_id', None))

			loggedin_users = User.objects.filter(id__in=user_id_list).values_list('username','last_login','first_name','last_name')

			print(loggedin_users)
			context['loggedin'] = loggedin_users
			return render(request,'employee/admin_console.html',context)
		
		# For Cashier Console
		else:
			return render(request,"employee/cashier_console.html",context)
	

	##### Employee Console
	else:
		# print(request.user.username)
		# print(request.user.groups.name)
		x = request.user.username
		e = employee_interview.objects.get(nomination_number = x)

		context['emp_data'] = e

		##remove all deposits with status = 0
		# e.deposits_table_set.filter(status=0).delete()

		return render(request,"employee/employee_dashboard.html",context)



def finance(request,fc_num):
	data = finance_table.objects.get(id=fc_num)

	x = {'nom_num': data.person.nomination_number,
	 'name':data.person.first_name+ ' ' + data.person.last_name ,
	 'amount': data.expected_amount,
	 'date': str(data.expected_date),
	 'loan_duration': data.loan_duration,
	 'duration_type': data.duration_type,
	 'emi_type': data.emi_type}
	dataset = json.dumps(x)
	return HttpResponse(dataset, status=200)



def db_select(request):
	
	if request.method == 'GET':
		context = {"backups" : os.listdir(os.getcwd())}

		return render(request,"employee/db_select.html",context=context)
	else:
		response = index(request)
		response.set_cookie(key='db', value=request.POST['db_type'])

		print(request.POST)
		return response


def handler404(request, exception):
    return HttpResponse(f"<h1> Error </h1> <h3>{exception}</h3>" )

def deposit_check(request):
	if request.user.is_authenticated:
		if ("admin" in request.user.username):
			x = {'admin': True}
		else:
			x = {'admin': False}
		data = json.dumps(x)
		# print(type(data))
		return HttpResponse(data, status=200)
	return HttpResponse("Not authenticated", status=403)

def doc_check(request, lan):
	if request.user.is_authenticated:
		try:
			ft = approved_finance_table.objects.get(finance__loan_account_number=lan)
		except:
			return HttpResponse("Not found1", status=404)
		if ft :
			print(ft.recieved, ft.total)
			if (ft.recieved > ft.total) and ('admin' or 'cashier' in request.user):
				x = {'change': True}
			else:
				x = {'change': False}
			data = json.dumps(x)
			return HttpResponse(data, status=200)
		else:
			return HttpResponse("Not found", status=404)

	return HttpResponse("Not authenticated", status=403)	

def deposit_collection(request, dt):

	if request.user.is_authenticated:
		data = deposits_table.objects.get(id=dt)
		dt_ = dtime.today().strftime("%B %d, %Y")
		dt_ = parser.parse(dt_).date()
		tot_interest = data.interest_collected
		balance = data.balance if(data.balance>0) else data.account_opening_amount
		latest_col = data.collection_deposit_set.all().order_by('-id')
		if(latest_col):
			create = str(latest_col[0].created_time)
			create = parser.parse(create).date()
			days = abs((dt_ - create).days)
			# days = abs((dt.now().date() - latest_col[0].payment_received_date).days)
		else:
			create = str(data.created_time)
			create = parser.parse(create).date()
			days = abs((dt_ - create).days)
			# days = abs((dt.now().date() - data.account_opening_date).days)
		days = 1 if (days==0) else days
		#calculate interest till date from last collection
		interest_delta = (balance * data.scheme.per_day_roi) * days
		#add with last interest 
		tot_interest +=  interest_delta
		tot_interest = int(tot_interest)
		x = {'balance': balance, 'interest': tot_interest, 'status': data.status}
		data = json.dumps(x)
		return HttpResponse(data, status=200)

	return HttpResponse("Not authenticated", status=403)

def finance_collection(request, ft):
	if request.user.is_authenticated:
		finance = approved_finance_table.objects.get(id=ft)
		x = {'emi': finance.emi_amount, 'status': finance.status}
		data = json.dumps(x)
		return HttpResponse(data, status=200)

	return HttpResponse("Not authenticated", status=403)

def check_collection(request):
	if request.user.is_authenticated:
		user = request.user
		print(user)
		emp = employee_interview.objects.filter(nomination_number=user)
		today = date.today()
		check = cash_collection.objects.filter(employee=emp[0], date__year=today.year, date__month=today.month, date__day=today.day).exists()
		x = {'collection': check}
		data = json.dumps(x)
		return HttpResponse(data, status=200)

def print_documents(request):
	doc_list = [
		'Loan QR Code',
		'Society QR Code',
		'Nomination Reciept',
		'EMP_ID_Card',
		'Loan NOC',
		'EMP Daily Cash',
		'Maturity Slip',
		'Upload Documents',
		'Monthly/OT Reciept',
		'FD Bond',
	]
	context={'docs': doc_list}

	return render(request, 'employee/printdocs.html', context)

def print_data(request,doc, pk):
	data = DocumentPrint.objects.filter(doc_name=doc, doc_for=pk)
	datas = []
	for i in range(len(data)):
		obj = {
			'index': i+1,
			'user': str(data[i].printed_by),
			'timestamp': str(data[i].timestamp),
		}
		datas.append(obj)

	data = json.dumps(datas)
	return HttpResponse(data, status=200)

def get_employees(request):
	employees = employee_joining.objects.all()
	dlist_1 = []
	dlist_2 = []
	dlist_3 = []
	for x in employees:
		dlist_1.append(x.employee.nomination_number)
		dlist_2.append(x.employee.mobile_number_1)
		dlist_3.append(x.employee.first_name + " " + x.employee.last_name)
	data_object = {
		'dlist_1': dlist_1,
		'dlist_2': dlist_2,
		'dlist_3': dlist_3
		}
	x = {'data': data_object}
	dataset = json.dumps(x)
	return HttpResponse(dataset, status=200)

def past_collection(request, date):
	e = employee_interview.objects.filter(nomination_number=request.user.username)
	if(e):
		emp = e.first()
		d_ = emp.collection_deposit_set.filter(payment_received_date=date).values_list('payment_received')
		f_ = emp.collection_finance_set.filter(loan_emi_received_date=date).values_list('loan_emi_received')
		total_f = sum([i[0] for i in f_])
		total_d = sum([i[0] for i in d_])
		x = {'f': total_f, 'd': total_d}
		dataset = json.dumps(x)
		return HttpResponse(dataset, status=200)
	else:
		return HttpResponse(status=403)



def approveloandata(request, num):
	loan = finance_table.objects.get(loan_account_number=num)
	x = {
		'amount': loan.expected_amount,
		'duration': loan.loan_duration,
		'duration_type': loan.duration_type,
		'emi_type': loan.emi_type,
	}
	dataset = json.dumps(x)
	return HttpResponse(dataset, status=200)

def accountstatus(request):
	context = {}
	if request.method == "POST":
		status = request.POST.get('status').upper()
		actype = request.POST.get('account_type')
		if actype=="d":
			accounts = deposits_table.objects.filter(status=status)
			context = {"type": "d", "accounts": accounts}
		if actype=="f":
			accounts = approved_finance_table.objects.filter(status=status)
			context = {"type": "f", "accounts": accounts}
		else:
			deps = deposits_table.objects.filter(status=status)
			loans = approved_finance_table.objects.filter(status=status)
			accounts = list(chain(deps, loans))
			return render(request, 'employee/accountstatus.html', context)
	return render(request, 'employee/accountstatus.html', context)

def changeaccountstatus(request):
	if request.method=="POST":
		actype = request.POST.get('type')
		if actype == "d":
			ac_id = request.POST.get('account_id')
			acc = deposits_table.objects.get(id=ac_id)
			new_status = request.POST.get('status').upper()
			if new_status == acc.status:
				messages.info(request, 'Status change cannot be same')
				return redirect('accountstatus')
			else:
				old = acc.status
				acc.status = new_status
				acc.save()
				messages.success(request, f'{acc.society_account_number} status changed from {old} to {new_status}')
				return redirect('accountstatus')
		if actype == "f":
			ac_id = request.POST.get('account_id')
			acc = approved_finance_table.objects.get(id=ac_id)
			new_status = request.POST.get('status').upper()
			if new_status == acc.status:
				messages.info(request, 'Status change cannot be same')
				return redirect('accountstatus')
			else:
				old = acc.status
				acc.status = new_status
				acc.save()
				messages.success(request, f'{acc.society_account_number} status changed from {old} to {new_status}')
				return redirect('accountstatus')
	return HttpResponse(status=200)

def docdispatch_tool(request):
	context = {'present': False}
	if request.method == "POST":
		search = request.POST.get('searchfc')
		if search == "Search by account":
			lan = request.POST.get('fc')
			data = approved_finance_table.objects.filter(finance__loan_account_number=lan)
			for x in data:
				if x.recieved >= x.total:
					docs = x.finance.documents_set.all()
					dispatched = False
					for d in docs:
						if d.status == "Dispatched":
							dispatched = True
					x.dispatched = dispatched
					x.completed = True
				else:
					x.complete = False
			context = {'data': data, 'present': True}
		else:
			data = approved_finance_table.objects.filter(recieved__gte=F('total'))
			for x in data:
				if x.recieved >= x.total:
					docs = x.finance.documents_set.all()
					dispatched = False
					for d in docs:
						if d.status == "Dispatched":
							dispatched = True
					x.dispatched = dispatched
					x.completed = True
				else:
					x.completed = False
			context = {'data': data, 'present': True}
	
	return render(request, 'employee/docdispatch.html', context)

def dispatchdocapi(request, lan):
	if 'admin' in str(request.user.username):
		try:
			docs = Documents.objects.filter(cli__loan_account_number=lan)
			for doc in docs:
				doc.status = 'Dispatched'
				doc.save()
			# messages.success(request, f'Documents dispatched for account number: {lan}')
			response = {'url':f'/bank/document/{docs[0].id}'}
			dataset = json.dumps(response)
			return HttpResponse(dataset, status=200)
		except:
			messages.warning(request, f'Unable to dispatch documents for account number: {lan}')
			return redirect('docdispatch')
	else:
		return HttpResponse(status=403)

def get_dates_list_from_string(weekstring):
    dates = []
    week = weekstring.replace("-", "").split('.')
    week_start, week_end = week
    week_start = dtime.strptime(week_start, "%Y%m%d").date()
    week_end = dtime.strptime(week_end, "%Y%m%d").date()
    delta = week_end - week_start
    dates = []
    for i in range(delta.days + 1):
        fay = week_start + timedelta(days=i)
        weekday = calendar.day_name[fay.weekday()] 
        day = fay.strftime('%d/%m/%Y')
        day2 = fay.strftime('%Y-%m-%d')
        x = [day, day2]
        dates.append(x)
    return dates

def uploadedDocs(request):
	context = {}
	if request.method == "POST":
		from_date = request.POST.get("from")
		to_date = request.POST.get("to")
		doc_list = ['Nomination Certificate', 'Loan NOC', 'Maturity', 'FD Bond', 'Loan Diary', 'Society Diary', 'Loan Monthly / Onetime Reciept', 'Other']
		reqtype = request.POST.get('type')
		if reqtype == 'account':
			actype = request.POST.get('actype')
			if actype == 'loan':
				if request.POST.get('extra') == 'all':
					fcs = finance_table.objects.filter(applied_date__range=[from_date, to_date])
				else:
					a = request.POST.get('acc')
					fcs = finance_table.objects.filter(person__nomination_number=a)
				docs = []
				for fc in fcs:
					fdocs = UploadDocs.objects.filter(id_num=fc.loan_account_number)
					data = {
						'fc': fc,
						'docs': fdocs,
					}
					docs.append(data)
				messages.success(request, f'Fetched Document details for loan account')
			if actype == 'deposit':
				if request.POST.get('extra') == 'all':
					dcs = deposits_table.objects.filter(account_opening_date__range=[from_date, to_date])
				else:
					a = request.POST.get('acc')
					dcs = deposits_table.objects.filter(person__nomination_number=a)
				docs = []
				for fc in dcs:
					fdocs = UploadDocs.objects.filter(id_num=fc.society_account_number)
					data = {
						'fc': fc,
						'docs': fdocs,
					}
					docs.append(data)
				messages.success(request, f'Fetched Document details for deposit account')
			context['dlist'] = doc_list
			context['data'] = docs
		if reqtype=='employee':
			dates = get_dates_list_from_string(f"{from_date}.{to_date}")
			context['dates'] = dates
			if request.POST.get('extra') == 'all':
				docs = UploadDocs.objects.filter(date__range=[from_date, to_date], TYPE="Cash Collection")
				emps = employee_joining.objects.all()
				datalist = []
				for emp in emps:
					doc = docs.filter(id_num=emp.employee.nomination_number)
					obj = {'emp': emp}
					emp_doclist = []
					for date in dates:
						date_docs = doc.filter(date=date[1])
						doc_object = {'date': date[0], 'docs': date_docs}
						emp_doclist.append(doc_object)
					obj['docdata'] = emp_doclist
					datalist.append(obj)
				print(datalist)
				context['empdoc'] = datalist
			else:
				a = request.POST.get('acc')
				docs = UploadDocs.objects.filter(date__range=[from_date, to_date], TYPE="Cash Collection")
				emp = employee_joining.objects.get(employee__nomination_number=a)
				datalist = []
				doc = docs.filter(id_num=emp.employee.nomination_number)
				obj = {'emp': emp}
				emp_doclist = []
				for date in dates:
					date_docs = doc.filter(date=date[1])
					doc_object = {'date': date[0], 'docs': date_docs}
					emp_doclist.append(doc_object)
				obj['docdata'] = emp_doclist
				datalist.append(obj)
				print(datalist)
				context['empdoc'] = datalist
	return render(request, 'employee/uploadedDocs.html', context)