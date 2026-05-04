# Exercices - Permissions type activite 004

> Objectif : s'entrainer aux exercices de droits d'acces comme dans l'activite 004.
>
> Pour chaque exercice :
> 1. identifier les droits a appliquer sur les dossiers et les fichiers ;
> 2. ecrire les commandes `chmod` ;
> 3. ecrire quelques commandes de test qui prouvent les acces autorises et refuses.

---

## Exercice 1 - `alpha`

Mettre les droits d'acces sur les dossiers et fichiers de l'arborescence ci-dessous.

1. Les fichiers ne sont pas executables.
2. Le proprietaire possede tous les droits sur toute l'arborescence.
3. Les utilisateurs du meme groupe que le proprietaire peuvent uniquement :
   1. traverser le dossier `./alpha`, sans lister son contenu et sans y creer de fichier ;
   2. lister et lire les fichiers du dossier `./alpha/docs`, sans les modifier et sans ajouter de fichier ;
   3. ajouter et effacer des fichiers dans `./alpha/drop`, sans lister le dossier et sans lire les fichiers deja presents.
4. Les autres utilisateurs n'ont aucun droit dans l'arborescence.

Arborescence de depart :

```text
alpha drwx --x ---
├── docs drwx r-x ---
│   ├── doc1.txt rw- r-- ---
│   ├── doc2.txt rw- r-- ---
│   └── doc3.txt rw- r-- ---
└── drop drwx -wx ---
    ├── old1.txt rw- --- ---
    └── old2.txt rw- --- ---
```

Questions :

1. Donner l'arborescence avec les droits attendus.
2. Donner les commandes `chmod`.
3. Donner des commandes de test pour verifier les acces autorises et refuses.

***les commandes chmod*** :
```
chmod 710 ./alpha
chmod 750 ./alpha/docs
chmod 640 ./alpha/docs/doc1.txt
chmod 640 ./alpha/docs/doc2.txt
chmod 640 ./alpha/docs/doc3.txt
chmod 730 ./alpha/drop
chmod 600 ./alpha/drop/old1.txt
chmod 600 ./alpha/drop/old2.txt
```



---

## Exercice 2 - `beta`

Mettre les droits d'acces sur les dossiers et fichiers de l'arborescence ci-dessous.

1. Les fichiers ne sont pas executables.
2. Le proprietaire possede tous les droits sur toute l'arborescence.
3. Les utilisateurs du meme groupe que le proprietaire peuvent uniquement :
   1. traverser `./beta`, sans le lister et sans y creer de fichier ;
   2. lire les fichiers connus de `./beta/secret`, sans pouvoir lister ce dossier ;
   3. lister `./beta/public`, sans pouvoir lire le contenu des fichiers ;
   4. lire et modifier les fichiers connus de `./beta/edit`, sans pouvoir lister, creer ou supprimer des fichiers dans ce dossier.
4. Les autres utilisateurs n'ont aucun droit dans l'arborescence.

Arborescence de depart :

```text
beta drwx--x---
├── edit drwx--x---
│   ├── page1.txt rw-rw----
│   └── page2.txt rw-rw----
├── public drwxr-x---
│   ├── name1.txt rw-------
│   ├── name2.txt rw-------
│   └── name3.txt rw-------
└── secret drwx--x---
    ├── key1.txt rw-r----
    └── key2.txt rw-r----
```

Questions :

1. Donner l'arborescence avec les droits attendus.
2. Donner les commandes `chmod`.
3. Donner des commandes de test pour verifier les acces autorises et refuses.

---

## Exercice 3 - `gamma`

Mettre les droits d'acces sur les dossiers et fichiers de l'arborescence ci-dessous.

1. Les fichiers ne sont pas executables.
2. Le proprietaire possede tous les droits sur toute l'arborescence.
3. Les utilisateurs du meme groupe que le proprietaire peuvent uniquement :
   1. traverser `./gamma` et `./gamma/projet`, sans les lister et sans y creer de fichier ;
   2. lister et lire les fichiers de `./gamma/projet/src`, sans les modifier et sans ajouter de fichier ;
   3. ajouter et effacer des fichiers dans `./gamma/projet/build`, sans lister le dossier et sans lire les fichiers existants ;
   4. lire et modifier les fichiers connus de `./gamma/projet/logs`, sans lister le dossier et sans creer ou supprimer de fichier.
4. Les autres utilisateurs n'ont aucun droit dans l'arborescence.

Arborescence de depart :

```text
gamma drwx--x---
└── projet drwx--x---
    ├── build drwx-wx---
    │   ├── bin1.txt rw-------
    │   └── bin2.txt rw-------
    ├── logs drwx--x---
    │   ├── app1.log rw-rw----
    │   └── app2.log rw-rw----
    └── src drwxr-x---
        ├── file1.txt rw-r-----
        ├── file2.txt rw-r-----
        └── file3.txt rw-r-----
```

Questions :

1. Donner l'arborescence avec les droits attendus.
2. Donner les commandes `chmod`.
3. Donner des commandes de test pour verifier les acces autorises et refuses.


```
chmod 710 ./gamma
chmod 710 ./gamma/projet
chmod 730 ./gamma/projet/build
chmod 600 ./gamma/projet/build/bin1.txt
chmod 600 ./gamma/projet/build/bin2.txt
chmod 710 ./gamma/projet/logs
chmod 660 ./gamma/projet/logs/app1.log
chmod 660 ./gamma/projet/logs/app2.log
chmod 750 ./gamma/projet/src
chmod 640 ./gamma/projet/src/file1.txt
chmod 640 ./gamma/projet/src/file2.txt
chmod 640 ./gamma/projet/src/file3.txt

```


---

## Exercice 4 - `delta`

Mettre les droits d'acces sur les dossiers et fichiers de l'arborescence ci-dessous.

1. Les fichiers ne sont pas executables.
2. Le proprietaire possede tous les droits sur toute l'arborescence.
3. Les utilisateurs du meme groupe que le proprietaire peuvent uniquement :
   1. traverser `./delta`, sans le lister et sans y creer de fichier ;
   2. lire les fichiers connus de `./delta/lecture-cachee`, sans lister ce dossier ;
   3. lister et lire toute l'arborescence `./delta/archives`, sans modifier ni ajouter de fichier ;
   4. lister, lire, modifier, ajouter et effacer des fichiers dans `./delta/partage`.
4. Les autres utilisateurs n'ont aucun droit dans l'arborescence.

Arborescence de départ :

```text
delta drwx--x---
├── archives drwxr-x---
│   └── 2026 drwxr-x---
│       ├── archive1.txt rw-r-----
│       ├── archive2.txt rw-r-----
│       └── archive3.txt rw-r-----
├── lecture-cachee drwx--x---
│   ├── secret1.txt rw-r-----
│   └── secret2.txt rw-r-----
└── partage drwxrwx---
    ├── travail1.txt rw-rw----
    └── travail2.txt rw-rw----
```

Questions :

1. Donner l'arborescence avec les droits attendus.
2. Donner les commandes `chmod`.
3. Donner des commandes de test pour verifier les acces autorises et refuses.

---

## Exercice 5 - `omega`

Mettre les droits d'acces sur les dossiers et fichiers de l'arborescence ci-dessous.

1. Les fichiers ne sont pas executables.
2. Le proprietaire possede tous les droits sur toute l'arborescence.
3. Les utilisateurs du meme groupe que le proprietaire peuvent uniquement :
   1. traverser `./omega`, sans le lister et sans y creer de fichier ;
   2. deposer et supprimer des fichiers dans `./omega/in`, sans lister le dossier et sans lire les fichiers existants ;
   3. lister et lire les fichiers de `./omega/out`, sans modifier, ajouter ou supprimer ;
   4. lire et modifier les fichiers connus de `./omega/work`, sans lister, creer ou supprimer ;
   5. lister les noms de `./omega/index`, sans lire le contenu des fichiers.
4. Les autres utilisateurs n'ont aucun droit dans l'arborescence.

Arborescence de depart :

```text
omega drwx--x---
├── in drwx-wx---
│   ├── depot1.txt rw-------
│   └── depot2.txt rw-------
├── index drwxr-x---
│   ├── item1.txt rw-------
│   ├── item2.txt rw-------
│   └── item3.txt rw-------
├── out drwxr-x---
│   ├── result1.txt rw-r-----
│   ├── result2.txt rw-r-----
│   └── result3.txt rw-r-----
└── work drwx--x---
    ├── task1.txt rw-rw----
    └── task2.txt rw-rw----
```

Questions :

1. Donner l'arborescence avec les droits attendus.
2. Donner les commandes `chmod`.
3. Donner des commandes de test pour verifier les acces autorises et refuses.
