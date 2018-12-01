FROM python:3.6

ADD assignment3_part1.py /

RUN pip install beautifulsoup4
RUN pip install lxml 
RUN pip install seaborn 
RUN pip install matplotlib
RUN pip install numpy 
RUN pip install mechanicalsoup

ENTRYPOINT  ["python","./assignment3_part1.py"]

CMD myinput
