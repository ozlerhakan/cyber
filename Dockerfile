FROM python:3.5-slim-jessie

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY cyber.py ./

COPY final_model.pkl ./

EXPOSE 5000

ENV SERVER_CYBER=docker

CMD [ "python", "./cyber.py" ]