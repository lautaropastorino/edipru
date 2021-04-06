# $args[0] = vm en la que ejecutar el codigo
# $args[1] = path al codigo en el host
# $args[2] = nombre que debe tomar el agente en el entorno
# $args[3] = args
# $args[4] = nombre del package java (puede ser vacio)

$vm = $args[0]
$path = $args[1]
$agente = $args[2]
$package = $args[4]

# Copio el codigo al filesystem de la vm
Copy-Item $path -Destination $PWD\${vm}FS\

# Obtengo el nombre del archivo sin la extension
$nombre=(Get-Item $path).Basename

$ARGS = @()
if ( $args[3] -ne 0 )
{
    $ARGS = -split $args[3] 
}

# Compilo y guardo dentro de la carpeta compartida jade/classes
$compile="javac -classpath /jade/lib/jade.jar -d /jade/classes /${vm}FS/$($nombre).java"

# SSH a la vm y ejecuto el código compilado
if ( 0 -eq $package ) { # no hay package name
    $run="java -cp /jade/lib/jade.jar:/jade/classes jade.Boot -container -host 192.168.50.4 -agents '$($agente):$($nombre)("
} else { # hay package name
    $run="java -cp /jade/lib/jade.jar:/jade/classes jade.Boot -container -host 192.168.50.4 -agents '$($agente):$($package).$($nombre)("
}

for ($i = 0; $i -lt $AGRS.count; $i++) {  # para cada arg
    $run = $run + "'$i' " # agrego el arg entre ''
}

$run=$run + ")'" # cierro parentesis

Write-Host $compile
Write-Host $run
vagrant ssh $vm -- "$compile && $run"