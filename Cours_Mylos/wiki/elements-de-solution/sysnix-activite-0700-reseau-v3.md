[[_TOC_]]

# SYSNIX - Virtualisation - Mise en réseau des machines virtuelles (Éléments de solution avec des machine Debian (debian-12-nocloud-amd64))

## Activité

```
-------+------------------------------------+---------------+----virbr10 10.10.10.0/24
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

1. Mettre en application le schéma ci-dessus.
   1. Les machines virtuelles vm1 et vm3 sont connecté au réseau virtuel natté virbr0. Ce réseau virtuel est le réseau par défaut de libvirt.
   1. La machine virtuelle vm2 est connecté au réseau virtuel isolé virbr10. Ce réseau virtuel est un nouveau réseau.
   1. La machine virtuelle vm3 est connecté au deux réseaux virbr0 et virbr10.
1. Connexion ssh
     1. `vm1` doit pouvoir se connecter en ssh à `vm3` (`vm1` --> `vm3`)
     1. `vm3` doit pouvoir se connecter en ssh à `vm2` (`vm3` --> `vm2`)
     1. `vm1` doit pouvoir se connecter à `vm2` 
          1. via un saut (jump) sur vm3 (`vm1` --> `vm3`(jump) --> `vm2`)
          1. via un tunnel ssh à travers `vm3`. (`vm1` --> `vm3`(tunnel) --> `vm2`)
1. Connexion ssh sans mot de passe
   1. Configurer vm1 et vm3 pour que vm1 puisse se connecter à vm3 sans saisir de mot de passe.

## Mise en place de l'infrastructure 

1. Récupération d'une image pour l'informatique dématérialisé
   ```shell
   ╭─ ~/tmp/sysnix  ✔  dom@domp14s  09:31:23 
   ╰─ wget https://cloud.debian.org/images/cloud/bookworm/latest/debian-12-nocloud-amd64.raw
   --2025-04-07 09:31:38--  https://cloud.debian.org/images/cloud/bookworm/latest/debian-12-nocloud-amd64.raw
   Résolution de cloud.debian.org (cloud.debian.org)… 2001:6b0:19::163, 2001:6b0:19::173, 194.71.11.163, ...
   Connexion à cloud.debian.org (cloud.debian.org)|2001:6b0:19::163|:443… connecté.
   requête HTTP transmise, en attente de la réponse… 302 Found
   Emplacement : https://chuangtzu.ftp.acc.umu.se/images/cloud/bookworm/latest/debian-12-nocloud-amd64.raw [suivant]
   --2025-04-07 09:31:38--  https://chuangtzu.ftp.acc.umu.se/images/cloud/bookworm/latest/debian-12-nocloud-amd64.raw
   Résolution de chuangtzu.ftp.acc.umu.se (chuangtzu.ftp.acc.umu.se)… 2001:6b0:19::167, 194.71.11.167
   Connexion à chuangtzu.ftp.acc.umu.se (chuangtzu.ftp.acc.umu.se)|2001:6b0:19::167|:443… connecté.
   requête HTTP transmise, en attente de la réponse… 200 OK
   Taille : 3221225472 (3.0G)
   Enregistre : ‘debian-12-nocloud-amd64.raw’

   debian-12-nocloud-amd64.raw                      100%[==========================================================================================================>]   3.00G  11.7MB/s    ds 4m 8s   

   2025-04-07 09:35:46 (12.4 MB/s) - ‘debian-12-nocloud-amd64.raw’ enregistré [3221225472/3221225472]

   ╭─ ~/tmp/sysnix  ✔  4m 8s  dom@domp14s  09:35:46 
   ╰─ ls -l
   total 3146016
   -rw-rw-r-- 1 dom dom 3221225472 Mar 17 17:20 debian-12-nocloud-amd64.raw
   ```

1. Création de la machine vm1

   1. Création du stockage

      ```shell
      ╭─ ~/tmp/sysnix  ✔  dom@domp14s  09:38:24 
      ╰─ virsh -c qemu:///system                                                               
      Welcome to virsh, the virtualization interactive terminal.

      Type:  'help' for help with commands
            'quit' to quit

      virsh # pool-list
      Name           State    Autostart
      ------------------------------------
      boot-scratch   active   yes
      default        active   yes
      iso            active   yes
      lvm            active   yes
      tmp            active   yes
      zfs            active   yes

      virsh # vol-list lvm
      Name   Path
      ------------------------------
      home   /dev/domp14s-vg/home
      root   /dev/domp14s-vg/root
      swap   /dev/domp14s-vg/swap

      virsh # vol-create-as --format raw --pool lvm --name vm1disk 4G
      Vol vm1disk created

      virsh # vol-list lvm
      Name      Path
      ------------------------------------
      home      /dev/domp14s-vg/home
      root      /dev/domp14s-vg/root
      swap      /dev/domp14s-vg/swap
      vm1disk   /dev/domp14s-vg/vm1disk

      virsh # vol-upload --file debian-12-nocloud-amd64.raw --pool lvm --vol vm1disk

      ```
   1. Création de la machine vm1

      ```bash
      ╭─ ~/tmp/sysnix  1 ✘  dom@domp14s  10:09:16 
      ╰─ cat vm1.xml 
      <domain type='kvm'>
      <name>vm1</name>
      <metadata>
         <libosinfo:libosinfo xmlns:libosinfo="http://libosinfo.org/xmlns/libvirt/domain/1.0">
            <libosinfo:os id="http://debian.org/debian/12"/>
         </libosinfo:libosinfo>
      </metadata>
      <memory unit='KiB'>2097152</memory>
      <currentMemory unit='KiB'>2097152</currentMemory>
      <vcpu placement='static'>2</vcpu>
      <os>
         <type arch='x86_64' machine='pc-q35-6.2'>hvm</type>
         <boot dev='hd'/>
      </os>
      <features>
         <acpi/>
         <apic/>
         <vmport state='off'/>
      </features>
      <cpu mode='host-passthrough' check='none' migratable='on'/>
      <clock offset='utc'>
         <timer name='rtc' tickpolicy='catchup'/>
         <timer name='pit' tickpolicy='delay'/>
         <timer name='hpet' present='no'/>
      </clock>
      <on_poweroff>destroy</on_poweroff>
      <on_reboot>restart</on_reboot>
      <on_crash>destroy</on_crash>
      <pm>
         <suspend-to-mem enabled='no'/>
         <suspend-to-disk enabled='no'/>
      </pm>
      <devices>
         <emulator>/usr/bin/qemu-system-x86_64</emulator>
         <disk type='block' device='disk'>
            <driver name='qemu' type='raw' cache='none' io='native' discard='unmap'/>
            <source dev='/dev/domp14s-vg/vm1disk'/>
            <target dev='vda' bus='virtio'/>
            <address type='pci' domain='0x0000' bus='0x04' slot='0x00' function='0x0'/>
         </disk>
         <controller type='usb' index='0' model='qemu-xhci' ports='15'>
            <address type='pci' domain='0x0000' bus='0x02' slot='0x00' function='0x0'/>
         </controller>
         <controller type='pci' index='0' model='pcie-root'/>
         <controller type='pci' index='1' model='pcie-root-port'>
            <model name='pcie-root-port'/>
            <target chassis='1' port='0x10'/>
            <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x0' multifunction='on'/>
         </controller>
         <controller type='pci' index='2' model='pcie-root-port'>
            <model name='pcie-root-port'/>
            <target chassis='2' port='0x11'/>
            <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x1'/>
         </controller>
         <controller type='pci' index='3' model='pcie-root-port'>
            <model name='pcie-root-port'/>
            <target chassis='3' port='0x12'/>
            <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x2'/>
         </controller>
         <controller type='pci' index='4' model='pcie-root-port'>
            <model name='pcie-root-port'/>
            <target chassis='4' port='0x13'/>
            <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x3'/>
         </controller>
         <controller type='pci' index='5' model='pcie-root-port'>
            <model name='pcie-root-port'/>
            <target chassis='5' port='0x14'/>
            <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x4'/>
         </controller>
         <controller type='pci' index='6' model='pcie-root-port'>
            <model name='pcie-root-port'/>
            <target chassis='6' port='0x15'/>
            <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x5'/>
         </controller>
         <controller type='pci' index='7' model='pcie-root-port'>
            <model name='pcie-root-port'/>
            <target chassis='7' port='0x16'/>
            <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x6'/>
         </controller>
         <controller type='pci' index='8' model='pcie-root-port'>
            <model name='pcie-root-port'/>
            <target chassis='8' port='0x17'/>
            <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x7'/>
         </controller>
         <controller type='pci' index='9' model='pcie-root-port'>
            <model name='pcie-root-port'/>
            <target chassis='9' port='0x18'/>
            <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0' multifunction='on'/>
         </controller>
         <controller type='pci' index='10' model='pcie-root-port'>
            <model name='pcie-root-port'/>
            <target chassis='10' port='0x19'/>
            <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x1'/>
         </controller>
         <controller type='pci' index='11' model='pcie-root-port'>
            <model name='pcie-root-port'/>
            <target chassis='11' port='0x1a'/>
            <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x2'/>
         </controller>
         <controller type='pci' index='12' model='pcie-root-port'>
            <model name='pcie-root-port'/>
            <target chassis='12' port='0x1b'/>
            <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x3'/>
         </controller>
         <controller type='pci' index='13' model='pcie-root-port'>
            <model name='pcie-root-port'/>
            <target chassis='13' port='0x1c'/>
            <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x4'/>
         </controller>
         <controller type='pci' index='14' model='pcie-root-port'>
            <model name='pcie-root-port'/>
            <target chassis='14' port='0x1d'/>
            <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x5'/>
         </controller>
         <controller type='virtio-serial' index='0'>
            <address type='pci' domain='0x0000' bus='0x03' slot='0x00' function='0x0'/>
         </controller>
         <controller type='sata' index='0'>
            <address type='pci' domain='0x0000' bus='0x00' slot='0x1f' function='0x2'/>
         </controller>
         <interface type='network'>
            <source network='default'/>
            <model type='virtio'/>
            <address type='pci' domain='0x0000' bus='0x01' slot='0x00' function='0x0'/>
         </interface>
         <serial type='pty'>
            <target type='isa-serial' port='0'>
            <model name='isa-serial'/>
            </target>
         </serial>
         <console type='pty'>
            <target type='serial' port='0'/>
         </console>
         <channel type='unix'>
            <target type='virtio' name='org.qemu.guest_agent.0'/>
            <address type='virtio-serial' controller='0' bus='0' port='1'/>
         </channel>
         <channel type='spicevmc'>
            <target type='virtio' name='com.redhat.spice.0'/>
            <address type='virtio-serial' controller='0' bus='0' port='2'/>
         </channel>
         <input type='mouse' bus='ps2'/>
         <input type='keyboard' bus='ps2'/>
         <graphics type='spice' autoport='yes'>
            <listen type='address'/>
            <image compression='off'/>
         </graphics>
         <audio id='1' type='spice'/>
         <video>
            <model type='virtio' heads='1' primary='yes'/>
            <address type='pci' domain='0x0000' bus='0x00' slot='0x01' function='0x0'/>
         </video>
         <memballoon model='virtio'>
            <address type='pci' domain='0x0000' bus='0x05' slot='0x00' function='0x0'/>
         </memballoon>
         <rng model='virtio'>
            <backend model='random'>/dev/urandom</backend>
            <address type='pci' domain='0x0000' bus='0x06' slot='0x00' function='0x0'/>
         </rng>
      </devices>
      </domain>

      ╭─ ~/tmp/sysnix  ✔  dom@domp14s  09:38:24 
      ╰─ virsh -c qemu:///system define vm1.xml
      Domain 'vm1' defined from vm1.xml
      ```

   1. Démarrer la machine vm1
      ```shell
      ╭─ ~/tmp/sysnix  ✔  dom@domp14s  09:38:24 
      ╰─ virsh -c qemu:///system start vm1
      Domain 'vm1' started
      ```
   1. Post installation de la machine vm1
      ```shell
      ╭─ ~/tmp/sysnix  ✔  dom@domp14s  09:38:24 
      ╰─ virsh -c qemu:///system  console vm1
      Connected to domain 'vm1'
      Escape character is ^] (Ctrl + ])

      localhost login: root
      Linux localhost 6.1.0-32-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.129-1 (2025-03-06) x86_64

      The programs included with the Debian GNU/Linux system are free software;
      the exact distribution terms for each program are described in the
      individual files in /usr/share/doc/*/copyright.

      Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
      permitted by applicable law.
      Last login: Mon Apr  7 07:59:06 UTC 2025 on ttyS0
      root@localhost:~# vim /etc/hostname 
      root@localhost:~# cat /etc/hostname 
      vm1
      root@localhost:~# vim /etc/hosts 
      root@localhost:~# cat /etc/hosts 
      127.0.0.1       localhost
      127.0.1.1       vm1
      ::1             localhost ip6-localhost ip6-loopback
      ff02::1         ip6-allnodes
      ff02::2         ip6-allrouters
      root@localhost:~# reboot

      ╭─ ~/tmp/sysnix  ✔  dom@domp14s  09:38:24 
      ╰─ virsh -c qemu:///system  console vm1
      Connected to domain 'vm1'
      Escape character is ^] (Ctrl + ])

      localhost login: root
      Linux localhost 6.1.0-32-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.129-1 (2025-03-06) x86_64

      The programs included with the Debian GNU/Linux system are free software;
      the exact distribution terms for each program are described in the
      individual files in /usr/share/doc/*/copyright.

      Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
      permitted by applicable law.
      Last login: Mon Apr  7 07:59:06 UTC 2025 on ttyS0

      root@vm1:~# apt update
      root@vm1:~# apt upgrade
      root@vm1:~# apt install openssh-server

      root@vm1:~# adduser debian
      Adding user `debian' ...
      Adding new group `debian' (1000) ...
      Adding new user `debian' (1000) with group `debian (1000)' ...
      Creating home directory `/home/debian' ...
      Copying files from `/etc/skel' ...
      New password: debian
      Retype new password: debian
      passwd: password updated successfully
      Changing the user information for debian
      Enter the new value, or press ENTER for the default
         Full Name []: 
         Room Number []: 
         Work Phone []: 
         Home Phone []: 
         Other []: 
      Is the information correct? [Y/n] y
      Adding new user `debian' to supplemental / extra groups `users' ...
      Adding user `debian' to group `users' ...

      root@vm1:~# su -l debian
      debian@vm1:~$ id
      uid=1000(debian) gid=1000(debian) groups=1000(debian),100(users)

      debian@vm1:~$ exit
      logout
      root@vm1:~# exit
      logout

      Debian GNU/Linux 12 vm1 ttyS0

      vm1 login: 
      ```

1. Refaire les mêmes opération pour les machines vm2 et vm3


##  Afficher les VM

```bash
╭─ ~/tmp/sysnix  ✔  dom@domp14s  10:45:54 
╰─ virsh -c qemu:///system list
 Id   Name   State
----------------------
 15   vm1    running
 16   vm2    running
 17   vm3    running


╭─ ~/tmp/sysnix  ✔  dom@domp14s  10:46:10 
╰─ virsh -c qemu:///system domifaddr vm1
 Name       MAC address          Protocol     Address
-------------------------------------------------------------------------------
 vnet13     52:54:00:ba:2a:4a    ipv4         192.168.122.168/24


╭─ ~/tmp/sysnix  ✔  dom@domp14s  10:46:29 
╰─ virsh -c qemu:///system domifaddr vm2
 Name       MAC address          Protocol     Address
-------------------------------------------------------------------------------
 vnet14     52:54:00:15:a7:05    ipv4         192.168.122.199/24


╭─ ~/tmp/sysnix  ✔  dom@domp14s  10:46:32 
╰─ virsh -c qemu:///system domifaddr vm3
 Name       MAC address          Protocol     Address
-------------------------------------------------------------------------------
 vnet15     52:54:00:19:85:3e    ipv4         192.168.122.249/24
```

## Configuration réseau

### Création du réseau isolé

```shell
╭─ ~/tmp/sysnix  ✔  dom@domp14s  10:46:34 
╰─ virsh -c qemu:///system net-list     
 Name            State    Autostart   Persistent
--------------------------------------------------
 default         active   yes         yes

╭─ ~/tmp/sysnix  ✔  2m 33s  dom@domp14s  10:48:27 
╰─ vim net-isole.xml           

╭─ ~/tmp/sysnix  ✔  23s  dom@domp14s  10:51:20 
╰─ cat net-isole.xml
<network connections='2'>
  <name>net-isole</name>
  <bridge name='virbr10' stp='on' delay='0'/>
  <ip address='10.10.10.1' netmask='255.255.255.0'>
    <dhcp>
      <range start="10.10.10.128" end="10.10.10.254"/>
    </dhcp>
  </ip>
</network>

╭─ ~/tmp/sysnix  ✔  dom@domp14s  10:51:24 
╰─ virsh -c qemu:///system net-define ./net-isole.xml 
Network net-isole defined from ./net-isole.xml

╭─ ~/tmp/sysnix  ✔  dom@domp14s  10:53:23 
╰─ virsh -c qemu:///system net-autostart net-isole
Network net-isole marked as autostarted


╭─ ~/tmp/sysnix  ✔  dom@domp14s  10:53:36 
╰─ virsh -c qemu:///system net-start net-isole
Network net-isole started

╭─ ~/tmp/sysnix  ✔  dom@domp14s  10:53:47 
╰─ virsh -c qemu:///system net-list      
 Name            State    Autostart   Persistent
--------------------------------------------------
 default         active   yes         yes
 net-isole       active   yes         yes
```

```shell
╭─ ~/tmp/sysnix  1 ✘  dom@domp14s  10:57:32 
╰─ virsh -c qemu:///system net-dumpxml default
<network connections='3'>
  <name>default</name>
  <uuid>c5738baf-ad6b-43e5-9eb4-db0b464c4885</uuid>
  <forward mode='nat'>
    <nat>
      <port start='1024' end='65535'/>
    </nat>
  </forward>
  <bridge name='virbr0' stp='on' delay='0'/>
  <mac address='52:54:00:16:7c:ee'/>
  <domain name='default'/>
  <ip address='192.168.122.1' netmask='255.255.255.0'>
    <dhcp>
      <range start='192.168.122.128' end='192.168.122.254'/>
    </dhcp>
  </ip>
</network>

╭─ ~/tmp/sysnix  ✔  dom@domp14s  10:57:37 
╰─ virsh -c qemu:///system net-dumpxml net-isole
<network>
  <name>net-isole</name>
  <uuid>a08b4229-f4d1-4211-9345-acae8a8f4dd4</uuid>
  <bridge name="virbr10" stp="on" delay="0"/>
  <mac address="52:54:00:89:aa:ce"/>
  <ip address="10.10.10.1" netmask="255.255.255.0">
    <dhcp>
      <range start="10.10.10.128" end="10.10.10.254"/>
    </dhcp>
  </ip>
</network>
```

### Configuration réseau de la machine hôte

```bash
╭─ ~/tmp/sysnix  ✔  dom@domp14s  10:53:50 
╰─ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
...
8: virbr0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 52:54:00:16:7c:ee brd ff:ff:ff:ff:ff:ff
    inet 192.168.122.1/24 brd 192.168.122.255 scope global virbr0
       valid_lft forever preferred_lft forever
...
187: virbr10: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default qlen 1000
    link/ether 52:54:00:89:aa:ce brd ff:ff:ff:ff:ff:ff
    inet 10.10.10.1/24 brd 10.10.10.255 scope global virbr10
       valid_lft forever preferred_lft forever
```

### Configuration réseau de la machine vm1

#### Configuration matériel
```bash
╭─ ~/tmp/sysnix  ✔  dom@domp14s  10:57:42 
╰─ virsh -c qemu:///system dumpxml vm1          
<domain type='kvm' id='15'>
  <name>vm1</name>
...
  <devices>
    <emulator>/usr/bin/qemu-system-x86_64</emulator>
    <disk type='block' device='disk'>
      <driver name='qemu' type='raw' cache='none' io='native' discard='unmap'/>
      <source dev='/dev/domp14s-vg/vm1disk' index='1'/>
      <backingStore/>
      <target dev='vda' bus='virtio'/>
      <alias name='virtio-disk0'/>
      <address type='pci' domain='0x0000' bus='0x04' slot='0x00' function='0x0'/>
    </disk>
...
    <interface type='network'>
      <mac address='52:54:00:ba:2a:4a'/>
      <source network='default' portid='cce613f1-3d60-45aa-b6cd-c37bece54ef5' bridge='virbr0'/>
      <target dev='vnet13'/>
      <model type='virtio'/>
      <alias name='net0'/>
      <address type='pci' domain='0x0000' bus='0x01' slot='0x00' function='0x0'/>
    </interface>
...
  </devices>
...
</domain>
```

#### configuration du système d'exploitation

```bash
root@vm1:~# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host noprefixroute 
       valid_lft forever preferred_lft forever
2: enp1s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 52:54:00:ba:2a:4a brd ff:ff:ff:ff:ff:ff
    inet 192.168.122.168/24 metric 100 brd 192.168.122.255 scope global dynamic enp1s0
       valid_lft 2285sec preferred_lft 2285sec
    inet6 fe80::5054:ff:feba:2a4a/64 scope link 
       valid_lft forever preferred_lft forever

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
        all-eth:
            match:
                name: eth*
            dhcp4: true
            dhcp4-overrides:
                use-domains: true
            dhcp6: true
            dhcp6-overrides:
                use-domains: true
```

### Configuration réseau de la machine vm2

#### Configuration matériel

```bash
╭─ ~/tmp/sysnix  ✔  dom@domp14s  11:14:18 
╰─ virsh -c qemu:///system dumpxml vm2
<domain type='kvm' id='19'>
  <name>vm2</name>
...
  <devices>
    <emulator>/usr/bin/qemu-system-x86_64</emulator>
    <disk type='block' device='disk'>
      <driver name='qemu' type='raw' cache='none' io='native' discard='unmap'/>
      <source dev='/dev/domp14s-vg/vm2disk' index='1'/>
      <backingStore/>
      <target dev='vda' bus='virtio'/>
      <alias name='virtio-disk0'/>
      <address type='pci' domain='0x0000' bus='0x04' slot='0x00' function='0x0'/>
    </disk>
...
    <interface type='network'>
      <mac address='52:54:00:15:a7:05'/>
      <source network='net-isole' portid='887a8a7a-12d2-461f-8367-3329dffad9ea' bridge='virbr10'/>
      <target dev='vnet17'/>
      <model type='virtio'/>
      <alias name='net0'/>
      <address type='pci' domain='0x0000' bus='0x01' slot='0x00' function='0x0'/>
    </interface>
...
  </devices>
...
</domain>
```

#### configuration du système d'exploitation

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
       valid_lft 3578sec preferred_lft 3578sec
    inet6 fe80::5054:ff:fe15:a705/64 scope link 
       valid_lft forever preferred_lft forever
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
        all-eth:
            match:
                name: eth*
            dhcp4: true
            dhcp4-overrides:
                use-domains: true
            dhcp6: true
            dhcp6-overrides:
                use-domains: true
```

### Configuration réseau de la machine vm3

#### Configuration matériel

```bash
╭─ ~/tmp/sysnix  ✔  dom@domp14s  11:14:28 
╰─ virsh -c qemu:///system dumpxml vm3
<domain type='kvm'>
  <name>vm3</name>
...
  <devices>
    <emulator>/usr/bin/qemu-system-x86_64</emulator>
    <disk type='block' device='disk'>
      <driver name='qemu' type='raw' cache='none' io='native' discard='unmap'/>
      <source dev='/dev/domp14s-vg/vm3disk'/>
      <target dev='vda' bus='virtio'/>
      <address type='pci' domain='0x0000' bus='0x04' slot='0x00' function='0x0'/>
    </disk>
...
    <interface type='network'>
      <mac address='52:54:00:19:85:3e'/>
      <source network='default'/>
      <model type='virtio'/>
      <address type='pci' domain='0x0000' bus='0x01' slot='0x00' function='0x0'/>
    </interface>
    <interface type='network'>
      <mac address='52:54:00:cb:30:7f'/>
      <source network='net-isole'/>
      <model type='virtio'/>
      <address type='pci' domain='0x0000' bus='0x07' slot='0x00' function='0x0'/>
    </interface>
...
  </devices>
</domain>
```
#### Configuration des dhcp pour la distribution des bonnes adresses ip à la machine vm3

```shell
╭─ ~/tmp/sysnix  ✔  dom@domp14s  11:26:37 
╰─ virsh -c qemu:///system net-dumpxml default
<network>
  <name>default</name>
  <uuid>c5738baf-ad6b-43e5-9eb4-db0b464c4885</uuid>
  <forward mode='nat'>
    <nat>
      <port start='1024' end='65535'/>
    </nat>
  </forward>
  <bridge name='virbr0' stp='on' delay='0'/>
  <mac address='52:54:00:16:7c:ee'/>
  <domain name='default'/>
  <ip address='192.168.122.1' netmask='255.255.255.0'>
    <dhcp>
      <range start='192.168.122.128' end='192.168.122.250'/>
      <host mac='52:54:00:19:85:3e' name='vm3' ip='192.168.122.254'/>
    </dhcp>
  </ip>
</network>


╭─ ~/tmp/sysnix  ✔  dom@domp14s  11:26:48 
╰─ virsh -c qemu:///system net-dumpxml net-isole
<network>
  <name>net-isole</name>
  <uuid>a08b4229-f4d1-4211-9345-acae8a8f4dd4</uuid>
  <bridge name='virbr10' stp='on' delay='0'/>
  <mac address='52:54:00:89:aa:ce'/>
  <ip address='10.10.10.1' netmask='255.255.255.0'>
    <dhcp>
      <range start='10.10.10.128' end='10.10.10.254'/>
      <host mac='52:54:00:cb:30:7f' name='vm3' ip='10.10.10.2'/>
    </dhcp>
  </ip>
</network>

```

#### configuration du système d'exploitation

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
       valid_lft 3505sec preferred_lft 3505sec
    inet6 fe80::5054:ff:fe19:853e/64 scope link 
       valid_lft forever preferred_lft forever
3: enp7s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 52:54:00:cb:30:7f brd ff:ff:ff:ff:ff:ff
    inet 10.10.10.2/24 metric 100 brd 10.10.10.255 scope global dynamic enp7s0
       valid_lft 3505sec preferred_lft 3505sec
    inet6 fe80::5054:ff:fecb:307f/64 scope link 
       valid_lft forever preferred_lft forever

root@vm3:~# cat /etc/netplan/90-default.yaml 
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
        all-eth:
            match:
                name: eth*
            dhcp4: true
            dhcp4-overrides:
                use-domains: true
            dhcp6: true
            dhcp6-overrides:
                use-domains: true


root@vm3:~# netplan status
     Online state: online
    DNS Addresses: 192.168.122.1 (compat)
                   10.10.10.1 (compat)
       DNS Search: default

●  1: lo ethernet UNKNOWN/UP (unmanaged)
      MAC Address: 00:00:00:00:00:00
        Addresses: 127.0.0.1/8
                   ::1/128

●  2: enp1s0 ethernet UP (networkd: all-en)
      MAC Address: 52:54:00:19:85:3e (Red Hat, Inc.)
        Addresses: 192.168.122.254/24 (dhcp)
                   fe80::5054:ff:fe19:853e/64 (link)
    DNS Addresses: 192.168.122.1
       DNS Search: default
           Routes: default via 192.168.122.1 from 192.168.122.254 metric 100 
(dhcp)
                   192.168.122.0/24 from 192.168.122.254 metric 100 (link)
                   192.168.122.1 from 192.168.122.254 metric 100 (dhcp, link)
                   fe80::/64 metric 256

●  3: enp7s0 ethernet UP (networkd: all-en)
      MAC Address: 52:54:00:cb:30:7f (Red Hat, Inc.)
        Addresses: 10.10.10.2/24 (dhcp)
                   fe80::5054:ff:fecb:307f/64 (link)
    DNS Addresses: 10.10.10.1
           Routes: 10.10.10.0/24 from 10.10.10.2 metric 100 (link)
                   10.10.10.1 from 10.10.10.2 metric 100 (dhcp, link)
                   fe80::/64 metric 256

```

## État du réseau après la configuration

```bash
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


## Connexion via ssh aux conteneurs et machine

### Connection ssh, Hôte -> vm1 -> vm3 -> vm2

```
hôte ---> vm1 ---> vm3 ---> vm2
     ssh     ssh     ssh
```
* hôte --> vm1

   ```bash
   ╭─ ~/tmp/sysnix  ✔  dom@domp14s  12:11:16 
   ╰─ ssh debian@192.168.122.177
   The authenticity of host '192.168.122.177 (192.168.122.177)' can't be established.
   ED25519 key fingerprint is SHA256:1WzFlWkm1suv4eSfzLfgetGsqHXay15hbl5dVgsmdBU.
   This key is not known by any other names
   Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
   Warning: Permanently added '192.168.122.177' (ED25519) to the list of known hosts.
   debian@192.168.122.177's password: 
   Linux vm1 6.1.0-32-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.129-1 (2025-03-06) x86_64

   The programs included with the Debian GNU/Linux system are free software;
   the exact distribution terms for each program are described in the
   individual files in /usr/share/doc/*/copyright.

   Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
   permitted by applicable law.
   Last login: Mon Apr  7 10:04:24 2025 from 192.168.122.168
   debian@vm1:~$
   ```

* vm1 --> vm3

   ```bash
   debian@vm1:~$ ssh debian@192.168.122.254
   The authenticity of host '192.168.122.254 (192.168.122.254)' can't be established.
   ED25519 key fingerprint is SHA256:d/CV/EUOY+JevqrhT6fcOHiXl83tcaznkgvJj9TdOuE.
   This key is not known by any other names.
   Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
   Warning: Permanently added '192.168.122.254' (ED25519) to the list of known hosts.
   debian@192.168.122.254's password: 
   Linux vm3 6.1.0-32-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.129-1 (2025-03-06) x86_64

   The programs included with the Debian GNU/Linux system are free software;
   the exact distribution terms for each program are described in the
   individual files in /usr/share/doc/*/copyright.

   Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
   permitted by applicable law.
   Last login: Mon Apr  7 08:45:13 2025
   debian@vm3:~$ 
   ```

* vm3 --> vm2

   ```bash
   debian@vm3:~$ ssh debian@10.10.10.199
   The authenticity of host '10.10.10.199 (10.10.10.199)' can't be established.
   ED25519 key fingerprint is SHA256:1kxFSco+y1heJMgl59SUXVEV208FWKQ3leHM6UfRxYA.
   This key is not known by any other names.
   Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
   Warning: Permanently added '10.10.10.199' (ED25519) to the list of known hosts.
   debian@10.10.10.199's password: 
   Linux vm2 6.1.0-32-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.129-1 (2025-03-06) x86_64

   The programs included with the Debian GNU/Linux system are free software;
   the exact distribution terms for each program are described in the
   individual files in /usr/share/doc/*/copyright.

   Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
   permitted by applicable law.
   Last login: Mon Apr  7 08:42:38 2025
   debian@vm2:~$
   ```

### connection de vm1 --> vm2 avec un ssh jump

```bash
debian@vm1:~$ ssh -J debian@192.168.122.254  debian@10.10.10.199
debian@192.168.122.254's password: 
The authenticity of host '10.10.10.199 (<no hostip for proxy command>)' can't be established.
ED25519 key fingerprint is SHA256:1kxFSco+y1heJMgl59SUXVEV208FWKQ3leHM6UfRxYA.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.10.199' (ED25519) to the list of known hosts.
debian@10.10.10.199's password: 
Linux vm2 6.1.0-32-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.129-1 (2025-03-06) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Mon Apr  7 11:13:56 2025 from 10.10.10.2
debian@vm2:~$
```

### tunnel ssh, vm1 -> vm2 via vm3 (tunnel) 

```
vm1 ------------------> vm2
       vm3 (tunnel)
   localhost:2222
```

* Création du tunnel. Le début du tunnel est localhost:2222 (vm1) et la sortie du tunnel est 10.10.10.199:22 (vm2) à travers la machine 192.168.122.254 (vm3)

   ```bash
   debian@vm1:~$ ssh -N -L2222:10.10.10.199:22 debian@192.168.122.254
   debian@192.168.122.254's password: 
   ```

* Mettre le processus en tâche de fond, presser CRTL-Z pour suspendre le processus

   ```bash
   ^Z
   [1]+  Stopped                 ssh -N -L2222:10.10.10.199:22 debian@192.168.122.254
   debian@vm1:~$ bg
   [1]+ ssh -N -L2222:10.10.10.199:22 debian@192.168.122.254 &
   debian@vm1:~$ jobs
   [1]+  Running                 ssh -N -L2222:10.10.10.199:22 debian@192.168.122.254 &
   ```

* Se connecter à test en entrant de le tunnel

   ```bash
   debian@vm1:~$ ssh debian@localhost -p 2222
   The authenticity of host '[localhost]:2222 ([::1]:2222)' can't be established.
   ED25519 key fingerprint is SHA256:1kxFSco+y1heJMgl59SUXVEV208FWKQ3leHM6UfRxYA.
   This host key is known by the following other names/addresses:
      ~/.ssh/known_hosts:4: [hashed name]
   Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
   Warning: Permanently added '[localhost]:2222' (ED25519) to the list of known hosts.
   debian@localhost's password: 
   Linux vm2 6.1.0-32-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.129-1 (2025-03-06) x86_64

   The programs included with the Debian GNU/Linux system are free software;
   the exact distribution terms for each program are described in the
   individual files in /usr/share/doc/*/copyright.

   Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
   permitted by applicable law.
   Last login: Mon Apr  7 11:15:09 2025 from 10.10.10.2
   debian@vm2:~$
   ```

* Arrêt du tunnel

   ```shell
   debian@vm1:~$ jobs
   [1]+  Running                 ssh -N -L2222:10.10.10.199:22 debian@192.168.122.254 &
   debian@vm1:~$ kill %1
   [1]+  Done                    ssh -N -L2222:10.10.10.199:22 debian@192.168.122.254
   ```

## Connexion ssh sans mot de passe

### Configurer vm1 et vm3 pour que vm1 puisse se connecter à vm3 sans saisir de mot de passe. 

* Création des clés d'authentification

   ```bash
   debian@vm1:~$ ssh-keygen
   Generating public/private rsa key pair.
   Enter file in which to save the key (/home/debian/.ssh/id_rsa): 
   Enter passphrase (empty for no passphrase): 
   Enter same passphrase again: 
   Your identification has been saved in /home/debian/.ssh/id_rsa
   Your public key has been saved in /home/debian/.ssh/id_rsa.pub
   The key fingerprint is:
   SHA256:LAoN2tFHGgwiWSIlszArioO4apN829bI0dEi81nSxiM debian@vm1
   The key's randomart image is:
   +---[RSA 3072]----+
   |X++o. .          |
   |=O ..+           |
   |+ o o . +        |
   |*o + + E B       |
   |B o . * S .      |
   | o . o =         |
   |o . o +          |
   |.= ..+ .         |
   |o o.o.           |
   +----[SHA256]-----+
   ```

* copie de la clé public sur vm3

   ```bash
   debian@vm1:~$ ssh-copy-id debian@192.168.122.254
   /usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/home/debian/.ssh/id_rsa.pub"
   /usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
   /usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys
   debian@192.168.122.254's password: 

   Number of key(s) added: 1

   Now try logging into the machine, with:   "ssh 'debian@192.168.122.254'"
   and check to make sure that only the key(s) you wanted were added.

   debian@vm1:~$
   ```

* vérification de la connexion 

   ```bash
   debian@vm1:~$ ssh -v debian@192.168.122.254
   OpenSSH_9.2p1 Debian-2+deb12u5, OpenSSL 3.0.15 3 Sep 2024
   debug1: Reading configuration data /etc/ssh/ssh_config
   debug1: /etc/ssh/ssh_config line 19: include /etc/ssh/ssh_config.d/*.conf matched no files
   debug1: /etc/ssh/ssh_config line 21: Applying options for *
   debug1: Connecting to 192.168.122.254 [192.168.122.254] port 22.
   debug1: Connection established.
   debug1: identity file /home/debian/.ssh/id_rsa type 0
   debug1: identity file /home/debian/.ssh/id_rsa-cert type -1
   debug1: identity file /home/debian/.ssh/id_ecdsa type -1
   debug1: identity file /home/debian/.ssh/id_ecdsa-cert type -1
   debug1: identity file /home/debian/.ssh/id_ecdsa_sk type -1
   debug1: identity file /home/debian/.ssh/id_ecdsa_sk-cert type -1
   debug1: identity file /home/debian/.ssh/id_ed25519 type -1
   debug1: identity file /home/debian/.ssh/id_ed25519-cert type -1
   debug1: identity file /home/debian/.ssh/id_ed25519_sk type -1
   debug1: identity file /home/debian/.ssh/id_ed25519_sk-cert type -1
   debug1: identity file /home/debian/.ssh/id_xmss type -1
   debug1: identity file /home/debian/.ssh/id_xmss-cert type -1
   debug1: identity file /home/debian/.ssh/id_dsa type -1
   debug1: identity file /home/debian/.ssh/id_dsa-cert type -1
   debug1: Local version string SSH-2.0-OpenSSH_9.2p1 Debian-2+deb12u5
   debug1: Remote protocol version 2.0, remote software version OpenSSH_9.2p1 Debian-2+deb12u5
   debug1: compat_banner: match: OpenSSH_9.2p1 Debian-2+deb12u5 pat OpenSSH* compat 0x04000000
   debug1: Authenticating to 192.168.122.254:22 as 'debian'
   debug1: load_hostkeys: fopen /home/debian/.ssh/known_hosts2: No such file or directory
   debug1: load_hostkeys: fopen /etc/ssh/ssh_known_hosts: No such file or directory
   debug1: load_hostkeys: fopen /etc/ssh/ssh_known_hosts2: No such file or directory
   debug1: SSH2_MSG_KEXINIT sent
   debug1: SSH2_MSG_KEXINIT received
   debug1: kex: algorithm: sntrup761x25519-sha512
   debug1: kex: host key algorithm: ssh-ed25519
   debug1: kex: server->client cipher: chacha20-poly1305@openssh.com MAC: <implicit> compression: none
   debug1: kex: client->server cipher: chacha20-poly1305@openssh.com MAC: <implicit> compression: none
   debug1: expecting SSH2_MSG_KEX_ECDH_REPLY
   debug1: SSH2_MSG_KEX_ECDH_REPLY received
   debug1: Server host key: ssh-ed25519 SHA256:d/CV/EUOY+JevqrhT6fcOHiXl83tcaznkgvJj9TdOuE
   debug1: load_hostkeys: fopen /home/debian/.ssh/known_hosts2: No such file or directory
   debug1: load_hostkeys: fopen /etc/ssh/ssh_known_hosts: No such file or directory
   debug1: load_hostkeys: fopen /etc/ssh/ssh_known_hosts2: No such file or directory
   debug1: Host '192.168.122.254' is known and matches the ED25519 host key.
   debug1: Found key in /home/debian/.ssh/known_hosts:1
   debug1: ssh_packet_send2_wrapped: resetting send seqnr 3
   debug1: rekey out after 134217728 blocks
   debug1: SSH2_MSG_NEWKEYS sent
   debug1: expecting SSH2_MSG_NEWKEYS
   debug1: ssh_packet_read_poll2: resetting read seqnr 3
   debug1: SSH2_MSG_NEWKEYS received
   debug1: rekey in after 134217728 blocks
   debug1: Will attempt key: /home/debian/.ssh/id_rsa RSA SHA256:LAoN2tFHGgwiWSIlszArioO4apN829bI0dEi81nSxiM
   debug1: Will attempt key: /home/debian/.ssh/id_ecdsa 
   debug1: Will attempt key: /home/debian/.ssh/id_ecdsa_sk 
   debug1: Will attempt key: /home/debian/.ssh/id_ed25519 
   debug1: Will attempt key: /home/debian/.ssh/id_ed25519_sk 
   debug1: Will attempt key: /home/debian/.ssh/id_xmss 
   debug1: Will attempt key: /home/debian/.ssh/id_dsa 
   debug1: SSH2_MSG_EXT_INFO received
   debug1: kex_input_ext_info: server-sig-algs=<ssh-ed25519,sk-ssh-ed25519@openssh.com,ecdsa-sha2-nistp256,ecdsa-sha2-nistp384,ecdsa-sha2-nistp521,sk-ecdsa-sha2-nistp256@openssh.com,webauthn-sk-ecdsa-sha2-nistp256@openssh.com,ssh-dss,ssh-rsa,rsa-sha2-256,rsa-sha2-512>
   debug1: kex_input_ext_info: publickey-hostbound@openssh.com=<0>
   debug1: SSH2_MSG_SERVICE_ACCEPT received
   debug1: Authentications that can continue: publickey,password
   debug1: Next authentication method: publickey
   debug1: Offering public key: /home/debian/.ssh/id_rsa RSA SHA256:LAoN2tFHGgwiWSIlszArioO4apN829bI0dEi81nSxiM
   debug1: Server accepts key: /home/debian/.ssh/id_rsa RSA SHA256:LAoN2tFHGgwiWSIlszArioO4apN829bI0dEi81nSxiM
   Authenticated to 192.168.122.254 ([192.168.122.254]:22) using "publickey".
   debug1: channel 0: new session [client-session] (inactive timeout: 0)
   debug1: Requesting no-more-sessions@openssh.com
   debug1: Entering interactive session.
   debug1: pledge: filesystem
   debug1: client_input_global_request: rtype hostkeys-00@openssh.com want_reply 0
   debug1: client_input_hostkeys: searching /home/debian/.ssh/known_hosts for 192.168.122.254 / (none)
   debug1: client_input_hostkeys: searching /home/debian/.ssh/known_hosts2 for 192.168.122.254 / (none)
   debug1: client_input_hostkeys: hostkeys file /home/debian/.ssh/known_hosts2 does not exist
   debug1: client_input_hostkeys: no new or deprecated keys from server
   debug1: Remote: /home/debian/.ssh/authorized_keys:1: key options: agent-forwarding port-forwarding pty user-rc x11-forwarding
   debug1: Remote: /home/debian/.ssh/authorized_keys:1: key options: agent-forwarding port-forwarding pty user-rc x11-forwarding
   debug1: Sending environment.
   debug1: channel 0: setting env LANG = "C.UTF-8"
   debug1: pledge: fork
   Linux vm3 6.1.0-32-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.129-1 (2025-03-06) x86_64

   The programs included with the Debian GNU/Linux system are free software;
   the exact distribution terms for each program are described in the
   individual files in /usr/share/doc/*/copyright.

   Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
   permitted by applicable law.
   Last login: Mon Apr  7 11:34:25 2025 from 192.168.122.177
   debian@vm3:~$
   ```

### De le cas où l'authorisation par mot de passe est désactivié sur vm3

1. Envoyer la clé publique (id_rsa.pub) à l'administrateur
   ```shell
   debian@vm1:~$ ls ~/.ssh/
   id_rsa	id_rsa.pub  known_hosts  known_hosts.old
   debian@vm1:~$ scp /home/debian/.ssh/id_rsa.pub debian@192.168.122.254:/home/debian
   id_rsa.pub                                    100%  564   230.2KB/s   00:00    
   ```
1. Ajouter le contenu du fichier pub dans le fichier ~/.ssh/authorized_key
   ```shell
   debian@vm3:~$ ls ~
   id_rsa.pub
   debian@vm3:~$ cat id_rsa.pub >> ~/.ssh/authorized_keys
   debian@vm3:~$ cat ~/.ssh/authorized_keys 
   ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCZAWjh5HPR7PJGHxpVhqJ2//mpjQ46RC0iU2VqHkhCZDQQGzkE0rpLp8bohG02Sw3zrcbg1aBpSRyXoYGCMBNBqxHJMX9crzo9t205yVBcVFTf2C4N6/vu4RbzdXanvt8Rd2mjP0Rk3U8drvHKxHQXmt2KXoNmU4F1KCnuKHA1Q5w9LPnqJC8cnCzAUEeVRPcIqEHwTXclLUjNKYsLccIrBHOlBSvpFmMyfNweFyAAtoD5hZwv3l57x1b19jsXT55TwJpO/BbGUnVT4rEyVeVvwiscblPE25JdxC+86Qh721hrqtF5FTUW6DWl/r99TEGumK47eYPM6OS17VzJQRsoR0PtRKwT26mUIf91/TVeuDizAGb0tNMhvXTqzoq+gjFo7OPlXVcrESxbmVowwToDXx1o6zSQzmKKBsXyXurZ0AdusBf2a7YcQ3g1tTDwiKteaQORfhTCn2su2CPfx55e8mJrPfH3exiJ2hMe+gGQ+SSKBeyz+IW3byQdttOAlqk= debian@vm1
   debian@vm3:~$ cat id_rsa.pub >> ~/.ssh/authorized_keys
   ```
   
## Références

1.  Accéder à un serveur distant à travers un tunnel SSH,  [tunnel-ssh][1]
1. [TUTORIALS ET FORMATION SSH - xavki](https://www.youtube.com/playlist?list=PLn6POgpklwWp0emQkznjREGn0SEkQYA6p)

[1]:http://mylos.cifom.ch/cours/int-sys1-nix/fiches/tunnel-ssh/
