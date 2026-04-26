# Leçon 01 - 2026-01-28 (5p)

>Présentation du module, prise en main, shell
>
>“graphical user interfaces make easy tasks easy, while command line interfaces make difficult tasks possible”

## Accueil

* [Bienvenue](<../../Cours_Mylos/site/cours/int-sys1-nix/bienvenue/index.html>)
* [Accueil](<../../Cours_Mylos/site/cours/int-sys1-nix/accueil/index.html>)

## Prise en main

* [Le shell](<../../Cours_Mylos/site/cours/int-sys1-nix/shell/index.html>)
   1. [Prise en main](<../../Cours_Mylos/site/cours/int-sys1-nix/shell/prise-en-main/index.html>)
      * [Présentation Unix, rappel et définition](<../../Cours_Mylos/site/cours/int-sys1-nix/shell/rappel-definition/index.html>)
      * [Bash, BNF](<../../Cours_Mylos/site/cours/int-sys1-nix/shell/bnf-bash/index.html>)
      * [The Linux Commande Line](http://linuxcommand.org/tlcl.php)
   1. [Accès au serveur pédagogique Linux](<../../Cours_Mylos/site/cours/int-sys1-nix/shell/serveur-pedagogique/index.html>)
      * [lien vers les clés](https://rpns2-my.sharepoint.com/:f:/g/personal/huguenindo_s2_rpn_ch/IgBJsjqBxNjAQqzvB9ARtZfPAd8HURsOOxQmGNADLsmNv6g?e=5W3nJB)
      * mot de passe pour l'utilisation des clés ssh : `<username>pass$`
      * diminuer les droits sur les clé privé (chmod go= <clé privé>)
   1. Activité [Activités, série 0001 - Prise en main](<../../Cours_Mylos/site/cours/int-sys1-nix/activites/sysnix-activite-0001-prise-en-main/index.html>)

## gameshell

[gameshell](https://github.com/phyver/GameShell/blob/master/README-fr.md)

* préparation
   ```bash
   huguenindo@lozan:~$ ln -s /usr/local/games/gameshell.sh gameshell.sh
   ```
* exécution de jeu
   ```bash
   huguenindo@lozan:~$ ./gameshell.sh
   ```

### missions  de gameshell

>Pour les personnes avancées, résoudre la mission en un minimum de commandes!

1. basic/01_cd_tower (réussie)
1. basic/02_cd.._cellar (réussie)
1. basic/03_cd_HOME_throne (réussie)
1. basic/04_mkdir_chest (réussie)
1. basic/05_rm_spiders_cellar (réussie)
1. basic/06_mv_coins_garden (réussie)
1. basic/07_mv_hidden_coins_garden (réussie)
1. basic/08_rm_wildcard_spiders_cellar (réussie)
1. basic/09_rm_wildcard_hidden_spiders_cellar (réussie)
1. basic/10_cp_standard_great_hall (réussie)
1. basic/11_cp_wildcards_tapestries_great_hall (réussie)
1. basic/12_cp_ls_mtime_paintings_tower (réussie)
1. misc/01_cal_nostradamus (réussie)
1. intermediate/01_alias_la (réussie)
1. misc/02_nano_journal (réussie)
1. intermediate/02_alias_journal (réussie)
1. intermediate/03_tab_spider_lair (réussie)
1. intermediate/04_bg_xeyes (annulée)
1. finding_files_maze/01_ls_cd (réussie)
1. finding_files_maze/02_tree (réussie)
1. finding_files_maze/03_find_1 (réussie)
1. pipe_intro_book_of_potions/01_head (réussie)
1. pipe_intro_book_of_potions/02_tail (réussie)
1. pipe_intro_book_of_potions/03_cat (réussie)
1. pipe_intro_book_of_potions/04_pipe (réussie)
1. pipe_intro_book_of_potions/05_pipe_head_tail (réussie)
1. processes/01_ps_kill (réussie)
1. processes/02_ps_kill_signal (réussie)
1. processes/03_pstree_kill (réussie)
1. stdin_stdout_stderr/01_stdin_additions (réussie)
1. stdin_stdout_stderr/02_stdin_redirection_multiplications (réussie)
1. stdin_stdout_stderr/03_stdout_redirection_inventory (réussie)
1. stdin_stdout_stderr/04_stderr_dev-null_grimoires (réussie)
1. stdin_stdout_stderr/05_stdout_stderr_redirection_merlin (réussie)
1. permissions/01_chmod_x_dir_king_quarter (réussie)
1. permissions/02_chmod_r_file_king_quarter (réussie)
1. permissions/03_chmod_rw_file_dir_throne_room (réussie)
1. finding_files_maze/04_find_2 (réussie)
1. finding_files_maze/05_find_xargs_grep (réussie)
1. pipes_merchant_stall/01_pipe_1 (réussie)
1. pipes_merchant_stall/02_pipe_2 (réussie)
1. misc/03_tr_caesar_shift (réussie)


## A faire

* A étudier les documents
   * [Présentation Unix, rappel et définition](<../../Cours_Mylos/site/cours/int-sys1-nix/shell/rappel-definition/index.html>)
   * [Motif Générique](<../../Cours_Mylos/site/cours/int-sys1-nix/shell/motif-generique/index.html>)
   * [Filtre et Redirection](<../../Cours_Mylos/site/cours/int-sys1-nix/shell/redirection-filtre/index.html>)
* faire gameshell jusqu'à la mission 12/43

## Note

1. supprimer la passphrase de la clé privée ssh [How to Remove the Passphrase From an Existing SSH Key](https://www.baeldung.com/linux/remove-ssh-key-password)
1. connexion à lozan
  ```bash
  huguenindo@debian-usb:~$ ssh huguenindo@lozan0.node.dhu -oProxyCommand="ssh huguenindo@kobenhavn.s2.rpn.ch -A -i ~/.ssh/huguenindo@kobenhavn_rsa -W %h:%p" -i ~/.ssh/huguenindo@lozan0_rsa -A
  Linux lozan 6.1.0-25-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.106-3 (2024-08-26) x86_64

  The programs included with the Debian GNU/Linux system are free software;
  the exact distribution terms for each program are described in the
  individual files in /usr/share/doc/*/copyright.

  Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
  permitted by applicable law.
  Last login: Tue Jan 28 11:05:55 2025 from 172.16.1.10
  huguenindo@lozan0:~$ w
  08:50:29 up 91 days, 21:51,  7 users,  load average: 0.12, 0.09, 0.09
  UTIL.    TTY      DE               LOGIN@   IDLE   JCPU   PCPU QUOI
  huguenin pts/0    172.16.1.10      08:29    1.00s  0.01s  0.01s w
  dilke    pts/1    172.16.1.10      08:30   12:09   0.00s   ?    -bash
  cattarin pts/2    172.16.1.10      08:31   13.00s  0.03s   ?    sudo -s
  hazerajh pts/3    172.16.1.10      08:31   18:34   0.00s   ?    -bash
  maurerr1 pts/4    172.16.1.10      08:32   18:18   0.00s   ?    -bash
  bastosda pts/6    172.16.1.10      08:41    8:47   0.00s   ?    -bash
  borcardj pts/7    172.16.1.10      08:43   14.00s  0.02s  0.02s -bash
  huguenindo@lozan:~$ exit
  déconnexion
  Connection to lozan0.node.dhu closed.
  huguenindo@debian-usb:~$ ssh lozan
  Linux lozan 6.1.0-25-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.106-3 (2024-08-26) x86_64

  The programs included with the Debian GNU/Linux system are free software;
  the exact distribution terms for each program are described in the
  individual files in /usr/share/doc/*/copyright.

  Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
  permitted by applicable law.
  Last login: Wed Jan 29 08:29:45 2025 from 172.16.1.10
  huguenindo@lozan0:~$ 
  huguenindo@lozan0:~$ 
  huguenindo@lozan0:~$ exit
  déconnexion
  Connection to lozan0.node.dhu closed.
  huguenindo@debian-usb:~$ ssh -F ~/.ssh/config lozan
  Linux lozan 6.1.0-25-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.106-3 (2024-08-26) x86_64

  The programs included with the Debian GNU/Linux system are free software;
  the exact distribution terms for each program are described in the
  individual files in /usr/share/doc/*/copyright.

  Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
  permitted by applicable law.
  Last login: Wed Jan 29 08:54:33 2025 from 172.16.1.10
  huguenindo@lozan0:~$ exit
  déconnexion
  Connection to lozan0.node.dhu closed.
  ```

![xournal](<../../Cours_Mylos/wiki/xournal/2026-01-28-Note-10-40-1.svg>)
q
![xournal](<../../Cours_Mylos/wiki/xournal/2026-01-28-Note-10-40-2.svg>)

![xournal](<../../Cours_Mylos/wiki/xournal/2026-01-28-Note-10-40-3.svg>)
