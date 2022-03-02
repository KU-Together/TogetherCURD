FROM python:3.9.8

RUN apt-get update

ENV DJANGO_SECRET_KEY $DJANGO_SECRET_KEY
ENV DB_HOST $DB_HOST
ENV DB_PORT $DB_PORT
ENV DB_PASSWORD $DB_PASSWORD

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8001
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "TogetherCURD.wsgi",  "--bind", "0.0.0.0:8001"]