FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./hotel_pymongo.py ./
CMD [ "python", "./hotel_pymongo.py" ]

