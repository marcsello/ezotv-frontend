FROM python:3

ADD ezotv requirements.txt /ezotv/
WORKDIR /ezotv/ezotv

RUN pip3 install -r  ../requirements.txt && pip3 install gunicorn

EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "ezotv:app"]

