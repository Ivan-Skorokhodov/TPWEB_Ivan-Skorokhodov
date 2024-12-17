# gunicorn_config.py

wsgi_app = "TPWEB_Ivan_Skorokhodov.wsgi:application"

bind = "127.0.0.1:8000"

workers = 2
