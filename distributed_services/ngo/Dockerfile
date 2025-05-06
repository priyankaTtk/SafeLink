FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir flask requests
EXPOSE 5000
CMD ["python", "ngo_service.py"]
