[[_TOC_]]


# SYSNIX - Virtualisation, créer un snapshot un volume logique LVM

>Montrer comment créer un snapshot d'une VM partant après coup de supprimer des modifications.



## Prérequis
Mettre en place une machine virtuelle `vm3` stocké dans le volume logique `/dev/vg/vm3`.


## Arrêter la machine virtuelle `vm3`

```
hote:~$ virsh destroy vm3
```

## Créer un snapshot du volume logique `vm3`

```
             .---------------------------------..-------------------------.
Hote         | LV - /dev/vg/vm3                || LV - /dev/vg/vm3-s1     | 
             +---------------------------------+`-------------------------'
Guest        | /dev/vda                        |
             +---------+-----------------------+
partition    |/dev/vda1                        |
             | primaire                        |
             +---------------------------------+
LVM          | PV                              | 
             +---------------------------------+
             | VG  vmLvm1-vg                   | 
             +-----------------------+---------+
             | LV root               |LV swap_1|
             +-----------------------+---------+
             | ext4                  | swap    |
             +-----------------------+---------+
             | /                     | swap    |
             `-----------------------+---------'
```



* Créer le snapshot

```
hote:~$ sudo lvcreate -s /dev/vg/vm3 -L 1G -n /dev/vg/vm3-s1
  Logical volume "vm3-s1" created
```
* Afficher les volumes logiques

```
$ sudo lvdisplay /dev/vg/vm3*
  --- Logical volume ---
  LV Path                /dev/vg/vm3
  LV Name                vm3
  VG Name                vg1
  LV UUID                5nrscC-4t3O-DUdt-LRw9-nQmP-FBA6-3n6ExV
  LV Write Access        read/write
  LV Creation host, time mc0-0315-00-lab, 2017-01-19 12:41:04 +0100
  LV snapshot status     source of
                         vm3-s1 [active]
  LV Status              available
  # open                 0
  LV Size                4.00 GiB
  Current LE             1024
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           252:14
   
  --- Logical volume ---
  LV Path                /dev/vg/vm3-s1
  LV Name                vm3-s1
  VG Name                vg1
  LV UUID                D0NMBY-7NFW-IVew-a91k-uccY-gn8B-CJy3BZ
  LV Write Access        read/write
  LV Creation host, time mc0-0315-00-lab, 2017-01-23 09:13:17 +0100
  LV snapshot status     active destination for vm3
  LV Status              available
  # open                 0
  LV Size                4.00 GiB
  Current LE             1024
  COW-table size         1.00 GiB
  COW-table LE           256
  Allocated to snapshot  0.00%
  Snapshot chunk size    4.00 KiB
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           252:17
```




## Redémarrer la machine virtuel et faire les modifications (ajouter apache)
* Redémarrer la vm

```
hote:~m$ virsh start vm3
Domaine vm3 démarré
```

```
hote:~$ virsh console vm3
Connected to domain vm3
Escape character is ^]

Ubuntu 14.04.1 LTS ubuntuSrv ttyS0

vm3 login: 
```
* sur la vm, faire les modifications

```
guest:~$ sudo apt-get install apache2
```

* Vérifier le fonctionnement du serveur web apache avec le navigateur internet


## Revernir à l'état précédent (supprimer apache)
* Arrêter la vm

```
hote:~$ virsh destroy vm3
```
* supprimer les modifications

```
hote:~$ sudo lvconvert --merge /dev/vg/vm3-s1
  Merging of volume vm3-s1 started.
  vmTest3: Merged: 21.3%
  vmTest3: Merged: 72.8%
  vmTest3: Merged: 86.8%
```
* Afficher les volumes logiques

```
hote:~$ sudo lvdisplay /dev/vg1/vm3*
  --- Logical volume ---
  LV Path                /dev/vg1/vm3
  LV Name                vm3
  VG Name                vg1
  LV UUID                5nrscC-4t3O-DUdt-LRw9-nQmP-FBA6-3n6ExV
  LV Write Access        read/write
  LV Creation host, time mc0-0315-00-lab, 2017-01-19 12:41:04 +0100
  LV Status              available
  # open                 0
  LV Size                4.00 GiB
  Current LE             1024
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           252:14

```
* Redémarrer la vm

```
hote:~m$ virsh start vm3
Domaine vm3 démarré
```
* Vérifier le __non__ fonctionnement du serveur web apache avec le navigateur internet


## Conserver les modifications
* Arrêter la vm

```
hote:~$ virsh destroy vm3
```
* Supprimer le snapshot

```
hote:~$ sudo lvremove /dev/vg/vm3-s1
```
* Redémarrer la vm

```
hote:~m$ virsh start vm3
Domaine vm3 démarré
```


## Références

1.  Linux KVM LVM Snapshots / Revent - Mwiki,  [http://mwiki.yyovkov.net/index.php/Linux_KVM_LVM_Snapshots_/_Revent][1]

[1]:http://mwiki.yyovkov.net/index.php/Linux_KVM_LVM_Snapshots_/_Revent
