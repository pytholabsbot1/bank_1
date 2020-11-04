os.system('sudo -i -u postgres pg_dump -Fc  --dbname=postgresql://vaqas:kdsfmsbAAMNVJHFHVjvhjhfks8736587365smdnbmfnsdbf2836487sdjbfjsd@127.0.0.1:5432/banking_data > /home/vaqas/backup.pgdump')


# refresh the server
Vaqasahmed!21998

sudo pkill gunicorn
sudo systemctl daemon-reload
sudo systemctl start gunicorn


# save github password
git config --global credential.helper store



# banking_dump

JUpyter notebook access : http://34.70.237.129:9780/?token=1b
c57402ae260bfa6885a8fddbb27cb8caa7a1bcb5cf76ba


Pass : 1bc57402ae260bfa6885a8fddbb27cb8caa7a1bcb5cf76ba

Superuser :
admin
sidhilekhraj!

source myprojectenv/bin/activate

# setup on other Machine




1. Installation

sudo apt-get update -y
sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib virtualenv nginx -y
pip3 install django django-crispy-forms django-mysql qrcode[pil] xhtml2pdf pdfkit django-session-timeout

# for PDF Generation Install this
wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox_0.12.5-1.bionic_amd64.deb
sudo dpkg -i wkhtmltox_0.12.5-1.bionic_amd64.deb

<!--  -->
pip3 install git+git://github.com/ojii/pymaging.git#egg=pymaging
pip3 install git+git://github.com/ojii/pymaging-png.git#egg=pymaging-png


>>> User creation
sudo adduser vaqas
sudo usermod -aG sudo vaqas

sudo adduser banking_data
sudo usermod -aG sudo banking_data

su - vaqas

sudo ufw enable
sudo ufw allow OpenSSH
sudo ufw allow 8000
sudo ufw allow 5432

Add rules with tags 
>>>>>>>>>>>>>>>>>>>>>>>>>>>


path : /Library/PostgreSQL/11/bin/pg_ctl restart -D /Library/PostgreSQL/11/data/

postgres :

sudo -i -u postgres
psql
CREATE DATABASE banking_data;
CREATE USER vaqas WITH PASSWORD 'kdsfmsbAAMNVJHFHVjvhjhfks8736587365smdnbmfnsdbf2836487sdjbfjsd';
ALTER ROLE vaqas SET client_encoding TO 'utf8';
ALTER ROLE vaqas SET default_transaction_isolation TO 'read committed';
ALTER ROLE vaqas SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE banking_data TO vaqas;
ALTER DATABASE banking_data OWNER TO vaqas;
\q
exit

>>>>>>>

git clone https://github.com/ish/banking_dump.git

cd banking_dump
pip3 install virtualenv jupyter notebook 


virtualenv --python=python3.6 myprojectenv
source myprojectenv/bin/activate
pip3 install -r req.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser


dev: python3 manage.py runserver 0.0.0.0:8000
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>



Setup gunicorn :

sudo nano /etc/systemd/system/gunicorn.service

[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=vaqas
Group=www-data
WorkingDirectory=/home/vaqas/banking_dump
ExecStart=/home/vaqas/banking_dump/myprojectenv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/vaqas/sidhi_society.sock sidhi_society.wsgi:application

[Install]
WantedBy=multi-user.target

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
nginx Setup:

sudo nano /etc/nginx/sites-available/sidhi_society

server {
    listen 80;
    server_name 34.70.237.129;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/vaqas/banking_dump;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/vaqas/sidhi_society.sock;
    }
}

sudo ln -s /etc/nginx/sites-available/sidhi_society /etc/nginx/sites-enabled

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

Update changes on server

sudo pkill gunicorn
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl restart gunicorn


sudo nginx -t
sudo systemctl restart nginx
sudo ufw delete allow 8000
sudo ufw allow 'Nginx Full'
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

Configure postgres remote connection :

sudo nano /etc/postgresql/10/main/pg_hba.conf

ADD at end*
host all all 0.0.0.0/0 md5

sudo nano /etc/postgresql/10/main/postgresql.conf 

localhost ---> '*'

restart = sudo service postgresql restart

>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


sudo ufw allow 8000

jupyter notebook --ip=0.0.0.0 --port=9780


>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

Adding ssl 

follow -> https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-16-04

# sudo certbot --nginx -d pytholabs.org -d www.pytholabs.org

# sudo certbot certonly --standalone --preferred-challenges http -d pytholabs.org
# sudo ls /etc/letsencrypt/live/pytholabs.org


Resources : 


https://docs.bitnami.com/aws/apps/noalyss/administration/configure-pgadmin/

https://www.digitalocean.com/community/tutorials/how-to-set-up-a-scalable-django-app-with-digitalocean-managed-databases-and-spaces

https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04#create-and-configure-a-new-django-project

https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04



DROP ALL TABLES OF DATABASE:

1. open psql and login to banking_data as vaqas

psql -U vaqas banking_data
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO vaqas;
GRANT ALL ON SCHEMA public TO public;

<!-- dump -->



###### Alternate Database

<!-- create copy database of original  -->

use crontab for cronjobs in django 

CREATE DATABASE shit_data TEMPLATE banking_data;

sudo -i -u postgres dropdb dummy

 sudo -i -u postgres pg_dump -Fc --dbname=postgresql://vaqas:kdsfmsbAAMNVJHFHVjvhjhfks8736587365smdnbmfnsdbf2836487sdjbfjsd@127.0.0.1:5432/banking_data > backup.pgdump &&\
 
 sudo -i -u postgres createdb dummy &&\
 
 sudo -i -u postgres pg_restore -d dummy backup.pgdump