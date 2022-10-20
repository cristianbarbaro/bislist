FROM python:3.10.8
ADD ./app /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD python main.py