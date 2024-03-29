# pull official base image
FROM python:3.11

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

# install dependencies
# install spacy dependencies
COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN python -m pip install tensorflow
RUN pip install -U pip setuptools wheel
RUN pip install seaborn
RUN pip install whitenoise
RUN pip install gunicorn
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -U spacy
RUN python -m spacy download en_core_web_sm

# copy project
COPY . .

# collect static files
RUN python manage.py collectstatic --noinput

# add and run as non-root user
RUN adduser -D myuser
USER myuser

# run gunicorn
CMD gunicorn app.wsgi:application --bind 0.0.0.0:$PORT
