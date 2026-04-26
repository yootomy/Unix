# SYSNIX - Activités, série 0003 - Redirection et filtre (Éléments de solution)

[[_TOC_]]

## Objectifs

* Redirections et filtres

## Exercices

### 1

Exercer les commandes cat, head, tail, less et more. Pour less exercer ses propres sous-commandes.

```
huguenindo@lozan:tmp$ ls /usr/include/ > include.txt
```

```
huguenindo@lozan:tmp$ cat < include.txt 
aio.h
aliases.h
alloca.h
argp.h
argz.h
ar.h
arpa
asm-generic
assert.h
byteswap.h
c++
...
wordexp.h
X11
x86_64-linux-gnu
xen
xlocale.h
```

```
huguenindo@lozan:tmp$ head < include.txt 
aio.h
aliases.h
alloca.h
argp.h
argz.h
ar.h
arpa
asm-generic
assert.h
byteswap.h
```

```
huguenindo@lozan:tmp$ tail < include.txt 
values.h
video
wait.h
wchar.h
wctype.h
wordexp.h
X11
x86_64-linux-gnu
xen
xlocale.h
```

### 2

Prendre deux fichiers texte identiques, en modifier un et lister les différences ( diff et cmp ).

* Création du fichier `./ex2.txt`

```
huguenindo@lozan:tmp$ cat <<_EOF_ > ./ex2.txt
> 123456789
> 123456789
> abcdefgh
> _EOF_
```

```
huguenindo@lozan:tmp$ cat ./ex2.txt 
123456789
123456789
abcdefgh
```

* Création du fichier `ex2_2.txt`

```
huguenindo@lozan:tmp$ cat <<_EOF_ > ./ex2_2.txt
> 1234  789
> abcdefgh
> adefgh
> 123456789
> _EOF_
```

```
huguenindo@lozan:tmp$ cat ./ex2_2.txt 
1234  789
abcdefgh
adefgh
123456789
```

* Comparaison ligne par ligne

```
huguenindo@lozan:tmp$ diff ex2.txt ex2_2.txt 
1,2c1
< 123456789
< 123456789
---
> 1234  789
3a3,4
> adefgh
> 123456789
```

```
huguenindo@lozan:tmp$ diff -y ex2.txt ex2_2.txt 
123456789						      |	1234  789
123456789						      <
abcdefgh							abcdefgh
							      >	adefgh
							      >	123456789
```

```
huguenindo@lozan:tmp$ diff -c ex2.txt ex2_2.txt 
***  ex2.txt	2017-11-14 12:51:54.658565908 +0100
--- ex2_2.txt	2017-11-14 12:54:07.790270076 +0100

*************** 
*** 1,3 **** 
###  123456789
###  123456789
  abcdefgh
--- 1,4 ----
###  1234  789
  abcdefgh
+ adefgh
+ 123456789
```

* Comparaison octet par octet

```
huguenindo@lozan:tmp$ cmp ./ex2.txt ./ex2_2.txt 
./ex2.txt ./ex2_2.txt sont différents: octet 5, ligne 1
```

### 3

Que fournissent les commandes suivantes ?

* Retourne le nombre d'utilisateurs locaux

```
huguenindoe@lozan:~$ wc -l /etc/passwd
48 /etc/passwd
```

* Affiche page par page la liste des utilisateurs locaux

```
huguenindoe@lozan:~$ more /etc/passwd
```

* Affiche la liste des utilisateurs locaux dont la configuration contient `li`

```
huguenindoe@lozan:~$ grep 'li' /etc/passwd
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
libuuid:x:100:101::/var/lib/libuuid:
colord:x:106:112:colord colour management daemon,,,:/var/lib/colord:/bin/false
nagios:x:107:113::/var/lib/nagios:/bin/false
```

* Affiche la liste des utilisateurs locaux qui ont un nom commençant par `li`

```
huguenindoe@lozan:~$ grep '^li' /etc/passwd
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
libuuid:x:100:101::/var/lib/libuuid:
```

* Affiche la liste des utilisateurs locaux dont la configuration contient `0`

```
huguenindoe@lozan:~$ grep 0 /etc/passwd
root:x:0:0:root:/root:/bin/bash
games:x:5:60:games:/usr/games:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
libuuid:x:100:101::/var/lib/libuuid:
...
```

* Afficher une liste contenant le nom des utilisateurs locaux et leur id de groupe

```
huguenindoe@lozan:~$ cut -d: -f1,4 /etc/passwd
root:0
...
usbmux:46
colord:112
nagios:113
ansible:19699
```

* Affiche page par page la liste des groupes locaux.

```
huguenindoe@lozan:~$ more /etc/group
```

* Affiche une liste contenant le nom du groupe et l'id du groupe.

```
huguenindoe@lozan:~$ cut -d: -f1,3 /etc/group
root:0
daemon:1
...
ansible:19699
mount:1021
```

### 4

Exécuter les commandes ci-dessous, comprendre ce qu'il se passe.

* Afficher les noms des utilisateurs locaux.

```
huguenindoe@lozan:~$ cat /etc/passwd | cut -d: -f1
root
daemon
bin
...
colord
nagios
ansible
```

* Afficher les noms des utilisateurs locaux et le nom de leur dossier personnel

```
huguenindoe@lozan:~$ cat /etc/passwd | cut -d: -f1,6
root:/root
daemon:/usr/sbin
bin:/bin
sys:/dev
sync:/bin
...
colord:/var/lib/colord
nagios:/var/lib/nagios
ansible:/home/ansible
```

* Afficher page par page les noms des utilisateurs locaux et le nom de leur dossier personnel

```
huguenindoe@lozan:~$ cat /etc/passwd | cut -d: -f1,6 | less
```

* Affiche des utilisateurs locaux ayant `101` comme id de groupe.

```
huguenindoe@lozan:~$ cat /etc/passwd | cut -d: -f1,4 | grep ':101$'
libuuid:101
```

* Affiche le nom des groupes commençant par `user`

```
huguenindoe@lozan:~$ cat /etc/group | grep ^user
users:x:100:
user00:x:1001:
user01:x:1002:
user02:x:1003:
user03:x:1004:
...
user17:x:1018:
user18:x:1019:
user19:x:1020:
```

* Affiche et écrit dans le fichier `liste_comptes` les noms des utilisateurs locaux et le nom de leur dossier personnel

```
huguenindoe@lozan:~$ cat /etc/passwd | cut -d: -f1,6 | tee liste_comptes 
root:/root
daemon:/usr/sbin
...
nagios:/var/lib/nagios
ansible:/home/ansible
```

* Écrit dans le fichier `liste_comptes.triee` les noms des utilisateurs locaux **triés** et le nom de leur dossier personnel.

```
huguenindoe@lozan:~$ sort < liste_comptes > liste_comptes.triee
huguenindoe@lozan:~$ cat liste_comptes.triee 
ansible:/home/ansible
backup:/var/backups
bin:/bin
colord:/var/lib/colord
daemon:/usr/sbin
games:/usr/games
gnats:/var/lib/gnats
...
```

* Affiche page par page et écrit dans le fichier `liste_comptes` les noms des utilisateurs locaux et le nom de leur dossier personnel

```
huguenindoe@lozan:~$ cat /etc/passwd | cut -d: -f1,6 | tee liste_comptes | less
```

* Complète le fichier `liste_comptes` avec le nom des utilisateurs et leur id du groupe.

```
huguenindoe@lozan:~$ cat /etc/passwd | cut -d: -f1,4 >> liste_comptes
```

### 5

Écrire les commandes fournissant:

* la liste des comptes avec leurs UID et GID (sur écran et sur fichier)

```
huguenindoe@lozan:~$ cat /etc/passwd | cut -d: -f3,4 | tee comptes_locaux.txt
0:0
1:1
2:2
3:3
4:65534
5:60
```

* la liste des nom des groupes locaux

```
huguenindoe@lozan:~$ cat /etc/group | cut -d: -f1 
root
daemon
bin
sys
adm
tty
disk
lp
mail
news
...
```

* le nombre de comptes locaux

```
huguenindoe@lozan:~$ cat /etc/passwd | wc -l
48
```

* le nombre de groupes locaux

```
huguenindoe@lozan:~$ cat /etc/group | wc -l
76
```

### 6

Exercer la commande `find` dans les 4 cas suivants:

* Création des fichiers de test

```
huguenindo@lozan:tmp$ touch ./ex{1..9}; chmod 111 ./ex7
huguenindo@lozan:tmp$ ls
ex1  ex2  ex3  ex4  ex5  ex6  ex7  ex8  ex9
```

* recherche selon le nom du fichier

```
huguenindo@lozan:tmp$ find . -name 'ex*'
./ex7
./ex2
./ex1
./ex6
./ex3
./ex8
./ex4
./ex9
./ex5
```

* recherche selon le code de protection

```
huguenindo@lozan:tmp$ find . -perm -111
./ex7
```

* recherche selon la date de modification\\liste les fichiers modifiées aujourd'hui

```
huguenindo@lozan:tmp$ find . -ctime 0
.
./ex7
./ex2
./ex1
./ex6
./ex3
./ex8
./ex4
./ex9
./ex5
```

* recherche selon un code de protection\\liste les fichiers modifiés aujourd'hui et exécutable par le propriétaire

```
huguenindo@lozan:tmp$ find . -ctime 0 -perm -100
.
./ex7
```

* recherche selon un code de protection et **le modifier**\\liste les fichiers modifiés aujourd'hui et exécutable par le propriétaire

```
huguenindo@lozan:tmp$ find . -maxdepth 1 -name 'ex*' -perm -600 -exec chmod u+x '{}' \;
huguenindo@lozan:tmp$ ls -l
total 0
-rwx------ 1 huguenindo domain users 0 nov 14 14:11 ex1
-rwx------ 1 huguenindo domain users 0 nov 14 14:11 ex2
-rwx------ 1 huguenindo domain users 0 nov 14 14:11 ex3
-rwx------ 1 huguenindo domain users 0 nov 14 14:11 ex4
-rwx------ 1 huguenindo domain users 0 nov 14 14:11 ex5
-rwx------ 1 huguenindo domain users 0 nov 14 14:11 ex6
---x--x--x 1 huguenindo domain users 0 nov 14 14:11 ex7
-rwx------ 1 huguenindo domain users 0 nov 14 14:11 ex8
-rwx------ 1 huguenindo domain users 0 nov 14 14:11 ex9
```

### 7

* Création des fichiers des test

```
huguenindo@lozan:tmp$ touch ./ex{1..9}; mkdir ./test; touch ./test/fichier{1..9}
huguenindo@lozan:tmp$ tree
.
├── ex1
├── ex2
├── ex3
├── ex4
├── ex5
├── ex6
├── ex7
├── ex8
├── ex9
└── test
    ├── fichier1
    ├── fichier2
    ├── fichier3
    ├── fichier4
    ├── fichier5
    ├── fichier6
    ├── fichier7
    ├── fichier8
    └── fichier9
```

* Créez un tuyau qui permet de compter le nombre de fichiers et de répertoires contenus dans un répertoire.

```
huguenindo@lozan:tmp$ find . -name '*' | wc -l
20
```

* Modifiez le tuyau sous 1) pour ne compter que les fichiers ordinaires.

```
huguenindo@lozan:tmp$ find . -name '*' -type f | wc -l
18
```

* Modifiez le tuyau sous 1) pour ne compter que les répertoires.

```
huguenindo@lozan:tmp$ find . -name '*' -type d | wc -l
2
```

### 8

Construire la commande qui

* permet de compter le nombre d’utilisateurs qui possède un GID compris entre 100 et 199.

```
huguenindo@lozan:tmp$ cat /etc/passwd | cut -d: -f4 | grep ^1[0-9][0-9]$ | wc -l
6
```

%%information Différentes syntaxes d'expression régulières

```
cat /etc/passwd | cut -d: -f4 | grep -e '1[0-9][0-9]' -w
cat /etc/passwd | cut -d: -f4 | grep -e '^1[0-9][0-9]$' 
cat /etc/passwd | cut -d: -f4 | grep -E '^1[0-9]{2}$' 
cat /etc/passwd | cut -d: -f4 | grep -P '^1\d{2}$' 
cat /etc/passwd | cut -d: -f4 | grep -P '^1[[:digit:]]{2}$' 
```

%%

* indique le nom de l'utilisateur et l'IP de sa machine connectés au système sur le terminal 4 (/dev/pts/4)

```
huguenindo@lozan:tmp$ w | grep 'pts/4'| cut -d' ' -f1
huguenin
```

ou

```
huguenindo@lozan:tmp$ w | grep 'pts/4'| tr -s ' ' ':' 
huguenin:pts/4:157.26.229.100:13:27:2.00s:0.14s:0.00s:w
```

```
huguenindo@lozan:tmp$ w | grep 'pts/4'| tr -s ' ' ':' | cut -d: -f1
huguenin
```

aide : utiliser la commande tr (translate) : tr –s ‘ ‘ ‘\\t’ file(s)

* autre solution avec awk

```
huguenindo@lozan:~$ w | grep 'pts/4' | awk '{print $1 " " $3}'
spychige 157.26.174.89
```

### 9

Analyser les commandes suivantes

```
find / -user "$USER"
```

* affiche tous les fichiers appartenant à l'utilisateur courant `$USER`

```
find / –user "$USER" 2>/dev/null
```

* affiche tous les fichiers appartenant à l'utilisateur courant `$USER`. Les messages d'erreurs ne sont pas affichés.

Constatations ?

## Références

1. Activités, série 0002 - Gestion des fichiers, https://mylos.cifom.ch/cours/int-sys1-nix/shell/activites/sysnix-activite-0003-redirection-filtre