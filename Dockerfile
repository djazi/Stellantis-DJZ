FROM python:3.8-slim-buster
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONNUNBUFFERED 1
ENV PATH="/scripts:${PATH}"
RUN pip install --upgrade pip

COPY ./requirements.txt /requirements.txt
RUN apt-get update
RUN apt-get install -y --no-install-recommends gcc libc-dev python3-dev musl-dev


RUN pip install -r /requirements.txt 


RUN mkdir /app
COPY ./Stellantis_Djz /app
WORKDIR /app
COPY ./scripts /scripts

RUN chmod +x /scripts/*

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

RUN useradd user
RUN chown -R user:user /vol

RUN chmod -R 755 /vol/web
RUN chown -R user:user /app
RUN chmod -R 755 /app
USER user

CMD ["entrypoint.sh"]


