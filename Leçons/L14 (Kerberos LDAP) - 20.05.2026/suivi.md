# Leçon 14 - 2026-05-20 (5p)


## Configuration du DNS d'antiterre sur la machine hôte

```shell
huguenindo@debian-usb:antiterre.infra$ sudo resolvectl dns antbr0 192.168.100.10
huguenindo@debian-usb:antiterre.infra$ sudo resolvectl domain antbr0 '~antiterre.lan'

huguenindo@debian-usb:antiterre.infra$ sudo resolvectl status --no-pager
Global
       Protocols: +LLMNR +mDNS -DNSOverTLS DNSSEC=no/unsupported
resolv.conf mode: stub

Link 2 (eno1)
    Current Scopes: DNS LLMNR/IPv4 LLMNR/IPv6
         Protocols: +DefaultRoute +LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported
Current DNS Server: 157.26.166.16
       DNS Servers: 157.26.166.16 157.26.166.17
        DNS Domain: s2.rpn.ch

...

Link 6 (antbr0)
    Current Scopes: DNS LLMNR/IPv4
         Protocols: -DefaultRoute +LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported
Current DNS Server: 192.168.100.10
       DNS Servers: 192.168.100.10
        DNS Domain: ~antiterre.lan

...

huguenindo@debian-usb:antiterre.infra$ ssh robick@cavi.antiterre.lan
The authenticity of host 'cavi.antiterre.lan (192.168.100.176)' can't be established.
ED25519 key fingerprint is SHA256:mdeELEFgyXlR2zvAqGypYsCd82Qa0IFSEfuEgtju9yo.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'cavi.antiterre.lan' (ED25519) to the list of known hosts.
robick@cavi.antiterre.lan's password: 
Linux cavi 6.1.0-34-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.135-1 (2025-04-25) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
robick@cavi:~$ exit
logout
Connection to cavi.antiterre.lan closed.

huguenindo@debian-usb:antiterre.infra$ dig cavi.antiterre.lan

; <<>> DiG 9.18.33-1~deb12u2-Debian <<>> cavi.antiterre.lan
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 62335
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 65494
;; QUESTION SECTION:
;cavi.antiterre.lan.		IN	A

;; ANSWER SECTION:
cavi.antiterre.lan.	110	IN	A	192.168.100.176

;; Query time: 0 msec
;; SERVER: 127.0.0.53#53(127.0.0.53) (UDP)
;; WHEN: Tue May 13 12:06:56 CEST 2025
;; MSG SIZE  rcvd: 63

huguenindo@debian-usb:antiterre.infra$ dig blossfeldtstad.antiterre.lan

; <<>> DiG 9.18.33-1~deb12u2-Debian <<>> blossfeldtstad.antiterre.lan
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 7080
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 65494
;; QUESTION SECTION:
;blossfeldtstad.antiterre.lan.	IN	A

;; ANSWER SECTION:
blossfeldtstad.antiterre.lan. 604800 IN	CNAME	ns1.antiterre.lan.
ns1.antiterre.lan.	604800	IN	A	192.168.100.10

;; Query time: 4 msec
;; SERVER: 127.0.0.53#53(127.0.0.53) (UDP)
;; WHEN: Tue May 13 12:07:12 CEST 2025
;; MSG SIZE  rcvd: 91

```
> le paquet systemd-resolved doit être installé!

## Services réseaux - AS, kerberos

* [Les principes du chiffrement](https://mylos.s2.rpn.ch/cours/int-sys2-iweb/https/chiffrement-principe/index.html)
* [Services réseaux](<../../Cours_Mylos/site/cours/int-sys1-nix/services-reseaux/index.html>)
   * [Service réseau - Service d'authentification](<../../Cours_Mylos/site/cours/int-sys1-nix/services-reseaux/authentification/index.html>)
      1. [Service réseau - Service d'authentification Kerberos](<../../Cours_Mylos/site/cours/int-sys1-nix/services-reseaux/srv-kerberos/index.html>)
         * montrer avec wireshark les échanges entre le client et le serveur kerberos lors de l'authentification. (kinit)

## Services réseaux - AS, LDAP

* [Services réseaux](<../../Cours_Mylos/site/cours/int-sys1-nix/services-reseaux/index.html>)
    * [Service réseau - Service d'authentification](<../../Cours_Mylos/site/cours/int-sys1-nix/services-reseaux/authentification/index.html>)
        1. [Service réseau - Service d'annuaire LDAP](<../../Cours_Mylos/site/cours/int-sys1-nix/services-reseaux/srv-ldap/index.html>)


## A faire

1. finaliser l'installation de [Service réseau - Service d'authentification Kerberos](<../../Cours_Mylos/site/cours/int-sys1-nix/services-reseaux/srv-kerberos/index.html>)
    * montrer avec wireshark les échanges entre le client et le serveur kerberos lors de l'authentification. (kinit)
1. [Service réseau - Service d'annuaire LDAP](<../../Cours_Mylos/site/cours/int-sys1-nix/services-reseaux/srv-ldap/index.html>)
   * installer le service ldap
   * créer l'utilisateur robick

## Notes

### Vérification de la configuration du DNS sur cavisudo vipw
```shell
huguenindo@debian-usb:antiterre.infra$ incus shell cavi
root@cavi:~# su -l admin
admin@cavi:~$ resolvectl status --no-pager
Global
       Protocols: +LLMNR +mDNS -DNSOverTLS DNSSEC=no/unsupported
resolv.conf mode: stub

Link 2 (enp5s0)
    Current Scopes: DNS LLMNR/IPv4 LLMNR/IPv6
         Protocols: +DefaultRoute +LLMNR -mDNS -DNSOverTLS DNSSEC=no/unsupported
Current DNS Server: 192.168.100.11
       DNS Servers: 192.168.100.11 192.168.100.10
admin@cavi:~$ dig blossfeldtstad.antiterre.lan

; <<>> DiG 9.18.33-1~deb12u2-Debian <<>> blossfeldtstad.antiterre.lan
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 27468
;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 65494
;; QUESTION SECTION:
;blossfeldtstad.antiterre.lan.	IN	A

;; ANSWER SECTION:
blossfeldtstad.antiterre.lan. 604800 IN	CNAME	ns1.antiterre.lan.
ns1.antiterre.lan.	604800	IN	A	192.168.100.10

;; Query time: 0 msec
;; SERVER: 127.0.0.53#53(127.0.0.53) (UDP)
;; WHEN: Wed May 21 06:30:06 UTC 2025
;; MSG SIZE  rcvd: 91

admin@cavi:~$ dig blossfeldtstad.antiterre.lan @192.168.100.10

; <<>> DiG 9.18.33-1~deb12u2-Debian <<>> blossfeldtstad.antiterre.lan @192.168.100.10
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 32658
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
; COOKIE: 78453df0a0eff11501000000682d7303af66132f64213c7f (good)
;; QUESTION SECTION:
;blossfeldtstad.antiterre.lan.	IN	A

;; ANSWER SECTION:
blossfeldtstad.antiterre.lan. 604800 IN	CNAME	ns1.antiterre.lan.
ns1.antiterre.lan.	604800	IN	A	192.168.100.10

;; Query time: 0 msec
;; SERVER: 192.168.100.10#53(192.168.100.10) (UDP)
;; WHEN: Wed May 21 06:30:26 UTC 2025
;; MSG SIZE  rcvd: 119
```

### Suppression du mot de passe d'un utilisateur local

* editer le fichier /etch/shadow
   ```shell
   admin@cavi:~$ sudo vipw -s
   ```
* Remplacer le mot de passe par le caractère `!`
