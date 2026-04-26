[[_TOC_]]

# SYSNIX - Virtualisation, cloner une machine virtuelle KVM


>Cloner une VM libvirt+kvm en ligne de commande.

## Rappel

>Une machine virtuelle VM est composé de :
>1. une description de matériel
>1. stockages

## Cloner une machine virtuelle KVM

### Créer une nouvelle description de matériel

* Copier une description existante

```
hote:~$ virsh -c qemu:///system dumpxml vm1 > ./vm2.xml
```

* Adapter la nouvelle description

```
hote:~$ cat ./vm2.xml 
```

```
<domain type='kvm'>
  <name>vm2</name>
  <memory unit='KiB'>524288</memory>
  <currentMemory unit='KiB'>524288</currentMemory>
  <vcpu placement='static'>1</vcpu>
  <os>
    <type arch='x86_64' machine='pc-i440fx-xenial'>hvm</type>
    <boot dev='hd'/>
  </os>
  <features>
    <acpi/>
    <apic/>
  </features>  
  <devices>
    <emulator>/usr/bin/kvm-spice</emulator>
    <disk type='file' device='disk'>
      <driver name='qemu' type='raw'/>
      <source file='/home/dhu/VM/vm2disk.img'/>
      <target dev='vda' bus='virtio'/>
    </disk>
    <interface type='network'>
      <source network='default'/>
      <model type='virtio'/>
    </interface>
    <serial type='pty'>
      <target port='0'/>
    </serial>
    <console type='pty'>
      <target type='serial' port='0'/>
    </console>
    <input type='mouse' bus='ps2'/>
    <input type='keyboard' bus='ps2'/>
    <graphics type='spice' autoport='yes'>
      <image compression='off'/>
    </graphics>
    <video>
      <model type='qxl' ram='65536' vram='65536' vgamem='16384' heads='1'/>
    </video>
  </devices>
</domain>

```

### Dupliquer le stockage

```
hote:~$ cp ./vm1disk.img ./vm2disk.img
```

### Inscrire la nouvelle VM `vm2` dans libvirt

```
hote:~$ virsh -c qemu:///system define  ./vm2.xml
```


### Tester la nouvelle VM

* Démarrer la VM

```
hote:~$ virsh -c qemu:///system start  vm2
```

* Afficher la liste de VM

```
hote:~$ virsh list --all
 ID    Nom                            État
----------------------------------------------------
 2     vm2                            en cours d'exécution
 -     vm1                            fermé
 -     vmLvm1                         fermé
```

* Se connecter à la console texte

```
hote:~$ virsh -c qemu:///system console vm2
```

* effectuer la post-installation décrit dans [Virtualisation - Post-installation d'une VM](https://mylos.cifom.ch/cours/int-sys1-nix/fiches/virtualisation-post-installation/)


## Cloner une machine virtuelle KVM sur un serveur hôte distant

### Dupliquer le stockage

```
hote:~$ ssh ubuntu@hoteDistant "mkdir ~/vm"
hote:~$ scp vm2disk.img ubuntu@hoteDistant:~/vm
```

### Inscrire la nouvelle VM `vm2` dans libvirt

```
hote:~$ virsh -c qemu+ssh://ubuntu@hoteDistant/system define  ./vm2.xml
```

### Tester la nouvelle VM

* Démarrer la VM

```
hote:~$ virsh -c qemu+ssh://ubuntu@hoteDistant/system start  vm2
```

* Afficher la liste de VM

```
hote:~$ virsh -c qemu+ssh://ubuntu@hoteDistant/system list --all
 ID    Nom                            État
----------------------------------------------------
6     vm2                          en cours d'exécution
```

* Se connecter à la console texte

```
hote:~$ virsh -c qemu+ssh://ubuntu@hoteDistant/system console vm2
Connected to domain vm2
Escape character is ^]

Ubuntu 16.04.1 LTS vm1 ttyS0

vm2 login: 
```

# Références

1.  How to access the text console of a virtual KVM guest from within virsh | Jared Evans Global Microbrand,  [http://www.jaredlog.com/?p=1484][1]
2.  libvirt: Guest migration,  [https://libvirt.org/migration.html#offline][2]

[1]:http://www.jaredlog.com/?p=1484
[2]:https://libvirt.org/migration.html#offline

