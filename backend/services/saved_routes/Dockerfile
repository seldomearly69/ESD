FROM python:3.8-slim

WORKDIR /backend/services/saved_routes

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "SavedRoutes.py"]
