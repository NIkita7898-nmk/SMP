FROM python:3.10

WORKDIR /smp

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /smp/

EXPOSE 8000

RUN chmod 777 ./entrypoint.sh