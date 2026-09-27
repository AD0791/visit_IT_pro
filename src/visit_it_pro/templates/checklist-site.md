---
cabinet: {OFFICE}
date: {DATE}
intervenant: {TECHNICIAN}
presents:
arrivee:
depart:
prochaine_visite:
---

# Visite du {DATE} — {OFFICE}

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
Avancement : visit-it-pro check {DATE}      Rapport : visit-it-pro report {DATE}
-->

## Synthèse

<!-- À rédiger en fin de visite : 4 à 5 phrases simples pour le/la responsable (état général, points forts, 2 ou 3 priorités, ce qui a été fait). Copié tel quel dans le rapport. -->

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

- Onduleur(s) (marque, modèle, âge) :
- Imprimante / scanner (marque, modèle) :

### Contrôles

- [ ] BUR-onduleur Onduleurs (postes fixes et box) ::
  <!-- Postes fixes et box sur onduleur, autonomie ≥ 5 min. Test en fin de visite (travail enregistré) : débrancher l'onduleur de la prise murale. Batterie d'onduleur à changer tous les 3 à 5 ans. -->
- [ ] BUR-surtension Protection contre les surtensions ::
  <!-- Multiprises parafoudre (pas de simples multiprises) ; aucune multiprise branchée sur une autre. -->
- [ ] BUR-ventilation Ventilation et poussière ::
  <!-- Unités centrales ni enfermées, ni collées au mur, ni posées sur un sol poussiéreux ; grilles d'aération propres. -->
- [ ] BUR-cablage Câblage ::
  <!-- Câbles rangés, sans tension ni pliure ; rien sur le passage. -->
- [ ] BUR-confidentialite Confidentialité aux postes de travail ::
  <!-- Écrans non visibles depuis l'accueil ; aucun mot de passe affiché (post-it, sous le clavier). -->
- [ ] BUR-portable Sécurité physique du portable ::
  <!-- Rangé sous clé ou attaché (câble antivol) en dehors des heures d'ouverture ; jamais laissé dans une voiture. -->
- [ ] BUR-impression Imprimante et scanner ::
  <!-- Page de test et numérisation de test depuis chaque poste concerné ; consommables disponibles. -->

## Internet et réseau (NET)

### Fiche

- Fournisseur d'accès :
- Offre / technologie (fibre, ADSL, 4G, satellite…) :
- Débit contractuel (descendant / montant) :
- Titulaire du contrat :
- Assistance (téléphone, n° client) :
- Box / routeur (marque, modèle) :

### Contrôles

- [ ] NET-box Box / routeur ::
  <!-- Emplacement ventilé, branché sur onduleur, voyants normaux. Demander à quelle fréquence il faut la redémarrer. -->
- [ ] NET-admin Mot de passe d'administration du routeur ::
  <!-- Différent de celui de l'étiquette ; connu du cabinet et conservé en lieu sûr. Ne jamais noter le mot de passe ici. -->
- [ ] NET-firmware Micrologiciel du routeur ::
  <!-- Page d'administration › Système / Mise à jour : version à jour ou mise à jour automatique activée. -->
- [ ] NET-wifi Sécurité du Wi-Fi ::
  <!-- WPA2 ou WPA3 (jamais WEP ni réseau ouvert), clé longue et non devinable, WPS désactivé. -->
- [ ] NET-invites Wi-Fi invités ::
  <!-- Les clients utilisent un réseau invités séparé (ou n'ont pas accès au Wi-Fi). Clients sur le réseau du cabinet = 🔴. -->
- [ ] NET-appareils Appareils connectés ::
  <!-- Liste des appareils dans la page du routeur : tous identifiés. Appareil inconnu = 🔴. -->
- [ ] NET-debit Débit conforme au contrat ::
  <!-- Meilleur poste ≥ 70 % du débit contractuel (voir « Internet depuis ce poste » de chaque poste). 🟢 ≥ 70 % · 🟠 50–70 % · 🔴 < 50 %. -->
- [ ] NET-stabilite Stabilité de la connexion ::
  <!-- Invite de commandes : ping -n 100 8.8.8.8 → perte 🟢 0 % · 🟠 1–2 % · 🔴 > 2 % ; noter aussi la latence moyenne. Refaire vers la box (ipconfig → « Passerelle par défaut ») pour distinguer un problème de Wi-Fi d'un problème de fournisseur. -->
- [ ] NET-coupures Coupures signalées ::
  <!-- Coupures ressenties le mois dernier : aucune 🟢 · occasionnelles 🟠 · fréquentes 🔴. -->
- [ ] NET-secours Solution de secours Internet ::
  <!-- Partage de connexion d'un téléphone testé sur un poste (ou second fournisseur). -->

{COMPUTERS}
## Sauvegardes et données (SAV)

### Fiche

- Emplacement des dossiers clients :
- Outil de sauvegarde :
- Support(s) de sauvegarde :
- Fréquence prévue :
- Messagerie professionnelle (fournisseur) :

### Contrôles

- [ ] SAV-cartographie Emplacement des données connu ::
  <!-- On sait où se trouvent les dossiers clients, les actes, les numérisations et la base du logiciel métier (quel poste, quel dossier, quel cloud). Aucun nom de client ici. -->
- [ ] SAV-existe Sauvegarde en place ::
  <!-- Chaque poste qui contient des données importantes est sauvegardé (Historique des fichiers, OneDrive, disque externe, NAS…). -->
- [ ] SAV-auto Sauvegarde automatique ::
  <!-- Se déclenche sans intervention humaine. Sauvegarde « quand on y pense » = 🔴. -->
- [ ] SAV-recente Dernière sauvegarde réussie ::
  <!-- Noter la date. 🟢 ≤ 7 jours · 🟠 8–30 jours · 🔴 > 30 jours ou inconnue. -->
- [ ] SAV-horssite Copie hors du cabinet ::
  <!-- Une copie hors des locaux (cloud, ou disque emporté) : protège contre l'incendie, le vol, les dégâts des eaux. -->
- [ ] SAV-rancongiciel Copie protégée contre les rançongiciels ::
  <!-- Une copie déconnectée (disque débranché après la sauvegarde) ou versionnée (historique des versions du cloud). Seulement un disque branché en permanence = 🔴. -->
- [ ] SAV-restauration Test de restauration ::
  <!-- Restaurer un vrai fichier dans un dossier temporaire et l'ouvrir. Noter le type de fichier (pas le nom du client) et la durée. C'est la seule preuve que la sauvegarde fonctionne. -->
- [ ] SAV-logiciel Données du logiciel métier sauvegardées ::
  <!-- La base de données ou le dossier de données du logiciel métier fait partie de la sauvegarde. -->
- [ ] SAV-comptes Comptes en ligne protégés ::
  <!-- Messagerie et comptes importants : double authentification activée, téléphone et courriel de récupération à jour, aucun mot de passe partagé ou réutilisé. -->

## Notes

<!-- PRIVÉ : jamais copié dans le rapport. À vérifier la prochaine fois, idées, questions. -->
