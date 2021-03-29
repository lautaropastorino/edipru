import sys, subprocess, os, argparse

def usage():
    return "Uso:\npython generator.py [1=true o 0=false iniciar entorno] [int num_vms] [1=true o 0=false GUI] [list archivos.java (opcional)]"

def main():

    parser = argparse.ArgumentParser(description="Utilidad de línea de comandos para construir un entorno de desarrollo distribuido utilizando JADE")
    parser.add_argument("-s", "--start", action="store_true", help="Iniciar el entorno una vez construido el Vagrantfile")
    parser.add_argument("-v", "--vms", required=True, type=int, nargs=1, action="store", help="Indicar la cantidad de máquinas virtuales a generar")
    parser.add_argument("-g", "--gui", action="store_true", help="Utilizar interfaz gráfica en la máquina virtual principal")

    args = parser.parse_args()

    vagrant_file = open("Vagrantfile", "w")
    vagrant_file.close()

    try:
        os.mkdir("jade")
    except FileExistsError:
        pass

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
            trigger.info = "Iniciando Jade..."
            trigger.run = {path: "start_main.sh"}
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
        vm.vm.provision :shell, path: "get_java.sh" # Instalamos openjdk-8
        vm.vm.network "private_network", type: "dhcp"
    end
            """)
        
        vagrant_file.write("""
end""")

    if args.start: #Levantar el entorno
        subprocess.run(["vagrant", "up"])
        

if __name__ == "__main__":
    main()