FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_APP=main.py
ENV SECRET_KEY=Event
ENV JWT_SECRET_KEY=Cosmos
ENV MONGODB_URI=mongodb+srv://tobiolajide01:cosmos@cluster0.bvt94.mongodb.net/
ENV aws_access_key_id=AKIAW5WU5F3U5ZROK254
ENV aws_secret_access_key=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
ENV region_name=us-east-2
ENV aws_picture_url=https://cosmos-bucket1.s3.us-east-2.amazonaws.com/
ENV CELERY_BROKER_URL='redis://backend-redis-1:6379/0'
ENV CELERY_RESULT_BACKEND='redis://backend-redis-1:6379/0'

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "main:app"]
