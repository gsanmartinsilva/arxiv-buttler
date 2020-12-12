# set base image (host OS)
FROM python:3.7

# set the working directory in the container
WORKDIR /home

# copy the dependencies file to the working directory
COPY requirements.txt ./

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# install pdftotext
RUN apt update
RUN apt install poppler-utils -y
RUN apt install vim -y

# Make directory for logs and for code
RUN mkdir arxiv-buttler

# Create volume inside /src
VOLUME arxiv-buttler

# run BASH
CMD bash
