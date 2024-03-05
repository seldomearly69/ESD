FROM python:3-slim
WORKDIR /backend/services/flight
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY ./flight.py .
CMD [ "python", "flight.py" ]
