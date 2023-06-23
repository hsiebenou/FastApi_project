# BASE IMAGE
FROM python:3.10
# Set environment python path
ENV PYTHONPATH /app

# Set work directory
WORKDIR /app

# Add application
COPY . /app

# upgrade pip and install requirements
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80",  "--reload"]
