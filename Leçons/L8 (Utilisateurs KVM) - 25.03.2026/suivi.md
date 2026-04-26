# Leçon 08 - 2026-03-25 (5p)

## Gestion des utilisateurs

1. [Activités, série 0008 - Gestion des utilisateurs](<../../Cours_Mylos/site/cours/int-sys1-nix/activites/sysnix-activite-0008-gestion-utilisateurs/index.html>)
    * [Éléments de solutions](<../../Cours_Mylos/wiki/elements-de-solution/sysnix-activite-0008-gestion-utilisateurs.md>)

## Script

* [Activités, série 0006 - Script](<../../Cours_Mylos/site/cours/int-sys1-nix/activites/sysnix-activite-0006-script/index.html>)

## Exemple de fonction en ligne de commande 

* compte de 1 à 10

  ```bash
  dom@domp14s:tmp$ for i in $(seq 1 10); do echo $i; done
  1
  2
  3
  4
  5
  6
  7
  8
  9
  10
  ```

* déclare la fonction `compteur` permettant de compter de 1 à 10   

  ```bash
  dom@domp14s:tmp$ compteur() { for i in $(seq 1 10); do echo $i; done }
  ```

* appel la fonction `compteur`  

  ```bash
  dom@domp14s:tmp$ compteur
  1
  2
  3
  4
  5
  6
  7
  8
  9
  10
  ```

* affiche la déclaration de la fonction `compteur`

  ```bash
  dom@domp14s:tmp$ type compteur
  compteur est une fonction
  compteur () 
  { 
      for i in $(seq 1 10);
      do
          echo $i;
      done
  }
  ```

* script contenant la fonction `compteur`

  ```bash
  huguenindo@mc0-0315-00:tmp$ cat test.sh 
  #!/bin/bash

  monCompteur() { 
    for i in $(seq 1 ${1}); do 
      echo $i 
    done 
  }

  monCompteur 100
  ```


* déclare une fonction `compteurRecursif` permettant de compter de 1 à 10   

  ```bash
  dom@domp14s:tmp$ compteurRecursif() { i="$1"; if [ -z "$i" ]; then i=1; fi; if [ $i -le 10 ]; then  echo $i ; compteurRecursif $(($i+1)); fi }
  ```

* appel la fonction `compteurRecursif`  

  ```
  dom@domp14s:tmp$ compteurRecursif
  1
  2
  3
  4
  5
  6
  7
  8
  9
  10
  ```

* affiche la déclaration de la fonction `compteurRecursif`

  ```
  dom@domp14s:tmp$ type compteurRecursif
  compteurRecursif est une fonction
  compteurRecursif () 
  { 
      i="$1";
      if [ -z "$i" ]; then
          i=1;
      fi;
      if [ $i -le 10 ]; then
          echo $i;
          compteurRecursif $(($i+1));
      fi
  }
  ```


## Virtualisation kvm

* installation kvm, libvirt sur le système du disque amovible
* [SYSNIX - Virtualisation](<../../Cours_Mylos/site/cours/int-sys1-nix/virtualisation/index.html>)
    1. [Virtualisation - libvirt+KVM, installation et configuration](<../../Cours_Mylos/site/cours/int-sys1-nix/virtualisation/virtualisation-kvm-libvirt/index.html>)
        1. Créer 2 VM selon la vidéo [Virtualisation, création d'une machine virtuelle Debian 12 avec libvirt](<../../Cours_Mylos/site/cours/int-sys1-nix/fiches/virtualisation-libvirt/index.html>) ou la vidéo [Virtualisation, création d'une machine virtuelle Debian 12 avec virt-manager](<../../Cours_Mylos/site/cours/int-sys1-nix/fiches/virtualisation-virt-manager/index.html>) 
            1. **vm1** *debian trixie*, stockage dans un fichier **raw** de **6G**, partitionnement "**assisté - utiliser un disque entier**"
            1. **vm2** *debian trixie*, stockage dans un fichier **raw** de **6G**, partitionnement "**assisté - utiliser tout un disque avec LVM**"
   1. accès à la vm
      1. [Virtualisation, Activation de l'accès à la console texte de VM KVM](<../../Cours_Mylos/site/cours/int-sys1-nix/fiches/virtualisation-console-virsh/index.html>)
      1. [Virtualisation, Accès à la VM avec la console ou le client SSH](<../../Cours_Mylos/site/cours/int-sys1-nix/fiches/virtualisation-console-vs-ssh/index.html>)
   1. [Activités, série 0500 - Libvirt + kvm + lvm](<../../Cours_Mylos/site/cours/int-sys1-nix/activites/sysnix-activite-0500-libvirt-kvm-lvm/index.html>)
         1. KVM - Cloner
            1. vm1 -> vm1b
      1. KVM - Cloner dans une LV
         1. vm1 -> vm3
         1. vm2 -> vm4


## A faire

* [Activités, série 0006 - Script](<../../Cours_Mylos/site/cours/int-sys1-nix/activites/sysnix-activite-0006-script/index.html>)
   * faire le script "Génération d'un projet en java"
1. configurer sur les machines vm1 et vm2 l'accès à la console texte. [Virtualisation, Activation de l'accès à la console texte de VM KVM](<../../Cours_Mylos/site/cours/int-sys1-nix/fiches/virtualisation-console-virsh/index.html>)
1. [Activités, série 0500 - Libvirt + kvm + lvm](<../../Cours_Mylos/site/cours/int-sys1-nix/activites/sysnix-activite-0500-libvirt-kvm-lvm/index.html>)
      1. KVM - Cloner
         1. vm1 -> vm1b
   1. KVM - Cloner dans une LV
      1. vm1 -> vm3
      1. vm2 -> vm4
   
## Notes

```
huguenindo@lozan0:~$ echo $moninvite

huguenindo@lozan0:~$ cd test
huguenindo@lozan0:test$ cat monScript
moninvite="bienvenue au cours SysNix"
echo $moninvite
huguenindo@lozan0:test$ monScript
bienvenue au cours SysNix
huguenindo@lozan0:test$ whereis monScript
monScript: /home/huguenindo/bin/monScript
huguenindo@lozan0:test$ monScript
bienvenue au cours SysNix
huguenindo@lozan0:test$ echo $moninvite

huguenindo@lozan0:test$ source monScript
bienvenue au cours SysNix
huguenindo@lozan0:test$ echo $moninvite
bienvenue au cours SysNix

huguenindo@lozan0:test$ cat AffVar 
#!/bin/bash
if [ -n "$ma_var" ]; then
  echo $ma_var
else
  echo "la variable 'ma_var' est vide!"
fi
huguenindo@lozan0:test$ ./AffVar 
la variable 'ma_var' est vide!
huguenindo@lozan0:test$ ma_var='coucou'
huguenindo@lozan0:test$ ./AffVar 
la variable 'ma_var' est vide!
huguenindo@lozan0:test$ export ma_var
huguenindo@lozan0:test$ ./AffVar 
coucou

```

![xournal](<../../Cours_Mylos/wiki/xournal/2026-03-25-Note-08-30_annoté.svg>)
