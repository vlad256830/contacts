# contacts
test application Contacts
readme
celery -A src worker -l info
flower --port=5555
celery flower -A src --address=127.0.0.1 --port=5555
