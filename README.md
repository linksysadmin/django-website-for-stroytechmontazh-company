
Помощь в deploy:
https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04

### Проверка готовности проекта к deploy на сервер
```
python3 manage.py check --deploy 
```
Для переноса данных:
python manage.py dumpdata --exclude auth.permission --exclude contenttypes > db.json



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
    User=sammy
    Group=www-data
    WorkingDirectory=/home/sammy/myprojectdir
    ExecStart=/home/sammy/myprojectdir/myprojectenv/bin/gunicorn \
              --access-logfile - \
              --workers 3 \
              --bind unix:/run/gunicorn.sock \
              myproject.wsgi:application
    
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

sudo tail -F /var/log/nginx/error.log

Check the Nginx process logs: 
```sudo journalctl -u nginx```

Check the Nginx access logs: 
```sudo less /var/log/nginx/access.log```

Check the Nginx error logs: 
```sudo less /var/log/nginx/error.log```

Check the Gunicorn application logs:
``` sudo journalctl -u gunicorn```

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