Vagrant.require_version ">= 1.8"

Vagrant.configure("2") do |config|

  begin
    cant_vm = Integer(ENV['VMS'])
    gui = Integer(ENV['GUI'])
    if gui < 0 or gui > 1
      raise TypeError
    end
  rescue TypeError, ArgumentError 
    puts "Uso:\nVMS=[int: vms a crear] GUI=[1=true o 0=false] vagrant [comando]"
    exit
  end

  # VM donde estará el main container
  config.vm.define "main" do |main|
    main.vm.box = "hashicorp/bionic64"
    
    main.vm.provider "virtualbox" do |vb|
      vb.linked_clone = true
    end

    # IP
    main.vm.network "private_network", ip: "192.168.50.4"

    if gui == 1 
      main.vm.provider "virtualbox" do |vb|
        vb.memory = 1024
        vb.gui = true # para que inicie el gui
      end
      # Descargo el Desktop Environment que utilizará para la gui
      main.vm.provision :shell, path: "gui_main_container.sh"
    else 
      main.vm.provider "virtualbox" do |vb|
        vb.memory = 512
      end
    end

    main.vm.provision :shell, path: "get_java.sh" # Instalamos openjdk-8

    # Borro la sincronización con la carpeta . que viene por defecto
    main.vm.synced_folder ".", "/vagrant", disabled: true
    # Sincronizo una carpeta donde hay que poner el JADE
    main.vm.synced_folder "jade/", "/jade", :mount_options => ["dmode=777", "fmode=666"]
    
  end

  # El resto de las vms
  (2..cant_vm).each do |i|
    config.vm.define "vm#{i}" do |vm|
      vm.vm.box = "hashicorp/bionic64" # Base box ubuntu

      vm.vm.provider "virtualbox" do |vb|
        vb.linked_clone = true
        vb.memory = 512
      end

      vm.vm.synced_folder ".", "/vagrant", disabled: true
      vm.vm.synced_folder "jade/", "/jade", :mount_options => ["dmode=777", "fmode=666"]

      vm.vm.provision :shell, path: "get_java.sh" # Instalamos openjdk-8
      
      vm.vm.network "private_network", type: "dhcp"

      # Creamos filesystems para cada vm y los sincronizamos
      # Dir.mkdir("vm#{i}") unless File.exists?("vm#{i}")
      # config.vm.synced_folder "vm#{i}/", "/filesystem"
    end
  end

end
