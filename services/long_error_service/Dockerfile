FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./long_error_service.py ./invokes.py ./amqp_setup.py ./
CMD [ "python", "./long_error_service.py" ]