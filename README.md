# edipru
Entorno DIstribuido de PRUebas automatizado para JADE sobre máquinas virtuales completas utilizando Vagrant

### Uso

El script generator.py es una utilidad de línea de comandos que acepta distintos parámetros:

* -h, --help         Mostrar un mensaje de ayuda que explica el uso de la herramienta y salir.
* -s, --start        Iniciar el entorno una vez construido el Vagrantfile
* -v VMS, --vms VMS  Indicar la cantidad de máquinas virtuales a generar
* -g, --gui          Utilizar interfaz gráfica en la máquina virtual principal. No se puede utilizar al mismo tiempo que -f/--files
* -f, --files        Indicar que se tienen que compilar y ejecutar archivos. No se puede utilizar al mismo tiempo que -g/--gui

El único argumento obligatorio es -v/--vms el cual indica la cantidad de máquinas virtuales que tendrá el entorno distribuido.

Dado que es un script escrito en Python se debe ejecutar con el comando `python generator.py`

Un ejemplo de uso de la herramienta es:

`$ python generator.py -v 3 -g -s`

El usuario está especificando que el entorno distribuido estará formado por 3 máquinas virtuales: una principal y dos secundarias. Además, el usuario indica que la máquina virtual principal se iniciará con interfaz gráfica. Finalmente, el usuario requiere que el entorno se inicie automáticamente una vez se cree el Vagrantfile.

La opción -f/--files sirve para que el usuario pueda indicar a cada máquina virtual de las generadas qué archivos .java debe compilar y ejecutar una vez se inicie el entorno. Si el usuario incluye esta opción en el comando inicial, deberá luego escribir en la línea de comandos la ruta de los archivos que desee. 

Si no se especifica la opción -s/--start, el entorno se podrá iniciar de igual manera utilizando el comando `vagrant up`
