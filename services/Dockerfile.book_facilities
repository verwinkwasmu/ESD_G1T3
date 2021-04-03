FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./book_facilities.py ./invokes.py ./amqp_setup.py ./
CMD [ "python", "./book_facilities.py" ]