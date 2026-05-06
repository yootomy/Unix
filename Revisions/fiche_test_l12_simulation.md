# Fiche de simulation — Test L12 (SYSNIX TE 2025.05)

> Reconstitution des questions à partir du fichier de vérification d'un examen précédent
> (`sysnix-te-202505-cattarin-nolan-verification 1.md`).
> Les commandes utilisées proviennent **exclusivement** des éléments de solution du cours :
>
> - `sysnix-activite-0004-gestion-acces` (permissions)
> - `sysnix-activite-0008-gestion-utilisateurs` (utilisateurs/groupes)
> - `sysnix-activite-0510-kvm-clone` (clone KVM, post-installation)
> - `sysnix-activite-0520-kvm-lvm-clone` (clone vers LV LVM)
> - `sysnix-activite-0560-kvm-lvm-add-pv` (ajout d'un volume physique)
> - `sysnix-activite-0570-kvm-lvm-add-lv` (création LV + format + montage permanent)
> - `sysnix-activite-0700-reseau-v3` (réseaux virtuels libvirt, ssh)
> - `sysnix-activite-0710-reseau-isole-v3` (réseau isolé, passerelle)
>
> Total estimé : **30 points** (3 × 10 pts).

---

## Contexte du test (déduit)

Le test demande de manipuler la machine **kvmRef1** (réf. présent sur l'hôte), de la **cloner** vers **kvmClone1** avec un disque secondaire LVM, et de mettre en place un réseau virtuel `te-network` avec une connexion **SSH par clés** entre **kvmRef1** et **kvmRef2**.

Schéma cible (déduit) :

```
                 +------------+        te-network 10.10.2.0/24
host (debian-usb-nc) ─────────| virbr1 |.1 ─── kvmRef1 (10.10.2.2 statique)
                 +------------+              kvmRef2 (10.10.2.x dhcp + nat default)
                 |                           kvmClone1 (default, dhcp)
                 +-- default 192.168.122.0/24 (nat libvirt)
```

---

## Partie 1 — Authentification et autorisation (10 points)

### Énoncé reconstitué

Sur **kvmRef1** :

1. Créer un groupe `int-s-pma`.
2. Créer **26 × 26 = 676 utilisateurs** nommés `user-AA` à `user-ZZ`, tous membres du groupe `int-s-pma`, avec un répertoire personnel.
3. Connecté en `user-AA`, créer l'arborescence suivante :
   ```
   ~/
   ├── dossierX
   │   ├── pif  (5 fichiers fichier01.txt … fichier05.txt)
   │   └── paf  (5 fichiers)
   └── dossierY
       ├── pif  (5 fichiers)
       └── paf  (5 fichiers)
   ```
4. Appliquer les droits suivants pour les membres du groupe `int-s-pma` (autres = aucun droit) :
   - Le **propriétaire** `user-AA` a tous les droits.
   - Les membres du groupe peuvent **traverser** `~user-AA` sans pouvoir lister son contenu.
   - Dans `dossierX` : lecture seule (lister, lire le contenu des fichiers).
   - Dans `dossierY` : lecture + écriture (ajouter / supprimer / modifier).
   - Le reste des utilisateurs n'a aucun accès.
5. Trouver tous les fichiers contenant `03` dans le nom et leur retirer **tous les droits** au groupe et aux autres (`-rw-------`). Vérifier avant/après.

---

### 1.1 Créer le groupe et les utilisateurs

#### Création du groupe

```bash
debian@kvmRef1:~$ sudo groupadd int-s-pma
debian@kvmRef1:~$ cat /etc/group | grep int-s-pma
```

#### Script `addusers.sh` (676 utilisateurs `user-AA` → `user-ZZ`)

```bash
debian@kvmRef1:~$ nano addusers.sh
```

Contenu :

```bash
#!/bin/bash
#################################
# Création des utilisateurs user-AA à user-ZZ
# membres du groupe int-s-pma
#################################
GROUP="int-s-pma"

for i in {A..Z}; do
    for j in {A..Z}; do
        USER="user-$i$j"
        useradd -m "$USER" -G "$GROUP"
    done
done
```

Exécution :

```bash
debian@kvmRef1:~$ chmod u+x addusers.sh
debian@kvmRef1:~$ sudo ./addusers.sh
```

#### Script `delusers.sh` (suppression de tous les utilisateurs)

```bash
debian@kvmRef1:~$ nano delusers.sh
```

Contenu :

```bash
#!/bin/bash
#################################
# Suppression des utilisateurs user-AA à user-ZZ
# (-r supprime aussi le home, -f force même si l'utilisateur est connecté)
#################################
for i in {A..Z}; do
    for j in {A..Z}; do
        USER="user-$i$j"
        userdel -r -f "$USER"
    done
done
```

Exécution :

```bash
debian@kvmRef1:~$ chmod u+x delusers.sh
debian@kvmRef1:~$ sudo ./delusers.sh
```

#### Vérification

```bash
debian@kvmRef1:~$ cat /etc/passwd | grep '^user-' | wc -l    # doit retourner 676
debian@kvmRef1:~$ id user-AA   # doit montrer le groupe secondaire int-s-pma
debian@kvmRef1:~$ id user-ZZ
```

> **Réf. cours :** structure des scripts `addusers.sh` / `delusers.sh` reprise
> de l'activité 0008 §7. `useradd -m` crée le home, `-G` ajoute aux groupes
> **secondaires** sans changer le primaire (cours 0008 §4).
> `userdel -r -f` supprime l'utilisateur **et** son répertoire personnel.

---

### 1.2 Créer l'arborescence (en tant que `user-AA`)

```bash
debian@kvmRef1:~$ sudo su -l user-AA
$ bash    # pour avoir un prompt complet (le shell par défaut est /bin/sh)

user-AA@kvmRef1:~$ mkdir -p ./dossier{X,Y}/p{i,a}f
user-AA@kvmRef1:~$ touch ./dossier{X,Y}/p{i,a}f/fichier0{1..5}.txt
user-AA@kvmRef1:~$ tree
```

> **Astuce :** l'expansion **brace** `{X,Y}` × `{i,a}` × `{1..5}` est exactement ce
> qu'utilise le cours pour générer plusieurs fichiers d'un coup (act. 0004 §13).

---

### 1.3 Appliquer les droits (instructions à l'admin et à `user-AA`)

Plan d'attaque (en se basant sur l'activité **0004 — Application des permissions**, exo `pier/d1/d2`) :

```bash
# 1) Changer le groupe propriétaire de toute l'arbo en int-s-pma
user-AA@kvmRef1:~$ chgrp -R int-s-pma .

# 2) Bloquer le reste du monde partout
user-AA@kvmRef1:~$ chmod -R o= .

# 3) Sur ~ : groupe = traverse uniquement (--x), pas de lecture
#    -> les autres user du groupe peuvent passer dans ~ mais pas lister son contenu
user-AA@kvmRef1:~$ chmod g=x .

# 4) dossierX : lecture seule pour le groupe (r-x sur dossiers, r-- sur fichiers)
#    'X' (X majuscule) = exécutable seulement si c'est un dossier
user-AA@kvmRef1:~$ chmod -R g=rX ./dossierX

# 5) dossierY : lecture + écriture pour le groupe (rwx sur dossiers, rw sur fichiers)
user-AA@kvmRef1:~$ chmod -R g=rwX ./dossierY

# Vérification
user-AA@kvmRef1:~$ tree -pug
```

> **Pourquoi `X` majuscule ?** D'après l'act. 0004, `chmod -R g=rX` met `r-x` sur
> les **dossiers** et `r--` sur les **fichiers** : exactement ce qu'on veut ici
> (sans rendre les `.txt` exécutables).
>
> Résultat attendu :
>
> ```
> [drwx--x---]  ~              (user-AA / int-s-pma)
> ├── [drwxr-x---]  dossierX
> │   ├── [drwxr-x---]  paf
> │   │   └── [-rw-r-----]  fichier0?.txt
> │   └── [drwxr-x---]  pif
> └── [drwxrwx---]  dossierY
>     ├── [drwxrwx---]  paf
>     │   └── [-rw-rw----]  fichier0?.txt
>     └── [drwxrwx---]  pif
> ```

---

### 1.4 Tests d'accès demandés (à exécuter en `user-CC` ou autre membre du groupe)

```bash
# user-AA (propriétaire) : tout est autorisé
user-AA$ mkdir test                      # autorisé
user-AA$ ls .                            # autorisé
user-AA$ rmdir test                      # autorisé

# user-CC (membre du groupe int-s-pma) : peut traverser, pas lister ~user-AA
user-CC$ ls /home/user-AA                # REFUSÉ (pas de 'r' sur ~)
user-CC$ ls /home/user-AA/dossierX       # autorisé (on connaît le nom)
user-CC$ ls /home/user-AA/dossierY       # autorisé

# dossierX : lecture seule
user-CC$ touch /home/user-AA/dossierX/paf/x.txt           # REFUSÉ
user-CC$ rm    /home/user-AA/dossierX/paf/fichier01.txt   # REFUSÉ
user-CC$ cat   /home/user-AA/dossierX/paf/fichier01.txt   # autorisé
user-CC$ ls    /home/user-AA/dossierX/paf/                # autorisé

# dossierY : lecture + écriture
user-CC$ touch /home/user-AA/dossierY/paf/fichier06.txt   # autorisé
user-CC$ rm    /home/user-AA/dossierY/paf/fichier06.txt   # autorisé
user-CC$ cat   /home/user-AA/dossierY/paf/fichier01.txt   # autorisé

# Utilisateur HORS groupe (ex: debian) : aucun accès
debian$ cd /home/user-AA                 # REFUSÉ
```

---

### 1.5 Recherche `find` + modification des droits sur les fichiers `*03*`

```bash
# Lister tous les fichiers (-type f) dont le nom contient '03'
debian@kvmRef1:~$ sudo find /home -name '*03*' -type f

# Afficher leurs droits AVANT
debian@kvmRef1:~$ sudo find /home -name '*03*' -type f -exec ls -ld {} \;

# Retirer tous les droits au groupe et aux autres (-> rw-------)
debian@kvmRef1:~$ sudo find /home -name '*03*' -type f -exec chmod o=,g= {} \;

# Vérifier APRÈS
debian@kvmRef1:~$ sudo find /home -name '*03*' -type f -exec ls -ld {} \;
```

> **Pièges fréquents** :
> - `chmod o=,g=` (signe `=` sans valeur) **réinitialise** à zéro, ne fait pas `+`.
> - Toujours `-type f` pour ne pas matcher les dossiers `0003-…`.
> - `find … -exec … {} \;` (point-virgule échappé) ; `+` regroupe mais ici on
>   garde `\;` comme dans le test de référence.

---

## Partie 2 — Virtualisation (10 points)

### Énoncé reconstitué

Sur l'hôte (`debian-usb-nc`) :

1. Créer **deux volumes logiques** dans le pool LVM `lvm` :
   - `lvKvmClone1-1` de **7 GiB** (disque système)
   - `lvKvmClone1-2` de **1 GiB** (disque secondaire pour `int-s-pma`)
2. **Cloner** la VM `kvmRef2` vers `kvmClone1` en plaçant son disque dans `lvKvmClone1-1`.
3. Faire la **post-installation** sur le clone (hostname, hosts, clés ssh, réseau).
4. Ajouter le second disque (`lvKvmClone1-2`) à la VM `kvmClone1` (via virt-manager
   ou `virsh attach-disk`).
5. À l'intérieur de `kvmClone1` : transformer ce second disque en LVM, créer un VG,
   un LV `int-s-pma`, formater en ext4 et le monter en permanence sur
   `/home/int-s-pma`. Le dossier doit appartenir à `debian:debian`.

---

### 2.1 Créer les deux volumes logiques côté hôte (dans `virsh`)

```bash
hote:~$ virsh -c qemu:///system

virsh # vol-create-as lvm lvKvmClone1-1 7G --format raw
virsh # vol-create-as lvm lvKvmClone1-2 1G --format raw
virsh # vol-list lvm
```

> **Réf. cours :** la création d'un volume avec `vol-create-as` provient de
> l'act. 0520 (KVM dans LVM) et 0560 (ajout d'un PV).

---

### 2.2 Cloner la VM `kvmRef2` vers `kvmClone1`

```bash
hote:~$ sudo virt-clone -o kvmRef2 \
                        --name kvmClone1 \
                        --file /dev/debian-usb-nc-vg/lvKvmClone1-1 \
                        --check path_exists=off
```

> Le flag `--check path_exists=off` évite l'erreur "le chemin existe déjà" car
> le LV est pré-créé. La taille du LV doit **être >=** au disque source.

Vérification :

```bash
hote:~$ virsh -c qemu:///system list --all
hote:~$ virsh -c qemu:///system dumpxml kvmClone1   # vérifier <source dev=…>
```

---

### 2.3 Post-installation du clone (act. 0510 §post-install)

Dans la VM `kvmClone1` (console) :

```bash
debian@kvmRef2:~$ sudo hostnamectl set-hostname kvmClone1
                    # ou : sudo nano /etc/hostname  -> 'kvmClone1'
debian@kvmRef2:~$ sudo nano /etc/hosts
                    # remplacer 'kvmRef2' par 'kvmClone1'

# Régénérer les clés SSH du serveur (sinon doublon avec kvmRef2)
debian@kvmRef2:~$ sudo rm /etc/ssh/ssh_host_*
debian@kvmRef2:~$ sudo dpkg-reconfigure openssh-server
                    # ou : sudo ssh-keygen -A
debian@kvmRef2:~$ sudo reboot
```

> **Pourquoi régénérer les clés ?** Sans cela, deux machines auraient la même
> empreinte d'hôte et SSH refuserait la connexion (act. 0510, fiche post-installation).

Après reboot, vérifier :

```bash
debian@kvmClone1:~$ cat /etc/hostname
debian@kvmClone1:~$ cat /etc/hosts
debian@kvmClone1:~$ for f in $(ls /etc/ssh/ssh_host_*.pub); do ssh-keygen -lf $f; done
```

---

### 2.4 Ajouter le second disque à la VM (côté hôte)

Option `virt-manager` : "Add Hardware" → Storage → Custom storage →
`/dev/debian-usb-nc-vg/lvKvmClone1-2` → bus `virtio`, type `raw`.

Option ligne de commande (act. 0560) :

```bash
hote:~$ virsh -c qemu:///system attach-disk \
        --domain kvmClone1 \
        --source /dev/debian-usb-nc-vg/lvKvmClone1-2 \
        --target vdb --targetbus virtio \
        --driver qemu --subdriver raw \
        --sourcetype block --persistent
```

---

### 2.5 Transformer `/dev/vdb` en LVM dans la VM (act. 0560 + 0570)

```bash
debian@kvmClone1:~$ sudo fdisk -l                # confirmer la présence de /dev/vdb (1 GiB)

# 1) Définir vdb comme volume physique LVM
debian@kvmClone1:~$ sudo pvcreate /dev/vdb
debian@kvmClone1:~$ sudo pvs

# 2) Créer un nouveau groupe de volume avec ce PV
debian@kvmClone1:~$ sudo vgcreate kvmRef2-ch-int-s-pma /dev/vdb

# 3) Créer un LV qui occupe tout l'espace libre du VG
debian@kvmClone1:~$ sudo lvcreate --extents 100%FREE \
                                  --name int-s-pma \
                                  kvmRef2-ch-int-s-pma

# 4) Formater en ext4
debian@kvmClone1:~$ sudo mkfs.ext4 /dev/kvmRef2-ch-int-s-pma/int-s-pma

# 5) Préparer le point de montage
debian@kvmClone1:~$ sudo mkdir /home/int-s-pma

# 6) Montage temporaire pour test
debian@kvmClone1:~$ sudo mount -t ext4 /dev/kvmRef2-ch-int-s-pma/int-s-pma /home/int-s-pma

# 7) Propriétaire du dossier
debian@kvmClone1:~$ sudo chown debian:debian /home/int-s-pma
```

---

### 2.6 Rendre le montage permanent (`/etc/fstab`)

```bash
debian@kvmClone1:~$ sudo nano /etc/fstab
```

Ajouter en fin de fichier :

```
/dev/mapper/kvmRef2--ch--int--s--pma-int--s--pma /home/int-s-pma ext4 defaults 0 2
```

> ⚠️ Dans `/dev/mapper/`, les **tirets** simples deviennent `--` (échappement systemd).
> `kvmRef2-ch-int-s-pma` (VG) → `kvmRef2--ch--int--s--pma`.

Test du fstab :

```bash
debian@kvmClone1:~$ sudo umount /home/int-s-pma
debian@kvmClone1:~$ sudo mount -a              # doit re-monter sans erreur
debian@kvmClone1:~$ mount -t ext4              # doit lister le LV
debian@kvmClone1:~$ df -h /home/int-s-pma
```

### 2.7 Commandes de vérification finales (côté hôte)

```bash
hote:~$ sudo vgdisplay -v                                # voit lvKvmClone1-1 et -2
hote:~$ virsh -c qemu:///system dumpxml kvmClone1        # 2 disques bus virtio
hote:~$ virsh -c qemu:///system list --all
hote:~$ virsh -c qemu:///system start kvmClone1
hote:~$ virsh -c qemu:///system domifaddr kvmClone1
```

Côté `kvmClone1` :

```bash
debian@kvmClone1:~$ cat /etc/hostname
debian@kvmClone1:~$ cat /etc/hosts
debian@kvmClone1:~$ ip a
debian@kvmClone1:~$ ip route
debian@kvmClone1:~$ sudo fdisk -l
debian@kvmClone1:~$ lsblk -f
debian@kvmClone1:~$ ls -ld /home/int-s-pma
debian@kvmClone1:~$ date > /home/int-s-pma/date.txt && cat /home/int-s-pma/date.txt
debian@kvmClone1:~$ cat /etc/fstab
debian@kvmClone1:~$ mount -t ext4
```

---

## Partie 3 — Mise en réseau et accès SSH (10 points)

### Énoncé reconstitué

Sur l'hôte :

1. Créer un **réseau virtuel libvirt** `te-network` :
   - Bridge `virbr1`, **non natté**, sous-réseau `10.10.2.0/24`, passerelle `10.10.2.1`,
     plage DHCP `10.10.2.100 → 10.10.2.254`.
2. Connecter la VM `kvmRef1` **uniquement** à `te-network`.
3. Connecter la VM `kvmRef2` à **deux réseaux** : `default` (NAT, pour internet)
   et `te-network`.
4. Configurer `kvmRef1` avec une adresse IP **statique** `10.10.2.2/24`,
   passerelle `10.10.2.1`.
5. Configurer `kvmRef2` en DHCP sur les deux interfaces.
6. Mettre en place une connexion SSH **sans mot de passe** depuis `kvmRef2` vers
   `kvmRef1` (clé RSA + `ssh-copy-id`).

---

### 3.1 Création du réseau `te-network` (côté hôte)

Fichier `te-network.xml` :

```xml
<network>
  <name>te-network</name>
  <bridge name='virbr1' stp='on' delay='0'/>
  <domain name='te-network'/>
  <ip address='10.10.2.1' netmask='255.255.255.0'>
    <dhcp>
      <range start='10.10.2.100' end='10.10.2.254'/>
    </dhcp>
  </ip>
</network>
```

> **Important :** pas de balise `<forward mode='nat'/>` → réseau **isolé**
> (act. 0700 §"Création du réseau isolé").

```bash
hote:~$ virsh -c qemu:///system net-define ./te-network.xml
hote:~$ virsh -c qemu:///system net-autostart te-network
hote:~$ virsh -c qemu:///system net-start te-network
hote:~$ virsh -c qemu:///system net-list --all
hote:~$ virsh -c qemu:///system net-dumpxml te-network
```

---

### 3.2 Brancher les VM (via virt-manager ou `virsh attach-interface`)

Sur `kvmRef1` (une seule interface, sur `te-network`) :
- Modifier la VM en éteignant : `Détails matériel` → `NIC` → source `te-network`
- ou `virsh attach-interface --domain kvmRef1 --type network --source te-network --model virtio --persistent` après avoir détaché l'ancienne.

Sur `kvmRef2` (garde `default` + ajoute `te-network`) :
- Ajouter une seconde NIC sur `te-network`.

Vérification côté hôte :

```bash
hote:~$ virsh -c qemu:///system dumpxml kvmRef1 | grep -A2 '<interface'
hote:~$ virsh -c qemu:///system dumpxml kvmRef2 | grep -A2 '<interface'
```

---

### 3.3 Configuration réseau de `kvmRef1` (IP statique)

```bash
debian@kvmRef1:~$ sudo nano /etc/network/interfaces
```

Contenu :

```
# This file describes the network interfaces available on your system
source /etc/network/interfaces.d/*

# loopback
auto lo
iface lo inet loopback

# carte principale, statique sur te-network
allow-hotplug enp1s0
iface enp1s0 inet static
  address 10.10.2.2
  netmask 255.255.255.0
  gateway 10.10.2.1
```

Application :

```bash
debian@kvmRef1:~$ sudo systemctl restart networking.service
debian@kvmRef1:~$ ip a
debian@kvmRef1:~$ ip route        # default via 10.10.2.1 dev enp1s0
debian@kvmRef1:~$ cat /etc/resolv.conf
```

---

### 3.4 Configuration réseau de `kvmRef2` (DHCP sur les deux interfaces)

```bash
debian@kvmRef2:~$ sudo nano /etc/network/interfaces
```

```
source /etc/network/interfaces.d/*

auto lo
iface lo inet loopback

# 1ère carte sur 'default' (NAT, internet)
allow-hotplug enp1s0
iface enp1s0 inet dhcp

# 2nde carte sur 'te-network'
allow-hotplug enp8s0
iface enp8s0 inet dhcp
```

```bash
debian@kvmRef2:~$ sudo systemctl restart networking.service
debian@kvmRef2:~$ ip a            # enp1s0 = 192.168.122.x ; enp8s0 = 10.10.2.x
debian@kvmRef2:~$ ip route        # default via 192.168.122.1
```

---

### 3.5 SSH sans mot de passe : `kvmRef2` → `kvmRef1`

Sur `kvmRef2` (le client) :

```bash
debian@kvmRef2:~$ ssh-keygen
# Entrer puis Enter, Enter, Enter — pas de passphrase pour automatiser
# -> /home/debian/.ssh/id_rsa et id_rsa.pub

debian@kvmRef2:~$ ssh-copy-id debian@10.10.2.2
# Mot de passe de debian@kvmRef1 demandé une seule fois

# Test de la connexion par clé
debian@kvmRef2:~$ ssh debian@10.10.2.2          # plus aucun mot de passe
debian@kvmRef2:~$ ssh -v debian@10.10.2.2 -- hostname -f
                                                # doit afficher 'kvmRef1'
```

> **Réf. cours :** procédure identique à l'act. 0700 §"Connexion ssh sans mot de
> passe" : `ssh-keygen` puis `ssh-copy-id`. Vérification finale avec `ssh -v`
> (lignes "Server accepts key … using publickey").

---

### 3.6 Vérifications finales

Sur l'hôte :

```bash
hote:~$ virsh -c qemu:///system net-list --all
hote:~$ virsh -c qemu:///system net-dumpxml te-network
hote:~$ virsh -c qemu:///system dumpxml kvmRef1
hote:~$ virsh -c qemu:///system dumpxml kvmRef2
hote:~$ virsh -c qemu:///system list --all
```

Sur `kvmRef1` :

```bash
debian@kvmRef1:~$ cat /etc/network/interfaces
debian@kvmRef1:~$ ip a
debian@kvmRef1:~$ ip route
debian@kvmRef1:~$ cat /etc/resolv.conf
debian@kvmRef1:~$ ls -l ~/.ssh/                       # contient authorized_keys
debian@kvmRef1:~$ ssh-keygen -lf ~/.ssh/authorized_keys
```

Sur `kvmRef2` :

```bash
debian@kvmRef2:~$ cat /etc/network/interfaces
debian@kvmRef2:~$ ip a
debian@kvmRef2:~$ ip route
debian@kvmRef2:~$ cat /etc/resolv.conf
debian@kvmRef2:~$ ls -l ~/.ssh/                       # id_rsa, id_rsa.pub, known_hosts
debian@kvmRef2:~$ ssh -v debian@10.10.2.2 -- hostname -f
```

---

## Récapitulatif des commandes-clés (anti-blanc)

### Utilisateurs / groupes (act. 0008)

| Action                        | Commande                                                |
| ----------------------------- | ------------------------------------------------------- |
| Créer un groupe               | `sudo groupadd <nom>`                                   |
| Créer un user avec home       | `sudo useradd -m <nom>`                                 |
| Définir mot de passe          | `sudo passwd <nom>`                                     |
| Ajouter à un groupe secondaire| `sudo useradd -m <nom> -G <groupe>`                     |
| Changer le groupe primaire    | `sudo usermod -g <groupe> <user>`                       |
| Voir UID/GID                  | `id <user>`                                             |
| Voir groupes                  | `groups <user>` ou `cat /etc/group \| grep <user>`      |

### Permissions (act. 0004)

| Forme           | Effet                                                       |
| --------------- | ----------------------------------------------------------- |
| `chmod -R o= .` | Aucun droit pour "autres" récursivement                     |
| `chmod g=x .`   | Le groupe peut **traverser** un dossier (pas le lister)     |
| `chmod g=rX d`  | Lecture + traversée (sans rendre les fichiers exécutables)  |
| `chmod g=rwX d` | Lecture + écriture + traversée                              |
| `chgrp -R <g> .`| Changer le groupe propriétaire récursivement                |
| `tree -pug`     | Voir droits + propriétaire + groupe                         |

### KVM/libvirt (act. 0510, 0520)

| Action                            | Commande                                                        |
| --------------------------------- | --------------------------------------------------------------- |
| Lister VM                         | `virsh -c qemu:///system list --all`                            |
| Démarrer / arrêter                | `virsh start <vm>` / `virsh shutdown <vm>` / `destroy`          |
| Console texte                     | `virsh -c qemu:///system console <vm>` (sortir : Ctrl+])        |
| Voir XML                          | `virsh dumpxml <vm>`                                            |
| Cloner                            | `virt-clone -o <src> --name <dst> --file <chemin> --check path_exists=off` |
| IP d'une VM                       | `virsh -c qemu:///system domifaddr <vm>`                        |
| Créer un volume LVM via virsh     | `vol-create-as <pool> <nom> <taille> --format raw`              |
| Attacher un disque                | `virsh attach-disk --domain <vm> --source <…> --target vdb --persistent` |

### LVM côté invité (act. 0560, 0570)

| Étape           | Commande                                          |
| --------------- | ------------------------------------------------- |
| Créer un PV     | `sudo pvcreate /dev/vdb`                          |
| Créer un VG     | `sudo vgcreate <vg> /dev/vdb`                     |
| Étendre un VG   | `sudo vgextend <vg> /dev/vdb`                     |
| Créer un LV     | `sudo lvcreate -L 500M -n <lv> <vg>` ou `--extents 100%FREE` |
| Formater        | `sudo mkfs.ext4 /dev/<vg>/<lv>`                   |
| Monter          | `sudo mount -t ext4 /dev/<vg>/<lv> /mnt`          |
| Voir mappings   | `lsblk -f` / `mount -t ext4` / `df -h`            |

### Réseau (act. 0700, 0710)

| Action                         | Commande                                             |
| ------------------------------ | ---------------------------------------------------- |
| Lister réseaux libvirt         | `virsh net-list --all`                               |
| XML d'un réseau                | `virsh net-dumpxml <net>`                            |
| Définir / démarrer / autostart | `virsh net-define f.xml` / `net-start` / `net-autostart` |
| Restart réseau Debian (interfaces) | `sudo systemctl restart networking.service`     |
| Voir IPs / routes              | `ip a` / `ip route`                                  |
| DNS                            | `cat /etc/resolv.conf`                               |

### SSH (act. 0700)

| Action                     | Commande                                       |
| -------------------------- | ---------------------------------------------- |
| Générer une paire de clés  | `ssh-keygen` (Enter, Enter, Enter)             |
| Copier la clé publique     | `ssh-copy-id <user>@<host>`                    |
| Tester en mode debug       | `ssh -v <user>@<host>`                         |
| Empreinte d'une clé        | `ssh-keygen -lf <fichier.pub>`                 |
| Lister clés du serveur     | `for f in /etc/ssh/ssh_host_*.pub; do ssh-keygen -lf $f; done` |

---

## Pièges à éviter

1. **`/etc/fstab` LVM** : doubler les tirets dans `/dev/mapper/<vg>-<lv>` (`-` → `--`).
2. **Post-installation d'un clone** : oublier de régénérer les clés SSH d'hôte
   et de changer `/etc/hostname` + `/etc/hosts` → conflits sur le réseau.
3. **`virt-clone --check path_exists=off`** est nécessaire si le LV cible a été
   pré-créé.
4. **`chmod o=,g=`** (sans valeur après `=`) supprime *tous* les droits ; ne pas
   confondre avec `chmod o-rwx,g-rwx`.
5. **`-type f`** dans `find` pour ne pas matcher les dossiers.
6. **Réseau isolé vs nat** : pas de `<forward mode='nat'/>` pour un réseau isolé,
   sinon les VM auront accès à internet.
7. **`useradd` vs `adduser`** : `useradd -m` est minimaliste (pas de mot de passe,
   shell `/bin/sh`) ; `adduser` est interactif.
8. **`-G` vs `-g`** dans `useradd`/`usermod` : `-g` change le groupe **primaire**,
   `-G` ajoute aux groupes **secondaires** (sans toucher au primaire).
9. **`chmod -R g=rX`** : le `X` majuscule applique `x` uniquement aux dossiers
   (et aux fichiers déjà exécutables) — toujours préférer à `g=rx` quand on
   manipule des arbres mixtes.
10. **`ssh-copy-id`** échoue si `/etc/ssh/sshd_config` interdit
    `PasswordAuthentication` côté serveur ; dans ce cas, copier manuellement
    `id_rsa.pub` dans `~/.ssh/authorized_keys` (act. 0700 §"De le cas où
    l'autorisation par mot de passe est désactivée").
