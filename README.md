App for automatic information gather and propagation for the rent/sell of the real estate.

To run, just type here:
#Term 1
$ python manage.py runserver
#Term 2
$ celery -A parsers worker -l info
#Term 3
$ celery -A parsers beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler

But before, you must have:
$ pip install -r requirements.text

Also you should install and setup RabbitMQ package...

         \\
          \\_   \\
           (')   \\_
   ok!    / )=.---(')
        o( )o( )_-\_

(shhh, don't tell anyone you saw this here!)
