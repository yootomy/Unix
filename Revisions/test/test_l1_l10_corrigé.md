# Corrigé — Évaluation finale Shell Unix, Permissions et Scripts Bash

> **Ne pas distribuer avec le sujet**

---

## Partie 1 — QCM et Réponses courtes (20 pts)

### 1.1 (2 pts)

**Réponse :** `1`

**Explication :** La commande `ls /fichier_inexistant` renvoie une erreur car le fichier n'existe pas. Le descripteur d'erreur standard (`stderr`) est redirigé vers `/dev/null`, donc on ne voit pas le message d'erreur. Cependant, `ls` quitte avec le code de retour **1** (échec). `$?` capture ce code. Le `echo $?` affiche donc `1`.

---

### 1.2 (3 pts)

**Réponse :** Il n'y a **aucune différence sur le résultat final** des permissions appliquées.

**Mécanisme :**
- `chmod 755` utilise la **notation octale**. Le chiffre `7` remplace entièrement les droits du propriétaire, `5` remplace ceux du groupe, `5` remplace ceux des autres.
- `chmod u=rwx,go=rx` utilise la **notation littérale / symbolique**. `=` signifie "les droits deviennent EXACTEMENT ceux spécifiés". C'est encore un remplacement total, classe par classe.

**Différence conceptuelle :** la notation littérale permet aussi d'utiliser `+` (ajouter) et `-` (retirer) sans toucher aux autres droits, ce que la notation octale ne permet pas. Ex : `chmod g+w` ajoute l'écriture au groupe sans changer le reste.

---

### 1.3 (3 pts)

**Problème :** Le shell fait l'expansion des wildcards (**globbing**) **AVANT** d'exécuter `find`. Si un fichier se terminant par `.h` existe dans le répertoire courant, le shell remplace `*.h` par ce nom de fichier. `find` reçoit alors `-name fichier.h` à la place de `-name *.h`.

**Correction :**
```bash
find /usr/include -name "*.h"
# ou
find /usr/include -name '*.h'
```

Les guillemets protègent l'étoile du shell : c'est `find` qui interprète le motif, pas le shell.

---

### 1.4 (4 pts)

**Explication :** Un script s'exécute dans un **sous-shell** (processus fils). Les variables définies dans un sous-shell n'affectent pas le shell parent. `ma_var` meurt à la fin du script.

**Deux façons de résoudre :**

1. **Sourcer le script** — il s'exécute dans le shell courant :
   ```bash
   source ./monScript.sh
   # ou
   . ./monScript.sh
   ```

2. **Exporter la variable** dans le sous-shell, la capturer dans le parent :
   ```bash
   # Dans le script : ajouter
   export ma_var="test"
   # Puis dans le shell parent :
   eval "$(./monScript.sh)"
   # (ou mieux : le script fait un echo et on capture)
   ma_var=$(./monScript.sh)
   ```

*(Deux réponses correctes parmi : source, export + évaluation, écriture dans un fichier temporaire, etc.)*

---

### 1.5 (2 pts)

**Réponse :** Sur un **répertoire**, le bit SGID (`g+s`, apparaissant comme `s` à la place du `x` du groupe) fait que **tout nouveau fichier ou sous-répertoire créé à l'intérieur hérite du groupe propriétaire du répertoire**, et non pas du groupe primaire de l'utilisateur qui crée.

C'est très utilisé pour des répertoires partagés : tous les fichiers appartiennent automatiquement au même groupe, facilitant le travail collaboratif.

---

### 1.6 (3 pts)

| Opération | fichier source | rep parent source | rep parent dest |
|-----------|---------------|-------------------|-----------------|
| `cp` | `r--` (lecture) | `--x` (traverser) | `-wx` (écriture + traverser) |
| `mv` | `r--` (lecture) | `-wx` (supprimer = écrire + traverser) | `-wx` (écriture + traverser) |

**Explication :**
- `cp` lit le fichier source et l'écrit à un nouvel emplacement. Il ne touche pas au fichier source d'origine. Le rep source n'a besoin que du droit de traverser.
- `mv` déplace l'entrée d'annuaire du fichier d'un rep à l'autre. Cela nécessite de **supprimer l'ancienne entrée** dans le rep source (besoin de `w` sur le rep source) et d'en **créer une nouvelle** dans le rep dest (besoin de `w` sur le rep dest). `mv` entre deux systèmes de fichiers fait en réalité `cp + rm`.

---

### 1.7 (3 pts)

**Réponse :** Sans guillemets doubles, le shell effectue :
1. **Expansion des variables**
2. **Word splitting** (découpage sur les espaces, tabulations, retours à la ligne)
3. **Globbing** (expansion des `*`, `?`, `[...]`)

**Cas concret dangereux :**
```bash
fichier="mon fichier.txt"
rm $fichier       # Sans quotes : rm voit deux arguments : "mon" et "fichier.txt"
                  # → essaie de supprimer "mon" et "fichier.txt" (erreur !)
rm "$fichier"     # Avec quotes : rm voit un seul argument : "mon fichier.txt"
                  # → fonctionne correctement
```

Autre cas catastrophique : `rm $var` avec `var="*"` supprime tous les fichiers du répertoire courant.

---

## Partie 2 — Commandes à écrire (30 pts)

### 2.1 (2 pts)

```bash
wc -l /etc/passwd
```

---

### 2.2 (3 pts)

```bash
awk -F: '$3 >= 1000 && $3 <= 1999 {print $1}' /etc/passwd
```

Ou alternativement :
```bash
cut -d: -f1,3 /etc/passwd | awk -F: '$2 >= 1000 && $2 <= 1999 {print $1}'
```

---

### 2.3 (2 pts)

```bash
touch data_{01..15}.txt
```

*(L'expansion des accolades crée la séquence avec le zéro de padding.)*

---

### 2.4 (4 pts)

```bash
find /etc -name "*.conf" -exec cp {} ~/backup_conf/ \; 2>/dev/null
```

Ou avec une autre approche (exit code de find diffère) :
```bash
find /etc -name "*.conf" -print0 2>/dev/null | xargs -0 -I{} cp {} ~/backup_conf/
```

---

### 2.5 (4 pts)

```bash
last | awk '{print $1}' | sort -u | tail -n 3
```

*(Note : selon les lignes vides éventuelles en fin de sortie `last`, on peut ajouter un `grep -v '^$'` avant le `awk`.)*

---

### 2.6 (3 pts)

```bash
find /usr/share/doc/ | wc -l
```

Ou :
```bash
find /usr/share/doc/ -print | wc -l
```

---

### 2.7 (4 pts)

```bash
w | tr -s ' ' ':' | cut -d: -f1,6
```

Ou avec `awk` (mais l'énoncé impose `tr`) :
```bash
w | tr -s ' ' ':' | awk -F: 'NR>1 {print $1":"$6}'
```

**Variante plus précise** selon les colonnes de `w` :
```bash
w | tr -s ' ' | cut -d' ' -f1,6
```

*(Accepté si `tr -s ' ' ':'` est utilisé.)*

---

### 2.8 (4 pts)

```bash
cat <<EOF > ~/rapport.txt
Rapport généré par $LOGNAME le $(date)
EOF
```

Ou :
```bash
cat <<EOF > ~/rapport.txt
Rapport généré par $(whoami) le $(date)
EOF
```

*(Le Here Document permet la substitution de variables et de commandes. `> ~/rapport.txt` redirige la sortie de `cat` vers le fichier.)*

---

### 2.9 (4 pts)

**1. Définir l'alias :**
```bash
alias lt='ls -lt'
```

**2. Rendre permanent :**
```bash
echo "alias lt='ls -lt'" >> ~/.bashrc
```

*(Alternative : ajouter dans `~/.profile` ou `~/.bash_aliases` selon la distribution.)*

---

## Partie 3 — Analyse et Débogage (20 pts)

### 3.1 (6 pts)

Analyse ligne par ligne :

**`mkdir ~/test_exam`** → Réussit. Crée le répertoire avec les droits par défaut (`755` ou selon `umask`).

**`chmod 600 ~/test_exam`** → Réussit. Applique `drw-------`. **Problème critique :** le droit `x` (exécution/traversée) est retiré au propriétaire.

**`touch ~/test_exam/fic1.txt`** → **ÉCHOUE** (`Permission denied`).
- Pour créer un fichier dans un répertoire, il faut **`w`** (écriture dans le répertoire) ET **`x`** (traverser le répertoire pour accéder aux inodes internes).
- Ici on a `rw-` mais pas `x`. On ne peut pas "entrer" dans le répertoire.

**`echo "hello" > ~/test_exam/fic1.txt`** → **ÉCHOUE** (`Permission denied`). Même raison : pas de `x` sur le répertoire.

**`ls -l ~/test_exam/fic1.txt`** → **ÉCHOUE ou affiche des `?`**.
- Sans le droit `x` sur `~/test_exam`, on ne peut pas résoudre le chemin `~/test_exam/fic1.txt`.
- `ls` affichera : `ls: cannot access '/home/user/test_exam/fic1.txt': Permission denied`
- Si on fait `ls -l ~/test_exam/`, on verra : `ls: cannot open directory '/home/user/test_exam': Permission denied`

**Conclusion :** Sur un répertoire, `r` seul permet de voir la liste des noms (mais pas leurs attributs), `w` seul ne permet presque rien, et **`x` est INDISPENSABLE** pour presque toute opération (créer, supprimer, lire des fichiers à l'intérieur).

---

### 3.2 (6 pts)

**a) Erreurs dans `compte.sh` :**

```bash
#!/bin/bash
for i in $(seq 1 10)
    echo $i
done
```

| Erreur | Correction |
|--------|------------|
| Il manque le mot-clé **`do`** après le `for` | `for i in $(seq 1 10); do` |
| `$i` non protégé (word splitting potentiel) | `"$i"` |
| `seq` fonctionne mais n'est pas le plus idiomatique | `{1..10} est préférable si l'on veut, mais `seq` est correct |

**Script corrigé :**
```bash
#!/bin/bash
for i in $(seq 1 10); do
    echo "$i"
done
```

**b) Avec `{1..10}` :**
```bash
#!/bin/bash
for i in {1..10}; do
    echo "$i"
done
```

---

### 3.3 (4 pts)

**Problème :** `chmod ugo= fichier.txt` retire **tous les droits** à tout le monde, y compris la lecture (`r`). `cp` a besoin de lire le fichier source pour le copier. Comme personne n'a le droit de lecture, `cp` échoue.

**Deux méthodes pour copier quand même (en tant que propriétaire) :**

1. **Se redonner temporairement le droit de lecture** :
   ```bash
   chmod u+r fichier.txt
   cp fichier.txt copie.txt
   chmod ugo= fichier.txt   # (optionnellement remettre comme avant)
   ```

2. **Utiliser `sudo` / `su` si configuré** :
   ```bash
   sudo cp fichier.txt copie.txt
   ```
   *(root ignore les permissions des fichiers sur les filesystems standards.)*

3. *(Bonus - méthode académique)* **Utiliser `dd`** : si on a accès au device bloc sous-jacent (root uniquement), on peut lire directement les blocs. Mais ce n'est pas une solution raisonnable en pratique.

*(Les deux premières méthodes suffisent pour un étudiant.)*

---

### 3.4 (4 pts)

**Problème :** Dans `grep ".txt"`, le point `.` est un **métacaractère** en expression régulière. Il correspond à **n'importe quel caractère unique**. Donc `.txt` correspond à ` atxt`, `btxt`, ` txt`, etc. — pas seulement aux fichiers se terminant par `.txt`.

**Correction :**

1. Échapper le point pour le traiter littéralement :
   ```bash
   ls -la ~ | grep '\.txt$'
   ```

2. Ou utiliser `grep -F` (mode fixed string, pas de regex) :
   ```bash
   ls -la ~ | grep -F ".txt"
   ```

3. Ou utiliser une autre commande comme `find` :
   ```bash
   ls -la ~ | awk '/\.txt$/'
   ```

---

## Partie 4 — Scripts Bash à écrire (30 pts)

### 4.1 `creer_projet.sh` (12 pts)

**Script attendu :**

```bash
#!/bin/bash

# Vérification : un argument est requis
if [ -z "$1" ]; then
    echo "Erreur : nom du projet requis" >&2
    exit 1
fi

# Définition des variables
projet="$1"
repertoire="$HOME/projets/$projet"

# Création de l'arborescence
mkdir -p "$repertoire"/{src,doc,bin}

# Création du README.md avec un Here Document
cat <<EOF > "$repertoire/README.md"
# Projet : $projet
Auteur : $LOGNAME
Date : $(date)
EOF

# Message de confirmation
echo "Projet '$projet' cree dans $repertoire"
```

**Barème indicatif :**
- Vérification de l'argument et sortie sur stderr (2 pts)
- Création correcte de l'arborescence avec `mkdir -p` (2 pts)
- Utilisation du Here Document (3 pts)
- Content correct du README (2 pts)
- Quotes doubles sur toutes les variables (2 pts)
- `exit 1` en cas d'erreur (1 pt)

---

### 4.2 `gestion_users.sh` (18 pts)

**Script attendu :**

```bash
#!/bin/bash

# Vérification root
if [ "$UID" -ne 0 ]; then
    echo "Ce script doit etre execute en root" >&2
    exit 1
fi

# Vérification des arguments
if [ "$#" -ne 2 ]; then
    echo "Usage : ./gestion_users.sh {create|delete} N" >&2
    exit 1
fi

action="$1"
n="$2"

# Vérification que N est un nombre entier positif
if ! [[ "$n" =~ ^[0-9]+$ ]]; then
    echo "Erreur : N doit etre un nombre entier positif" >&2
    exit 1
fi

# Création du groupe si nécessaire (action create uniquement)
if [ "$action" = "create" ]; then
    if ! getent group exam_group > /dev/null; then
        groupadd exam_group
        echo "Groupe exam_group cree"
    fi
fi

# Boucle while obligatoire
i=1
while [ "$i" -le "$n" ]; do
    user="exam_user$i"

    if [ "$action" = "create" ]; then
        useradd -m -g exam_group "$user"
        echo "Cree : $user"
    elif [ "$action" = "delete" ]; then
        userdel -r "$user"
        echo "Supprime : $user"
    else
        echo "Usage : ./gestion_users.sh {create|delete} N" >&2
        exit 1
    fi

    i=$((i + 1))
done
```

**Barème indicatif :**
- Vérification root avec `UID` (2 pts)
- Vérification du nombre d'arguments (2 pts)
- Vérification que l'action est `create` ou `delete` (2 pts)
- Création automatique du groupe `exam_group` (2 pts)
- Boucle `while` obligatoire correcte (3 pts)
- `useradd -m -g exam_group` pour create (2 pts)
- `userdel -r` pour delete (2 pts)
- Affichage ligne par ligne `Cree :` / `Supprime :` (2 pts)
- Quotes doubles et style shellcheck-compatible (1 pt)

---

## Notes pédagogiques

### Erreurs fréquentes à surveiller chez les étudiants :

1. **Oublier les quotes** dans les scripts — sanctionné immédiatement.
2. **Confusion `useradd` / `adduser`** : `useradd` est la commande bas niveau, option `-m` pour créer le home est obligatoire.
3. **Groupe existant** : ne pas vérifier si `exam_group` existe avant de le créer = erreur.
4. **Boucle `while` correcte** : `[ "$i" -le "$n" ]` avec espaces obligatoires.
5. **Here Document** : oublier que le mot limite doit être seul sur sa ligne à la fin.
6. **Permissions répertoire** : penser que `r` suffit à accéder aux fichiers = erreur classique. `x` est indispensable.
7. **Globbing dans `find`** : c'est l'erreur la plus sournoise en shell.

---

**FIN DU CORRIGE**
