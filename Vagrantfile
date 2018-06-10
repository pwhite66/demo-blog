# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

config.vm.box = "ubuntu/xenial64"

config.vm.box_check_update = true

config.vm.network "forwarded_port", guest: 8080, host: 8080
config.vm.network "forwarded_port", guest: 5432, host: 5432

config.vm.provision "shell", inline: <<-SHELL
  apt-get update
  apt-get upgrade

  apt-get install -y python3-pip

  cd /vagrant
  pip3 install -r requirements.txt

SHELL
end
