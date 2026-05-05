# Corrigé - Examen blanc virtualisation KVM/libvirt L6-L10

> Ce corrigé donne une solution type. Les noms d'interfaces, les IP DHCP, le nom du VG LVM et le nom de l'utilisateur peuvent changer selon votre installation. Remplacez toujours les placeholders : `<ISO_DEBIAN>`, `<VG>`, `<USER_VM>`, `<IP_VM1>`, `<IP_VM2>`, `<IP_VM3>`, `<INTERFACE>`.

---

## Partie 1 - Questions courtes

**1.1 - Rôles**

- **KVM** : module du noyau Linux qui permet d'utiliser les extensions de virtualisation du CPU.
- **QEMU** : émulateur et moteur d'exécution de la VM ; avec KVM, il exécute le code invité avec accélération matérielle.
- **libvirt** : couche d'administration qui fournit une API et des outils pour gérer les VM, réseaux et stockages.
- **`virt-install`** : outil en ligne de commande pour créer une VM libvirt.
- **`virsh`** : console d'administration libvirt pour lister, démarrer, arrêter, éditer, définir et inspecter les domaines, réseaux et pools.

**1.2 - VM, conteneur, hyperviseur**

- Une **machine virtuelle** exécute un système invité complet avec son propre noyau.
- Un **conteneur** isole des processus qui partagent le noyau de l'hôte.
- Un **hyperviseur** fournit la couche qui permet d'exécuter des machines virtuelles.

**1.3 - `raw` vs `qcow2`**

- `raw` : image disque simple, sans fonctionnalités avancées. Avantage : performances et simplicité. Inconvénient : pas de snapshot interne, taille souvent moins flexible.
- `qcow2` : format QEMU avec allocation dynamique, snapshots internes et options avancées. Avantage : flexible. Inconvénient : plus complexe et parfois moins performant.

**1.4 - Réseaux libvirt**

- `default` : réseau NAT libvirt habituel, souvent en `192.168.122.0/24`, qui permet aux VM de sortir vers l'extérieur via l'hôte.
- Réseau isolé : réseau virtuel interne entre VM et hôte, sans accès automatique au réseau extérieur.
- Pont réseau : bridge qui connecte les VM au même réseau que l'interface physique de l'hôte.

**1.5 - Console série vs SSH**

- La console série sert quand le réseau de la VM ne fonctionne pas, quand SSH n'est pas installé ou quand on doit dépanner le démarrage.
- SSH nécessite une IP, un serveur SSH démarré et une authentification valide.

**1.6 - LVM**

- **PV** : Physical Volume, support de stockage utilisé par LVM.
- **VG** : Volume Group, groupe qui rassemble un ou plusieurs PV.
- **LV** : Logical Volume, volume utilisable comme disque ou partition.
- **Snapshot LVM** : copie logique à un instant donné ; elle permet de revenir à un état précédent si le snapshot est conservé.

---

## Partie 2 - Préparation et création des VM

### 2.1 - Préparer l'environnement

```bash
mkdir -p ~/revision-virt/{images,xml,logs}
touch ~/revision-virt/logs/rapport.md
```

Commandes utiles pour le rapport :

```bash
{
  echo "# Rapport virtualisation"
  date
  whoami
  hostname
} >> ~/revision-virt/logs/rapport.md
```

Vérifier l'accès libvirt :

```bash
id
virsh -c qemu:///system list --all
```

Si l'utilisateur n'a pas les droits, solution habituelle :

```bash
sudo usermod -aG libvirt "$USER"
newgrp libvirt
```

Selon la distribution, il peut aussi être nécessaire d'appartenir au groupe `kvm`.

### 2.2 - Vérifier KVM/libvirt

Virtualisation CPU :

```bash
lscpu | grep -i virtualization
```

Modules KVM :

```bash
lsmod | grep kvm
```

Services possibles selon la distribution :

```bash
systemctl status libvirtd
systemctl status virtqemud
```

Liste des domaines :

```bash
virsh -c qemu:///system list --all
```

### 2.3 - Activer le réseau `default`

```bash
virsh -c qemu:///system net-list --all
```

Si `default` est inactif :

```bash
virsh -c qemu:///system net-start default
```

Activer le démarrage automatique :

```bash
virsh -c qemu:///system net-autostart default
```

Vérification :

```bash
virsh -c qemu:///system net-list --all
virsh -c qemu:///system net-dumpxml default | grep -E "name|ip address"
```

### 2.4 - Créer `rev-vm1` et `rev-vm2`

Exemple avec `virt-install` et une ISO Debian.

Créer `rev-vm1` :

```bash
virt-install --connect qemu:///system \
  --name rev-vm1 \
  --memory 1024 \
  --vcpus 1 \
  --disk path="$HOME/revision-virt/images/rev-vm1.raw",format=raw,bus=virtio,size=6 \
  --cdrom <ISO_DEBIAN> \
  --network network=default,model=virtio \
  --osinfo detect=on,require=off
```

Créer `rev-vm2` :

```bash
virt-install --connect qemu:///system \
  --name rev-vm2 \
  --memory 1024 \
  --vcpus 1 \
  --disk path="$HOME/revision-virt/images/rev-vm2.raw",format=raw,bus=virtio,size=6 \
  --cdrom <ISO_DEBIAN> \
  --network network=default,model=virtio \
  --osinfo detect=on,require=off
```

Pendant l'installation :

- `rev-vm1` : partitionnement assisté simple sur tout le disque.
- `rev-vm2` : partitionnement assisté avec LVM.

Variante console texte avec `--location` :

```bash
virt-install --connect qemu:///system \
  --name rev-vm1 \
  --memory 1024 \
  --vcpus 1 \
  --disk path="$HOME/revision-virt/images/rev-vm1.raw",format=raw,bus=virtio,size=6 \
  --location <ISO_DEBIAN> \
  --network network=default,model=virtio \
  --osinfo detect=on,require=off \
  --graphics none \
  --console pty,target_type=serial \
  --extra-args "console=ttyS0,115200n8"
```

Vérifications :

```bash
virsh -c qemu:///system list --all
virsh -c qemu:///system domblklist rev-vm1
virsh -c qemu:///system domblklist rev-vm2
```

### 2.5 - Console et SSH

Dans la VM, activer une console série :

```bash
sudo sed -i 's/^GRUB_CMDLINE_LINUX_DEFAULT=.*/GRUB_CMDLINE_LINUX_DEFAULT="console=ttyS0"/' /etc/default/grub
sudo update-grub
sudo systemctl enable --now serial-getty@ttyS0.service
sudo reboot
```

Depuis l'hôte :

```bash
virsh -c qemu:///system console rev-vm1
```

Installer et activer SSH dans la VM :

```bash
sudo apt update
sudo apt install -y openssh-server
sudo systemctl enable --now ssh
```

Trouver l'IP :

```bash
virsh -c qemu:///system domifaddr rev-vm1
```

Se connecter :

```bash
ssh <USER_VM>@<IP_VM1>
```

---

## Partie 3 - Clonage KVM/libvirt et clonage vers LVM

### 3.1 - Clonage fichier vers fichier

Arrêter proprement `rev-vm1` :

```bash
virsh -c qemu:///system shutdown rev-vm1
virsh -c qemu:///system domstate rev-vm1
```

Si la VM ne s'arrête pas après un délai raisonnable :

```bash
virsh -c qemu:///system destroy rev-vm1
```

Exporter le XML :

```bash
virsh -c qemu:///system dumpxml rev-vm1 > ~/revision-virt/xml/rev-vm1b.xml
```

Copier le disque :

```bash
cp ~/revision-virt/images/rev-vm1.raw ~/revision-virt/images/rev-vm1b.raw
```

Adapter `~/revision-virt/xml/rev-vm1b.xml` :

- remplacer `<name>rev-vm1</name>` par `<name>rev-vm1b</name>` ;
- supprimer la ligne `<uuid>...</uuid>` ;
- supprimer les lignes `<mac address='...'/>` ;
- remplacer la source disque par `~/revision-virt/images/rev-vm1b.raw`.

Exemple de source disque attendue :

```xml
<disk type='file' device='disk'>
  <driver name='qemu' type='raw'/>
  <source file='/home/<USER>/revision-virt/images/rev-vm1b.raw'/>
  <target dev='vda' bus='virtio'/>
</disk>
```

Définir et démarrer :

```bash
virsh -c qemu:///system define ~/revision-virt/xml/rev-vm1b.xml
virsh -c qemu:///system start rev-vm1b
virsh -c qemu:///system list --all
```

Pour éviter les doublons d'identité, une bonne pratique est d'utiliser `virt-sysprep` sur le disque copié avant le premier démarrage du clone :

```bash
sudo virt-sysprep -a ~/revision-virt/images/rev-vm1b.raw --hostname rev-vm1b
```

### 3.2 - Clonage fichier vers LV

Créer le LV de l'hôte :

```bash
sudo lvcreate -n rev-vm3 -L 6G <VG>
sudo lvs
```

Copier le contenu du disque de `rev-vm1`.

Méthode avec `qemu-img` :

```bash
sudo qemu-img convert -O raw ~/revision-virt/images/rev-vm1.raw /dev/<VG>/rev-vm3
```

Méthode avec `dd` :

```bash
sudo dd if=~/revision-virt/images/rev-vm1.raw of=/dev/<VG>/rev-vm3 bs=64M status=progress conv=fsync
```

Créer le XML :

```bash
virsh -c qemu:///system dumpxml rev-vm1 > ~/revision-virt/xml/rev-vm3.xml
```

Adapter `~/revision-virt/xml/rev-vm3.xml` :

- nom : `rev-vm3` ;
- supprimer `<uuid>...</uuid>` ;
- supprimer les adresses MAC ;
- remplacer le disque fichier par un disque bloc.

Exemple de disque bloc :

```xml
<disk type='block' device='disk'>
  <driver name='qemu' type='raw'/>
  <source dev='/dev/<VG>/rev-vm3'/>
  <target dev='vda' bus='virtio'/>
</disk>
```

Définir et démarrer :

```bash
virsh -c qemu:///system define ~/revision-virt/xml/rev-vm3.xml
virsh -c qemu:///system start rev-vm3
virsh -c qemu:///system domblklist rev-vm3
```

### 3.3 - Post-installation des clones

Dans chaque clone :

```bash
sudo hostnamectl set-hostname rev-vm1b
```

ou :

```bash
sudo hostnamectl set-hostname rev-vm3
```

Si nécessaire, régénérer l'identité machine :

```bash
sudo rm -f /etc/machine-id
sudo systemd-machine-id-setup
```

Si les clés hôte SSH sont dupliquées :

```bash
sudo rm -f /etc/ssh/ssh_host_*
sudo dpkg-reconfigure openssh-server
sudo systemctl restart ssh
```

Pourquoi : un clone brut peut garder le même hostname, le même identifiant machine et les mêmes clés SSH que la VM source. Cela crée des conflits réseau, des avertissements SSH et des comportements difficiles à diagnostiquer.

---

## Partie 4 - Stockage

### 4.1 - Étendre le disque de `rev-vm3`

Arrêter la VM :

```bash
virsh -c qemu:///system shutdown rev-vm3
virsh -c qemu:///system domstate rev-vm3
```

Agrandir le LV côté hôte :

```bash
sudo lvresize -L +2G /dev/<VG>/rev-vm3
sudo lvs /dev/<VG>/rev-vm3
```

Démarrer la VM :

```bash
virsh -c qemu:///system start rev-vm3
```

Dans la VM, identifier le disque et la partition racine :

```bash
lsblk
df -h /
findmnt /
```

Si l'outil `growpart` est disponible et que la racine est sur `/dev/vda2` :

```bash
sudo growpart /dev/vda 2
sudo resize2fs /dev/vda2
df -h /
```

Si la racine est sur une partition logique comme `/dev/vda5`, adaptez le numéro de partition :

```bash
sudo growpart /dev/vda 5
sudo resize2fs /dev/vda5
df -h /
```

Méthode manuelle possible avec `fdisk` :

```bash
sudo fdisk /dev/vda
```

Principe :

- noter le secteur de début de la partition racine ;
- supprimer puis recréer la partition avec le même secteur de début ;
- utiliser la nouvelle fin de disque ;
- écrire la table ;
- redémarrer ou exécuter `partprobe` ;
- lancer `resize2fs` sur la partition racine.

Piège important : agrandir le LV de l'hôte ne suffit pas. Il faut aussi agrandir la partition ou le LV invité, puis le système de fichiers.

### 4.2 - Snapshot LVM et retour arrière

Arrêter `rev-vm3` :

```bash
virsh -c qemu:///system shutdown rev-vm3
```

Créer le snapshot :

```bash
sudo lvcreate -s -n rev-vm3-s1 -L 1G /dev/<VG>/rev-vm3
sudo lvs
```

Démarrer la VM et installer Apache :

```bash
virsh -c qemu:///system start rev-vm3
```

Dans `rev-vm3` :

```bash
sudo apt update
sudo apt install -y apache2
systemctl status apache2
dpkg -l apache2
```

Revenir en arrière :

```bash
virsh -c qemu:///system shutdown rev-vm3
sudo lvconvert --merge /dev/<VG>/rev-vm3-s1
virsh -c qemu:///system start rev-vm3
```

Vérifier dans la VM :

```bash
dpkg -l apache2
systemctl status apache2
```

Si l'objectif était de conserver les modifications au lieu de revenir en arrière :

```bash
sudo lvremove /dev/<VG>/rev-vm3-s1
```

La VM doit être arrêtée pour créer un snapshot cohérent et pour fusionner proprement le snapshot.

### 4.3 - Ajouter un disque à `rev-vm2`

Créer une image `raw` de 1G :

```bash
qemu-img create -f raw ~/revision-virt/images/rev-data.raw 1G
```

Attacher le disque à `rev-vm2` :

```bash
virsh -c qemu:///system attach-disk rev-vm2 \
  "$HOME/revision-virt/images/rev-data.raw" \
  vdb \
  --targetbus virtio \
  --subdriver raw \
  --persistent \
  --live
```

Vérifier côté hôte :

```bash
virsh -c qemu:///system domblklist rev-vm2
```

Dans `rev-vm2` :

```bash
lsblk
```

Créer le PV :

```bash
sudo pvcreate /dev/vdb
sudo pvs
```

Trouver le VG invité :

```bash
sudo vgs
```

Ajouter le nouveau PV au VG invité :

```bash
sudo vgextend <VG_INVITE> /dev/vdb
sudo vgs
```

### 4.4 - Créer un LV `data` et le monter

Créer le LV :

```bash
sudo lvcreate -L 500M -n data <VG_INVITE>
sudo lvs
```

Formater :

```bash
sudo mkfs.ext4 /dev/<VG_INVITE>/data
```

Créer le point de montage :

```bash
sudo mkdir -p /mnt/data
```

Monter temporairement :

```bash
sudo mount /dev/<VG_INVITE>/data /mnt/data
df -Th /mnt/data
```

Récupérer l'UUID :

```bash
sudo blkid /dev/<VG_INVITE>/data
```

Ajouter une ligne dans `/etc/fstab` :

```fstab
UUID=<UUID_DATA> /mnt/data ext4 defaults 0 2
```

Tester :

```bash
sudo umount /mnt/data
sudo mount -a
df -Th /mnt/data
```

Bonne pratique : utiliser l'UUID dans `/etc/fstab`, car les noms `/dev/vdb`, `/dev/vdc` peuvent changer selon l'ordre de détection des disques.

---

## Partie 5 - Réseau virtuel, passerelle et SSH

### 5.1 - Créer le réseau isolé `rev-isole`

Créer `~/revision-virt/xml/rev-isole.xml` :

```xml
<network>
  <name>rev-isole</name>
  <bridge name='virbr50' stp='on' delay='0'/>
  <ip address='10.10.50.1' netmask='255.255.255.0'/>
</network>
```

Définir, démarrer et activer :

```bash
virsh -c qemu:///system net-define ~/revision-virt/xml/rev-isole.xml
virsh -c qemu:///system net-start rev-isole
virsh -c qemu:///system net-autostart rev-isole
virsh -c qemu:///system net-list --all
```

### 5.2 - Connecter les interfaces

Ajouter `rev-isole` à `rev-vm3` :

```bash
virsh -c qemu:///system attach-interface \
  --domain rev-vm3 \
  --type network \
  --source rev-isole \
  --model virtio \
  --config \
  --live
```

Ajouter `rev-isole` à `rev-vm2` :

```bash
virsh -c qemu:///system attach-interface \
  --domain rev-vm2 \
  --type network \
  --source rev-isole \
  --model virtio \
  --config \
  --live
```

Si `rev-vm2` doit être uniquement sur `rev-isole`, repérer puis détacher son interface `default` :

```bash
virsh -c qemu:///system domiflist rev-vm2
virsh -c qemu:///system detach-interface \
  --domain rev-vm2 \
  --type network \
  --mac <MAC_DEFAULT_VM2> \
  --config \
  --live
```

Dans `rev-vm3`, configurer deux interfaces. Exemple Netplan :

```yaml
network:
  version: 2
  ethernets:
    <IF_DEFAULT>:
      dhcp4: true
    <IF_ISOLE>:
      addresses:
        - 10.10.50.2/24
```

Appliquer :

```bash
sudo netplan apply
ip a
ip route
```

Dans `rev-vm2`, configurer l'interface isolée :

```yaml
network:
  version: 2
  ethernets:
    <IF_ISOLE>:
      addresses:
        - 10.10.50.20/24
      routes:
        - to: 192.168.122.0/24
          via: 10.10.50.2
```

Appliquer :

```bash
sudo netplan apply
ip a
ip route
```

Dans `rev-vm1`, garder le DHCP sur `default`.

### 5.3 - Configurer `rev-vm3` comme passerelle

Dans `rev-vm3`, activer le routage IPv4 immédiatement :

```bash
sudo sysctl -w net.ipv4.ip_forward=1
```

Activation permanente :

```bash
echo 'net.ipv4.ip_forward=1' | sudo tee /etc/sysctl.d/99-rev-gateway.conf
sudo sysctl --system
```

Route dans `rev-vm2` vers le réseau `default` :

```bash
sudo ip route add 192.168.122.0/24 via 10.10.50.2
```

Version persistante via Netplan déjà montrée :

```yaml
routes:
  - to: 192.168.122.0/24
    via: 10.10.50.2
```

Trouver l'adresse de `rev-vm3` sur `default` :

```bash
virsh -c qemu:///system domifaddr rev-vm3
```

Dans `rev-vm1`, ajouter une route vers le réseau isolé :

```bash
sudo ip route add 10.10.50.0/24 via <IP_VM3_DEFAULT>
```

Version persistante Netplan dans `rev-vm1` :

```yaml
network:
  version: 2
  ethernets:
    <IF_DEFAULT>:
      dhcp4: true
      routes:
        - to: 10.10.50.0/24
          via: <IP_VM3_DEFAULT>
```

Vérifications :

```bash
ip route
ping -c 3 10.10.50.2
ping -c 3 10.10.50.20
traceroute 10.10.50.20
```

Si le ping de `rev-vm1` vers `rev-vm2` échoue, vérifier les deux sens :

- route de `rev-vm1` vers `10.10.50.0/24` ;
- route de `rev-vm2` vers `192.168.122.0/24` ;
- `net.ipv4.ip_forward=1` sur `rev-vm3` ;
- firewall éventuel dans les VM.

### 5.4 - SSH direct, jump et tunnel

Sur chaque VM :

```bash
sudo apt update
sudo apt install -y openssh-server
sudo systemctl enable --now ssh
```

Depuis `rev-vm1` vers `rev-vm3` :

```bash
ssh <USER_VM>@<IP_VM3_DEFAULT>
```

Depuis `rev-vm3` vers `rev-vm2` :

```bash
ssh <USER_VM>@10.10.50.20
```

Depuis `rev-vm1` vers `rev-vm2` avec un jump par `rev-vm3` :

```bash
ssh -J <USER_VM>@<IP_VM3_DEFAULT> <USER_VM>@10.10.50.20
```

Tunnel local depuis `rev-vm1` :

```bash
ssh -fN -L 2222:10.10.50.20:22 <USER_VM>@<IP_VM3_DEFAULT>
```

Entrer dans le tunnel :

```bash
ssh -p 2222 <USER_VM>@localhost
```

Arrêter le tunnel :

```bash
pkill -f 'ssh -fN -L 2222:10.10.50.20:22'
```

### 5.5 - SSH sans mot de passe

Depuis `rev-vm1`, générer une clé :

```bash
ssh-keygen -t ed25519
```

Copier la clé vers `rev-vm3` :

```bash
ssh-copy-id <USER_VM>@<IP_VM3_DEFAULT>
```

Vérifier sans interaction :

```bash
ssh -o BatchMode=yes <USER_VM>@<IP_VM3_DEFAULT> hostname
```

Si `ssh-copy-id` n'est pas disponible :

```bash
cat ~/.ssh/id_ed25519.pub | ssh <USER_VM>@<IP_VM3_DEFAULT> 'mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys'
```

---

## Pièges fréquents

- **Réseau `default` inactif** : les VM démarrent, mais n'obtiennent pas d'IP NAT.
- **VM non arrêtée avant copie ou snapshot LVM** : risque de disque incohérent.
- **UUID libvirt dupliqué** : deux domaines ne doivent pas partager le même `<uuid>`.
- **Adresse MAC dupliquée** : DHCP, ARP et SSH deviennent confus.
- **Mauvais type de disque dans le XML** : fichier `raw` = `<source file='...'>`, LV bloc = `<source dev='...'>`.
- **Agrandissement incomplet** : après `lvresize`, il faut agrandir la partition ou le volume invité, puis le système de fichiers avec `resize2fs`.
- **Snapshot trop petit** : si beaucoup de blocs changent, le snapshot peut se remplir.
- **`/etc/fstab` avec `/dev/vdb`** : fragile ; préférer `UUID=<UUID_DATA>`.
- **Routes configurées dans un seul sens** : pour joindre deux réseaux via une passerelle, le chemin retour doit aussi être connu.
- **Confusion console/SSH** : `virsh console` dépanne sans réseau ; SSH exige que le réseau et le service SSH fonctionnent.
- **`virsh destroy`** : arrêt brutal, pas un arrêt propre. À utiliser seulement si `shutdown` ne suffit pas.

---

## Commandes de vérification finale

Depuis l'hôte :

```bash
virsh -c qemu:///system list --all
virsh -c qemu:///system net-list --all
virsh -c qemu:///system domblklist rev-vm1
virsh -c qemu:///system domblklist rev-vm2
virsh -c qemu:///system domblklist rev-vm3
virsh -c qemu:///system domifaddr rev-vm1
virsh -c qemu:///system domifaddr rev-vm2
virsh -c qemu:///system domifaddr rev-vm3
sudo lvs
```

Dans les VM :

```bash
hostname
ip a
ip route
lsblk
df -h
df -Th
```

Tests SSH attendus :

```bash
ssh <USER_VM>@<IP_VM3_DEFAULT> hostname
ssh -J <USER_VM>@<IP_VM3_DEFAULT> <USER_VM>@10.10.50.20 hostname
ssh -fN -L 2222:10.10.50.20:22 <USER_VM>@<IP_VM3_DEFAULT>
ssh -p 2222 <USER_VM>@localhost hostname
ssh -o BatchMode=yes <USER_VM>@<IP_VM3_DEFAULT> hostname
```
