# $args[0] = vm en la que ejecutar el codigo
# $args[1] = path al codigo en el host
# $args[2] = nombre que debe tomar el agente en el entorno
# $args[3] = nombre del package java (puede ser vacio)
# $args[4:] = args

$vm = $args[0]
$path = $args[1]
$agente = $args[2]
$package = $args[3]

# Copio el codigo al filesystem de la vm
Copy-Item $path -Destination $PWD\${vm}FS\

# Obtengo el nombre del archivo sin la extension
$nombre=(Get-Item $path).Basename

$params = @()
for ($i = 4; $i -lt $args.Count; $i++) {
    $params += $args[$i]
}


# Compilo y guardo dentro de la carpeta compartida jade/classes
$compile="javac -classpath /jade/lib/jade.jar -d /jade/classes /${vm}FS/$($nombre).java"

# SSH a la vm y ejecuto el código compilado
if ( 0 -eq $package ) { # no hay package name
    $run="java -cp /jade/lib/jade.jar:/jade/classes jade.Boot -container -host 192.168.50.4 -agents '$($agente):$($nombre)("
} else { # hay package name
    $run="java -cp /jade/lib/jade.jar:/jade/classes jade.Boot -container -host 192.168.50.4 -agents '$($agente):$($package).$($nombre)("
}

for ($i = 0; $i -lt $params.count; $i++) {  # para cada arg
    $param = $params[$i]
    $run = $run + "'$param' " # agrego el arg entre ''
}

$run=$run + ")'" # cierro parentesis

Write-Host $compile
Write-Host $run

$cmd = 'vagrant ssh ' + $vm  + ' -- "' + $compile + ' && ' + $run + '"'
Write-Host $cmd

$sb = [scriptblock]::Create($cmd)
Start-Job -ScriptBlock $sb 
Wait-Job -ID 1 -Timeout 120
