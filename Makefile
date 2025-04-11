install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt


deploy:
	aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 318489830920.dkr.ecr.us-east-1.amazonaws.com
	docker build -t video-summarization .
	docker tag video-summarization:latest 318489830920.dkr.ecr.us-east-1.amazonaws.com/video-summarization:latest
	docker push 318489830920.dkr.ecr.us-east-1.amazonaws.com/video-summarization:latest
	
all: install  deploy