#!/bin/bash

# Creacion de los containers que recorreremos

java -cp /jade/lib/jade.jar jade.Boot -gui -container 192.168.54.0 &
java -cp /jade/lib/jade.jar jade.Boot -gui -container 192.168.54.0 &
java -cp /jade/lib/jade.jar jade.Boot -gui -container 192.168.54.0 &
java -cp /jade/lib/jade.jar jade.Boot -gui -container 192.168.54.0 &
java -cp /jade/lib/jade.jar jade.Boot -gui -container 192.168.54.0 &

sleep 3 # Así se crean bien los containers

# Hay que cambiar el puerto porque el 1099 ya va a estar ocupado
java -cp /jade/lib/jade.jar:../jade/classes jade.Boot -gui -container -agents ej1:ejercicio1.Agente -host 192.168.54.0





