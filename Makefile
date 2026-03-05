mig:
	./manage.py makemigrations
	./manage.py migrate

loaddata:
	./manage.py loaddata currencies languages categories techstacks