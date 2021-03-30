#!/bin/bash

# $1 = vm en la que ejecutar el codigo
# $2 = path al codigo en el host
# $3 = nombre que debe tomar el agente en el entorno
# $4 = args
# $5 = nombre del package java (puede ser vacio)

# Copio el codigo al filesystem de la vm
cp $2 $1FS/

nombre=$(basename $2 | cut -f 1 -d '.') # obtengo el nombre del archivo sin la extension

ARGS=()
if [ "0" != "$4" ]; then # Si hay args
    IFS=' '     # space is set as delimiter
    read -ra ARGS <<< "$4" # Es como $4.split(" ") ==> Guardo los args en un arreglo
fi

# Compilo y guardo dentro de la carpeta compartida jade/classes
compile="javac -classpath /jade/lib/jade.jar -d /jade/classes /$1FS/$nombre.java"

# SSH a la vm y ejecuto el código compilado
if [ "0" = "$5" ]; then # no hay package name
    run="java -cp /jade/lib/jade.jar:/jade/classes jade.Boot -container -host 192.168.50.4 -agents '$3:$nombre("
else # hay package name
    run="java -cp /jade/lib/jade.jar:/jade/classes jade.Boot -container -host 192.168.50.4 -agents '$3:$5.$nombre("
fi

for i in "${ARGS[@]}"; do   # para cada arg
    run="$run'$i' " # agrego el arg entre ''
done

run="$run)'" # cierro parentesis

echo $compile
echo $run
vagrant ssh $1 -- "$compile && $run" 