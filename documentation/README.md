# BRBR Virus — Documentation technique

## Présentation

BRBR Virus est un jeu de simulation de gestion de crise sanitaire développé en Python avec Pygame. L'épidémie se propage en temps réel sur une carte des États-Unis rendue pixel par pixel grâce à NumPy. Le joueur pilote les politiques sanitaires et économiques de 46 États pour maximiser le nombre de survivants à la découverte du vaccin.

---

## Prérequis

- Python 3.10 ou supérieur
- pip

### Installation des dépendances

```bash
pip install pygame numpy
```

---

## Lancement du jeu

```bash
python brbr_main.py
```

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
├── licence.txt
└── requirements.txt
```

---

## Description des modules

### `brbr_main.py`
Point d'entrée du programme. Initialise Pygame, crée la fenêtre (1500×850 px), instancie le menu principal et orchestre la transition vers la simulation. La boucle principale tourne à 60 FPS.

### `brbr_menu.py`
Gère l'écran titre animé (grille de fond en défilement, particules flottantes, effet vignette, halo pulsant sur le titre). Contient le sélecteur de difficulté (3 niveaux : Facile / Moyen / Difficile, qui ajustent la fréquence de mise à jour de l'infection) et la page des règles scrollable.

### `brbr_continent.py`
Classe centrale `Continent`. Charge la carte `.npy`, initialise un pixel infecté aléatoire dans des États centraux, et orchestre à chaque tick : la propagation (`Infection.update`), la mise à jour économique des États (`update_infos`), et l'affichage. Gère aussi la logique de fin de partie (`end_game`).

### `brbr_infection.py`
Classe `Infection`. Contient tout le moteur épidémique : propagation par contact (8-voisinage avec saut de bordière), transmission aérienne aléatoire sur un rayon de 175 px, et mortalité des pixels infectés. Utilise NumPy de façon vectorisée pour traiter simultanément tous les pixels infectés à chaque tick.

### `brbr_data.py`
Données statiques de chaque État : population réelle, production alimentaire, taux d'obésité, position UI. Contient la classe `KinderState` qui représente l'état dynamique d'un État (population vivante, réserves alimentaires, statut confinement/frontières, exportations).

### `brbr_ui.py`
Interface utilisateur complète : panneau latéral gauche (informations d'État, configuration des exportations, mesures sanitaires), panneau secondaire de sélection du destinataire d'exportation, barre de progression du vaccin, indicateurs globaux. Tous les composants sont dessinés via Pygame avec animations d'interpolation (lerp).

---

## Mécaniques de jeu

### Propagation de l'épidémie
- **Contact** : chaque pixel infecté tente d'infecter ses 8 voisins directs à chaque tick (probabilité 2/15 par voisin).
- **Aérien** : à chaque tick, avec une probabilité de 1/50, un nouveau foyer apparaît dans un rayon de 175 px autour d'un pixel infecté aléatoire.
- **Frontières** : les bordures (pixels 255) bloquent la propagation directe mais peuvent être franchies (saut de 5 px). Fermer les frontières d'un État interdit ce saut.
- **Confinement** : désactive la transmission aérienne pour les États confinés.

### Économie alimentaire
- Chaque tick, un État produit de la nourriture proportionnellement à sa population vivante.
- La consommation est `population_vivante × (1 + taux_obésité)`.
- Les confinements et fermetures de frontières réduisent chacun la production d'un tiers.
- Les États peuvent exporter jusqu'à 4 flux (destinataire + pourcentage de production).
- Si les réserves tombent à zéro, jusqu'à 10 pixels meurent de famine par tick.

### Vaccin et fin de partie
- La progression du vaccin augmente de 0,115 % à chaque tick, indépendamment des actions du joueur.
- À 100 %, la simulation s'arrête et le score est calculé : `(population_vivante / population_initiale) × 100`.

---

## Paramètres techniques de l'infection

| Paramètre | Valeur |
|---|---|
| Probabilité de contamination par contact | 2/15 ≈ 13,3 % |
| Probabilité de transmission aérienne | 1/50 = 2 % par tick |
| Rayon de transmission aérienne | 175 pixels |
| Probabilité de mort d'un pixel infecté | 1/15 ≈ 6,7 % par tick |
| Morts de famine par tick (si réserves = 0) | jusqu'à 10 pixels |

---

## Licence

Voir `licence.txt`.
