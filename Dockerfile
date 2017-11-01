FROM python:2.7.10

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

RUN cp /usr/local/lib/libcrfpp.so.0 /usr/lib/

EXPOSE 5000

RUN mkdir /app
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

RUN python /app/setup.py install

CMD python app.py