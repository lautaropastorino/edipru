import sys, subprocess, os, argparse, platform, pathlib

def read_files(args):
    """ Lee un path y verifica que exista. Luego lo asocia a una vm.
        Devuelve un diccionario del tipo 
        {"vm0": [(path, nombre, args, package)], "vm1": [(path, nombre, args, package)], ...}
    """
    files = {}
    vms = args.vms[0]
    for i in range(0, vms):
        files[f"vm{i}"] = []
        if i == 0:
            print(f"Agentes a compilar y ejecutar en main")
        else:
            print(f"Agentes a compilar y ejecutar en vm{i}")
        f = input("Nombre del archivo (0 para siguiente vm): ")
        while (f != "0"):
            if os.path.isfile(f):
                f = pathlib.Path(f)
                a = input("Nombre que tomará el agente: ")
                if a == "" or a[0].isnumeric():
                    n = len(files[f"vm{i}"])
                    a = f"Agente_{i}_{n}"
                    print(f"Nombre de agente inválido, se le asignará {a}")
                p = input("Nombre del package java (puede ser vacío): ")
                if p == "": # Si queda vacio le guardamos un 0 para poder darse cuenta en el shell script
                    p = "0" 
                args = input("Argumentos separados por espacios (puede ser vacío): ")
                if args == "": # Lo mismo que con p
                    args = "0"
                files[f"vm{i}"].append((f, a, p, args))
            else:
                print("El archivo no existe, verifique el path")
            f = input("Nombre del archivo (0 para siguiente vm): ")
        print()
    return files

def main():
    parser = argparse.ArgumentParser(description="Utilidad de línea de comandos para construir un entorno de desarrollo distribuido utilizando JADE")
    parser.add_argument("-s", "--start", action="store_true", help="Iniciar el entorno una vez construido el Vagrantfile")
    parser.add_argument("-v", "--vms", required=True, type=int, nargs=1, action="store", help="Indicar la cantidad de máquinas virtuales a generar")
    parser.add_argument("-g", "--gui", action="store_true", help="Utilizar interfaz gráfica en la máquina virtual principal. No se puede utilizar al mismo tiempo que -f/--files")
    parser.add_argument("-f", "--files", action="store_true", help="Indicar que se tienen que compilar y ejecutar archivos. No se puede utilizar al mismo tiempo que -g/--gui")

    args = parser.parse_args()

    files = {}

    if args.files and args.gui:
        print("No se puede utilizar GUI al mismo tiempo que FILES")
        sys.exit()
    elif args.files:
        files = read_files(args)

    vagrant_file = open("Vagrantfile", "w")
    vagrant_file.close()

    try:
        os.mkdir("jade")
    except FileExistsError:
        pass

    sistema_operativo = "ps1" if platform.system() == 'Windows' else 'sh' # Cambio la extension según el SO 

    with open("Vagrantfile", "a") as vagrant_file:
        vagrant_file.write("""Vagrant.require_version ">= 1.8"\nVagrant.configure("2") do |config|""")

        # MAIN VM
        vagrant_file.write("""
    config.vm.define "main" do |main|
        main.vm.box = "hashicorp/bionic64"
        main.vm.provider "virtualbox" do |vb|
            vb.linked_clone = true
        end
        main.vm.network "private_network", ip: "192.168.50.4"
        main.vm.synced_folder ".", "/vagrant", disabled: true
        main.vm.synced_folder "jade/", "/jade", :mount_options => ["dmode=777", "fmode=666"]
        main.vm.synced_folder "mainFS/", "/mainFS", :mount_options => ["dmode=777", "fmode=666"], :create => true
        """)

        if args.gui: # GUI
            vagrant_file.write("""
        main.vm.provider "virtualbox" do |vb|
            vb.memory = 1024
            vb.gui = true # para que inicie el gui
        end
        main.vm.provision :shell, path: "gui_main_container.sh"
            """)
        else:
            vagrant_file.write(""" 
        main.vm.provider "virtualbox" do |vb|
            vb.memory = 512
        end
        main.trigger.after :up do |trigger|
            trigger.info = "Iniciando Jade en la main vm..."
            trigger.run = {path: """)
            vagrant_file.write(f""""start_main.{sistema_operativo}" """)
            vagrant_file.write("""}
        end
            """)

        if files:
            for f in files["vm0"]:
                vagrant_file.write(f""" 
        main.trigger.after :up do |trigger|
            trigger.info = "Compilando y ejecutando agente {f[1]}"
        """)
                vagrant_file.write("""
            trigger.run = {:path => '""")
                vagrant_file.write(f"""compile_and_run.{sistema_operativo}', :args => '""")
                vagrant_file.write(f"""main {str(f[0])} {f[1]} {f[2]} "{f[3]}"'""")
                vagrant_file.write("""}
        end
        """)

        vagrant_file.write("""
        main.vm.provision :shell, path: "get_java.sh" # Instalamos openjdk-8    
    end
        """)

        for i in range(1, args.vms[0]):
            vagrant_file.write(f"""
    config.vm.define "vm{i}" do |vm|
        vm.vm.box = "hashicorp/bionic64" # Base box ubuntu
        vm.vm.provider "virtualbox" do |vb|
            vb.linked_clone = true
            vb.memory = 512
        end
        vm.vm.synced_folder ".", "/vagrant", disabled: true
        vm.vm.synced_folder "jade/", "/jade", :mount_options => ["dmode=777", "fmode=666"]
        vm.vm.synced_folder "vm{i}FS/", "/vm{i}FS", :mount_options => ["dmode=777", "fmode=666"], :create => true
        vm.vm.provision :shell, path: "get_java.sh" # Instalamos openjdk-8
        vm.vm.network "private_network", type: "dhcp"
            """)

            if files:
                for f in files[f"vm{i}"]:
                    vagrant_file.write(f""" 
        vm.trigger.after :up do |trigger|
            trigger.info = "Compilando y ejecutando agente {f[1]}"
        """)
                    vagrant_file.write("""
            trigger.run = {:path => '""")
                    vagrant_file.write(f"""compile_and_run.{sistema_operativo}', :args => '""")
                    s = f[0]
                    if sistema_operativo == "ps1": #En windows tengo que poner /// entre cada carpeta
                        s = str(f[0]).split("\\")
                        s = r"///".join(s)
                    vagrant_file.write(f"""vm{i} {s} {f[1]} {f[2]} "{f[3]}"'""")
                    vagrant_file.write("""}
        end
            """)
        
            vagrant_file.write("""
    end""")
        vagrant_file.write("""
end""")

    if args.start: #Levantar el entorno
        print("Iniciando entorno...\n")
        subprocess.run(["vagrant", "up"])
        

if __name__ == "__main__":
    main()