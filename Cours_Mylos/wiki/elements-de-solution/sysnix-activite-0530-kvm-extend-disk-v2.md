[[_TOC_]]


# SYSNIX - Virtualisation, extension de la taille d'un volume logique contenant une machine virtuelle (v2)

>Étendre la taille de stockage d'un VM

## Prérequis

Mettre en place une machine virtuelle `vm3` stocké dans un volume logique `/dev/domp14svg/vm3`.


### Information sur l'espace de stockage


>Pour ubuntu 20.04, le partitionnement assisté crée le partitionnement ci-dessous. La swap  (fichier d'échange) est stocké dans le fichier `/swapfile`

```
.---------------------------------.
| LV - /dev/domp14svg/vm3  6G     | Hote
+---------------------------------+
| /dev/sda   6GB                  | disque VM
+------------+--------------------+
| /dev/sda1  |/dev/sda2           | partition
| primaire   |etendue    5.5G     |
| 512M       +--------------------+
|            |/dev/sda5           | 
|            |logique    5.5G     |
+------------+--------------------+
|  /boot/efi  | /                 |
|  FAT        | etx4              |
`---------------------------------'
```

* Taille du volume logique `/dev/domp14svg/vm3` de l'hote

  ```bash
  ╭─ ~      ✔  dom@domp14s  10:28:51 
  ╰─ sudo lvdisplay /dev/domp14svg/vm3
  [sudo] Mot de passe de dom : 
  --- Logical volume ---
  LV Path                /dev/domp14svg/vm3
  LV Name                vm3
  VG Name                domp14svg
  LV UUID                Dpgf5I-0GAQ-Gun3-xB9i-TFdl-yP0x-gFv7iC
  LV Write Access        read/write
  LV Creation host, time domp14s, 2021-04-14 14:35:45 +0200
  LV Status              available
  # open                 0
  LV Size                6.00 GiB
  Current LE             1536
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:4
  ```

* utilisation de l'espace disque par le système d'exploitation  

  ```bash
  ubuntu@vm3:~$ df -h
  Filesystem      Size  Used Avail Use% Mounted on
  udev            448M     0  448M   0% /dev
  tmpfs            99M  640K   98M   1% /run
  /dev/sda5       5.4G  2.4G  2.8G  47% /
  tmpfs           491M     0  491M   0% /dev/shm
  tmpfs           5.0M     0  5.0M   0% /run/lock
  tmpfs           491M     0  491M   0% /sys/fs/cgroup
  /dev/sda1       511M  4.0K  511M   1% /boot/efi
  tmpfs            99M     0   99M   0% /run/user/1000
  ```

* Liste des disques et partitions

  ```bash
  ubuntu@vm3:~$ sudo fdisk -l
  [sudo] password for ubuntu: 
  Disk /dev/sda: 6 GiB, 6442450944 bytes, 12582912 sectors
  Disk model: QEMU HARDDISK   
  Units: sectors of 1 * 512 = 512 bytes
  Sector size (logical/physical): 512 bytes / 512 bytes
  I/O size (minimum/optimal): 512 bytes / 512 bytes$
  Disklabel type: dos
  Disk identifier: 0x89ab78e4

  Device     Boot   Start      End  Sectors  Size Id Type
  /dev/sda1  *       2048  1050623  1048576  512M  b W95 FAT32
  /dev/sda2       1052670 12580863 11528194  5.5G  5 Extended
  /dev/sda5       1052672 12580863 11528192  5.5G 83 Linux
  ```


* Emplacement de la swap

  ```bash
  ubuntu@vm3:~$ swapon -s
    Filename				Type		Size	Used	Priority
    /swapfile                           	file    	190916	0	-2
  ```

* Utilisation de la mémoire

  ```bash
  ubuntu@vm3:~$ free -h
              total        used        free      shared  buff/cache   available
  Mem:          981Mi        89Mi       718Mi       0.0Ki       173Mi       747Mi
  Swap:         257Mi          0B       257Mi
  ```



##  Sur l'hôte - Agrandir le volume logique

```
.----------------------------------------------.
| LV - /dev/domp14svg/vm3  8G                  | Hote
+----------------------------------------------+
| /dev/sda   8GB                               | disque VM
+------------+---------------------------------+
| /dev/sda1  |/dev/sda2           | partition
| primaire   |etendue    5.5G     |
| 512M       +--------------------+
|            |/dev/sda5           | 
|            |logique    5.5G     |
+------------+--------------------+
|  /boot/efi  | /                  |
`---------------------------------'
```

* Agrandir de 2G le volume logique

    ```bash
    ╭─ ~      ✔  dom@domp14s  10:32:25 
    ╰─ sudo lvresize -L +2G /dev/domp14svg/vm3
    Size of logical volume domp14svg/vm3 changed from 6.00 GiB (1536 extents) to 8.00 GiB (2048 extents).
    Logical volume domp14svg/vm3 successfully resized.


    ╭─ ~      ✔  dom@domp14s  10:33:03 
    ╰─ sudo lvdisplay /dev/domp14svg/vm3
    --- Logical volume ---
    LV Path                /dev/domp14svg/vm3
    LV Name                vm3
    VG Name                domp14svg
    LV UUID                Dpgf5I-0GAQ-Gun3-xB9i-TFdl-yP0x-gFv7iC
    LV Write Access        read/write
    LV Creation host, time domp14s, 2021-04-14 14:35:45 +0200
    LV Status              available
    # open                 0
    LV Size                8.00 GiB
    Current LE             2048
    Segments               2
    Allocation             inherit
    Read ahead sectors     auto
    - currently set to     256
    Block device           253:4
    
    ```


## Sur l'hôte - Redimensionner les partitions du disque virtuel `/dev/domp14svg/vm3` 

Sur le volume logique `/dev/domp14svg/vm3` redimensionner la partition système `/dev/sda2` et `/dev/sda5` pour obtenir le configuration suivante:


```
.----------------------------------------------.
| LV - /dev/domp14svg/vm3  8G                  | Hote
+----------------------------------------------+
| /dev/sda   8GB                               | disque VM
+------------+---------------------------------+
| /dev/sda1  |/dev/sda2                        | partition
| primaire   |etendue    7.5G                  |
| 512M       +---------------------------------+
|            |/dev/sda5                        | 
|            |logique    7.5G                  |
+------------+---------------------------------+
|  /boot/efi  | /                  |
`---------------------------------'
```

* Arrêter la VM

  ```bash
  ╭─ ~      ✔  dom@domp14s  10:32:18 
  ╰─ virsh destroy vm3
  Domain vm3 destroyed
  ```

### Avec  l'outil `fdisk`

* Afficher l'état du disque

  ```bash
  ╭─ ~      ✔  dom@domp14s  10:33:29 
  ╰─ sudo fdisk /dev/domp14svg/vm3

  Bienvenue dans fdisk (util-linux 2.34).
  Les modifications resteront en mémoire jusqu'à écriture.
  Soyez prudent avant d'utiliser la commande d'écriture.


  Commande (m pour l'aide) : p
  Disque /dev/domp14svg/vm3 : 8 GiB, 8589934592 octets, 16777216 secteurs
  Unités : secteur de 1 × 512 = 512 octets
  Taille de secteur (logique / physique) : 512 octets / 512 octets
  taille d'E/S (minimale / optimale) : 512 octets / 512 octets
  Type d'étiquette de disque : dos
  Identifiant de disque : 0x89ab78e4

  Périphérique         Amorçage   Début      Fin Secteurs Taille Id Type
  /dev/domp14svg/vm3p1 *           2048  1050623  1048576   512M  b W95 FAT32
  /dev/domp14svg/vm3p2          1052670 12580863 11528194   5.5G  5 Étendue
  /dev/domp14svg/vm3p5          1052672 12580863 11528192   5.5G 83 Linux

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
  ```


* Supprimer la partition logique 5 et étendue 2

  ```bash
  Commande (m pour l'aide) : d
  Numéro de partition (1,2,5, 5 par défaut) : 5

  La partition 5 a été supprimée.

  Commande (m pour l'aide) : d
  Numéro de partition (1,2, 2 par défaut) : 2
  ```

* Recréer la partition étendue 2 et logique 4

  ```bash

  La partition 2 a été supprimée.

  Commande (m pour l'aide) : n
  Type de partition
  p   primaire (1 primaire, 0 étendue, 3 libre)
  e   étendue (conteneur pour partitions logiques)
  Sélectionnez (p par défaut) : e
  Numéro de partition (2-4, 2 par défaut) : 2
  Premier secteur (1050624-16777215, 1050624 par défaut) : 
  Last sector, +/-sectors or +/-size{K,M,G,T,P} (1050624-16777215, 16777215 par défaut) : 

  Une nouvelle partition 2 de type « Extended » et de taille 7.5 GiB a été créée.

  Commande (m pour l'aide) : n
  Tout l’espace des partitions primaires est utilisé.
  Ajout de la partition logique 5
  Premier secteur (1052672-16777215, 1052672 par défaut) : 
  Last sector, +/-sectors or +/-size{K,M,G,T,P} (1052672-16777215, 16777215 par défaut) : 

  Une nouvelle partition 5 de type « Linux » et de taille 7.5 GiB a été créée.
  La partition #5 contient une signature ext4.

  Voulez-vous supprimer la signature ? [O]ui/[N]on : n
  ```

* Afficher l'état du disque

  ```bash
  Commande (m pour l'aide) : p

  Disque /dev/domp14svg/vm3 : 8 GiB, 8589934592 octets, 16777216 secteurs
  Unités : secteur de 1 × 512 = 512 octets
  Taille de secteur (logique / physique) : 512 octets / 512 octets
  taille d'E/S (minimale / optimale) : 512 octets / 512 octets
  Type d'étiquette de disque : dos
  Identifiant de disque : 0x89ab78e4

  Périphérique         Amorçage   Début      Fin Secteurs Taille Id Type
  /dev/domp14svg/vm3p1 *           2048  1050623  1048576   512M  b W95 FAT32
  /dev/domp14svg/vm3p2          1050624 16777215 15726592   7.5G  5 Étendue
  /dev/domp14svg/vm3p5          1052672 16777215 15724544   7.5G 83 Linux
  ```

* Valider les modifications

  ```bash
  Commande (m pour l'aide) : w
  La table de partitions a été altérée.
  Failed to remove partition 2 from system: Aucun périphérique ou adresse
  Failed to update system information about partition 5: Aucun périphérique ou adresse
  Failed to add partition 2 to system: Argument invalide

  The kernel still uses the old partitions. The new table will be used at the next reboot. 
  Synchronisation des disques.
  ```


## Sur la vm - Redimensionner la taille du système de fichiers EXT

```
.----------------------------------------------.
| LV - /dev/domp14svg/vm3  8G                  | Hote
+----------------------------------------------+
| /dev/sda   8GB                               | disque VM
+------------+---------------------------------+
| /dev/sda1  |/dev/sda2                        | partition
| primaire   |etendue    7.5G                  |
| 512M       +---------------------------------+
|            |/dev/sda5                        | 
|            |logique    7.5G                  |
+------------+---------------------------------+
|  /boot/efi  | /                              |
`----------------------------------------------'
```


```bash
ubuntu@vm3:~$ df -h
Filesystem      Size  Used Avail Use% Mounted on
udev            448M     0  448M   0% /dev
tmpfs            99M  644K   98M   1% /run
/dev/sda5       5.4G  2.4G  2.7G  47% /
tmpfs           491M     0  491M   0% /dev/shm
tmpfs           5.0M     0  5.0M   0% /run/lock
tmpfs           491M     0  491M   0% /sys/fs/cgroup
/dev/sda1       511M  4.0K  511M   1% /boot/efi
tmpfs            99M     0   99M   0% /run/user/1000

ubuntu@vm3:~$ sudo fdisk -l
[sudo] password for ubuntu: 
Disk /dev/sda: 8 GiB, 8589934592 bytes, 16777216 sectors
Disk model: QEMU HARDDISK   
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x89ab78e4

Device     Boot   Start      End  Sectors  Size Id Type
/dev/sda1  *       2048  1050623  1048576  512M  b W95 FAT32
/dev/sda2       1050624 16777215 15726592  7.5G  5 Extended
/dev/sda5       1052672 16777215 15724544  7.5G 83 Linux
```

* Redimensionner la taille du système de fichier EXT 

```bash
ubuntu@vm3:~$ sudo resize2fs /dev/sda5
resize2fs 1.45.5 (07-Jan-2020)
Filesystem at /dev/sda5 is mounted on /; on-line resizing required
old_desc_blocks = 1, new_desc_blocks = 1
The filesystem on /dev/sda5 is now 1965568 (4k) blocks long.
```


```bash
ubuntu@vm3:~$ df -h
Filesystem      Size  Used Avail Use% Mounted on
udev            448M     0  448M   0% /dev
tmpfs            99M  640K   98M   1% /run
/dev/sda5       7.4G  2.4G  4.6G  35% /
tmpfs           491M     0  491M   0% /dev/shm
tmpfs           5.0M     0  5.0M   0% /run/lock
tmpfs           491M     0  491M   0% /sys/fs/cgroup
/dev/sda1       511M  4.0K  511M   1% /boot/efi
tmpfs            99M     0   99M   0% /run/user/1000
```


>La taille de la partition `/dev/sda5` est maintenant 2G plus grande :-)
