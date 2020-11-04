from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from employee.models import *
import qrcode
from qrcode.image.pure import PymagingImage
from PIL import Image
from django.contrib.sessions.models import Session
from django.db.models import Q

# to check sessions
# users = User.objects.all()
# for user in users:
#     LoggedInUser.objects.get_or_create(user=user)

@login_required()
def index(request): 
	context={}
	
# -------------------------------------this section is for admin console-------------------------------- 
	
	if request.user.is_superuser :
		context ={}
		#------------------------------  fetching details of clients console who had applied for loan---------------------
		try:
			data = finance_table.objects.all().values_list('loan_holder_name','father_name','entry_date','loan_account_number','expected_date','expected_amount','nomination_number')
		except Exception as exp:
			return HttpResponse(str(exp))

		data_dict = { el[-1] : (el[0],el[1],el[2],el[3],el[4],el[5]) for el in data }
		context['data']= data_dict  # sending dictionary of client to admin console who had applied for loan

		#--------------------   for getting info of all loggedin users --------------------------------------
		active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
		user_id_list = []
		for session in active_sessions:
			data = session.get_decoded()
		user_id_list.append(data.get('_auth_user_id', None))
		loggedin_users = User.objects.filter(id__in=user_id_list).values_list('username','email')
		context['loggedin'] = loggedin_users
		#------------------------------------------------------------------------------------
		return render(request,'employee/admin_console.html',context)

		#---------------- for employee console ------------------------------------------------
	elif emp_joining.objects.filter(employee_id = (str(request.user)).split("_")[-1]).exists():
		
		attributes =  ['employee_id','employee_name','employee_photograph','father_name',
		'current_address','mobile_number_1','email_id','referal','referal_mobile_number_1']
		#---------------- fetching details of current user -----------------------------------

		
		details_emp = employee_interview.objects.filter(employee_id = str(request.user).split("_")[-1])
		data = { attribute : getattr(details_emp[0],attribute) for attribute in attributes}
		data['joining_date'] = emp_joining.objects.filter(employee_id = (str(request.user)).split("_")[-1])[0].joining_date
		
		context['emp_data'] = data
		

		return render(request,"employee/employee_dashboard.html",context)
	else:
		return HttpResponse("Client")

# Create your views here.
