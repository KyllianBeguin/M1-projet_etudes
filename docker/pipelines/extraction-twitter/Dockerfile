FROM python:3.11

COPY ./mnt/requirements.txt .
RUN pip install -r requirements.txt
RUN pip3 install git+https://github.com/JustAnotherArchivist/snscrape.git

CMD [ "/bin/bash" ]