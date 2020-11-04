from django.shortcuts import render
from employee.models import *
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime as dt
from dateutil import parser
from django.contrib import admin
from django.contrib.auth.models import User
# from employee.models import DocumentPrintCounter, CounterAndTime
import json
# ___________________________________________________
# Components
# ___________________________________________________



@login_required
def tansition(request , tp ,nom_num):
	if(tp=='fc'):
		url = f'/bank/fc_pdf/{nom_num}'

	elif(tp=='client'):
		url = f'/bank/client_pdf/{nom_num}'

	elif(tp=='id_card'):
		url = f'/bank/id_card/{nom_num}'

	elif(tp=='noc'):
		url = f'/bank/noc_pdf/{nom_num}'

	elif(tp=='cash_col'):
		url = f'/bank/cash_reciept/{nom_num}'

	elif(tp=='withdrawl'):
		url = f'/bank/withdrawl/{nom_num}'
	
	elif(tp == 'document'):
		url = f'/bank/document/{nom_num}'

	elif(tp == 'financecollection'):
		url = f'/bank/financecollection/{nom_num}'

	elif('dp' in tp):
		if("FD" in tp):
			url = f'/bank/fd_pdf/{nom_num}'	
		else:
			url = f'/bank/deposit_pdf/{nom_num}'
           
	else:
		print(tp ,' ---- none')
		url = '/bank/'

	html = f'''<h1>Redirecting...</h1>
				<br><br>
				<h2>Welcome {str(request.user)}</h2>
				<button onclick="location.href = '{url}';" >Print PDF</button>
				<br><br>
				<button onclick="location.href = '/bank';">GO to Home</button>
				'''
	return HttpResponse(html)
	# #Document print counter
	# if (tp):
	# 	user = request.user.id
	# 	document = tp
	# 	exists = DocumentPrintCounter.objects.filter(document_name=document, user=user).exists()
	# 	if not("EMP" in str(request.user)):
	# 		if not exists:
	# 			print("Ye hai hi nahi, banana hai, pun intended")
	# 			user_instance = User.objects.get(id=user)
	# 			createdoc = DocumentPrintCounter(
	# 				document_name = document,
	# 				user = user_instance,
	# 			)
	# 			createdoc.save()
	# 			counterfordoc = CounterAndTime(
	# 				total_prints = 1,
	# 				documentprintcounter = createdoc
	# 			)
	# 			counterfordoc.save()
	# 			print("Counter for PDF " + document + " and user: " + str(request.user) + " created!")

	# 			return HttpResponse(html)
	# 		else:
	# 			print("COUNTER ALREADY EXISTS, INCREMENT COUNTER")
	# 			doccounter = DocumentPrintCounter.objects.get(document_name=document, user=user)
	# 			all_counts = CounterAndTime.objects.filter(documentprintcounter=doccounter)
	# 			latest_counter = all_counts.last()
	# 			new_count = latest_counter.total_prints + 1
	# 			new_count_instance = CounterAndTime(
	# 				total_prints=new_count,
	# 				documentprintcounter=doccounter
	# 			)
	# 			new_count_instance.save()

	# 			print("NEW INSTANCE SAVED SUCCESSFULLY ==>>" + "COUNT NUMBER: " + str(new_count_instance.total_prints))
	# 			print(doccounter)
	# 			context = {
	# 				"counterobjects": all_counts,
	# 				"document": doccounter,
	# 				"url": url
	# 			}
	# 			return render(request, 'employee/doc_table.html', context)
	# 	else:
	# 		if exists:
	# 			#CREATE FUNCTION TO REDIRECT TO BANK/
	# 			print("THIS IS EMPLOYEE BITCH!")
	# 			return redirect('/bank/')
				
	# return html




def wd_componets(request , acc_num):
	dp =  deposits_table.objects.get(id = acc_num)
	holder_name = f'{dp.person.first_name} {dp.person.last_name}' 
	available_amount = dp.balance 
	intrest_amount = dp.interest_collected
	photo = dp.person.photograph.name.split("/")[-1]  
	sign =  dp.person.signature.name.split("/")[-1] 

	return HttpResponse(f"{holder_name},{available_amount},{intrest_amount},{photo},{sign}")


@login_required
def render_table(request, tp):

	e = employee_interview.objects.get(nomination_number= request.user.username)
	deposit_collections = [ [dp.bill_no , round(dp.payment_received , 1), dp.payment_received_date ,'Deposit'] for dp in e.employee_interview.collection_deposit_set.filter(payment_received_date=timezone.now())]

	finance_collections = [ [fc.bill_no , round(fc.loan_emi_received ,1) , fc.loan_emi_received_date , 'Finance'] for fc in e.employee_interview.collection_finance_set.filter(loan_emi_received_date=timezone.now())]
	
	tables = ""

	if(deposit_collections):
		context = {'headers':['bill no','Payment', 'Date' , 'Type']}
		context['rows'] = deposit_collections 
		context['title'] = 'Deposit Collections'
		dp_table =  render(request,"employee/table.html",context)
		tables += dp_table.content.decode()
	
	if(finance_collections):
		context = {'headers':['bill no','Payment', 'Date' , 'Type']}
		context['rows'] = finance_collections 
		context['title'] = 'Finance Collections'
		fc_table =  render(request,"employee/table.html",context)
		tables += fc_table.content.decode()

	if(not tables):
		tables = """<div class="card" style="border-radius: 20px;margin: 30px;margin-top: -10px;"> No Collections Yet <div>"""
	
	return HttpResponse(tables)


@login_required
def collection_data(request,num):
	dt_ = dt.today().strftime("%B %d, %Y")
	dt_ = parser.parse(dt_).date()
	
	data = deposits_table.objects.get(society_account_number = num)
	tot_interest = data.interest_collected

	print(data.balance , ' < --- ')
	balance = data.balance if(data.balance>0) else data.account_opening_amount
	
	latest_col = data.collection_deposit_set.all().order_by('-id')
	
	##currently this is dummy
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

	print(days, data.scheme.per_day_roi)
	days = 1 if (days==0) else days
	#calculate interest till date from last collection
	interest_delta = (balance * data.scheme.per_day_roi) * days
	#add with last interest 
	tot_interest +=  interest_delta
	tot_interest = int(tot_interest)
	print(balance  ,interest_delta , tot_interest)
	
	s = '{},{},{} {},{},{}'.format(data.id ,balance, data.person.first_name, data.person.last_name , tot_interest, data.status)
	return HttpResponse(s)


@login_required
def collection_fc(request,num):
	data = finance_table.objects.get(loan_account_number=num).approved_finance_table_set.all()[0] 

	emi_amount = data.emi_amount
	
	remaining = data.total - data.recieved
	
	#Appfinance ID , emi amt , recieved till date , remaining total to pay
	s = '{},{},{},{},{}'.format(data.id ,emi_amount, data.recieved, remaining , data.finance.person.first_name+ ' ' + data.finance.person.last_name )

	return HttpResponse(s)


@login_required
def tot_coll(request):
	dp_colls = collection_deposit.objects.filter(payment_received_date=timezone.now()).values_list('payment_recieved')
	fc_colls = collection_finance.objects.filter(payment_received_date=timezone.now()).values_list('loan_emi_received')

	return HttpResponse( f"{sum(dp_colls)} , {sum(fc_colls)}")

@login_required
def get_data_by_document(request, doc_type):
	tp = doc_type
	if(tp=='fc') or (tp=='noc'):
		data = approved_finance_table.objects.all()
		dlist_1 = []
		dlist_2 = []
		dlist_3 = []
		for x in data:
			dlist_1.append(x.finance.loan_account_number)
			dlist_2.append(x.finance.person.nomination_number)
			dlist_3.append(x.finance.person.first_name + " " + x.finance.person.last_name)
		data_object = {
			'dlist_1': dlist_1,
			'dlist_2': dlist_2,
			'dlist_3': dlist_3
		}
		url = f'/bank/fc_pdf/'
	
	elif(tp=='all_loans'):
		data = finance_table.objects.all()
		dlist_1 = []
		dlist_2 = []
		dlist_3 = []
		for x in data:
			dlist_1.append(x.loan_account_number)
			dlist_2.append(x.person.nomination_number)
			dlist_3.append(x.person.first_name + " " + x.person.last_name)
		data_object = {
			'dlist_1': dlist_1,
			'dlist_2': dlist_2,
			'dlist_3': dlist_3
		}
		url = f'/bank/fc_pdf/'

	elif(tp=='client'):
		data = client.objects.all()
		dlist_1 = []
		dlist_2 = []
		dlist_3 = []
		for x in data:
			dlist_1.append(x.nomination_number)
			dlist_2.append(x.mobile_number_1)
			dlist_3.append(x.first_name + " " + x.last_name)
		data_object = {
			'dlist_1': dlist_1,
			'dlist_2': dlist_2,
			'dlist_3': dlist_3
		}
		url = f'/bank/client_pdf/'

	elif(tp=='id_card'):
		data = employee_joining.objects.all()
		dlist_1 = []
		dlist_2 = []
		dlist_3 = []
		for x in data:
			dlist_1.append(x.employee.nomination_number)
			dlist_2.append(x.employee.mobile_number_1)
			dlist_3.append(x.employee.first_name + " " + x.employee.last_name)
		data_object = {
			'dlist_1': dlist_1,
			'dlist_2': dlist_2,
			'dlist_3': dlist_3
		}
		url = f'/bank/id_card/'

	elif(tp=='cash_col'):
		data = cash_collection.objects.all()
		dlist_1 = []
		dlist_2 = []
		dlist_3 = []
		for x in data:
			dlist_1.append(x.bill_number)
			dlist_2.append(x.employee.mobile_number_1)
			dlist_3.append(x.employee.first_name + " " + x.employee.last_name)
		data_object = {
			'dlist_1': dlist_1,
			'dlist_2': dlist_2,
			'dlist_3': dlist_3
		}
		url = f'/bank/cash_reciept/'

	elif(tp=='withdrawl'):
		data = withdrawl_entry.objects.all()
		dlist_1 = []
		dlist_2 = []
		dlist_3 = []
		for x in data:
			dlist_1.append(x.bill_no)
			dlist_2.append(x.society_account.person.mobile_number_1)
			dlist_3.append(x.society_account.person.first_name + " " + x.society_account.person.last_name)
		data_object = {
			'dlist_1': dlist_1,
			'dlist_2': dlist_2,
			'dlist_3': dlist_3
		}
		url = f'/bank/withdrawl/'
	
	elif(tp == 'document'):
		data = Documents.objects.all()
		dlist_1 = []
		dlist_2 = []
		dlist_3 = []
		for x in data:
			dlist_1.append(x.id)
			dlist_2.append(x.name)
			dlist_3.append(str(x.Submit_date))
		data_object = {
			'dlist_1': dlist_1,
			'dlist_2': dlist_2,
			'dlist_3': dlist_3
		}
		url = f'/bank/document/'

	elif(tp == 'financecollection'):
		data = collection_finance.objects.all()
		dlist_1 = []
		dlist_2 = []
		dlist_3 = []
		for x in data:
			dlist_1.append(x.id)
			dlist_2.append(x.finance.finance.person.first_name + " " + x.finance.finance.person.last_name)
			dlist_3.append(x.bill_no)
		data_object = {
			'dlist_1': dlist_1,
			'dlist_2': dlist_2,
			'dlist_3': dlist_3
		}
		url = f'/bank/financecollection/'

	elif('dp' in tp):
		if("FD" in tp):
			data = deposits_table.objects.all()
			dlist_1 = []
			dlist_2 = []
			dlist_3 = []
			for x in data:
				dlist_1.append(x.society_account_number)
				dlist_2.append(x.person.first_name + " " + x.person.last_name)
				dlist_3.append(x.person.mobile_number_1)
			data_object = {
				'dlist_1': dlist_1,
				'dlist_2': dlist_2,
				'dlist_3': dlist_3
			}
			url = f'/bank/fd_pdf/'	
		else:
			data = deposits_table.objects.all()
			dlist_1 = []
			dlist_2 = []
			dlist_3 = []
			for x in data:
				dlist_1.append(x.society_account_number)
				dlist_2.append(x.person.first_name + " " + x.person.last_name)
				dlist_3.append(x.person.mobile_number_1)
			data_object = {
				'dlist_1': dlist_1,
				'dlist_2': dlist_2,
				'dlist_3': dlist_3
			}
			url = f'/bank/deposit_pdf/'
           
	else:
		print(tp ,' ---- none')
		url = '/bank/'
	

	x = {'tp': tp, 'url': url, 'data': data_object}
	dataset = json.dumps(x)
	return HttpResponse(dataset, status=203)