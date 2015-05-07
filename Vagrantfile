# -*- mode: ruby -*-
# vi: set ft=ruby :
# sudo apt-get update
$script = <<SCRIPT
APP_DIR = /vagrant/clScrape

echo Installing dependencies...
apt-get update
apt-get install -y python-pip python-virtualenv build-essential python-dev libxml2-dev python-lxml libxml2-dev libxslt-dev zlib1g-dev
cd ${APP_DIR}
virtualenv .venv
. /${APP_DIR}/.venv/bin/activate
pip install -r /${APP_DIR}/requirements.txt
python manage.py runserver > /tmp/scrape.log 2>&1 &
echo "App running on 0.0.0.0:5000, vagrant ssh; tail -f /tmp/scrape.log; hit it with http://localhost:5000"
SCRIPT

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.provider "virtualbox" do |vb|
    vb.memory = 1024
  end
  config.vm.box = "ubuntu/trusty64"
  config.vm.box_url = "https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box" 
  config.vm.provision "shell", inline: $script, :privileged => true
  
  config.vm.network "forwarded_port", guest: 5000, host: 5000
  config.vm.network "private_network", ip: "55.55.55.5"
end
