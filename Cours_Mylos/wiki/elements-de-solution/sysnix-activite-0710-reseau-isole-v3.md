[[_TOC_]]

# SYSNIX - Virtualisation, passerelle entre réseaux (Éléments de solution avec des machine Debian (debian-12-nocloud-amd64))
>Configuration réseau permettant à un réseau isolé de sortir sur internet



## Activité

```
-------+------------------------------------+---------------+----virbr1 10.10.10.0/24
       |                                    |               |    net-isole
       |                                    |               |
-------|--+------------+-----------------+--|---------------|----virbr0 192.168.122.0/24
virbr10|  |virbr0      |             eth0|  |eth1       eth0|    default
     .1|  |.1          |             .254|  |.2             |
     .-+--+-. nat    .-+----.          .-+--+-.           .-+----.
     |      |        |      |          |      |           |      |
     | hôte |        | vm1  |          | vm3  |           | vm2  |
     |      |        |      |          |      |           |      |
     `--+---'        `------'          `------'           `------'
        |eth0                         passerelle 
        |
 -------+----------------------------------------S2 157.26.229.0/24
```

Configurer la machine vm3 comme passerelle permettant à la machine vm2 d'accéder aux machines du réseau virbr0.
Le réseau virbr10 est un réseau virtuel isolé.


## Configuration des réseaux virtuels

On reprend la configuration de [Éléments de solution avec des machine Debian (debian-12-nocloud-amd64)](sysnix-activite-0700-reseau-v3)

```shell
╭─ ~/tmp/sysnix  ✔  dom@domp14s  10:45:54 
╰─ virsh -c qemu:///system list
 Id   Name   State
----------------------
 15   vm1    running
 16   vm2    running
 17   vm3    running

╭─ ~/tmp/sysnix  ✔  dom@domp14s  12:10:34 
╰─ virsh -c qemu:///system domifaddr vm1
 Name       MAC address          Protocol     Address
-------------------------------------------------------------------------------
 vnet22     52:54:00:ba:2a:4a    ipv4         192.168.122.177/24


╭─ ~/tmp/sysnix  ✔  dom@domp14s  12:11:09 
╰─ virsh -c qemu:///system domifaddr vm2
 Name       MAC address          Protocol     Address
-------------------------------------------------------------------------------
 vnet23     52:54:00:15:a7:05    ipv4         10.10.10.199/24


╭─ ~/tmp/sysnix  ✔  dom@domp14s  12:11:13 
╰─ virsh -c qemu:///system domifaddr vm3
 Name       MAC address          Protocol     Address
-------------------------------------------------------------------------------
 vnet24     52:54:00:19:85:3e    ipv4         192.168.122.254/24
 vnet25     52:54:00:cb:30:7f    ipv4         10.10.10.2/24
```

## Configuration de la vm1


### État du réseau

```shell
debian@vm1:~$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host noprefixroute 
       valid_lft forever preferred_lft forever
2: enp1s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 52:54:00:ba:2a:4a brd ff:ff:ff:ff:ff:ff
    inet 192.168.122.177/24 metric 100 brd 192.168.122.255 scope global dynamic enp1s0
       valid_lft 2168sec preferred_lft 2168sec
    inet6 fe80::5054:ff:feba:2a4a/64 scope link 
       valid_lft forever preferred_lft forever

debian@vm1:~$ ip route
default via 192.168.122.1 dev enp1s0 proto dhcp src 192.168.122.177 metric 100 
192.168.122.0/24 dev enp1s0 proto kernel scope link src 192.168.122.177 metric 100 
192.168.122.1 dev enp1s0 proto dhcp scope link src 192.168.122.177 metric 100 
```
## Configuration de la vm2 

### État du réseau

```shell
root@vm2:~# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host noprefixroute 
       valid_lft forever preferred_lft forever
2: enp1s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 52:54:00:15:a7:05 brd ff:ff:ff:ff:ff:ff
    inet 10.10.10.199/24 metric 100 brd 10.10.10.255 scope global dynamic enp1s0
       valid_lft 2034sec preferred_lft 2034sec
    inet6 fe80::5054:ff:fe15:a705/64 scope link 
       valid_lft forever preferred_lft forever

root@vm2:~# ip route
10.10.10.0/24 dev enp1s0 proto kernel scope link src 10.10.10.199 metric 100 
10.10.10.1 dev enp1s0 proto dhcp scope link src 10.10.10.199 metric 100 
```


## Configuration de la vm3

### État du réseau

```shell
root@vm3:~# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host noprefixroute 
       valid_lft forever preferred_lft forever
2: enp1s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 52:54:00:19:85:3e brd ff:ff:ff:ff:ff:ff
    inet 192.168.122.254/24 metric 100 brd 192.168.122.255 scope global dynamic enp1s0
       valid_lft 2068sec preferred_lft 2068sec
    inet6 fe80::5054:ff:fe19:853e/64 scope link 
       valid_lft forever preferred_lft forever
3: enp7s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 52:54:00:cb:30:7f brd ff:ff:ff:ff:ff:ff
    inet 10.10.10.2/24 metric 100 brd 10.10.10.255 scope global dynamic enp7s0
       valid_lft 2039sec preferred_lft 2039sec
    inet6 fe80::5054:ff:fecb:307f/64 scope link 
       valid_lft forever preferred_lft forever

root@vm3:~# ip route
default via 192.168.122.1 dev enp1s0 proto dhcp src 192.168.122.254 metric 100 
10.10.10.0/24 dev enp7s0 proto kernel scope link src 10.10.10.2 metric 100 
10.10.10.1 dev enp7s0 proto dhcp scope link src 10.10.10.2 metric 100 
192.168.122.0/24 dev enp1s0 proto kernel scope link src 192.168.122.254 metric 100 
192.168.122.1 dev enp1s0 proto dhcp scope link src 192.168.122.254 metric 100 
```

### Configuration réseau du système

* activation du "pontage" entre les deux cartes réseaux (Activation temporaire)

```shell
root@vm3:~# cat /proc/sys/net/ipv4/ip_forward
0
root@vm3:~# echo 1 > /proc/sys/net/ipv4/ip_forward
root@vm3:~# cat /proc/sys/net/ipv4/ip_forward
1
```

* activation du "pontage" entre les deux cartes réseaux (Activation permanente) dans `/etc/sysctl.conf` ajouter:

```shell
root@vm3:~# cat /etc/sysctl.conf | grep net.ipv4.ip
net.ipv4.ip_forward=1
```
* Après redémarrage

```shell
root@vm3:~# cat /proc/sys/net/ipv4/ip_forward
1
```

## Configuration du routage (permanent)

### sur vm2
```shell
root@vm2:~# cat /etc/netplan/90-default.yaml 
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
            - to: 192.168.122.0/24
              via: 10.10.10.2
        all-eth:
            match:
                name: eth*
            dhcp4: true
            dhcp4-overrides:
                use-domains: true
            dhcp6: true
            dhcp6-overrides:
                use-domains: true

root@vm2:~# netplan apply

root@vm2:~# netplan status
     Online state: offline
    DNS Addresses: 10.10.10.1 (compat)
       DNS Search: .

●  1: lo ethernet UNKNOWN/UP (unmanaged)
      MAC Address: 00:00:00:00:00:00
        Addresses: 127.0.0.1/8
                   ::1/128

●  2: enp1s0 ethernet UP (networkd: all-en)
      MAC Address: 52:54:00:15:a7:05 (Red Hat, Inc.)
        Addresses: 10.10.10.199/24 (dhcp)
                   fe80::5054:ff:fe15:a705/64 (link)
    DNS Addresses: 10.10.10.1
           Routes: 10.10.10.0/24 from 10.10.10.199 metric 100 (link)
                   10.10.10.1 from 10.10.10.199 metric 100 (dhcp, link)
                   192.168.122.0/24 via 10.10.10.2 (static)
                   fe80::/64 metric 256

root@vm2:~# ip route
10.10.10.0/24 dev enp1s0 proto kernel scope link src 10.10.10.199 metric 100 
10.10.10.1 dev enp1s0 proto dhcp scope link src 10.10.10.199 metric 100 
192.168.122.0/24 via 10.10.10.2 dev enp1s0 proto static onlink 
```

### sur vm1
```shell
root@vm1:~# cat /etc/netplan/90-default.yaml 
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

        all-eth:
            match:
                name: eth*
            dhcp4: true
            dhcp4-overrides:
                use-domains: true
            dhcp6: true
            dhcp6-overrides:
                use-domains: true

root@vm1:~# netplan apply

root@vm1:~# netplan status
     Online state: online
    DNS Addresses: 192.168.122.1 (compat)
       DNS Search: default

●  1: lo ethernet UNKNOWN/UP (unmanaged)
      MAC Address: 00:00:00:00:00:00
        Addresses: 127.0.0.1/8
                   ::1/128

●  2: enp1s0 ethernet UP (networkd: all-en)
      MAC Address: 52:54:00:ba:2a:4a (Red Hat, Inc.)
        Addresses: 192.168.122.177/24 (dhcp)
                   fe80::5054:ff:feba:2a4a/64 (link)
    DNS Addresses: 192.168.122.1
       DNS Search: default
           Routes: default via 192.168.122.1 from 192.168.122.177 metric 100 
(dhcp)
                   10.10.10.0/24 via 192.168.122.254 (static)
                   192.168.122.0/24 from 192.168.122.177 metric 100 (link)
                   192.168.122.1 from 192.168.122.177 metric 100 (dhcp, link)
                   fe80::/64 metric 256

root@vm1:~# ip route
default via 192.168.122.1 dev enp1s0 proto dhcp src 192.168.122.177 metric 100 
10.10.10.0/24 via 192.168.122.254 dev enp1s0 proto static onlink 
192.168.122.0/24 dev enp1s0 proto kernel scope link src 192.168.122.177 metric 100 
192.168.122.1 dev enp1s0 proto dhcp scope link src 192.168.122.177 metric 100 

```

### Vérification

### vm3 -> vm1

```shell
root@vm3:~# ping -c 4 192.168.122.177
PING 192.168.122.177 (192.168.122.177) 56(84) bytes of data.
64 bytes from 192.168.122.177: icmp_seq=1 ttl=64 time=0.461 ms
64 bytes from 192.168.122.177: icmp_seq=2 ttl=64 time=0.638 ms
64 bytes from 192.168.122.177: icmp_seq=3 ttl=64 time=0.573 ms
64 bytes from 192.168.122.177: icmp_seq=4 ttl=64 time=0.471 ms

--- 192.168.122.177 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3005ms
rtt min/avg/max/mdev = 0.461/0.535/0.638/0.073 ms
```

### vm3 -> vm2

```shell
root@vm3:~# ping -c 4 10.10.10.199
PING 10.10.10.199 (10.10.10.199) 56(84) bytes of data.
64 bytes from 10.10.10.199: icmp_seq=1 ttl=64 time=0.887 ms
64 bytes from 10.10.10.199: icmp_seq=2 ttl=64 time=0.719 ms
64 bytes from 10.10.10.199: icmp_seq=3 ttl=64 time=0.891 ms
64 bytes from 10.10.10.199: icmp_seq=4 ttl=64 time=0.534 ms

--- 10.10.10.199 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3005ms
rtt min/avg/max/mdev = 0.534/0.757/0.891/0.146 ms
```

###  vm1 -> vm3-> vm2 

```shell
root@vm1:~# ping -c 4 192.168.122.254
PING 192.168.122.254 (192.168.122.254) 56(84) bytes of data.
64 bytes from 192.168.122.254: icmp_seq=1 ttl=64 time=1.61 ms
64 bytes from 192.168.122.254: icmp_seq=2 ttl=64 time=0.442 ms
64 bytes from 192.168.122.254: icmp_seq=3 ttl=64 time=0.494 ms
64 bytes from 192.168.122.254: icmp_seq=4 ttl=64 time=0.654 ms

--- 192.168.122.254 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3005ms
rtt min/avg/max/mdev = 0.442/0.798/1.605/0.472 ms

root@vm1:~# ping -c 4 10.10.10.2
PING 10.10.10.2 (10.10.10.2) 56(84) bytes of data.
64 bytes from 10.10.10.2: icmp_seq=1 ttl=64 time=1.07 ms
64 bytes from 10.10.10.2: icmp_seq=2 ttl=64 time=0.769 ms
64 bytes from 10.10.10.2: icmp_seq=3 ttl=64 time=0.387 ms
64 bytes from 10.10.10.2: icmp_seq=4 ttl=64 time=0.523 ms

--- 10.10.10.2 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3005ms
rtt min/avg/max/mdev = 0.387/0.687/1.070/0.259 ms

root@vm1:~# traceroute 10.10.10.2
traceroute to 10.10.10.2 (10.10.10.2), 30 hops max, 60 byte packets
 1  10.10.10.2 (10.10.10.2)  1.137 ms  1.063 ms  1.042 ms

root@vm1:~# ping -c 4 10.10.10.199
PING 10.10.10.199 (10.10.10.199) 56(84) bytes of data.
64 bytes from 10.10.10.199: icmp_seq=1 ttl=63 time=1.10 ms
64 bytes from 10.10.10.199: icmp_seq=2 ttl=63 time=0.981 ms
64 bytes from 10.10.10.199: icmp_seq=3 ttl=63 time=1.20 ms
64 bytes from 10.10.10.199: icmp_seq=4 ttl=63 time=0.724 ms

--- 10.10.10.199 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3005ms
rtt min/avg/max/mdev = 0.724/1.000/1.198/0.177 ms

root@vm1:~# traceroute 10.10.10.199
traceroute to 10.10.10.199 (10.10.10.199), 30 hops max, 60 byte packets
 1  vm3.default (192.168.122.254)  2.082 ms  1.989 ms  1.972 ms
 2  10.10.10.199 (10.10.10.199)  2.722 ms  2.701 ms  2.682 ms
```
```shell
root@vm3:~# tcpdump -nni enp7s0 icmp
[ 1964.943415] device enp7s0 entered promiscuous mode
tcpdump: verbose output suppressed, use -v[v]... for full protocol decode
listening on enp7s0, link-type EN10MB (Ethernet), snapshot length 262144 bytes
13:22:11.885233 IP 10.10.10.199 > 192.168.122.177: ICMP 10.10.10.199 udp port 33437 unreachable, length 68
13:22:11.885233 IP 10.10.10.199 > 192.168.122.177: ICMP 10.10.10.199 udp port 33438 unreachable, length 68
13:22:11.885233 IP 10.10.10.199 > 192.168.122.177: ICMP 10.10.10.199 udp port 33439 unreachable, length 68
13:22:11.885233 IP 10.10.10.199 > 192.168.122.177: ICMP 10.10.10.199 udp port 33440 unreachable, length 68
13:22:11.885233 IP 10.10.10.199 > 192.168.122.177: ICMP 10.10.10.199 udp port 33441 unreachable, length 68
13:22:11.885233 IP 10.10.10.199 > 192.168.122.177: ICMP 10.10.10.199 udp port 33442 unreachable, length 68
13:22:22.842571 IP 192.168.122.177 > 10.10.10.199: ICMP echo request, id 443, seq 1, length 64
13:22:22.843013 IP 10.10.10.199 > 192.168.122.177: ICMP echo reply, id 443, seq 1, length 64
13:22:23.844072 IP 192.168.122.177 > 10.10.10.199: ICMP echo request, id 443, seq 2, length 64
13:22:23.844647 IP 10.10.10.199 > 192.168.122.177: ICMP echo reply, id 443, seq 2, length 64
13:22:24.846046 IP 192.168.122.177 > 10.10.10.199: ICMP echo request, id 443, seq 3, length 64
13:22:24.846530 IP 10.10.10.199 > 192.168.122.177: ICMP echo reply, id 443, seq 3, length 64
13:22:25.847914 IP 192.168.122.177 > 10.10.10.199: ICMP echo request, id 443, seq 4, length 64
13:22:25.848484 IP 10.10.10.199 > 192.168.122.177: ICMP echo reply, id 443, seq 4, length 64
^C
14 packets captured
14 packets [ 2002.527210] device enp7s0 left promiscuous mode
received by filter
0 packets dropped by kernel
```
>installation du paquet tcpdump, sudo apt install tcpdump

## Références

1. [Debian Permanent Static Routes](https://www.mybluelinux.com/debian-permanent-static-routes/)
1. [fr/LXC/SimpleBridge - Debian Wiki](https://wiki.debian.org/fr/LXC/SimpleBridge)
1. [VirtualNetworking - Libvirt Wiki](https://wiki.libvirt.org/page/VirtualNetworking)
1. [Flockport   -  Flockport labs - Using LXC containers as routers](https://www.flockport.com/flockport-labs-use-lxc-containers-as-routers/)
1. [Netplan documentation](https://netplan.readthedocs.io/en/stable/)

