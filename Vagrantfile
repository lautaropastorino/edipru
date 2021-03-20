Vagrant.configure("2") do |config|

  begin
    cant_vm = Integer(ENV['VMS'])
  rescue TypeError, ArgumentError
    puts "Uso:\nVMS=[int: vms a crear] vagrant [comando]"
    exit
  end

  (1..cant_vm).each do |i|
    config.vm.define "vm#{i}" do |vm|
      vm.vm.box = "hashicorp/bionic64"
    end
  end

end
