[[_TOC_]]

# SYSNIX - Virtualisation, cloner une machine virtuelle KVM dans un volume logique LVM

>Cloner une VM libvirt+kvm en ligne de commande. Le stockage de la VM est un volume logique LVM de l'hôte.


## Dupliquer le contenu d'un fichier dans un volume logique (LV)

### Créer un volume logique de 4G

* Création du volume logique

```
hote:~$ sudo lvcreate -n vm3 -L 4G vg
```

* ``vm3`` est le nouveau volume logique de ``4G`` dans le groupe de volume ``vg``


* Vérification

```
hote:~$ sudo lvdisplay /dev/vg/vm3
  --- Logical volume ---
  LV Path                /dev/vg/vm3
  LV Name                vm3
  VG Name                vgdata
  LV UUID                SbOzIU-KSvY-yNfA-yvRw-uZrQ-gYiB-s9LFjZ
  LV Write Access        read/write
  LV Creation host, time thinkdom, 2015-02-12 14:57:57 +0100
  LV Status              available
  # open                 0
  LV Size                4.00 GiB
  Current LE             1024
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           252:33
```


### Copie des données dans le volume logique

```
hote:~$ sudo dd if=vm1disk.img of=/dev/vg/vm3
```
>#### Autre possibilité
>```
>hote:~$ sudo qemu-img convert /var/lib/libvirt/images/vm1disk.img /dev/debian-usb-vg/vm3
>```


## Créer une nouvelle description de matériel

### Copier une description existante

```
hote:~$ virsh dumpxml vm1 > ./vm3.xml
```

### Adapter la nouvelle description. La source du stockage doit être ``/dev/vg/vm3``

```
hote:~$ cat ./vm3.xml 
```

```
<domain type='kvm'>
  <name>vm3</name>
  <memory unit='KiB'>524288</memory>
  <currentMemory unit='KiB'>524288</currentMemory>
  <vcpu placement='static'>1</vcpu>
  <os>
    <type arch='x86_64' machine='pc-i440fx-xenial'>hvm</type>
    <boot dev='hd'/>
  </os>
  <devices>
    <emulator>/usr/bin/kvm-spice</emulator>
    <disk type='block' device='disk'>
      <driver name='qemu' type='raw'/>
      <source dev='/dev/vg/vm3'/>
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

## Inscrire la nouvelle VM ``vm3`` dans libvirt

```
hote:~$ virsh -c qemu:///system define  ./vm3.xml
```

## Autre solution pour la création de la machine virtuelle

```
huguenindo@debian-usb:~$ virt-install --connect qemu:///system\
                                      -n vm3\
                                      -r 1024\
                                      --disk path=/dev/debian-usb-vg/vm3,format=raw,bus=virtio,size=4\
                                      --network network=default,model=virtio\
                                      --osinfo name=debian13\
                                      --boot hd
```


## Tester la nouvelle VM

* Démarrer la VM

```
hote:~$ virsh -c qemu:///system start  vm3
```

* Afficher la liste de VM

```
hote:~$ virsh list --all
 ID    Nom                            État
----------------------------------------------------
 6     vm3                          en cours d'exécution
```


* Se connecter à la console texte

```
hote:~$ virsh -c qemu:///system console vm3
Connected to domain vm3
Escape character is ^]

Ubuntu 16.04.1 LTS vm1 ttyS0

vm3 login: 
```


* finir  avec les commandes de [post-installation](https://mylos.cifom.ch/cours/int-sys1-nix/fiches/virtualisation-post-installation/)

    * Adapter le nom de la machine en modifiant les fichiers ``/etc/hostname``, ``/etc/hosts`` et la mise à jour des clés ssh après un premier reboot.


## Dupliquer le contenu d'un fichier dans un volume logique (LV) avec ``virsh``

### Pool de stockage

* Créer un pool de stockage ``poolDir``  dans un dossier

```
virsh # pool-define-as  poolDir --type dir  --target /home/dhu/tmp/pool
```

```
virsh # pool-dumpxml poolDir
<pool type='dir'>
  <name>poolDir</name>
  <uuid>5fbfa77f-3eb2-4a3d-813c-fc83249776c9</uuid>
  <capacity unit='bytes'>0</capacity>
  <allocation unit='bytes'>0</allocation>
  <available unit='bytes'>0</available>
  <source>
  </source>
  <target>
    <path>/home/dhu/tmp/pool</path>
  </target>
</pool>
```


* Pool de stockage ``poolLvm`` dans un groupe de volume (VG)

```
virsh # pool-create-as poolLvm logical\
                       --target /dev/vg\
                       --source-name vg                        
```

```
virsh # pool-dumpxml poolLvm
<pool type='logical'>
  <name>poolLvm</name>
  <uuid>1f3d6aa9-8deb-4a05-8f2f-6c2f2e2a90fa</uuid>
  <capacity unit='bytes'>0</capacity>
  <allocation unit='bytes'>0</allocation>
  <available unit='bytes'>0</available>
  <source>
    <device path='vg'/>
    <name>vg</name>
    <format type='lvm2'/>
  </source>
  <target>
    <path>/dev/vg</path>
  </target>
</pool>
```

### Volume de stockage

* Créer un volume ``vmLvm3`` dans le pool ``poolLvm``

```
virsh # vol-create-as poolLvm vmLvm3 4G --format raw
Volume vmLvm3 créé
```


```
virsh # vol-list poolLvm
 Name                 Path                                    
------------------------------------------------------------------------------
...
 vmLvm3                  /dev/vg/vmLvm3                             
... 
```

### Copie du contenu d'un volume dans un fichier local (volume -> fichier local)

```
virsh # vol-list default
 Name                 Path                                    
------------------------------------------------------------------------------
 kvm-vmLvm1.img       /var/lib/libvirt/images/vmLvm1.img  
```


```
virsh # vol-download --pool default vmLvm1.img ./vmLvm1.img
```


### Copie du contenu d'un fichier local dans un volume (fichier local -> volume)

* Copie le contenu du fichier ``./vm1disk.img`` dans le volume ``kvm-vm1`` du pool ``poolLvm``

```
virsh # vol-upload vmLvm3 ./vmLvm1.img --pool poolLvm
```

