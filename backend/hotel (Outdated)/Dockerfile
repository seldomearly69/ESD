FROM python:3-slim
WORKDIR /backend/services/hotel
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./hotel.py .
CMD [ "python", "hotel.py" ]
