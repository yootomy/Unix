# SYSNIX - Activités, série 0004 - Gestion des accès (Éléments de solution)
[[_TOC_]]
## Objectifs: 

* Gestion accès et autorisation

## Exercices

### 1

Créez 3 fichiers dans `~`

```
file1
file2
file3
```

```bash
huguenindo@lozan:tmp$ touch ./file{1..3}
```
```bash
huguenindo@lozan:tmp$ ls -l ./file[1-3]
-rw------- 1 huguenindo domain users 0 nov 21 08:32 ./file1
-rw------- 1 huguenindo domain users 0 nov 21 08:32 ./file2
-rw------- 1 huguenindo domain users 0 nov 21 08:32 ./file3
```

Vérifier les droits par défaut.

### 2

Assignez les droits suivants grâce à la forme littérale
```
file1 rwx------
file2 r--r-----
file3 r----x--x
```

```bash
huguenindo@lozan:tmp$ chmod u=rwx,go= ./file1

huguenindo@lozan:tmp$ chmod ug=r,o= ./file2

huguenindo@lozan:tmp$ chmod u=r,g=x,o=x ./file3
#ou
huguenindo@lozan:tmp$ chmod u=r,go=x ./file3
```
```
huguenindo@lozan:tmp$ ls -l ./file[1-3]
-rwx------ 1 huguenindo domain users 0 nov 21 08:32 ./file1
-r--r--r-- 1 huguenindo domain users 0 nov 21 08:32 ./file2
-r----x--x 1 huguenindo domain users 0 nov 21 08:32 ./file3
```

### 3

A l’aide de la forme octale , définissez les droits d’accès comme suit :
```
file1 r-x-----x
file2 -w--w--w-
file3 ---rwx--x
```

```bash
huguenindo@lozan:tmp$ chmod 0501 ./file1
huguenindo@lozan:tmp$ chmod 0222 ./file2
huguenindo@lozan:tmp$ chmod 0071 ./file3
```
```bash
huguenindo@lozan:tmp$ ls -l ./file[1-3]
-r-x-----x 1 huguenindo domain users 0 nov 21 08:32 ./file1
--w--w--w- 1 huguenindo domain users 0 nov 21 08:32 ./file2
----rwx--x 1 huguenindo domain users 0 nov 21 08:32 ./file3
```
### 4

1. Insérez un texte dans le fichier file1. Constatations ?
1. Idem pour file2. Constatations ?
1. Idem pour file3. Constatations ?

```bash
huguenindo@lozan:tmp$ ls -l ./file[1-3]
-r-x-----x 1 huguenindo domain users 0 nov 21 08:32 ./file1
--w--w--w- 1 huguenindo domain users 0 nov 21 08:32 ./file2
----rwx--x 1 huguenindo domain users 0 nov 21 08:32 ./file3
```

```bash
huguenindo@lozan:tmp$ echo "coucou" >> ./file1
-bash: ./file1: Permission non accordée
```
Le propriétaire __n__'a __pas__ le __droit__ de modifier le fichier.

```bash
huguenindo@lozan:tmp$ echo "coucou" >> ./file2
```
Le propriétaire __a__ le __droit__ de modifier le fichier.

```bash
huguenindo@lozan:tmp$ echo "coucou" >> ./file3
-bash: ./file3: Permission non accordée
```
LE propriétaire n'a __aucun droit__ sur le fichier

### 5

Assigner les droits suivants:
```
file1 ---------
file2 r--------
file3 rw-------
```

```bash
huguenindo@lozan:tmp$ chmod 0000 ./file1
huguenindo@lozan:tmp$ chmod 0400 ./file2
huguenindo@lozan:tmp$ chmod 0600 ./file3
```
```bash
huguenindo@lozan:tmp$ ls -l ./file[1-3]
---------- 1 huguenindo domain users 0 nov 21 08:32 ./file1
-r-------- 1 huguenindo domain users 7 nov 21 08:38 ./file2
-rw------- 1 huguenindo domain users 0 nov 21 08:32 ./file3
```

* Copier le fichier file1 en file4. Constations ?

  L'utilisateur n'a pas le droit de lecture du fichier `./file1`

    ```bash
    huguenindo@lozan:tmp$ cp ./file1 ./file4
    cp: impossible d'ouvrir «./file1» en lecture: Permission non accordée
    ```

* Copier le fichier file2 en file5 et regarder les droits d’accès. Constatations ?

    le fichier `./file5` est créé avec les mêmes droits que le fichier `./file2`

    ```bash
    huguenindo@lozan:tmp$ cp ./file2 ./file5
    huguenindo@lozan:tmp$ ls -l ./file?
    ---------- 1 huguenindo domain users 0 nov 21 08:32 ./file1
    -r-------- 1 huguenindo domain users 7 nov 21 08:38 ./file2
    -rw------- 1 huguenindo domain users 0 nov 21 08:32 ./file3
    -r-------- 1 huguenindo domain users 7 nov 21 08:44 ./file5
    ```

* Supprimez les fichiers file1 à file5. Constations ?

    La suppression des fichiers est possible. Le droit de suppression est lié au dossier contenant les fichier.

    ```bash
    huguenindo@lozan:tmp$ rm ./file?
    rm : supprimer fichier vide (protégé en écriture) «./file1» ? y
    rm : supprimer fichier (protégé en écriture) «./file2» ? y
    rm : supprimer fichier (protégé en écriture) «./file5» ? y
    ```
    ```bash
    huguenindo@lozan:tmp$ ls -l ./file?
    ls: impossible d'accéder à ./file?: Aucun fichier ou dossier de ce type
    ```

### 6

Créez un répertoire ~/test avec les droits suivants :
```
test drwx------
```

```bash
huguenindo@lozan:~$ mkdir -m u=rwx,go= ./test
```
```bash
huguenindo@lozan:~$ ls -ld ./test
drwx------ 2 huguenindo domain users 4096 nov 21 10:30 ./test
```

* Dans le répertoire test, créez les fichier file1,file2,file5,file6,file7 
    ```bash
    huguenindo@lozan:tmp$ touch ./test/file{1..2} ./test/file{5..7}
    ```
    ```bash
    huguenindo@lozan:tmp$ ls -l ./test/
    total 0
    -rw------- 1 huguenindo domain users 0 nov 21 11:01 file1
    -rw------- 1 huguenindo domain users 0 nov 21 11:01 file2
    -rw------- 1 huguenindo domain users 0 nov 21 11:01 file5
    -rw------- 1 huguenindo domain users 0 nov 21 11:01 file6
    -rw------- 1 huguenindo domain users 0 nov 21 11:01 file7
    ```
* Dans le répertoire test, créez un fichier testdroit.txt. Droits par défaut ?
    ```bash
    huguenindo@lozan:tmp$ touch ./test/testdroit.txt
    ```
    ```bash
    huguenindo@lozan:tmp$ ls -l ./test/
    total 0
    -rw------- 1 huguenindo domain users 0 nov 21 11:01 file1
    -rw------- 1 huguenindo domain users 0 nov 21 11:01 file2
    -rw------- 1 huguenindo domain users 0 nov 21 11:01 file5
    -rw------- 1 huguenindo domain users 0 nov 21 11:01 file6
    -rw------- 1 huguenindo domain users 0 nov 21 11:01 file7
    -rw------- 1 huguenindo domain users 0 nov 21 11:02 testdroit.txt
    ```
    ```bash
    huguenindo@lozan:tmp$ umask
    0077
    ```

    `umask ` retire les droits `rwx` au groupe et au reste du monde.

* Ajouter un texte dans ce fichier. Constatations? 

    L'ajout est possible.
    ```bash
    huguenindo@lozan:tmp$ echo "coucou" >> ./test/testdroit.txt
    ```
    ```bash
    huguenindo@lozan:tmp$ cat ./test/testdroit.txt
    coucou
    ```

* Supprimer le fichier file1 . Constatations?

    La suppression est possible.
    ```bash
    huguenindo@lozan:tmp$ rm ./test/file1 
    ```
    ```
    huguenindo@lozan:tmp$ ls -l ./test/ | grep file1
    ```

### 7
Positionnez-vous sur le répertoire « parent » de test et modifier les droits comme suit : `test drw-------`
```bash
huguenindo@lozan:tmp$ pwd
/home/S2/huguenindo/tmp

huguenindo@lozan:tmp$ chmod u=rw,go= ./test
huguenindo@lozan:tmp$ ls -ld ./test
drw------- 2 huguenindo domain users 4096 nov 21 11:06 ./test
```

* Visualisez le contenu du répertoire test et vérifiez les droits d’accès du fichier testdroit.txt. Constatation ?

    L'absence de droit `x` empêche d'être dans le dossier. 
    ```bash
    huguenindo@lozan:tmp$ ls -l ./test
    ls: impossible d'accéder à ./test/file7: Permission non accordée
    ls: impossible d'accéder à ./test/file6: Permission non accordée
    ls: impossible d'accéder à ./test/testdroit.txt: Permission non accordée
    ls: impossible d'accéder à ./test/file5: Permission non accordée
    ls: impossible d'accéder à ./test/file2: Permission non accordée
    total 0
    -????????? ? ? ? ?            ? file2
    -????????? ? ? ? ?            ? file5
    -????????? ? ? ? ?            ? file6
    -????????? ? ? ? ?            ? file7
    -????????? ? ? ? ?            ? testdroit.txt
    ```

* Créer un nouveau fichier testdroit1.txt dans le répertoire test. Constations ?

    L'absence de droit `x` empêche d'être dans le dossier. 

    ```bash
    huguenindo@lozan:tmp$ touch ./test/testdroit1.txt
    touch: impossible de faire un touch «./test/testdroit1.txt»: Permission non accordée
    ```
* Supprimez le fichier file2. Constations ?

    L'absence de droit `x` empêche d'être dans le dossier. 

    ```bash
    huguenindo@lozan:tmp$ rm ./test/file2
    rm: impossible de supprimer «./test/file2»: Permission non accordée
    ```

### 8
Positionnez-vous sur le répertoire « parent » de test et modifier les droits comme suit : `test d-w-------`

```bash
huguenindo@lozan:tmp$ chmod u=w,go= ./test
huguenindo@lozan:tmp$ ls -ld ./test/
d-w------- 2 huguenindo domain users 4096 nov 21 11:06 ./test/
```

* Visualisez le contenu du répertoire `./test` et vérifiez les droits d’accès aux fichiers contenus dans ce répertoire. Constatation ?
    ```bash
    huguenindo@lozan:tmp$ ls -l ./test/
    ls: impossible d'ouvrir le répertoire ./test/: Permission non accordée
    ```

### 9

Positionnez-vous sur le répertoire « parent » de test et modifier les droits comme suit : `test dr--------`

```bash
huguenindo@lozan:tmp$ ls -ld ./test/
dr-------- 2 huguenindo domain users 4096 nov 21 11:06 ./test/
```

* Visualisez le contenu du répertoire test et vérifiez les droits d’accès aux fichiers contenus dans ce répertoire. Constatation ?

    ```bash
    huguenindo@lozan:tmp$ ls -l ./test/
    ls: impossible d'accéder à ./test/file7: Permission non accordée
    ls: impossible d'accéder à ./test/file6: Permission non accordée
    ls: impossible d'accéder à ./test/testdroit.txt: Permission non accordée
    ls: impossible d'accéder à ./test/file5: Permission non accordée
    ls: impossible d'accéder à ./test/file2: Permission non accordée
    total 0
    -????????? ? ? ? ?            ? file2
    -????????? ? ? ? ?            ? file5
    -????????? ? ? ? ?            ? file6
    -????????? ? ? ? ?            ? file7
    -????????? ? ? ? ?            ? testdroit.txt
    ```

### 10
Positionnez-vous sur le répertoire « parent » de test et modifier les droits comme suit : `test dr-x------`

```bash
huguenindo@lozan:tmp$ chmod u=rx,go= ./test
huguenindo@lozan:tmp$ ls -ld ./test/
dr-x------ 2 huguenindo domain users 4096 nov 21 11:06 ./test/
```

* Visualisez le contenu du répertoire test et vérifiez les droits d’accès aux fichiers contenus dans ce répertoire. Constatation ?

    ```bash
    huguenindo@lozan:tmp$ ls -l ./test/
    total 4
    -rw------- 1 huguenindo domain users 0 nov 21 11:01 file2
    -rw------- 1 huguenindo domain users 0 nov 21 11:01 file5
    -rw------- 1 huguenindo domain users 0 nov 21 11:01 file6
    -rw------- 1 huguenindo domain users 0 nov 21 11:01 file7
    -rw------- 1 huguenindo domain users 7 nov 21 11:05 testdroit.txt
    ```

* Créez un nouveau fichier testdroit5.txt dans le répertoire test. Remarques ?

    ```bash
    huguenindo@lozan:tmp$ touch ./test/testdroit5.txt
    touch: impossible de faire un touch «./test/testdroit5.txt»: Permission non accordée
    ```

* Ajoutez un texte  au fichier file5. Constations ?
    ```bash
    huguenindo@lozan:tmp$ echo "coucou" >>  ./test/file5
    huguenindo@lozan:tmp$ cat ./test/file5
    coucou
    ```

* Supprimez le fichier file5. Constatations ?

    ```bash
    huguenindo@lozan:tmp$ rm ./test/file5
    rm: impossible de supprimer «./test/file5»: Permission non accordée
    ```

### 11
Positionnez-vous sur le répertoire « parent » de test et modifier les droits comme suit : `test d--x------`

    ```bash
    huguenindo@lozan:tmp$ chmod u=x,go= ./test
    huguenindo@lozan:tmp$ ls -ld ./test/
    d--x------ 2 huguenindo domain users 4096 nov 21 11:06 ./test/
    ```

* Visualisez le contenu du répertoire test et vérifiez les droits d’accès aux fichiers contenus dans ce répertoire. Constatations ?

    ```bash
    huguenindo@lozan:tmp$ ls -l ./test/
    ls: impossible d'ouvrir le répertoire ./test/: Permission non accordée
    ```

* Créez un fichier testdroit6.txt dans test. Constatations ?
    ```bash
    huguenindo@lozan:tmp$ touch ./test/testdroit6.txt
    touch: impossible de faire un touch «./test/testdroit6.txt»: Permission non accordée
    ```

* Ajoutez un texte de votre choix au fichier file6. Constatations ?
    ```bash
    huguenindo@lozan:tmp$ echo "coucou" >>  ./test/file6
    huguenindo@lozan:tmp$ cat ./test/file6
    coucou
    ```

* Supprimez le fichier file6. Constatations ?
    ```bash
    huguenindo@lozan:tmp$ rm  ./test/file6
    rm: impossible de supprimer «./test/file6»: Permission non accordée
    ```

### 12
Positionnez-vous sur le répertoire « parent » de test et modifier les droits comme suit : `test d-wx------`

```bash
huguenindo@lozan:tmp$ chmod u=wx,go= ./test
huguenindo@lozan:tmp$ ls -ld ./test/
d-wx------ 2 huguenindo domain users 4096 nov 21 11:06 ./test/
```

* Visualisez le contenu du répertoire test et vérifiez les droits d’accès aux fichiers contenus dans ce répertoire. Constatations ?
    ```bash
    huguenindo@lozan:tmp$ ls -l ./test/
    ls: impossible d'ouvrir le répertoire ./test/: Permission non accordée
    ```

* Créez un fichier testdroit7.txt dans test. Constatations ?

    Les droits permettent de créer un fichier et de voir le contenu du fichier.
    ```bash
    huguenindo@lozan:tmp$ touch ./test/testdroit7.txt
    huguenindo@lozan:tmp$ cat ./test/testdroit7.txt
    huguenindo@lozan:tmp$  ls -l ./test/testdroit7.txt
    -rw-rw-r-- 1 huguenindo huguenindo 29 Sep 23 08:11 ./test/testdroit7.txt
    huguenindo@lozan:tmp$ ls -l ./test/
    ls: cannot open directory './test/': Permission denied    
    ```

* Ajoutez un texte de votre choix au fichier file7. Constatations ?
    ```bash
    huguenindo@lozan:tmp$ echo "coucou" >>  ./test/file7
    huguenindo@lozan:tmp$ cat ./test/file7
    coucou
    huguenindo@lozan:tmp$ ls -l ./test/file7
    -rw-rw-r-- 1 huguenindo huguenindo 7 Sep 23 08:16 ./test/file7
    huguenindo@lozan:tmp$ ls -l ./test
    ls: cannot open directory './test': Permission denied    
    ```

* Supprimez le fichier file7. Constatations ?
    ```bash
    huguenindo@lozan:tmp$ rm ./test/file7
    huguenindo@lozan:tmp$ ls -l ./test/file7
    ls: cannot access './test/file7': No such file or directory
    huguenindo@lozan:tmp$ ls -l ./test
    ls: cannot open directory './test': Permission denied    
    ```

### 13
Créer un sous-répertoire test_sec et y placer quelques fichiers.

```bash
huguenindo@lozan:tmp$ umask 0077
huguenindo@lozan:tmp$ mkdir ./test_sec
huguenindo@lozan:tmp$ ls -ld ./test_sec/
drwx------ 2 huguenindo huguenindo 4096 Sep 23 08:18 ./test_sec/
huguenindo@lozan:tmp$ touch ./test_sec/file{1..4}
huguenindo@lozan:tmp$ ls -l ./test_sec/
total 0
-rw------- 1 huguenindo huguenindo 0 Sep 23 08:18 file1
-rw------- 1 huguenindo huguenindo 0 Sep 23 08:18 file2
-rw------- 1 huguenindo huguenindo 0 Sep 23 08:18 file3
-rw------- 1 huguenindo huguenindo 0 Sep 23 08:18 file4
```

### 14
Placer les bons codes de protection à votre répertoire test_sec et à ses fichiers afin de permettre aux membres de votre groupe de:

* lire le contenu des fichiers
    ```bash
    huguenindo@lozan:tmp$ chmod -r g=rX ./test_sec


    huguenindo@lozan:tmp$ ls -l ./test_sec/
    total 0
    -rw-r----- 1 huguenindo domain users 0 nov 21 12:50 file1
    -rw-r----- 1 huguenindo domain users 0 nov 21 12:50 file2
    -rw-r----- 1 huguenindo domain users 0 nov 21 12:50 file3
    -rw-r----- 1 huguenindo domain users 0 nov 21 12:50 file4
    ```

* lister les fichiers sans pouvoir lire leur contenu
    ```bash
    huguenindo@lozan:tmp$ chmod g=rx ./test_sec 
    huguenindo@lozan:tmp$ chmod g= ./test_sec/file? 

    huguenindo@lozan:tmp$ ls -ld ./test_sec/;ls -l ./test_sec/
    qdrwxr-x--- 2 huguenindo domain users 4096 nov 21 12:50 ./test_sec/
    total 0
    -rw------- 1 huguenindo domain users 0 nov 21 12:50 file1
    -rw------- 1 huguenindo domain users 0 nov 21 12:50 file2
    -rw------- 1 huguenindo domain users 0 nov 21 12:50 file3
    -rw------- 1 huguenindo domain users 0 nov 21 12:50 file4
    ```

* lire le contenu d'un fichier connu sans pouvoir faire la liste des fichiers
    ```bash
    huguenindo@lozan:tmp$ chmod g=x ./test_sec 
    huguenindo@lozan:tmp$ chmod g=r ./test_sec/file? 
    huguenindo@lozan:tmp$ ls -ld ./test_sec/;ls -l ./test_sec/
    drwx--x--- 2 huguenindo domain users 4096 nov 21 12:50 ./test_sec/
    total 0
    -rw-r----- 1 huguenindo domain users 0 nov 21 12:50 file1
    -rw-r----- 1 huguenindo domain users 0 nov 21 12:50 file2
    -rw-r----- 1 huguenindo domain users 0 nov 21 12:50 file3
    -rw-r----- 1 huguenindo domain users 0 nov 21 12:50 file4
    ```

* modifier un fichier existant
    ```bash
    huguenindo@lozan:tmp$ chmod g=rx ./test_sec 
    huguenindo@lozan:tmp$ chmod g=rw ./test_sec/file?
    huguenindo@lozan:tmp$ huguenindo@lozan:tmp$ ls -ld ./test_sec/;ls -l ./test_sec/
    total 0
    -rw-rw---- 1 huguenindo domain users 0 nov 21 12:50 file1
    -rw-rw---- 1 huguenindo domain users 0 nov 21 12:50 file2
    -rw-rw---- 1 huguenindo domain users 0 nov 21 12:50 file3
    -rw-rw---- 1 huguenindo domain users 0 nov 21 12:50 file4

    cat < ./test_sec/file?
    ```

* ajouter et effacer un fichier
    ```bash
    huguenindo@lozan:tmp$ chmod g=rwx ./test_sec/

    huguenindo@lozan:tmp$ ls -ld ./test_sec/;ls -l ./test_sec/
    drwxrwx--- 2 huguenindo domain users 4096 nov 21 12:50 ./test_sec/
    ```

## Application des permissions

### Identifier les droits d'accès

Mettre les droits d'accès sur les dossiers et fichiers de l'arborescence ci-dessous. 
1. Les fichiers txt ne sont pas exécutables.
1. Le propriétaire pier possède tous les droits sur les dossiers et fichiers l'arborescence
1. Les utilisateurs, appartenant au même groupe que pier, peuvent uniquement:
    1. lire le contenu, des dossiers et des fichiers, du dossier ./d1
    1. lire et ajouter de nouveaux fichiers dans le dossier ./d2.
1. Le reste des utilisateurs n'ont aucun droit dans l'arborescence de pier.

```
|
├── home [dr-xr-xr-x]  
│   │
│   └── pier [drwx--x---]  
│       │
│       ├── d1 [drwxr-x---]  
│       │   │
│       │   ├── f1.txt [-rw-r-----]  
│       │   │
│       │   ├── f2.txt [-rw-r-----]  
│       │   │
│       │   ├── f3.txt [-rw-r-----]  
│       │   │
│       │   ├── f4.txt [-rw-r-----] 
│       │   │
│       │   └── f5.txt [-rw-r-----]  
│       │   
│       └── d2 [drwxrwx---]  
│           │
│           ├── f1.txt [-rw-rw----]  
│           │
│           ├── f2.txt [-rw-rw----]  
│           │
│           ├── f3.txt [-rw-rw----]  
│           │
│           ├── f4.txt [-rw-rw----]  
│           │
│           └── f5.txt [-rw-rw----]  
```

### Tester les droits d'accès

Écrire les instructions de création/suppression/visualisation permettant de vérifier les accès autorisés et refusés des membres du même groupe de `pier`.

* Les utilisateurs, appartenant au même groupe que pier, peuvent traverser le dossier de pier
```
$ cd ./pier                # autorise
$ ls ./pier                # refusé
$ touch ./pier/fichier.txt # refusé

```

* Les utilisateurs, appartenant au même groupe que pier, peuvent lire le contenu, des dossiers et des fichiers, du dossier ./d1
```
$ cd ./pier/d1                            #autorisé
$ ls ./pier/d1                            #autorisé
$ touch ./pier/f10.txt                    #refusé
$ touch ./pier/d1/f10.txt                 #refusé
$ echo nouveau texte >> ./pier/d1/f1.txt  #refusé
$ cat ./pier/d1/f[1-5].txt                #autorisé
```

* Les utilisateurs, appartenant au même groupe que pier, peuvent lire et ajouter de nouveaux fichiers dans le dossier ./d2.
```
$ ls ./pier/d2                            #autorisé
$ touch ./pier/d2/f10.txt                 #autorisé
$ echo nouveau texte >> ./pier/d2/f1.txt  #autorisé
$ cat ./pier/d2/f[1-5].txt                #autorisé
```

### Création des fichiers de test
```
huguenindo@lozan:tmp$ mkdir -p ./pier/d{1..2} && touch ./pier/d{1..2}/f{1..5}.txt
```
```
huguenindo@lozan:tmp$ tree ./pier -p
./pier
├── [drwx------]  d1
│   ├── [-rw-------]  f1.txt
│   ├── [-rw-------]  f2.txt
│   ├── [-rw-------]  f3.txt
│   ├── [-rw-------]  f4.txt
│   └── [-rw-------]  f5.txt
└── [drwx------]  d2
    ├── [-rw-------]  f1.txt
    ├── [-rw-------]  f2.txt
    ├── [-rw-------]  f3.txt
    ├── [-rw-------]  f4.txt
    └── [-rw-------]  f5.txt
```


### Appliquer les droits d'accès
Écrire les instructions qui permettent d'appliquer les droits d'accès ci-dessus. 

* Le propriétaire possède tous les droits sur les dossiers et fichiers l'arborescence et le reste des utilisateurs n'ont aucun droit dans l'arborescence de pier.
```
huguenindo@lozan:tmp$ chmod u=rwX,g=X,o= ./pier
huguenindo@lozan:tmp$ chmod -R u=rwX,go= ./pier/d[1-2] 
huguenindo@lozan:tmp$ tree ./pier -p
[drwx--x---] ./pier
├── [drwx------]  d1
│   ├── [-rw-------]  f1.txt
│   ├── [-rw-------]  f2.txt
│   ├── [-rw-------]  f3.txt
│   ├── [-rw-------]  f4.txt
│   └── [-rw-------]  f5.txt
└── [drwx------]  d2
    ├── [-rw-------]  f1.txt
    ├── [-rw-------]  f2.txt
    ├── [-rw-------]  f3.txt
    ├── [-rw-------]  f4.txt
    └── [-rw-------]  f5.txt
```

* Les utilisateurs, appartenant au même groupe que pier, peuvent lire le contenu, des dossiers et des fichiers, du dossier ./d1
```
huguenindo@lozan:tmp$ chmod -R g=rX ./pier/d1
huguenindo@lozan:tmp$ tree ./pier -p
./pier
├── [drwxr-x---]  d1
│   ├── [-rw-r-----]  f1.txt
│   ├── [-rw-r-----]  f2.txt
│   ├── [-rw-r-----]  f3.txt
│   ├── [-rw-r-----]  f4.txt
│   └── [-rw-r-----]  f5.txt
└── [drwx------]  d2
    ├── [-rw-------]  f1.txt
    ├── [-rw-------]  f2.txt
    ├── [-rw-------]  f3.txt
    ├── [-rw-------]  f4.txt
    └── [-rw-------]  f5.txt
```

* Les utilisateurs, appartenant au même groupe que pier, peuvent lire et ajouter de nouveaux fichiers dans le dossier ./d2.
```
huguenindo@lozan:tmp$ chmod -R g=rwX ./pier/d2
huguenindo@lozan:tmp$ tree ./pier -p
./pier
├── [drwxr-x---]  d1
│   ├── [-rw-r-----]  f1.txt
│   ├── [-rw-r-----]  f2.txt
│   ├── [-rw-r-----]  f3.txt
│   ├── [-rw-r-----]  f4.txt
│   └── [-rw-r-----]  f5.txt
└── [drwxrwx---]  d2
    ├── [-rw-rw----]  f1.txt
    ├── [-rw-rw----]  f2.txt
    ├── [-rw-rw----]  f3.txt
    ├── [-rw-rw----]  f4.txt
    └── [-rw-rw----]  f5.txt
```



## Références

1. [Activité](https://mylos.cifom.ch/cours/int-sys1-nix/shell/activites/sysnix-activite-0004-gestion-acces/)
