# -*- mode: ruby -*-
# et ft=ruby :
#
Vagrant.configure("2") do |config|
  config.vm.box = "fedora/25-cloud-base"
  config.vm.box_version = "20161122"

    config.vm.network "public_network", dev: "virbr0",
      mode: "bridge", type: "bridge", libvirt__network_name: "default"
end
