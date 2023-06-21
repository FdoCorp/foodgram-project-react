FROM python:3.11-alpine
WORKDIR /app
RUN pwd
RUN ls
COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . .
WORKDIR /app/foodgram/
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn foodgram.wsgi:application --bind 0:8000"]
