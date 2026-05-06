# Variantes de scripts de création d'utilisateurs

> Inspirées de l'activité **0008 §7** (`addusers.sh`/`delusers.sh` officiels du cours).
> Pour chaque variante, le **script de suppression** symétrique est fourni à droite.
>
> Avant la première utilisation sur une machine où l'allocation automatique des UID
> subordonnés pose problème (`Impossible d'obtenir une gamme d'UID uniques subordonnés`),
> faire **une fois** :
>
> ```bash
> sudo sed -i 's/^SUB_UID_COUNT.*/SUB_UID_COUNT 0/' /etc/login.defs
> sudo sed -i 's/^SUB_GID_COUNT.*/SUB_GID_COUNT 0/' /etc/login.defs
> ```

---

## Variante 1 — `user001` à `user100` (numérique simple, 3 chiffres)

```bash
#!/bin/bash
#################################
# Création de user001 à user100
#################################
USER_PREFIX="user"

for i in {001..100}; do
    USER="${USER_PREFIX}${i}"
    useradd -m "$USER" -s /bin/bash
done
```

```bash
#!/bin/bash
# Suppression
USER_PREFIX="user"
for i in {001..100}; do
    userdel -r -f "${USER_PREFIX}${i}"
done
```

> **Note :** `{001..100}` produit `001 002 … 100` avec **padding** automatique (zéros).

---

## Variante 2 — `user-AA` à `user-ZZ` (676 utilisateurs, format examen)

```bash
#!/bin/bash
#################################
# Création de user-AA à user-ZZ (676 utilisateurs)
# membres du groupe int-s-pma
#################################
GROUP="int-s-pma"

for i in {A..Z}; do
    for j in {A..Z}; do
        USER="user-$i$j"
        useradd -m "$USER" -G "$GROUP"
    done
done
```

```bash
#!/bin/bash
# Suppression
for i in {A..Z}; do
    for j in {A..Z}; do
        userdel -r -f "user-$i$j"
    done
done
```

---

## Variante 3 — `user-A` à `user-Z` (lettres simples, 26 utilisateurs)

```bash
#!/bin/bash
#################################
# Création de user-A à user-Z
#################################
for i in {A..Z}; do
    USER="user-$i"
    useradd -m "$USER" -s /bin/bash
done
```

```bash
#!/bin/bash
# Suppression
for i in {A..Z}; do
    userdel -r -f "user-$i"
done
```

---

## Variante 4 — `user1` à `user1000` (sans padding, numérique étendu)

```bash
#!/bin/bash
#################################
# Création de user1 à user1000 (1000 utilisateurs)
#################################
USER_PREFIX="user"

for i in {1..1000}; do
    USER="${USER_PREFIX}${i}"
    useradd -m "$USER" -s /bin/bash
done
```

```bash
#!/bin/bash
USER_PREFIX="user"
for i in {1..1000}; do
    userdel -r -f "${USER_PREFIX}${i}"
done
```

---

## Variante 5 — `eleve01` à `eleve30` avec mot de passe identique au login

```bash
#!/bin/bash
#################################
# Création des comptes élèves d'une classe
# mot de passe = login (à changer au premier login)
#################################
GROUP="eleves"

# Créer le groupe s'il n'existe pas
groupadd -f "$GROUP"

for i in {01..30}; do
    USER="eleve${i}"
    useradd -m "$USER" -s /bin/bash -G "$GROUP"
    echo "${USER}:${USER}" | chpasswd
    # forcer le changement de mdp à la première connexion
    chage -d 0 "$USER"
done
```

```bash
#!/bin/bash
for i in {01..30}; do
    userdel -r -f "eleve${i}"
done
groupdel eleves
```

> **`chpasswd`** lit des paires `user:mdp` sur stdin — pratique pour scripter
> les mots de passe sans `passwd` interactif.

---

## Variante 6 — Création depuis une **liste de noms** dans un fichier

Fichier `users.txt` (un nom par ligne) :

```
jeannette
lucien
jack
joe
pier
```

```bash
#!/bin/bash
#################################
# Création des utilisateurs listés dans users.txt
#################################
LISTE="./users.txt"

while IFS= read -r USER; do
    [ -z "$USER" ] && continue                # ignorer les lignes vides
    useradd -m "$USER" -s /bin/bash
    echo "${USER}:${USER}" | chpasswd
done < "$LISTE"
```

```bash
#!/bin/bash
LISTE="./users.txt"
while IFS= read -r USER; do
    [ -z "$USER" ] && continue
    userdel -r -f "$USER"
done < "$LISTE"
```

> **`while IFS= read -r`** lit ligne par ligne en préservant les espaces et
> sans interpréter les `\`.

---

## Variante 7 — `vmadmin01` à `vmadmin10` avec **groupe primaire** dédié

```bash
#!/bin/bash
#################################
# Comptes administrateurs de VM
# - groupe primaire = vmadmins
# - groupes secondaires = sudo, libvirt
# - shell = /bin/bash
#################################
PRIMARY="vmadmins"
SECONDARY="sudo,libvirt"

groupadd -f "$PRIMARY"

for i in {01..10}; do
    USER="vmadmin${i}"
    useradd -m "$USER" -g "$PRIMARY" -G "$SECONDARY" -s /bin/bash
    echo "${USER}:${USER}" | chpasswd
done
```

```bash
#!/bin/bash
for i in {01..10}; do
    userdel -r -f "vmadmin${i}"
done
groupdel vmadmins
```

> **`-g`** = groupe primaire (un seul) ; **`-G`** = groupes secondaires (liste
> séparée par des virgules). Cours 0008 §4.

---

## Variante 8 — Avec **UID/GID explicites** (séries contigües)

```bash
#!/bin/bash
#################################
# Création de stagiaire01..20 avec UID 5001..5020
#################################
GROUP="stagiaires"
GID_BASE=5000
UID_BASE=5000

groupadd -g "$GID_BASE" "$GROUP" 2>/dev/null

for i in {1..20}; do
    USER=$(printf "stagiaire%02d" "$i")
    UID_NEW=$((UID_BASE + i))
    useradd -m -u "$UID_NEW" -g "$GROUP" -s /bin/bash "$USER"
    echo "${USER}:${USER}" | chpasswd
done
```

```bash
#!/bin/bash
for i in {1..20}; do
    USER=$(printf "stagiaire%02d" "$i")
    userdel -r -f "$USER"
done
groupdel stagiaires
```

> **`printf "%02d"`** = padding zéro sur 2 chiffres. Utile quand la plage n'est
> pas exprimable avec l'expansion brace `{01..20}`.

---

## Variante 9 — `dev-{frontend,backend,devops}-{01..05}` (combinaisons multiples)

```bash
#!/bin/bash
#################################
# 3 équipes × 5 membres = 15 comptes
#################################
for ROLE in frontend backend devops; do
    groupadd -f "$ROLE"
    for i in {01..05}; do
        USER="dev-${ROLE}-${i}"
        useradd -m "$USER" -g "$ROLE" -s /bin/bash
        echo "${USER}:${USER}" | chpasswd
    done
done
```

```bash
#!/bin/bash
for ROLE in frontend backend devops; do
    for i in {01..05}; do
        userdel -r -f "dev-${ROLE}-${i}"
    done
    groupdel "$ROLE"
done
```

---

## Variante 10 — Format **historique du cours** (avec `mkpasswd`)

> Reprise quasi à l'identique du script officiel `addusers.sh` du cours
> (act. 0008 §7), adapté à 100 utilisateurs.

```bash
#!/bin/bash
#################################
# Création de 100 utilisateurs
# Mot de passe haché généré par mkpasswd
# dominique.huguenin AT rpn.ch
#################################
USER_PREFIX="user"

for USER in $(echo ${USER_PREFIX}{000..099}); do
    PASS=$(mkpasswd "$USER")
    useradd -m "$USER" -p "$PASS" -s /bin/bash
done
```

```bash
#!/bin/bash
USER_PREFIX="user"
for USER in $(echo ${USER_PREFIX}{000..099}); do
    userdel -r -f "$USER"
done
```

> **`mkpasswd <chaîne>`** retourne un hash chiffré utilisable directement avec
> `useradd -p`. Sur Debian, paquet `whois` (`sudo apt install whois`).
> ⚠️ `useradd -p <hash>` attend un **hash**, pas un mot de passe en clair.

---

## Mémo — comment sont passés les utilisateurs à `useradd`

| Option       | Effet                                                          |
| ------------ | -------------------------------------------------------------- |
| `-m`         | Créer le répertoire personnel `/home/<user>`                   |
| `-d <chemin>`| Spécifier un home alternatif                                   |
| `-s <shell>` | Définir le shell de login (`/bin/bash`, `/bin/sh`, `/usr/sbin/nologin`) |
| `-u <uid>`   | UID explicite                                                  |
| `-g <gid>`   | Groupe **primaire** (un seul)                                  |
| `-G g1,g2`   | Groupes **secondaires** (liste séparée par `,`)                |
| `-p <hash>`  | Mot de passe sous forme **hashée** (cf. `mkpasswd`)            |
| `-c "texte"` | Champ "GECOS" (nom complet, etc.)                              |
| `-e <date>`  | Date d'expiration du compte (`YYYY-MM-DD`)                     |

| Option       | `userdel`                                                      |
| ------------ | -------------------------------------------------------------- |
| `-r`         | Supprime aussi le home et la boîte mail                        |
| `-f`         | Force la suppression même si l'utilisateur est connecté        |

---

## Modèle générique réutilisable

```bash
#!/bin/bash
#################################
# Modèle générique — adapter PREFIX, MIN, MAX, GROUP
#################################
PREFIX="user"
MIN=1
MAX=100
GROUP="eleves"

groupadd -f "$GROUP"

for i in $(seq -f "%03g" "$MIN" "$MAX"); do
    USER="${PREFIX}${i}"
    useradd -m "$USER" -G "$GROUP" -s /bin/bash
    echo "${USER}:${USER}" | chpasswd
done
```

> **`seq -f "%03g"`** = génère une suite avec padding zéro sur 3 chiffres.
> Plus flexible que l'expansion brace si les bornes sont des **variables**
> (l'expansion `{$MIN..$MAX}` ne fonctionne pas en bash standard).
