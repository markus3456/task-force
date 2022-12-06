FROM ubuntu
RUN apt-get update -y && \
    apt-get install -y python-dev-is-python3 python3-psycopg2\
    python3-pip
    

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "python" ]

CMD ["routes.py","python3", "-m" , "flask", "run", "--host=0.0.0.0"]