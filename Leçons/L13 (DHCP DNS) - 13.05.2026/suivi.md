# Leçon 13 - 2026-05-13 (5p)


> correction de l'évaluation
> Service réseau dhcp - dns

## Service réseau

* [Services réseaux](<../../Cours_Mylos/site/cours/int-sys1-nix/services-reseaux/index.html>)
   * [Service réseau - Cas d'études](<../../Cours_Mylos/site/cours/int-sys1-nix/services-reseaux/cas-etude/index.html>)
   * [Service réseau - Mise en place de l'infrastructure de virtualisation](<../../Cours_Mylos/site/cours/int-sys1-nix/services-reseaux/infrastructure-virtualisation/index.html>)
      1. Création d'un projet `antiterre`
      1. Création du réseau virtuelle `antbr0` en `192.168.100.0/24` sans DHCP
      1. Création du profil antiterre utilisant par défaut le réseau `antbr0`
      1. Création du conteneur `blossfeldtstad`

## DHCP

* [Services réseaux](<../../Cours_Mylos/site/cours/int-sys1-nix/services-reseaux/index.html>)
    1. installer le service DHCP - [Service réseau - Service DHCP, Dynamic Host Configuration Protocol](<../../Cours_Mylos/site/cours/int-sys1-nix/services-reseaux/srv-dhcp/index.html>)

* verification des log

  ```bash
  root@blossfeldtstad:~# journalctl -u isc-dhcp-server
  ```
  q
* Vérification de la configuration

    ```bash
    debian@blossfeldtstad:~$ dhcpd -t -cf /etc/dhcp/dhcpd.conf
    ```

* Demander une adresse au DHCP

  ```bash
  huguenindo@mc0-0315-00:~$ sudo dhclient -v
  ```


## Services réseaux - DNS

* [Service réseau - Mise en réseau](<../../Cours_Mylos/site/cours/int-sys1-nix/services-reseaux/mise-en-reseau/index.html>)
    1. [Service réseau - Service DNS, Domaine Name System](<../../Cours_Mylos/site/cours/int-sys1-nix/services-reseaux/srv-dns/index.html>)

## A faire

1. finir l'installation du DHCP, DNS sur blossfeldtstad
1. Créer les machines galatograd (conteneur), urbicande (VM), cavi (VM), luna (VM)
   * C'est le dhcp qui distribue les adresses ip static à galatograd et urbicande

## Notes

### Création d'un projet
```shel
huguenindo@debian-usb:~$ incus project create test
Project test created
huguenindo@debian-usb:~$ incus project list
+---------------------+--------+---------+-----------------+-----------------+----------+---------------+-----------------------------------------------------------------+-------------+
|         NOM         | IMAGES | PROFILS | STORAGE VOLUMES | STORAGE BUCKETS | NETWORKS | NETWORK ZONES |                           DESCRIPTION                           | UTILISÉ PAR |
+---------------------+--------+---------+-----------------+-----------------+----------+---------------+-----------------------------------------------------------------+-------------+
| test                | OUI    | OUI     | OUI             | OUI             | NON      | NON           |                                                                 | 1           |
+---------------------+--------+---------+-----------------+-----------------+----------+---------------+-----------------------------------------------------------------+-------------+
huguenindo@debian-usb:~$ incus project create test2 -c features.images=false
Project test2 created
huguenindo@debian-usb:~$ incus project list
+---------------------+--------+---------+-----------------+-----------------+----------+---------------+-----------------------------------------------------------------+-------------+
|         NOM         | IMAGES | PROFILS | STORAGE VOLUMES | STORAGE BUCKETS | NETWORKS | NETWORK ZONES |                           DESCRIPTION                           | UTILISÉ PAR |
+---------------------+--------+---------+-----------------+-----------------+----------+---------------+-----------------------------------------------------------------+-------------+
| test                | OUI    | OUI     | OUI             | OUI             | NON      | NON           |                                                                 | 1           |
+---------------------+--------+---------+-----------------+-----------------+----------+---------------+-----------------------------------------------------------------+-------------+
| test2               | NON    | OUI     | OUI             | OUI             | NON      | NON           |                                                                 | 1           |
+---------------------+--------+---------+-----------------+-----------------+----------+---------------+-----------------------------------------------------------------+-------------+

huguenindo@debian-usb:~$ incus project switch test2
huguenindo@debian-usb:~$ incus project list
+-----------------+--------+---------+-----------------+-----------------+----------+---------------+-----------------------------------------------------------------+-------------+
|       NOM       | IMAGES | PROFILS | STORAGE VOLUMES | STORAGE BUCKETS | NETWORKS | NETWORK ZONES |                           DESCRIPTION                           | UTILISÉ PAR |
+-----------------+--------+---------+-----------------+-----------------+----------+---------------+-----------------------------------------------------------------+-------------+
| test            | OUI    | OUI     | OUI             | OUI             | NON      | NON           |                                                                 | 1           |
+-----------------+--------+---------+-----------------+-----------------+----------+---------------+-----------------------------------------------------------------+-------------+
| test2 (current) | NON    | OUI     | OUI             | OUI             | NON      | NON           |                                                                 | 1           |
+-----------------+--------+---------+-----------------+-----------------+----------+---------------+-----------------------------------------------------------------+-------------+
huguenindo@debian-usb:~$ 

```
