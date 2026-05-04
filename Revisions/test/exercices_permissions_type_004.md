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
alpha
├── docs
│   ├── doc1.txt
│   ├── doc2.txt
│   └── doc3.txt
└── drop
    ├── old1.txt
    └── old2.txt
```

Questions :

1. Donner l'arborescence avec les droits attendus.
2. Donner les commandes `chmod`.
3. Donner des commandes de test pour verifier les acces autorises et refuses.

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
beta
├── edit
│   ├── page1.txt
│   └── page2.txt
├── public
│   ├── name1.txt
│   ├── name2.txt
│   └── name3.txt
└── secret
    ├── key1.txt
    └── key2.txt
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
gamma
└── projet
    ├── build
    │   ├── bin1.txt
    │   └── bin2.txt
    ├── logs
    │   ├── app1.log
    │   └── app2.log
    └── src
        ├── file1.txt
        ├── file2.txt
        └── file3.txt
```

Questions :

1. Donner l'arborescence avec les droits attendus.
2. Donner les commandes `chmod`.
3. Donner des commandes de test pour verifier les acces autorises et refuses.

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

Arborescence de depart :

```text
delta
├── archives
│   └── 2026
│       ├── archive1.txt
│       ├── archive2.txt
│       └── archive3.txt
├── lecture-cachee
│   ├── secret1.txt
│   └── secret2.txt
└── partage
    ├── travail1.txt
    └── travail2.txt
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
omega
├── in
│   ├── depot1.txt
│   └── depot2.txt
├── index
│   ├── item1.txt
│   ├── item2.txt
│   └── item3.txt
├── out
│   ├── result1.txt
│   ├── result2.txt
│   └── result3.txt
└── work
    ├── task1.txt
    └── task2.txt
```

Questions :

1. Donner l'arborescence avec les droits attendus.
2. Donner les commandes `chmod`.
3. Donner des commandes de test pour verifier les acces autorises et refuses.
