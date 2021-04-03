FROM python:3-slim
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./process_checkout.py ./invokes.py ./
CMD [ "python", "./process_checkout.py" ]