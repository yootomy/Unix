[[_TOC_]]


# SYSNIX - Virtualisation, extension de la taille d'un volume logique contenant une machine virtuelle utilisant LVM

>Étendre la taille de stockage d'un VM utilisant un volume logique comme stockage et en ligne de commande.



## Prérequis
Mettre en place une machine virtuelle `vmLvm3` stocké dans un volume logique `/dev/vg/vmLvm3`. Le système d'exploitation de la VM utilise le gestion de volume lvm.


### Information sur l'espace de stockage


```
.---------------------------------.
| LV - /dev/vg/vmlvm3  6G         | Hote
+---------------------------------+
| /dev/sda   6GB                  | disque VM
+------------+--------------------+
| /dev/sda1  |/dev/sda2           | partition
| primaire   |etendue    5.5G     |
| 512M       +--------------------+
|            |/dev/sda5           | 
|            |logique    5.5G     |
|            +--------------------+
|            | PV                 | LVM
|            +--------------------+
|            | VG  vgvmlvm3       | VG
|            +----------+---------+
|            | LV root  |LV swap_1|
+------------+----------+---------+
| fat        |ext4      | swap    | système de fichiers
+------------+----------+---------+
| /boot/efi  |/         | swap    |
`------------+----------+---------'
```

* Taille du volume logique `vmLvm3` de l'hote

```
╭─ ~     ✔  dom@domp14s  16:58:38 
╰─ sudo lvdisplay /dev/domp14svg/vmlvm3 
  --- Logical volume ---
  LV Path                /dev/domp14svg/vmlvm3
  LV Name                vmlvm3
  VG Name                domp14svg
  LV UUID                irCLbw-2TbZ-e9Qy-1cug-thEw-VLlW-jAbPS6
  LV Write Access        read/write
  LV Creation host, time domp14s, 2021-04-14 14:38:27 +0200
  LV Status              available
  # open                 0
  LV Size                6.00 GiB
  Current LE             1536
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:5
```

* Taille des volumes sur la VM


```
ubuntu@vmlvm3:~$ sudo vgdisplay -v
  --- Volume group ---
  VG Name               vgvmlvm3
  System ID             
  Format                lvm2
  Metadata Areas        1
  Metadata Sequence No  3
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                2
  Open LV               2
  Max PV                0
  Cur PV                1
  Act PV                1
  VG Size               <5.50 GiB
  PE Size               4.00 MiB
  Total PE              1407
  Alloc PE / Size       1406 / 5.49 GiB
  Free  PE / Size       1 / 4.00 MiB
  VG UUID               SW2SIc-JBfX-VK9x-pdUs-MkGP-WYGp-4ebk58
   
  --- Logical volume ---
  LV Path                /dev/vgvmlvm3/root
  LV Name                root
  VG Name                vgvmlvm3
  LV UUID                0BefEg-Mf21-anem-i5ld-6fcI-fXdR-3Zj01O
  LV Write Access        read/write
  LV Creation host, time vmlvm3, 2021-04-14 14:53:33 +0200
  LV Status              available
  # open                 1
  LV Size                <4.54 GiB
  Current LE             1162
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:0
   
  --- Logical volume ---
  LV Path                /dev/vgvmlvm3/swap_1
  LV Name                swap_1
  VG Name                vgvmlvm3
  LV UUID                ZUDu01-traD-GJwJ-XeRz-8nUS-JFL2-VZGdh7
  LV Write Access        read/write
  LV Creation host, time vmlvm3, 2021-04-14 14:53:33 +0200
  LV Status              available
  # open                 2
  LV Size                976.00 MiB
  Current LE             244
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:1
   
  --- Physical volumes ---
  PV Name               /dev/sda5     
  PV UUID               yGUrJM-5vdV-547j-PqVR-a2Yt-06L5-eMnoYw
  PV Status             allocatable
  Total PE / Free PE    1407 / 1

```

* volume physique sur la vm

```
ubuntu@vmlvm3:~$ sudo pvs
  PV         VG       Fmt  Attr PSize  PFree
  /dev/sda5  vgvmlvm3 lvm2 a--  <5.50g 4.00m
```  
* groupe de volume

```
ubuntu@vmlvm3:~$ sudo vgs
  VG       #PV #LV #SN Attr   VSize  VFree
  vgvmlvm3   1   2   0 wz--n- <5.50g 4.00m
```

* volume logique

```  
ubuntu@vmlvm3:~$ sudo lvs
  LV     VG       Attr       LSize   Pool Origin ...
  root   vgvmlvm3 -wi-ao----  <4.54g
  swap_1 vgvmlvm3 -wi-ao---- 976.00m
```

* utilisation de l'espace disque par le système d'exploitation  

```
ubuntu@vmlvm3:~$ df -h
Filesystem                 Size  Used Avail Use% Mounted on
udev                       448M     0  448M   0% /dev
tmpfs                       99M  652K   98M   1% /run
/dev/mapper/vgvmlvm3-root  4.5G  2.7G  1.6G  63% /
tmpfs                      491M     0  491M   0% /dev/shm
tmpfs                      5.0M     0  5.0M   0% /run/lock
tmpfs                      491M     0  491M   0% /sys/fs/cgroup
/dev/sda1                  511M  4.0K  511M   1% /boot/efi
tmpfs                       99M     0   99M   0% /run/user/1000
```

* utilisation de la swap

```
ubuntu@vmlvm3:~$ free -h
              total        used        free      shared  buff/cache   available
Mem:          981Mi        90Mi       658Mi       0.0Ki       232Mi       743Mi
Swap:         975Mi          0B       975Mi
```

* utilisation 

```
ubuntu@vmlvm3:~$ swapon -s
Filename				Type		Size	Used	Priority
/dev/dm-1                              	partition	999420	0	-2
```

## Sur l'hote - Agrandir le volume logique

```
.---------------------------------.-------------.
| LV - /dev/vg/vmlvm3  6G         | +2G         | Hote
+---------------------------------+-------------+
| /dev/sda   8GB                                | disque VM
+------------+--------------------+-------------+
| /dev/sda1  |/dev/sda2           |               partition
| primaire   |etendue    5.5G     |
| 512M       +--------------------+
|            |/dev/sda5           | 
|            |logique    5.5G     |
|            +--------------------+
|            | PV                 |               LVM
|            +--------------------+
|            | VG  vgvmlvm3       |               VG
|            +----------+---------+
|            | LV root  |LV swap_1|
+------------+----------+---------+
| fat        |ext4      | swap    |               système de fichiers
+------------+----------+---------+
| /boot/efi  |/         | swap    |
`------------+----------+---------'
```

* Arrêter la vm

```
hote:~$ virsh destroy vmLvm3
```

* Agrandir de 2G le volume logique

```
╭─ ~      3 ✘  dom@domp14s  17:13:10 
╰─ sudo lvresize -L +2G /dev/domp14svg/vmlvm3 
  Size of logical volume domp14svg/vmlvm3 changed from 6.00 GiB 
  (1536 extents) to 8.00 GiB (2048 extents).
  Logical volume domp14svg/vmlvm3 successfully resized.
```  

```
╭─ ~      ✔  dom@domp14s  17:13:18 
╰─ sudo lvdisplay /dev/domp14svg/vmlvm3 
  --- Logical volume ---
  LV Path                /dev/domp14svg/vmlvm3
  LV Name                vmlvm3
  VG Name                domp14svg
  LV UUID                irCLbw-2TbZ-e9Qy-1cug-thEw-VLlW-jAbPS6
  LV Write Access        read/write
  LV Creation host, time domp14s, 2021-04-14 14:38:27 +0200
  LV Status              available
  # open                 0
  LV Size                8.00 GiB
  Current LE             2048
  Segments               2
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:5

```


## Sur la vm - Agrandir les partitions

```
.---------------------------------.-------------.
| LV - /dev/vg/vmlvm3  6G         | +2G         | Hote
+---------------------------------+-------------+
| /dev/sda   8GB                                | disque VM
+------------+--------------------+-------------+
| /dev/sda1  |/dev/sda2           | /dev/sda3   |  partition
| primaire   |etendue    5.5G     | primaire 2G |
| 512M       +--------------------+             |
|            |/dev/sda5           |             |
|            |logique    5.5G     |             |
|            +--------------------+-------------+
|            | PV                 |               LVM
|            +--------------------+
|            | VG  vgvmlvm3       |               VG
|            +----------+---------+
|            | LV root  |LV swap_1|
+------------+----------+---------+
| fat        |ext4      | swap    |               système de fichiers
+------------+----------+---------+
| /boot/efi  |/         | swap    |
`------------+----------+---------'
```


### Afficher la nouvelle taille du disque (8G)

```
╭─ ~        ✔  dom@domp14s  17:14:14 
╰─ sudo fdisk /dev/domp14svg/vmlvm3 

Bienvenue dans fdisk (util-linux 2.34).
Les modifications resteront en mémoire jusqu'à écriture.
Soyez prudent avant d'utiliser la commande d'écriture.


Commande (m pour l'aide) : p

Disque /dev/domp14svg/vmlvm3 : 8 GiB, 8589934592 octets, 16777216 secteurs
Unités : secteur de 1 × 512 = 512 octets
Taille de secteur (logique / physique) : 512 octets / 512 octets
taille d'E/S (minimale / optimale) : 512 octets / 512 octets
Type d'étiquette de disque : dos
Identifiant de disque : 0x178ffc8f

Périphérique            Amorçage   Début      Fin Secteurs Taille Id Type
/dev/domp14svg/vmlvm3p1 *           2048  1050623  1048576   512M  b W95 FAT32
/dev/domp14svg/vmlvm3p2          1052670 12580863 11528194   5.5G  5 Étendue
/dev/domp14svg/vmlvm3p5          1052672 12580863 11528192   5.5G 8e LVM Linux


```

### Création d'une nouvelle partition et la partition logique LVM Linux sur la machine hôte


>Le modification seront appliqués à la fin des modifications par la commande `w`!


* Création d'une nouvelle partition

```
Commande (m pour l'aide) : n
Type de partition
   p   primaire (1 primaire, 1 étendue, 2 libre)
   l   logique (numéroté à partir de 5)
Sélectionnez (p par défaut) : p
Numéro de partition (3,4, 3 par défaut) : 3
Premier secteur (12580864-16777215, 12580864 par défaut) : 
Last sector, +/-sectors or +/-size{K,M,G,T,P} (12580864-16777215, 16777215 par défaut) : 

Une nouvelle partition 3 de type « Linux » et de taille 2 GiB a été créée.

Commande (m pour l'aide) : p
Disque /dev/domp14svg/vmlvm3 : 8 GiB, 8589934592 octets, 16777216 secteurs
Unités : secteur de 1 × 512 = 512 octets
Taille de secteur (logique / physique) : 512 octets / 512 octets
taille d'E/S (minimale / optimale) : 512 octets / 512 octets
Type d'étiquette de disque : dos
Identifiant de disque : 0x178ffc8f

Périphérique            Amorçage    Début      Fin Secteurs Taille Id Type
/dev/domp14svg/vmlvm3p1 *            2048  1050623  1048576   512M  b W95 FAT32
/dev/domp14svg/vmlvm3p2           1052670 12580863 11528194   5.5G  5 Étendue
/dev/domp14svg/vmlvm3p3          12580864 16777215  4196352     2G 83 Linux
/dev/domp14svg/vmlvm3p5           1052672 12580863 11528192   5.5G 8e LVM Linux

Les entrées de la table de partitions ne sont pas dans l'ordre du disque.

Commande (m pour l'aide) : 

```

* Appliquer les modifications

```
Commande (m pour l'aide) : w
La table de partitions a été altérée.
Failed to add partition 3 to system: Argument invalide

The kernel still uses the old partitions. The new table will be used at the next reboot. 
Synchronisation des disques.
```

## Sur la vm - Agrandir les volumes LVM

```
.---------------------------------.-------------.
| LV - /dev/vg/vmlvm3  6G           +2G         | Hote
+---------------------------------+-------------+
| /dev/sda   8GB                                | disque VM
+------------+--------------------+-------------+
| /dev/sda1  |/dev/sda2           | /dev/sda3   |  partition
| primaire   |etendue    5.5G     | primaire 2G |
| 512M       +--------------------+             |
|            |/dev/sda5           |             |
|            |logique    5.5G     |             |
|            +--------------------+-------------+
|            | PV                 | PV          |  LVM
|            +--------------------+-------------+
|            | VG  vgvmlvm3                     |  VG
|            +------------------------+---------+
|            | LV root                |LV swap_1|
+------------+------------------------+---------+
| fat        |ext4                    | swap    |  système de fichiers
+------------+------------------------+---------+
| /boot/efi  |/                       | swap    |
`------------+------------------------+---------'
```

### Création d'un nouveau volume physique

* Afficher la taille du PV avant la modification

  ```bash  
  ubuntu@vmlvm3:~$ sudo pvs
    PV         VG       Fmt  Attr PSize  PFree
    /dev/sda5  vgvmlvm3 lvm2 a--  <5.50g 4.00m
  ```

* Création d'un nouveau PV

  ```bash
  ubuntu@vmlvm3:~$ sudo pvcreate /dev/sda3
    Physical volume "/dev/sda3" successfully created.
  ```

* Afficher la taille du PV après la modification

  ```bash  
  ubuntu@vmlvm3:~$ sudo pvs
    PV         VG       Fmt  Attr PSize  PFree
    /dev/sda3           lvm2 ---   2.00g 2.00g
    /dev/sda5  vgvmlvm3 lvm2 a--  <5.50g 4.00m
  ```

### Agrandir le groupe de volume

* Étendre le groupe de volume

  ```bash
  ubuntu@vmlvm3:~$ sudo vgextend vgvmlvm3 /dev/sda3
    Volume group "vgvmlvm3" successfully extended
  ```

* Affichage du groupe de volume

  ```bash
  ubuntu@vmlvm3:~$ sudo vgdisplay -v
    --- Volume group ---
    VG Name               vgvmlvm3
    System ID             
    Format                lvm2
    Metadata Areas        2
    Metadata Sequence No  4
    VG Access             read/write
    VG Status             resizable
    MAX LV                0
    Cur LV                2
    Open LV               2
    Max PV                0
    Cur PV                2
    Act PV                2
    VG Size               <7.50 GiB
    PE Size               4.00 MiB
    Total PE              1919
    Alloc PE / Size       1406 / 5.49 GiB
    Free  PE / Size       513 / 2.00 GiB
    VG UUID               SW2SIc-JBfX-VK9x-pdUs-MkGP-WYGp-4ebk58
    
    --- Logical volume ---
    LV Path                /dev/vgvmlvm3/root
    LV Name                root
    VG Name                vgvmlvm3
    LV UUID                0BefEg-Mf21-anem-i5ld-6fcI-fXdR-3Zj01O
    LV Write Access        read/write
    LV Creation host, time vmlvm3, 2021-04-14 14:53:33 +0200
    LV Status              available
    # open                 1
    LV Size                <4.54 GiB
    Current LE             1162
    Segments               1
    Allocation             inherit
    Read ahead sectors     auto
    - currently set to     256
    Block device           253:0
    
    --- Logical volume ---
    LV Path                /dev/vgvmlvm3/swap_1
    LV Name                swap_1
    VG Name                vgvmlvm3
    LV UUID                ZUDu01-traD-GJwJ-XeRz-8nUS-JFL2-VZGdh7
    LV Write Access        read/write
    LV Creation host, time vmlvm3, 2021-04-14 14:53:33 +0200
    LV Status              available
    # open                 2
    LV Size                976.00 MiB
    Current LE             244
    Segments               1
    Allocation             inherit
    Read ahead sectors     auto
    - currently set to     256
    Block device           253:1
    
    --- Physical volumes ---
    PV Name               /dev/sda5     
    PV UUID               yGUrJM-5vdV-547j-PqVR-a2Yt-06L5-eMnoYw
    PV Status             allocatable
    Total PE / Free PE    1407 / 1
    
    PV Name               /dev/sda3     
    PV UUID               JOOZmV-vf4I-jgNe-BXCD-XfEl-IhFc-ceP5hn
    PV Status             allocatable
    Total PE / Free PE    512 / 512

  ```

### Agrandir le volume logique `root`

* Affiche la taille des LV avant la modification

  ```bash
  ubuntu@vmlvm3:~$ sudo lvs
    LV     VG       Attr       LSize   Pool Origin Data%  
    root   vgvmlvm3 -wi-ao----  <4.54g
    swap_1 vgvmlvm3 -wi-ao---- 976.00m 
  ```

* Agrandir de 2G le LV root

  ```bash
  ubuntu@vmlvm3:~$ sudo lvresize -L +2G /dev/vgvmlvm3/root
    Size of logical volume vgvmlvm3/root changed from 
    <4.54 GiB (1162 extents) to <6.54 GiB (1674 extents).
    Logical volume vgvmlvm3/root successfully resized.
  ```

* Afficher les nouvelles tailles des LV  

  ```bash
  ubuntu@vmlvm3:~$ sudo lvs
    LV     VG       Attr       LSize   Pool Origin 
    root   vgvmlvm3 -wi-ao----  <6.54g
    swap_1 vgvmlvm3 -wi-ao---- 976.00m
  ```  

  ```bash
  ubuntu@vmlvm3:~$ sudo vgdisplay -v
    --- Volume group ---
    VG Name               vgvmlvm3
    System ID             
    Format                lvm2
    Metadata Areas        2
    Metadata Sequence No  5
    VG Access             read/write
    VG Status             resizable
    MAX LV                0
    Cur LV                2
    Open LV               2
    Max PV                0
    Cur PV                2
    Act PV                2
    VG Size               <7.50 GiB
    PE Size               4.00 MiB
    Total PE              1919
    Alloc PE / Size       1918 / 7.49 GiB
    Free  PE / Size       1 / 4.00 MiB
    VG UUID               SW2SIc-JBfX-VK9x-pdUs-MkGP-WYGp-4ebk58
    
    --- Logical volume ---
    LV Path                /dev/vgvmlvm3/root
    LV Name                root
    VG Name                vgvmlvm3
    LV UUID                0BefEg-Mf21-anem-i5ld-6fcI-fXdR-3Zj01O
    LV Write Access        read/write
    LV Creation host, time vmlvm3, 2021-04-14 14:53:33 +0200
    LV Status              available
    # open                 1
    LV Size                <6.54 GiB
    Current LE             1674
    Segments               3
    Allocation             inherit
    Read ahead sectors     auto
    - currently set to     256
    Block device           253:0
    
    --- Logical volume ---
    LV Path                /dev/vgvmlvm3/swap_1
    LV Name                swap_1
    VG Name                vgvmlvm3
    LV UUID                ZUDu01-traD-GJwJ-XeRz-8nUS-JFL2-VZGdh7
    LV Write Access        read/write
    LV Creation host, time vmlvm3, 2021-04-14 14:53:33 +0200
    LV Status              available
    # open                 2
    LV Size                976.00 MiB
    Current LE             244
    Segments               1
    Allocation             inherit
    Read ahead sectors     auto
    - currently set to     256
    Block device           253:1
    
    --- Physical volumes ---
    PV Name               /dev/sda5     
    PV UUID               yGUrJM-5vdV-547j-PqVR-a2Yt-06L5-eMnoYw
    PV Status             allocatable
    Total PE / Free PE    1407 / 0
    
    PV Name               /dev/sda3     
    PV UUID               JOOZmV-vf4I-jgNe-BXCD-XfEl-IhFc-ceP5hn
    PV Status             allocatable
    Total PE / Free PE    512 / 1
  ```


## Sur la vm - Agrandir la partition EXT

* Redimensionner la taille du système de fichier EXT

  ```bash
  ubuntu@vmlvm3:~$ sudo resize2fs /dev/vgvmlvm3/root
  resize2fs 1.45.5 (07-Jan-2020)
  Filesystem at /dev/vgvmlvm3/root is mounted on /; on-line resizing required
  old_desc_blocks = 1, new_desc_blocks = 1
  The filesystem on /dev/vgvmlvm3/root is now 1714176 (4k) blocks long.
  ```

* Afficher les nouvelles dimensions

  ```
  ubuntu@vmlvm3:~$ df -h
  Filesystem                 Size  Used Avail Use% Mounted on
  udev                       448M     0  448M   0% /dev
  tmpfs                       99M  664K   98M   1% /run
  /dev/mapper/vgvmlvm3-root  6.4G  2.7G  3.5G  44% /
  tmpfs                      491M     0  491M   0% /dev/shm
  tmpfs                      5.0M     0  5.0M   0% /run/lock
  tmpfs                      491M     0  491M   0% /sys/fs/cgroup
  /dev/sda1                  511M  4.0K  511M   1% /boot/efi
  tmpfs                       99M     0   99M   0% /run/user/1000
  ```


>La taille de la partition `/dev/mapper/vgvmlvm3-root` est maintenant 2G plus grande :-)



## Références

1.  Increasing a KVM Virtual Machine Disk when using LVM and ext4 | Steven Gordon, [http://sandilands.info/sgordon/increasing-kvm-virtual-machine-disk-using-lvm-ext4][1]

[1]:http://sandilands.info/sgordon/increasing-kvm-virtual-machine-disk-using-lvm-ext4

