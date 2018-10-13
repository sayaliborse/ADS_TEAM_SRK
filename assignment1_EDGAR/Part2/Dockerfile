FROM python:3.6

ADD Part2.py /


RUN pip install lxml
RUN apt-get update && apt-get -y install libxml2-dev libxslt1-dev libxslt-dev python-lxml
RUN pip install pandas
RUN pip install requests
RUN pip install tabulate
RUN pip install BeautifulSoup4
RUN pip3 install boto



CMD [ "python", "./Part2.py" ]

ENTRYPOINT  ["python","./Part2.py"]

CMD myinput

