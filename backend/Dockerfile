FROM python:3.11-alpine
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt --no-cache-dir
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn foodgram.wsgi:application --bind 0:8000"]
