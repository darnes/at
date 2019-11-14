FROM fedora:31
RUN mkdir /home/at/
WORKDIR /home/at/

RUN yum -y install python-pip gcc python-devel rpm-build python-psycopg2

ADD src /home/at/

RUN pip install -r dshw/requirements.txt

# todo: run tests
RUN cd dshw && python setup.py bdist_rpm
