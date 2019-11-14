FROM fedora:31
RUN mkdir /home/at/
WORKDIR /home/at/

ADD ./dist /home/at/

RUN yum install -y ./*.noarch.rpm