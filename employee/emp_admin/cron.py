from django.core import management
import os
from datetime import datetime as dt
from pathlib import Path
from datetime import date
from employee.models import *

def daily():
    #use management.call_command

    # paths = sorted(Path("/home/vaqas/backups").iterdir(), key=os.path.getmtime)

    # if(len(paths)>6):
    #     os.remove(paths[-1])
    os.system('sudo -i -u postgres pg_dump -Fc  --dbname=postgresql://vaqas:kdsfmsbAAMNVJHFHVjvhjhfks8736587365smdnbmfnsdbf2836487sdjbfjsd@127.0.0.1:5432/banking_data > /home/vaqas/daily_backups/backup_{}.pgdump'.format(str(dt.now()).replace(' ','_').split('.')[0]))


def monthly():
     os.system('sudo -i -u postgres pg_dump -Fc  --dbname=postgresql://vaqas:kdsfmsbAAMNVJHFHVjvhjhfks8736587365smdnbmfnsdbf2836487sdjbfjsd@127.0.0.1:5432/banking_data > /home/vaqas/monthly_backups/backup_{}.pgdump'.format(str(dt.now()).replace(' ','_').split('.')[0]))
    

def ten_day_no_deposit():
	accounts = deposits_table.objects.all()
	for account in accounts:
		deposits = collection_deposit.objects.filter(deposit=account).order_by('created_time')
		latest_deposit = deposits[len(deposits)-1]
		last_day_difference = (latest_deposit.payment_received_date - date.today()).days
		#if the last deposit was made more than ten days ago
		if last_day_difference >= 10:
			account.status = "HOLD"
			account.save()
			print("THE ACCOUNT IS NOW PUT ON HOLD!")
		else:
			if account.status != "ACTIVE":
				account.status == "ACTIVE"
				account.save()
				print("THE ACCOUNT IS NOW ACTIVE!")
    



    