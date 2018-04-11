FROM centos

RUN yum -y update \
 && yum -y install \
    epel-release \
 && yum -y install \
    https://centos7.iuscommunity.org/ius-release.rpm \
 && yum -y install \
    gcc \
    httpd24u \
    httpd24u-devel \
    python36u \
    python36u-pip \
    python36u-devel \
    python36u-setuptools \
    python36u-tools \
 && yum clean all \
 && pip3.6 install --upgrade pip

ENV production true

COPY requirements.txt /tmp/requirements.txt

RUN pip3.6 install -r /tmp/requirements.txt mod_wsgi \
 && rm /tmp/requirements.txt

COPY deploy/entrypoint.sh /bin/entrypoint.sh

RUN chmod -R 755 /bin/entrypoint.sh

CMD entrypoint.sh
