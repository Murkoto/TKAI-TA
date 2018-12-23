FROM python:3

EXPOSE 5000
RUN mkdir /app
WORKDIR /app
COPY . /app

RUN pip install psycopg2 Flask-SQLAlchemy Flask-Migrate
CMD [ "python", "manage.py", "migrate" ]
CMD [ "python", "user.py"]