# INT_SYS1_NIX — Activités 0700 et 0710

## Table des matières

- [1. Objectif](#1-objectif)
- [2. Topologie du labo](#2-topologie-du-labo)
- [3. État actuel de mes machines](#3-état-actuel-de-mes-machines)
- [4. Vérifications utiles](#4-vérifications-utiles)
- [5. Activité 0700 — SSH, jump et tunnel](#5-activité-0700--ssh-jump-et-tunnel)
- [6. Activité 0710 — Passerelle entre réseaux](#6-activité-0710--passerelle-entre-réseaux)
- [7. Test temporaire fait puis retiré](#7-test-temporaire-fait-puis-retiré)
- [8. Résumé rapide](#8-résumé-rapide)

---

## 1. Objectif

Ce document résume ce qui a été préparé pour les activités `0700` et `0710` du cours `INT_SYS1_NIX`.

Le but est d'avoir :

- `vm1` sur le réseau `default`
- `vm2` sur le réseau `net-isole`
- `vm3` sur les deux réseaux
- `vm3` utilisée comme machine intermédiaire pour :
  - le SSH simple
  - le saut SSH (`jump host`)
  - le tunnel SSH
  - plus tard la passerelle réseau

---

## 2. Topologie du labo

Topologie logique du labo :

```text
default / virbr0    192.168.122.0/24
net-isole / virbr1  10.10.10.0/24

vm1  -> default uniquement
vm2  -> net-isole uniquement
vm3  -> default + net-isole
```

Remarque :

- dans la fiche, le réseau isolé est dessiné comme `virbr10`
- sur ma machine, libvirt l'a créé en `virbr1`
- ce n'est pas gênant ; ce qui compte est le sous-réseau `10.10.10.0/24`

---

## 3. État actuel de mes machines

État observé pendant les vérifications :

- `vm1`
  - interface : `ens3`
  - IP : `192.168.122.179`
  - rôle : machine cliente sur `default`

- `vm2`
  - interface : `ens3`
  - IP : `10.10.10.168`
  - rôle : machine dans le réseau isolé
  - actuellement en DHCP sur `net-isole`

- `vm3`
  - interface `ens3` : `192.168.122.254`
  - interface `ens9` : `10.10.10.2`
  - rôle : machine intermédiaire entre les deux réseaux

Important :

- les noms `eth0` et `eth1` du schéma sont des noms logiques
- dans Debian récent, les noms réels sont ici `ens3` et `ens9`

---

## 4. Vérifications utiles

### Voir les réseaux libvirt

```bash
sudo virsh -c qemu:///system net-list --all
```

Cette commande affiche les réseaux virtuels disponibles comme `default` et `net-isole`.

### Voir les interfaces d'une VM depuis l'hôte

```bash
sudo virsh -c qemu:///system domiflist vm1
sudo virsh -c qemu:///system domiflist vm2
sudo virsh -c qemu:///system domiflist vm3
```

Cette commande permet de vérifier sur quel réseau chaque VM est branchée.

### Voir les adresses IP dans une VM

```bash
ip -br a
ip route
```

`ip -br a` donne une vue courte et claire des interfaces et de leurs IP.  
`ip route` montre les routes utilisées par la machine.

### Tester si SSH répond

```bash
ssh debian@192.168.122.254
ssh debian@10.10.10.168
```

Si la connexion demande un mot de passe, le service SSH répond déjà correctement.

---

## 5. Activité 0700 — SSH, jump et tunnel

### 5.0 Ce qu'il fallait mettre en place avant les tests

Avant de faire les commandes SSH, il fallait d'abord reproduire le schéma du cours.

Concrètement, ce qui a été fait :

#### a. Création du réseau isolé dans `virt-manager`

Dans `QEMU/KVM - Détails de connexion` :

- ouverture de l'onglet `Réseaux virtuels`
- création d'un nouveau réseau nommé `net-isole`
- choix du mode `Isolé`
- IPv4 activé
- réseau configuré en `10.10.10.0/24`
- DHCP activé sur `10.10.10.100` à `10.10.10.200`

Résultat :

- `default` sert pour le réseau `192.168.122.0/24`
- `net-isole` sert pour le réseau `10.10.10.0/24`

#### b. Raccordement des machines virtuelles

Dans les détails des VM :

- `vm1`
  - laissée sur `default`
- `vm2`
  - retirée de `default`
  - branchée sur `net-isole`
- `vm3`
  - gardée sur `default`
  - ajout d'une deuxième carte réseau sur `net-isole`

Résultat vu depuis l'hôte :

- `vm1` : une interface sur `default`
- `vm2` : une interface sur `net-isole`
- `vm3` : deux interfaces, une sur chaque réseau

#### c. Vérification des interfaces depuis l'hôte

Commande utilisée :

```bash
sudo virsh -c qemu:///system domiflist vm1
sudo virsh -c qemu:///system domiflist vm2
sudo virsh -c qemu:///system domiflist vm3
```

Explication :

- `domiflist` affiche les cartes réseau attachées à chaque VM
- cette étape permet de vérifier que le câblage correspond bien au schéma

#### d. Mise en IP de `vm3`

Dans `vm3`, les deux interfaces réelles étaient :

- `ens3` vers `default`
- `ens9` vers `net-isole`

Adresses retenues :

- `ens3` : `192.168.122.254/24`
- `ens9` : `10.10.10.2/24`

Méthode recommandée par le prof :

- ne pas mettre une IP statique directement dans la VM
- laisser `vm3` en DHCP
- faire une réservation DHCP au niveau des réseaux `libvirt`

Cette méthode est plus propre parce que :

- la VM reste simple à configurer
- l'adresse dépend du réseau virtuel
- la même carte réseau reçoit toujours la même IP grâce à sa MAC

### Configuration de `vm3` dans Debian

Dans `vm3`, les interfaces doivent rester en DHCP.

Contenu conseillé pour `/etc/network/interfaces` :

```bash
source /etc/network/interfaces.d/*

auto lo
iface lo inet loopback

allow-hotplug ens3
iface ens3 inet dhcp

allow-hotplug ens9
iface ens9 inet dhcp
```

Explication :

- `ens3` demande une adresse au réseau `default`
- `ens9` demande une adresse au réseau `net-isole`
- ensuite c'est `libvirt` qui décide quelles IP leur attribuer

### Réservation DHCP pour `vm3` sur `default`

Commande :

```bash
sudo virsh -c qemu:///system net-edit default
```

Dans le bloc `<dhcp>`, ajouter :

```xml
<host mac='52:54:00:dc:00:39' name='vm3' ip='192.168.122.254'/>
```

Exemple de bloc :

```xml
<dhcp>
  <range start='192.168.122.2' end='192.168.122.254'/>
  <host mac='52:54:00:dc:00:39' name='vm3' ip='192.168.122.254'/>
</dhcp>
```

Explication :

- `52:54:00:dc:00:39` est la MAC de `vm3` sur `default`
- `192.168.122.254` devient l'IP fixe donnée par DHCP à cette carte

Remarque :

- ici l'adresse `.254` est dans la plage dynamique actuelle
- si on veut éviter tout chevauchement possible, on peut réduire la fin de la plage dynamique avant d'ajouter la réservation

### Réservation DHCP pour `vm3` sur `net-isole`

Commande :

```bash
sudo virsh -c qemu:///system net-edit net-isole
```

Dans le bloc `<dhcp>`, ajouter :

```xml
<host mac='52:54:00:b9:a1:3d' name='vm3' ip='10.10.10.2'/>
```

Exemple de bloc :

```xml
<dhcp>
  <range start='10.10.10.100' end='10.10.10.200'/>
  <host mac='52:54:00:b9:a1:3d' name='vm3' ip='10.10.10.2'/>
</dhcp>
```

Explication :

- `52:54:00:b9:a1:3d` est la MAC de `vm3` sur `net-isole`
- `10.10.10.2` devient l'IP fixe donnée à cette carte
- ici l'adresse est hors de la plage dynamique, ce qui est propre et pratique

Important :

- pas de réservation demandée pour `vm2` dans ce document
- `vm2` peut rester en DHCP sur `net-isole`

### Vérification après réservation DHCP

Dans `vm3` :

```bash
ip -br a
ip route
```

Résultat attendu :

- `ens3` doit recevoir `192.168.122.254`
- `ens9` doit recevoir `10.10.10.2`
- la route par défaut doit passer par `192.168.122.1`

Si l'ancienne adresse est encore présente, on peut renouveler les baux DHCP ou redémarrer la VM :

```bash
sudo reboot
```

Vérification :

```bash
ip -br a
ip route
```

Explication :

- `ip -br a` montre rapidement les interfaces et leurs IP
- `ip route` montre comment la VM envoie ses paquets

#### e. Vérification de `vm2`

`vm2` a bien reçu une IP sur le réseau isolé :

- `10.10.10.168/24`

Commande utilisée :

```bash
ip -br a
ip route
```

À ce stade, le labo était prêt pour faire l'activité `0700`.

### 5.1 Connexion SSH simple

Depuis `vm1`, se connecter à `vm3` :

```bash
ssh debian@192.168.122.254
```

Explication :

- `ssh` lance une connexion SSH
- `debian` est l'utilisateur dans la VM
- `192.168.122.254` est l'adresse de `vm3` côté réseau `default`

Depuis `vm3`, se connecter à `vm2` :

```bash
ssh debian@10.10.10.168
```

Explication :

- ici on vise `vm2` sur le réseau isolé
- cela valide que `vm3` est bien reliée aux deux réseaux

### 5.1.1 Ce que cela prouve

Quand ces deux commandes fonctionnent :

- `vm1 -> vm3` prouve que le réseau `default` fonctionne
- `vm3 -> vm2` prouve que `vm3` voit bien le réseau isolé
- on sait donc que `vm3` peut servir de machine intermédiaire

### 5.2 Saut SSH avec `-J`

Depuis `vm1` :

```bash
ssh -J debian@192.168.122.254 debian@10.10.10.168
```

Explication :

- `-J` veut dire `Jump`
- la connexion passe d'abord par `vm3`
- puis `vm3` ouvre la connexion vers `vm2`

### 5.2.1 Lecture simple de la commande

```bash
ssh -J debian@192.168.122.254 debian@10.10.10.168
```

se lit comme :

- connecte-toi d'abord à `vm3`
- puis, depuis `vm3`, connecte-toi à `vm2`

C'est la méthode la plus simple quand on veut passer par une machine relais.

### 5.3 Tunnel SSH

Depuis `vm1` :

```bash
ssh -N -L 2222:10.10.10.168:22 debian@192.168.122.254
```

Explication :

- `-N` : ne lance pas de shell distant ; la commande ne sert qu'au tunnel
- `-L` : crée un tunnel local
- `2222` : port local sur `vm1`
- `10.10.10.168:22` : destination finale, ici `vm2` sur son port SSH
- `debian@192.168.122.254` : machine tunnel, donc `vm3`

Dans un deuxième terminal sur `vm1` :

```bash
ssh -p 2222 debian@localhost
```

Explication :

- `localhost:2222` redirige vers `vm2:22`
- on se connecte donc à `vm2` en passant par `vm3`

### 5.3.1 Lecture simple du tunnel

La commande :

```bash
ssh -N -L 2222:10.10.10.168:22 debian@192.168.122.254
```

veut dire :

- ouvre une connexion SSH vers `vm3`
- garde-la ouverte
- et redirige le port local `2222` vers le port `22` de `vm2`

Ensuite, quand on écrit :

```bash
ssh -p 2222 debian@localhost
```

on ne se connecte pas vraiment au poste local ; on passe en réalité dans le tunnel et on arrive sur `vm2`.

### 5.4 SSH sans mot de passe de `vm1` vers `vm3`

Depuis `vm1` :

```bash
ssh-keygen
ssh-copy-id debian@192.168.122.254
```

Explication :

- `ssh-keygen` crée une paire de clés
- `ssh-copy-id` installe la clé publique sur `vm3`
- ensuite `vm1` peut se connecter à `vm3` sans taper le mot de passe

Test :

```bash
ssh debian@192.168.122.254
```

### 5.5 Résumé concret du 0700

En pratique, l'activité `0700` a été faite dans cet ordre :

1. création du réseau `net-isole`
2. branchement de `vm2` sur `net-isole`
3. ajout d'une deuxième carte réseau à `vm3`
4. attribution d'IP fixes à `vm3`
5. vérification que `vm1` atteint `vm3`
6. vérification que `vm3` atteint `vm2`
7. test du saut SSH avec `-J`
8. test du tunnel SSH avec `-L`
9. configuration optionnelle du SSH sans mot de passe de `vm1` vers `vm3`

---

## 6. Activité 0710 — Passerelle entre réseaux

Objectif de la fiche :

- configurer `vm3` comme passerelle du réseau `10.10.10.0/24`
- permettre à `vm2` d'atteindre des machines du réseau `192.168.122.0/24`

Solution propre attendue :

- sur `vm3`
  - avoir deux interfaces actives
  - activer le forwarding IP
- sur `vm2`
  - ajouter une route vers `192.168.122.0/24` via `10.10.10.2`
- sur `vm1`
  - ajouter une route de retour vers `10.10.10.0/24` via `192.168.122.254`

Autrement dit :

- `vm2` envoie vers `vm3` tout ce qui doit aller sur `192.168.122.0/24`
- `vm3` route les paquets entre `ens9` et `ens3`
- `vm1` doit savoir que pour répondre vers `10.10.10.0/24`, il faut repasser par `vm3`

### 6.1 Version de test

Cette version permet de tester sans modifier immédiatement les fichiers permanents.

#### Sur `vm3`

```bash
echo 'debianpass' | sudo -S sysctl -w net.ipv4.ip_forward=1
cat /proc/sys/net/ipv4/ip_forward
```

Explication :

- active le routage IPv4 dans le noyau
- la valeur finale doit être `1`

#### Sur `vm2`

```bash
echo 'debianpass' | sudo -S ip route add 192.168.122.0/24 via 10.10.10.2 dev ens3
ip route
```

Explication :

- dit à `vm2` que `192.168.122.0/24` est joignable via `vm3`
- `10.10.10.2` est l'adresse de `vm3` côté réseau isolé

#### Sur `vm1`

```bash
echo 'debianpass' | sudo -S ip route add 10.10.10.0/24 via 192.168.122.254 dev ens3
ip route
```

Explication :

- dit à `vm1` que les réponses vers `10.10.10.0/24` doivent repartir via `vm3`
- `192.168.122.254` est l'adresse de `vm3` côté réseau `default`

### 6.2 Tests à faire

Depuis `vm2` :

```bash
ping -c 1 10.10.10.2
ping -c 1 192.168.122.254
ping -c 1 192.168.122.179
ssh debian@192.168.122.179
```

Explication :

- `10.10.10.2` vérifie le lien direct avec `vm3`
- `192.168.122.254` vérifie le passage d'un réseau à l'autre
- `192.168.122.179` vérifie que `vm2` atteint `vm1`
- le `ssh` valide le fonctionnement réel, pas seulement le ping

### 6.3 Pourquoi mon premier test ne suffisait pas

Lors du premier essai, j'avais seulement fait :

- activation du routage sur `vm3`
- ajout de la route sur `vm2`

Le trafic aller partait bien, mais `vm1` n'avait pas de route de retour vers `10.10.10.0/24`.

Donc la bonne solution n'est pas forcément de faire du NAT, mais simplement d'ajouter la route de retour sur `vm1`.

### 6.4 Version persistante

#### a. Rendre `ip_forward` permanent sur `vm3`

Dans `vm3`, ouvrir le fichier :

```bash
sudo nano /etc/sysctl.conf
```

Ajouter ou décommenter :

```bash
net.ipv4.ip_forward=1
```

Appliquer sans redémarrer :

```bash
sudo sysctl -p
```

#### b. Route persistante sur `vm2`

Dans `vm2`, si l'interface est `ens3`, on peut ajouter la route dans `/etc/network/interfaces` :

```bash
source /etc/network/interfaces.d/*

auto lo
iface lo inet loopback

allow-hotplug ens3
iface ens3 inet dhcp
    post-up ip route add 192.168.122.0/24 via 10.10.10.2 dev ens3 || true
    pre-down ip route del 192.168.122.0/24 via 10.10.10.2 dev ens3 || true
```

Explication :

- la route est ajoutée quand l'interface monte
- elle est retirée quand l'interface descend

#### c. Route persistante sur `vm1`

Dans `vm1`, si l'interface est `ens3`, on peut ajouter :

```bash
source /etc/network/interfaces.d/*

auto lo
iface lo inet loopback

allow-hotplug ens3
iface ens3 inet dhcp
    post-up ip route add 10.10.10.0/24 via 192.168.122.254 dev ens3 || true
    pre-down ip route del 10.10.10.0/24 via 192.168.122.254 dev ens3 || true
```

Explication :

- cela ajoute la route de retour automatiquement à chaque démarrage réseau

### 6.5 Résumé du 0710

Pour que `0710` fonctionne proprement :

1. `vm3` doit avoir `192.168.122.254` et `10.10.10.2`
2. `vm3` doit avoir `ip_forward=1`
3. `vm2` doit avoir une route vers `192.168.122.0/24` via `10.10.10.2`
4. `vm1` doit avoir une route vers `10.10.10.0/24` via `192.168.122.254`

Avec ces 4 éléments, `vm3` joue bien le rôle de passerelle entre les deux réseaux.

---

## 7. Test temporaire fait puis retiré

Pour valider le comportement de `0710`, un test temporaire a été fait puis annulé.

### Commandes temporaires utilisées

Sur `vm3` :

```bash
echo 'debianpass' | sudo -S sysctl -w net.ipv4.ip_forward=1
```

Sur `vm2` :

```bash
echo 'debianpass' | sudo -S ip route replace 192.168.122.0/24 via 10.10.10.2 dev ens3
```

### Commandes de retour arrière

Sur `vm3` :

```bash
echo 'debianpass' | sudo -S sysctl -w net.ipv4.ip_forward=0
```

Sur `vm2` :

```bash
echo 'debianpass' | sudo -S ip route del 192.168.122.0/24 via 10.10.10.2 dev ens3
```

État final après nettoyage :

- `ip_forward` sur `vm3` remis à `0`
- route ajoutée sur `vm2` supprimée
- aucun fichier de configuration permanent modifié pour `0710`

---

## 8. Résumé rapide

Ce qui est prêt :

- `net-isole` est créé
- `vm1`, `vm2` et `vm3` sont branchées correctement
- `vm3` a ses IP statiques
- l'activité `0700` peut être faite avec SSH, jump et tunnel

Ce qui reste pour `0710` :

- choisir la méthode finale pour que `vm2` atteigne vraiment le réseau `default`
- probablement avec :
  - forwarding IP
  - route sur `vm2`
  - et éventuellement NAT/MASQUERADE sur `vm3`

Commandes les plus utiles à retenir :

```bash
ip -br a
ip route
sudo virsh -c qemu:///system domiflist vm3
ssh debian@192.168.122.254
ssh -J debian@192.168.122.254 debian@10.10.10.168
ssh -N -L 2222:10.10.10.168:22 debian@192.168.122.254
ssh -p 2222 debian@localhost
```
