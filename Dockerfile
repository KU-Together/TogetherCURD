FROM python:3.9.8

RUN apt-get update

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "TogetherCURD.wsgi",  "--bind", "0.0.0.0:8000"]