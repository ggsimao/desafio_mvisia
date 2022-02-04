FROM python:3 AS desafio_mvisia
EXPOSE 3000
ADD app.py management/* db/* handlers/* /
RUN pip3 install flask flask_bcrypt flask_session
CMD ["python3", "./app.py"]