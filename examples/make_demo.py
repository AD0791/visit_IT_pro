"""Regenerate the two filled checklists of the demo workspace (fictional data).

    uv run python examples/make_demo.py

Run it after changing the templates: the tests and the README screenshots use these files.
The October visit deliberately keeps one unchecked item (NET-secours), one 🔴 without a
recommendation (PC3-distance) and a private remark in the interview ("neveu") that must never
reach the report.
"""

from __future__ import annotations

import re
from pathlib import Path

from visit_it_pro.checklist import build_checklist
from visit_it_pro.config import load_workspace

DEMO = Path(__file__).parent / "demo"

# Checkpoint ID -> (code, value, note, lines under the item)
OCTOBER = {
    "BUR-onduleur": (
        "~",
        "Bureau 1 seulement",
        "box et Bureau 2 sans onduleur",
        ["reco haute: Ajouter un onduleur pour le Bureau 2 et la box Internet"],
    ),
    "BUR-surtension": (
        "!",
        "Multiprises simples en cascade sous le Bureau 2",
        "",
        ["reco haute: Remplacer par une multiprise parafoudre unique"],
    ),
    "BUR-ventilation": (
        "~",
        "Unité centrale du Bureau 2 posée au sol",
        "",
        ["fait: Grilles d'aération dépoussiérées", "reco basse: Surélever l'unité centrale (support ou meuble)"],
    ),
    "BUR-cablage": ("x", "", "", []),
    "BUR-confidentialite": (
        "~",
        "Écran du Bureau 1 visible depuis l'accueil",
        "",
        ["reco moyenne: Réorienter l'écran ou poser un filtre de confidentialité"],
    ),
    "BUR-portable": ("x", "Rangé dans l'armoire fermée à clé le soir", "", []),
    "BUR-impression": ("x", "Page et numérisation de test OK depuis les 3 postes", "", []),
    "NET-box": ("x", "Ventilée, voyants normaux", "", []),
    "NET-admin": (
        "x",
        "Changé pendant la visite",
        "",
        ["fait: Mot de passe d'usine remplacé ; nouveau mot de passe remis à la responsable sous enveloppe"],
    ),
    "NET-firmware": (
        "~",
        "Version de 2024, mise à jour automatique désactivée",
        "",
        ["reco moyenne: Mettre à jour le micrologiciel en dehors des heures d'ouverture"],
    ),
    "NET-wifi": ("x", "WPA2, clé longue", "", ["fait: WPS désactivé"]),
    "NET-invites": (
        "!",
        "Les clients utilisent le Wi-Fi du cabinet",
        "",
        ["reco haute: Créer un réseau Wi-Fi invités séparé et changer la clé du Wi-Fi du cabinet"],
    ),
    "NET-appareils": ("x", "7 appareils, tous identifiés", "", []),
    "NET-debit": ("x", "88 Mb/s sur le meilleur poste (88 %)", "", []),
    "NET-stabilite": ("x", "0 % de perte, 14 ms", "", []),
    "NET-coupures": (
        "~",
        "2 coupures ressenties en septembre",
        "",
        ["reco basse: Noter la date et la durée des prochaines coupures pour les signaler au fournisseur"],
    ),
    # NET-secours deliberately left unchecked.
    "PC1-windows": ("~", "Windows 11 Pro 24H2", "", ["reco haute: Installer Windows 11 25H2 avant le 13 octobre 2026"]),
    "PC1-maj": ("x", "Dernière installation le 12/09/2026", "", []),
    "PC1-antivirus": ("x", "Microsoft Defender à jour", "", []),
    "PC1-parefeu": ("x", "", "", []),
    "PC1-chiffrement": (
        "!",
        "Désactivé",
        "portable emporté chaque soir",
        ["reco haute: Activer BitLocker et conserver la clé de récupération en lieu sûr"],
    ),
    "PC1-comptes": (
        "~",
        "Compte unique, administrateur",
        "",
        ["reco moyenne: Créer un compte standard pour l'usage quotidien"],
    ),
    "PC1-verrouillage": ("x", "5 min", "", []),
    "PC1-espace": ("x", "62 %", "", []),
    "PC1-disque": ("x", "SSD sain", "", []),
    "PC1-stabilite": ("x", "8,7/10", "", []),
    "PC1-demarrage": ("x", "38 s", "", []),
    "PC1-logiciels": ("x", "Microsoft 365 à jour", "", []),
    "PC1-distance": ("x", "Aucun", "", []),
    "PC1-usages": ("x", "", "", []),
    "PC1-internet": ("x", "↓88 ↑45 Mb/s · 12 ms · Wi-Fi 81 %", "", []),
    "PC1-etat": ("x", "", "", []),
    "PC1-batterie": ("~", "71 %", "", ["reco basse: Prévoir le remplacement de la batterie en 2027"]),
    "PC2-windows": ("x", "Windows 11 Pro 25H2", "", []),
    "PC2-maj": (
        "x",
        "À jour après redémarrage",
        "",
        ["fait: Redémarrage : mises à jour en attente depuis 19 jours installées"],
    ),
    "PC2-antivirus": ("x", "Microsoft Defender à jour", "", []),
    "PC2-parefeu": ("x", "", "", []),
    "PC2-chiffrement": ("~", "Non chiffré", "", ["reco moyenne: Activer BitLocker"]),
    "PC2-comptes": ("x", "", "", []),
    "PC2-verrouillage": ("x", "10 min", "", ["fait: Verrouillage automatique réglé sur 10 min (était désactivé)"]),
    "PC2-espace": (
        "~",
        "17 %",
        "",
        [
            "fait: Nettoyage de disque : 9 Go libérés",
            "reco moyenne: Archiver les anciennes numérisations sur un disque externe",
        ],
    ),
    "PC2-disque": ("x", "SSD sain", "", []),
    "PC2-stabilite": ("x", "7,9/10", "", []),
    "PC2-demarrage": ("x", "52 s", "", []),
    "PC2-logiciels": (
        "!",
        "Office 2019",
        "fin de support le 14 oct. 2025",
        ["reco haute: Passer à Microsoft 365 ou Office 2024"],
    ),
    "PC2-distance": ("x", "Aucun", "", []),
    "PC2-usages": ("x", "", "", []),
    "PC2-internet": ("x", "câble · ↓94 ↑48 Mb/s · 9 ms", "", []),
    "PC2-etat": ("x", "", "", []),
    "PC3-windows": (
        "!",
        "Windows 10 Pro 22H2, non inscrit à l'ESU",
        "processeur non compatible Windows 11",
        ["reco haute: Remplacer ce poste (non compatible Windows 11)"],
    ),
    "PC3-maj": ("~", "Dernière installation le 14/10/2025", "", []),
    "PC3-antivirus": ("x", "Microsoft Defender à jour", "", []),
    "PC3-parefeu": ("x", "", "", []),
    "PC3-chiffrement": ("~", "Non chiffré", "", []),
    "PC3-comptes": (
        "x",
        "Code PIN créé",
        "",
        ["fait: Code PIN créé avec l'utilisatrice (le compte n'avait pas de mot de passe)"],
    ),
    "PC3-verrouillage": ("x", "10 min", "", []),
    "PC3-espace": ("~", "14 %", "", []),
    "PC3-disque": ("~", "HDD sain (disque mécanique)", "", []),
    "PC3-stabilite": ("~", "5,2/10", "3 arrêts inattendus en septembre", []),
    "PC3-demarrage": ("~", "150 s", "", []),
    "PC3-logiciels": ("x", "Microsoft 365 à jour", "", []),
    # 🔴 without a recommendation on purpose.
    "PC3-distance": ("!", "AnyDesk installé, usage inconnu", "", []),
    "PC3-usages": ("x", "Scanner lent mais fonctionnel", "", []),
    "PC3-internet": ("~", "↓41 ↑22 Mb/s · 25 ms · Wi-Fi 58 %", "", ["reco basse: Relier ce poste à la box par câble"]),
    "PC3-etat": ("~", "Ventilateur bruyant, poussière", "", ["fait: Dépoussiérage", "photo: photos/PC3-poussiere.png"]),
    "SAV-cartographie": ("x", "Dossier partagé sur le Bureau 1 + documents du portable", "", []),
    "SAV-existe": (
        "~",
        "Bureau 1 seulement",
        "portable et Bureau 2 non sauvegardés",
        ["reco haute: Étendre la sauvegarde au portable et au Bureau 2"],
    ),
    "SAV-auto": ("x", "Historique des fichiers, toutes les heures", "", []),
    "SAV-recente": ("x", "01/10/2026", "", []),
    "SAV-horssite": (
        "!",
        "Aucune copie hors du cabinet",
        "",
        ["reco haute: Ajouter une sauvegarde cloud chiffrée ou un second disque emporté chaque semaine"],
    ),
    "SAV-rancongiciel": (
        "!",
        "Disque USB branché en permanence",
        "",
        ["reco haute: Alterner deux disques et débrancher le disque après chaque sauvegarde"],
    ),
    "SAV-restauration": ("x", "Document Word restauré et ouvert en 2 min", "", []),
    "SAV-logiciel": (
        "~",
        "Base du logiciel métier hors sauvegarde",
        "",
        ["reco haute: Ajouter le dossier de données du logiciel métier à la sauvegarde"],
    ),
    "SAV-comptes": (
        "~",
        "Double authentification désactivée sur la messagerie",
        "",
        ["reco haute: Activer la double authentification sur la messagerie"],
    ),
}

# The first (baseline) visit: worse on several points that were fixed by October.
JULY = {
    **OCTOBER,
    "BUR-ventilation": (
        "!",
        "Unité centrale du Bureau 2 posée au sol, grilles bouchées",
        "",
        ["reco moyenne: Dépoussiérer et surélever l'unité centrale"],
    ),
    "NET-admin": (
        "!",
        "Mot de passe d'usine (étiquette de la box)",
        "",
        ["reco haute: Changer le mot de passe d'administration de la box"],
    ),
    "NET-wifi": ("~", "WPA2, clé longue, WPS activé", "", ["reco moyenne: Désactiver le WPS"]),
    "NET-debit": ("~", "61 Mb/s sur le meilleur poste (61 %)", "", []),
    "NET-stabilite": ("~", "1 % de perte, 22 ms", "", []),
    "NET-coupures": (
        "!",
        "Coupures presque quotidiennes en juin",
        "",
        ["reco haute: Signaler les coupures au fournisseur avec leurs dates et durées"],
    ),
    "NET-secours": ("x", "Partage de connexion testé sur le portable", "", []),
    "PC1-maj": ("x", "Dernière installation le 11/06/2026", "", []),
    "PC1-espace": ("x", "55 %", "", []),
    "PC1-stabilite": ("x", "8,1/10", "", []),
    "PC1-demarrage": ("x", "41 s", "", []),
    "PC1-internet": ("x", "↓63 ↑30 Mb/s · 18 ms · Wi-Fi 79 %", "", []),
    "PC1-batterie": ("~", "74 %", "", ["reco basse: Surveiller l'usure de la batterie"]),
    "PC2-maj": (
        "!",
        "Mises à jour en échec depuis mai",
        "",
        ["reco haute: Réparer Windows Update et installer les mises à jour"],
    ),
    "PC2-verrouillage": ("!", "Jamais", "", ["reco haute: Régler le verrouillage automatique sur 10 min"]),
    "PC2-espace": ("!", "11 %", "", ["reco haute: Libérer de l'espace disque"]),
    "PC2-stabilite": ("~", "6,8/10", "", []),
    "PC2-demarrage": ("x", "58 s", "", []),
    "PC2-internet": ("x", "câble · ↓66 ↑31 Mb/s · 11 ms", "", []),
    "PC3-comptes": ("!", "Compte sans mot de passe", "", ["reco haute: Protéger le compte par un code PIN"]),
    "PC3-espace": ("~", "12 %", "", []),
    "PC3-stabilite": ("~", "4,6/10", "5 arrêts inattendus en juin", []),
    "PC3-demarrage": ("~", "165 s", "", []),
    "PC3-distance": (
        "!",
        "AnyDesk installé, usage inconnu",
        "",
        ["reco haute: Désinstaller AnyDesk s'il n'est pas utilisé"],
    ),
    "PC3-internet": ("~", "↓35 ↑18 Mb/s · 30 ms · Wi-Fi 55 %", "", ["reco basse: Relier ce poste à la box par câble"]),
    "PC3-etat": ("~", "Ventilateur bruyant, poussière", "", []),
    "SAV-recente": (
        "!",
        "12/05/2026",
        "disque de sauvegarde plein",
        ["reco haute: Libérer le disque de sauvegarde et relancer la sauvegarde"],
    ),
    "SAV-restauration": (
        "!",
        "Échec : disque de sauvegarde plein",
        "",
        ["reco haute: Refaire un test de restauration après correction"],
    ),
}

FICHE = {
    "Onduleur(s) (marque, modèle, âge)": "1 onduleur 700 VA (2023) sur le Bureau 1",
    "Imprimante / scanner (marque, modèle)": "Multifonction laser réseau (exemple)",
    "Fournisseur d'accès": "Fournisseur X (exemple)",
    "Offre / technologie (fibre, ADSL, 4G, satellite…)": "Fibre",
    "Débit contractuel (descendant / montant)": "100 / 50 Mb/s",
    "Titulaire du contrat": "Le cabinet",
    "Box / routeur (marque, modèle)": "Box du fournisseur (exemple)",
    "Emplacement des dossiers clients": "Dossier partagé sur le Bureau 1",
    "Outil de sauvegarde": "Historique des fichiers Windows",
    "Support(s) de sauvegarde": "Disque USB 1 To",
    "Fréquence prévue": "Toutes les heures (automatique)",
    "Messagerie professionnelle (fournisseur)": "Messagerie en ligne (exemple)",
}
COMPUTER_FICHE = {  # values in the order of the computer template's "Fiche" lines
    "PC1": [
        "Responsable du cabinet",
        "Portable 14 pouces (exemple)",
        "EXEMPLE-PC1",
        "Windows 11 Pro 24H2",
        "Core i5 / 16 Go",
        "SSD 512 Go",
        "2022",
        "Microsoft 365",
        "Logiciel notarial (exemple)",
        "Microsoft Defender",
    ],
    "PC2": [
        "Secrétariat",
        "Tour de bureau (exemple)",
        "EXEMPLE-PC2",
        "Windows 11 Pro 25H2",
        "Core i5 / 8 Go",
        "SSD 256 Go",
        "2021",
        "Office 2019",
        "Logiciel notarial (exemple)",
        "Microsoft Defender",
    ],
    "PC3": [
        "Assistante",
        "Tour de bureau ancienne (exemple)",
        "EXEMPLE-PC3",
        "Windows 10 Pro 22H2",
        "Core i3 6e génération / 8 Go",
        "HDD 1 To",
        "2016",
        "Microsoft 365",
        "Logiciel notarial (exemple)",
        "Microsoft Defender",
    ],
}

ADMIN_QUESTION = "- Autres intervenants informatiques ; qui connaît les mots de passe administrateur :"

VISITS = {
    "2026-07-03": {
        "items": JULY,
        "meta": {
            "presents": "Responsable du cabinet, secrétariat",
            "arrivee": "9 h 30",
            "depart": "12 h 15",
            "prochaine_visite": "2026-10-02",
        },
        "summary": (
            "Première visite de référence. Les postes fonctionnent, mais la sauvegarde est en échec "
            "depuis mai (disque plein) et aucune restauration n'a pu être testée. Priorités : rétablir la "
            "sauvegarde, sécuriser la box (mot de passe d'usine) et remettre en ordre le Bureau 1 "
            "(mises à jour en échec, disque presque plein, écran jamais verrouillé)."
        ),
        "interview": {},
    },
    "2026-10-02": {
        "items": OCTOBER,
        "meta": {
            "presents": "Responsable du cabinet, secrétariat",
            "arrivee": "9 h 00",
            "depart": "11 h 40",
            "prochaine_visite": "2026-11-06",
        },
        "summary": (
            "Les trois postes et la connexion Internet fonctionnent correctement au quotidien, et la "
            "sauvegarde du Bureau 1 a été testée avec succès. Trois priorités ressortent : protéger les "
            "données (sauvegarde du portable et du Bureau 2, copie hors du cabinet, chiffrement du portable), "
            "remplacer le Bureau 2 qui n'est plus mis à jour par Microsoft, et séparer le Wi-Fi des clients "
            "de celui du cabinet. Plusieurs corrections ont été faites sur place, dont le changement du mot "
            "de passe de la box et le verrouillage automatique des écrans."
        ),
        "interview": {ADMIN_QUESTION: "Le neveu de la secrétaire intervient parfois à distance sur le Bureau 2."},
    },
}

ITEM_RE = re.compile(r"^- \[ \] (\S+) (.*?) ::$")
FICHE_RE = re.compile(r"^- (.+?) :$")
COMPUTER_RE = re.compile(r"^## Poste \d+ — .* \((\w+)\)$")


def fill(text: str, items: dict, meta: dict, summary: str, interview: dict) -> str:
    lines, out = text.split("\n"), []
    computer, fiche_index, i = None, 0, 0
    while i < len(lines):
        line = lines[i]
        if m := COMPUTER_RE.match(line):
            computer, fiche_index = m.group(1), 0
        elif line.startswith("## "):
            computer = None
        if (m := ITEM_RE.match(line)) and m.group(1) in items:
            code, value, note, subs = items[m.group(1)]
            tail = " :: ".join(p for p in (value, note) if p)
            out.append(f"- [{code}] {m.group(1)} {m.group(2)} ::" + (f" {tail}" if tail else ""))
            if i + 1 < len(lines) and lines[i + 1].lstrip().startswith("<!--"):
                out.append(lines[i + 1])
                i += 1
            out += [f"  - {sub}" for sub in subs]
            i += 1
            continue
        if line in interview:
            line = f"{line} {interview[line]}"
        elif m := FICHE_RE.match(line):
            if computer:
                line = f"- {m.group(1)} : {COMPUTER_FICHE[computer][fiche_index]}"
                fiche_index += 1
            elif m.group(1) in FICHE:
                line = f"- {m.group(1)} : {FICHE[m.group(1)]}"
        out.append(line)
        i += 1
    text = "\n".join(out)
    for key, value in meta.items():
        text = re.sub(rf"^{key}:\s*$", f"{key}: {value}", text, count=1, flags=re.M)
    return text.replace(
        "Copié tel quel dans le rapport. -->\n\n", f"Copié tel quel dans le rapport. -->\n\n{summary}\n\n", 1
    )


def main() -> None:
    ws = load_workspace(DEMO)
    for date, visit in VISITS.items():
        folder = ws.visits_dir / date
        (folder / "photos").mkdir(parents=True, exist_ok=True)
        text = fill(build_checklist(ws, date), visit["items"], visit["meta"], visit["summary"], visit["interview"])
        (folder / "checklist.md").write_text(text, encoding="utf-8")
        print(f"wrote {folder / 'checklist.md'}")


if __name__ == "__main__":
    main()
