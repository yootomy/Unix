# Here Documents — Notes de cours (Bash)

---

## Principe

Un **here document** redirige un bloc de texte vers l'entrée standard (`stdin`) d'une commande.

```bash
COMMANDE <<MOT_LIMITE
...contenu...
MOT_LIMITE
```

Le `<<` redirige tout ce qui suit vers la commande, jusqu'au mot limite final.

---

## Syntaxe de base

```bash
cat <<EOF
Ligne 1
Ligne 2
Ligne 3
EOF
```

> Le mot limite (`EOF`, `END`, `STOP`...) doit être **unique** et ne pas apparaître dans le contenu.

---

## Règles importantes

- Le **mot limite final** doit être en **première position** sur sa ligne (pas d'espaces avant)
- Pas d'espaces après le mot limite non plus
- Le non-respect de ces règles empêche la reconnaissance du mot limite

---

## Supprimer les tabulations avec `<<-`

```bash
cat <<-EOF
    Cette ligne a des tabs au début.
    Ils seront supprimés à l'affichage.
EOF
```

> Supprime les **tabs** en début de ligne (pas les espaces).

---

## Substitution de variables (activée par défaut)

```bash
NAME="Alice"
cat <<EOF
Bonjour, $NAME !
Date : $(date)
EOF
```

Les variables et substitutions de commandes sont **interprétées**.

---

## Désactiver la substitution (guillemets sur le mot limite)

```bash
cat <<'EOF'
Ceci est littéral : $NAME
`ls` ne sera pas exécuté
EOF
```

> Mettre le mot limite entre `'...'` ou `"..."` ou le précéder de `\` pour désactiver l'interprétation.

---

## Écrire dans un fichier

```bash
cat <<EOF > monfichier.txt
Contenu du fichier
ligne 2
EOF
```

---

## Utilisation avec des fonctions

```bash
lire_donnees() {
  read prenom
  read nom
}

lire_donnees <<RECORD
Alice
Dupont
RECORD
```

---

## Commenter un bloc de code

```bash
: <<COMMENTBLOCK
echo "Ce code ne s'exécute pas"
rm -rf /tmp/test
COMMENTBLOCK
```

> `:` est une commande vide. Pratique pour désactiver temporairement un bloc.

---

## Capturer la sortie dans une variable

```bash
ma_var=$(cat <<EOF
Ceci s'étale
sur plusieurs lignes.
EOF
)
echo "$ma_var"
```

---

## Exemples pratiques

### Afficher un message multi-lignes

```bash
cat <<FIN
------------------------------
Bienvenue dans ce script !
Appuyez sur Entrée pour continuer.
------------------------------
FIN
```

### Générer un script depuis un script

```bash
cat <<'EOF' > nouveau_script.sh
#!/bin/bash
echo "Script généré automatiquement"
echo "La variable \$HOME est : $HOME"
EOF
chmod +x nouveau_script.sh
```

### Session FTP automatisée

```bash
ftp -n serveur.example.com <<END_SESSION
user anonymous mon@email.com
binary
cd /pub
get fichier.tar.gz
bye
END_SESSION
```

---

## Récapitulatif des variantes

| Syntaxe | Effet |
|---------|-------|
| `<<MOT` | Here document standard, substitution activée |
| `<<'MOT'` | Substitution désactivée (texte littéral) |
| `<<"MOT"` | Idem, substitution désactivée |
| `<<\MOT` | Idem, substitution désactivée |
| `<<-MOT` | Supprime les tabulations en début de ligne |

---

## Références

- *Advanced Bash-Scripting Guide* — Chapitre 19 : Here Documents
