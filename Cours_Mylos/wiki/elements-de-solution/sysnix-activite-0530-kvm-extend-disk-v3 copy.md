[[_TOC_]]


# SYSNIX - Virtualisation, extension de la taille d'un volume logique contenant une machine virtuelle (v2)

>Étendre la taille de stockage d'un VM

## Prérequis

Mettre en place une machine virtuelle `vm3` stocké dans un volume logique `/dev/ubuntu-usb-vg/vm3`.


### Information sur l'espace de stockage

État du disque après un partitionnement assisté sur le disque complet d'une installation de Debian 12 (boookworm)

```
.---------------------------------.
| LV - /dev/vg/vm3  6G            | Hote
+---------------------------------+
| /dev/vda   6GB                  | disque VM
+-------------------+-------------+
| /dev/vda1         |/dev/vda2    | partition
| primaire          |etendue 975M |
| 5G                +-------------+
|                   |/dev/vda5    | 
|                   |logique 975M |
+-------------------+-------------+
|  /                | swap        | système de fichiers
|  ext4             |             |
`---------------------------------'
```

* Taille du volume logique `/dev/ubuntu-usb-vg/vm3` de l'hote

  ```bash
  huguenindo@ubuntu-usb-dhu:tmp$ sudo lvdisplay /dev/ubuntu-usb-vg/vm3
  [sudo] Mot de passe de huguenindo : 
    --- Logical volume ---
    LV Path                /dev/ubuntu-usb-vg/vm3
    LV Name                vm3
    VG Name                ubuntu-usb-vg
    LV UUID                HOVwEL-MBtt-N2k3-h7fp-zzxH-hhQ2-P2IkkQ
    LV Write Access        read/write
    LV Creation host, time ubuntu-usb-dhu, 2023-11-24 09:35:31 +0100
    LV Status              available
    # open                 1
    LV Size                6.00 GiB
    Current LE             1536
    Segments               1
    Allocation             inherit
    Read ahead sectors     auto
    - currently set to     131064
    Block device           253:5
  ```

* utilisation de l'espace disque par le système d'exploitation  

  ```bash
  debian@vm3:~$ df -h
  Sys. de fichiers Taille Utilisé Dispo Uti% Monté sur
  udev               459M       0  459M   0% /dev
  tmpfs               97M    596K   96M   1% /run
  /dev/vda1          4.9G    1.4G  3.4G  29% /
  tmpfs              481M       0  481M   0% /dev/shm
  tmpfs              5.0M       0  5.0M   0% /run/lock
  tmpfs               97M       0   97M   0% /run/user/1000
  ```

* Liste des disques et partitions

  ```bash
  debian@vm3:~$ sudo fdisk -l
  Disque /dev/vda : 6 GiB, 6442450944 octets, 12582912 secteurs
  Unités : secteur de 1 × 512 = 512 octets
  Taille de secteur (logique / physique) : 512 octets / 512 octets
  taille d'E/S (minimale / optimale) : 512 octets / 512 octets
  Type d'étiquette de disque : dos
  Identifiant de disque : 0x02bd8444

  Périphérique Amorçage    Début      Fin Secteurs Taille Id Type
  /dev/vda1    *            2048 10582015 10579968     5G 83 Linux
  /dev/vda2             10584062 12580863  1996802   975M  5 Étendue
  /dev/vda5             10584064 12580863  1996800   975M 82 partition d'échange Linux / Solaris
  ```


* Emplacement de la swap

  ```bash
  debian@vm3:~$ sudo swapon -s
  Nom fichier       Type      Taille    Utilisé   Priorité
  /dev/vda5         partition	998396		0	        -2

  ```

* Utilisation de la mémoire

  ```bash
  debian@vm3:~$ free -h
                total       utilisé      libre     partagé tamp/cache   disponible
  Mem:           960Mi       221Mi       764Mi       3.6Mi        91Mi       739Mi
  Échange:       974Mi          0B       974Mi
  ```

##  Sur l'hôte - Agrandir le volume logique

* Arrêter la VM

  ```bash
  huguenindo@ubuntu-usb-dhu:tmp$ virsh destroy vm3
  Domain vm3 destroyed
  ```

```
.----------------------------------------------.
| LV - /dev/vg/vm3  8G                         | Hote
+----------------------------------------------+
| /dev/sda   8GB                               | disque VM
+-------------------+--------------------------+
| /dev/vda1         |/dev/vda2    | partition
| primaire          |etendue 975M |
| 5G                +-------------+
|                   |/dev/vda5    | 
|                   |logique 975M |
+-------------------+-------------+
|  /                | swap        | système de fichiers
|  ext4             |             |
`---------------------------------'
```

* Agrandir de 2G le volume logique

    ```bash
    huguenindo@ubuntu-usb-dhu:tmp$ sudo lvresize -L +2G /dev/ubuntu-usb-vg/vm3
    [sudo] Mot de passe de huguenindo : 
      Size of logical volume ubuntu-usb-vg/vm3 changed from 6.00 GiB (1536 extents) to 8.00 GiB (2048 extents).
      Logical volume ubuntu-usb-vg/vm3 successfully resized.

    huguenindo@ubuntu-usb-dhu:tmp$ sudo lvdisplay /dev/ubuntu-usb-vg/vm3
      --- Logical volume ---
      LV Path                /dev/ubuntu-usb-vg/vm3
      LV Name                vm3
      VG Name                ubuntu-usb-vg
      LV UUID                HOVwEL-MBtt-N2k3-h7fp-zzxH-hhQ2-P2IkkQ
      LV Write Access        read/write
      LV Creation host, time ubuntu-usb-dhu, 2023-11-24 09:35:31 +0100
      LV Status              available
      # open                 0
      LV Size                8.00 GiB
      Current LE             2048
      Segments               2
      Allocation             inherit
      Read ahead sectors     auto
      - currently set to     131064
      Block device           253:5
    ```


## Sur l'hôte - Redimensionner les partitions du disque virtuel `/dev/ubuntu-usb-vg/vm3` 

Sur le volume logique `/dev/vg/vm3` redimensionner la partition système `/dev/vda1` pour obtenir le configuration suivante. Pour cela, il faut supprimer les partitions et les recréer!


```
.----------------------------------------------.
| LV - /dev/vg/vm3  8G                         | Hote
+----------------------------------------------+
| /dev/sda   8GB                               | disque VM
+-------------------+--------------------------+
| /dev/vda1                      |/dev/vda2    | partition
| primaire                       |etendue 975M |
| 7G                             +-------------+
|                                |/dev/vda5    | 
|                                |logique 975M |
+--------------------------------+-------------+
|  /                | swap       | système de fichiers
|  ext4             |            |
`--------------------------------'
```


### Avec  l'outil `fdisk`

* Afficher l'état du disque

  ```bash
  huguenindo@ubuntu-usb-dhu:tmp$ sudo fdisk /dev/ubuntu-usb-vg/vm3

  Bienvenue dans fdisk (util-linux 2.37.2).
  Les modifications resteront en mémoire jusqu'à écriture.
  Soyez prudent avant d'utiliser la commande d'écriture.

  Commande (m pour l'aide) : p
  Disque /dev/ubuntu-usb-vg/vm3 : 8 GiB, 8589934592 octets, 16777216 secteurs
  Unités : secteur de 1 × 512 = 512 octets
  Taille de secteur (logique / physique) : 512 octets / 512 octets
  taille d'E/S (minimale / optimale) : 512 octets / 33553920 octets
  Type d'étiquette de disque : dos
  Identifiant de disque : 0x02bd8444

  Périphérique             Amorçage    Début      Fin Secteurs Taille Id Type
  /dev/ubuntu-usb-vg/vm3p1 *            2048 10582015 10579968     5G 83 Linux
  /dev/ubuntu-usb-vg/vm3p2          10584062 12580863  1996802   975M  5 Étendue
  /dev/ubuntu-usb-vg/vm3p5          10584064 12580863  1996800   975M 82 partition d'échange Linux / Solaris

  Commande (m pour l'aide) : m

  Aide :

    DOS (secteur d'amorçage)
    a   modifier un indicateur d'amorçage
    b   éditer l'étiquette BSD imbriquée du disque
    c   modifier l'indicateur de compatibilité DOS

    Générique
    d   supprimer la partition
    F   afficher l’espace libre non partitionné
    l   afficher les types de partitions connues
    n   ajouter une nouvelle partition
    p   afficher la table de partitions
    t   modifier le type d'une partition
    v   vérifier la table de partitions
    i   Afficher des renseignements sur la partition

    Autre
    m   afficher ce menu
    u   modifier les unités d'affichage et de saisie
    x   fonctions avancées (réservées aux spécialistes)

    Script
    I   chargement de l’agencement à partir du fichier de script sfdisk
    O   sauvegarde de l’agencement vers le fichier de script sfdisk

    Sauvegarder et quitter
    w   écrire la table sur le disque et quitter
    q   quitter sans enregistrer les modifications

    Créer une nouvelle étiquette
    g   créer une nouvelle table vide de partitions GPT
    G   créer une nouvelle table vide de partitions SGI (IRIX)
    o   créer une nouvelle table vide de partitions DOS
    s   créer une nouvelle table vide de partitions Sun


  Commande (m pour l'aide) : 
  ```


* Supprimer la partition logique 5, étendue 2, primaire 1

  ```bash
  Commande (m pour l'aide) : d
  Numéro de partition (1,2,5, 5 par défaut) : 5

  La partition 5 a été supprimée.

  Commande (m pour l'aide) : d2
  Numéro de partition (1,2, 2 par défaut) : 2

  La partition 2 a été supprimée.

  Commande (m pour l'aide) : d
  Partition 1 sélectionnée
  La partition 1 a été supprimée.
  ```


* Recréer les partitions primaire 1,  étendue 2 et logique 5

  ```bash
  Commande (m pour l'aide) : n
  Type de partition
    p   primaire (0 primary, 0 extended, 4 free)
    e   étendue (conteneur pour partitions logiques)
  Sélectionnez (p par défaut) : p
  Numéro de partition (1-4, 1 par défaut) : 
  Premier secteur (2048-16777215, 2048 par défaut) : 
  Last sector, +/-sectors or +/-size{K,M,G,T,P} (2048-16777215, 16777215 par défaut) : +7G

  Une nouvelle partition 1 de type « Linux » et de taille 7 GiB a été créée.
  La partition #1 contient une signature ext4.

  Voulez-vous supprimer la signature ? [O]ui/[N]on : n

  Commande (m pour l'aide) : p

  Disque /dev/ubuntu-usb-vg/vm3 : 8 GiB, 8589934592 octets, 16777216 secteurs
  Unités : secteur de 1 × 512 = 512 octets
  Taille de secteur (logique / physique) : 512 octets / 512 octets
  taille d'E/S (minimale / optimale) : 512 octets / 33553920 octets
  Type d'étiquette de disque : dos
  Identifiant de disque : 0x02bd8444

  Périphérique             Amorçage Début      Fin Secteurs Taille Id Type
  /dev/ubuntu-usb-vg/vm3p1           2048 14682111 14680064     7G 83 Linux

  Commande (m pour l'aide) : n
  Type de partition
    p   primaire (1 primary, 0 extended, 3 free)
    e   étendue (conteneur pour partitions logiques)
  Sélectionnez (p par défaut) : e
  Numéro de partition (2-4, 2 par défaut) : 
  Premier secteur (14682112-16777215, 14682112 par défaut) : 
  Last sector, +/-sectors or +/-size{K,M,G,T,P} (14682112-16777215, 16777215 par défaut) : 

  Une nouvelle partition 2 de type « Extended » et de taille 1023 MiB a été créée.

  Commande (m pour l'aide) : n
  Tout l’espace des partitions primaires est utilisé.
  Ajout de la partition logique 5
  Premier secteur (14684160-16777215, 14684160 par défaut) : 
  Last sector, +/-sectors or +/-size{K,M,G,T,P} (14684160-16777215, 16777215 par défaut) : 

  Une nouvelle partition 5 de type « Linux » et de taille 1022 MiB a été créée.
  ```

* Afficher l'état du disque

  ```bash
  Commande (m pour l'aide) : p
  Disque /dev/ubuntu-usb-vg/vm3 : 8 GiB, 8589934592 octets, 16777216 secteurs
  Unités : secteur de 1 × 512 = 512 octets
  Taille de secteur (logique / physique) : 512 octets / 512 octets
  taille d'E/S (minimale / optimale) : 512 octets / 33553920 octets
  Type d'étiquette de disque : dos
  Identifiant de disque : 0x02bd8444

  Périphérique             Amorçage    Début      Fin Secteurs Taille Id Type
  /dev/ubuntu-usb-vg/vm3p1              2048 14682111 14680064     7G 83 Linux
  /dev/ubuntu-usb-vg/vm3p2          14682112 16777215  2095104  1023M  5 Étendue
  /dev/ubuntu-usb-vg/vm3p5          14684160 16777215  2093056  1022M 83 Linux
  ```

* changer le type de la partition 5

    ```bash
    Commande (m pour l'aide) : t
    Numéro de partition (1,2,5, 5 par défaut) : 5
    Hex code or alias (type L to list all): L

    00 Vide             24 NEC DOS          81 Minix / Linux a  bf Solaris        
    01 FAT12            27 TFS WinRE masqu  82 partition d'éch  c1 DRDOS/sec (FAT-
    02 root XENIX       39 Plan 9           83 Linux            c4 DRDOS/sec (FAT-
    03 usr XENIX        3c récupération Pa  84 OS/2 hidden or   c6 DRDOS/sec (FAT-
    04 FAT16 <32M       40 Venix 80286      85 Linux étendue    c7 Syrinx         
    05 Étendue          41 PPC PReP Boot    86 NTFS volume set  da Non-FS data    
    06 FAT16            42 SFS              87 NTFS volume set  db CP/M / CTOS / .
    07 HPFS/NTFS/exFAT  4d QNX4.x           88 Linux plaintext  de Dell Utility   
    08 AIX              4e 2e partie QNX4.  8e LVM Linux        df BootIt         
    09 Amorçable AIX    4f 3e partie QNX4.  93 Amoeba           e1 DOS access     
    0a Gestionnaire d'  50 OnTrack DM       94 Amoeba BBT       e3 DOS R/O        
    0b W95 FAT32        51 OnTrack DM6 Aux  9f BSD/OS           e4 SpeedStor      
    0c W95 FAT32 (LBA)  52 CP/M             a0 IBM Thinkpad hi  ea Amorçage Linux 
    0e W95 FAT16 (LBA)  53 OnTrack DM6 Aux  a5 FreeBSD          eb BeOS fs        
    0f Étendue W95 (LB  54 OnTrackDM6       a6 OpenBSD          ee GPT            
    10 OPUS             55 EZ-Drive         a7 NeXTSTEP         ef EFI (FAT-12/16/
    11 FAT12 masquée    56 Golden Bow       a8 UFS Darwin       f0 Linux/PA-RISC b
    12 Compaq diagnost  5c Priam Edisk      a9 NetBSD           f1 SpeedStor      
    14 FAT16 masquée <  61 SpeedStor        ab Amorçage Darwin  f4 SpeedStor      
    16 FAT16 masquée    63 GNU HURD ou Sys  af HFS / HFS+       f2 DOS secondaire 
    17 HPFS/NTFS masqu  64 Novell Netware   b7 BSDI fs          fb VMware VMFS    
    18 AST SmartSleep   65 Novell Netware   b8 partition d'éch  fc VMware VMKCORE 
    1b W95 FAT32 masqu  70 DiskSecure Mult  bb Boot Wizard mas  fd RAID Linux auto
    1c W95 FAT32 masqu  75 PC/IX            bc Acronis FAT32 L  fe LANstep        
    1e W95 FAT16 masqu  80 Minix ancienne   be Amorçage Solari  ff BBT            

    Aliases:
      linux          - 83
      swap           - 82
      extended       - 05
      uefi           - EF
      raid           - FD
      lvm            - 8E
      linuxex        - 85
    Hex code or alias (type L to list all): 82

    Type de partition « Linux » modifié en « Linux swap / Solaris ».

    Commande (m pour l'aide) : p
    Disque /dev/ubuntu-usb-vg/vm3 : 8 GiB, 8589934592 octets, 16777216 secteurs
    Unités : secteur de 1 × 512 = 512 octets
    Taille de secteur (logique / physique) : 512 octets / 512 octets
    taille d'E/S (minimale / optimale) : 512 octets / 33553920 octets
    Type d'étiquette de disque : dos
    Identifiant de disque : 0x02bd8444

    Périphérique             Amorçage    Début      Fin Secteurs Taille Id Type
    /dev/ubuntu-usb-vg/vm3p1              2048 14682111 14680064     7G 83 Linux
    /dev/ubuntu-usb-vg/vm3p2          14682112 16777215  2095104  1023M  5 Étendue
    /dev/ubuntu-usb-vg/vm3p5          14684160 16777215  2093056  1022M 82 partition d'échange Linux / Solaris
    ```

* Valider les modifications

  ```bash
  Commande (m pour l'aide) : w
  La table de partitions a été altérée.
  Appel d'ioctl() pour relire la table de partitions.
  Échec de relecture de la table de partitions.: Argument invalide

  The kernel still uses the old table. The new table will be used at the next reboot or after you run partprobe(8) or partx(8).
  ```


## Sur la vm - Redimensionner la taille du système de fichiers EXT

```
.----------------------------------------------.
| LV - /dev/vg/vm3  8G                         | Hote
+----------------------------------------------+
| /dev/sda   8GB                               | disque VM
+-------------------+--------------------------+
| /dev/vda1                      |/dev/vda2    | partition
| primaire                       |etendue 975M |
| 7G                             +-------------+
|                                |/dev/vda5    | 
|                                |logique 975M |
+--------------------------------+-------------+
|  /                             | swap        | système de fichiers
|  ext4                          |             |
`----------------------------------------------'
```

* Redémarrer la vm. Cette opération peut prendre du temps à cause 


```bash
debian@vm3:~$ df -h
Sys. de fichiers Taille Utilisé Dispo Uti% Monté sur
udev               459M       0  459M   0% /dev
tmpfs               97M    604K   96M   1% /run
/dev/vda1          4.9G    1.4G  3.3G  29% /
tmpfs              481M       0  481M   0% /dev/shm
tmpfs              5.0M       0  5.0M   0% /run/lock
tmpfs               97M       0   97M   0% /run/user/1000


debian@vm3:~$ sudo fdisk -l
[sudo] Mot de passe de debian : 
Disque /dev/vda : 8 GiB, 8589934592 octets, 16777216 secteurs
Unités : secteur de 1 × 512 = 512 octets
Taille de secteur (logique / physique) : 512 octets / 512 octets
taille d'E/S (minimale / optimale) : 512 octets / 512 octets
Type d'étiquette de disque : dos
Identifiant de disque : 0x02bd8444

Périphérique Amorçage    Début      Fin Secteurs Taille Id Type
/dev/vda1                 2048 14682111 14680064     7G 83 Linux
/dev/vda2             14682112 16777215  2095104  1023M  5 Étendue
/dev/vda5             14684160 16777215  2093056  1022M 82 partition d'échange Linux / Solaris
```

* Redimensionner la taille du système de fichier EXT 

```bash
debian@vm3:~$ sudo resize2fs /dev/vda1
resize2fs 1.47.0 (5-Feb-2023)
Filesystem at /dev/vda1 is mounted on /; on-line resizing required
old_desc_blocks = 1, new_desc_blocks = 1
The filesystem on /dev/vda1 is now 1835008 (4k) blocks long.
```


```bash
debian@vm3:~$ df -h
Sys. de fichiers Taille Utilisé Dispo Uti% Monté sur
udev               459M       0  459M   0% /dev
tmpfs               97M    608K   96M   1% /run
/dev/vda1          6.9G    1.4G  5.2G  21% /
tmpfs              481M       0  481M   0% /dev/shm
tmpfs              5.0M       0  5.0M   0% /run/lock
tmpfs               97M       0   97M   0% /run/user/1000
```


>La taille de la partition `/dev/vda1` est maintenant 2G plus grande :-)

## Sur la vm - recréer la partition d'échange swap

* recréer la partition swap

  ```bash
  debian@vm3:~$ sudo mkswap /dev/vda5
  Configure l'espace d'échange (swap) en version 1, taille = 1022 MiB (1071640576 octets)
  pas d'étiquette, UUID=fd635b56-390a-48a2-b536-5fd9d06dc4f8
  ```
  ```bash
  debian@vm3:~$ sudo swapon /dev/vda5
  ```
  ```bash
  debian@vm3:~$ sudo swapon -s
  Nom fichier				Type		Taille		Utilisé		Priorité
  /dev/vda5                               partition	1046524		0		-2
  ```

* mettre à jour le fichier de montage avec le nouveau UUID de la partition swap

  ```bash
  debian@vm3:~$ cat /etc/fstab 
  # /etc/fstab: static file system information.
  #
  # Use 'blkid' to print the universally unique identifier for a
  # device; this may be used with UUID= as a more robust way to name devices
  # that works even if disks are added and removed. See fstab(5).
  #
  # systemd generates mount units based on this file, see systemd.mount(5).
  # Please run 'systemctl daemon-reload' after making changes here.
  #
  # <file system> <mount point>   <type>  <options>       <dump>  <pass>
  # / was on /dev/vda1 during installation
  UUID=dacd9c4b-6dda-4d8b-98b7-b44572a383c7 /               ext4    errors=remount-ro 0       1
  # swap was on /dev/vda5 during installation
  UUID=fd635b56-390a-48a2-b536-5fd9d06dc4f8 none            swap    sw              0       0
  /dev/sr0        /media/cdrom0   udf,iso9660 user,noauto     0       0
  ```