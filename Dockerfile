FROM python:3.10.8
ADD ./app /code
COPY requirements.txt /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD python main.py