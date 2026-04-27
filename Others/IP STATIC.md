Pour finir proprement l’exercice, dans vm3 il faut rendre ça permanent dans /etc/network/interfaces:

```
auto lo
iface lo inet loopback

allow-hotplug ens3
iface ens3 inet static
    address 192.168.122.254/24
    gateway 192.168.122.1

allow-hotplug ens9
iface ens9 inet static
    address 10.10.10.2/24

```