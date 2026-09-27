---
cabinet: Cabinet Exemple
date: 2026-07-03
intervenant: Technicien Exemple
presents: Responsable du cabinet, secrétariat
arrivee: 9 h 30
depart: 12 h 15
prochaine_visite: 2026-10-02
---

# Visite du 2026-07-03 — Cabinet Exemple

<!--
MODE D'EMPLOI
Codes : [x] Bon 🟢   [~] À surveiller 🟠   [!] À corriger 🔴   [-] Sans objet   [ ] non vérifié
Le code reflète l'état EN FIN DE VISITE : ce qui a été corrigé sur place passe au vert et va dans « fait: ».
Ligne : - [x] ID Libellé :: valeur :: note          (valeur et note facultatives)
Sous une ligne (indenté de 2 espaces) :
  - fait: ce qui a été corrigé pendant la visite
  - reco haute|moyenne|basse: ce qu'il faut faire ensuite
  - photo: photos/NOM.jpg
Tout 🔴 doit avoir une « reco ». Ne jamais noter : mots de passe, clés de récupération, noms de clients.
Avancement : visit-it-pro check 2026-07-03      Rapport : visit-it-pro report 2026-07-03
-->

## Synthèse

<!-- À rédiger en fin de visite : 4 à 5 phrases simples pour le/la responsable (état général, points forts, 2 ou 3 priorités, ce qui a été fait). Copié tel quel dans le rapport. -->

Première visite de référence. Les postes fonctionnent, mais la sauvegarde est en échec depuis mai (disque plein) et aucune restauration n'a pu être testée. Priorités : rétablir la sauvegarde, sécuriser la box (mot de passe d'usine) et remettre en ordre le Bureau 1 (mises à jour en échec, disque presque plein, écran jamais verrouillé).

## Entretien

<!-- PRIVÉ : jamais copié dans le rapport. 15 min avec le/la responsable et le personnel. -->

- Problèmes constatés récemment (lenteurs, plantages, coupures Internet, impression, fichiers perdus) :
- Tâches et logiciels critiques pour chaque personne :
- Où sont rangés les dossiers clients et les actes (poste, dossier, cloud, clé USB) :
- Incidents passés (virus, vol, perte de données, dégâts électriques) :
- Autres intervenants informatiques ; qui connaît les mots de passe administrateur :
- Conséquences d'une journée sans ordinateur ou sans Internet :
- Attentes du cabinet :

## Bureau et alimentation (BUR)

### Fiche

- Onduleur(s) (marque, modèle, âge) : 1 onduleur 700 VA (2023) sur le Bureau 1
- Imprimante / scanner (marque, modèle) : Multifonction laser réseau (exemple)

### Contrôles

- [~] BUR-onduleur Onduleurs (postes fixes et box) :: Bureau 1 seulement :: box et Bureau 2 sans onduleur
  <!-- Postes fixes et box sur onduleur, autonomie ≥ 5 min. Test en fin de visite (travail enregistré) : débrancher l'onduleur de la prise murale. Batterie d'onduleur à changer tous les 3 à 5 ans. -->
  - reco haute: Ajouter un onduleur pour le Bureau 2 et la box Internet
- [!] BUR-surtension Protection contre les surtensions :: Multiprises simples en cascade sous le Bureau 2
  <!-- Multiprises parafoudre (pas de simples multiprises) ; aucune multiprise branchée sur une autre. -->
  - reco haute: Remplacer par une multiprise parafoudre unique
- [!] BUR-ventilation Ventilation et poussière :: Unité centrale du Bureau 2 posée au sol, grilles bouchées
  <!-- Unités centrales ni enfermées, ni collées au mur, ni posées sur un sol poussiéreux ; grilles d'aération propres. -->
  - reco moyenne: Dépoussiérer et surélever l'unité centrale
- [x] BUR-cablage Câblage ::
  <!-- Câbles rangés, sans tension ni pliure ; rien sur le passage. -->
- [~] BUR-confidentialite Confidentialité aux postes de travail :: Écran du Bureau 1 visible depuis l'accueil
  <!-- Écrans non visibles depuis l'accueil ; aucun mot de passe affiché (post-it, sous le clavier). -->
  - reco moyenne: Réorienter l'écran ou poser un filtre de confidentialité
- [x] BUR-portable Sécurité physique du portable :: Rangé dans l'armoire fermée à clé le soir
  <!-- Rangé sous clé ou attaché (câble antivol) en dehors des heures d'ouverture ; jamais laissé dans une voiture. -->
- [x] BUR-impression Imprimante et scanner :: Page et numérisation de test OK depuis les 3 postes
  <!-- Page de test et numérisation de test depuis chaque poste concerné ; consommables disponibles. -->

## Internet et réseau (NET)

### Fiche

- Fournisseur d'accès : Fournisseur X (exemple)
- Offre / technologie (fibre, ADSL, 4G, satellite…) : Fibre
- Débit contractuel (descendant / montant) : 100 / 50 Mb/s
- Titulaire du contrat : Le cabinet
- Assistance (téléphone, n° client) :
- Box / routeur (marque, modèle) : Box du fournisseur (exemple)

### Contrôles

- [x] NET-box Box / routeur :: Ventilée, voyants normaux
  <!-- Emplacement ventilé, branché sur onduleur, voyants normaux. Demander à quelle fréquence il faut la redémarrer. -->
- [!] NET-admin Mot de passe d'administration du routeur :: Mot de passe d'usine (étiquette de la box)
  <!-- Différent de celui de l'étiquette ; connu du cabinet et conservé en lieu sûr. Ne jamais noter le mot de passe ici. -->
  - reco haute: Changer le mot de passe d'administration de la box
- [~] NET-firmware Micrologiciel du routeur :: Version de 2024, mise à jour automatique désactivée
  <!-- Page d'administration › Système / Mise à jour : version à jour ou mise à jour automatique activée. -->
  - reco moyenne: Mettre à jour le micrologiciel en dehors des heures d'ouverture
- [~] NET-wifi Sécurité du Wi-Fi :: WPA2, clé longue, WPS activé
  <!-- WPA2 ou WPA3 (jamais WEP ni réseau ouvert), clé longue et non devinable, WPS désactivé. -->
  - reco moyenne: Désactiver le WPS
- [!] NET-invites Wi-Fi invités :: Les clients utilisent le Wi-Fi du cabinet
  <!-- Les clients utilisent un réseau invités séparé (ou n'ont pas accès au Wi-Fi). Clients sur le réseau du cabinet = 🔴. -->
  - reco haute: Créer un réseau Wi-Fi invités séparé et changer la clé du Wi-Fi du cabinet
- [x] NET-appareils Appareils connectés :: 7 appareils, tous identifiés
  <!-- Liste des appareils dans la page du routeur : tous identifiés. Appareil inconnu = 🔴. -->
- [~] NET-debit Débit conforme au contrat :: 61 Mb/s sur le meilleur poste (61 %)
  <!-- Meilleur poste ≥ 70 % du débit contractuel (voir « Internet depuis ce poste » de chaque poste). 🟢 ≥ 70 % · 🟠 50–70 % · 🔴 < 50 %. -->
- [~] NET-stabilite Stabilité de la connexion :: 1 % de perte, 22 ms
  <!-- Invite de commandes : ping -n 100 8.8.8.8 → perte 🟢 0 % · 🟠 1–2 % · 🔴 > 2 % ; noter aussi la latence moyenne. Refaire vers la box (ipconfig → « Passerelle par défaut ») pour distinguer un problème de Wi-Fi d'un problème de fournisseur. -->
- [!] NET-coupures Coupures signalées :: Coupures presque quotidiennes en juin
  <!-- Coupures ressenties le mois dernier : aucune 🟢 · occasionnelles 🟠 · fréquentes 🔴. -->
  - reco haute: Signaler les coupures au fournisseur avec leurs dates et durées
- [x] NET-secours Solution de secours Internet :: Partage de connexion testé sur le portable
  <!-- Partage de connexion d'un téléphone testé sur un poste (ou second fournisseur). -->

## Poste 1 — Portable (PC1)

### Fiche

- Utilisateur(s) : Responsable du cabinet
- Marque et modèle : Portable 14 pouces (exemple)
- Numéro de série : EXEMPLE-PC1
- Windows (édition et version) : Windows 11 Pro 24H2
- Processeur / mémoire (RAM) : Core i5 / 16 Go
- Disque système (SSD ou HDD, capacité) : SSD 512 Go
- Année d'achat / garantie : 2022
- Suite bureautique (version) : Microsoft 365
- Logiciel métier : Logiciel notarial (exemple)
- Antivirus : Microsoft Defender

<!-- Numéro de série : étiquette sous l'appareil, ou PowerShell : Get-CimInstance Win32_BIOS | Select-Object SerialNumber. Windows : touche Windows › winver. Matériel : Paramètres › Système › Informations système ; SSD ou HDD : Gestionnaire des tâches › Performance. -->

### Contrôles

- [~] PC1-windows Version de Windows :: Windows 11 Pro 24H2
  <!-- winver. 🟢 Windows 11 25H2 ou plus récent (support jusqu'au 13 oct. 2027). 🟠 Windows 11 24H2 : fin de support le 13 oct. 2026, passer en 25H2 (🔴 après cette date). 🔴 Windows 11 23H2 ou plus ancien. 🔴 Windows 10 : fin de support le 14 oct. 2025 (🟠 seulement si inscrit aux mises à jour de sécurité étendues « ESU », jusqu'au 12 oct. 2027) ; noter la compatibilité Windows 11 (application « Contrôle d'intégrité du PC »). -->
  - reco haute: Installer Windows 11 25H2 avant le 13 octobre 2026
- [x] PC1-maj Mises à jour Windows :: Dernière installation le 11/06/2026
  <!-- Paramètres › Windows Update : rien en attente ni en échec ; Historique des mises à jour : dernière installation < 30 jours. Redémarré récemment : Gestionnaire des tâches › Performance › « Temps d'activité » (🟠 si > 14 jours). -->
- [x] PC1-antivirus Antivirus :: Microsoft Defender à jour
  <!-- Sécurité Windows › Protection contre les virus et menaces : protection en temps réel activée, informations de sécurité < 3 jours, aucune menace. Un seul antivirus (pas d'essai McAfee/Norton expiré). -->
- [x] PC1-parefeu Pare-feu ::
  <!-- Sécurité Windows › Pare-feu et protection du réseau : activé sur les 3 profils (domaine, privé, public). -->
- [!] PC1-chiffrement Chiffrement du disque :: Désactivé :: portable emporté chaque soir
  <!-- Paramètres › Confidentialité et sécurité › Chiffrement de l'appareil (édition Famille) ou BitLocker (Pro) ; ou invite de commandes administrateur : manage-bde -status. Clé de récupération conservée en lieu sûr (ne pas la noter ici). Désactivé : 🔴 sur un portable, 🟠 sur un poste fixe. -->
  - reco haute: Activer BitLocker et conserver la clé de récupération en lieu sûr
- [~] PC1-comptes Comptes utilisateurs :: Compte unique, administrateur
  <!-- Invite de commandes : net user, puis net localgroup Administrateurs (« Administrators » sur un Windows anglais). Chaque personne a son compte protégé (mot de passe ou code PIN) ; compte du quotidien administrateur = 🟠 ; compte sans mot de passe = 🔴. -->
  - reco moyenne: Créer un compte standard pour l'usage quotidien
- [x] PC1-verrouillage Verrouillage automatique :: 5 min
  <!-- Paramètres › Comptes › Options de connexion, et Système › Alimentation (mise en veille de l'écran) : verrouillage ≤ 10 min. Réflexe Windows + L en quittant le poste. -->
- [x] PC1-espace Espace disque libre (C:) :: 55 %
  <!-- Explorateur › Ce PC. Noter le % libre. 🟢 ≥ 20 % · 🟠 10–20 % · 🔴 < 10 %. -->
- [x] PC1-disque Santé du disque :: SSD sain
  <!-- PowerShell : Get-PhysicalDisk | Format-Table FriendlyName, MediaType, HealthStatus → « Healthy ». Disque système mécanique (HDD) = 🟠, recommander un SSD. Noter par ex. « SSD sain ». -->
- [x] PC1-stabilite Stabilité (indice /10) :: 8,1/10
  <!-- Touche Windows › perfmon /rel (Moniteur de fiabilité). Noter l'indice, par ex. « 8,5/10 ». 🟢 ≥ 7 sans plantages répétés ni arrêts inattendus sur 30 jours · 🟠 4–7 · 🔴 < 4. -->
- [x] PC1-demarrage Temps de démarrage :: 41 s
  <!-- Chronomètre : bouton marche → bureau utilisable ; noter en secondes. 🟢 < 90 s · 🟠 90–180 s · 🔴 > 180 s. Gestionnaire des tâches au repos : processeur < 20 %, mémoire < 80 % ; onglet « Applications de démarrage » : peu d'impact « élevé ». -->
- [x] PC1-logiciels Logiciels à jour et licenciés :: Microsoft 365 à jour
  <!-- Paramètres › Applications. 🔴 Office 2016/2019 (fin de support 14 oct. 2025). 🟠 Office 2021 (fin de support 13 oct. 2026, 🔴 ensuite). 🟢 Microsoft 365 ou Office 2024. Lecteur PDF et navigateur à jour ; pas de logiciel piraté ni d'« optimiseur de PC ». -->
- [x] PC1-distance Accès à distance :: Aucun
  <!-- Paramètres › Applications : TeamViewer, AnyDesk, etc. Aucun, ou connu, justifié et protégé. Outil inconnu ou inutilisé = 🔴 (à désinstaller). -->
- [x] PC1-usages Test des usages quotidiens ::
  <!-- Ouvrir le logiciel métier, imprimer, numériser, envoyer et recevoir un courriel, ouvrir un site : tout fonctionne. -->
- [x] PC1-internet Internet depuis ce poste :: ↓63 ↑30 Mb/s · 18 ms · Wi-Fi 79 %
  <!-- fast.com ou speedtest.net, puis invite de commandes : netsh wlan show interfaces (ligne « Signal »). Noter par ex. « ↓85 ↑20 Mb/s · 12 ms · Wi-Fi 78 % » ou « câble ». Signal Wi-Fi 🟢 ≥ 70 % · 🟠 50–70 % · 🔴 < 50 %. -->
- [x] PC1-etat État physique ::
  <!-- Grilles propres, ventilateurs silencieux ; écran, clavier, souris et ports en bon état. -->
- [~] PC1-batterie Batterie :: 74 %
  <!-- Invite de commandes : powercfg /batteryreport, puis ouvrir le fichier battery-report.html indiqué : capacité de charge complète ÷ capacité de conception. Noter le %. 🟢 ≥ 80 % · 🟠 60–80 % · 🔴 < 60 %. Chargeur et câble en bon état. -->
  - reco basse: Surveiller l'usure de la batterie

## Poste 2 — Bureau 1 (PC2)

### Fiche

- Utilisateur(s) : Secrétariat
- Marque et modèle : Tour de bureau (exemple)
- Numéro de série : EXEMPLE-PC2
- Windows (édition et version) : Windows 11 Pro 25H2
- Processeur / mémoire (RAM) : Core i5 / 8 Go
- Disque système (SSD ou HDD, capacité) : SSD 256 Go
- Année d'achat / garantie : 2021
- Suite bureautique (version) : Office 2019
- Logiciel métier : Logiciel notarial (exemple)
- Antivirus : Microsoft Defender

<!-- Numéro de série : étiquette sous l'appareil, ou PowerShell : Get-CimInstance Win32_BIOS | Select-Object SerialNumber. Windows : touche Windows › winver. Matériel : Paramètres › Système › Informations système ; SSD ou HDD : Gestionnaire des tâches › Performance. -->

### Contrôles

- [x] PC2-windows Version de Windows :: Windows 11 Pro 25H2
  <!-- winver. 🟢 Windows 11 25H2 ou plus récent (support jusqu'au 13 oct. 2027). 🟠 Windows 11 24H2 : fin de support le 13 oct. 2026, passer en 25H2 (🔴 après cette date). 🔴 Windows 11 23H2 ou plus ancien. 🔴 Windows 10 : fin de support le 14 oct. 2025 (🟠 seulement si inscrit aux mises à jour de sécurité étendues « ESU », jusqu'au 12 oct. 2027) ; noter la compatibilité Windows 11 (application « Contrôle d'intégrité du PC »). -->
- [!] PC2-maj Mises à jour Windows :: Mises à jour en échec depuis mai
  <!-- Paramètres › Windows Update : rien en attente ni en échec ; Historique des mises à jour : dernière installation < 30 jours. Redémarré récemment : Gestionnaire des tâches › Performance › « Temps d'activité » (🟠 si > 14 jours). -->
  - reco haute: Réparer Windows Update et installer les mises à jour
- [x] PC2-antivirus Antivirus :: Microsoft Defender à jour
  <!-- Sécurité Windows › Protection contre les virus et menaces : protection en temps réel activée, informations de sécurité < 3 jours, aucune menace. Un seul antivirus (pas d'essai McAfee/Norton expiré). -->
- [x] PC2-parefeu Pare-feu ::
  <!-- Sécurité Windows › Pare-feu et protection du réseau : activé sur les 3 profils (domaine, privé, public). -->
- [~] PC2-chiffrement Chiffrement du disque :: Non chiffré
  <!-- Paramètres › Confidentialité et sécurité › Chiffrement de l'appareil (édition Famille) ou BitLocker (Pro) ; ou invite de commandes administrateur : manage-bde -status. Clé de récupération conservée en lieu sûr (ne pas la noter ici). Désactivé : 🔴 sur un portable, 🟠 sur un poste fixe. -->
  - reco moyenne: Activer BitLocker
- [x] PC2-comptes Comptes utilisateurs ::
  <!-- Invite de commandes : net user, puis net localgroup Administrateurs (« Administrators » sur un Windows anglais). Chaque personne a son compte protégé (mot de passe ou code PIN) ; compte du quotidien administrateur = 🟠 ; compte sans mot de passe = 🔴. -->
- [!] PC2-verrouillage Verrouillage automatique :: Jamais
  <!-- Paramètres › Comptes › Options de connexion, et Système › Alimentation (mise en veille de l'écran) : verrouillage ≤ 10 min. Réflexe Windows + L en quittant le poste. -->
  - reco haute: Régler le verrouillage automatique sur 10 min
- [!] PC2-espace Espace disque libre (C:) :: 11 %
  <!-- Explorateur › Ce PC. Noter le % libre. 🟢 ≥ 20 % · 🟠 10–20 % · 🔴 < 10 %. -->
  - reco haute: Libérer de l'espace disque
- [x] PC2-disque Santé du disque :: SSD sain
  <!-- PowerShell : Get-PhysicalDisk | Format-Table FriendlyName, MediaType, HealthStatus → « Healthy ». Disque système mécanique (HDD) = 🟠, recommander un SSD. Noter par ex. « SSD sain ». -->
- [~] PC2-stabilite Stabilité (indice /10) :: 6,8/10
  <!-- Touche Windows › perfmon /rel (Moniteur de fiabilité). Noter l'indice, par ex. « 8,5/10 ». 🟢 ≥ 7 sans plantages répétés ni arrêts inattendus sur 30 jours · 🟠 4–7 · 🔴 < 4. -->
- [x] PC2-demarrage Temps de démarrage :: 58 s
  <!-- Chronomètre : bouton marche → bureau utilisable ; noter en secondes. 🟢 < 90 s · 🟠 90–180 s · 🔴 > 180 s. Gestionnaire des tâches au repos : processeur < 20 %, mémoire < 80 % ; onglet « Applications de démarrage » : peu d'impact « élevé ». -->
- [!] PC2-logiciels Logiciels à jour et licenciés :: Office 2019 :: fin de support le 14 oct. 2025
  <!-- Paramètres › Applications. 🔴 Office 2016/2019 (fin de support 14 oct. 2025). 🟠 Office 2021 (fin de support 13 oct. 2026, 🔴 ensuite). 🟢 Microsoft 365 ou Office 2024. Lecteur PDF et navigateur à jour ; pas de logiciel piraté ni d'« optimiseur de PC ». -->
  - reco haute: Passer à Microsoft 365 ou Office 2024
- [x] PC2-distance Accès à distance :: Aucun
  <!-- Paramètres › Applications : TeamViewer, AnyDesk, etc. Aucun, ou connu, justifié et protégé. Outil inconnu ou inutilisé = 🔴 (à désinstaller). -->
- [x] PC2-usages Test des usages quotidiens ::
  <!-- Ouvrir le logiciel métier, imprimer, numériser, envoyer et recevoir un courriel, ouvrir un site : tout fonctionne. -->
- [x] PC2-internet Internet depuis ce poste :: câble · ↓66 ↑31 Mb/s · 11 ms
  <!-- fast.com ou speedtest.net, puis invite de commandes : netsh wlan show interfaces (ligne « Signal »). Noter par ex. « ↓85 ↑20 Mb/s · 12 ms · Wi-Fi 78 % » ou « câble ». Signal Wi-Fi 🟢 ≥ 70 % · 🟠 50–70 % · 🔴 < 50 %. -->
- [x] PC2-etat État physique ::
  <!-- Grilles propres, ventilateurs silencieux ; écran, clavier, souris et ports en bon état. -->

## Poste 3 — Bureau 2 (PC3)

### Fiche

- Utilisateur(s) : Assistante
- Marque et modèle : Tour de bureau ancienne (exemple)
- Numéro de série : EXEMPLE-PC3
- Windows (édition et version) : Windows 10 Pro 22H2
- Processeur / mémoire (RAM) : Core i3 6e génération / 8 Go
- Disque système (SSD ou HDD, capacité) : HDD 1 To
- Année d'achat / garantie : 2016
- Suite bureautique (version) : Microsoft 365
- Logiciel métier : Logiciel notarial (exemple)
- Antivirus : Microsoft Defender

<!-- Numéro de série : étiquette sous l'appareil, ou PowerShell : Get-CimInstance Win32_BIOS | Select-Object SerialNumber. Windows : touche Windows › winver. Matériel : Paramètres › Système › Informations système ; SSD ou HDD : Gestionnaire des tâches › Performance. -->

### Contrôles

- [!] PC3-windows Version de Windows :: Windows 10 Pro 22H2, non inscrit à l'ESU :: processeur non compatible Windows 11
  <!-- winver. 🟢 Windows 11 25H2 ou plus récent (support jusqu'au 13 oct. 2027). 🟠 Windows 11 24H2 : fin de support le 13 oct. 2026, passer en 25H2 (🔴 après cette date). 🔴 Windows 11 23H2 ou plus ancien. 🔴 Windows 10 : fin de support le 14 oct. 2025 (🟠 seulement si inscrit aux mises à jour de sécurité étendues « ESU », jusqu'au 12 oct. 2027) ; noter la compatibilité Windows 11 (application « Contrôle d'intégrité du PC »). -->
  - reco haute: Remplacer ce poste (non compatible Windows 11)
- [~] PC3-maj Mises à jour Windows :: Dernière installation le 14/10/2025
  <!-- Paramètres › Windows Update : rien en attente ni en échec ; Historique des mises à jour : dernière installation < 30 jours. Redémarré récemment : Gestionnaire des tâches › Performance › « Temps d'activité » (🟠 si > 14 jours). -->
- [x] PC3-antivirus Antivirus :: Microsoft Defender à jour
  <!-- Sécurité Windows › Protection contre les virus et menaces : protection en temps réel activée, informations de sécurité < 3 jours, aucune menace. Un seul antivirus (pas d'essai McAfee/Norton expiré). -->
- [x] PC3-parefeu Pare-feu ::
  <!-- Sécurité Windows › Pare-feu et protection du réseau : activé sur les 3 profils (domaine, privé, public). -->
- [~] PC3-chiffrement Chiffrement du disque :: Non chiffré
  <!-- Paramètres › Confidentialité et sécurité › Chiffrement de l'appareil (édition Famille) ou BitLocker (Pro) ; ou invite de commandes administrateur : manage-bde -status. Clé de récupération conservée en lieu sûr (ne pas la noter ici). Désactivé : 🔴 sur un portable, 🟠 sur un poste fixe. -->
- [!] PC3-comptes Comptes utilisateurs :: Compte sans mot de passe
  <!-- Invite de commandes : net user, puis net localgroup Administrateurs (« Administrators » sur un Windows anglais). Chaque personne a son compte protégé (mot de passe ou code PIN) ; compte du quotidien administrateur = 🟠 ; compte sans mot de passe = 🔴. -->
  - reco haute: Protéger le compte par un code PIN
- [x] PC3-verrouillage Verrouillage automatique :: 10 min
  <!-- Paramètres › Comptes › Options de connexion, et Système › Alimentation (mise en veille de l'écran) : verrouillage ≤ 10 min. Réflexe Windows + L en quittant le poste. -->
- [~] PC3-espace Espace disque libre (C:) :: 12 %
  <!-- Explorateur › Ce PC. Noter le % libre. 🟢 ≥ 20 % · 🟠 10–20 % · 🔴 < 10 %. -->
- [~] PC3-disque Santé du disque :: HDD sain (disque mécanique)
  <!-- PowerShell : Get-PhysicalDisk | Format-Table FriendlyName, MediaType, HealthStatus → « Healthy ». Disque système mécanique (HDD) = 🟠, recommander un SSD. Noter par ex. « SSD sain ». -->
- [~] PC3-stabilite Stabilité (indice /10) :: 4,6/10 :: 5 arrêts inattendus en juin
  <!-- Touche Windows › perfmon /rel (Moniteur de fiabilité). Noter l'indice, par ex. « 8,5/10 ». 🟢 ≥ 7 sans plantages répétés ni arrêts inattendus sur 30 jours · 🟠 4–7 · 🔴 < 4. -->
- [~] PC3-demarrage Temps de démarrage :: 165 s
  <!-- Chronomètre : bouton marche → bureau utilisable ; noter en secondes. 🟢 < 90 s · 🟠 90–180 s · 🔴 > 180 s. Gestionnaire des tâches au repos : processeur < 20 %, mémoire < 80 % ; onglet « Applications de démarrage » : peu d'impact « élevé ». -->
- [x] PC3-logiciels Logiciels à jour et licenciés :: Microsoft 365 à jour
  <!-- Paramètres › Applications. 🔴 Office 2016/2019 (fin de support 14 oct. 2025). 🟠 Office 2021 (fin de support 13 oct. 2026, 🔴 ensuite). 🟢 Microsoft 365 ou Office 2024. Lecteur PDF et navigateur à jour ; pas de logiciel piraté ni d'« optimiseur de PC ». -->
- [!] PC3-distance Accès à distance :: AnyDesk installé, usage inconnu
  <!-- Paramètres › Applications : TeamViewer, AnyDesk, etc. Aucun, ou connu, justifié et protégé. Outil inconnu ou inutilisé = 🔴 (à désinstaller). -->
  - reco haute: Désinstaller AnyDesk s'il n'est pas utilisé
- [x] PC3-usages Test des usages quotidiens :: Scanner lent mais fonctionnel
  <!-- Ouvrir le logiciel métier, imprimer, numériser, envoyer et recevoir un courriel, ouvrir un site : tout fonctionne. -->
- [~] PC3-internet Internet depuis ce poste :: ↓35 ↑18 Mb/s · 30 ms · Wi-Fi 55 %
  <!-- fast.com ou speedtest.net, puis invite de commandes : netsh wlan show interfaces (ligne « Signal »). Noter par ex. « ↓85 ↑20 Mb/s · 12 ms · Wi-Fi 78 % » ou « câble ». Signal Wi-Fi 🟢 ≥ 70 % · 🟠 50–70 % · 🔴 < 50 %. -->
  - reco basse: Relier ce poste à la box par câble
- [~] PC3-etat État physique :: Ventilateur bruyant, poussière
  <!-- Grilles propres, ventilateurs silencieux ; écran, clavier, souris et ports en bon état. -->

## Sauvegardes et données (SAV)

### Fiche

- Emplacement des dossiers clients : Dossier partagé sur le Bureau 1
- Outil de sauvegarde : Historique des fichiers Windows
- Support(s) de sauvegarde : Disque USB 1 To
- Fréquence prévue : Toutes les heures (automatique)
- Messagerie professionnelle (fournisseur) : Messagerie en ligne (exemple)

### Contrôles

- [x] SAV-cartographie Emplacement des données connu :: Dossier partagé sur le Bureau 1 + documents du portable
  <!-- On sait où se trouvent les dossiers clients, les actes, les numérisations et la base du logiciel métier (quel poste, quel dossier, quel cloud). Aucun nom de client ici. -->
- [~] SAV-existe Sauvegarde en place :: Bureau 1 seulement :: portable et Bureau 2 non sauvegardés
  <!-- Chaque poste qui contient des données importantes est sauvegardé (Historique des fichiers, OneDrive, disque externe, NAS…). -->
  - reco haute: Étendre la sauvegarde au portable et au Bureau 2
- [x] SAV-auto Sauvegarde automatique :: Historique des fichiers, toutes les heures
  <!-- Se déclenche sans intervention humaine. Sauvegarde « quand on y pense » = 🔴. -->
- [!] SAV-recente Dernière sauvegarde réussie :: 12/05/2026 :: disque de sauvegarde plein
  <!-- Noter la date. 🟢 ≤ 7 jours · 🟠 8–30 jours · 🔴 > 30 jours ou inconnue. -->
  - reco haute: Libérer le disque de sauvegarde et relancer la sauvegarde
- [!] SAV-horssite Copie hors du cabinet :: Aucune copie hors du cabinet
  <!-- Une copie hors des locaux (cloud, ou disque emporté) : protège contre l'incendie, le vol, les dégâts des eaux. -->
  - reco haute: Ajouter une sauvegarde cloud chiffrée ou un second disque emporté chaque semaine
- [!] SAV-rancongiciel Copie protégée contre les rançongiciels :: Disque USB branché en permanence
  <!-- Une copie déconnectée (disque débranché après la sauvegarde) ou versionnée (historique des versions du cloud). Seulement un disque branché en permanence = 🔴. -->
  - reco haute: Alterner deux disques et débrancher le disque après chaque sauvegarde
- [!] SAV-restauration Test de restauration :: Échec : disque de sauvegarde plein
  <!-- Restaurer un vrai fichier dans un dossier temporaire et l'ouvrir. Noter le type de fichier (pas le nom du client) et la durée. C'est la seule preuve que la sauvegarde fonctionne. -->
  - reco haute: Refaire un test de restauration après correction
- [~] SAV-logiciel Données du logiciel métier sauvegardées :: Base du logiciel métier hors sauvegarde
  <!-- La base de données ou le dossier de données du logiciel métier fait partie de la sauvegarde. -->
  - reco haute: Ajouter le dossier de données du logiciel métier à la sauvegarde
- [~] SAV-comptes Comptes en ligne protégés :: Double authentification désactivée sur la messagerie
  <!-- Messagerie et comptes importants : double authentification activée, téléphone et courriel de récupération à jour, aucun mot de passe partagé ou réutilisé. -->
  - reco haute: Activer la double authentification sur la messagerie

## Notes

<!-- PRIVÉ : jamais copié dans le rapport. À vérifier la prochaine fois, idées, questions. -->
