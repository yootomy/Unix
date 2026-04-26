# Leçon 06 - 2026-03-11 (5p)

>virtualisation - kvm

>Système d'exploitation

## Virtualisation kvm

* [Debian -- Obtenir Debian](https://www.debian.org/distrib/)
    * distribuer les archives contenues sur la clé usb
* [SYSNIX - Virtualisation](<../../Cours_Mylos/site/cours/int-sys1-nix/virtualisation/index.html>)
    * [Virtualisation - Éléments théoriques](<../../Cours_Mylos/site/cours/int-sys1-nix/virtualisation/virtualisation-theorie/index.html>)
    * [Virtualisation - Kernel-based Virtual Machine (KVM))](<../../Cours_Mylos/site/cours/int-sys1-nix/virtualisation/virtualisation-kvm/index.html>)
    * [Virtualisation - libvirt+KVM, installation et configuration](<../../Cours_Mylos/site/cours/int-sys1-nix/virtualisation/virtualisation-kvm-libvirt/index.html>)

#### Envoyer des combinaisons de touches \<CTRL>\<ALT>\<F1>

* https://askubuntu.com/questions/54814/how-can-i-ctrl-alt-f-to-get-to-a-tty-in-a-qemu-session

    ```
    <CTRL><ALT><2>

    (qemu) sendkey ctrl-alt-f1

    <CTRL><ALT><1>
    ```

## Manipulation

* vidéo [Virtualisation, Création d'une machine virtuelle Debian 12 avec qemu](<../../Cours_Mylos/site/cours/int-sys1-nix/fiches/virtualisation-qemu/index.html>) 
* vidéo [Virtualisation, création d'une machine virtuelle Debian 12 avec libvirt](<../../Cours_Mylos/site/cours/int-sys1-nix/fiches/virtualisation-libvirt/index.html>) 
* vidéo [Virtualisation, création d'une machine virtuelle Debian 12 avec virt-manager](<../../Cours_Mylos/site/cours/int-sys1-nix/fiches/virtualisation-virt-manager/index.html>) 

## Gestion des utilisateurs

* [Mise en place du système d'exploitation](<../../Cours_Mylos/site/cours/int-sys1-nix/mise-en-route-systeme-exploitation/index.html>)
   1. [Gestion des utilisateurs et des groupes](<../../Cours_Mylos/site/cours/int-sys1-nix/mise-en-route-systeme-exploitation/user-group/index.html>)
   1. [Activités, série 0008 - Gestion des utilisateurs](<../../Cours_Mylos/site/cours/int-sys1-nix/activites/sysnix-activite-0008-gestion-utilisateurs/index.html>)


## A Faire

1. terminer `Application des permissions` [Activités, série 0004 - Gestion des accès](<../../Cours_Mylos/site/cours/int-sys1-nix/activites/sysnix-activite-0004-gestion-acces/index.html>)
1. [Activités, série 0006 - Script](<../../Cours_Mylos/site/cours/int-sys1-nix/activites/sysnix-activite-0006-script/index.html>)
    1. Valider avec `shellcheck` les convention de codage des scripts
1. [Activités, série 0008 - Gestion des utilisateurs](<../../Cours_Mylos/site/cours/int-sys1-nix/activites/sysnix-activite-0008-gestion-utilisateurs/index.html>)
    1. terminer la série

## Notes

* https://anthropic.skilljar.com/

* activation du réseau default
```
uguenindo@debian-usb:tmp$ virsh -c qemu:///system
Bienvenue dans virsh, le terminal de virtualisation interactif.

Taper :  « help » pour l’aide ou « help » avec la commande
         « quit » pour quitter

virsh # net-list --all
 Nom       État    Démarrage automatique   Persistent
-------------------------------------------------------
 default   inactif   Non                     Oui

virsh # net-start default

virsh # net-list --all
 Nom       État    Démarrage automatique   Persistent
-------------------------------------------------------
 default   actif   Non                      Oui

virsh # net-autostart default
Réseau default marqué en démarrage automatique

virsh # net-list
 Nom       État    Démarrage automatique   Persistent
-------------------------------------------------------
 default   actif   Oui                     Oui
```

```
$ virt-install --connect qemu:///system \
   -n vm1 \
   -r 1024 \
   --disk path=/tmp/vm1disk.img,format=raw,bus=virtio,size=4 \
   -c /tmp/debian-13.3.0-amd64-netinst.iso \
   --network network=default,model=virtio \
   --osinfo name=debian11 
```

* installation dans une console 
  ```
  huguenindo@debian-usb:tmp$ virt-install --connect qemu:///system \
    -n vm1 \
    -r 1024 \
    --disk path=./vm1disk.img,format=raw,bus=virtio,size=6 \
    --location ~/iso/debian-13.3.0-amd64-netinst.iso \
    --network network=default,model=virtio \
    --osinfo name=debian11 \
    --graphics none \
    --console pty,target_type=serial \
    --extra-args "console=ttyS0,115200n8"
  ```

* droit sur  l'arborescence
  ```
  huguenindo@debian-usb:tmp$ tree -dp -L 1 ~
  [drwx--x--x]  /home/huguenindo
  ...
  ├── [drwxr-xr-x]  tmp
  ...
  ```

![xournal](<../../Cours_Mylos/wiki/xournal/2026-03-11-Note-08-59-1.svg>)

![xournal](<../../Cours_Mylos/wiki/xournal/2026-03-11-Note-08-59-2.svg>)
