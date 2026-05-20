<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0e0e0c,50:1a1a17,100:2c2c28&height=140&section=header" />

<div align="center">

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Inter&weight=700&size=26&pause=1000&color=F0EEE6&center=true&vCenter=true&width=700&lines=AccessiAdapt;Interface+Adaptative+%26+Accessible;HTML+%2B+CSS+%2B+JavaScript+%2B+Python;L%27interface+s%27adapte+%C3%A0+l%27utilisateur)](https://github.com/lovasoarm)

<br/>

![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Python](https://img.shields.io/badge/Python_3-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-FF6F00?style=for-the-badge&logo=python&logoColor=white)

</div>

---

## C'est quoi

AccessiAdapt est un prototype logiciel qui s'adapte automatiquement à l'utilisateur selon son type de handicap.

L'idée : les interfaces classiques supposent un utilisateur standard. AccessiAdapt fait l'inverse, l'interface s'adapte à l'utilisateur selon son profil d'accessibilité.

Quatre profils couverts : **visuel**, **moteur**, **auditif**, **cognitif**. Un mode standard pour les combinaisons.

---

## Structure du projet

```
AccessiAdapt/
├── assets/                    # Logo et favicon
├── prototype/
│   ├── pages/                 # Pages HTML par mode
│   │   ├── index.html         # Écran de sélection
│   │   ├── mode_visuel.html
│   │   ├── mode_moteur.html
│   │   ├── mode_auditif.html
│   │   ├── mode_cognitif.html
│   │   └── mode_standard.html
│   ├── styles/                # CSS par mode + global
│   │   ├── global.css
│   │   └── mode_*.css
│   └── scripts/               # JavaScript
│       ├── app.js             # Routage et sélection
│       ├── adapter.js         # Logique d'adaptation
│       └── mode_*.js
└── src/                       # Version Python (Tkinter)
    ├── main.py
    ├── profile.py
    ├── adapter.py
    ├── ui/
    ├── modules/               # Scanner, speech, analytics
    └── ai/                    # Classifieur sklearn
```

---

## Lancer le prototype

### Version web

Ouvrir directement `prototype/pages/index.html` dans un navigateur.

Aucun serveur nécessaire.

### Version Python

```bash
cd src
pip install pyttsx3 scikit-learn
python main.py
```

---

## Les profils

| Profil   | Code | Ce que ça fait                                                                      |
| -------- | ---- | ----------------------------------------------------------------------------------- |
| Visuel   | `v`  | Fond noir / texte blanc, grande police, navigation clavier, barre TTS               |
| Moteur   | `m`  | Balayage automatique, bouton Valider unique, support barre espace, vitesse réglable |
| Auditif  | `a`  | Zéro dépendance audio, notifications visuelles, barre de description                |
| Cognitif | `c`  | Interface épurée, pictogrammes, guide contextuel, max 4 actions                     |
| Standard | `s`  | Mode combiné, applique les adaptations compatibles                                  |

En cas de sélection multiple : **Moteur > Visuel > Cognitif > Auditif**. Si deux profils ou plus sont sélectionnés → mode standard automatiquement.

---

## Comment ça marche

**Sélection** : `index.html` + `app.js` gèrent le choix du profil et le routage.

**Routage** : `resolveDestination()` retourne l'URL de destination avec les profils en paramètre (`?profiles=v,m`).

**Adaptation** : `adapter.js` lit les paramètres, construit la config, applique les classes CSS sur le `<body>`.

**Rendu** : chaque `mode_*.js` gère les interactions propres à ce mode.

---

## Modules Python spécifiques

- `modules/scanner.py` : balayage automatique des boutons pour le mode moteur
- `modules/speech.py` : synthèse vocale réelle via pyttsx3
- `modules/analytics.py` : journalisation des événements en JSON
- `ai/classifier.py` : classifieur sklearn pour recommandation automatique de mode

---

## Auteur

**Lovasoarm** aka ARAMIS

---

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:2c2c28,50:1a1a17,100:0e0e0c&height=100&section=footer" />
