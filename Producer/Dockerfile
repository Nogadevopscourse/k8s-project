FROM python:2.7-onbuild
ENV PYTHONPATH /usr/src/app
WORKDIR /app
ADD producer.py /app
ADD requirements.txt /app
RUN pip install --requirement /app/requirements.txt

# Use ENTRYPOINT to pass arguments like --port
ENTRYPOINT ["python", "/app/producer.py"]
