# -*- mode: ruby -*-
# vi: set ft=ruby :
$script = <<SCRIPT
    cd /vagrant
    sudo dnf install -y tito tracer

    # the following deps fail during the tito --install due to tito using --cache-only option, so install them beforehand
    sudo dnf install -y python2-cssselect python2-html5lib python2-rpm python2-webencodings python2-future python2-psutil

    sudo dnf builddep -y tracer.spec
    tito build --rpm --test --install
SCRIPT
Vagrant.configure("2") do |config|
  config.vm.box = "fedora/30-cloud-base"
  config.vm.synced_folder "./", "/vagrant"
  config.vm.provision "shell", inline: $script

  config.vm.provider :libvirt do |provider|
    provider.memory = 1024
  end
end
