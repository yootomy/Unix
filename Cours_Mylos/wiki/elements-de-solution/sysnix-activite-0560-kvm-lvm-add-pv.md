[[_TOC_]]

# SYSNIX - Ajouter un nouveau volume physique 

>Ajouter un nouveau volume physique à un groupe de volume existant


## Marche à suivre 

```
             .---------------------------------..---------------------------------.
Hote         | LV - /dev/vg/vmLvm3             || fichier - ~/tmp/pool/vol1.img   | 
             +---------------------------------++---------------------------------+
Guest        | /dev/vda                        || /dev/vdb                        | 
             +---------------------------------++---------------------------------+
partition    | /dev/vda1                       || /dev/vdb1                       | 
             | primaire                        || primaire                        |
             +---------------------------------++---------------------------------+
LVM          | PV                              || PV                              |
             +---------------------------------++---------------------------------+
             | VG  vmLvm3-vg                                                      | 
             +-----------------------+---------+----------------------------------'
             | LV root               |LV swap_1|
             +-----------------------+---------+
             | ext4                  | swap    |
             +-----------------------+---------'
             | /                     | swap    |
             `-----------------------+---------'
```


1. Créer le stockage dans le cas d'une vm.
1. Ajouter le nouveau stockage à la machine.
1. Étendre le groupe de volume avec le nouveau stockage


## Création d'un stockage avec virsh

### Création d'un nouveau pool de stockage
* Créer le dossier de stockage

```
$ mkdir ~/tmp/pool
```

* Créer le pool de stockage de libvirt avec virsh

```
virsh # pool-define-as  poolTmp --type dir  --target /home/dhu/tmp/pool
pool home défini
```
* Afficher le fichier xml du nouveau pool

```
virsh # pool-dumpxml poolTmp
<pool type='dir'>
  <name>poolTmp</name>
  <uuid>5fbfa77f-3eb2-4a3d-813c-fc83249776c9</uuid>
  <capacity unit='bytes'>98291167232</capacity>
  <allocation unit='bytes'>31762505728</allocation>
  <available unit='bytes'>66528661504</available>
  <source>
  </source>
  <target>
    <path>/home/dhu/tmp/pool</path>
    <permissions>
      <mode>0775</mode>
      <owner>1000</owner>
      <group>1000</group>
    </permissions>
  </target>
</pool>
```

* Démarrer le pool

```
virsh # pool-start poolTmp
Pool poolTmp démarré
```
* Afficher la liste des pools

```
virsh # pool-list
 Nom                  État      Démarrage automatique
-------------------------------------------
 default              actif      yes       
 iso                  actif      yes       
 poolTmp              actif      no        
 vgdata               actif      yes       
```

* Création du volume vol1.img de 1G dans le pool poolTmp

```
virsh # vol-create-as poolTmp vol1.img --capacity 1G --format raw
Volume vol1.img créé
```
* Afficher la liste des volume du pool

```
virsh # vol-list poolTmp
 Nom                  Chemin                                  
------------------------------------------------------------------------------
 vol1.img             /home/dhu/tmp/pool/vol1.img             
```


* Afficher le chemin du nouveau volume

```
virsh # vol-path vol1.img --pool poolTmp
/home/dom/tmp/pool/vol1.img
```


### Ajouter le nouveau stockage à la machine
* Ajoute du périphérique avec la commande attach-disk de virsh 

```
virsh # attach-disk --domain vmLvm3 --source /home/dhu/tmp/pool/vol1.img \
                    --target vdb --targetbus virtio \
                    --driver qemu --subdriver raw \
                    --sourcetype file --persistent
```

**source**: valeur de `virsh vol-path`

**target**: nom du périphérique vda, vdb, vdc,... 


* Contenu de la description de la vm après l'ajout


```
virsh # edit vmLvm3
```

```
<domain type='kvm'>
...
  <devices>
    ...
    <disk type='file' device='disk'>
      <driver name='qemu' type='raw'/>
      <source file='/home/dhu/tmp/pool/vol1.img'/>
      <target dev='vdb' bus='virtio'/>
    </disk>
    ...
  </devices>
</domain>
```




## Étendre le groupe de volume avec le nouveau stockage

* démarrer la vm


### Afficher la liste des disques de la vm

```
guest:~$ sudo fdisk -l
```

```
...
Disque /dev/vdb : 1 GiB, 1073741824 octets, 2097152 secteurs
Unités : sectors of 1 * 512 = 512 octets
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
...
```

### Définir  le périphérique comme volume physique

```
guest:~$ sudo pvcreate /dev/vdb
  Physical volume "/dev/vdb" successfully created
```


```
guest:~$ sudo pvdisplay /dev/vdb
  "/dev/vdb" is a new physical volume of "1.00 GiB"
  --- NEW Physical volume ---
  PV Name               /dev/vdb
  VG Name               
  PV Size               1.00 GiB
  Allocatable           NO
  PE Size               0   
  Total PE              0
  Free PE               0
  Allocated PE          0
  PV UUID               H3OTVp-v9Kx-7kF2-Y5R0-Mg3f-aYx9-iwckBl
```


### Étendre le groupe de volume vg avec le nouveau volume physique

```
guest:~$ sudo vgextend vmLvm3-vg /dev/vdb
  Volume group "vmLvm1-vg" successfully extended
```


```
guest:~$ sudo pvdisplay /dev/vdb
  --- Physical volume ---
  PV Name               /dev/vdb
  VG Name               vmLvm1-vg
  PV Size               1.00 GiB / not usable 4.00 MiB
  Allocatable           yes 
  PE Size               4.00 MiB
  Total PE              255
  Free PE               255
  Allocated PE          0
  PV UUID               E4xjuB-46FK-Pepk-Tc1d-sWK5-1E6H-sMrasL
```


```
guest:~$ sudo vgdisplay -v
    Finding all volume groups
    Finding volume group "vg"
  --- Volume group ---
...   
  --- Logical volume ---
...   
  --- Physical volumes ---
 PV Name               /dev/vda5     
  PV UUID               e5IYDk-aL45-kFxU-gmZq-cQiy-FMAM-3XiDpg
  PV Status             allocatable
  Total PE / Free PE    1413 / 0
   
  PV Name               /dev/vdb     
  PV UUID               E4xjuB-46FK-Pepk-Tc1d-sWK5-1E6H-sMrasL
  PV Status             allocatable
  Total PE / Free PE    255 / 255
```


>A partir de là, le groupe de volume possède de la place supplémentaire pour créer de nouveaux volumes logiques.
