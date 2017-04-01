## [Dressing room API](http://mydressing.ru)

#### Python 3.4.4

Debug mode settings in 
```text
local_settings.py
```

#### Run locally
```bash
python application.py
```
or
```bash
gunicorn 'application:gunicorn()' -c conf/gunicorn.conf.py
```

#### Run in production
```bash
sudo service supervisor reload
sudo service supervisor restart droom_api
```

#### Database
```bash
export FLASK_APP=application.py
flask db init                       # If first time
flask db migrate                    # And check the changes
flask db upgrade
```
[More about Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)
