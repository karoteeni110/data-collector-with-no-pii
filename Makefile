
SHELL := /bin/bash

install: requirements.txt
	pip3 install -r requirements.txt

test-flask: 
	cd 02-flask-app && pwd && \
		python3 app.py

aws-cred: 
	source ~/venvs/aws/bin/activate && samlauth.py
