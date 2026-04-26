# Leçon 03 - 2026-02-11 (5p)

>Système d'exploitation

## redirection et filtre

* [Le shell](<../../Cours_Mylos/site/cours/int-sys1-nix/shell/index.html>)
   1. [Activités, série 0003 - Redirection et filtre](<../../Cours_Mylos/site/cours/int-sys1-nix/activites/sysnix-activite-0003-redirection-filtre/index.html>) 
      * correction 
      * [Éléments de solution](<../../Cours_Mylos/wiki/elements-de-solution/sysnix-activite-0003-redirection-filtre.md>)
   1. [Fiches - Rôle de l'apostrophe dans la commande `find`](<../../Cours_Mylos/site/cours/int-sys1-nix/fiches/shell-find-role-apostrophes/index.html>)


## Installation et configuration

* [Mise en place du système d'exploitation](<../../Cours_Mylos/site/cours/int-sys1-nix/mise-en-route-systeme-exploitation/index.html>)
    * [Gestion des volumes logique LVM](<../../Cours_Mylos/site/cours/int-sys1-nix/mise-en-route-systeme-exploitation/volume-logique-lvm/index.html>)
    * [Installation GNU/Linux Debian Server](<../../Cours_Mylos/site/cours/int-sys1-nix/mise-en-route-systeme-exploitation/linux-installation/index.html>)
        * connecter le cable réseau LAB-Px à la place du cable réseau S2-Px. La machine est branché sur le résean lan.dhu
        * démarrer la machine sur la carte réseau (IBA GE SLOT). la touche F8 permet de sélection le périphérique de démarrage.
        * Nom de la machine lmb-b315-dhu  
        * Partitionner le disque
          * utiliser partitionnement tout le disqe avec LVM et faire des changements avant de commencer l'intallation
          * LVM, volume logique root, swap, var, home (optionnel)

>Préparation évaluation : installer le manuel en français.
>```
>sudo apt-get install manpages-fr manpages-fr-dev
>```
>
>* configurer le périphérique réseau
>* sélection la langue du manuel
>   ```
>   dhu:beuseu$ man -L en bash
>   dhu:beuseu$ man -L fr bash
>   ```

### Post-installation

* mettre à jour le système

    ```
    $ sudo apt update
    $ sudo apt upgrade
    ```

* arrêt de la machine

    ```
    $ sudo shutdown now
    ```


## A Faire

* terminer l'[Activités, série 0003 - Redirection et filtre](<../../Cours_Mylos/site/cours/int-sys1-nix/activites/sysnix-activite-0003-redirection-filtre/index.html>) 
* A étudier [Gestion des permissions](<../../Cours_Mylos/site/cours/int-sys1-nix/shell/gestion-acces/index.html>)

## Notes

```
huguenindo@lozan0:tmp$ cat <<_EOF_ > ./ex2.txt
> asddffgg
> qweweer
> dsdsdsd
> 6656566
> _EOF_
huguenindo@lozan0:tmp$ cat ex2.txt 
asddffgg
qweweer
dsdsdsd
6656566
huguenindo@lozan0:tmp$ cat <<pierpoljak > ./ex3.txt
asddffgg
qweweer
dsdsdsd
6656566
pierpoljak 


huguenindo@lozan0:tmp$ cat /etc/passwd| cut -d: -f1,4 | grep 3
sys:3
sync:65534
proxy:13
www-data:33
backup:34
list:38
irc:39
_apt:65534
nobody:65534
sshd:65534
ferrarip:1003
gerbert3:1020
marquesrda1:1030
merillata:1031
sampaolof1:1032
bastosda1:1033
borcardj:1034
cattarinn1:1035
dilke:1036
germaniertr:1037
hazerajh:1038
mafillem:1043
kneubuehlv:1053
huguenindo@lozan0:tmp$ cat /etc/passwd| cut -d: -f1,4 | grep :3
sys:3
www-data:33
backup:34
list:38
irc:39
huguenindo@lozan0:tmp$ cat /etc/passwd| cut -d: -f1,4 | grep :3$
sys:3
huguenindo@lozan0:tmp$ cat /etc/passwd| cut -d: -f1,4 | grep 3$
sys:3
proxy:13
www-data:33
ferrarip:1003
bastosda1:1033
mafillem:1043
kneubuehlv:1053
huguenindo@lozan0:tmp$ cat /etc/passwd| cut -d: -f1,4 | grep :3$
sys:3

huguenindo@lozan0:tmp$ cut -d: -f1,6 /etc/passwd
root:/root
daemon:/usr/sbin
bin:/bin
sys:/dev
sync:/bin
games:/usr/games
man:/var/cache/man
lp:/var/spool/lpd
mail:/var/mail
news:/var/spool/news
uucp:/var/spool/uucp
proxy:/bin
www-data:/var/www
backup:/var/backups
list:/var/list
irc:/run/ircd
_apt:/nonexistent
nobody:/nonexistent
messagebus:/nonexistent
systemd-network:/
systemd-resolve:/
polkitd:/nonexistent
admin:/home/admin
sshd:/run/sshd
consul:/home/consul
prometheus:/var/lib/prometheus
uuidd:/run/uuidd
huguenindo:/home/huguenindo
jaeggil:/home/jaeggil
ferrarip:/home/ferrarip
eltschingera:/home/eltschingera
riederl1:/home/riederl1
wohlhauserfa:/home/wohlhauserfa
sacchettip:/home/sacchettip
gonthierc:/home/gonthierc
bouquetr1:/home/bouquetr1
barraudqu:/home/barraudqu
devantheyj:/home/devantheyj
gerbert3:/home/gerbert3
koggalamt2:/home/koggalamt2
haussenero:/home/haussenero
marquesrda1:/home/marquesrda1
merillata:/home/merillata
sampaolof1:/home/sampaolof1
bastosda1:/home/bastosda1
borcardj:/home/borcardj
cattarinn1:/home/cattarinn1
dilke:/home/dilke
germaniertr:/home/germaniertr
hazerajh:/home/hazerajh
mafillem:/home/mafillem
nothj:/home/nothj
stuckia1:/home/stuckia1
barzaghim1:/home/barzaghim1
brossardl1:/home/brossardl1
deojt:/home/deojt
faivrel:/home/faivrel
geiserj:/home/geiserj
henochrjt:/home/henochrjt
kilchert1:/home/kilchert1
kneubuehlv:/home/kneubuehlv
maurerr1:/home/maurerr1
pachoude1:/home/pachoude1
sejdio1:/home/sejdio1
zeinalovd:/home/zeinalovd
huguenindo@lozan0:tmp$ cut -d: -f1,6 < /etc/passwd
root:/root
daemon:/usr/sbin
bin:/bin
sys:/dev
sync:/bin
games:/usr/games
man:/var/cache/man
lp:/var/spool/lpd
mail:/var/mail
news:/var/spool/news
uucp:/var/spool/uucp
proxy:/bin
www-data:/var/www
backup:/var/backups
list:/var/list
irc:/run/ircd
_apt:/nonexistent
nobody:/nonexistent
messagebus:/nonexistent
systemd-network:/
systemd-resolve:/
polkitd:/nonexistent
admin:/home/admin
sshd:/run/sshd
consul:/home/consul
prometheus:/var/lib/prometheus
uuidd:/run/uuidd
huguenindo:/home/huguenindo
jaeggil:/home/jaeggil
ferrarip:/home/ferrarip
eltschingera:/home/eltschingera
riederl1:/home/riederl1
wohlhauserfa:/home/wohlhauserfa
sacchettip:/home/sacchettip
gonthierc:/home/gonthierc
bouquetr1:/home/bouquetr1
barraudqu:/home/barraudqu
devantheyj:/home/devantheyj
gerbert3:/home/gerbert3
koggalamt2:/home/koggalamt2
haussenero:/home/haussenero
marquesrda1:/home/marquesrda1
merillata:/home/merillata
sampaolof1:/home/sampaolof1
bastosda1:/home/bastosda1
borcardj:/home/borcardj
cattarinn1:/home/cattarinn1
dilke:/home/dilke
germaniertr:/home/germaniertr
hazerajh:/home/hazerajh
mafillem:/home/mafillem
nothj:/home/nothj
stuckia1:/home/stuckia1
barzaghim1:/home/barzaghim1
brossardl1:/home/brossardl1
deojt:/home/deojt
faivrel:/home/faivrel
geiserj:/home/geiserj
henochrjt:/home/henochrjt
kilchert1:/home/kilchert1
kneubuehlv:/home/kneubuehlv
maurerr1:/home/maurerr1
pachoude1:/home/pachoude1
sejdio1:/home/sejdio1
zeinalovd:/home/zeinalovd
huguenindo@lozan0:tmp$ cat < /etc/passwd | cut -d: -f1,6
root:/root
daemon:/usr/sbin
bin:/bin
sys:/dev
sync:/bin
games:/usr/games
man:/var/cache/man
lp:/var/spool/lpd
mail:/var/mail
news:/var/spool/news
uucp:/var/spool/uucp
proxy:/bin
www-data:/var/www
backup:/var/backups
list:/var/list
irc:/run/ircd
_apt:/nonexistent
nobody:/nonexistent
messagebus:/nonexistent
systemd-network:/
systemd-resolve:/
polkitd:/nonexistent
admin:/home/admin
sshd:/run/sshd
consul:/home/consul
prometheus:/var/lib/prometheus
uuidd:/run/uuidd
huguenindo:/home/huguenindo
jaeggil:/home/jaeggil
ferrarip:/home/ferrarip
eltschingera:/home/eltschingera
riederl1:/home/riederl1
wohlhauserfa:/home/wohlhauserfa
sacchettip:/home/sacchettip
gonthierc:/home/gonthierc
bouquetr1:/home/bouquetr1
barraudqu:/home/barraudqu
devantheyj:/home/devantheyj
gerbert3:/home/gerbert3
koggalamt2:/home/koggalamt2
haussenero:/home/haussenero
marquesrda1:/home/marquesrda1
merillata:/home/merillata
sampaolof1:/home/sampaolof1
bastosda1:/home/bastosda1
borcardj:/home/borcardj
cattarinn1:/home/cattarinn1
dilke:/home/dilke
germaniertr:/home/germaniertr
hazerajh:/home/hazerajh
mafillem:/home/mafillem
nothj:/home/nothj
stuckia1:/home/stuckia1
barzaghim1:/home/barzaghim1
brossardl1:/home/brossardl1
deojt:/home/deojt
faivrel:/home/faivrel
geiserj:/home/geiserj
henochrjt:/home/henochrjt
kilchert1:/home/kilchert1
kneubuehlv:/home/kneubuehlv
maurerr1:/home/maurerr1
pachoude1:/home/pachoude1
sejdio1:/home/sejdio1
zeinalovd:/home/zeinalovd

huguenindo@lozan0:tmp$ ls -l
total 16
-rw-r--r-- 1 huguenindo huguenindo    0 11 fév 08:52 ex1
-rw-r--r-- 1 huguenindo huguenindo    0 11 fév 08:52 ex2
-rw-r--r-- 1 huguenindo huguenindo   33 11 fév 07:50 ex2.txt
-rw-r--r-- 1 huguenindo huguenindo    0 11 fév 08:52 ex3
-rw-r--r-- 1 huguenindo huguenindo   33 11 fév 07:50 ex3.txt
-rw-r--r-- 1 huguenindo huguenindo    0 11 fév 08:52 ex4
-rw-r--r-- 1 huguenindo huguenindo    0 11 fév 08:52 ex5
-rw-r--r-- 1 huguenindo huguenindo    0 11 fév 08:52 ex6
---x--x--x 1 huguenindo huguenindo    0 11 fév 08:52 ex7
-rw-r--r-- 1 huguenindo huguenindo    0 11 fév 08:52 ex8
-rw-r--r-- 1 huguenindo huguenindo    0 11 fév 08:52 ex9
-rw-r--r-- 1 huguenindo huguenindo 1239 11 fév 07:35 include.txt
-rw-r--r-- 1 huguenindo huguenindo 1437 11 fév 08:40 liste_comptes
huguenindo@lozan0:tmp$ find . -name 'ex*'
./ex7
./ex8
./ex1
./ex4
./ex5
./ex2.txt
./ex3
./ex9
./ex2
./ex3.txt
./ex6
huguenindo@lozan0:tmp$ find . -name ex*
find: paths must precede expression: `ex2'
find: possible unquoted pattern after predicate `-name'?
huguenindo@lozan0:tmp$ set -x
huguenindo@lozan0:tmp$ find . -name 'ex*'
+ find . -name 'ex*'
./ex7
./ex8
./ex1
./ex4
./ex5
./ex2.txt
./ex3
./ex9
./ex2
./ex3.txt
./ex6
huguenindo@lozan0:tmp$ find . -name ex*
+ find . -name ex1 ex2 ex2.txt ex3 ex3.txt ex4 ex5 ex6 ex7 ex8 ex9
find: paths must precede expression: `ex2'
find: possible unquoted pattern after predicate `-name'?
huguenindo@lozan0:tmp$ find . -perm -111
+ find . -perm -111
.
./ex7
huguenindo@lozan0:tmp$ set +x
+ set +x
huguenindo@lozan0:tmp$ find . -perm -111
.
./ex7
huguenindo@lozan0:tmp$ find . -perm 111
./ex7

huguenindo@lozan0:tmp$ find . -perm -u=x,g=x,o=x
.
./ex7
huguenindo@lozan0:tmp$ find . -perm u=x,g=x,o=x
./ex7
huguenindo@lozan0:tmp$ find . -perm u=x,g=,o=x
huguenindo@lozan0:tmp$ find . -perm -u=x,g=,o=x
.
./ex7

```

![xournal](<../../Cours_Mylos/wiki/xournal/2026-02-11-Note-11-09-1.svg>)

![xournal](<../../Cours_Mylos/wiki/xournal/2026-02-11-Note-11-09-2.svg>)
