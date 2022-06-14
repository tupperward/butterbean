FROM python:3
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y postgresql-client-13
ENTRYPOINT [ "python", "butterbean.py" ]