FROM python:3

# CRF++
RUN DEBIAN_FRONTEND=noninteractive && apt-get update && \
	apt-get -y upgrade && \
	git clone https://github.com/taku910/crfpp.git /crfpp && \
	cd /crfpp && \
	./configure && \
	sed -i '/#include "winmain.h"/d' crf_test.cpp && \
	sed -i '/#include "winmain.h"/d' crf_learn.cpp && \
	make && \
	make install

EXPOSE 5000

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

RUN python /app/setup.py install

CMD python app.py