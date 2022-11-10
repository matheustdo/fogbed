#!/bin/bash

# ----------- Criando br.ufba.dcc.wiser.soft_iot.local_storage.cfg ------------#
rm -rf opt/servicemix/etc/br.ufba.dcc.wiser.soft_iot.local_storage.cfg

cat <<EOF >opt/servicemix/etc/br.ufba.dcc.wiser.soft_iot.local_storage.cfg
#Host of MQTT server used by devices
MQTTHost=localhost

#Port of MQTT server used by devices
MQTTPort=1883

#Username and password of MQTT server used by devices. If broker MQTT accepts anonymous connection, you can keep these properties empty
#If you are using ActiveMQ Artemis as broker you need to use the same user and password of Karaf
MQTTUsername=karaf
MQTTPassword=karaf

#Name of MQTT server connection. Only used for internal operations.
MQTTServerId=FoTGatway


#In SOFT-IoT platform to get data from sensor the local storage module need two informations:
#(These properties are used when collection/publishing configuration of device hasn't been defined)
#The first is the collection time (in milliseconds) of data sensors  
DefaultCollectionTimeSensorData=$COLLECT_TIME
#The second is the publishing time (in milliseconds), that it will set the time of the device will publish in broker MQTT a array with every collected data.
DefaultPublishingTimeSensorData=$PUBLISH_TIME

#Number of hours of data that the system will keep stored. Data with older than this time will be cleaned
NumberOfHoursDataStored=24

# Enable/Disable debug mode that shows data generate and steps of module
debugMode=false
EOF

# -------------------------- Iniciando o container -----------------------------#
bash