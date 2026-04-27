# SysNix — Leçons 08 et 09 : Toutes les commandes

---

## 1. Vérification de l'installation KVM/libvirt

```bash
# Vérifier que virsh et virt-manager sont installés
which virsh
which virt-manager

# Vérifier que tu es dans le groupe libvirt
id
groups

# Vérifier les paquets installés
dpkg -l | grep -E "libvirt|qemu|kvm"
```

---

## 2. Création du pool de stockage

```bash
# Créer le dossier pour stocker les disques des VMs
sudo mkdir -p /home/henochrjt/vms
sudo chown henochrjt:henochrjt /home/henochrjt/vms

# Définir et démarrer le pool de stockage dans libvirt
sudo virsh pool-define-as vms-home dir --target /home/henochrjt/vms
sudo virsh pool-start vms-home
sudo virsh pool-autostart vms-home

# Vérifier
sudo virsh pool-list --all
```

---

## 3. Création des disques raw et des VMs vm1 et vm2

```bash
# Créer les fichiers disque raw de 6G
sudo qemu-img create -f raw /home/henochrjt/vms/vm1.raw 6G
sudo qemu-img create -f raw /home/henochrjt/vms/vm2.raw 6G
sudo chown libvirt-qemu:kvm /home/henochrjt/vms/vm1.raw /home/henochrjt/vms/vm2.raw

# Générer le XML de vm1 sans la démarrer
sudo virt-install \
  --connect qemu:///system \
  --name vm1 \
  --memory 1024 \
  --vcpus 1 \
  --disk path=/home/henochrjt/vms/vm1.raw,format=raw,bus=virtio \
  --cdrom /home/henochrjt/Téléchargements/debian-13.4.0-amd64-netinst.iso \
  --network network=default,model=virtio \
  --osinfo detect=on,require=off \
  --graphics spice \
  --print-xml > /tmp/vm1.xml

# Générer le XML de vm2
sudo virt-install \
  --connect qemu:///system \
  --name vm2 \
  --memory 1024 \
  --vcpus 1 \
  --disk path=/home/henochrjt/vms/vm2.raw,format=raw,bus=virtio \
  --cdrom /home/henochrjt/Téléchargements/debian-13.4.0-amd64-netinst.iso \
  --network network=default,model=virtio \
  --osinfo detect=on,require=off \
  --graphics spice \
  --print-xml > /tmp/vm2.xml

# Extraire le premier bloc XML valide (le fichier contient 2 blocs)
python3 -c "
import re
for fname in ['/tmp/vm1.xml', '/tmp/vm2.xml']:
    with open(fname) as f: content = f.read()
    match = re.search(r'(<domain.*?</domain>)', content, re.DOTALL)
    name = fname.replace('.xml', '_clean.xml')
    with open(name, 'w') as f: f.write(match.group(1))
"

# Définir les VMs sans les démarrer
sudo virsh define /tmp/vm1_clean.xml
sudo virsh define /tmp/vm2_clean.xml

# Vérifier — les VMs doivent être à l'état "fermé"
sudo virsh list --all
```

> **Action manuelle requise :** Ouvrir `virt-manager`, démarrer vm1 et vm2, et
> installer Debian trixie :
> - **vm1** → partitionnement : *Assisté - utiliser un disque entier*
> - **vm2** → partitionnement : *Assisté - utiliser tout un disque avec LVM*

---

## 4. Éjecter l'ISO après installation

```bash
# Vérifier que l'ISO est encore attachée
sudo virsh domblklist vm1
sudo virsh domblklist vm2

# Éjecter l'ISO des deux VMs
sudo virsh change-media vm1 hda --eject --config
sudo virsh change-media vm2 hda --eject --config

# Vérifier
sudo virsh domblklist vm1
sudo virsh domblklist vm2
```

---

## 5. Configuration de l'accès console texte (GRUB)

```bash
# Démarrer les VMs
sudo virsh start vm1
sudo virsh start vm2

# Attendre le démarrage et récupérer les IPs
sleep 20
sudo virsh domifaddr vm1
sudo virsh domifaddr vm2

# Se connecter en SSH et configurer GRUB sur vm1
# (remplacer IP_VM1 et IP_VM2 par les IPs obtenues ci-dessus)
ssh debian@IP_VM1 "echo 'debianpass' | sudo -S bash -c \
  \"sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT=.*/GRUB_CMDLINE_LINUX_DEFAULT=\\\"quiet console=ttyS0\\\"/' \
  /etc/default/grub && update-grub\""

ssh debian@IP_VM2 "echo 'debianpass' | sudo -S bash -c \
  \"sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT=.*/GRUB_CMDLINE_LINUX_DEFAULT=\\\"quiet console=ttyS0\\\"/' \
  /etc/default/grub && update-grub\""

# Vérifier la config
ssh debian@IP_VM1 "grep GRUB_CMDLINE_LINUX_DEFAULT /etc/default/grub"
ssh debian@IP_VM2 "grep GRUB_CMDLINE_LINUX_DEFAULT /etc/default/grub"

# Éteindre proprement les VMs
ssh debian@IP_VM1 "echo 'debianpass' | sudo -S poweroff"
ssh debian@IP_VM2 "echo 'debianpass' | sudo -S poweroff"
```

---

## 6. Clonage vm1 → vm1b (fichier raw vers fichier raw)

```bash
# vm1 doit être éteinte
sudo virsh list --all

# Cloner vm1 vers vm1b
sudo virt-clone \
  --connect qemu:///system \
  --original vm1 \
  --name vm1b \
  --file /home/henochrjt/vms/vm1b.raw

# Vérifier
sudo virsh list --all
ls -lh /home/henochrjt/vms/
```

---

## 7. Clonage vm1 → vm3 et vm2 → vm4 (dans des volumes logiques LVM)

```bash
# Créer les volumes logiques de 6G dans le VG existant
sudo lvcreate -L 6G -n kvm-vm3 debian-usb-jth-vg
sudo lvcreate -L 6G -n kvm-vm4 debian-usb-jth-vg

# Vérifier
sudo lvs | grep kvm

# Copier le contenu de vm1.raw dans kvm-vm3
sudo dd if=/home/henochrjt/vms/vm1.raw of=/dev/debian-usb-jth-vg/kvm-vm3 bs=4M status=progress

# Copier le contenu de vm2.raw dans kvm-vm4
sudo dd if=/home/henochrjt/vms/vm2.raw of=/dev/debian-usb-jth-vg/kvm-vm4 bs=4M status=progress

# Créer les définitions VM pour vm3 et vm4 (avec --preserve-data pour ne pas écraser le LV)
sudo virt-clone \
  --connect qemu:///system \
  --original vm1 \
  --name vm3 \
  --file /dev/debian-usb-jth-vg/kvm-vm3 \
  --preserve-data

sudo virt-clone \
  --connect qemu:///system \
  --original vm2 \
  --name vm4 \
  --file /dev/debian-usb-jth-vg/kvm-vm4 \
  --preserve-data

# Vérifier
sudo virsh list --all
```

---

## 8. Post-installation de vm3 et vm4

```bash
# Démarrer vm3 et vm4
sudo virsh start vm3
sudo virsh start vm4
sleep 25

# Récupérer les IPs
sudo virsh domifaddr vm3
sudo virsh domifaddr vm4

# Post-installation vm3 (remplacer IP_VM3 par l'IP obtenue)
ssh debian@IP_VM3 "echo 'debianpass' | sudo -S bash -c '
  echo vm3 > /etc/hostname
  sed -i \"s/vm1/vm3/g\" /etc/hosts
  rm -v /etc/ssh/ssh_host_*
  dpkg-reconfigure -f noninteractive openssh-server
'"

# Post-installation vm4 (remplacer IP_VM4 par l'IP obtenue)
ssh debian@IP_VM4 "echo 'debianpass' | sudo -S bash -c '
  echo vm4 > /etc/hostname
  sed -i \"s/vm2/vm4/g\" /etc/hosts
  rm -v /etc/ssh/ssh_host_*
  dpkg-reconfigure -f noninteractive openssh-server
'"

# Redémarrer les VMs pour appliquer le nouveau hostname
sudo virsh reboot vm3
sudo virsh reboot vm4
sleep 30

# Vérifier les hostnames
ssh debian@IP_VM3 "hostname"
ssh debian@IP_VM4 "hostname"
```

---

## 9. KVM — Snapshot sur vm3

```bash
# Éteindre vm3 avant de créer le snapshot
ssh debian@IP_VM3 "echo 'debianpass' | sudo -S poweroff"
sleep 15

# Créer le snapshot du LV kvm-vm3
sudo lvcreate -s -L 2G -n kvm-vm3-s1 /dev/debian-usb-jth-vg/kvm-vm3

# Vérifier le snapshot
sudo lvs | grep kvm-vm3

# Démarrer vm3 et installer apache2
sudo virsh start vm3
sleep 25
ssh debian@IP_VM3 "echo 'debianpass' | sudo -S apt-get install -y apache2"

# Vérifier qu'apache2 fonctionne
ssh debian@IP_VM3 "sudo systemctl is-active apache2"
ssh debian@IP_VM3 "wget -q -O - http://localhost | grep -o '<title>.*</title>'"

# Éteindre vm3 avant de revenir au snapshot
ssh debian@IP_VM3 "echo 'debianpass' | sudo -S poweroff"
sleep 15

# Revenir à l'état avant l'installation d'apache2 (merge du snapshot)
sudo lvconvert --merge /dev/debian-usb-jth-vg/kvm-vm3-s1

# Vérifier que le snapshot a bien été fusionné
sudo lvs | grep kvm-vm3

# Redémarrer vm3 et vérifier qu'apache2 n'est plus là
sudo virsh start vm3
sleep 25
ssh debian@IP_VM3 "dpkg -l apache2 2>/dev/null | grep apache2 || echo 'apache2 absent — snapshot OK'"
```

---

## 10. KVM — Ajouter un nouveau disque à vm4

```bash
# Créer le répertoire pool et le fichier disque de 2G
mkdir -p /home/henochrjt/tmp/pool
sudo qemu-img create -f raw /home/henochrjt/tmp/pool/vol1.img 2G
sudo chown libvirt-qemu:kvm /home/henochrjt/tmp/pool/vol1.img

# Attacher le disque à vm4 (à chaud et de façon persistante)
sudo virsh attach-disk vm4 \
  /home/henochrjt/tmp/pool/vol1.img \
  vdb \
  --driver qemu \
  --subdriver raw \
  --config \
  --live

# Vérifier que le disque est bien attaché
sudo virsh domblklist vm4

# Depuis l'intérieur de vm4 : partitionner vdb, créer PV, étendre VG, créer LV data
ssh debian@IP_VM4 "echo 'debianpass' | sudo -S bash -c '
  # Créer une partition primaire LVM sur vdb
  echo -e \"n\np\n1\n\n\nt\n8e\nw\" | fdisk /dev/vdb
  sleep 1

  # Créer le Physical Volume
  pvcreate /dev/vdb1

  # Étendre le VG avec le nouveau PV
  vgextend vm2-vg /dev/vdb1

  # Créer le LV data de 1.9G
  lvcreate -L 1.9G -n data vm2-vg

  # Formater en ext4
  mkfs.ext4 /dev/vm2-vg/data

  # Monter sur /mnt
  mount /dev/vm2-vg/data /mnt

  # Rendre le montage permanent
  echo \"/dev/vm2-vg/data /mnt ext4 defaults 0 2\" >> /etc/fstab

  # Vérifier
  df -h /mnt
  lvs
'"
```

---

## 11. KVM — Étendre le disque de vm3 (LV hôte + partition interne)

### Côté hôte

```bash
# Éteindre vm3
ssh debian@IP_VM3 "echo 'debianpass' | sudo -S poweroff"
sleep 15

# Étendre le LV de 2G (de 6G à 8G)
sudo lvextend -L +2G /dev/debian-usb-jth-vg/kvm-vm3

# Vérifier
sudo lvs | grep kvm-vm3

# Mapper les partitions du LV pour travailler dessus depuis l'hôte
sudo apt-get install -y kpartx
sudo kpartx -av /dev/debian-usb-jth-vg/kvm-vm3

# Vérifier le filesystem avant modification
sudo e2fsck -fy /dev/mapper/debian--usb--jth--vg-kvm--vm3p1

# Réorganiser la table de partitions :
# Supprimer vda2+vda5 (swap), supprimer vda1, recréer vda1 plus grande, recréer swap
sudo kpartx -d /dev/debian-usb-jth-vg/kvm-vm3
(
echo d; echo 5      # supprimer partition swap logique
echo d; echo 2      # supprimer partition étendue
echo d; echo 1      # supprimer partition root
echo n; echo p; echo 1; echo 2048; echo +7400M  # nouvelle root ~7.4G
echo n; echo e; echo 2; echo ""; echo ""         # nouvelle étendue (reste)
echo n; echo ""; echo ""; echo ""               # nouveau swap logique
echo t; echo 5; echo 82                         # type swap
echo a; echo 1                                  # marquer vda1 comme bootable
echo w
) | sudo fdisk /dev/debian-usb-jth-vg/kvm-vm3

# Remapper et redimensionner le filesystem
sudo kpartx -av /dev/debian-usb-jth-vg/kvm-vm3
sudo e2fsck -fy /dev/mapper/debian--usb--jth--vg-kvm--vm3p1
sudo resize2fs /dev/mapper/debian--usb--jth--vg-kvm--vm3p1
sudo mkswap /dev/mapper/debian--usb--jth--vg-kvm--vm3p5
sudo kpartx -d /dev/debian-usb-jth-vg/kvm-vm3
```

### Vérification dans vm3

```bash
# Démarrer vm3
sudo virsh start vm3
sleep 30

# Vérifier la nouvelle taille
ssh debian@IP_VM3 "lsblk && df -h /"
# Attendu : vda = 8G, vda1 = ~7.2G, / = ~7.1G utilisable
```

---

## 12. KVM — Étendre le disque de vm4 (LV hôte + LVM interne)

### Côté hôte

```bash
# Éteindre vm4
ssh debian@IP_VM4 "echo 'debianpass' | sudo -S poweroff"
sleep 15

# Étendre le LV de 2G (de 6G à 8G)
sudo lvextend -L +2G /dev/debian-usb-jth-vg/kvm-vm4

# Vérifier
sudo lvs | grep kvm-vm4

# Redémarrer vm4
sudo virsh start vm4
sleep 35
sudo virsh domifaddr vm4
```

### Côté vm4 (depuis l'intérieur)

```bash
# Se connecter à vm4
ssh debian@IP_VM4

# Vérifier que le disque fait bien 8G
sudo lsblk /dev/vda

# Créer une nouvelle partition primaire vda3 dans les 2G libres
(
echo n; echo p; echo 3; echo ""; echo ""
echo t; echo 3; echo 8e
echo w
) | sudo fdisk /dev/vda

# Actualiser la table de partition
sudo partx -u /dev/vda

# Créer le Physical Volume sur vda3
sudo pvcreate /dev/vda3

# Étendre le VG avec le nouveau PV
sudo vgextend vm2-vg /dev/vda3

# Étendre le LV root avec tout l'espace libre
sudo lvextend -l +100%FREE /dev/vm2-vg/root

# Redimensionner le filesystem en ligne (sans reboot)
sudo resize2fs /dev/vm2-vg/root

# Vérifier le résultat
df -h /
sudo vgs
sudo lvs vm2-vg
# Attendu : / = ~6.4G, VG utilise 2 PVs (vda5 + vda3)
```

---

## Résumé des VMs créées

| VM   | Stockage                                    | Base   | LV hôte étendu |
|------|---------------------------------------------|--------|-----------------|
| vm1  | `/home/henochrjt/vms/vm1.raw` (raw 6G)     | install| non             |
| vm2  | `/home/henochrjt/vms/vm2.raw` (raw 6G)     | install| non             |
| vm1b | `/home/henochrjt/vms/vm1b.raw` (raw 6G)    | clone vm1 | non          |
| vm3  | `/dev/debian-usb-jth-vg/kvm-vm3` (LV 8G)  | clone vm1 | oui → 8G      |
| vm4  | `/dev/debian-usb-jth-vg/kvm-vm4` (LV 8G)  | clone vm2 | oui → 8G      |

## Commandes virsh utiles

```bash
sudo virsh list --all              # lister toutes les VMs
sudo virsh start <vm>              # démarrer une VM
sudo virsh shutdown <vm>           # arrêt propre
sudo virsh destroy <vm>            # forcer l'arrêt
sudo virsh domifaddr <vm>          # voir l'adresse IP
sudo virsh domblklist <vm>         # lister les disques
sudo virsh console <vm>            # accéder à la console texte (après config GRUB)
sudo virsh undefine <vm>           # supprimer la définition d'une VM
```
