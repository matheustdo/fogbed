FROM larsid/soft-iot-base:1.1.3
LABEL maintainder="AllanCapistrano <asantos@ecomp.uefs.br>"

ENV COLLECT_TIME=200 \
    PUBLISH_TIME=2000

ADD servicemix-init.sh /usr/local/bin/servicemix-init.sh

RUN chmod +x /usr/local/bin/servicemix-init.sh

RUN apt update -y \
	&& apt install net-tools -y\
	&& apt install iproute2 -y\
	&& apt install iputils-ping -y 

ENTRYPOINT ["/bin/bash", "./usr/local/bin/servicemix-init.sh"]