# Corrige - Exercices permissions type activite 004

> Les commandes sont ecrites dans l'esprit du corrige du professeur :
> creation de l'arborescence, identification des tests, puis application des droits.
>
> Rappel utile : `X` dans `chmod` met le droit `x` uniquement sur les dossiers et sur les fichiers deja executables. C'est pratique pour garder les fichiers `.txt` non executables.

---

## Exercice 1 - `alpha`

### Creation des fichiers de test

```bash
mkdir -p ./alpha/{docs,drop}
touch ./alpha/docs/doc{1..3}.txt ./alpha/drop/old{1..2}.txt
```

### Droits attendus

```text
alpha [drwx--x---]
├── docs [drwxr-x---]
│   ├── doc1.txt [-rw-r-----]
│   ├── doc2.txt [-rw-r-----]
│   └── doc3.txt [-rw-r-----]
└── drop [drwx-wx---]
    ├── old1.txt [-rw-------]
    └── old2.txt [-rw-------]
```

### Tester les droits d'acces

Les utilisateurs du meme groupe peuvent traverser `alpha`, mais pas le lister :

```bash
$ cd ./alpha                         # autorise
$ ls ./alpha                         # refuse
$ touch ./alpha/fichier.txt          # refuse
```

Ils peuvent lire `docs` :

```bash
$ ls ./alpha/docs                    # autorise
$ cat ./alpha/docs/doc1.txt          # autorise
$ touch ./alpha/docs/doc4.txt        # refuse
$ echo test >> ./alpha/docs/doc1.txt # refuse
```

Ils peuvent deposer et effacer dans `drop`, sans lister ni lire :

```bash
$ touch ./alpha/drop/new.txt         # autorise
$ rm ./alpha/drop/new.txt            # autorise
$ ls ./alpha/drop                    # refuse
$ cat ./alpha/drop/old1.txt          # refuse
$ rm ./alpha/drop/old1.txt           # autorise
```

### Appliquer les droits d'acces

```bash
chmod u=rwX,g=X,o= ./alpha
chmod -R u=rwX,go= ./alpha/{docs,drop}

chmod g=rx ./alpha/docs
chmod g=r ./alpha/docs/*.txt

chmod g=wx ./alpha/drop
chmod g= ./alpha/drop/*.txt
```

---

## Exercice 2 - `beta`

### Creation des fichiers de test

```bash
mkdir -p ./beta/{edit,public,secret}
touch ./beta/edit/page{1..2}.txt
touch ./beta/public/name{1..3}.txt
touch ./beta/secret/key{1..2}.txt
```

### Droits attendus

```text
beta [drwx--x---]
├── edit [drwx--x---]
│   ├── page1.txt [-rw-rw----]
│   └── page2.txt [-rw-rw----]
├── public [drwxr-x---]
│   ├── name1.txt [-rw-------]
│   ├── name2.txt [-rw-------]
│   └── name3.txt [-rw-------]
└── secret [drwx--x---]
    ├── key1.txt [-rw-r-----]
    └── key2.txt [-rw-r-----]
```

### Tester les droits d'acces

Traverser `beta`, sans lister :

```bash
$ cd ./beta                          # autorise
$ ls ./beta                          # refuse
$ touch ./beta/test.txt              # refuse
```

Lire un fichier connu dans `secret`, sans lister :

```bash
$ cat ./beta/secret/key1.txt         # autorise
$ ls ./beta/secret                   # refuse
$ touch ./beta/secret/key3.txt       # refuse
```

Lister `public`, sans lire les fichiers :

```bash
$ ls ./beta/public                   # autorise
$ cat ./beta/public/name1.txt        # refuse
$ echo test >> ./beta/public/name1.txt # refuse
```

Lire et modifier les fichiers connus de `edit`, sans lister ni creer :

```bash
$ cat ./beta/edit/page1.txt          # autorise
$ echo test >> ./beta/edit/page1.txt # autorise
$ ls ./beta/edit                     # refuse
$ touch ./beta/edit/page3.txt        # refuse
$ rm ./beta/edit/page1.txt           # refuse
```

### Appliquer les droits d'acces

```bash
chmod u=rwX,g=X,o= ./beta
chmod -R u=rwX,go= ./beta/{edit,public,secret}

chmod g=x ./beta/secret
chmod g=r ./beta/secret/*.txt

chmod g=rx ./beta/public
chmod g= ./beta/public/*.txt

chmod g=x ./beta/edit
chmod g=rw ./beta/edit/*.txt
```

---

## Exercice 3 - `gamma`

### Creation des fichiers de test

```bash
mkdir -p ./gamma/projet/{build,logs,src}
touch ./gamma/projet/build/bin{1..2}.txt
touch ./gamma/projet/logs/app{1..2}.log
touch ./gamma/projet/src/file{1..3}.txt
```

### Droits attendus

```text
gamma [drwx--x---]
└── projet [drwx--x---]
    ├── build [drwx-wx---]
    │   ├── bin1.txt [-rw-------]
    │   └── bin2.txt [-rw-------]
    ├── logs [drwx--x---]
    │   ├── app1.log [-rw-rw----]
    │   └── app2.log [-rw-rw----]
    └── src [drwxr-x---]
        ├── file1.txt [-rw-r-----]
        ├── file2.txt [-rw-r-----]
        └── file3.txt [-rw-r-----]
```

### Tester les droits d'acces

Traverser les dossiers parents, sans les lister :

```bash
$ cd ./gamma/projet                  # autorise
$ ls ./gamma                         # refuse
$ ls ./gamma/projet                  # refuse
$ touch ./gamma/projet/test.txt      # refuse
```

Lire `src` :

```bash
$ ls ./gamma/projet/src              # autorise
$ cat ./gamma/projet/src/file1.txt   # autorise
$ touch ./gamma/projet/src/file4.txt # refuse
$ echo test >> ./gamma/projet/src/file1.txt # refuse
```

Deposer dans `build`, sans lister ni lire :

```bash
$ touch ./gamma/projet/build/new.txt # autorise
$ rm ./gamma/projet/build/new.txt    # autorise
$ ls ./gamma/projet/build            # refuse
$ cat ./gamma/projet/build/bin1.txt  # refuse
```

Modifier des logs connus, sans lister ni creer :

```bash
$ cat ./gamma/projet/logs/app1.log        # autorise
$ echo test >> ./gamma/projet/logs/app1.log # autorise
$ ls ./gamma/projet/logs                  # refuse
$ touch ./gamma/projet/logs/app3.log      # refuse
$ rm ./gamma/projet/logs/app1.log         # refuse
```

### Appliquer les droits d'acces

```bash
chmod -R u=rwX,go= ./gamma

chmod g=x ./gamma
chmod g=x ./gamma/projet

chmod g=rx ./gamma/projet/src
chmod g=r ./gamma/projet/src/*.txt

chmod g=wx ./gamma/projet/build
chmod g= ./gamma/projet/build/*.txt

chmod g=x ./gamma/projet/logs
chmod g=rw ./gamma/projet/logs/*.log
```

---

## Exercice 4 - `delta`

### Creation des fichiers de test

```bash
mkdir -p ./delta/{lecture-cachee,partage} ./delta/archives/2026
touch ./delta/lecture-cachee/secret{1..2}.txt
touch ./delta/archives/2026/archive{1..3}.txt
touch ./delta/partage/travail{1..2}.txt
```

### Droits attendus

```text
delta [drwx--x---]
├── archives [drwxr-x---]
│   └── 2026 [drwxr-x---]
│       ├── archive1.txt [-rw-r-----]
│       ├── archive2.txt [-rw-r-----]
│       └── archive3.txt [-rw-r-----]
├── lecture-cachee [drwx--x---]
│   ├── secret1.txt [-rw-r-----]
│   └── secret2.txt [-rw-r-----]
└── partage [drwxrwx---]
    ├── travail1.txt [-rw-rw----]
    └── travail2.txt [-rw-rw----]
```

### Tester les droits d'acces

Traverser `delta`, sans lister :

```bash
$ cd ./delta                         # autorise
$ ls ./delta                         # refuse
$ touch ./delta/test.txt             # refuse
```

Lire un fichier connu dans `lecture-cachee`, sans lister :

```bash
$ cat ./delta/lecture-cachee/secret1.txt # autorise
$ ls ./delta/lecture-cachee              # refuse
$ touch ./delta/lecture-cachee/s3.txt    # refuse
```

Lire toute l'arborescence `archives` :

```bash
$ ls ./delta/archives                # autorise
$ ls ./delta/archives/2026           # autorise
$ cat ./delta/archives/2026/archive1.txt # autorise
$ touch ./delta/archives/2026/a4.txt # refuse
$ echo test >> ./delta/archives/2026/archive1.txt # refuse
```

Tout faire dans `partage` :

```bash
$ ls ./delta/partage                 # autorise
$ cat ./delta/partage/travail1.txt   # autorise
$ echo test >> ./delta/partage/travail1.txt # autorise
$ touch ./delta/partage/new.txt      # autorise
$ rm ./delta/partage/new.txt         # autorise
```

### Appliquer les droits d'acces

```bash
chmod -R u=rwX,go= ./delta

chmod g=x ./delta

chmod g=x ./delta/lecture-cachee
chmod g=r ./delta/lecture-cachee/*.txt

chmod -R g=rX ./delta/archives

chmod -R g=rwX ./delta/partage
```

---

## Exercice 5 - `omega`

### Creation des fichiers de test

```bash
mkdir -p ./omega/{in,index,out,work}
touch ./omega/in/depot{1..2}.txt
touch ./omega/index/item{1..3}.txt
touch ./omega/out/result{1..3}.txt
touch ./omega/work/task{1..2}.txt
```

### Droits attendus

```text
omega [drwx--x---]
├── in [drwx-wx---]
│   ├── depot1.txt [-rw-------]
│   └── depot2.txt [-rw-------]
├── index [drwxr-x---]
│   ├── item1.txt [-rw-------]
│   ├── item2.txt [-rw-------]
│   └── item3.txt [-rw-------]
├── out [drwxr-x---]
│   ├── result1.txt [-rw-r-----]
│   ├── result2.txt [-rw-r-----]
│   └── result3.txt [-rw-r-----]
└── work [drwx--x---]
    ├── task1.txt [-rw-rw----]
    └── task2.txt [-rw-rw----]
```

### Tester les droits d'acces

Traverser `omega`, sans lister :

```bash
$ cd ./omega                         # autorise
$ ls ./omega                         # refuse
$ touch ./omega/test.txt             # refuse
```

Deposer dans `in`, sans lire ni lister :

```bash
$ touch ./omega/in/new.txt           # autorise
$ rm ./omega/in/new.txt              # autorise
$ ls ./omega/in                      # refuse
$ cat ./omega/in/depot1.txt          # refuse
```

Lire `out`, sans modifier :

```bash
$ ls ./omega/out                     # autorise
$ cat ./omega/out/result1.txt        # autorise
$ echo test >> ./omega/out/result1.txt # refuse
$ touch ./omega/out/result4.txt      # refuse
$ rm ./omega/out/result1.txt         # refuse
```

Modifier des fichiers connus dans `work`, sans lister ni creer :

```bash
$ cat ./omega/work/task1.txt         # autorise
$ echo test >> ./omega/work/task1.txt # autorise
$ ls ./omega/work                    # refuse
$ touch ./omega/work/task3.txt       # refuse
$ rm ./omega/work/task1.txt          # refuse
```

Lister les noms dans `index`, sans lire les fichiers :

```bash
$ ls ./omega/index                   # autorise
$ cat ./omega/index/item1.txt        # refuse
$ echo test >> ./omega/index/item1.txt # refuse
```

### Appliquer les droits d'acces

```bash
chmod -R u=rwX,go= ./omega

chmod g=x ./omega

chmod g=wx ./omega/in
chmod g= ./omega/in/*.txt

chmod g=rx ./omega/out
chmod g=r ./omega/out/*.txt

chmod g=x ./omega/work
chmod g=rw ./omega/work/*.txt

chmod g=rx ./omega/index
chmod g= ./omega/index/*.txt
```
