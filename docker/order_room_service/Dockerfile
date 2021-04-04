FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./order_room_service.py ./invokes.py ./amqp_setup.py ./
CMD [ "python", "./order_room_service.py" ]