FROM python:3.10.6-buster

WORKDIR /prod

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY aixhunter aixhunter
COPY setup.py setup.py
COPY django_project django_project
COPY api api
COPY manage.py manage.py
RUN mkdir models
RUN pip install .

# run development server
CMD ["gunicorn", "django_project.wsgi:application", "--workers", "2", "--bind", "0.0.0.0:8080", "--timeout", "500"]
