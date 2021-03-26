#!/bin/bash

# Creacion de los containers que recorreremos

java -cp /jade/lib/jade.jar jade.Boot -container -host 192.168.50.4 &
java -cp /jade/lib/jade.jar jade.Boot -container -host 192.168.50.4 &
java -cp /jade/lib/jade.jar jade.Boot -container -host 192.168.50.4 &
java -cp /jade/lib/jade.jar jade.Boot -container -host 192.168.50.4 &
java -cp /jade/lib/jade.jar jade.Boot -container -host 192.168.50.4 &

sleep 3 # Así se crean bien los containers

# Hay que cambiar el puerto porque el 1099 ya va a estar ocupado
java -cp /jade/lib/jade.jar:/jade/classes jade.Boot -container -agents ej1:ejercicio1.Agente -host 192.168.50.4





