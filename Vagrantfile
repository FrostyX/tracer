# -*- mode: ruby -*-
# vi: set ft=ruby :
$script = <<SCRIPT
    cd /vagrant
    sudo dnf install -y tito python-ipdb python-nose
    sudo dnf install -y tracer
    sudo dnf builddep -y tracer.spec
    tito build --rpm --test --install
SCRIPT
Vagrant.configure("2") do |config|
  config.vm.box = "boxcutter/fedora24"
  config.vm.synced_folder "./", "/vagrant"
  config.vm.provision "shell", inline: $script
end