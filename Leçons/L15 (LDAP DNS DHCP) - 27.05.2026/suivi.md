# Leçon 15 - 2026-05-27 (5p)

## Services réseaux - AS, LDAP

* [Services réseaux](<../../Cours_Mylos/site/cours/int-sys1-nix/services-reseaux/index.html>)
    * [Service réseau - Service d'authentification](<../../Cours_Mylos/site/cours/int-sys1-nix/services-reseaux/authentification/index.html>)
        1. [Utilitaires LDAP](<../../Cours_Mylos/site/cours/int-sys1-nix/services-reseaux/srv-ldap/index.html>)
        1. [Activité, Requêtes LDAP](<../../Cours_Mylos/site/cours/int-sys1-nix/activites/services-reseaux-activite-1300-ldap-requetes/index.html>)
            * [Éléments de solution](./elements-de-solution/services-reseaux-activite-1300-ldap-requetes)
            * chaîne de connexion sur ldap.s2.rpn.ch
                ```bash
                huguenindo@ubuntu-usb-dhu:~$ ldapsearch -H ldap://ldap.s2.rpn.ch\
                            -D "CN=Huguenin Dominique (DHU),OU=Enseignants,OU=TI,OU=CPNE,OU=Utilisateurs,DC=s2,DC=rpn,DC=ch"\
                            -W\
                            -b OU=CPNE,OU=Utilisateurs,DC=s2,DC=rpn,DC=ch\
                            "(cn=*Huguenin*)"\
                            dn
                Enter LDAP Password: 
                # extended LDIF
                #
                # LDAPv3
                # base <OU=CPNE,OU=Utilisateurs,DC=s2,DC=rpn,DC=ch> with scope subtree
                # filter: (cn=*Huguenin*)
                # requesting: dn 
                #

                # Huguenin-Elie Nathan, 2DIN-C-DMa, DIN-C-D, Eleves, AS, CPNE, Utilisateurs, s2
                .rpn.ch
                dn: CN=Huguenin-Elie Nathan,OU=2DIN-C-DMa,OU=DIN-C-D,OU=Eleves,OU=AS,OU=CPNE,O
                U=Utilisateurs,DC=s2,DC=rpn,DC=ch

                # Huguenin-Dumittan Timoth\C3\A9e, 4MMA-C-DKa, MMA-CD, Eleves, TI, CPNE, Utilis
                ateurs, s2.rpn.ch
                dn:: Q049SHVndWVuaW4tRHVtaXR0YW4gVGltb3Row6llLE9VPTRNTUEtQy1ES2EsT1U9TU1BLUNEL
                E9VPUVsZXZlcyxPVT1USSxPVT1DUE5FLE9VPVV0aWxpc2F0ZXVycyxEQz1zMixEQz1ycG4sREM9Y2
                g=

                # Huguenin-Virchaux Ma\C3\ABl, 4HOR-C-PKa, HOR-CP, Eleves, TI, CPNE, Utilisateu
                rs, s2.rpn.ch
                dn:: Q049SHVndWVuaW4tVmlyY2hhdXggTWHDq2wsT1U9NEhPUi1DLVBLYSxPVT1IT1ItQ1AsT1U9R
                WxldmVzLE9VPVRJLE9VPUNQTkUsT1U9VXRpbGlzYXRldXJzLERDPXMyLERDPXJwbixEQz1jaA==

                # Huguenin-Dumittan Lo\C3\AFc, 4PME-4TDKa, PME-4TD, Eleves, TI, CPNE, Utilisate
                urs, s2.rpn.ch
                dn:: Q049SHVndWVuaW4tRHVtaXR0YW4gTG/Dr2MsT1U9NFBNRS00VERLYSxPVT1QTUUtNFRELE9VP
                UVsZXZlcyxPVT1USSxPVT1DUE5FLE9VPVV0aWxpc2F0ZXVycyxEQz1zMixEQz1ycG4sREM9Y2g=

                # Huguenin-Elie Ethan, 2MML-C-DKa, MML-CD, Eleves, TI, CPNE, Utilisateurs, s2.r
                pn.ch
                dn: CN=Huguenin-Elie Ethan,OU=2MML-C-DKa,OU=MML-CD,OU=Eleves,OU=TI,OU=CPNE,OU=
                Utilisateurs,DC=s2,DC=rpn,DC=ch

                # Huguenin Dominique - El\C3\A8ve, Eleves, TI, CPNE, Utilisateurs, s2.rpn.ch
                dn:: Q049SHVndWVuaW4gRG9taW5pcXVlIC0gRWzDqHZlLE9VPUVsZXZlcyxPVT1USSxPVT1DUE5FL
                E9VPVV0aWxpc2F0ZXVycyxEQz1zMixEQz1ycG4sREM9Y2g=

                # Huguenin Brayan, 3PRO-S-EMa, PRO-SE, Eleves, TI, CPNE, Utilisateurs, s2.rpn.c
                h
                dn: CN=Huguenin Brayan,OU=3PRO-S-EMa,OU=PRO-SE,OU=Eleves,OU=TI,OU=CPNE,OU=Util
                isateurs,DC=s2,DC=rpn,DC=ch

                # HugueninBGr, 4CAP-C-DKa, CAP-CD, Eleves, TI, CPNE, Utilisateurs, s2.rpn.ch
                dn: CN=HugueninBGr,OU=4CAP-C-DKa,OU=CAP-CD,OU=Eleves,OU=TI,OU=CPNE,OU=Utilisat
                eurs,DC=s2,DC=rpn,DC=ch

                # Huguenin-Virchaux Nicolas (NIH), Enseignants, TI, CPNE, Utilisateurs, s2.rpn.
                ch
                dn: CN=Huguenin-Virchaux Nicolas (NIH),OU=Enseignants,OU=TI,OU=CPNE,OU=Utilisa
                teurs,DC=s2,DC=rpn,DC=ch

                # Huguenin-Vuillemin Philippe (PHG), Enseignants, TI, CPNE, Utilisateurs, s2.rp
                n.ch
                dn: CN=Huguenin-Vuillemin Philippe (PHG),OU=Enseignants,OU=TI,OU=CPNE,OU=Utili
                sateurs,DC=s2,DC=rpn,DC=ch

                # Huguenin Dominique (DHU), Enseignants, TI, CPNE, Utilisateurs, s2.rpn.ch
                dn: CN=Huguenin Dominique (DHU),OU=Enseignants,OU=TI,OU=CPNE,OU=Utilisateurs,D
                C=s2,DC=rpn,DC=ch

                # Huguenin Damien, Eleves, CMOD, CPNE, Utilisateurs, s2.rpn.ch
                dn: CN=Huguenin Damien,OU=Eleves,OU=CMOD,OU=CPNE,OU=Utilisateurs,DC=s2,DC=rpn,
                DC=ch

                # Huguenin-Dumittan Amalia (AHD), Enseignants, 2S, CPNE, Utilisateurs, s2.rpn.c
                h
                dn: CN=Huguenin-Dumittan Amalia (AHD),OU=Enseignants,OU=2S,OU=CPNE,OU=Utilisat
                eurs,DC=s2,DC=rpn,DC=ch

                # Huguenin-Virchaux Nathan, 1FOB-C-DAa, FOB-C-D, Eleves, TN, CPNE, Utilisateurs
                , s2.rpn.ch
                dn: CN=Huguenin-Virchaux Nathan,OU=1FOB-C-DAa,OU=FOB-C-D,OU=Eleves,OU=TN,OU=CP
                NE,OU=Utilisateurs,DC=s2,DC=rpn,DC=ch

                # Huguenin Dumittan Eliot, 3MEB-C-DLa, MEB-C-D, Eleves, BC, CPNE, Utilisateurs,
                s2.rpn.ch
                dn: CN=Huguenin Dumittan Eliot,OU=3MEB-C-DLa,OU=MEB-C-D,OU=Eleves,OU=BC,OU=CPN
                E,OU=Utilisateurs,DC=s2,DC=rpn,DC=ch

                # HugueninDDa, 3AGE-C-DMa, AEC-C-D, Eleves, BC, CPNE, Utilisateurs, s2.rpn.ch
                dn: CN=HugueninDDa,OU=3AGE-C-DMa,OU=AEC-C-D,OU=Eleves,OU=BC,OU=CPNE,OU=Utilisa
                teurs,DC=s2,DC=rpn,DC=ch

                # Huguenin Noah, 3INS-C-DLa, INS-C-D, Eleves, BC, CPNE, Utilisateurs, s2.rpn.ch
                dn: CN=Huguenin Noah,OU=3INS-C-DLa,OU=INS-C-D,OU=Eleves,OU=BC,OU=CPNE,OU=Utili
                sateurs,DC=s2,DC=rpn,DC=ch

                # Huguenin-Bergenat Michael, 4IEL-C-DLb, IEL-C-D, Eleves, BC, CPNE, Utilisateur
                s, s2.rpn.ch
                dn: CN=Huguenin-Bergenat Michael,OU=4IEL-C-DLb,OU=IEL-C-D,OU=Eleves,OU=BC,OU=C
                PNE,OU=Utilisateurs,DC=s2,DC=rpn,DC=ch

                # Huguenin-Dezot Laura, 1EDC-C-DPe, EDC-C-D, Eleves, CG, CPNE, Utilisateurs, s2
                .rpn.ch
                dn: CN=Huguenin-Dezot Laura,OU=1EDC-C-DPe,OU=EDC-C-D,OU=Eleves,OU=CG,OU=CPNE,O
                U=Utilisateurs,DC=s2,DC=rpn,DC=ch

                # Huguenin-Bergenat Talia, 1EDC-C-DPc, EDC-C-D, Eleves, CG, CPNE, Utilisateurs,
                s2.rpn.ch
                dn: CN=Huguenin-Bergenat Talia,OU=1EDC-C-DPc,OU=EDC-C-D,OU=Eleves,OU=CG,OU=CPN
                E,OU=Utilisateurs,DC=s2,DC=rpn,DC=ch

                # HugueninV1, 1MPE-1EPMd, MPE2, Eleves, CG, CPNE, Utilisateurs, s2.rpn.ch
                dn: CN=HugueninV1,OU=1MPE-1EPMd,OU=MPE2,OU=Eleves,OU=CG,OU=CPNE,OU=Utilisateur
                s,DC=s2,DC=rpn,DC=ch

                # Huguenin-Virchaux M\C3\A9lanie (MHV), Enseignants, CG, CPNE, Utilisateurs, s2
                .rpn.ch
                dn:: Q049SHVndWVuaW4tVmlyY2hhdXggTcOpbGFuaWUgKE1IViksT1U9RW5zZWlnbmFudHMsT1U9Q
                0csT1U9Q1BORSxPVT1VdGlsaXNhdGV1cnMsREM9czIsREM9cnBuLERDPWNo

                # search result
                search: 2
                result: 0 Success

                # numResponses: 23
                # numEntries: 22
                ```
        1. [Service réseau - Installation du client graphique ldap Apache directory Studio](<../../Cours_Mylos/site/cours/int-sys1-nix/services-reseaux/apache-directory-studio/index.html>)
        1. [Service réseau - Service Kerberos pour l'authentification et service LDAP pour le stockage ](<../../Cours_Mylos/site/cours/int-sys1-nix/services-reseaux/srv-kerberos-ldap/index.html>)
        1. [Service réseau - Service réseau - service SSSD pour Kerberos et LDAP](<../../Cours_Mylos/site/cours/int-sys1-nix/services-reseaux/client-kerberos-ldap/index.html>)
        1. faire une trace avec wireshark montrant les échanges ldap et kerberos durant le login de vonrathen.
            [trace wireshark pour le login](./elements-de-solution/wireshark-capture-login-vonrathen-sur-cavi.txt)


## A faire

* [Activité, Requêtes LDAP](<../../Cours_Mylos/site/cours/int-sys1-nix/activites/services-reseaux-activite-1300-ldap-requetes/index.html>)
* [Services réseaux - Activité 1000, Service DNS secondaire](<../../Cours_Mylos/site/cours/int-sys1-nix/activites/services-reseaux-activite-1000-dns-secondaire/index.html>)
  * [éléments de solution](./elements-de-solution/services-reseaux-activite-1000-dns-secondaire)
* [Services réseaux - Activité 1200, Mise à jour du DNS par le service DHCP](<../../Cours_Mylos/site/cours/int-sys1-nix/activites/services-reseaux-activite-1200-dns-update-dhcp/index.html>)
  * [éléments de solution](./elements-de-solution/services-reseaux-activite-1200-dns-update-dhcp)
* [Services réseaux - Activité 1600, Service DHCP Secondaire](<../../Cours_Mylos/site/cours/int-sys1-nix/activites/services-reseaux-activite-1600-dhcp-secondaire/index.html>)
  * [éléments de solution](./elements-de-solution/services-reseaux-activite-1600-dhcp-secondaire)

## Notes
