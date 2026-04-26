#  SYSNIX - Activités, série 0002 - Gestion des fichiers (Éléments de solution)
[[_TOC_]]
##  Objectifs

* Introduction aux commandes UNIX 
* Gestion des répertoires et des fichiers

>* Résoudre chaque problème suivant en un minimum d'instructions. Généralement une instruction suffit
>* Écrire la commande permettant de vérifier le résultat


##  Exercices

###  1

Créer trois sous-répertoires dans votre «home directory»: trav1, trav2 et trav3.

```
dom@domx1:~$ cd ~/tmp
dom@domx1:tmp$ mkdir ./trav{1..3}
```
```
dom@domx1:tmp$ ls ./trav[1-3]
./trav1:

./trav2:

./trav3:
```

###  2

Copier dans le répertoire trav1 tous les fichiers .h dont le nom commence par a, b, c ou d et qui se trouvent dans le répertoire /usr/include.

```
dom@domx1:tmp$ cp /usr/include/[a-d]*.h ./trav1
cp: omission du répertoire '/usr/include/arpa'
cp: omission du répertoire '/usr/include/asm-generic'
cp: omission du répertoire '/usr/include/btrfs'
cp: omission du répertoire '/usr/include/c++'
cp: omission du répertoire '/usr/include/cups'
cp: omission du répertoire '/usr/include/cupsfilters'
cp: omission du répertoire '/usr/include/dbus-1.0'
cp: omission du répertoire '/usr/include/drm'
```
```
dom@domx1:tmp$ ls ./trav1/[a-d]*.h
./trav1/aio.h      ./trav1/argz.h         ./trav1/byteswap.h   ./trav1/crypt.h
./trav1/aliases.h  ./trav1/ar.h           ./trav1/cifsidmap.h  ./trav1/ctype.h
./trav1/alloca.h   ./trav1/assert.h       ./trav1/complex.h    ./trav1/dirent.h
./trav1/argp.h     ./trav1/autosprintf.h  ./trav1/cpio.h       ./trav1/dlfcn.h
```

###  3

Copier dans le répertoire trav2 tous les fichiers dont le nom commence par 3 caractères quelconques suivis d'un caractère compris entre e et z et se terminant par .h. Les fichiers sources se trouvent dans le répertoire /usr/include.

```
dom@domx1:tmp$ cp /usr/include/???[e-z]*.h ./trav2
```

```
dom@domx1:tmp$ ls ./trav2/???[e-z]*.h
./trav2/alloca.h       ./trav2/jpegint.h           ./trav2/resolv.h
./trav2/argp.h         ./trav2/jpeglib.h           ./trav2/sched.h
./trav2/argz.h         ./trav2/langinfo.h          ./trav2/search.h
./trav2/assert.h       ./trav2/lastlog.h           ./trav2/setjmp.h
./trav2/autosprintf.h  ./trav2/libgen.h            ./trav2/sgtty.h
./trav2/byteswap.h     ./trav2/libintl.h           ./trav2/signal.h
./trav2/cifsidmap.h    ./trav2/libio.h             ./trav2/spawn.h
./trav2/complex.h      ./trav2/libsync.h           ./trav2/stdint.h
./trav2/cpio.h         ./trav2/libudev.h           ./trav2/stdio_ext.h
./trav2/crypt.h        ./trav2/limits.h            ./trav2/stdio.h
./trav2/ctype.h        ./trav2/link.h              ./trav2/stdlib.h
./trav2/dirent.h       ./trav2/ltdl.h              ./trav2/string.h
./trav2/endian.h       ./trav2/malloc.h            ./trav2/strings.h
./trav2/envz.h         ./trav2/math.h              ./trav2/stropts.h
./trav2/errno.h        ./trav2/mcheck.h            ./trav2/sudo_plugin.h
./trav2/error.h        ./trav2/memory.h            ./trav2/sysexits.h
./trav2/fcntl.h        ./trav2/mntent.h            ./trav2/syslog.h
./trav2/features.h     ./trav2/monetary.h          ./trav2/termio.h
./trav2/fenv.h         ./trav2/mqueue.h            ./trav2/termios.h
./trav2/fmtmsg.h       ./trav2/nl_types.h          ./trav2/thread_db.h
./trav2/gawkapi.h      ./trav2/obstack.h           ./trav2/time.h
./trav2/gconv.h        ./trav2/paths.h             ./trav2/ttyent.h
./trav2/getopt.h       ./trav2/pcrecpparg.h        ./trav2/ucontext.h
./trav2/gettext-po.h   ./trav2/pcrecpp.h           ./trav2/ulimit.h
./trav2/gmpxx.h        ./trav2/pcre.h              ./trav2/unistd.h
./trav2/gnumake.h      ./trav2/pcreposix.h         ./trav2/utime.h
./trav2/iconv.h        ./trav2/pcre_scanner.h      ./trav2/utmp.h
./trav2/inttypes.h     ./trav2/pcre_stringpiece.h  ./trav2/utmpx.h
./trav2/jbig85.h       ./trav2/poll.h              ./trav2/values.h
./trav2/jbig_ar.h      ./trav2/printf.h            ./trav2/wait.h
./trav2/jbig.h         ./trav2/pthread.h           ./trav2/wctype.h
./trav2/jerror.h       ./trav2/regex.h             ./trav2/zconf.h
./trav2/jmorecfg.h     ./trav2/regexp.h

```

###  4

Lister le contenu de ces répertoires. 

```
dom@domx1:tmp$ ls ./trav?
./trav1:
aio.h      argp.h  assert.h       cifsidmap.h  crypt.h   dlfcn.h
aliases.h  argz.h  autosprintf.h  complex.h    ctype.h
alloca.h   ar.h    byteswap.h     cpio.h       dirent.h

./trav2:
alloca.h       gawkapi.h     libsync.h       pcre_stringpiece.h  sudo_plugin.h
argp.h         gconv.h       libudev.h       poll.h              sysexits.h
argz.h         getopt.h      limits.h        printf.h            syslog.h
assert.h       gettext-po.h  link.h          pthread.h           termio.h
autosprintf.h  gmpxx.h       ltdl.h          regex.h             termios.h
byteswap.h     gnumake.h     malloc.h        regexp.h            thread_db.h
cifsidmap.h    iconv.h       math.h          resolv.h            time.h
complex.h      inttypes.h    mcheck.h        sched.h             ttyent.h
cpio.h         jbig85.h      memory.h        search.h            ucontext.h
crypt.h        jbig_ar.h     mntent.h        setjmp.h            ulimit.h
ctype.h        jbig.h        monetary.h      sgtty.h             unistd.h
dirent.h       jerror.h      mqueue.h        signal.h            utime.h
endian.h       jmorecfg.h    nl_types.h      spawn.h             utmp.h
envz.h         jpegint.h     obstack.h       stdint.h            utmpx.h
errno.h        jpeglib.h     paths.h         stdio_ext.h         values.h
error.h        langinfo.h    pcrecpparg.h    stdio.h             wait.h
fcntl.h        lastlog.h     pcrecpp.h       stdlib.h            wctype.h
features.h     libgen.h      pcre.h          string.h            zconf.h
fenv.h         libintl.h     pcreposix.h     strings.h
fmtmsg.h       libio.h       pcre_scanner.h  stropts.h

./trav3:

```

###  5

Visualiser votre répertoire de travail courant et choisir trav3.

```
dom@domx1:tmp$ pwd
/home/dom/tmp
```
```
dom@domx1:tmp$ cd ./trav3
```
```
dom@domx1:trav3$ pwd
/home/dom/tmp/trav3
```

###  6

Copier dans trav3 les fichiers a.out.h, crypt.h et math.h qui se trouvent dans l’un de vos répertoires.

```
dom@domx1:trav3$ cd ~/tmp
dom@domx1:tmp$ cp ./*/{a.out.h,crypt.h,math.h} ./trav3
cp: impossible d'évaluer './*/a.out.h': Aucun fichier ou dossier de ce type
cp: n'écrasera pas './trav3/crypt.h' qui vient d'être créé par './trav2/crypt.h'
```

```
dom@domx1:tmp$ ls ./trav3/{a.out.h,crypt.h,math.h}
ls: impossible d'accéder à './trav3/a.out.h': Aucun fichier ou dossier de ce type
./trav3/crypt.h  ./trav3/math.h
```

```
dom@domx1:tmp$ ls ./trav3/{a.out.h,crypt.h,math.h} 2>/dev/null
./trav3/crypt.h  ./trav3/math.h
```

###  7

Renommer le fichier aliases.h du répertoire trav1 et math.h du répertoire trav3 en Aliases.H et Math.H.

```
dom@domx1:tmp$ ls ./trav?/{aliases,math}.h
./trav1/aliases.h  ./trav2/math.h
```
```
dom@domx1:tmp$ mv ./trav1/aliases.h ./trav1/Aliases.H
dom@domx1:tmp$ mv ./trav3/math.h ./trav3/Math.H
```
```
dom@domx1:tmp$ ls ./trav?/{Aliases,Math}.H
./trav1/Aliases.H  ./trav2/Math.H
```


#### version utilisant les expressions rationnelles

```
dom@domx1:tmp$ ls ./trav?/{aliases,math}.h
./trav1/aliases.h  ./trav2/math.h
```
```
dom@domx1:tmp$ rename -v 's/(.*\/)(.)(.*)\.(.)/$1\u$2$3.\u$4/' ./trav?/{aliases,math}.h
./trav1/aliases.h renamed as ./trav1/Aliases.H
./trav2/math.h renamed as ./trav2/Math.H
```
```
dom@domx1:tmp$ ls ./trav?/{Aliases,Math}.H
./trav1/Aliases.H  ./trav2/Math.H
```

###  8

Effacer tous les fichiers dont le nom commence par cry et qui se trouvent dans le répertoire trav1.


```
dom@domx1:tmp$ ls ./trav1/cry*
./trav2/crypt.h
```
```
dom@domx1:tmp$ rm ./trav1/cry*
```
```
dom@domx1:tmp$ ls ./trav1/cry*
ls: impossible d'accéder à './trav2/cry*': Aucun fichier ou dossier de ce type
```

###  9

Supprimer le répertoire trav3.

```
dom@domx1:tmp$ rm -R ./trav3
dom@domx1:tmp$ ls ./trav3
ls: impossible d'accéder à './trav3': Aucun fichier ou dossier de ce type
```

##  Références

1. Activités, série 0002 - Gestion des fichiers, https://mylos.cifom.ch/cours/int-sys1-nix/shell/activites/sysnix-activite-0002-gestion-fichier