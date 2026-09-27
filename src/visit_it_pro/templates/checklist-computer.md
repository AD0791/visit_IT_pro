## Poste {N} — {NAME} ({ID})

### Fiche

- Utilisateur(s) :
- Marque et modèle :
- Numéro de série :
- Windows (édition et version) :
- Processeur / mémoire (RAM) :
- Disque système (SSD ou HDD, capacité) :
- Année d'achat / garantie :
- Suite bureautique (version) :
- Logiciel métier :
- Antivirus :

<!-- Numéro de série : étiquette sous l'appareil, ou PowerShell : Get-CimInstance Win32_BIOS | Select-Object SerialNumber. Windows : touche Windows › winver. Matériel : Paramètres › Système › Informations système ; SSD ou HDD : Gestionnaire des tâches › Performance. -->

### Contrôles

- [ ] {ID}-windows Version de Windows ::
  <!-- winver. 🟢 Windows 11 25H2 ou plus récent (support jusqu'au 13 oct. 2027). 🟠 Windows 11 24H2 : fin de support le 13 oct. 2026, passer en 25H2 (🔴 après cette date). 🔴 Windows 11 23H2 ou plus ancien. 🔴 Windows 10 : fin de support le 14 oct. 2025 (🟠 seulement si inscrit aux mises à jour de sécurité étendues « ESU », jusqu'au 12 oct. 2027) ; noter la compatibilité Windows 11 (application « Contrôle d'intégrité du PC »). -->
- [ ] {ID}-maj Mises à jour Windows ::
  <!-- Paramètres › Windows Update : rien en attente ni en échec ; Historique des mises à jour : dernière installation < 30 jours. Redémarré récemment : Gestionnaire des tâches › Performance › « Temps d'activité » (🟠 si > 14 jours). -->
- [ ] {ID}-antivirus Antivirus ::
  <!-- Sécurité Windows › Protection contre les virus et menaces : protection en temps réel activée, informations de sécurité < 3 jours, aucune menace. Un seul antivirus (pas d'essai McAfee/Norton expiré). -->
- [ ] {ID}-parefeu Pare-feu ::
  <!-- Sécurité Windows › Pare-feu et protection du réseau : activé sur les 3 profils (domaine, privé, public). -->
- [ ] {ID}-chiffrement Chiffrement du disque ::
  <!-- Paramètres › Confidentialité et sécurité › Chiffrement de l'appareil (édition Famille) ou BitLocker (Pro) ; ou invite de commandes administrateur : manage-bde -status. Clé de récupération conservée en lieu sûr (ne pas la noter ici). Désactivé : 🔴 sur un portable, 🟠 sur un poste fixe. -->
- [ ] {ID}-comptes Comptes utilisateurs ::
  <!-- Invite de commandes : net user, puis net localgroup Administrateurs (« Administrators » sur un Windows anglais). Chaque personne a son compte protégé (mot de passe ou code PIN) ; compte du quotidien administrateur = 🟠 ; compte sans mot de passe = 🔴. -->
- [ ] {ID}-verrouillage Verrouillage automatique ::
  <!-- Paramètres › Comptes › Options de connexion, et Système › Alimentation (mise en veille de l'écran) : verrouillage ≤ 10 min. Réflexe Windows + L en quittant le poste. -->
- [ ] {ID}-espace Espace disque libre (C:) ::
  <!-- Explorateur › Ce PC. Noter le % libre. 🟢 ≥ 20 % · 🟠 10–20 % · 🔴 < 10 %. -->
- [ ] {ID}-disque Santé du disque ::
  <!-- PowerShell : Get-PhysicalDisk | Format-Table FriendlyName, MediaType, HealthStatus → « Healthy ». Disque système mécanique (HDD) = 🟠, recommander un SSD. Noter par ex. « SSD sain ». -->
- [ ] {ID}-stabilite Stabilité (indice /10) ::
  <!-- Touche Windows › perfmon /rel (Moniteur de fiabilité). Noter l'indice, par ex. « 8,5/10 ». 🟢 ≥ 7 sans plantages répétés ni arrêts inattendus sur 30 jours · 🟠 4–7 · 🔴 < 4. -->
- [ ] {ID}-demarrage Temps de démarrage ::
  <!-- Chronomètre : bouton marche → bureau utilisable ; noter en secondes. 🟢 < 90 s · 🟠 90–180 s · 🔴 > 180 s. Gestionnaire des tâches au repos : processeur < 20 %, mémoire < 80 % ; onglet « Applications de démarrage » : peu d'impact « élevé ». -->
- [ ] {ID}-logiciels Logiciels à jour et licenciés ::
  <!-- Paramètres › Applications. 🔴 Office 2016/2019 (fin de support 14 oct. 2025). 🟠 Office 2021 (fin de support 13 oct. 2026, 🔴 ensuite). 🟢 Microsoft 365 ou Office 2024. Lecteur PDF et navigateur à jour ; pas de logiciel piraté ni d'« optimiseur de PC ». -->
- [ ] {ID}-distance Accès à distance ::
  <!-- Paramètres › Applications : TeamViewer, AnyDesk, etc. Aucun, ou connu, justifié et protégé. Outil inconnu ou inutilisé = 🔴 (à désinstaller). -->
- [ ] {ID}-usages Test des usages quotidiens ::
  <!-- Ouvrir le logiciel métier, imprimer, numériser, envoyer et recevoir un courriel, ouvrir un site : tout fonctionne. -->
- [ ] {ID}-internet Internet depuis ce poste ::
  <!-- fast.com ou speedtest.net, puis invite de commandes : netsh wlan show interfaces (ligne « Signal »). Noter par ex. « ↓85 ↑20 Mb/s · 12 ms · Wi-Fi 78 % » ou « câble ». Signal Wi-Fi 🟢 ≥ 70 % · 🟠 50–70 % · 🔴 < 50 %. -->
- [ ] {ID}-etat État physique ::
  <!-- Grilles propres, ventilateurs silencieux ; écran, clavier, souris et ports en bon état. -->
<!-- if laptop -->
- [ ] {ID}-batterie Batterie ::
  <!-- Invite de commandes : powercfg /batteryreport, puis ouvrir le fichier battery-report.html indiqué : capacité de charge complète ÷ capacité de conception. Noter le %. 🟢 ≥ 80 % · 🟠 60–80 % · 🔴 < 60 %. Chargeur et câble en bon état. -->
<!-- endif -->

