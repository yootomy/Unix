[[_TOC_]]

# SYSNIX - Création d'un nouveau volume logique 

>Ajouter un nouveau volume logique, formater et monter ce volume logique au système de fichiers existant


## Marche à suivre 


```
             .---------------------------------..---------------------------------.
Hote         | LV - /dev/vg/vmLvm3             || fichier - ~/tmp/pool/vol1.img   | 
             +---------------------------------++---------------------------------+
Guest        | /dev/vda                        || /dev/vdb                        | 
             +---------------------------------++---------------------------------+
partition    | /dev/vda1                       || /dev/vda1                       | 
             | primaire                        || primaire                        |
             +---------------------------------++---------------------------------+
LVM          | PV                              || PV                              | 
             +---------------------------------++---------------------------------+
             | VG  vmLvm3-vg                                                      | 
             +-----------------------+---------+----------+-----------------------'
             | LV root               |LV swap_1|  LV data |                       
             +-----------------------+---------+----------+
             |  ext4                 | swap    | ext4     |
             +-----------------------+---------+----------'
             | /                     | swap    |  /mnt    |
             `-----------------------+---------+----------'
```

Dans le machine vmLvm3, 
* Créer un nouveau volume logique __data__
* Formater ce volume logique en __ext4__
* Monter ce stockage en __/mnt__
* Faire en sorte que le montage soit permanent.


## Créer un nouveau volume logique __data__


```
ubuntu@vmlvm3:~$ sudo lvcreate -L 500M -n data vmLvm3-vg
  Logical volume "data" created.
```


```
ubuntu@vmlvm3:~$ sudo lvdisplay /dev/vmLvm3-vg/data
  --- Logical volume ---
  LV Path                /dev/vmLvm3-vg/data
  LV Name                data
  VG Name                vmLvm3-vg
  LV UUID                2tBqRy-ZsJM-n5gU-kIrP-AxMc-FQWS-yByneO
  LV Write Access        read/write
  LV Creation host, time vmlvm3, 2018-02-19 14:52:31 +0100
  LV Status              available
  # open                 0
  LV Size                500.00 MiB
  Current LE             125
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           252:2
```


```
ubuntu@vmlvm3:~$ sudo vgdisplay -v
    Using volume group(s) on command line.
  --- Volume group ---
  VG Name               vmLvm3-vg
  System ID             
  Format                lvm2
  Metadata Areas        2
  Metadata Sequence No  5
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                3
  Open LV               2
  Max PV                0
  Cur PV                2
  Act PV                2
  VG Size               4.52 GiB
  PE Size               4.00 MiB
  Total PE              1156
  Alloc PE / Size       1026 / 4.01 GiB
  Free  PE / Size       130 / 520.00 MiB
  VG UUID               kldwgg-YSld-puZC-YXPv-TVb9-hbs6-hNFGxg
   
  --- Logical volume ---
  LV Path                /dev/vmLvm3-vg/root
  LV Name                root
  VG Name                vmLvm3-vg
  LV UUID                tjWB1D-VUbY-VMbY-CG7X-26xA-FSdc-ud4Nga
  LV Write Access        read/write
  LV Creation host, time vmLvm3, 2018-01-30 14:14:07 +0100
  LV Status              available
  # open                 1
  LV Size                2.52 GiB
  Current LE             645
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           252:0
   
  --- Logical volume ---
  LV Path                /dev/vmLvm3-vg/swap_1
  LV Name                swap_1
  VG Name                vmLvm3-vg
  LV UUID                41jmAs-STdq-m9G8-QcMv-xKG2-Elne-kjNMVv
  LV Write Access        read/write
  LV Creation host, time vmLvm3, 2018-01-30 14:14:07 +0100
  LV Status              available
  # open                 2
  LV Size                1.00 GiB
  Current LE             256
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           252:1
   
  --- Logical volume ---
  LV Path                /dev/vmLvm3-vg/data
  LV Name                data
  VG Name                vmLvm3-vg
  LV UUID                2tBqRy-ZsJM-n5gU-kIrP-AxMc-FQWS-yByneO
  LV Write Access        read/write
  LV Creation host, time vmlvm3, 2018-02-19 14:52:31 +0100
  LV Status              available
  # open                 0
  LV Size                500.00 MiB
  Current LE             125
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           252:2
   
  --- Physical volumes ---
  PV Name               /dev/vda5     
  PV UUID               V1Tk9G-9tLg-nFpX-aG2G-jfko-RFUI-vdNnre
  PV Status             allocatable
  Total PE / Free PE    901 / 0
   
  PV Name               /dev/vdb     
  PV UUID               So6WIr-2B8c-kdhv-RURY-m7Zi-oX01-6fp0JN
  PV Status             allocatable
  Total PE / Free PE    255 / 130
```

## Formater ce volume logique en __ext4__


```
ubuntu@vmlvm3:~$ sudo mkfs.ext4 /dev/vmLvm3-vg/data
mke2fs 1.42.13 (17-May-2015)
En train de créer un système de fichiers avec 512000 1k blocs et 128016 i-noeuds.
UUID de système de fichiers=e63c5298-82c1-4aca-abdd-3d5bca1e98a5
Superblocs de secours stockés sur les blocs : 
	8193, 24577, 40961, 57345, 73729, 204801, 221185, 401409

Allocation des tables de groupe : complété                        
Écriture des tables d'i-noeuds : complété                        
Création du journal (8192 blocs) : complété
Écriture des superblocs et de l'information de comptabilité du système de
fichiers : complété
```

## Monter ce stockage en __/mnt__

```
ubuntu@vmlvm3:~$ sudo mount -t ext4 /dev/vmLvm3-vg/data /mnt
```

```
ubuntu@vmlvm3:~$ mount -t ext4
/dev/mapper/vmLvm3--vg-root on / type ext4 (rw,relatime,errors=remount-ro,data=ordered)
/dev/mapper/vmLvm3--vg-data on /mnt type ext4 (rw,relatime,data=ordered)
```

## Faire en sorte que le montage soit permanent.

```
ubuntu@vmlvm3:~$ cat /etc/fstab 
# /etc/fstab: static file system information.
#
# Use 'blkid' to print the universally unique identifier for a
# device; this may be used with UUID= as a more robust way to name devices
# that works even if disks are added and removed. See fstab(5).
#
# <file system> <mount point>   <type>  <options>           <dump>  <pass>
/dev/mapper/vmLvm3--vg-root      /     ext4 errors=remount-ro    0 1
# /boot was on /dev/sda1 during installation
UUID=c4bcb41b-a988-4437-b7dc-4f4000b27de3 /boot  ext2  defaults  0 2
/dev/mapper/vmLvm3--vg-swap_1    none  swap sw       0 0

/dev/mapper/vmLvm3--vg-data	 /mnt  ext4 defaults 0 2
```

```
ubuntu@vmlvm3:~$ df -Th
Sys. de fichiers            Type     Taille Utilisé Dispo Uti% Monté sur
udev                        devtmpfs   226M       0  226M   0% /dev
tmpfs                       tmpfs       49M    1.2M   48M   3% /run
/dev/mapper/vmLvm3--vg-root ext4       2.5G    1.3G  1.1G  56% /
tmpfs                       tmpfs      245M       0  245M   0% /dev/shm
tmpfs                       tmpfs      5.0M       0  5.0M   0% /run/lock
tmpfs                       tmpfs      245M       0  245M   0% /sys/fs/cgroup
/dev/vda1                   ext2       472M     56M  393M  13% /boot
tmpfs                       tmpfs       49M       0   49M   0% /run/user/1000
/dev/mapper/vmLvm3--vg-data ext4       477M    2.3M  445M   1% /mnt
```
