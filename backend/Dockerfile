FROM python:3.7-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .

WORKDIR /app/foodgram/

CMD ["gunicorn", "foodgram_project.wsgi:application", "--bind", "0:8000"]
