# SYSNIX - Activité 0007 - Gestion des utilisateurs (Éléments de solution)
[[_TOC_]]

## A faire


### 2. 

Connectez-vous au système.

Afficher l’ UID, et les GID’s de l'utilisateur courant.


```
$ id
uid=1000(ubuntu) gid=1000(ubuntu) groupes=4(adm),20(dialout),24(cdrom),46(plugdev),109(lpadmin),
110(sambashare),111(admin),1000(ubuntu)
```


### 3. 

Créer les comptes pour `Jeannette` et `Lucien` avec les commandes `adduser` ou `useradd`

```
$ sudo useradd -m jeannette
$ sudo passwd jeannette
Entrez le nouveau mot de passe UNIX : [jeannette]
Retapez le nouveau mot de passe UNIX : [jeannette]
passwd: password updated successfully
$ id jeannette
uid=1001(jeannette) gid=1001(jeannette) groupes=1001(jeannette)
```

```
$ sudo useradd -m lucien
$ sudo passwd lucien
Entrez le nouveau mot de passe UNIX : [lucien]
Retapez le nouveau mot de passe UNIX : [lucien]
passwd: password updated successfully
$ id lucien
uid=1002(lucien) gid=1002(lucien) groupes=1002(lucien)
```

* Vérifier que ces comptes soient fonctionnels. 

    ```
    $ su jeannette
    Mot de passe : [jeannette]
    $ whoami
    jeannette
    ```

    ```
    $ su lucien
    Mot de passe : [lucien]
    $ whoami 
    lucien
    ```

* Vérifier les groupes auxquels appartiennent `Jeannette` et `Lucien`

    ```
    $ groups jeannette
    jeannette : jeannette
    ```

    ```
    $ groups lucien
    lucien : lucien
    ```


### 4. 

1. Ajouter les groupes `stock`, `comptabilite`, `eleves` au système.

    ```
    $ sudo -s
    # groupadd stock
    # groupadd comptabilite
    # groupadd eleves
    # exit
    ```

    ```
    $ cat /etc/group | grep -w  'stock\|comptabilite\|eleves'
    stock:x:1003:
    comptabilite:x:1004:
    eleves:x:1005:
    ```

1. Effectuer les assignations suivante pour l’utilisateur `lucien` et vérifier pour chaque situation:

    >Remarques. Le premier groupe de chaque situation est le groupe initial de lucien

    1. `users`, `stock`, `comptabilite`

        ```
        $ sudo usermod -g users -G stock,comptabilite lucien
        $ id lucien
        uid=1002(lucien) gid=100(users) groupes=100(users),1003(stock),1004(comptabilite)
        ```

    1. `stock`

        ```
        $ sudo usermod -G stock lucien
        $ sudo usermod -g stock lucien
        $ id lucien
        uid=1002(lucien) gid=1003(stock) groupes=1003(stock)
        ```

    1. `users`, stock 

        ```
        $ sudo usermod -g users lucien
        $ sudo usermod -G stock lucien
        $ id lucien
        uid=1002(lucien) gid=100(users) groupes=100(users),1003(stock)
        ```

    1. `users`, `comptabilite`

        ```
        $ sudo usermod -g users lucien
        $ sudo usermod -G comptabilite lucien
        $ id lucien
        uid=1002(lucien) gid=100(users) groupes=100(users),1004(comptabilite)
        ```

    1.  `users`, `comptabilite`, `eleves`

        ```
        $ sudo usermod -g users lucien
        $ sudo usermod -G comptabilite,eleves lucien
        $ id lucien
        uid=1002(lucien) gid=100(users) groupes=100(users),1004(comptabilite),1005(eleves)
        ```


### 5. 

>Rétablir la situation de l’exercice précèdent et connectez-vous en `lucien` au système.
>Lucien appartient aux groupes `users`, `comptabilite`
>
>```
>$ sudo usermod -g users lucien
>$ sudo usermod -G comptabilite lucien
>$ id lucien
>uid=1002(lucien) gid=100(users) groupes=100(users),1004(comptabilite)
>```
>
>```
>$ su -l lucien
>Mot de passe : [lucien]
>$ whoami
>lucien
>$ pwd
>/home/lucien
>```

1. Créez un fichier `testgroupe` dans votre répertoire personnel.

    ```
    $ touch ~/testgroupe
    ```

1. Vérifier les propriétés du fichier `testgroupe`.

    ```
    $ ls -l ~/testgroupe
    -rw-r--r-- 1 lucien users 0 2011-01-24 11:43 /home/lucien/testgroupe
    ```

1. Changer l’appartenance du fichier `testgroupe` au groupe `comptabilite`. Constatations ?

    ```
    $ chgrp comptabilite ~/testgroupe
    $ ls -l ~/testgroupe
    -rw-r--r-- 1 lucien comptabilite 0 2011-01-24 11:43 /home/lucien/testgroupe
    ```

1. Changer l’appartenance du fichier `testgroupe` au groupe `eleves`. Constatations ?

    ```
    $ chgrp eleves ~/testgroupe
    chgrp: modification du groupe de «/home/lucien/testgroupe»: Opération non permise
    ```


### 6.

créer les utilisateurs jack et joe et réaliser cette arborescence

```
/-home  
  +-jack  
  | `-projet  
  |   `-main_jack.cpp  
  `-joe 
     `-projet      
       `-main_joe.cpp  
```


```
$ sudo useradd -m jack
$ sudo passwd jack
Entrez le nouveau mot de passe UNIX : [jack]
Retapez le nouveau mot de passe UNIX : [jack]
passwd: password updated successfully
```

```
$ sudo useradd -m joe
$ sudo passwd joe
Entrez le nouveau mot de passe UNIX : [joe]
Retapez le nouveau mot de passe UNIX : [joe]
passwd: password updated successfully
```

```
$ su -l jack
Mot de passe : 
jack@:~$ mkdir projet
jack@:~$ touch projet/main_jack.cpp
jack@:~$ exit
logout
```

```
$ tree -pug
.
└── [drwxr-xr-x jack     jack    ]  projet
    └── [-rw-r--r-- jack     jack    ]  main_jack.cpp
```


```
$ su -l joe
Mot de passe : 
joe@:~$ mkdir projet
joe@:~$ touch projet/main_joe.cpp
joe@:~$ exit
logout
```

```
$ tree -pug
.
└── [drwxr-xr-x joe      joe     ]  projet
    └── [-rw-r--r-- joe      joe     ]  main_joe.cpp
```

Joe et Jack désirent partager leur répertoire projet respectif et les fichiers qu’il contient uniquement entre eux. (tout autre utilisateurs du système ne pourra pas y accéder)

* Indiquer les demandes à faire à l’administrateur et les commandes qu’il doit taper.

    ```
    $ sudo groupadd jackjoe
    $ cat /etc/group | grep ^jackjoe
    jackjoe:x:1008:jack,joe
    ```

    ```
    $ sudo usermod -G jackjoe jack
    $ id jack
    uid=1003(jack) gid=1006(jack) groupes=1006(jack),1008(jackjoe)
    ```

    ```
    $ sudo usermod -G jackjoe joe
    $ id joe
    uid=1004(joe) gid=1007(joe) groupes=1007(joe),1008(jackjoe)
    ```

* Indiquer les commandes que doit taper Joe.

    ```
    $ su -l joe
    Mot de passe : [joe]
    joe@:~$ chgrp -R jackjoe ~/projet
    joe@:~$ chmod -R g+rw ~/projet/
    ```

    ```
    joe@:~$ tree -pug
    .
    └── [drwxrwxr-x joe      jackjoe ]  projet
        └── [-rw-rw-r-- joe      jackjoe ]  main_joe.cpp
    ```

* Indiquer les commandes que doit taper Jack.

    ```
    $ su -l jack
    Mot de passe : [jack]
    jack@:~$  chgrp -R jackjoe ~/projet
    jack@:~$ chmod -R g+rw ~/projet/
    ```

    ```
    jack@:~$ tree -pug
    .
    └── [drwxrwxr-x jack     jackjoe ]  projet
        └── [-rw-rw-r-- jack     jackjoe ]  main_jack.cpp
    ```


* Test, Joe ajoute un fichier dans {{/home/jack/projet/main_joe.cpp}}

    ```
    $ su -l joe
    joe@:~$ touch ~jack/projet/main_joe.cpp
    joe@:~$ tree -pug ~jack
    /home/jack
    └── [drwxrwxr-x jack     jackjoe ]  projet
        ├── [-rw-rw-r-- jack     jackjoe ]  main_jack.cpp
        └── [-rw-r--r-- joe      joe     ]  main_joe.cpp
    ```

* Test, Jack ajoute un fichier dans {{/home/joe/projet/main_jack.cpp}}

    ```
    $ su -l jack
    Mot de passe : 
    jack@:~$ touch ~joe/projet/main_jack.cpp
    jack@:~$ tree -pug ~joe
    /home/joe
    └── [drwxrwxr-x joe      jackjoe ]  projet
        ├── [-rw-r--r-- jack     jack    ]  main_jack.cpp
        └── [-rw-rw-r-- joe      jackjoe ]  main_joe.cpp
    ```

>**ATTENTION**
>
>Jack et Joe doivent encore changer le groupe du fichier nouvellement créer s'ils veulent que le fichier soit modifiable par l'autre.
>
>```
>$ chgrp jackjoe main_*.cpp
>```




### 7.

Écrire un script permettant de créer ou de supprimer 100 comptes utilisateurs.

* Script 

```shell
#!/bin/bash
#################################
# Création de 10 utilisateurs
#
# dominique.huguenin AT rpn.ch
#################################
USER_PREFIX="user"

for USER in $(echo ${USER_PREFIX}{00..10}); do
        PASS=$(mkpasswd $USER)
        useradd -m $USER -p $PASS -s /bin/bash
done
```

* [source](https://mylos.cifom.ch/gitlab/dhu.cours/intsys1nix/intsys1nix.documents/-/blob/60aa0e5a37fe552db2d56c5083c83d14b26ffe50/exercices/scripts/addusers.sh)


```shell
#!/bin/bash
#################################
# Suppression de 10 utilisateurs
#
# dominique.huguenin AT rpn.ch
#################################
USER_PREFIX="user"

for USER in $(echo ${USER_PREFIX}{00..10}); do
	userdel -r -f $USER
done
```

* [source](https://mylos.cifom.ch/gitlab/dhu.cours/intsys1nix/intsys1nix.documents/-/blob/60aa0e5a37fe552db2d56c5083c83d14b26ffe50/exercices/scripts/delusers.sh)


## Références

1. [Activité](https://mylos.cifom.ch/cours/int-sys1-nix/shell/activites/sysnix-activite-0008-gestion-utilisateurs/)
