FROM ubuntu:18.04

RUN apt-get -y update && apt-get -y upgrade && echo "update ok"

RUN apt-get -y install supervisor

RUN apt-get -y install python3.7

RUN apt-get -y install python3-pip

ADD ./sources.list /etc/apt/


RUN apt-get -y autoclean && apt-get -y autoremove && apt-get -y clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /server/

# RUN cp ./* /server/

EXPOSE 80 8000 443 

ENTRYPOINT [ "supervisord" ]

CMD ["-c", "/server/Patricklab/supervisor/lab.conf"]
