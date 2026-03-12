mig:
	./manage.py makemigrations
	./manage.py migrate

loaddata:
	./manage.py loaddata currencies languages categories techstacks users employer_user companies mixed
flush:
	./manage.py flush