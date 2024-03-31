FROM python:3.8-slim

WORKDIR /backend/services/manage_booking

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "manage_booking.py"]