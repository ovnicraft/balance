Balance Score Card
==================

Proyecto para creación de un Balance Scorecard liviano


Uso:

    python manage.py runserver

Iniciando:

    pip install virtualenv
    virtualenv bsc
    source bsc/bin/activate
    pip install Django==1.6
    git clone https://github.com/ovnicraft/balance.git
    cd balance
    pip install -r requirements.txt
    python manage.py syncdb
    python manage.py runserver

Observaciones:

    Por defecto el settings.py usa sqlite para ambientes de producción
    se recomienda usar Postgres.