install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt


deploy:
	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 354918363202.dkr.ecr.us-east-1.amazonaws.com
	docker build -t wikipedia .
	docker tag wikipedia:latest 354918363202.dkr.ecr.us-east-1.amazonaws.com/wikipedia:latest
	docker push 354918363202.dkr.ecr.us-east-1.amazonaws.com/wikipedia:latest
	
all: install test lint format deploy