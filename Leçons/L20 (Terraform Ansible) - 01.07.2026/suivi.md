# Leçon 20 - 2026-07-01 (5p)

> automatisation

## Activités -  automatisation

* [tuto.infra - tutoriel pour la mise ne place d'infrastructure informatique à l'aide de terraform et ansible](<../../Cours_Mylos/site/cours/int-sys1-nix/fiches/tuto-infra/index.html>)
  1. Faire fonctionner l'infra
      1. configurer l'environnement avec direnv ... [tuto.infra - configuration de environnement](https://mylos.s2.rpn.ch/gitlab/dhu.infrastructure/tuto.infra/-/wikis/environnement)
      1. forker le projet uniquement la branche master
      1. modifier les clés public ssh dans le fichier tf/variables.tf dans le profile cloud-init
      1. valider le fonctionnement terraform apply
  1. Analyser le code  (suivre les [Étapes](https://mylos.s2.rpn.ch/gitlab/dhu.infrastructure/tuto.infra/-/wikis/home#%C3%A9tapes))

      Créer un branche sur le 3e commit, à chaque étape faire un cherry peek.

* activité - story

  En tant que développeur, je souhaite disposer d’une infrastructure de post-production, où le service REST est déployé sur une machine `rest0` et la base de données PostgreSQL sur une machine `db0`, afin de pouvoir tester le fonctionnement de mon service dans un environnement neutre. Cette infrastructure doit pouvoir être provisionnée et configurée automatiquement à l’aide de `Terraform` et `Ansible`, pour me permettre de la recréer à tout moment de façon fiable et reproductible.
