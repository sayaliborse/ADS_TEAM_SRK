FROM python:3.6

ADD Part1.py /
ADD ALL_CIK.csv /

RUN apt-get update && apt-get -y install libxml2-dev libxslt1-dev libxslt-dev python-lxml
RUN pip install lxml
RUN pip install pandas
RUN pip install requests
RUN pip install tabulate
RUN pip install BeautifulSoup4


CMD [ "python", "./Part1.py" ]

ENTRYPOINT  ["python","./Part1.py"]

CMD myinput

