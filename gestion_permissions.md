# Gestion des permissions — Notes de cours (INT_SYS1_NIX)

---

## Commandes utiles

| Commande | Description |
|----------|-------------|
| `id`     | Afficher les identifiants d'utilisateur et de groupe |
| `chmod`  | Modifier les bits de permission d'un fichier |
| `umask`  | Afficher ou définir le masque de création de fichier |
| `su`     | Changer d'identité utilisateur |
| `sudo`   | Exécuter une commande en tant qu'un autre utilisateur |
| `chown`  | Modifier le propriétaire et le groupe d'un fichier |
| `chgrp`  | Changer le groupe propriétaire d'un fichier |
| `passwd` | Modifier le mot de passe |

---

## Identifier l'utilisateur courant

```bash
$ id
uid=10250(huguenindo) gid=10005(domain users) groupes=10005(domain users), ...
```

- `uid` : identifiant de l'utilisateur
- `gid` : identifiant du groupe principal

---

## Afficher les droits

```bash
$ ls -l foo.txt
-rw------- 1 huguenindo domain users 0 2010-10-25 16:16 foo.txt
```

### Type de fichier (1er caractère)

| Symbole | Type |
|---------|------|
| `-`     | Fichier ordinaire |
| `d`     | Dossier / répertoire |
| `l`     | Lien symbolique |
| `b`     | Périphérique bloc (disque) |
| `c`     | Périphérique caractère (clavier) |

---

## Structure des permissions

```
-rwxrwxr-x  1  dom  dom  1306  fév 16 2017  backup
```

Les 9 caractères après le type représentent **3 classes de 3 droits** :

| Classe | Symbole | Description |
|--------|---------|-------------|
| Propriétaire | `u` (user) | Le possesseur du fichier |
| Groupe | `g` (group) | Le groupe propriétaire |
| Autres | `o` (other) | Tous les autres utilisateurs |
| Tous | `a` (all) | u + g + o |

| Droit | Symbole | Sur fichier | Sur dossier |
|-------|---------|-------------|-------------|
| Lecture | `r` | `cat`, lire | `ls`, lister |
| Écriture | `w` | `echo`, modifier | `touch`, `rm`, `mkdir`, `ln` |
| Exécution | `x` | Lancer le programme | `cd`, traverser |
| Aucun droit | `-` | — | — |

---

## Permissions spéciales

| Bit | Symbole | Effet sur fichier | Effet sur dossier |
|-----|---------|-------------------|-------------------|
| Sticky bit | `t` | Garder en mémoire après exécution | Seul le proprio peut supprimer ses fichiers |
| SUID / SGID | `s` | Exécuter avec les droits du propriétaire/groupe | Nouveaux fichiers héritent du groupe |

---

## Permission en octal

| Octal | Binaire | Mode |
|-------|---------|------|
| 0 | 000 | `---` |
| 1 | 001 | `--x` |
| 2 | 010 | `-w-` |
| 3 | 011 | `-wx` |
| 4 | 100 | `r--` |
| 5 | 101 | `r-x` |
| 6 | 110 | `rw-` |
| 7 | 111 | `rwx` |

> Exemple : `chmod 0664 foo.txt` → `rw-rw-r--`

---

## Changer les permissions — forme littérale

```bash
chmod u+x,g-w,o= foo.txt     # ajoute x au proprio, retire w au groupe, vide les autres
chmod a=rw foo.txt            # tout le monde a rw, rien d'autre
```

| Symbole cible | Description |
|---------------|-------------|
| `u` | Propriétaire |
| `g` | Groupe |
| `o` | Autres |
| `a` | Tous (u+g+o) |

| Opérateur | Description |
|-----------|-------------|
| `=` | La permission devient exactement celle spécifiée |
| `+` | Le droit est ajouté à la permission actuelle |
| `-` | Le droit est retiré de la permission actuelle |

---

## Changer les permissions — forme octale

```bash
chmod 0664 foo.txt
# résultat : -rw-rw-r--
```

---

## Droits minimums requis

### Copier un fichier `cp ./tmp/foo.txt ./tmp2`

```
tmp/       --x    (traverser)
foo.txt    r--    (lire)
tmp2/      -wx    (écrire + traverser)
```

### Déplacer un fichier `mv ./tmp/foo.txt ./tmp2`

```
tmp/       -wx    (supprimer = écrire + traverser)
foo.txt    r--    (lire)
tmp2/      -wx    (écrire + traverser)
```

---

## Permission par défaut — `umask`

Le `umask` est un masque qui **retire** des droits aux droits de base.

| | Fichier | Dossier |
|---|---------|---------|
| Droits de base | `rw-rw-rw-` (666) | `rwxrwxrwx` (777) |

### Exemples

| `umask` | Fichier créé | Dossier créé |
|---------|-------------|-------------|
| `0000`  | `rw-rw-rw-` | `rwxrwxrwx` |
| `0077`  | `rw-------` | `rwx------` |
| `0022`  | `rw-r--r--` | `rwxr-xr-x` |

> **Calcul :** droits de base **ET NON** masque (opération bit à bit)

---

## Changement d'identité

### `su` — devenir un autre utilisateur

```bash
$ su ubuntu
Password: [mot de passe de ubuntu]
ubuntu@lozan:~$ whoami
ubuntu
ubuntu@lozan:~$ exit
```

### `sudo` — exécuter une commande en tant qu'un autre

```bash
$ sudo -u huguenindo whoami
Password: [mot de passe de l'utilisateur courant]
huguenindo
```

> L'utilisateur doit avoir les droits `sudo` configurés.

---

## Références

- *The Linux Command Line* — chapitre 10 : Permissions
- Permissions UNIX — Wikipédia
