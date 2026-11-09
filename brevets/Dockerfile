FROM python:3.9-slim
LABEL maintainer="Makai DeBerry <Makai.deberry@gmail.com>"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["flask_brevets.py"]
