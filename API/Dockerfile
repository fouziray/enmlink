FROM python:3.8.0

ENV PYTHONUNBUFFERED 1

WORKDIR /app/backend

COPY requirements.txt /app/backend/

RUN pip install -r requirements.txt

COPY . /app/backend/

EXPOSE 8000

CMD ["python","manage.py","runserver","0.0.0.0:8000"] 