FROM 420811272222.dkr.ecr.ap-southeast-1.amazonaws.com/rinz-staging-ecr:pythonbase_v2

RUN apk update && apk add --no-cache  tzdata git make  build-base cargo gcc 

RUN apk upgrade -U \
    && apk add --no-cache -u ca-certificates  libressl-dev  musl-dev libffi-dev libva-intel-driver supervisor python3-dev build-base linux-headers pcre-dev curl busybox-extras \
    && rm -rf /tmp/* /var/cache/*

COPY requirements.txt /
COPY lib/requirements.txt /lib/requirements.txt
RUN pip --no-cache-dir install --upgrade pip setuptools
RUN pip --no-cache-dir install --upgrade -r /lib/requirements.txt
RUN pip --no-cache-dir install -r requirements.txt

COPY conf/supervisor/ /etc/supervisor.d/
COPY . /webapps

WORKDIR /webapps
