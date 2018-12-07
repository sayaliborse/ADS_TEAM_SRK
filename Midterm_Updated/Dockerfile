# Use an official Python runtime as a base image
FROM python:latest

#Create working directory
RUN mkdir -p /usr/src/Assignment3
#RUN mkdir -p /usr/src/Midterm_Part1/Data

# Set the working directory to /usr/src/Assignment3
WORKDIR /usr/src/Assignment3

# Copy the current directory contents into the container at /usr/src/Assignment3
COPY *.txt *.py *.json *.sh /usr/src/Assignment3/

# Bundle Midterm_Part1 source
#COPY . /usr/src/Midterm_Part1

RUN chmod +x /usr/src/Assignment3/run.sh

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
#RUN pip install jupyter notebook

#ENV PASSWD='sha1:828476503395:25e994e559920285505f622f746ef6beeb194e54'

#RUN mkdir -p -m 700 /root/.jupyter/ && \
#    echo "c.NotebookApp.ip = '*'" >> /root/.jupyter/rawDataEDA.ipynb

# Make port 8888 available to the world outside this container
#EXPOSE 8888

# Define environment variable
#ENV NAME World

# Run app.py when the container launches
#CMD ["./run.sh"]
#RUN /run.sh