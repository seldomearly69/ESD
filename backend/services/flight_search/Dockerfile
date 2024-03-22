FROM python:3-slim

WORKDIR /backend/services/flight_search

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "flight_search.py"]