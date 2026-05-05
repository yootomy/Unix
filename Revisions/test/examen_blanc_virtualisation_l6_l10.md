# Examen blanc - Virtualisation KVM/libvirt L6-L10

> **Module :** Systèmes d'exploitation de type Unix  
> **Durée conseillée :** 3h00  
> **Barème :** 100 points  
> **But :** refaire un parcours pratique complet sur KVM, libvirt, LVM, snapshots, réseaux virtuels et SSH.

---

## Règles de sécurité

- Travaillez uniquement avec des objets jetables dont le nom commence par `rev-`.
- Avant toute commande qui arrête, modifie ou supprime une VM, un disque, un LV ou un réseau, vérifiez le nom de l'objet.
- Ne modifiez aucun domaine libvirt, volume logique, image disque ou réseau qui ne fait pas partie de cet examen blanc.
- Si votre machine ne dispose pas de KVM, d'une ISO Debian ou d'un volume group LVM, écrivez les commandes exactes que vous auriez exécutées et expliquez ce qui manque.
- Remplacez les placeholders par vos valeurs réelles : `<ISO_DEBIAN>`, `<VG>`, `<USER_VM>`, `<IP_VM1>`, `<IP_VM2>`, `<IP_VM3>`, `<INTERFACE>`.

---

## À rendre pour s'auto-corriger

Créez un dossier de travail :

```bash
mkdir -p ~/revision-virt/{images,xml,logs}
```

Pendant l'exercice, gardez les traces utiles dans `~/revision-virt/logs/rapport.md` :

- commandes principales exécutées ;
- sorties de vérification : `virsh list --all`, `virsh net-list --all`, `virsh domifaddr`, `lsblk`, `df -h`, `ip a`, `ip route` ;
- captures de résultats SSH : connexion directe, jump, tunnel, connexion sans mot de passe.

---

## Partie 1 - Questions courtes (15 pts)

Répondez brièvement, mais avec les mots techniques corrects.

**1.1** (3 pts) Expliquez le rôle de chacun :

- KVM
- QEMU
- libvirt
- `virt-install`
- `virsh`

**1.2** (2 pts) Quelle différence faites-vous entre une machine virtuelle, un conteneur et un hyperviseur ?

**1.3** (2 pts) Quelle différence pratique y a-t-il entre un disque virtuel `raw` et un disque `qcow2` ? Donnez un avantage et un inconvénient du format `raw`.

**1.4** (3 pts) Expliquez la différence entre :

- le réseau libvirt `default` ;
- un réseau virtuel isolé ;
- un pont réseau vers le réseau physique.

**1.5** (2 pts) Pourquoi faut-il parfois configurer une console série dans une VM KVM ? Quelle différence avec un accès SSH ?

**1.6** (3 pts) Expliquez les notions LVM suivantes :

- PV
- VG
- LV
- snapshot LVM

---

## Partie 2 - Préparation et création des VM (20 pts)

Objectif : créer deux VM Debian jetables :

- `rev-vm1` : Debian avec disque `raw` de 6G, partitionnement simple ;
- `rev-vm2` : Debian avec disque `raw` de 6G, partitionnement avec LVM dans la VM.

### 2.1 - Préparer l'environnement (3 pts)

Dans `~/revision-virt`, préparez les dossiers et un fichier de rapport.

À vérifier :

- votre utilisateur peut administrer libvirt ;
- la connexion `qemu:///system` répond ;
- les commandes KVM/libvirt nécessaires sont présentes.

### 2.2 - Vérifier KVM/libvirt (4 pts)

Écrivez et exécutez les commandes qui permettent de vérifier :

- la présence de la virtualisation CPU ;
- le chargement des modules KVM ;
- l'état du service libvirt ;
- la liste des domaines libvirt.

### 2.3 - Activer le réseau `default` (4 pts)

Avec `virsh`, affichez les réseaux virtuels, démarrez `default` si nécessaire, puis activez son démarrage automatique.

Résultat attendu :

- `default` est actif ;
- `default` est marqué en autostart.

### 2.4 - Créer `rev-vm1` et `rev-vm2` (7 pts)

Créez les deux VM avec `virt-install` ou `virt-manager`, mais gardez les informations suivantes dans le rapport :

- nom exact des VM ;
- mémoire et CPU choisis ;
- emplacement des disques `raw` ;
- taille des disques ;
- réseau utilisé ;
- type de partitionnement choisi pendant l'installation.

Contraintes :

- disque `raw` de 6G pour chaque VM ;
- carte réseau `virtio` connectée au réseau `default` ;
- Debian installée avec un utilisateur standard `<USER_VM>` ;
- serveur SSH installé ou installable après le premier démarrage.

### 2.5 - Console et accès SSH (2 pts)

Configurez au moins `rev-vm1` pour être accessible avec :

- `virsh console rev-vm1` ;
- `ssh <USER_VM>@<IP_VM1>`.

---

## Partie 3 - Clonage KVM/libvirt et clonage vers LVM (20 pts)

Objectif : cloner `rev-vm1` de deux façons.

### 3.1 - Clonage fichier vers fichier (8 pts)

Clonez `rev-vm1` vers `rev-vm1b`.

Contraintes :

- `rev-vm1` doit être arrêtée avant la copie du disque ;
- exportez la description XML avec `virsh dumpxml` ;
- copiez le disque `raw` ;
- adaptez le XML : nom, disque, UUID et adresse MAC ;
- définissez puis démarrez la nouvelle VM ;
- vérifiez que `rev-vm1` et `rev-vm1b` apparaissent bien comme deux domaines distincts.

### 3.2 - Clonage fichier vers LV (8 pts)

Clonez `rev-vm1` vers `rev-vm3`, mais le stockage de `rev-vm3` doit être un LV de l'hôte.

Contraintes :

- créez un LV nommé `rev-vm3` dans `<VG>` ;
- copiez le contenu du disque de `rev-vm1` vers `/dev/<VG>/rev-vm3` avec `dd` ou `qemu-img convert` ;
- créez une description XML adaptée à un disque bloc ;
- définissez et démarrez `rev-vm3` ;
- vérifiez que le disque de `rev-vm3` est bien un périphérique bloc.

### 3.3 - Post-installation des clones (4 pts)

Sur `rev-vm1b` et `rev-vm3`, corrigez ce qui doit l'être pour éviter les conflits :

- nom d'hôte ;
- adresse IP si elle est statique ;
- clés machine SSH si nécessaire ;
- fichier `/etc/machine-id` si nécessaire.

Expliquez pourquoi cette étape est importante.

---

## Partie 4 - Stockage : extension, snapshot, disque supplémentaire (25 pts)

### 4.1 - Étendre le disque de `rev-vm3` (8 pts)

`rev-vm3` utilise un LV de l'hôte comme disque.

Étendez son disque de 2G.

Résultat attendu :

- le LV de l'hôte gagne 2G ;
- la VM voit le disque agrandi ;
- la partition ou le volume contenant `/` est agrandi ;
- le système de fichiers est agrandi ;
- `df -h` montre l'espace supplémentaire.

### 4.2 - Snapshot LVM et retour arrière (6 pts)

Créez un snapshot LVM de `rev-vm3`, puis :

1. démarrez `rev-vm3` ;
2. installez `apache2` dans la VM ;
3. vérifiez que le service fonctionne ;
4. revenez à l'état précédent grâce au snapshot ;
5. vérifiez qu'`apache2` n'est plus installé ou plus actif.

Expliquez à quel moment la VM doit être arrêtée.

### 4.3 - Ajouter un nouveau disque à `rev-vm2` (5 pts)

Ajoutez un disque `raw` de 1G à `rev-vm2`.

Dans la VM :

- repérez le nouveau disque avec `lsblk` ;
- transformez-le en PV ;
- ajoutez-le au VG existant de `rev-vm2`.

### 4.4 - Créer un LV `data` et le monter (6 pts)

Dans `rev-vm2`, créez un nouveau LV :

- nom : `data` ;
- taille : 500M ;
- système de fichiers : `ext4` ;
- point de montage : `/mnt/data` ;
- montage permanent via `/etc/fstab`.

Résultat attendu :

- `df -Th` affiche `/mnt/data` ;
- `mount -a` ne produit pas d'erreur ;
- après redémarrage, `/mnt/data` est toujours monté.

---

## Partie 5 - Réseau virtuel, passerelle et SSH (20 pts)

Objectif réseau :

```text
rev-vm1 ---- default/NAT ---- rev-vm3 ---- rev-isole ---- rev-vm2
              192.168.122.0/24             10.10.50.0/24
```

- `rev-vm1` est connectée au réseau `default`.
- `rev-vm2` est connectée au réseau isolé `rev-isole`.
- `rev-vm3` est connectée aux deux réseaux et sert de passerelle.

### 5.1 - Créer le réseau isolé `rev-isole` (4 pts)

Avec `virsh`, créez un réseau isolé :

- nom : `rev-isole`;
- adresse du pont libvirt : `10.10.50.1/24`;
- réseau persistant ;
- autostart activé.

### 5.2 - Connecter les interfaces (5 pts)

Configurez les interfaces libvirt pour obtenir :

- `rev-vm1` sur `default` ;
- `rev-vm2` sur `rev-isole` uniquement ;
- `rev-vm3` sur `default` et `rev-isole`.

Dans les VM, configurez les adresses :

- `rev-vm3` côté réseau isolé : `10.10.50.2/24`;
- `rev-vm2` côté réseau isolé : `10.10.50.20/24`;
- `rev-vm1` garde une adresse obtenue sur `default`.

### 5.3 - Configurer `rev-vm3` comme passerelle (4 pts)

Configurez :

- l'activation permanente du routage IPv4 sur `rev-vm3` ;
- la route de `rev-vm2` vers `192.168.122.0/24` via `10.10.50.2` ;
- la route de `rev-vm1` vers `10.10.50.0/24` via l'adresse `default` de `rev-vm3`.

Vérifiez avec `ping`, `ip route` et si disponible `traceroute`.

### 5.4 - SSH direct, jump et tunnel (5 pts)

Installez et démarrez le serveur SSH si nécessaire.

À démontrer :

- `rev-vm1` peut joindre `rev-vm3` en SSH ;
- `rev-vm3` peut joindre `rev-vm2` en SSH ;
- depuis `rev-vm1`, connexion à `rev-vm2` avec un jump SSH par `rev-vm3` ;
- depuis `rev-vm1`, création d'un tunnel local vers le SSH de `rev-vm2` à travers `rev-vm3`.

### 5.5 - SSH sans mot de passe (2 pts)

Configurez une clé SSH pour que `<USER_VM>` sur `rev-vm1` puisse se connecter à `<USER_VM>` sur `rev-vm3` sans saisir de mot de passe.

Vérification attendue :

```bash
ssh -o BatchMode=yes <USER_VM>@<IP_VM3> hostname
```

---

## Fin du sujet

Quand vous avez terminé, votre rapport doit contenir au minimum :

- `virsh list --all`;
- `virsh net-list --all`;
- `virsh domifaddr rev-vm1`, `rev-vm2`, `rev-vm3`;
- `lsblk` et `df -h` dans les VM concernées ;
- les routes réseau ;
- les commandes SSH de vérification.
