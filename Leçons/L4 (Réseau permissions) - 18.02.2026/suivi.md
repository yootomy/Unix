# Leçon 04 - 2026-02-18 (5p)

## disque système de remplacement

1. HD-S-604
1. HD-S-459
1. HD-S-629

## A voir

1. configuration du prompt
1. ascinema

## redirection et filtre

* [Le shell](<../../Cours_Mylos/site/cours/int-sys1-nix/shell/index.html>)
   1. [Activités, série 0003 - Redirection et filtre](<../../Cours_Mylos/site/cours/int-sys1-nix/activites/sysnix-activite-0003-redirection-filtre/index.html>) 
      * finir la correction de 7 à la fin
      * [Éléments de solution](<../../Cours_Mylos/wiki/elements-de-solution/sysnix-activite-0003-redirection-filtre.md>)
   1. [Fiches - Rôle de l'apostrophe dans la commande `find`](<../../Cours_Mylos/site/cours/int-sys1-nix/fiches/shell-find-role-apostrophes/index.html>)

## Couche graphique

* [Installation du serveur X](<../../Cours_Mylos/site/cours/int-sys1-nix/mise-en-route-systeme-exploitation/how-to-ubuntu-x/index.html>)
* [Utilisation d'une application graphique en réseau](<../../Cours_Mylos/site/cours/int-sys1-nix/mise-en-route-systeme-exploitation/linux-couche-graphique-reseau/index.html>)

>Sur Ubuntu Server 22.04, tu peux lancer une application avec startx <application> si tu as installé xterm.
> 
>Quelques exemples qui fonctionnent très bien (après installation des paquets correspondants) :
>* `startx xclock`
>* `startx xeyes`
>* `startx midori`
>* `startx nautilus`
>
>Un bon moyen de montrer qu’on n’a besoin de rien ou presque pour lancer une application graphique !

## configuration réseau (network/interfaces)

* activer le network-manager en commentant les lignes dans le fichier /etc/network/interfaces correspondant à la carte réseau puis redémarrer la machine

```
# This file describes the network interfaces available on your system
# and how to activate them. For more information, see interfaces(5).

source /etc/network/interfaces.d/*

# The loopback network interface
auto lo
iface lo inet loopback

# The primary network interface
#allow-hotplug enp5s0
#iface enp5s0 inet dhcp
```

## configuration réseau (netplan)

* activer le network-manager

    ```
    huguenindo@mc0-0315-00:~$ cat /etc/netplan/01-netcfg.yaml 
    # Let NetworkManager manage all devices on this system
    network:
        version: 2
        renderer: NetworkManager

    huguenindo@mc0-0315-00:~$ sudo netplan apply  
    ```

    rebooter la machine

## Accès à Lozan

* Configurer l'accès ssh à lozan depuis la machine lmb-315-dhu

## gameshell

1. la mission 18 nécessite un serveur X coté client!

  ```
  gsh index
  gsh goal 18
  ```

## Gestion des permissions

* [Le shell](<../../Cours_Mylos/site/cours/int-sys1-nix/shell/index.html>)
   1. [Gestion des permissions](<../../Cours_Mylos/site/cours/int-sys1-nix/shell/gestion-acces/index.html>)
      * question?
   1. [Activités, série 0004 - Gestion des accès](<../../Cours_Mylos/site/cours/int-sys1-nix/activites/sysnix-activite-0004-gestion-acces/index.html>)

## A Faire


* étudier la solution [Activités, série 0003 - Redirection et filtre - Éléments de solution](<../../Cours_Mylos/wiki/elements-de-solution/sysnix-activite-0003-redirection-filtre.md>)
* A étudier [Gestion des permissions](<../../Cours_Mylos/site/cours/int-sys1-nix/shell/gestion-acces/index.html>)
* Terminer [Activités, série 0004 - Gestion des accès](<../../Cours_Mylos/site/cours/int-sys1-nix/activites/sysnix-activite-0004-gestion-acces/index.html>)

## Notes

```
huguenindo@lozan0:tmp$ tree
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

2 directories, 18 files
huguenindo@lozan0:tmp$ find . -name '*' | wc -l
20
huguenindo@lozan0:tmp$ find . | wc -l
20
huguenindo@lozan0:tmp$ find . -type f | wc -l
18
huguenindo@lozan0:tmp$ man tree 
huguenindo@lozan0:tmp$ tree -p
[drwxr-xr-x]  .
├── [-rw-r--r--]  ex1
├── [-rw-r--r--]  ex2
├── [-rw-r--r--]  ex3
├── [-rw-r--r--]  ex4
├── [-rw-r--r--]  ex5
├── [-rw-r--r--]  ex6
├── [-rw-r--r--]  ex7
├── [-rw-r--r--]  ex8
├── [-rw-r--r--]  ex9
└── [drwxr-xr-x]  test
    ├── [-rw-r--r--]  fichier1
    ├── [-rw-r--r--]  fichier2
    ├── [-rw-r--r--]  fichier3
    ├── [-rw-r--r--]  fichier4
    ├── [-rw-r--r--]  fichier5
    ├── [-rw-r--r--]  fichier6
    ├── [-rw-r--r--]  fichier7
    ├── [-rw-r--r--]  fichier8
    └── [-rw-r--r--]  fichier9

2 directories, 18 files
huguenindo@lozan0:tmp$ cat /etc/passwd | cut -d: -f4 | grep ^1[0-9][0-9]$
101
107
108
huguenindo@lozan0:tmp$ cat /etc/passwd | cut -d: -f4 | grep ^1[0-9][0-9]
101
1000
107
108
1001
1002
1003
1004
1005
1006
1007
1008
1017
1018
1019
1020
1021
1029
1030
1031
1032
1033
1034
1035
1036
1037
1038
1043
1044
1045
1046
1047
1048
1049
1050
1051
1052
1053
1054
1055
1057
1059
huguenindo@lozan0:tmp$ cat /etc/passwd | cut -d: -f4 | grep 1[0-9][0-9]$
101
107
108
huguenindo@lozan0:tmp$ cat /etc/passwd | cut -d: -f4 | grep 1[0-9][0-9]
101
1000
107
108
1001
1002
1003
1004
1005
1006
1007
1008
1017
1018
1019
1020
1021
1029
1030
1031
1032
1033
1034
1035
1036
1037
1038
1043
1044
1045
1046
1047
1048
1049
1050
1051
1052
1053
1054
1055
1057
1059
huguenindo@lozan0:tmp$ 
huguenindo@lozan0:tmp$ w
 07:54:42 up 104 days, 17:27,  3 users,  load average: 0.00, 0.01, 0.00
UTIL.    TTY      DE               LOGIN@   IDLE   JCPU   PCPU QUOI
geiserj  pts/0    172.16.1.10      07:23    2:16   0.03s  0.03s -bash
huguenin pts/1    172.16.1.10      07:33    1.00s  0.08s  0.02s w
maurerr1 pts/2    172.16.1.10      07:49    4:33   0.01s  0.01s -bash
huguenindo@lozan0:tmp$ w | tr -s ' ' ':'
:07:55:54:up:104:days,:17:29,:3:users,:load:average:0.07,:0.04,:0.01
UTIL.:TTY:DE:LOGIN@:IDLE:JCPU:PCPU:QUOI
geiserj:pts/0:172.16.1.10:07:23:2.00s:0.04s:0.04s:-bash
huguenin:pts/1:172.16.1.10:07:33:2.00s:0.08s:0.01s:w
maurerr1:pts/2:172.16.1.10:07:49:5:45:0.01s:0.01s:-bash
huguenindo@lozan0:tmp$ w | tr -s ' ' ':' | cut -d: -f1

UTIL.
geiserj
huguenin
maurerr1
huguenindo@lozan0:tmp$ w | tr -s ' ' ':' | cut -d: -f2
07
TTY
pts/0
pts/1
pts/2
huguenindo@lozan0:tmp$ w | tr -s ' ' ':' | cut -d: -f3
56
DE
172.16.1.10
172.16.1.10
172.16.1.10
huguenindo@lozan0:tmp$ w | tr -s ' ' ':' | cut -d: -f1,3
:56
UTIL.:DE
geiserj:172.16.1.10
huguenin:172.16.1.10
maurerr1:172.16.1.10
huguenindo@lozan0:tmp$ w | tr -s ' ' ':' | cut -d: -f1,3 | head -n 2
:57
UTIL.:DE
huguenindo@lozan0:tmp$ w | tr -s ' ' ':' | cut -d: -f1,3 | tail -2
huguenin:172.16.1.10
maurerr1:172.16.1.10
huguenindo@lozan0:tmp$ w | grep 'pts/2' | tr -s ' ' ':' | cut -d: -f1,3 | tail -2
maurerr1:172.16.1.10
huguenindo@lozan0:tmp$ w | awk '{print $1 " " $3}'
07:59:12 104
UTIL. DE
geiserj 172.16.1.10
huguenin 172.16.1.10
maurerr1 172.16.1.10
huguenindo@lozan0:tmp$ w | awk '{print $1 " " $3}' | tail -n 2
huguenin 172.16.1.10
maurerr1 172.16.1.10
huguenindo@lozan0:tmp$ w | awk '{print $1 " " $4}' | tail -n 2
huguenin 07:33
maurerr1 07:49
huguenindo@lozan0:tmp$ w | awk '{print $1 " " $5}' | tail -n 2
huguenin 4.00s
maurerr1 9:58
huguenindo@lozan0:tmp$ w | awk '{print $1 " " $6}' | tail -n 2
huguenin 0.12s
maurerr1 0.01s
huguenindo@lozan0:tmp$ w | awk '{print $1 " " $7}' | tail -n 2
huguenin 0.01s
maurerr1 0.01s
huguenindo@lozan0:tmp$ w | awk '{print $1 " " $8}' | tail -n 2
huguenin w
maurerr1 -bash
huguenindo@lozan0:tmp$ man awk
huguenindo@lozan0:tmp$ man sed
huguenindo@lozan0:tmp$ tty
/dev/pts/1
huguenindo@lozan0:tmp$ cat > /dev/pts/1
aaaaa
aaaaa
aaaa
aaaa
aaa
aaa
```

## find -name avec ou sans apostrophe (')

```
huguenindo@lozan0:tmp$ rm -R *
huguenindo@lozan0:tmp$ find  /usr/include -name al*.h
/usr/include/c++/12/bits/allocator.h
/usr/include/c++/12/bits/allocated_ptr.h
/usr/include/c++/12/bits/alloc_traits.h
/usr/include/c++/12/bits/align.h
/usr/include/c++/12/bits/algorithmfwd.h
/usr/include/c++/12/ext/aligned_buffer.h
/usr/include/c++/12/ext/alloc_traits.h
/usr/include/c++/12/parallel/algo.h
/usr/include/c++/12/parallel/algorithmfwd.h
/usr/include/c++/12/parallel/algobase.h
/usr/include/c++/12/pstl/algorithm_impl.h
/usr/include/c++/12/pstl/algorithm_fwd.h
/usr/include/alloca.h
/usr/include/aliases.h
huguenindo@lozan0:tmp$ find  /usr/include -name 'al*.h'
/usr/include/c++/12/bits/allocator.h
/usr/include/c++/12/bits/allocated_ptr.h
/usr/include/c++/12/bits/alloc_traits.h
/usr/include/c++/12/bits/align.h
/usr/include/c++/12/bits/algorithmfwd.h
/usr/include/c++/12/ext/aligned_buffer.h
/usr/include/c++/12/ext/alloc_traits.h
/usr/include/c++/12/parallel/algo.h
/usr/include/c++/12/parallel/algorithmfwd.h
/usr/include/c++/12/parallel/algobase.h
/usr/include/c++/12/pstl/algorithm_impl.h
/usr/include/c++/12/pstl/algorithm_fwd.h
/usr/include/alloca.h
/usr/include/aliases.h
huguenindo@lozan0:tmp$ set -x
huguenindo@lozan0:tmp$ find  /usr/include -name 'al*.h'
+ find /usr/include -name 'al*.h'
/usr/include/c++/12/bits/allocator.h
/usr/include/c++/12/bits/allocated_ptr.h
/usr/include/c++/12/bits/alloc_traits.h
/usr/include/c++/12/bits/align.h
/usr/include/c++/12/bits/algorithmfwd.h
/usr/include/c++/12/ext/aligned_buffer.h
/usr/include/c++/12/ext/alloc_traits.h
/usr/include/c++/12/parallel/algo.h
/usr/include/c++/12/parallel/algorithmfwd.h
/usr/include/c++/12/parallel/algobase.h
/usr/include/c++/12/pstl/algorithm_impl.h
/usr/include/c++/12/pstl/algorithm_fwd.h
/usr/include/alloca.h
/usr/include/aliases.h
huguenindo@lozan0:tmp$ find  /usr/include -name al*.h
+ find /usr/include -name 'al*.h'
/usr/include/c++/12/bits/allocator.h
/usr/include/c++/12/bits/allocated_ptr.h
/usr/include/c++/12/bits/alloc_traits.h
/usr/include/c++/12/bits/align.h
/usr/include/c++/12/bits/algorithmfwd.h
/usr/include/c++/12/ext/aligned_buffer.h
/usr/include/c++/12/ext/alloc_traits.h
/usr/include/c++/12/parallel/algo.h
/usr/include/c++/12/parallel/algorithmfwd.h
/usr/include/c++/12/parallel/algobase.h
/usr/include/c++/12/pstl/algorithm_impl.h
/usr/include/c++/12/pstl/algorithm_fwd.h
/usr/include/alloca.h
/usr/include/aliases.h
huguenindo@lozan0:tmp$ touch al123456789.h
+ touch al123456789.h
huguenindo@lozan0:tmp$ ls
+ ls --color=auto
al123456789.h
huguenindo@lozan0:tmp$ find  /usr/include -name 'al*.h'
+ find /usr/include -name 'al*.h'
/usr/include/c++/12/bits/allocator.h
/usr/include/c++/12/bits/allocated_ptr.h
/usr/include/c++/12/bits/alloc_traits.h
/usr/include/c++/12/bits/align.h
/usr/include/c++/12/bits/algorithmfwd.h
/usr/include/c++/12/ext/aligned_buffer.h
/usr/include/c++/12/ext/alloc_traits.h
/usr/include/c++/12/parallel/algo.h
/usr/include/c++/12/parallel/algorithmfwd.h
/usr/include/c++/12/parallel/algobase.h
/usr/include/c++/12/pstl/algorithm_impl.h
/usr/include/c++/12/pstl/algorithm_fwd.h
/usr/include/alloca.h
/usr/include/aliases.h
huguenindo@lozan0:tmp$ find  /usr/include -name al*.h
+ find /usr/include -name al123456789.h
huguenindo@lozan0:tmp$ ls 'al*.h'
+ ls --color=auto 'al*.h'
ls: impossible d'accéder à 'al*.h': Aucun fichier ou dossier de ce type
huguenindo@lozan0:tmp$ ls al*.h
+ ls --color=auto al123456789.h
al123456789.h
huguenindo@lozan0:tmp$ touch 'al*.h'
+ touch 'al*.h'
huguenindo@lozan0:tmp$ ls al*.h
+ ls --color=auto al123456789.h 'al*.h'
 al123456789.h  'al*.h'
huguenindo@lozan0:tmp$ ls 'al*.h'
+ ls --color=auto 'al*.h'
'al*.h'
huguenindo@lozan0:tmp$ ls 'al   *.h'
+ ls --color=auto 'al   *.h'
ls: impossible d'accéder à 'al   *.h': Aucun fichier ou dossier de ce type
huguenindo@lozan0:tmp$ touch 'al   1.h'
+ touch 'al   1.h'
huguenindo@lozan0:tmp$ ls
+ ls --color=auto
 al123456789.h  'al   1.h'  'al*.h'


```

### Réponse de gemini

C'est un classique du shell ! Ce que tu observes est le résultat d'un mécanisme appelé le **Globbing** (ou expansion des métacaractères) effectué par ton shell (Bash, Zsh, etc.) **avant** même que la commande `find` ne soit exécutée.

Voici l'explication étape par étape de ce qui s'est passé dans ton terminal :

---

### 1. Pourquoi la première commande fonctionne ?

```bash
find /usr/include -name al*.h

```

À ce moment-là, ton dossier actuel (`tmp`) est vide (ou ne contient aucun fichier commençant par "al" et finissant par ".h").

* Le shell cherche dans le répertoire courant s'il y a un fichier qui correspond à `al*.h`.
* Il n'en trouve pas.
* **Comportement par défaut :** S'il n'y a pas de correspondance, le shell laisse la chaîne `al*.h` telle quelle et la transmet à `find`.
* `find` reçoit donc bien l'argument `-name al*.h` et cherche récursivement dans `/usr/include`.

### 2. L'élément perturbateur : `touch al123456789.h`

Tu viens de créer un fichier qui correspond exactement au motif `al*.h` dans ton répertoire de travail actuel.

### 3. Le piège de la dernière commande

```bash
find /usr/include -name al*.h

```

Ici, avant de lancer `find`, le shell analyse la ligne. Il voit `al*.h`, regarde dans le dossier courant, et se dit : *"Tiens ! J'ai un fichier qui correspond : al123456789.h"*.

Le shell **remplace** alors ton texte par le nom du fichier trouvé. La commande réellement exécutée devient :
`find /usr/include -name al123456789.h`

Comme ce fichier précis n'existe pas dans `/usr/include` (il n'existe que dans ton dossier `tmp`), `find` ne renvoie rien ou presque rien.

---

### La règle d'or pour `find`

Pour éviter que le shell n'interprète les astérisques (`*`) à ta place, il faut **toujours mettre le motif entre guillemets**.

| Commande | Risque |
| --- | --- |
| `find . -name *.h` | **Dangereux** : Le shell peut remplacer `*.h` par les fichiers du dossier local. |
| `find . -name "*.h"` | **Sûr** : Le shell ignore l'astérisque, et c'est `find` qui l'interprète. |

C'est d'ailleurs ce que tu as fait dans ton avant-dernière commande (`find /usr/include -name 'al*.h'`), et c'est pour cela qu'elle a fonctionné correctement malgré la présence du fichier dans ton dossier.

Souhaites-tu que je t'explique comment désactiver temporairement ce comportement du shell (le globbing) pour tes tests ?

![xournal](<../../Cours_Mylos/wiki/xournal/2026-02-18-Note-10-50.svg>)
