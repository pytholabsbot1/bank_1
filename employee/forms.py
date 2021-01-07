from django import forms
from django.forms.fields import CharField, DateField, IntegerField, FloatField
from django.contrib.auth.models import User
from .models import *


class ReportForm(forms.Form):

        date_field = forms.CharField(label='date_field', max_length=100)
        from_date = forms.DateField(widget=forms.TextInput(attrs={ 'class':'datepicker' }))
        to_date = forms.DateField(widget=forms.TextInput(attrs={ 'class':'datepicker' }))

        table = forms.CharField(label='table', max_length=100)
        
        target = forms.CharField(label='Target Table', max_length=100)
        # filter_by = forms.CharField(label='Filter By', max_length=100)
        filter_val = forms.CharField(label='Filter Value', max_length=100)
        search_by = forms.CharField(label='Search By', max_length=100)
        search_val = forms.CharField(label='Search Value', max_length=100)
        order_by = forms.CharField(label='Order By', max_length=100,required=False)

        display_fields = forms.CharField(label='Display Fields', max_length=1000)

        client = forms.ModelChoiceField(queryset=client.objects.all() , required=True)


class AgentCollectionReport(forms.Form):
        from_date = forms.DateField(widget=forms.TextInput(attrs={ 'class':'datepicker' }))
        to_date = forms.DateField(widget=forms.TextInput(attrs={ 'class':'datepicker' }))

        search_val = forms.CharField(label='Nomination Number', max_length=16,required=False)
        account_val = forms.CharField(label='Account Number', max_length=16 , required=False)
        filter_val = forms.ModelChoiceField(queryset = DepositChoice.objects.all() , required=False)

        all_ = forms.BooleanField(required=False)
        audit = forms.BooleanField(required=False , initial = True ,label='-' )

class ClientCollectionReport(forms.Form):
        from_date = forms.DateField(widget=forms.TextInput(attrs={ 'class':'datepicker' }))
        to_date = forms.DateField(widget=forms.TextInput(attrs={ 'class':'datepicker' }))

        search_val = forms.CharField(label='Nomination Number', max_length=16 , required=False)
        account_val = forms.CharField(label='Account Number', max_length=16 , required=False)

        all_ = forms.BooleanField(required=False)
        audit = forms.BooleanField(required=False , initial = True ,label='-' )

class Ledger(forms.Form):
        from_date = forms.DateField(widget=forms.TextInput(attrs={ 'class':'datepicker' }))
        to_date = forms.DateField(widget=forms.TextInput(attrs={ 'class':'datepicker' }))

        nom_num = forms.CharField(label='Nomination Number', max_length=100 , required=False)
        Ledger_for = forms.ChoiceField(choices = ( ("Society","Society") ,("Loan","Loan") ) , required=False)
        audit = forms.BooleanField(required=False , initial = True ,label='-' )
       
class MajorReport(forms.Form):
        from_date = forms.DateField(widget=forms.TextInput(attrs={ 'class':'datepicker' }))
        to_date = forms.DateField(widget=forms.TextInput(attrs={ 'class':'datepicker' }))
        search = forms.CharField(required=False, widget=forms.Select(choices = [('', 'Select'),]))
        audit = forms.BooleanField(required=False , initial = True ,label='-' )

class CashBook(forms.Form):
        from_date = forms.DateField(widget=forms.TextInput(attrs={ 'class':'datepicker' }))
        to_date = forms.DateField(widget=forms.TextInput(attrs={ 'class':'datepicker' }))
        audit = forms.BooleanField(required=False , initial = True ,label='-' )

class DividendReport(forms.Form):
        financial_year = forms.DateField(widget=forms.TextInput(attrs={ 'class':'datepicker' }))
        percentage = forms.IntegerField(required=False)
        audit = forms.BooleanField(required=False , initial = True ,label='-' )
        
class EmpReport(forms.Form):
        from_date = forms.DateField(widget=forms.TextInput(attrs={ 'class':'datepicker' }))
        to_date = forms.DateField(widget=forms.TextInput(attrs={ 'class':'datepicker' }))

        filter_val = forms.ChoiceField(choices=(("Finance","Finance"),("Deposits","Deposits")) , required=False)

class ClientReport(forms.Form):
        acc_num = forms.CharField(label='Account Number', max_length=20)
        secure_key = forms.CharField(label='Secure Key', max_length=16)

class DailyCash(forms.Form):
        from_date = forms.DateField(widget=forms.TextInput(attrs={ 'class':'datepicker' }))
        to_date = forms.DateField(widget=forms.TextInput(attrs={ 'class':'datepicker' }))
        search = forms.CharField(required=False, widget=forms.Select(choices = [('', 'Select'),]))
        all_ = forms.BooleanField(required=False)
        audit = forms.BooleanField(required=False , initial = True ,label='-' )

class UpcomingMaturity(forms.Form):
        from_date = forms.DateField(widget=forms.TextInput(attrs={ 'class':'datepicker' }))
        to_date = forms.DateField(widget=forms.TextInput(attrs={ 'class':'datepicker' }))

class AccountStatus(forms.Form):
        STATUS =("ACTIVE", ("ACTIVE")), ("DEACTIVE", ("DEACTIVE")),("SUSPENDED", ("SUSPENDED")),("HOLD", ("HOLD")),("DEAD", ("DEAD"))
        TYPES = ("DEPOSIT", ("DEPOSIT")), ("LOAN", ("LOAN")), ("BOTH", ("BOTH"))
        status = forms.ChoiceField(choices = STATUS, required=True)
        account_type = forms.ChoiceField(choices = TYPES, required=True)