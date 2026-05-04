# Évaluation finale — Shell Unix, Permissions et Scripts Bash

> **Module :** Systèmes d'exploitation de type Unix | **Leçons :** L1 à L10
> **Durée :** 120 min | **Barème :** 100 points | **Documents :** aucun
> **HORS SUJET :** KVM, LXC, Incus, LVM, netplan, configuration réseau avancée

---

## Partie 1 — QCM et Réponses courtes (20 pts)

Rédigez vos réponses de manière concise. Une phrase suffit si la réponse est complète.

---

**1.1** (2 pts) On exécute la commande suivante :
```bash
ls /fichier_inexistant 2>/dev/null ; echo $?
```
Quelle valeur s'affiche ? Expliquez brièvement.

$? = variable qui contient le code de sortie de la dernière commande

**Les codes de sortie courants en Unix/Linux sont :** 
0= succès 
1= erreur générale 
2= fichier ou répertoire non trouvé (ou utilisation incorrecte de la commande) 
127= commande non trouvée

---

**1.2** (3 pts) Quelle est la différence entre :
```bash
chmod 755 rep/
```
et :
```bash
chmod u=rwx,go=rx rep/
```
Y a-t-il une différence sur le résultat final ? Expliquez en quoi le mécanisme diffère cependant.

Non y'a aucune différence, la seule différence c'est le format octale ou littérale

---

**1.3** (3 pts) Pourquoi la commande suivante peut-elle échouer ou donner des résultats inattendus ?
```bash
find /usr/include -name *.h
```
Donnez la correction et expliquez la cause.

Si on ne met pas les guillemets, le bash interprète le *.h mais je comprends pas trop comment ça marche

---

**1.4** (4 pts) Un script `monScript.sh` contient :
```bash
#!/bin/bash
ma_var="test"
```
On l'exécute avec `./monScript.sh`, puis dans le terminal courant on tape `echo $ma_var` : la valeur est vide. Pourquoi ? Donnez **deux** façons de rendre `ma_var` accessible dans le shell courant après exécution du script.

La variable n'affiche rien car elle est déclarée uniquement dans le script.. par contre je ne sais pas comment le rendre accessible.

---

**1.5** (2 pts) Quel est l'effet du bit **SGID** (`chmod g+s`) lorsqu'il est appliqué sur un **répertoire** ?

Je ne sais plus

---

**1.6** (3 pts) Expliquez la différence entre `cp file1 file2` et `mv file1 file2` en termes de **droits minimaux** nécessaires :
- sur le fichier source `file1`
- sur le répertoire parent de `file1`
- sur le répertoire parent de `file2`

pour pouvoir faire cp il faut uniquement avec accès en mode lecture sur file1 et pour faire un mv il faut un accès en écriture

---

**1.7** (3 pts) Dans un script Bash, pourquoi faut-il (presque) toujours mettre une variable entre **doubles quotes** : `"$var"` ? Donnez un cas concret où l'absence de quotes produit un résultat incorrect ou dangereux.

je ne sais pas

---

## Partie 2 — Commandes à écrire (30 pts)

> Résolvez chaque problème en une **seule ligne de commande** (pipes et redirections autorisés).
> Si nécessaire, les commandes de préparation (`mkdir -p`, etc.) ne comptent pas dans la ligne.

---

**2.1** (2 pts) Affichez le nombre de lignes contenues dans le fichier `/etc/passwd`.

cat /etc/passwd | wc -l 

---

**2.2** (3 pts) Affichez **uniquement les noms d'utilisateurs** (1er champ) dont l'UID (3ème champ) est compris entre 1000 et 1999 dans `/etc/passwd`.

```
cat /etc/passwd | cut -d: -f1,3 | grep :1[0-9][0-9][0-9]$
```

---

**2.3** (2 pts) Créez en **une seule commande** les fichiers suivants dans le répertoire courant : `data_01.txt`, `data_02.txt`, ..., `data_15.txt`.

touch data_{01..15}.txt

---

**2.4** (4 pts) Écrivez une commande qui :
- copie **tous** les fichiers `.conf` du répertoire `/etc/` (y compris dans ses sous-répertoires)
- dans le répertoire `~/backup_conf/`
- en **supprimant les messages d'erreur** (`permission denied`) de l'affichage

*(Vous pouvez supposer que `~/backup_conf/` existe déjà.)*

```
find /etc -name "*.conf" -exec cp {} ~/backup_conf/ \;
```

---

**2.5** (4 pts) Écrivez une commande qui :
- affiche les **3 derniers utilisateurs connectés** au système (commande `last`)
- extrait **uniquement leur nom**
- supprime les doublons
- trie alphabétiquement


```
last | cut -d ' ' -f1 | head -n 3
```

---

**2.6** (3 pts) Écrivez une commande qui compte le nombre total **d'entrées** (fichiers + répertoires) dans `/usr/share/doc/` et **tous ses sous-répertoires**.


```
find /usr/share/doc/ | wc -l
```


---

**2.7** (4 pts) Écrivez une commande qui :
- affiche les utilisateurs actuellement connectés (commande `w`)
- extrait pour chacun leur **nom d'utilisateur** et leur **temps d'inactivité (IDLE)**
- formate la sortie comme : `nom:idle`
- utilise obligatoirement la commande `tr` pour transformer les espaces successifs


```
w | tr -s ' ' | cut -d ' ' -f1,5 | tail -n +3 | tr ' ' ':'
```

---

**2.8** (4 pts) Écrivez une commande qui crée un fichier `~/rapport.txt` contenant exactement le texte suivant, avec **substitution de variables activée** :
```
Rapport généré par <votre_login> le <date_du_jour>
```
Par exemple :
```bash
Rapport généré par henochrjt le dim 3 mai 2026 14:30:00 UTC
```


```bash
echo Rapport généré par $USER le $(date) > ~/rapport.txt

cat ~/rapport.txt
```


```bash
cat <<EOF > ~/rapport.txt
Rapport généré par $(whoami) le $(date)
EOF
```


> [!note]
> - ~/rapport.txt : fichier rapport.txt dans ton dossier personnel (~ = /home/ton_login).
> - ./rapport.txt : fichier rapport.txt dans le dossier courant (. = là où tu te trouves maintenant).
> Exemple :
> - si tu es dans /tmp, alors ./rapport.txt = /tmp/rapport.txt
> - mais ~/rapport.txt = /home/henochrjt/rapport.txt (toujours le home)
> Donc ~ = emplacement fixe (ton home), . = emplacement relatif au répertoire actuel.


---

**2.9** (4 pts) Créez l'alias `lt` qui affiche la liste détaillée des fichiers **triés par date de modification** (du plus récent au plus ancien). Donnez :
1. La commande pour définir l'alias
2. La commande pour le rendre permanent à chaque nouvelle session


```
echo "alias lt='ls -lt'" >> ~/.bashrc
```


> [!note]
> Pour le rendre permanent, ajoute la ligne dans ~/.bashrc (ou ~/.zshrc si zsh), puis recharge :
> source ~/.bashrc


---

## Partie 3 — Analyse et Débogage (20 pts)

---

**3.1** (6 pts) On exécute les commandes suivantes successivement :

```bash
mkdir ~/test_exam
chmod 600 ~/test_exam
touch ~/test_exam/fic1.txt
echo "hello" > ~/test_exam/fic1.txt
ls -l ~/test_exam/fic1.txt
```

Analysez précisément le résultat de **chaque commande** (la 3e, 4e et 5e) en expliquant :
- si elle réussit ou échoue
- pourquoi, en termes de **droits sur le répertoire** et de **droits sur le fichier**

---

**3.2** (6 pts) Le script suivant, nommé `compte.sh`, est censé afficher les nombres de 1 à 10 :

```bash
#!/bin/bash
for i in $(seq 1 10)
    echo $i
done
```

**a)** Il ne fonctionne pas. Identifiez et corrigez **toutes les erreurs** de syntaxe et de style.

**b)** Réécrivez la boucle en utilisant la syntaxe `{1..10}` à la place de `seq`, sans changer le résultat.

---

**3.3** (4 pts) Un étudiant tape :

```bash
chmod ugo= fichier.txt
cp fichier.txt copie.txt
```

La deuxième commande échoue. Expliquez pourquoi, puis décrivez **deux méthodes** différentes (en tant que propriétaire du fichier) pour parvenir quand même à copier le contenu de `fichier.txt`.

---

**3.4** (4 pts) Expliquez pourquoi la commande suivante ne retourne pas tous les fichiers `.txt` attendus dans le home, puis corrigez-la :

```bash
ls -la ~ | grep ".txt"
```

---

## Partie 4 — Scripts Bash à écrire (30 pts)

---

### Exercice 4.1 : `creer_projet.sh` (12 pts)

Écrivez un script Bash qui accepte **un seul argument** : le nom d'un projet.

**Comportement attendu :**
- Crée l'arborescence `~/projets/<nom_projet>/` avec trois sous-répertoires : `src/`, `doc/` et `bin/`
- Crée un fichier `README.md` à la racine du projet contenant :
  ```markdown
  # Projet : <nom_du_projet>
  Auteur : <login_de_l'utilisateur>
  Date : <date_actuelle>
  ```
- Affiche un message de confirmation : `Projet '<nom>' cree dans ~/projets/<nom>/`
- Si aucun argument n'est fourni, affiche sur **stderr** :
  ```
  Erreur : nom du projet requis
  ```
  et quitte avec le code de retour **1**.

**Contraintes :**
- Le script doit être validable par `shellcheck` (pas d'erreurs, quotes obligatoires)
- Vous **devez** utiliser un **Here Document** pour générer le contenu du `README.md`

---

### Exercice 4.2 : `gestion_users.sh` (18 pts)

Écrivez un script Bash qui accepte **exactement deux arguments** :
1. Une action : `create` ou `delete`
2. Un nombre entier `N` (par exemple `50`)

**Comportement si `create` :**
- Crée les utilisateurs `exam_user1` à `exam_userN`
- Chaque utilisateur doit avoir un **répertoire home** (option `-m` ou équivalent)
- Le **groupe principal** de chaque utilisateur doit être `exam_group`
- Si le groupe `exam_group` n'existe pas encore sur le système, le script le crée automatiquement **avant** de créer les utilisateurs

**Comportement si `delete` :**
- Supprime les utilisateurs `exam_user1` à `exam_userN`
- Supprime également leur répertoire home (option `-r` ou équivalent)
- **Ne supprime pas** le groupe `exam_group`

**Contraintes et vérifications :**
- Le script **doit** vérifier qu'il est exécuté en tant que **root** (`UID` == 0). Sinon, affiche sur stderr `Ce script doit etre execute en root` et quitte avec le code **1**.
- Le script **doit** vérifier que les deux arguments sont présents. Sinon, affiche sur stderr :
  ```
  Usage : ./gestion_users.sh {create|delete} N
  ```
  et quitte avec le code **1**.
- Vous **devez** utiliser une boucle **`while`** (interdiction formelle d'utiliser `for` ou `seq`).
- Affichez un compte-rendu ligne par ligne : `Cree : exam_user1` ou `Supprime : exam_user1`.

---

## FIN DU SUJET

---

> **Rappels importants pour ce genre d'épreuve :**
> - Faites attention aux droits sur les répertoires (pas seulement sur les fichiers)
> - Pensez à toujours protéger vos variables avec des guillemets doubles
> - `man <commande>` est votre ami... sauf que vous n'avez pas accès aux manuels ici !
> - Testez mentalement votre script avant de l'écrire : qu'arrive-t-il si N = 0 ?
