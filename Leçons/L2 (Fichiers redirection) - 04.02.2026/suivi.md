# Leçon 02 - 2026-02-04 (5p)

>shell

## Questions?

## Fichiers
* [Le shell](<../../Cours_Mylos/site/cours/int-sys1-nix/shell/index.html>)
   1. [Système de fichier](<../../Cours_Mylos/site/cours/int-sys1-nix/shell/systeme-fichier/index.html>)
      * [Motif Générique](<../../Cours_Mylos/site/cours/int-sys1-nix/shell/motif-generique/index.html>)
   1. Activité [Activités, série 0002 - Gestion Fichier](<../../Cours_Mylos/site/cours/int-sys1-nix/activites/sysnix-activite-0002-gestion-fichier/index.html>)
      * [Éléments de solution](<../../Cours_Mylos/wiki/elements-de-solution/sysnix-activite-0002-gestion-fichier.md>)

## Fiches

1. [Fiches - Lien hardware et symbolique](<../../Cours_Mylos/site/cours/int-sys1-nix/fiches/shell-lien/index.html>)
1. [Fiches - Processus et sous-processus](<../../Cours_Mylos/site/cours/int-sys1-nix/fiches/shell-processus/index.html>)
1. [Fiches - Chaînage des commandes](<../../Cours_Mylos/site/cours/int-sys1-nix/fiches/shell-chainage-commande/index.html>)
1. [Fiches - Prototype C](<../../Cours_Mylos/site/cours/int-sys1-nix/fiches/shell-prototype-c/index.html>)

## redirection et filtre

* [Le shell](<../../Cours_Mylos/site/cours/int-sys1-nix/shell/index.html>)
   1. [Filtre et Redirection](<../../Cours_Mylos/site/cours/int-sys1-nix/shell/redirection-filtre/index.html>)
   1. [Activités, série 0003 - Redirection et filtre](<../../Cours_Mylos/site/cours/int-sys1-nix/activites/sysnix-activite-0003-redirection-filtre/index.html>) 
      * [Éléments de solution](<../../Cours_Mylos/wiki/elements-de-solution/sysnix-activite-0003-redirection-filtre.md>)

## Script

* [Le shell](<../../Cours_Mylos/site/cours/int-sys1-nix/shell/index.html>)
   1. [Édition des fichiers avec VIM](<../../Cours_Mylos/site/cours/int-sys1-nix/shell/vim/index.html>)
      * faire le tutorial `vimtutor fr`

## A faire

1. faire le tutorial `vimtutor fr`
1. terminer l'[Activités, série 0003 - Redirection et filtre](<../../Cours_Mylos/site/cours/int-sys1-nix/activites/sysnix-activite-0003-redirection-filtre/index.html>) 
1. Continuer gameshell

## Note

```
huguenindo@lozan0:~$ ls -la
total 272
drwxr-xr-x  5 huguenindo huguenindo   4096  4 fév 07:43 .
drwxr-xr-x 41 root       root         4096 19 jan 13:49 ..
-rw-------  1 huguenindo huguenindo   3330  2 fév 11:12 .bash_history
-rw-r--r--  1 huguenindo huguenindo    220  6 jun  2025 .bash_logout
-rw-r--r--  1 huguenindo huguenindo   3526  6 jun  2025 .bashrc
-rw-r--r--  1 huguenindo huguenindo     28  2 fév 08:22 cat2.txt
-rw-r--r--  1 huguenindo huguenindo     17 28 jan 10:39 cat.txt
drwx------  3 huguenindo huguenindo   4096  2 fév 09:38 .config
-rwxr-xr-x  1 huguenindo huguenindo 217232 28 jan 11:11 gameshell-save.sh
lrwxrwxrwx  1 huguenindo huguenindo     29 19 jan 14:22 gameshell.sh -> /usr/local/games/gameshell.sh
-rw-------  1 huguenindo huguenindo     46  2 fév 10:11 .lesshst
-rw-r--r--  1 huguenindo huguenindo    807  6 jun  2025 .profile
drwx------  2 huguenindo huguenindo   4096 26 jan 09:41 .ssh
-rw-r--r--  1 huguenindo huguenindo      0  2 fév 08:21 test.tmp
drwxr-xr-x  2 huguenindo huguenindo   4096  2 fév 10:08 tmp
-rw-------  1 huguenindo huguenindo   1077  2 fév 10:25 .viminfo
-rw-------  1 huguenindo huguenindo     52  4 fév 07:43 .Xauthority
huguenindo@lozan0:~$ ls .
cat2.txt  cat.txt  gameshell-save.sh  gameshell.sh  test.tmp  tmp
huguenindo@lozan0:~$ ls ..
admin       borcardj    deojt         faivrel   germaniertr  henochrjt   kneubuehlv   maurerr1   riederl1    stuckia1
barraudqu   bouquetr1   devantheyj    ferrarip  gonthierc    huguenindo  koggalamt2   merillata  sacchettip  wohlhauserfa
barzaghim1  brossardl1  dilke         geiserj   haussenero   jaeggil     mafillem     nothj      sampaolof1  zeinalovd
bastosda1   cattarinn1  eltschingera  gerbert3  hazerajh     kilchert1   marquesrda1  pachoude1  sejdio1
huguenindo@lozan0:~$ ls ./././././
cat2.txt  cat.txt  gameshell-save.sh  gameshell.sh  test.tmp  tmp
huguenindo@lozan0:~$ ls ./..
admin       borcardj    deojt         faivrel   germaniertr  henochrjt   kneubuehlv   maurerr1   riederl1    stuckia1
barraudqu   bouquetr1   devantheyj    ferrarip  gonthierc    huguenindo  koggalamt2   merillata  sacchettip  wohlhauserfa
barzaghim1  brossardl1  dilke         geiserj   haussenero   jaeggil     mafillem     nothj      sampaolof1  zeinalovd
bastosda1   cattarinn1  eltschingera  gerbert3  hazerajh     kilchert1   marquesrda1  pachoude1  sejdio1
huguenindo@lozan0:~$ ls ./../..
bin   dev  home        initrd.img.old  lib64       media  opt   root  sbin  sys  usr  vmlinuz
boot  etc  initrd.img  lib             lost+found  mnt    proc  run   srv   tmp  var  vmlinuz.old

huguenindo@lozan0:~$ set -x
+ set -x
huguenindo@lozan0:~$ cd ~
+ cd /home/huguenindo
huguenindo@lozan0:~$ echo $HOME
+ echo /home/huguenindo
/home/huguenindo
huguenindo@lozan0:~$ cd ~maurerr1
+ cd /home/maurerr1
huguenindo@lozan0:/home/maurerr1$ cd -
+ cd -
/home/huguenindo

huguenindo@lozan0:~$ file cat.txt 
cat.txt: ASCII text
huguenindo@lozan0:~$ file /bin/ls
/bin/ls: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=15dfff3239aa7c3b16a71e6b2e3b6e4009dab998, for GNU/Linux 3.2.0, stripped
huguenindo@lozan0:~$ file /dev/sda
/dev/sda: block special (8/0)
huguenindo@lozan0:~$ file /dev/pts/0
/dev/pts/0: character special (136/0)

huguenindo@lozan0:~$ ls 
cat2.txt  cat.txt  gameshell-save.sh  gameshell.sh  test.tmp  tmp
huguenindo@lozan0:~$ set -x
huguenindo@lozan0:~$ ls g*
+ ls --color=auto gameshell-save.sh gameshell.sh
gameshell-save.sh  gameshell.sh
huguenindo@lozan0:~$ ls --color=auto gameshell-save.sh gameshell.sh
+ ls --color=auto --color=auto gameshell-save.sh gameshell.sh
gameshell-save.sh  gameshell.sh
huguenindo@lozan0:~$ ls ?a*
+ ls --color=auto cat2.txt cat.txt gameshell-save.sh gameshell.sh
cat2.txt  cat.txt  gameshell-save.sh  gameshell.sh
huguenindo@lozan0:~$ ls [cg]*
+ ls --color=auto cat2.txt cat.txt gameshell-save.sh gameshell.sh
cat2.txt  cat.txt  gameshell-save.sh  gameshell.sh
huguenindo@lozan0:~$ ls [ct]*
+ ls --color=auto cat2.txt cat.txt test.tmp tmp
cat2.txt  cat.txt  test.tmp

tmp:
ls.log  monLienHard.txt  monLienSymbolique.txt  wc.log
huguenindo@lozan0:~$ ls [c-t]*
+ ls --color=auto cat2.txt cat.txt gameshell-save.sh gameshell.sh test.tmp tmp
cat2.txt  cat.txt  gameshell-save.sh  gameshell.sh  test.tmp

tmp:
ls.log  monLienHard.txt  monLienSymbolique.txt  wc.log
huguenindo@lozan0:~$ ls [!c-t]*
+ ls --color=auto '[!c-t]*'
ls: impossible d'accéder à '[!c-t]*': Aucun fichier ou dossier de ce type
huguenindo@lozan0:~$ ls a{1..10}
+ ls --color=auto a1 a2 a3 a4 a5 a6 a7 a8 a9 a10
ls: impossible d'accéder à 'a1': Aucun fichier ou dossier de ce type
ls: impossible d'accéder à 'a2': Aucun fichier ou dossier de ce type
ls: impossible d'accéder à 'a3': Aucun fichier ou dossier de ce type
ls: impossible d'accéder à 'a4': Aucun fichier ou dossier de ce type
ls: impossible d'accéder à 'a5': Aucun fichier ou dossier de ce type
ls: impossible d'accéder à 'a6': Aucun fichier ou dossier de ce type
ls: impossible d'accéder à 'a7': Aucun fichier ou dossier de ce type
ls: impossible d'accéder à 'a8': Aucun fichier ou dossier de ce type
ls: impossible d'accéder à 'a9': Aucun fichier ou dossier de ce type
ls: impossible d'accéder à 'a10': Aucun fichier ou dossier de ce type
huguenindo@lozan0:~$ cd tmp
+ cd tmp
huguenindo@lozan0:~/tmp$ touch a{1..10}
+ touch a1 a2 a3 a4 a5 a6 a7 a8 a9 a10
huguenindo@lozan0:~/tmp$ ls
+ ls --color=auto
a1  a10  a2  a3  a4  a5  a6  a7  a8  a9  ls.log  monLienHard.txt  monLienSymbolique.txt  wc.log
huguenindo@lozan0:~/tmp$ ls a{1..10}
+ ls --color=auto a1 a2 a3 a4 a5 a6 a7 a8 a9 a10
a1  a10  a2  a3  a4  a5  a6  a7  a8  a9
huguenindo@lozan0:~/tmp$ ls a{!1..10}
ls a{exit..10}
+ ls --color=auto 'a{exit..10}'
ls: impossible d'accéder à 'a{exit..10}': Aucun fichier ou dossier de ce type
huguenindo@lozan0:~/tmp$ set +x
+ set +x
huguenindo@lozan0:~/tmp$ ls a[1-10]
a1
huguenindo@lozan0:~/tmp$ ls a[1-10]
a1
huguenindo@lozan0:~/tmp$ ls a{1..10}
a1  a10  a2  a3  a4  a5  a6  a7  a8  a9
huguenindo@lozan0:~/tmp$ ls a[1-9]
a1  a2  a3  a4  a5  a6  a7  a8  a9
huguenindo@lozan0:~/tmp$ ls a[1-9]*
a1  a10  a2  a3  a4  a5  a6  a7  a8  a9
huguenindo@lozan0:~/tmp$ ls a[1-9]?
a10

huguenindo@lozan0:~/tmp$ cat < /dev/zero > /dev/null 
^Z
[1]+  Stoppé                 cat < /dev/zero > /dev/null
huguenindo@lozan0:~/tmp$ bg
[1]+ cat < /dev/zero > /dev/null &
huguenindo@lozan0:~/tmp$ jobs
[1]+  En cours d'exécution   cat < /dev/zero > /dev/null &
huguenindo@lozan0:~/tmp$ ps -xf
    PID TTY      STAT   TIME COMMAND
2665047 ?        S      0:01 sshd: huguenindo@pts/5
2665048 pts/5    Ss     0:00  \_ -bash
2677334 pts/5    R      0:56      \_ cat
2677337 pts/5    R+     0:00      \_ ps -xf
2665025 ?        Ss     0:00 /lib/systemd/systemd --user
2665028 ?        S      0:00  \_ (sd-pam)
huguenindo@lozan0:~/tmp$ top

top - 10:22:23 up 90 days, 19:55,  9 users,  load average: 0.61, 0.21, 0.07
Tâches: 142 total,   2 en cours, 140 en veille,   0 arrêté,   0 zombie
%Cpu(s):  3.7 ut, 96.3 sy,  0.0 ni,  0.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 
MiB Mem :    856.9 total,    123.8 libr,    530.5 util,    365.4 tamp/cache  
MiB Éch :      0.0 total,      0.0 libr,      0.0 util.    326.4 dispo Mem 

    PID UTIL.     PR  NI    VIRT    RES    SHR S  %CPU  %MEM    TEMPS+ COM.  
2677334 hugueni+  20   0    5616    892    800 R  99.7   0.1   1:14.08 cat   
      1 root      20   0  168276  10964   7492 S   0.0   1.2  44:44.04 syst+ 
      2 root      20   0       0      0      0 S   0.0   0.0   0:01.12 kthr+ 
      3 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 rcu_+ 
      4 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 rcu_+ 
      5 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 slub+ 
      6 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 netns 
      8 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 kwor+ 
     10 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 mm_p+ 
     11 root      20   0       0      0      0 I   0.0   0.0   0:00.00 rcu_+ 
     12 root      20   0       0      0      0 I   0.0   0.0   0:00.00 rcu_+ 
     13 root      20   0       0      0      0 I   0.0   0.0   0:00.00 rcu_+ 
     14 root      20   0       0      0      0 S   0.0   0.0   3:26.34 ksof+ 
     15 root      20   0       0      0      0 I   0.0   0.0  80:56.20 rcu_+ 
     16 root      rt   0       0      0      0 S   0.0   0.0   1:12.95 migr+ 
     18 root      20   0       0      0      0 S   0.0   0.0   0:00.00 cpuh+ 
     20 root      20   0       0      0      0 S   0.0   0.0   0:00.00 kdev+ 
     21 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 inet+ 
     22 root      20   0       0      0      0 S   0.0   0.0   0:00.00 kaud+ 
     24 root      20   0       0      0      0 S   0.0   0.0   0:05.09 khun+ 
     25 root      20   0       0      0      0 S   0.0   0.0   0:00.00 oom_+ 
     28 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 writ+ 
     29 root      20   0       0      0      0 S   0.0   0.0   7:10.66 kcom+ 
     30 root      25   5       0      0      0 S   0.0   0.0   0:00.00 ksmd  
     31 root      39  19       0      0      0 S   0.0   0.0   1:35.94 khug+ 
huguenindo@lozan0:~/tmp$ cat < /dev/zero > /dev/null &
[2] 2677354
huguenindo@lozan0:~/tmp$ jobs
[1]-  En cours d'exécution   cat < /dev/zero > /dev/null &
[2]+  En cours d'exécution   cat < /dev/zero > /dev/null &
huguenindo@lozan0:~/tmp$ top

top - 10:23:05 up 90 days, 19:56,  9 users,  load average: 1.04, 0.37, 0.14
Tâches: 143 total,   3 en cours, 140 en veille,   0 arrêté,   0 zombie
%Cpu(s):  3.0 ut, 97.0 sy,  0.0 ni,  0.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 
MiB Mem :    856.9 total,    123.8 libr,    530.3 util,    365.5 tamp/cache  
MiB Éch :      0.0 total,      0.0 libr,      0.0 util.    326.6 dispo Mem 

    PID UTIL.     PR  NI    VIRT    RES    SHR S  %CPU  %MEM    TEMPS+ COM.  
2677334 hugueni+  20   0    5616    892    800 R  49.3   0.1   1:48.52 cat   
2677354 hugueni+  20   0    5616    892    804 R  49.3   0.1   0:07.75 cat   
   3982 prometh+  20   0 1319756  28612   9416 S   1.0   3.3      7,41 prom+ 
    496 message+  20   0    9716   4920   3720 S   0.3   0.6 120:18.75 dbus+ 
2039896 consul    20   0 1359556  48132  13832 S   0.3   5.5 120:47.20 cons+ 
2665047 hugueni+  20   0   18160   6392   4512 S   0.3   0.7   0:01.20 sshd  
2677355 hugueni+  20   0   11852   5380   3444 R   0.3   0.6   0:00.01 top   
      1 root      20   0  168276  10964   7492 S   0.0   1.2  44:44.04 syst+ 
      2 root      20   0       0      0      0 S   0.0   0.0   0:01.12 kthr+ 
      3 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 rcu_+ 
      4 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 rcu_+ 
      5 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 slub+ 
      6 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 netns 
      8 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 kwor+ 
     10 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 mm_p+ 
     11 root      20   0       0      0      0 I   0.0   0.0   0:00.00 rcu_+ 
     12 root      20   0       0      0      0 I   0.0   0.0   0:00.00 rcu_+ 
     13 root      20   0       0      0      0 I   0.0   0.0   0:00.00 rcu_+ 
     14 root      20   0       0      0      0 S   0.0   0.0   3:26.34 ksof+ 
     15 root      20   0       0      0      0 I   0.0   0.0  80:56.20 rcu_+ 
     16 root      rt   0       0      0      0 S   0.0   0.0   1:12.95 migr+ 
     18 root      20   0       0      0      0 S   0.0   0.0   0:00.00 cpuh+ 
     20 root      20   0       0      0      0 S   0.0   0.0   0:00.00 kdev+ 
     21 root       0 -20       0      0      0 I   0.0   0.0   0:00.00 inet+ 
     22 root      20   0       0      0      0 S   0.0   0.0   0:00.00 kaud+ 
huguenindo@lozan0:~/tmp$ fg %1
cat < /dev/zero > /dev/null
^C
huguenindo@lozan0:~/tmp$ jobs
[2]+  En cours d'exécution   cat < /dev/zero > /dev/null &
huguenindo@lozan0:~/tmp$ kill %2
huguenindo@lozan0:~/tmp$ 
[2]+  Complété              cat < /dev/zero > /dev/null
huguenindo@lozan0:~/tmp$ jobs

huguenindo@lozan0:~/tmp$ date
mer 04 fév 2026 10:10:29 UTC
huguenindo@lozan0:~/tmp$ echo $?
0
huguenindo@lozan0:~/tmp$ date --erreur
date : option non reconnue '--erreur'

Saisissez « date --help » pour plus d'informations.
huguenindo@lozan0:~/tmp$ echo $?
1
huguenindo@lozan0:~/tmp$ date; pwd
mer 04 fév 2026 10:11:35 UTC
/home/huguenindo/tmp
huguenindo@lozan0:~/tmp$ date && pwd
mer 04 fév 2026 10:12:06 UTC
/home/huguenindo/tmp
huguenindo@lozan0:~/tmp$ date --erreur && pwd
date : option non reconnue '--erreur'

Saisissez « date --help » pour plus d'informations.


huguenindo@lozan0:~/tmp$ ls -1 /
bin
boot
dev
etc
home
initrd.img
initrd.img.old
lib
lib64
lost+found
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var
vmlinuz
vmlinuz.old
huguenindo@lozan0:~/tmp$ ls -1 / | sort
bin
boot
dev
etc
home
initrd.img
initrd.img.old
lib
lib64
lost+found
media
mnt
opt
proc
root
run
sbin
srv
sys
tmp
usr
var
vmlinuz
vmlinuz.old

```

![xournal](<../../Cours_Mylos/wiki/xournal/2026-02-04-Note-09-45-1.svg>)

![xournal](<../../Cours_Mylos/wiki/xournal/2026-02-04-Note-09-45-2.svg>)

![xournal](<../../Cours_Mylos/wiki/xournal/2026-02-04-Note-09-45-3.svg>)
