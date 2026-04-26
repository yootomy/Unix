# Leçon 07 - 2026-03-18 (5p)

>virtualisation - kvivm

## Installation du disque bootable

>Dans les préférences de virt-manager, activer l'édition de xml

* [Mise en place du système d'exploitation](<../../Cours_Mylos/site/cours/int-sys1-nix/mise-en-route-systeme-exploitation/index.html>)
    * rappel des manipulations des volumes logique [Partitionnement avec LVM avant l’installation](<../../Cours_Mylos/site/cours/int-sys1-nix/mise-en-route-systeme-exploitation/partitionnement-lvm-avant-installation/index.html>)
    * [SYSNIX - Debian 12, création d'un disque externe USB bootable](<../../Cours_Mylos/site/cours/int-sys1-nix/fiches/debian-12-disque-externe-bootable/index.html>)
* installation du gestionnaire de paquet `synaptic`

    ```
    $ sudo apt install synaptic
    ```

* configurer wifi

  ![config wifi](<../../Cours_Mylos/wiki/images/config-wifi-rpns2mobile.png>)

  > installation des paquets permettant de gestion du wifi
  > * wireless-tools  
  > * firmware-iwlwifi : Pour la majorité des cartes Intel.
  > * firmware-realtek : Pour les cartes Realtek (très communes sur portables).
  > * ajouter les dépôt  firmware-linux-nonfree  

* accès à teams via https://onedrive.live.com/login/ ou https://rpns2-my.sharepoint.com


## Gestion des permissions

* [Le shell](<../../Cours_Mylos/site/cours/int-sys1-nix/shell/index.html>)
   1. Corriger l'[Activités, série 0004 - Gestion des accès](<../../Cours_Mylos/site/cours/int-sys1-nix/activites/sysnix-activite-0004-gestion-acces/index.html>)
      * [Éléments de solutions](<../../Cours_Mylos/wiki/elements-de-solution/sysnix-activite-0004-gestion-acces.md>)

## Gestion des utilisateurs

* [Mise en place du système d'exploitation](<../../Cours_Mylos/site/cours/int-sys1-nix/mise-en-route-systeme-exploitation/index.html>)
   1. [Activités, série 0008 - Gestion des utilisateurs](<../../Cours_Mylos/site/cours/int-sys1-nix/activites/sysnix-activite-0008-gestion-utilisateurs/index.html>)

## A Faire

* faire fonctionner le disque USB linux sur vorte ordinateur portable
* terminer [Activités, série 0008 - Gestion des utilisateurs](<../../Cours_Mylos/site/cours/int-sys1-nix/activites/sysnix-activite-0008-gestion-utilisateurs/index.html>)
