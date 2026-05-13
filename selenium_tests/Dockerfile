FROM selenium/standalone-chrome:latest

USER root

WORKDIR /selenium_tests

COPY selenium_test.py .

RUN apt-get update && apt-get install -y python3 python3-pip

RUN pip3 install selenium pytest --break-system-packages

CMD ["pytest", "selenium_test.py"]