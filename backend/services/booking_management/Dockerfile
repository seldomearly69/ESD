FROM python:3.8-slim

WORKDIR /backend/services/booking_management

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "booking_management.py"]