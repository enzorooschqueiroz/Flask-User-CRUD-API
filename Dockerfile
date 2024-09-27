FROM python:3.9.12-alpine3.15

EXPOSE 5000

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY app.py .

ENV FLASK_ENV=development

CMD ["flask", "run", "--host=0.0.0.0"]
