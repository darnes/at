FROM fedora:31
RUN mkdir /home/at/
WORKDIR /home/at/

RUN yum -y install python-pip gcc python-devel rpm-build python-psycopg2

ADD src /home/at/

RUN pip install -r dshw/requirements.txt
# todo: run tests
RUN cd dshw && python setup.py bdist_rpm


#todo: clean this file

# for installation:
# python setup.py bdist_rpm  --install-script     Specify a script for the INSTALL phase of RPM building
# https://github.com/django/django/blob/master/setup.cfg

# https://forums.docker.com/t/systemctl-status-is-not-working-in-my-docker-container/9075/12

# to list contents of package
# rpm -ql at_monitor