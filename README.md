# NoobToRoot_

> Apprends **Python**, le **Shell** et le **HTML**, une commande à la fois.

NoobToRoot est un jeu d'apprentissage au look terminal : une question s'affiche, tu tapes la commande ou le code, et le jeu valide ta réponse. Il tient dans un seul fichier HTML et fonctionne **sans Internet et sans installation**, depuis une clé USB ou en ligne sur GitHub Pages.

```
noob@root:~$ ls -la
✔ Accès accordé. +1
```

---

## Fonctionnalités

- **180 questions** : 60 par langage (Shell, Python, HTML), réparties en 20 faciles, 20 moyennes et 20 difficiles.
- **OldToRoot**, une page cachée de 200 questions sur les langages d'avant : Fortran, COBOL, BASIC, Pascal et MS-DOS.
- **3 niveaux de difficulté** et **3 niveaux d'aide**, réglables séparément.
- **3 modes de chrono**, du jeu tranquille au compte à rebours sans pitié.
- **Coloration syntaxique en direct** pendant la frappe, propre à chaque langage.
- **Correction immédiate** : en cas d'erreur, le jeu affiche la réponse attendue et une explication courte.
- **Saisie tolérante** : espaces en trop, guillemets simples ou doubles et ordre des attributs HTML ne comptent pas comme des erreurs.
- **Records personnels** : `best_score` et `best_time` sont enregistrés dans le navigateur.
- **Révision des erreurs** : en fin de partie, tu peux rejouer uniquement les questions ratées.
- **Banque de questions éditable** dans Excel ou Google Sheets, sans toucher au code.

## Niveau et aide : deux réglages séparés

Le **niveau** règle la difficulté des questions, l'**assist** règle l'aide reçue. Les 9 combinaisons permettent une vraie progression : des bases sans aucune aide pour vérifier qu'on les maîtrise, ou des commandes avancées avec propositions pour les découvrir.

| `--niveau` | Questions |
|---|---|
| **Noob** | 75 % faciles, 25 % moyennes pour tirer vers le haut |
| **Geek** | 75 % moyennes, 25 % difficiles pour tirer vers le haut |
| **Elite** | 100 % difficiles |

| `--assist` | Aide |
|---|---|
| **Pick** | 3 propositions affichées, tu tapes la bonne |
| **Hint** | Un indice pour te mettre sur la piste |
| **Raw** | Saisie brute, comme dans un vrai terminal |

Dans une partie, les questions vont toujours de la plus facile à la plus difficile. Les records sont propres à chaque combinaison de langage, niveau et assist.

## Les modes de chrono

| Mode | Fonctionnement |
|---|---|
| **Chill** | Pas de chrono, prends ton temps. |
| **Serious** | Un chrono qui monte, pour suivre ton temps. |
| **Killer** | Un compte à rebours global : à zéro, la partie s'arrête et les questions restantes comptent comme ratées. |

En mode Killer, le temps alloué dépend du niveau : **30 s par question en Noob, 25 s en Geek, 20 s en Elite**.

Dans les deux modes chronométrés, le temps se met en pause pendant l'affichage des corrections : seul le temps de réflexion et de frappe compte. Le `best_time` n'est enregistré que sur un sans-faute.

## OldToRoot : la salle des archives

Une pierre tombale, en haut à droite de l'accueil, ouvre **OldToRoot**, la page jumelle consacrée aux langages qui ont fait l'informatique. Une icône de terminal ramène à NoobToRoot.

- **200 questions** : 40 par langage (Fortran, COBOL, BASIC, Pascal, MS-DOS).
- **Pas de choix de niveau** : chaque partie mélange 50 % de questions Noob, 25 % de Geek et 25 % d'Elite, de la plus facile à la plus difficile.
- On garde `--assist`, `--questions` et `--chrono`. En mode Killer, 25 s par question.
- Des invites d'époque : `READY.` pour BASIC, `C:\>` pour MS-DOS…
- Saisie insensible à la casse, comme sur les machines de l'époque (sauf le texte entre guillemets).
- Records séparés de ceux de NoobToRoot.

## Jouer

**En local ou sur clé USB** : ouvre `index.html` dans un navigateur, d'un double-clic. Garde `data.js`, `oldtoroot.html` et `data_old.js` dans le même dossier.

**En ligne avec GitHub Pages**

1. Pousse `index.html`, `data.js`, `oldtoroot.html` et `data_old.js` à la racine du dépôt.
2. Va dans **Settings → Pages**.
3. Choisis la branche `main` et le dossier `/ (root)`, puis enregistre.
4. Le jeu est disponible à l'adresse `https://<ton-compte>.github.io/<nom-du-depot>/`.

**Commandes**

- `Entrée` valide la réponse, puis passe à la question suivante.
- Sur téléphone, toucher la zone de correction fait avancer.
- Un clic sur le titre **NoobToRoot** ramène à l'accueil.

## Structure du dépôt

```
.
├── index.html          # NoobToRoot : interface, règles, coloration syntaxique, chrono
├── data.js             # les questions de NoobToRoot
├── oldtoroot.html      # OldToRoot : la page des langages d'avant
├── data_old.js         # les questions d'OldToRoot
├── NoobToRoot.xlsx     # les deux banques, à éditer dans Excel (onglets « questions » et « OldToRoot »)
├── questions.csv       # la banque NoobToRoot, à importer dans Google Sheets
├── questions_old.csv   # la banque OldToRoot, à importer dans Google Sheets
├── csv_vers_data.py    # regénère data.js et data_old.js depuis l'Excel ou les CSV
├── LISEZMOI.txt        # mode d'emploi court, pour la clé USB
└── README.md
```

## Ajouter ou modifier des questions

La banque se gère dans un tableur, une ligne par question.

**Depuis Excel**

```bash
python3 csv_vers_data.py NoobToRoot.xlsx
```

Le script convertit les deux onglets d'un coup : « questions » donne `data.js`, « OldToRoot » donne `data_old.js`.

**Depuis Google Sheets**

1. Importe `questions.csv` (Fichier → Importer).
2. Modifie le tableau, puis exporte-le (Fichier → Télécharger → .csv).
3. Lance la conversion :

```bash
python3 csv_vers_data.py questions.csv        # → data.js
python3 csv_vers_data.py questions_old.csv    # → data_old.js
```

Le script vérifie chaque ligne et signale les erreurs (langage inconnu, difficulté invalide, leurre manquant) avant d'écrire `data.js`. La lecture de l'Excel nécessite `openpyxl` (`pip install openpyxl`).

### Les colonnes

| Colonne | Contenu |
|---|---|
| `id` | Identifiant unique, par exemple `SH-12`, `PY-03`, `HT-40` |
| `langage` | `shell`, `python`, `html` (NoobToRoot) ; `basic`, `msdos`, `cobol`, `pascal`, `fortran` (OldToRoot) |
| `difficulte` | `1` facile, `2` moyen, `3` difficile |
| `question` | La consigne affichée au joueur |
| `reponse1` | La réponse affichée en correction |
| `reponse2` à `reponse6` | Variantes également acceptées (facultatives) |
| `leurre1`, `leurre2` | Les deux mauvaises propositions du mode Pick |
| `indice` | L'aide affichée en mode Hint |
| `explication` | Affichée en cas d'erreur ; le code se met entre `backticks` |

Une réponse qui commence par `re:` est une expression régulière. Par exemple, `re:^#.*` accepte n'importe quel commentaire Python.

### Règles de tolérance

| Langage | Ce qui est ignoré |
|---|---|
| Tous | Espaces en trop, guillemets simples ou doubles |
| Shell | Espaces autour de `\|`, `>`, `>>`, `<`, `;`. La casse compte (`ls` ≠ `LS`), comme dans un vrai terminal. |
| Python | Espaces autour des opérateurs, parenthèses, crochets, virgules et deux-points |
| HTML | Majuscules et minuscules, espaces entre les balises, `<br/>` équivaut à `<br>` |
| Langages d'OldToRoot | Majuscules et minuscules (hors texte entre guillemets), espaces autour de la ponctuation. Le `;` final en Pascal et le `.` final en COBOL sont facultatifs. |

## Technique

- HTML, CSS et JavaScript natifs, sans framework ni dépendance.
- Polices JetBrains Mono et VT323 depuis Google Fonts. Hors ligne, le jeu bascule sur les polices à chasse fixe du système.
- Scores et records stockés dans le `localStorage` du navigateur : rien n'est envoyé nulle part.
- Respecte le réglage système « réduire les animations ».

## Idées pour la suite

- Un choix de 30 questions par partie.
- De nouveaux langages : Git, SQL, CSS… et, dans OldToRoot, Logo, C ou l'assembleur.
- Un mode révision qui reprend les questions les plus souvent ratées.
