#!/bin/bash

# SSH a la vm e iniciar jade
vagrant ssh main -- 'java -cp /jade/lib/jade.jar jade.Boot -gui' &
