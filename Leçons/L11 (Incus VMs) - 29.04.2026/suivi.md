# Leçon 11 - 2026-04-29 (5p)


## Installer les VMs pour l'évaluation

### Installation des VM kvmRef

1. Mettre en place une machine de référence KVM nommée `kvmRef1`.
  1. Copier le fichier `kvmRef1.qcow2` dans le dossier `/var/lib/libvirt/images`
      ```shell
      hote:$ sudo cp ./kvmRef1.qcow2 /var/lib/libvirt/images
      ```
  1. Créer la vm `kvmRef1`
      ```shell
      hote:$ virsh -c qemu:///system define ./kvmRef1.xml
      ```
1. Mettre en place une machine de référence KVM nommée kvmRef2.
  1. Copier le fichier kvmRef2.img dans le dossier /var/lib/libvirt/images
      ```shell
      hote:$ sudo cp ./kvmRef2.img /var/lib/libvirt/images
      ```
  1. Créer la vm `kvmRef2`
      ```shell
      hote:$ virsh -c qemu:///system define ./kvmRef2.xml        
      ```
### Vérifier leurs fonctionnements

```bash
hote:~$ virsh -c qemu:///system                                                                                          
Bienvenue dans virsh, le terminal de virtualisation interactif.
Taper :  « help » pour l’aide des commandes
         « quit » pour quitter

virsh # destroy kvmRef1
Domaine 'kvmRef1' détruit

virsh # destroy kvmRef2
Domaine 'kvmRef2' détruit

virsh # list --all
 ID   Nom         État
-------------------------
 -    kvmRef1     fermé
 -    kvmRef2     fermé

virsh # vol-list default
 Nom             Chemin
--------------------------------------------------------
 kvmRef1.qcow2   /var/lib/libvirt/images/kvmRef1.qcow2
 kvmRef2.img     /var/lib/libvirt/images/kvmRef2.img

virsh # start kvmRef1
Domaine 'kvmRef1' démarré

virsh # start kvmRef2
Domaine 'kvmRef2' démarré

virsh # list --all
 ID   Nom         État
----------------------------------------
 5    kvmRef1     en cours d’exécution
 6    kvmRef2     en cours d’exécution

hote:~$ virsh -c qemu:///system                                                                                          
Bienvenue dans virsh, le terminal de virtualisation interactif.
Taper :  « help » pour l’aide des commandes
         « quit » pour quitter

virsh # domifaddr kvmRef1
 Nom        adresse MAC          Protocole     Adresse
-------------------------------------------------------------------------------
 vnet4      52:54:00:f1:46:99    ipv4         192.168.122.150/24

virsh # console kvmRef1
Connecté au domaine 'kvmRef1'
Le caractère d'échappement est ^] (Ctrl + ])
kvmRef1 login: debian
Mot de passe : 

Linux kvmRef1 6.12.74+deb13+1-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.12.74-2 (2026-03-08) x86_64
The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.
Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.

debian@kvmRef1:~$

debian@kvmRef1:~$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host noprefixroute 
       valid_lft forever preferred_lft forever
2: enp1s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 52:54:00:f1:46:99 brd ff:ff:ff:ff:ff:ff
    altname enx525400f14699
    inet 192.168.122.150/24 brd 192.168.122.255 scope global dynamic noprefixroute enp1s0
       valid_lft 3534sec preferred_lft 3084sec
    inet6 fe80::8819:2ffe:7309:640b/64 scope link 
       valid_lft forever preferred_lft forever

debian@kvmRef1:~$ for f in $(ls /etc/ssh/ssh_host_*.pub); do ssh-keygen -lf $f; done;
256 SHA256:ZWE6+aUsX1obh5nTH1rLWhll2rJ/CPXcIpcZZAMGp0Y root@kvmRef1 (ECDSA)
256 SHA256:IsDC9iNtNP+MKYzIe8qXQB/zcKdLa8QNptl8bQD/Rcs root@kvmRef1 (ED25519)
3072 SHA256:rn0M+vtBsxRiW3p2Ry4Wes1Qfam4X3TeWnwQFa8m3p4 root@kvmRef1 (RSA)

debian@kvmRef1:~$ 
debian@kvmRef1:~$ exit
déconnexion

Debian GNU/Linux 13 kvmRef1 ttyS0
kvmRef1 login: 

virsh # exit

hote:~$ ssh -o IdentitiesOnly=yes debian@192.168.122.150
debian@192.168.122.150's password: 

Linux kvmRef1 6.12.74+deb13+1-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.12.74-2 (2026-03-08) x86_64
The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.
Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Mon Mar 30 16:07:19 2026 from 192.168.122.1

debian@kvmRef1:~$ exit
déconnexion

Connection to 192.168.122.150 closed.

hote:~$ virsh -c qemu:///system
Bienvenue dans virsh, le terminal de virtualisation interactif.
Taper :  « help » pour l’aide des commandes
         « quit » pour quitter

virsh # domifaddr kvmRef2
 Nom        adresse MAC          Protocole     Adresse
-------------------------------------------------------------------------------
 vnet5      52:54:00:47:21:40    ipv4         192.168.122.206/24
 -          -                    ipv4         192.168.122.207/24

virsh # console kvmRef2
Connecté au domaine 'kvmRef2'
Le caractère d'échappement est ^] (Ctrl + ])
kvmRef2 login: debian
Mot de passe : 

Linux kvmRef2 6.12.74+deb13+1-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.12.74-2 (2026-03-08) x86_64
The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.
Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.

debian@kvmRef2:~$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host noprefixroute 
       valid_lft forever preferred_lft forever
2: enp1s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 52:54:00:47:21:40 brd ff:ff:ff:ff:ff:ff
    altname enx525400472140
    inet 192.168.122.207/24 brd 192.168.122.255 scope global dynamic noprefixroute enp1s0
       valid_lft 3276sec preferred_lft 2644sec
    inet6 fe80::2467:9613:4d3d:c829/64 scope link 
       valid_lft forever preferred_lft forever
       
debian@kvmRef2:~$ for f in $(ls /etc/ssh/ssh_host_*.pub); do ssh-keygen -lf $f; done;
256 SHA256:489zjWSu0lXHGDw7vCg0Vw/THlA4yfdsdsaHQl6eCk8 root@kvmRef2 (ECDSA)
256 SHA256:ZbrOceXdD5dqYmAlkw0LKWLWYwRFZQ3BCuClim0Mb+k root@kvmRef2 (ED25519)
3072 SHA256:7v0OjFLXTMCpjpiyyRVZD/qDZI9/EiKKJOSIaNORaBc root@kvmRef2 (RSA)

debian@kvmRef2:~$ exit
déconnexion

Debian GNU/Linux 13 kvmRef2 ttyS0
kvmRef2 login: 

virsh # exit

hote:~$ ssh -o IdentitiesOnly=yes debian@192.168.122.207
The authenticity of host '192.168.122.207 (192.168.122.207)' can't be established.
ED25519 key fingerprint is SHA256:ZbrOceXdD5dqYmAlkw0LKWLWYwRFZQ3BCuClim0Mb+k.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '192.168.122.207' (ED25519) to the list of known hosts.

debian@192.168.122.207's password: 

Linux kvmRef2 6.12.74+deb13+1-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.12.74-2 (2026-03-08) x86_64
The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.
Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.

debian@kvmRef2:~$ exit
déconnexion

Connection to 192.168.122.207 closed.
```


## installation et configuration Incus

* installer et configurer incus fork de lxd [Virtualisation - incus + zfs](<../../Cours_Mylos/site/cours/int-sys1-nix/fiches/virtualisation-incus-zfs/index.html>)
* [Virtualisation - machine virtuelle versus conteneur](<../../Cours_Mylos/site/cours/int-sys1-nix/fiches/virtualisation-vm-conteneur/index.html>) - impact sur les ressources 
* [Installation de la base de données PostgreSQL](https://mylos.s2.rpn.ch/cours/int-prog1-db/infrastructure/installation-postgresql/) dans un conteneur incus
   1. configuration du schéma magasin [intbasdb.schema-magasin](https://mylos.s2.rpn.ch/gitlab/dhu.cours/intbasdb/activites/intbasdb.schema-magasin)
   1. Configuration du schéma recette [intbasdb.100-modelisation-recette](https://mylos.s2.rpn.ch/gitlab/dhu.cours/intbasdb/activites/intbasdb.100-modelisation-recette)

### Accès via ssh sur un conteneur

```
huguenindo@debian-usb:~$ incus launch images:debian/bookworm/cloud test

huguenindo@debian-usb:~$ incus list
+---------+---------+-------------------------+------+-----------------+-------------+
|   NOM   |  ÉTAT   |          IPV4           | IPV6 |      TYPE       | INSTANTANÉS |
+---------+---------+-------------------------+------+-----------------+-------------+
| netboot | STOPPED |                         |      | VIRTUAL-MACHINE | 0           |
+---------+---------+-------------------------+------+-----------------+-------------+
| test    | RUNNING | 10.246.230.156 (eth0)   |      | CONTAINER       | 0           |
+---------+---------+-------------------------+------+-----------------+-------------+

huguenindo@debian-usb:~$ ls ~/.ssh/
authorized_keys  huguenindo@kobenhavn_rsa      huguenindo@lozan_rsa      id_rsa      known_hosts      kobenhavn_id_rsa      other_keys.seahorse
config           huguenindo@kobenhavn_rsa.pub  huguenindo@lozan_rsa.pub  id_rsa.pub  known_hosts.old  kobenhavn_id_rsa.pub

huguenindo@debian-usb:~$ cat ~/.ssh/id_rsa.pub 
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC3fJWK08d4ciGf/1tbrefIEDZXlqtJrtiCstFXjwodxFimVpjz/mSu7TrqGKDDu0vcZ7Ph4K70i/tjcYaJACEk/Vtb8cUm1KejsHdKue0bBGPZQAqyQc35hmDALRqYXYRsgf3NacGaUKg3O1FlOPPJZrZ+h50H7swJF7HN3obWR7R3AuReSWxsenKNHNB31LidJN07Rix0BNrFf6Hk8EIDfx2DIDgIIs5t0DgGgIG5GZkkUA/kf6+WIx6Gs2VQAy8mjW5HahJaoAcBtAy9j/nrtPpgQA+amoEEn01+h8P0xkYJyiwpriFps9Z0C3Y8xMbzBu/LFKGlRsdmAZOom8mLEicOOwiD3qebdS5UTYp1ErGSLTcQpOjVEGhGFPM2UYPD6+qCmnsosFEZMQQDZ+Icaip2QV8I3zJ17DiXuWQ+F8vj85sZLPx4st/ri2Xhrfm7jRi0NtYf9+Xe1FPZyUbkIiqpzSffhAYK4giMdb/Rnh6mD1YBab5sYpsoHdYvfaM= huguenindo@ubuntu-usb-dhu

huguenindo@debian-usb:~$ incus shell test
root@test:~# su -l debian
debian@test:~$ echo 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC3fJWK08d4ciGf/1tbrefIEDZXlqtJrtiCstFXjwodxFimVpjz/mSu7TrqGKDDu0vcZ7Ph4K70i/tjcYaJACEk/Vtb8cUm1KejsHdKue0bBGPZQAqyQc35hmDALRqYXYRsgf3NacGaUKg3O1FlOPPJZrZ+h50H7swJF7HN3obWR7R3AuReSWxsenKNHNB31LidJN07Rix0BNrFf6Hk8EIDfx2DIDgIIs5t0DgGgIG5GZkkUA/kf6+WIx6Gs2VQAy8mjW5HahJaoAcBtAy9j/nrtPpgQA+amoEEn01+h8P0xkYJyiwpriFps9Z0C3Y8xMbzBu/LFKGlRsdmAZOom8mLEicOOwiD3qebdS5UTYp1ErGSLTcQpOjVEGhGFPM2UYPD6+qCmnsosFEZMQQDZ+Icaip2QV8I3zJ17DiXuWQ+F8vj85sZLPx4st/ri2Xhrfm7jRi0NtYf9+Xe1FPZyUbkIiqpzSffhAYK4giMdb/Rnh6mD1YBab5sYpsoHdYvfaM= huguenindo@ubuntu-usb-dhu' >> ~/.ssh/authorized_keys 

root@test:~# apt install openssh-server
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following additional packages will be installed:
  libwrap0 ncurses-term openssh-sftp-server runit-helper ucf
Suggested packages:
  molly-guard monkeysphere ssh-askpass ufw
The following NEW packages will be installed:
  libwrap0 ncurses-term openssh-server openssh-sftp-server runit-helper ucf
0 upgraded, 6 newly installed, 0 to remove and 0 not upgraded.
Need to get 1,140 kB of archives.
After this operation, 6,942 kB of additional disk space will be used.
Do you want to continue? [Y/n] y
...
root@test:~# exit
logout

huguenindo@debian-usb:~$ ssh debian@10.246.230.156
The authenticity of host '10.246.230.156 (10.246.230.156)' can't be established.
ED25519 key fingerprint is SHA256:iRbev6oNGgWTaqwk+xw0cwOH/NAXL9NzLtluvXoctDE.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.246.230.156' (ED25519) to the list of known hosts.
Linux test 6.1.0-34-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.135-1 (2025-04-25) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
debian@test:~$ 
```

### Affichage des vm 

```
huguenindo@debian-usb:~$ incus list
+---------+---------+-------------------------+------+-----------------+-------------+
|   NOM   |  ÉTAT   |          IPV4           | IPV6 |      TYPE       | INSTANTANÉS |
+---------+---------+-------------------------+------+-----------------+-------------+
| netboot | STOPPED |                         |      | VIRTUAL-MACHINE | 0           |
+---------+---------+-------------------------+------+-----------------+-------------+
| test    | RUNNING | 10.246.230.156 (eth0)   |      | CONTAINER       | 0           |
+---------+---------+-------------------------+------+-----------------+-------------+
| vm1     | RUNNING | 10.246.230.209 (enp5s0) |      | VIRTUAL-MACHINE | 0           |
+---------+---------+-------------------------+------+-----------------+-------------+
huguenindo@debian-usb:~$ incus list --project dev
+-----+---------+--------------------+-----------------------------------------------+-----------+-------------+
| NOM |  ÉTAT   |        IPV4        |                     IPV6                      |   TYPE    | INSTANTANÉS |
+-----+---------+--------------------+-----------------------------------------------+-----------+-------------+
| db  | RUNNING | 172.16.3.23 (eth0) | fd42:81fc:4834:eaa8:216:3eff:fe1e:1e63 (eth0) | CONTAINER | 0           |
+-----+---------+--------------------+-----------------------------------------------+-----------+-------------+
huguenindo@debian-usb:~$ incus list --all-projects
+---------+---------+---------+-------------------------+-----------------------------------------------+-----------------+-------------+
| PROJECT |   NOM   |  ÉTAT   |          IPV4           |                     IPV6                      |      TYPE       | INSTANTANÉS |
+---------+---------+---------+-------------------------+-----------------------------------------------+-----------------+-------------+
| default | netboot | STOPPED |                         |                                               | VIRTUAL-MACHINE | 0           |
+---------+---------+---------+-------------------------+-----------------------------------------------+-----------------+-------------+
| default | test    | RUNNING | 10.246.230.156 (eth0)   |                                               | CONTAINER       | 0           |
+---------+---------+---------+-------------------------+-----------------------------------------------+-----------------+-------------+
| default | vm1     | RUNNING | 10.246.230.209 (enp5s0) |                                               | VIRTUAL-MACHINE | 0           |
+---------+---------+---------+-------------------------+-----------------------------------------------+-----------------+-------------+
| dev     | db      | RUNNING | 172.16.3.23 (eth0)      | fd42:81fc:4834:eaa8:216:3eff:fe1e:1e63 (eth0) | CONTAINER       | 0           |
+---------+---------+---------+-------------------------+-----------------------------------------------+-----------------+-------------+
| intdb   | intdb   | RUNNING | 10.246.230.223 (eth0)   |                                               | CONTAINER       | 0           |
+---------+---------+---------+-------------------------+-----------------------------------------------+-----------------+-------------+
```

### Installation du l'interface web

```
huguenindo@debian-usb:~$ sudo apt install incus-ui-canonical
[sudo] Mot de passe de huguenindo : 
Lecture des listes de paquets... Fait
Construction de l'arbre des dépendances... Fait
Lecture des informations d'état... Fait      
Les paquets suivants ont été installés automatiquement et ne sont plus nécessaires :
  linux-headers-6.1.0-28-amd64 linux-headers-6.1.0-28-common linux-headers-6.1.0-30-amd64 linux-headers-6.1.0-30-common
  linux-headers-6.1.0-31-amd64 linux-headers-6.1.0-31-common linux-image-6.1.0-28-amd64 linux-image-6.1.0-30-amd64 linux-image-6.1.0-31-amd64
Veuillez utiliser « sudo apt autoremove » pour les supprimer.
Les NOUVEAUX paquets suivants seront installés :
  incus-ui-canonical
0 mis à jour, 1 nouvellement installés, 0 à enlever et 0 non mis à jour.
Il est nécessaire de prendre 3’597 ko dans les archives.
Après cette opération, 20.2 Mo d'espace disque supplémentaires seront utilisés.
Réception de :1 https://pkgs.zabbly.com/incus/stable bookworm/main amd64 incus-ui-canonical amd64 1:6.12-debian12-202504242211 [3’597 kB]
3’597 ko réceptionnés en 2s (2’239 ko/s)         
Sélection du paquet incus-ui-canonical précédemment désélectionné.
(Lecture de la base de données... 498080 fichiers et répertoires déjà installés.)
Préparation du dépaquetage de .../incus-ui-canonical_1%3a6.12-debian12-202504242211_amd64.deb ...
Dépaquetage de incus-ui-canonical (1:6.12-debian12-202504242211) ...
Paramétrage de incus-ui-canonical (1:6.12-debian12-202504242211) ...

huguenindo@debian-usb:~$ incus webui
Web server running at: http://127.0.0.1:33887/ui?auth_token=40fefe3f-3c9e-444a-a3a3-6c698a1e5603
^C

```


## Notes
