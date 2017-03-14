## [Dressing room API](http://mydressing.ru)

#### Python 3.4.4

Debug mode settings in 
```text
local_settings.py
```

#### Run locally
```bash
python main.py
```
or
```bash
gunicorn 'main:gunicorn()' -c conf/gunicorn.conf.py
```

#### Run in production
```bash
sudo supervisorctl reload
sudo supervisorctl restart droom_api
```
