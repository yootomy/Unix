# Examen blanc — Virtualisation (entraînement L12)

> **Module :** Systèmes d'exploitation de type Unix | **Périmètre :** L6 → L10
> **Durée recommandée :** 2 h (sur les ≈ 4 h du test, le reste étant pour la partie shell)
> **Barème :** 100 pts + 10 pts bonus | **Documents :** notes de révision autorisées
> **Hors sujet :** Incus, Terraform/Ansible, DNS/DHCP serveur, LDAP/Kerberos (matières L11+)

---

## Matériel de départ

Le prof t'a fourni deux VMs de référence pré-installées (Debian 13, 2 Go RAM, 2 vCPU, virtio, raccordées au réseau libvirt `default`) :

```
/home/henochrjt/Documents/usb-copies/f8cdaa79-887f-463d-9355-e13b955c013f/vmref/
├── kvmRef1.qcow2  + kvmRef1.xml   (format qcow2, supporte les snapshots fichier)
└── kvmRef2.img    + kvmRef2.xml   (format raw, plus rapide)
```

> **CONSIGNE STRICTE :** Tu ne **modifies jamais** les fichiers d'origine du dossier `vmref/`. Toutes les manipulations se font sur des **copies** (clones, conversions vers LV, snapshots, etc.). Si tu te trompes, tu dois pouvoir tout recommencer depuis le matériel de référence intact.

---

## Scénario fil-rouge

Tu vas, à partir des deux images de référence, monter une infrastructure à 3 VMs (`vmA`, `vmB`, `vmC`) avec deux réseaux libvirt (`default` NAT et `net-test` 10.10.10.0/24), où `vmC` joue le rôle de passerelle entre les deux. Tu testeras la connectivité SSH (simple, jump, tunnel) et l'extension d'un disque LVM côté invité.

```
   ┌──────┐        ┌──────┐                       ┌──────┐
   │ hôte │        │ vmA  │                       │ vmC  │
   └──┬───┘        └──┬───┘                       └──┬───┘
   .1 │           .??? │                       .254  │
══════╪═══════════════╪═══════════════════════════════╪═══════
              default  ─  virbr0  ─  192.168.122.0/24  (NAT)


                                   ┌──────┐        ┌──────┐
                                   │ vmC  │        │ vmB  │
   ┌──────┐                        └──┬───┘        └──┬───┘
   │ hôte │                       .2  │           .?? │
   └──┬───┘                           │               │
   .1 │                               │               │
══════╪═══════════════════════════════╪═══════════════╪═══════
            net-test  ─  virbr20  ─  10.10.10.0/24  (isolé)

   vmC = passerelle entre les deux réseaux  (ip_forward = 1)
```

---

## Partie A — Préparation et import (10 pts)

**A.1** (3 pts) Tu veux importer `kvmRef1.qcow2` dans libvirt sans modifier l'original. Donne la commande qui copie l'image vers le pool de stockage `default` (typiquement `/var/lib/libvirt/images/`) sous le nom `vmA.qcow2`. Justifie pourquoi tu copies plutôt que de définir directement la VM sur le fichier d'origine.

**A.2** (3 pts) Tu veux maintenant ajouter cette VM à libvirt. Donne les deux commandes successives :
1. Adapter le XML de référence (en supposant que `kvmRef1.xml` existe déjà) → produire `vmA.xml`.
2. Inscrire la VM dans libvirt sans la démarrer.



Indique précisément les **trois champs au minimum** à modifier dans le XML pour éviter les conflits avec la VM d'origine.

**A.3** (2 pts) Donne les commandes pour :
1. Lister toutes les VMs (démarrées et arrêtées).

```
virsh -c qemu:///system list --all
```

1. Démarrer `vmA`.

```
virsh -c qemu:///system start VmA
```


2. Ouvrir la console série de `vmA`.

```
virsh -c qemu:///system console VmA
```


**A.4** (2 pts) Une fois en console, tu dois quitter `virsh console`. Quelle séquence de touches ?

Ctrl +  ALT + ]

---

## Partie B — Clonage et stockage LVM (25 pts)

**B.1** (5 pts) Tu veux **cloner `kvmRef2.img` (raw) vers un volume logique** `/dev/vg/vmB` du groupe de volume `vg` de l'hôte. Donne dans l'ordre :
1. La commande pour créer le LV de 6 Go.
2. La commande pour copier les données du fichier raw vers le LV.
3. Les modifications à apporter à un XML de définition pour que la VM `vmB` utilise ce LV comme disque (montre la balise `<disk>` complète).

**B.2** (4 pts) Une fois `vmB` clonée et démarrée, comment vérifies-tu côté **hôte** que l'image LVM est bien utilisée par la VM ? Donne deux commandes différentes (l'une côté libvirt, l'autre côté LVM).

**B.3** (5 pts) Tu veux **étendre la LV `/dev/vg/vmB` de +2 G** pour donner plus d'espace à la VM. Détaille la procédure complète (en supposant que la VM utilise une partition ext4 directe, pas de LVM-in-guest). Précise impérativement à quel moment la VM doit être **arrêtée** vs **démarrée**.

**B.4** (5 pts) **Snapshot LVM**. Avant une opération risquée dans `vmB`, tu veux faire un snapshot. Donne :
1. La commande pour créer le snapshot `vmB-s1` de 1 Go (sur la LV `/dev/vg/vmB`).
2. La commande pour fusionner le snapshot dans la LV d'origine après validation.
3. Le piège classique : à quel moment `vmB` doit-elle être arrêtée pour que la fusion soit appliquée ?

**B.5** (6 pts) Tu veux **ajouter un disque secondaire** de 2 Go à `vmB` (sans LVM in-guest), pour stocker des données. Donne la séquence complète :
1. Créer un nouveau LV `/dev/vg/vmB-data` de 2 Go côté hôte.
2. Attacher ce disque à `vmB` à chaud (sans redémarrer).
3. Côté invité : formater en ext4, créer un point de montage `/srv/data`, monter, vérifier.
4. Quelle ligne ajouter dans `/etc/fstab` pour rendre le montage persistant ?

---

## Partie C — Réseau libvirt et IPs fixes (25 pts)

**C.1** (4 pts) Donne le contenu **complet** d'un fichier `net-test.xml` qui définit un réseau libvirt isolé (sans NAT, sans forward) avec :
- nom `net-test`
- bridge `virbr20`
- IP de la passerelle `10.10.10.1/24`
- DHCP qui distribue de `10.10.10.128` à `10.10.10.254`

**C.2** (3 pts) Donne les trois commandes successives pour :
1. Inscrire ce réseau dans libvirt à partir du XML.
2. Activer son démarrage automatique au boot.
3. Le démarrer maintenant.

**C.3** (4 pts) Tu dois créer une **3ᵉ VM `vmC`** clonée depuis `kvmRef1.qcow2` (comme pour `vmA`), mais raccordée aux **deux réseaux** (`default` ET `net-test`). À quoi ressemble le bloc XML complet pour ses deux interfaces ? (Adresses MAC fictives à choisir, mais cohérentes.)

**C.4** (5 pts) Après avoir démarré les trois VMs, tu veux **fixer les adresses IP** suivantes par réservation DHCP :
- `vmC` sur `default` → `192.168.122.254`
- `vmC` sur `net-test` → `10.10.10.2`

Explique la procédure, et donne le bloc `<host>` à ajouter dans chacun des deux réseaux, en réutilisant les adresses MAC du XML de la question C.3.

**C.5** (3 pts) Quelle commande exécutes-tu pour **éditer** le XML d'un réseau libvirt qui tourne déjà ? Et que faut-il faire après modification pour que les nouvelles réservations s'appliquent ?

**C.6** (3 pts) Une fois les trois VMs redémarrées, tu veux vérifier depuis l'hôte les IPs effectives. Donne deux commandes différentes (l'une côté libvirt, l'autre côté hôte).

**C.7** (3 pts) Sur les VMs Debian-12-nocloud du prof, comment s'appellent les interfaces réseau ? (Donne les **deux** noms typiquement vus dans les solutions du cours, et précise lequel correspond à quel slot PCI.)

---

## Partie D — SSH multi-saut (20 pts)

**D.1** (3 pts) Depuis l'hôte, tu te connectes en SSH à `vmA` avec l'utilisateur `debian`. Donne la commande. Que se passe-t-il à la **première** connexion concernant les host keys ? (Réponse en une phrase.)

**D.2** (4 pts) Tu veux configurer la **connexion SSH sans mot de passe** depuis `vmA` (utilisateur `debian`) vers `vmC` (utilisateur `debian`). Donne la séquence de commandes à exécuter côté `vmA`. Si l'authentification par mot de passe est désactivée sur `vmC`, comment fais-tu ?

**D.3** (5 pts) Depuis l'hôte, tu veux te connecter à `vmB` (qui n'est pas joignable directement parce qu'elle est sur `net-test`) en passant par `vmC` comme **jump host**. Donne la commande SSH (option `-J`). Dans quel ordre les mots de passe sont-ils demandés (avant clé publique) ?

**D.4** (5 pts) Tu veux créer un **tunnel SSH** depuis `vmA` qui rend `vmB` (10.10.10.199:22) accessible localement sur `vmA:2222`, à travers `vmC`. Donne :
1. La commande qui ouvre le tunnel (en arrière-plan).
2. La commande pour s'y connecter ensuite.
3. La commande pour arrêter le tunnel proprement.

**D.5** (3 pts) Après avoir cloné une VM, tu te connectes en SSH et tu obtiens `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!`. Quelle est la cause exacte côté serveur ? Quelle est la procédure correcte côté **serveur** (la nouvelle VM clonée) pour résoudre proprement ?

---

## Partie E — Passerelle et débogage (20 pts)

**E.1** (4 pts) Tu veux activer le **forwarding IPv4** sur `vmC` de manière **permanente** (survie au reboot). Donne :
1. La commande qui active immédiatement le forwarding (sans toucher aux fichiers).
2. La modification de configuration permanente (fichier + ligne exacte).
3. La commande pour appliquer cette configuration sans rebooter.

**E.2** (5 pts) Sur `vmA` (Debian-12-nocloud, qui utilise **netplan**), tu veux ajouter une **route persistante** pour que `10.10.10.0/24` passe via `vmC` (`192.168.122.254`). Donne le bloc YAML à ajouter dans `/etc/netplan/90-default.yaml`, sous la rubrique `all-en`. Quelle commande appliques-tu ensuite ?

**E.3** (3 pts) Même question pour `vmB` : ajoute la route vers `192.168.122.0/24` via `vmC` (`10.10.10.2`). Bloc YAML uniquement.

**E.4** (4 pts) Pour vérifier que la passerelle fonctionne, tu fais depuis `vmA` :
```
ping -c 4 10.10.10.199
```
Ça ne répond pas. Liste **trois** causes possibles (par ordre de probabilité), avec pour chacune la commande de diagnostic à lancer depuis `vmA`, `vmB` ou `vmC`.

**E.5** (4 pts) **Cas de débogage.** Après avoir cloné `vmC` depuis `kvmRef1`, tu te connectes en console et tu lances :
```
ip a
```
Tu n'as **aucune adresse IP** sur `enp1s0`. Cite **deux causes** possibles courantes (on parle de VMs Debian-nocloud, netplan en place) et la commande de diagnostic associée pour chacune.

---

## Bonus — Stockage avancé (10 pts hors barème)

**Bonus.1** (5 pts) Sur `vmB` (qui utilise LVM-in-guest, supposons que le VG s'appelle `vmLvm-vg` et la racine `/dev/vmLvm-vg/root`), tu veux **étendre la racine** de +1 Go en ajoutant un nouveau PV via un disque virtuel ajouté à chaud. Détaille la séquence complète (côté hôte + côté invité).

**Bonus.2** (5 pts) Sur la même VM, tu veux créer un nouveau LV `data` de 500 Mo dans `vmLvm-vg`, le formater en ext4 et le monter persistant sur `/srv/data`. Donne les commandes (côté invité uniquement).

---

## Auto-évaluation

| Partie                    | Points    | Ton score |
| ------------------------- | --------- | --------- |
| A — Préparation           | / 10      |           |
| B — Clonage + LVM         | / 25      |           |
| C — Réseau libvirt        | / 25      |           |
| D — SSH multi-saut        | / 20      |           |
| E — Passerelle + débogage | / 20      |           |
| **Total**                 | **/ 100** |           |
| Bonus                     | / 10      |           |

> Seuil de réussite : ≥ 60 / 100. Si tu vises l'aisance pour le test : ≥ 80.

---

<!-- ⚠️ Éléments de solution ci-dessous — ne consulter qu'après avoir tenté chaque question. -->

---

# ÉLÉMENTS DE SOLUTION

## Partie A

**A.1** (3 pts)
```bash
sudo cp /home/henochrjt/Documents/usb-copies/f8cdaa79-887f-463d-9355-e13b955c013f/vmref/kvmRef1.qcow2 \
        /var/lib/libvirt/images/vmA.qcow2
```
On copie pour deux raisons : (1) l'original sur la clé USB ne doit jamais être modifié (consigne du prof) ; (2) une VM démarrée écrit dans son disque, donc utiliser l'image de référence directement la corromprait.

**A.2** (3 pts)
```bash
cp kvmRef1.xml vmA.xml
# éditer vmA.xml :
#   <name>vmA</name>                            ← nom unique
#   <uuid>...</uuid>                            ← supprimer la ligne (libvirt en générera un)
#   <source file='/var/lib/libvirt/images/vmA.qcow2'/>   ← chemin du nouveau disque
#   <mac address='...'/>                        ← supprimer pour qu'une nouvelle MAC soit tirée
sudo virsh define vmA.xml
```
Champs minimum à modifier : **`<name>`**, **`<source file=...>`** (chemin du disque), et il faut **supprimer `<uuid>` et `<mac address>`** sinon libvirt refuse à cause de doublons.

**A.3** (2 pts)
```bash
sudo virsh list --all
sudo virsh start vmA
sudo virsh console vmA
```

**A.4** (2 pts) `Ctrl + ]` (l'invite l'indique : « Escape character is ^] »).

---

## Partie B

**B.1** (5 pts)
```bash
sudo lvcreate -n vmB -L 6G vg
sudo dd if=/path/vers/copie/de/kvmRef2.img of=/dev/vg/vmB bs=4M status=progress
# (ou : sudo qemu-img convert -O raw kvmRef2.img /dev/vg/vmB)
```
Bloc XML pour vmB :
```xml
<disk type='block' device='disk'>
  <driver name='qemu' type='raw' cache='none' io='native' discard='unmap'/>
  <source dev='/dev/vg/vmB'/>
  <target dev='vda' bus='virtio'/>
</disk>
```
Note : `type='block'` (pas `'file'`) et `<source dev=...>` (pas `<source file=...>`).

**B.2** (4 pts)
```bash
sudo virsh domblklist vmB          # côté libvirt : montre les disques attachés à vmB
sudo lvdisplay /dev/vg/vmB         # côté LVM : confirme l'existence du LV
# (variante : sudo lsblk /dev/vg/vmB)
```

**B.3** (5 pts)
```bash
# 1. Arrêter la VM (impératif pour éviter la corruption ext4)
sudo virsh destroy vmB     # ou shutdown propre depuis l'invité

# 2. Étendre le LV côté hôte
sudo lvextend -L +2G /dev/vg/vmB

# 3. Redémarrer la VM
sudo virsh start vmB
sudo virsh console vmB

# 4. Côté invité, redimensionner la partition puis le système de fichiers
#    (en supposant qu'il n'y a qu'une partition vda1 ext4, sans LVM in-guest)
sudo growpart /dev/vda 1
sudo resize2fs /dev/vda1
df -h /
```
> Piège : si la VM utilise des partitions classiques (pas LVM in-guest), il faut **growpart** (ou `fdisk` en supprimant/recréant la partition à la même position) AVANT `resize2fs`.

**B.4** (5 pts)
```bash
# 1. Créer le snapshot (la VM peut tourner pour LVM, mais arrêt recommandé pour cohérence ext4)
sudo virsh destroy vmB
sudo lvcreate -s /dev/vg/vmB -L 1G -n vmB-s1

# 2. Travailler dans la VM, tester ; si on veut garder l'état pré-snapshot :
sudo virsh destroy vmB
sudo lvconvert --merge /dev/vg/vmB-s1
sudo virsh start vmB
```
> Piège : `lvconvert --merge` exige que la LV d'origine **ne soit pas montée/utilisée**. La VM doit donc être **arrêtée** au moment de la fusion. Si elle tourne, la fusion sera planifiée pour le prochain démontage.

**B.5** (6 pts)
```bash
# Côté hôte
sudo lvcreate -n vmB-data -L 2G vg
sudo virsh attach-disk vmB /dev/vg/vmB-data vdb \
     --driver qemu --type disk --subdriver raw --persistent

# Côté invité (vmB)
sudo mkfs.ext4 /dev/vdb
sudo mkdir -p /srv/data
sudo mount /dev/vdb /srv/data
df -h /srv/data
```
Ligne `/etc/fstab` :
```
/dev/vdb  /srv/data  ext4  defaults  0  2
```
> Mieux : utiliser un UUID (`blkid /dev/vdb`) plutôt que `/dev/vdb`, car les noms `vdX` peuvent changer si on réorganise les disques.

---

## Partie C

**C.1** (4 pts)
```xml
<network>
  <name>net-test</name>
  <bridge name='virbr20' stp='on' delay='0'/>
  <ip address='10.10.10.1' netmask='255.255.255.0'>
    <dhcp>
      <range start='10.10.10.128' end='10.10.10.254'/>
    </dhcp>
  </ip>
</network>
```
> Pas de `<forward mode='nat'/>` : c'est ce qui rend le réseau **isolé** (pas d'accès extérieur).

**C.2** (3 pts)
```bash
sudo virsh net-define net-test.xml
sudo virsh net-autostart net-test
sudo virsh net-start net-test
```

**C.3** (4 pts)
```xml
<interface type='network'>
  <mac address='52:54:00:aa:bb:01'/>
  <source network='default'/>
  <model type='virtio'/>
</interface>
<interface type='network'>
  <mac address='52:54:00:aa:bb:02'/>
  <source network='net-test'/>
  <model type='virtio'/>
</interface>
```
> Les MAC commencent par `52:54:00` (préfixe attribué à QEMU). Elles doivent être uniques sur l'hôte.

**C.4** (5 pts)
1. Arrêter la VM ou laisser tourner (les modifs prennent effet au prochain DHCP).
2. `sudo virsh net-edit default` puis dans le bloc `<dhcp>`, ajouter :
   ```xml
   <host mac='52:54:00:aa:bb:01' name='vmC' ip='192.168.122.254'/>
   ```
3. `sudo virsh net-edit net-test` puis :
   ```xml
   <host mac='52:54:00:aa:bb:02' name='vmC' ip='10.10.10.2'/>
   ```
4. Pour que les nouvelles réservations s'appliquent : `sudo virsh net-destroy <réseau> && sudo virsh net-start <réseau>` (ou redémarrer la VM pour forcer un nouveau bail DHCP).

**C.5** (3 pts)
```bash
sudo virsh net-edit default
```
Après modification : il faut **redémarrer le réseau** (`net-destroy` + `net-start`) — `net-edit` seul met à jour la config persistante mais pas le réseau actif. Il faut aussi forcer un nouveau bail DHCP sur la VM (reboot ou `dhclient -r && dhclient`).

**C.6** (3 pts)
```bash
sudo virsh domifaddr vmC                        # côté libvirt
sudo virsh net-dhcp-leases default              # côté libvirt, vue des baux
ip neigh                                         # côté hôte (table ARP)
```

**C.7** (3 pts) Les interfaces **n'ont plus le préfixe `eth0`/`ens3`** sur Debian-12-nocloud avec systemd-udev v249+ : elles sont nommées d'après leur **slot PCI**. Exemples concrets vus dans les solutions du prof :
- `enp1s0` → premier NIC virtio, sur le bus PCI 0x01
- `enp7s0` → deuxième NIC virtio, sur le bus PCI 0x07

> C'est pour ça que netplan utilise un **match par glob** : `match: { name: en* }`.

---

## Partie D

**D.1** (3 pts)
```bash
ssh debian@<ip_de_vmA>
```
À la première connexion, la **clé d'hôte** (host key) du serveur est inconnue : SSH demande une confirmation interactive (`yes`) et l'enregistre dans `~/.ssh/known_hosts`.

**D.2** (4 pts) Sur `vmA` :
```bash
ssh-keygen                                # accepter les valeurs par défaut
ssh-copy-id debian@192.168.122.254        # copie ~/.ssh/id_rsa.pub vers vmC:~/.ssh/authorized_keys
ssh debian@192.168.122.254                # doit se connecter sans mot de passe
```
Si l'authentification par mot de passe est **désactivée** sur vmC (PasswordAuthentication no) :
```bash
# Sur vmA : envoyer la clé publique à l'admin via un canal hors SSH (mail, scp via un autre user qui peut, USB...)
scp ~/.ssh/id_rsa.pub admin@vmC:/tmp/cle_debian_vmA.pub
# Sur vmC (en root ou via l'admin)
cat /tmp/cle_debian_vmA.pub >> /home/debian/.ssh/authorized_keys
chown debian:debian /home/debian/.ssh/authorized_keys
chmod 600 /home/debian/.ssh/authorized_keys
```

**D.3** (5 pts)
```bash
ssh -J debian@192.168.122.254 debian@10.10.10.199
```
Ordre des mots de passe :
1. d'abord **vmC** (le jump) : `debian@192.168.122.254's password:`
2. ensuite **vmB** (la cible) : `debian@10.10.10.199's password:`

> Si la clé est posée vmA → vmC (D.2), seul le mot de passe de vmB est demandé.

**D.4** (5 pts)
```bash
# 1. Ouvrir le tunnel en arrière-plan
ssh -f -N -L 2222:10.10.10.199:22 debian@192.168.122.254
#   -f = passe en arrière-plan après auth, -N = pas de commande exécutée

# 2. Se connecter via le tunnel (depuis vmA)
ssh -p 2222 debian@localhost

# 3. Arrêter le tunnel
jobs                       # repérer le job number
kill %1                    # ou : pkill -f "ssh.*-L 2222"
```

**D.5** (3 pts) Après clonage, la VM clonée a hérité des **clés d'hôte SSH** de la VM d'origine, donc deux machines présentent la même empreinte → SSH alerte. Côté serveur (la nouvelle VM clonée) :
```bash
sudo rm /etc/ssh/ssh_host_*
sudo dpkg-reconfigure openssh-server
# alternative : sudo ssh-keygen -A
sudo systemctl restart ssh
```
Côté client (qui se reconnecte) : `ssh-keygen -R <ip_ou_nom>` pour purger l'ancienne entrée de `known_hosts`.

---

## Partie E

**E.1** (4 pts)
```bash
# 1. Activation immédiate (volatile)
sudo sysctl -w net.ipv4.ip_forward=1
# alternative : echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward

# 2. Permanent : éditer /etc/sysctl.conf (ou un fichier dans /etc/sysctl.d/)
#    Ajouter / décommenter :
net.ipv4.ip_forward=1

# 3. Recharger sans rebooter
sudo sysctl -p
```

**E.2** (5 pts)
```yaml
network:
    version: 2
    ethernets:
        all-en:
            match:
                name: en*
            dhcp4: true
            dhcp4-overrides:
                use-domains: true
            dhcp6: true
            dhcp6-overrides:
                use-domains: true
            routes:
              - to: 10.10.10.0/24
                via: 192.168.122.254
```
Application :
```bash
sudo netplan apply
```
> Indenter avec **4 espaces** sous `all-en:` est important — netplan est strict. Vérifier avec `netplan status` ou `ip route`.

**E.3** (3 pts)
```yaml
        all-en:
            match:
                name: en*
            dhcp4: true
            dhcp4-overrides:
                use-domains: true
            dhcp6: true
            dhcp6-overrides:
                use-domains: true
            routes:
              - to: 192.168.122.0/24
                via: 10.10.10.2
```

**E.4** (4 pts) Trois causes par ordre de probabilité :

| # | Cause | Diagnostic |
|---|---|---|
| 1 | **Forwarding IP non activé sur vmC** | sur vmC : `cat /proc/sys/net/ipv4/ip_forward` → doit valoir `1` |
| 2 | **Route inverse manquante sur vmB** : vmB ne sait pas comment renvoyer la réponse vers `192.168.122.0/24` | sur vmB : `ip route` → cherche `192.168.122.0/24 via 10.10.10.2` |
| 3 | **Route absente sur vmA** : vmA ne sait pas atteindre `10.10.10.0/24` | sur vmA : `ip route` → cherche `10.10.10.0/24 via 192.168.122.254` |

> Outils complémentaires : `traceroute 10.10.10.199` depuis vmA (montre où ça s'arrête), `tcpdump -nni enp7s0 icmp` sur vmC (voit les paquets ICMP transiter ou non).

**E.5** (4 pts)

| Cause | Diagnostic |
|---|---|
| **Le clone a les mêmes adresses MAC que la VM d'origine** : conflit DHCP, ou DHCP refuse de baillir deux fois la même IP | `ip link show enp1s0` (voir la MAC) puis comparer avec la MAC de la VM source |
| **Netplan n'a pas été appliqué** ou la conf est invalide | `sudo netplan status` ou `sudo netplan generate` (affiche les erreurs YAML) |

> Bonus de débogage : `journalctl -u systemd-networkd` montre les échecs DHCP. Solution typique pour MAC dupliquée : éditer le XML de la VM clonée (`virsh edit vmC`) et changer la MAC manuellement, ou supprimer la ligne `<mac>` pour que libvirt en tire une nouvelle.

---

## Bonus

**Bonus.1** (5 pts)
```bash
# Côté hôte : créer et attacher un nouveau disque virtio
sudo lvcreate -n vmB-extra -L 1G vg
sudo virsh attach-disk vmB /dev/vg/vmB-extra vdb \
     --driver qemu --type disk --subdriver raw --persistent

# Côté invité (vmB)
sudo pvcreate /dev/vdb
sudo vgextend vmLvm-vg /dev/vdb
sudo lvextend -L +1G /dev/vmLvm-vg/root
sudo resize2fs /dev/vmLvm-vg/root
df -h /
```

**Bonus.2** (5 pts)
```bash
sudo lvcreate -n data -L 500M vmLvm-vg
sudo mkfs.ext4 /dev/vmLvm-vg/data
sudo mkdir -p /srv/data
sudo mount /dev/vmLvm-vg/data /srv/data

# /etc/fstab (récupérer l'UUID avec : sudo blkid /dev/vmLvm-vg/data)
echo "UUID=<uuid_obtenu>  /srv/data  ext4  defaults  0  2" | sudo tee -a /etc/fstab
sudo mount -a   # test sans reboot
```

---

## Pièges récurrents repérés dans le cours

1. **Cloner un .qcow2 avec `cp`** → la VM clonée et l'original ont le même UUID interne ; toujours utiliser `qemu-img convert` pour casser la chaîne, ou modifier l'UUID après coup.
2. **Oublier de supprimer la ligne `<mac>`** dans le XML cloné → conflit DHCP et IP qui ne s'affecte pas.
3. **`virsh net-edit`** modifie la config persistante mais **pas** le réseau actif : il faut `net-destroy` + `net-start` pour que les nouvelles réservations DHCP soient prises en compte.
4. **`echo 1 > /proc/sys/net/ipv4/ip_forward`** est **volatile** : perdu au reboot. Toujours le mettre dans `/etc/sysctl.conf` (ou `/etc/sysctl.d/99-forward.conf`) en plus.
5. **Routes ajoutées avec `ip route add`** : non persistantes. Sur Debian-nocloud, passer par **netplan** (`routes:` sous l'ethernet) ou par `post-up` dans `/etc/network/interfaces` selon la distro.
6. **`lvconvert --merge` sur une LV en cours d'utilisation** : la fusion est différée jusqu'au prochain démontage. Toujours `virsh destroy vm` AVANT.
7. **Interfaces `enp1s0` / `enp7s0`** (pas `eth0`/`ens3`) : c'est le naming systemd-udev par slot PCI. Le netplan du cours utilise `match: { name: en* }` pour s'en abstraire.
8. **Clés d'hôte SSH identiques après clonage** → régénérer côté serveur cloné via `dpkg-reconfigure openssh-server` ou `ssh-keygen -A`.
9. **`virsh console`** : sortir avec `Ctrl + ]`, et l'activation du tty série dans la VM passe par `console=ttyS0,115200n8` dans GRUB (déjà fait sur les images cloud Debian).
10. **Pool de stockage** : par défaut `/var/lib/libvirt/images/` (pool `default`). Quand on travaille en LV, on peut définir un pool LVM dédié (`virsh pool-define-as lvm logical ...`) pour que `vol-create-as` y crée automatiquement les LV.
