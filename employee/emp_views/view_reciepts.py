from django.shortcuts import render
from employee.models import *
from django.http import HttpResponse , HttpResponseRedirect
from dateutil import parser
import qrcode
import pdfkit
from django.contrib.auth.decorators import login_required
from employee.utils import render_to_pdf #created in step 4
import os , base64
from datetime import datetime as dt



def print_counter(user, doctype, model):
	docs = DocumentPrint.objects.filter(doc_name=doctype, printed_by=user, doc_for=str(model)).count()

	if docs > 0:
		if 'admin' in str(user):
			countplus = DocumentPrint(
				doc_name = doctype,
				doc_for = str(model),
				printed_by = user,
			)
			countplus.save()
			print(f"increment counter{docs}")
			return True
		else:
			return False
	else:
		init_count = DocumentPrint(
			doc_name = doctype,
			doc_for = str(model),
			printed_by = user,
		)
		init_count.save()
		print("successfully creted instance")
		return True

#dependency
def create_qr(nom_num):
	qr = qrcode.QRCode(
	version = 1,
	error_correction = qrcode.constants.ERROR_CORRECT_H,
	box_size = 10,
	border = 4,)

	qr.add_data(nom_num)
	qr.make(fit=True)
	img = qr.make_image()		
	img.save(f"media/users/qrcode/{nom_num}.jpg")




# ___________________________________________________
# PDF SECTION (VIEWS)
# ___________________________________________________

def test(request):
	dp_num = 1920062001
	data = deposits_table.objects.get(society_account_number = dp_num)

	# create and save qr code
	create_qr(dp_num)
	print('qr')


	print('hello')
	context = {}
	context['num_wrd'] = num2words(data.balance, lang='en_IN') + ' Only /-'

	img1 = open(data.person.photograph.url[1:],"rb").read()
	img2 = open(f'media/users/qrcode/{ dp_num }.jpg',"rb").read()
	encoded_string1 = base64.b64encode(img1).decode()
	encoded_string2 = base64.b64encode(img2).decode()

	context['qr_photo'] = encoded_string2
	context['photo'] =  encoded_string1
	context['name'] = data.person.first_name.upper() + ' ' + data.person.last_name.upper()
	context['fd'] = data

	page = render(request,'employee/reciepts/client_test.html',context)
	page = page.content.decode('utf-8')
	pdf = pdfkit.from_string(page, False , options={
	'orientation':'landscape',
	})
	# pdf = pdfkit.from_string(page, False ,options={'orientation':'portrait'})

	print(context['num_wrd'])	

	return HttpResponse(pdf, content_type='application/pdf')

@login_required
def client_pdf(request,nom_num):
	data = client.objects.get(nomination_number = nom_num)
	context = {}
	if not print_counter(request.user, "client", nom_num):
		return HttpResponse("Not Authorized", status=403)
	context['photo'] = os.getcwd() + data.photograph.url
	context['logo'] = os.getcwd() + '/media/users/logo.jpg'
	context['client'] = data

	page = render(request,'employee/reciepts/client_cert.html',context=context)
	page = page.content.decode('utf-8')

	print(page)
	pdf = pdfkit.from_string(page, False , options={
	'orientation':'portrait',
	'page-size': 'A4',
	'dpi': '300',
	})
	return HttpResponse(pdf, content_type='application/pdf')

@login_required
def document_pdf(request, nom_num):
	document = Documents.objects.get(id=nom_num)
	context = {'data': document, 'time': timezone.now()}
	if not print_counter(request.user, "document", nom_num):
		return HttpResponse("Not Authorized", status=403)
	page = render(request,"employee/reciepts/doc_dispatch.html",context=context)
	page = page.content.decode('utf-8')
	
	pdf = pdfkit.from_string(page, False , options={
	'orientation':'portrait',
	'page-size': 'A4',
	'dpi': '300',
	})
	return HttpResponse(pdf, content_type='application/pdf')

@login_required
def collectionFinance_reciept(request, nom_num):
	data = collection_finance.objects.get(id = nom_num)
	emi_count = collection_finance.objects.filter(finance=data.finance).count()
	print(emi_count)
	if not print_counter(request.user, "financecollection", nom_num):
		return HttpResponse("Not Authorized", status=403)
	context = {'data' : data, 'time': timezone.now(), 'emi_count': emi_count}
	page = render(request,"employee/reciepts/collection_finance.html",context=context)
	# return page
	page = page.content.decode('utf-8')
	pdf = pdfkit.from_string(page, False , options={
	'orientation':'portrait',
	'page-size': 'A4',
	'dpi': '300',
	})
	return HttpResponse(pdf, content_type='application/pdf')


@login_required
def FD_pdf(request,dp_num):
	
	data = deposits_table.objects.get(society_account_number = dp_num)

	# create and save qr code
	create_qr(dp_num)
	print('qr')
	if not print_counter(request.user, "FD_pdf", dp_num):
		return HttpResponse("Not Authorized", status=403)

	print('hello')
	context = {}
	context['num_wrd'] = num2words(data.balance, lang='en_IN') + ' Only /-'

	img1 = open(data.person.photograph.url[1:],"rb").read()
	img2 = open(f'media/users/qrcode/{ dp_num }.jpg',"rb").read()
	encoded_string1 = base64.b64encode(img1).decode()
	encoded_string2 = base64.b64encode(img2).decode()

	context['qr_photo'] = encoded_string2
	context['photo'] =  encoded_string1
	context['name'] = data.person.first_name.upper() + ' ' + data.person.last_name.upper()
	context['fd'] = data

	page = render(request,'employee/reciepts/fd.html',context)
	page = page.content.decode('utf-8')
	pdf = pdfkit.from_string(page, False , options={
	'orientation':'portrait',
	'page-size': 'A4',
	'dpi': '300',
	})
	# pdf = pdfkit.from_string(page, False ,options={'orientation':'portrait'})

	print(context['num_wrd'])	

	return HttpResponse(pdf, content_type='application/pdf')
	# return render(request,'employee/reciepts/fd.html',context)


# @login_required
def id_card(request,nom_num):
	e_= employee_joining.objects.get(employee__nomination_number=nom_num)
	e = e_.employee
	if not print_counter(request.user, "id_card", nom_num):
		return HttpResponse("Not Authorized", status=403)
	img1 = open(e.photograph.url[1:],"rb").read()
	img2 = open(e.signature.url[1:],"rb").read()
	img3 = open("media/docs/header.png","rb").read()

	encoded_string1 = base64.b64encode(img1).decode()
	encoded_string2 = base64.b64encode(img2).decode()
	encoded_string3 = base64.b64encode(img3).decode()

	context = {'e':e , 'photo_data':encoded_string1, 'sign_data': encoded_string2,'header_data': encoded_string3, 'joining_date':e_.joining_date}
	page = render(request,'employee/reciepts/id.html',context=context)
	page = page.content.decode('utf-8')

	
	pdf = pdfkit.from_string(page, False , options={'orientation':'landscape', 'page-height':'216', 'page-width':'324'})
	return HttpResponse(pdf, content_type='application/pdf')

	# return HttpResponse(page)

	
@login_required
def deposit_pdf(request,nom_num):

	#cretae qrcode with nom_num
	create_qr(nom_num)

	data = deposits_table.objects.get(society_account_number = nom_num)
	if not print_counter(request.user, "dp_pdf", nom_num):
		return HttpResponse("Not Authorized", status=403)
	context = {}
	# print(qr_data)
	primary_info = {
		'Nomination ID' : data.person.nomination_number,
		'Name': data.person.first_name + ' ' + data.person.last_name,
		'Area': data.person.area,
		'F Name': data.person.father_name,
		'Opening Date' : data.account_opening_date,
		'Secure Key' : data.secure_key,
	}
	extra_info = {
		'type': data.account_opening_amount, 
	}
	if(not data.scheme.duration):
		#current account
		context['id_tp'] = 'Current Account'
	else:
		primary_info['Duration']= f'{str(data.scheme.duration)} years, <strong>DP</strong>: {str(data.account_opening_amount)}'
	
	context['id_num_url'] = os.getcwd() + f'/media/users/qrcode/{ nom_num }.jpg'
	context['id_num'] = nom_num 
	context['photo'] = os.getcwd() + data.person.photograph.url
	context['type'] = data.category.name
	context['primary_info'] = primary_info
	context['extra_info'] = extra_info


	page = render(request,'employee/reciepts/temp.html',context)
	page = page.content.decode('utf-8')

	pdf = pdfkit.from_string(page, False )

	return HttpResponse(pdf, content_type='application/pdf')



@login_required
def fc_pdf(request,fc_num):
	data = approved_finance_table.objects.get(finance__loan_account_number =fc_num)
	nom_num = data.finance.loan_account_number
	#cretae qrcode with nom_num
	create_qr(nom_num)
	if not print_counter(request.user, "fc", fc_num):
		return HttpResponse("Not Authorized", status=403)
	context = {}
	# print(qr_data)
	primary_info = {
		'Nomination ID' : data.finance.person.nomination_number,
		'Name': data.finance.person.first_name + ' ' + data.finance.person.last_name,
		'Area': data.finance.person.area,
		'Fathers Name': data.finance.person.father_name,
		'Opening Date' : data.loan_start_date,
		'Duration' : f'{str(data.loan_duration)} {data.duration_type},<strong> EMI</strong>: {data.emi_amount}',
		'Secure Key' : data.secure_key,
	}

	context['id_tp'] = 'Finance'
	context['id_num_url'] = os.getcwd() + f'/media/users/qrcode/{ nom_num }.jpg'
	context['id_num'] = data.finance.loan_account_number
	context['photo'] = os.getcwd() + data.finance.person.photograph.url
	context['type'] = data.emi_type
	context['primary_info'] = primary_info
	page = render(request,'employee/reciepts/temp.html',context)
	page = page.content.decode('utf-8')

	pdf = pdfkit.from_string(page, False )
	return HttpResponse(pdf, content_type='application/pdf')






# testing ---------------->>>>>>>>>>>>>>>>>>
@login_required
def pdf(request,nom_num):

	data = client.objects.get(nomination_number = nom_num)
	context = {}
	if not print_counter(request.user, "pdf", nom_num):
		return HttpResponse("Not Authorized", status=403)
	# print(qr_data)
	primary_info = {
		'Nomination ID' : data.nomination_number,
		'Name': data.first_name + ' ' + data.last_name,
		'Adress': data.current_address,
		'Date': data.entry_date,
		'DOB' : data.date_of_birth
	
	}

	sec_info = {
		'Fathers Name': data.father_name,
		'Mobile': data.mobile_number_1,
		'Nomination Fees' : data.nomination_fees,
		'Sharing Amount' : data.sharing_amount
	}

	context['photo'] = os.getcwd() + data.photograph.url
	context['primary_info'] = primary_info
	context['sec_info'] = sec_info
	context['logo'] = os.getcwd() + '/media/users/logo.jpg'
	
	
	# context['headers'] = ['Name','Marks','y','x','z']
	# context['rows'] = [ ['ram',200,2,3,4] ,['sam',300,5,6,7] ]

	# print(primary_info , qr_data.photograph.url)

	# pdf = render_to_pdf('employee/reciepts/temp.html',context)
	# return HttpResponse(pdf, content_type='application/pdf')

	page = render(request,'employee/reciepts/pdf.html',context)
	page = page.content.decode('utf-8')

	print(page)
	pdf = pdfkit.from_string(page, False , options={'orientation':'landscape'})
	return HttpResponse(pdf, content_type='application/pdf')

	# return render(request,'employee/reciepts/pdf.html',context)



@login_required
def cash_coll(request , bill_num):
	
	c = cash_collection.objects.get(bill_number=bill_num)
	context = {"c":c}
	if not print_counter(request.user, "cash_col", bill_num):
		return HttpResponse("Not Authorized", status=403)
	reciept_amt = c.total_loan_deposit + c.total_society_deposit

	p_ = sum([i[0] for i in c.emp_payments_set.all().values_list("amount")])
	context['net'] = reciept_amt - p_
	context['tot_reciept'] = reciept_amt
	context['tot_payment'] = p_
	page = render(request,'employee/reciepts/cash_coll.html',context)
	# return page
	page = page.content.decode('utf-8')

	print(page)
	pdf = pdfkit.from_string(page, False , options={
	'orientation':'portrait',
	'page-size': 'A4',
	'dpi': '300',
	})
	return HttpResponse(pdf, content_type='application/pdf')


@login_required
def noc(request , fc_num):
	a = approved_finance_table.objects.get(finance__loan_account_number = fc_num)
	if not print_counter(request.user, "noc", fc_num):
		return HttpResponse("Not Authorized", status=403)
	person = a.finance.person
	recent_col =  a.collection_finance_set.all().order_by('-id')[0].loan_emi_received_date
	
	context = {'person' : person}
	context['col_date'] = recent_col
	context['f'] = a
	context['date'] = timezone.now()
	# return render(request,'employee/reciepts/noc.html',context)

	page = render(request,'employee/reciepts/noc.html',context)
	page = page.content.decode('utf-8')

	print(page)
	pdf = pdfkit.from_string(page, False , options={
	'orientation':'portrait',
	'page-size': 'A4',
	'dpi': '300',
	})
	return HttpResponse(pdf, content_type='application/pdf')



@login_required
def withdrawl(request , num):
	d = withdrawl_entry.objects.get(bill_no=num)
	if not print_counter(request.user, "withdrawl", num):
		return HttpResponse("Not Authorized", status=403)
	ds = collection_deposit.objects.filter(deposit=d.society_account)
	pa = sum([x.payment_received for x in ds])
	context = {'d': d, 'pa': pa}
	page = render(request,'employee/reciepts/withdrawl.html',context)
	page = page.content.decode('utf-8')
	pdf = pdfkit.from_string(page, False , options={
	'orientation':'portrait',
	'page-size': 'A4',
	'dpi': '300',
	})
	return HttpResponse(pdf, content_type='application/pdf')
