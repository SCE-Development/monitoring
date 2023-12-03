FROM prom/prometheus:latest

USER root

RUN wget http://security.ubuntu.com/ubuntu/pool/main/a/apt/apt_2.7.7_amd64.deb -O /apt.deb

RUN mkdir -p /var/lib/dpkg

RUN touch /var/lib/dpkg/status

RUN dpkg -i /apt.deb

RUN apt-get update

RUN apk add --update --no-cache openssh

RUN echo 123123

COPY ./prometheus/what.sh /

ENTRYPOINT [ "/what.sh" ]
