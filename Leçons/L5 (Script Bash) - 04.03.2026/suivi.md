# Leçon 05 - 2026-03-04 (5p)

* [Le shell](<../../Cours_Mylos/site/cours/int-sys1-nix/shell/index.html>)
   1. [Gestion des permissions](<../../Cours_Mylos/site/cours/int-sys1-nix/shell/gestion-acces/index.html>)
      * question?
   1. [Activités, série 0004 - Gestion des accès](<../../Cours_Mylos/site/cours/int-sys1-nix/activites/sysnix-activite-0004-gestion-acces/index.html>)
   1. [Gestion des utilisateurs et des groupes](<../../Cours_Mylos/site/cours/int-sys1-nix/mise-en-route-systeme-exploitation/user-group/index.html>)
      * Création d'un utilisateur guest manuellement   
      * ajouter l'utilisateur guest dans votre groupe initial

        ```
        huguenindo@debian-usb:~$ id guest
        uid=1002(guest) gid=1002(guest) groupes=1002(guest),100(users)
        huguenindo@debian-usb:~$ sudo adduser guest huguenindo
        Ajout de l'utilisateur « guest » au groupe « huguenindo » ...
        Fait.
        huguenindo@debian-usb:~$ id guest
        uid=1002(guest) gid=1002(guest) groupes=1002(guest),100(users),1000(huguenindo)
        ```

## Script

* [Script Bash](<../../Cours_Mylos/site/cours/int-sys1-nix/shell/bash-script/index.html>)
    * [Bash, commandes internes](<../../Cours_Mylos/site/cours/int-sys1-nix/shell/bash-builtin/index.html>)
    * [Langage de programmation Bash](<../../Cours_Mylos/site/cours/int-sys1-nix/shell/bash-script-langage/index.html>)
* [Activités, série 0006 - Script](<../../Cours_Mylos/site/cours/int-sys1-nix/activites/sysnix-activite-0006-script/index.html>)

>Vérifier la syntax des script avec shellcheck
>
>```
>$ sudo apt install shellcheck
>```
>


## A faire

1. terminer `Application des permissions` [Activités, série 0004 - Gestion des accès](<../../Cours_Mylos/site/cours/int-sys1-nix/activites/sysnix-activite-0004-gestion-acces/index.html>)
1. faire l'[Activités, série 0006 - Script](<../../Cours_Mylos/site/cours/int-sys1-nix/activites/sysnix-activite-0006-script/index.html>)
    1. faire les scripts suivant:
        1. Table de multiplication
        1. Carré de multiplication
        1. Génération d’un projet en java

**1h max**

>Pensez au Here Document https://tldp.org/LDP/abs/html/here-docs.html

## Notes
