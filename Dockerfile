FROM python:3.12 

WORKDIR /app

RUN pip install pipenv setuptools

RUN apt-get update && apt-get install -y build-essential

COPY Pipfile Pipfile.lock ./

RUN pipenv install --deploy --ignore-pipfile --python /usr/local/bin/python3.12

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["pipenv", "run", "gunicorn", "contactsapi.wsgi:application", "--bind", "0.0.0.0:8000"]
