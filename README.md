# BRBR Virus — Documentation technique

## Présentation

BRBR Virus est un jeu de simulation de gestion de crise sanitaire développé en Python avec Pygame. Une épidémie fictive (le Beta-Respiratory-Bacterial-Resistant Virus) éclate aléatoirement sur une carte des États-Unis et se propage pixel par pixel en temps réel grâce à NumPy. Le joueur pilote les politiques sanitaires et économiques de 46 États pour maximiser le nombre de survivants à la découverte du vaccin.

---

## Prérequis

- **Python 3.10 ou supérieur** (testé sur Python 3.10, 3.11 et 3.12)
- **pip**

> ⚠️ Le projet utilise Pygame et NumPy. Pygame peut présenter des incompatibilités selon les plateformes — voir la note ci-dessous.

---

## Installation des dépendances

```bash
pip install -r requirements.txt
```

Les dépendances requises sont :

- `pygame >= 2.5.0`
- `numpy >= 1.24.0`

---

## Lancement du jeu

```bash
python brbr_main.py
```

Le jeu s'ouvre dans une fenêtre de **1500 × 850 pixels**. Assurez-vous que votre résolution d'écran est suffisante.

---

## Structure du projet

```
brbr/
│
├── brbr_main.py          # Point d'entrée : initialisation Pygame et boucle principale
├── brbr_menu.py          # Menu principal animé + page des règles
├── brbr_continent.py     # Logique centrale : grille, états, famine, fin de partie
├── brbr_infection.py     # Moteur de propagation de l'épidémie
├── brbr_data.py          # Données statiques des 46 États + classe KinderState
├── brbr_ui.py            # Interface utilisateur (panneaux, boutons, graphiques)
│
├── graphics/
│   └── dessin.npy        # Carte des USA encodée sous forme de tableau NumPy
│
├── README.md
├── presentation.md
├── nature_du_code.md
├── licence.txt
└── requirements.txt
```

> ⚠️ Le fichier `graphics/dessin.npy` est indispensable au fonctionnement du jeu. Sans lui, le programme ne peut pas se lancer.

---

## Description des modules

### `brbr_main.py`
Point d'entrée du programme. Initialise Pygame, crée la fenêtre (1500 × 850 px), instancie le menu principal et orchestre la transition vers la simulation. La boucle principale tourne à 60 FPS.

### `brbr_menu.py`
Gère l'écran titre animé (grille de fond en défilement, particules flottantes, effet vignette, halo pulsant sur le titre). Contient le sélecteur de difficulté (3 niveaux : Facile / Moyen / Difficile, qui ajustent la fréquence de mise à jour de l'infection) et la page des règles scrollable.

### `brbr_continent.py`
Classe centrale `Continent`. Charge la carte `.npy`, initialise un pixel infecté aléatoire dans des États centraux, et orchestre à chaque tick : la propagation (`Infection.update`), la mise à jour économique des États (`update_infos`), et l'affichage. Gère aussi la logique de fin de partie (`end_game`).

### `brbr_infection.py`
Classe `Infection`. Contient tout le moteur épidémique : propagation par contact (8-voisinage), transmission aérienne aléatoire sur un rayon de 175 px, et mortalité des pixels infectés. Utilise NumPy de façon vectorisée pour traiter simultanément tous les pixels infectés à chaque tick.

### `brbr_data.py`
Données statiques de chaque État : population réelle, production alimentaire, taux d'obésité, position UI. Contient la classe `KinderState` qui représente l'état dynamique d'un État (population vivante, réserves alimentaires, statut confinement/frontières, exportations).

### `brbr_ui.py`
Interface utilisateur complète : panneau latéral gauche (informations d'État, configuration des exportations, mesures sanitaires), panneau secondaire de sélection du destinataire d'exportation, barre de progression du vaccin, indicateurs globaux. Tous les composants sont dessinés via Pygame avec animations d'interpolation (lerp).

---

## Guide de jeu

### Objectif
Maintenir en vie le maximum d'habitants le temps que le vaccin soit découvert (progression automatique, ~7 à 8 minutes en mode Moyen). Le score final est `(population vivante / population initiale) × 100`.

### Contrôles
- **Cliquer sur un État** sur la carte : ouvre le panneau de gestion de cet État.
- **Panneau État** (à gauche) : consulter les statistiques, activer/désactiver le confinement ou la fermeture des frontières, configurer les exportations alimentaires.
- **Boutons d'export** : choisir un État destinataire et un pourcentage de production à lui transférer (jusqu'à 4 flux par État).

### Mécaniques principales

#### Propagation de l'épidémie
- **Contact** : chaque pixel infecté tente d'infecter ses 8 voisins directs à chaque tick (probabilité 2/15 par voisin).
- **Aérien** : à chaque tick, avec une probabilité de 1/50, un nouveau foyer apparaît dans un rayon de 175 px autour d'un pixel infecté aléatoire.
- **Frontières** : les bordures entre États bloquent la propagation directe, mais peuvent être franchies par un saut de 5 px. Fermer les frontières bloque ce saut.
- **Confinement** : désactive la transmission aérienne pour l'État confiné.

#### Économie alimentaire
- Chaque tick, un État produit de la nourriture proportionnellement à sa population vivante, pondérée par son taux d'obésité.
- Confinement et fermeture des frontières réduisent chacun la production d'un tiers (effets cumulatifs).
- Si les réserves tombent à zéro, jusqu'à 10 pixels meurent de famine par tick.

#### Contrainte
- Maximum **4 États** simultanément en confinement, et maximum **4 États** avec frontières fermées.

### Paramètres techniques de l'infection

| Paramètre | Valeur |
|---|---|
| Probabilité de contamination par contact | 2/15 ≈ 13,3 % |
| Probabilité de transmission aérienne | 1/50 = 2 % par tick |
| Rayon de transmission aérienne | 175 pixels |
| Probabilité de mort d'un pixel infecté | 1/15 ≈ 6,7 % par tick |
| Morts de famine par tick (si réserves = 0) | jusqu'à 10 pixels |

### Niveaux de difficulté

| Difficulté | Intervalle entre ticks | Durée approximative |
|---|---|---|
| Facile | 750 ms | ~12 minutes |
| Moyen | 500 ms | ~8 minutes |
| Difficile | 300 ms | ~5 minutes |

---

## Note sur la compatibilité

Pygame peut présenter des comportements différents selon le système d'exploitation et la version Python. Le projet a été développé et testé sur [système d'exploitation de l'équipe]. Si le jeu ne se lance pas, vérifier que la version de Pygame installée est bien ≥ 2.5.0 avec `pip show pygame`.

Le projet n'utilise pas de musique ni de sons pour éviter les problèmes d'encodage audio selon les plateformes.

Les chemins d'accès aux fichiers utilisent `os.path.join` ou `os.sep.join` pour garantir la compatibilité Windows/Linux/macOS.

---

## Licence

Voir `licence.txt`.
