
Помощь в deploy:
https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04

### Проверка готовности проекта к deploy на сервер
```
python3 manage.py check --deploy 
```
Для переноса данных:
```
python manage.py dumpdata --exclude auth.permission --exclude contenttypes > db.json
```

```
python manage.py loaddata db.json
```
### POSTGRESQL

```
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add - ;
RELEASE=$(lsb_release -cs) ;
echo "deb http://apt.postgresql.org/pub/repos/apt/ ${RELEASE}"-pgdg main | sudo tee  /etc/apt/sources.list.d/pgdg.list ;
sudo apt update ;
sudo apt -y install postgresql-11 ;
sudo passwd postgres
su - postgres
export PATH=$PATH:/usr/lib/postgresql/11/bin
createdb --encoding UNICODE dbms_db --username postgres
exit
sudo -u postgres psql
    create user dbms with password 'some_password';
    ALTER USER dbms CREATEDB;
    grant all privileges on database dbms_db to dbms;
    \c dbms_db
    GRANT ALL ON ALL TABLES IN SCHEMA public to dbms;
    GRANT ALL ON ALL SEQUENCES IN SCHEMA public to dbms;
    GRANT ALL ON ALL FUNCTIONS IN SCHEMA public to dbms;
    CREATE EXTENSION pg_trgm;
    ALTER EXTENSION pg_trgm SET SCHEMA public;
    UPDATE pg_opclass SET opcdefault = true WHERE opcname='gin_trgm_ops';
    \q
exit

nano ~/.pgpass
	localhost:5432:dbms_db:inside:some_password
chmod 600 ~/.pgpass
psql -h localhost -U inside dbms_db
```

Если ошибка PERMISSION:
```
ALTER DATABASE database OWNER TO user;
```

python manage.py migrate

### Установка компонентов на сервере
```
sudo apt install python3-pip python3-dev libpq-dev
```
```
sudo -H pip3 install --upgrade pip
cd /var/www/
```
Далее копируем наш локальный проект который загрузили на сервак
```cp /home/inside/stroytechmontazh /var/www/stroytechmontazh```
или копируем из github и извлекаем папку stroytechmontazh
```
git clone git@github.com:linksysadmin/django_stroytechmontazh.git
```
Создаем виртуальное окружение в папке stroytechmontazh:
```
cd stroytechmontazh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Меняем настройки в settings.py
```
nano config/settings.py
    ALLOWED_HOSTS = ['your_server_domain_or_IP', 'second_domain_or_IP', . . ., 'localhost']
```
Добавляем суперпользователя:
```
python manage.py createsuperuser
```
Собираем весь статический контент в настроенном каталоге, выполнив следующую команду:
```
python manage.py collectstatic
```
Наконец, протестируйте свой проект, запустив сервер разработки Django с помощью следующей команды:
```
python manage.py runserver 0.0.0.0:8000
```
#### Настройка Gunicorn
Прежде чем покинуть виртуальную среду, протестируйте Gunicorn, чтобы убедиться, что он может обслуживать приложение. Вы можете сделать это, сначала перейдя в каталог вашего проекта:
```
gunicorn --bind 0.0.0.0:8000 config.wsgi
deactivate
```
Создание системных сокетов и служебных файлов для Gunicorn
Теперь, когда вы проверили, что Gunicorn может взаимодействовать с вашим приложением Django, вам следует реализовать более надежный способ запуска и остановки сервера приложений. Для этого вы создадите файлы службы и сокета systemd.
```
sudo nano /etc/systemd/system/gunicorn.socket
    [Unit]
    Description=gunicorn socket
    
    [Socket]
    ListenStream=/run/gunicorn.sock
    
    [Install]
    WantedBy=sockets.target
```

```
sudo nano /etc/systemd/system/gunicorn.service
    [Unit]
    Description=gunicorn daemon
    Requires=gunicorn.socket
    After=network.target
    
    [Service]
    User=inside
    Group=www-data
    WorkingDirectory=/var/www/stroytechmontazh
    ExecStart=/var/www/stroytechmontazh/venv/bin/gunicorn \
              --access-logfile - \
              --workers 3 \
              --bind unix:/run/gunicorn.sock \
              config.wsgi:application
    
    [Install]
    WantedBy=multi-user.target
    
```

Далее запустите сокет Gunicorn. Это создаст файл сокета в /run/gunicorn.sock сейчас и при загрузке:
```
sudo systemctl start gunicorn.socket
```
Затем включите его, чтобы при подключении к этому сокету systemd автоматически запускал Gunicorn.service для его обработки:
```
sudo systemctl enable gunicorn.socket
```

Проверьте статус процесса, чтобы узнать, удалось ли ему запуститься:
```
sudo systemctl status gunicorn.socket

```
Затем проверьте наличие файла Gunicorn.sock в каталоге /run:
```
file /run/gunicorn.sock
```

Если команда systemctl status указывает на то, что произошла ошибка или вы не можете найти файл Gunicorn.sock в каталоге, это указывает на то, что сокет Gunicorn был создан неправильно. Проверьте журналы сокета Gunicorn, выполнив следующую команду:
```sudo journalctl -u gunicorn.socket```

Если вы только запустили модуль Gunicorn.socket, Gunicorn.service еще не будет активен, поскольку сокет не получил никаких подключений. Проверьте статус:

```
sudo systemctl status gunicorn
```
Чтобы протестировать механизм активации сокета, отправьте соединение с сокетом через curl:
```
curl --unix-socket /run/gunicorn.sock localhost
```
Если выходные данные Curl или выходные данные systemctl status указывают на возникновение проблемы, проверьте журналы для получения дополнительных сведений:
```
sudo journalctl -u gunicorn
```
Проверьте файл /etc/systemd/system/gunicorn.service на наличие проблем. Если вы вносите изменения в файл /etc/systemd/system/gunicorn.service, перезагрузите демон, чтобы перечитать определение сервиса:
```
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
```

### Nginx
Теперь, когда Gunicorn настроен, вам нужно настроить Nginx для передачи трафика процессу.
Начните с создания и открытия нового блока сервера в каталоге доступных сайтов Nginx:

```
server {
    listen 80;
    server_name server_domain_or_IP;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/sammy/myprojectdir;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```
Сохраните и закройте файл, когда закончите. Теперь вы можете включить файл, связав его с каталогом с поддержкой сайтов:
```
sudo ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled
```


```
sudo nginx -t
sudo systemctl restart nginx
```





### Логи
```
sudo tail -F /var/log/nginx/error.log
```
Check the Nginx process logs: 
```sudo journalctl -u nginx```

Check the Nginx access logs: 
```sudo less /var/log/nginx/access.log```

Check the Nginx error logs: 
```sudo less /var/log/nginx/error.log```

Check the Gunicorn application logs:
``` sudo journalctl -u gunicorn```
```sudo journalctl -u gunicorn -n 10```

Check the Gunicorn socket logs: 
```sudo journalctl -u gunicorn.socket```


### UPDATE SETTINGS
If you update your Django application, you can restart the Gunicorn process to pick up the changes by running the following:
```
sudo systemctl restart gunicorn
```
If you change Gunicorn socket or service files, reload the daemon and restart the process by running the following:
```
sudo systemctl daemon-reload && sudo systemctl restart gunicorn.socket gunicorn.service
```

If you change the Nginx server block configuration, test the configuration and then Nginx by running the following:
```
sudo nginx -t && sudo systemctl restart nginx
```


Добавляем Robots.txt
```
User-agent: *                   
                                                   
Allow: /rss/*
Sitemap: https://stroytechmontazh.ru/sitemap.xml
```


Nginx .conf

```
server {
        server_name stroytechmontazh.ru www.stroytechmontazh.ru;
        charset utf-8;
        location = /favicon.ico { access_log off; log_not_found off; }
        location /static/ {
                root /var/www/stroytechmontazh;           #путь до static каталога
                expires max;
        }

        location /robots.txt {
                alias /var/www/stroytechmontazh/robots.txt;
        }

        location /media/ {
                root /var/www/stroytechmontazh;           #путь до media каталога
        }

        location / {
            include proxy_params;
            proxy_pass http://unix:/run/gunicorn.sock;
        }

    listen 443 ssl http2; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/stroytechmontazh.ru/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/stroytechmontazh.ru/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot


}
server {
    if ($host = stroytechmontazh.ru) {
        return 301 https://$host$request_uri;
    } # managed by Certbot


        server_name stroytechmontazh.ru www.stroytechmontazh.ru;
    listen 80;
    return 404; # managed by Certbot


}
```


### Настройка sitemap.xml
settings.py
```
INSTALLED_APPS = [
    'django.contrib.sitemaps',
    'django.contrib.sites',
    ...
    ]

SITE_ID = 1
```



sitemaps.py
```
from django.contrib.sitemaps import Sitemap
from flushing.models import *


class ServicesSitemap(Sitemap):
    def items(self):
        return FlushingService.published.all()


class ArticlesSitemap(Sitemap):
    def items(self):
        return Article.published.all()


class TopicArticleSitemap(Sitemap):
    def items(self):
        return TopicArticle.objects.all()
```

stroytechmontazh/config/urls.py
```
from django.contrib.sitemaps.views import sitemap
from .sitemaps import *

sitemaps = {
    'services': ServicesSitemap,
    'articles': ArticlesSitemap,
    'topic_articles': TopicArticleSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path('', include('flushing.urls')),
]
```
http://127.0.0.1:8000/admin
Изменить url адрес для формирования sitemap.xml на свое доменное имя
```
sudo systemctl daemon-reload && sudo systemctl restart gunicorn.socket gunicorn.service
```





