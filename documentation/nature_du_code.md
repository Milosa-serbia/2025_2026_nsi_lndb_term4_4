# Nature du code — BRBR Virus

Ce document décrit la nature du code produit dans le cadre du projet BRBR Virus, conformément aux exigences de la section 4.5 du règlement des Trophées NSI 2026.

---

## 1. Degré de création originale

**BRBR Virus est une création entièrement originale.**

Le projet a été conçu et développé intégralement par l'équipe. Ni l'architecture générale, ni les algorithmes de propagation épidémique, ni le moteur économique, ni l'interface graphique ne proviennent d'un projet informatique existant. L'idée centrale — coupler une simulation épidémique pixel par pixel avec un moteur économique alimentaire par État, sur une carte géographique réelle encodée en tableau NumPy — est propre au projet.

Le découpage en 6 modules à responsabilités séparées (`brbr_main`, `brbr_menu`, `brbr_continent`, `brbr_infection`, `brbr_data`, `brbr_ui`) a été conçu par l'équipe dès la phase de conception, sans s'inspirer d'un projet existant.

---

## 2. Citation des sources externes

Les seuls éléments non originaux du projet sont les suivants :

**Bibliothèques tierces :**
- **Pygame** (LGPL v2.1, https://www.pygame.org/) : utilisée pour l'affichage, la gestion des événements clavier/souris et le rendu graphique.
- **NumPy** (BSD 3-Clause, https://numpy.org/) : utilisée pour le stockage de la grille de pixels et tous les calculs vectorisés sur cette grille.

**Données publiques :**
- Populations par État : United States Census Bureau, recensement 2020.
- Productions agricoles par État : United States Department of Agriculture (USDA).
- Taux d'obésité par État : Centers for Disease Control and Prevention (CDC).

Ces données sont utilisées à titre pédagogique dans une simulation fictive. Elles ne constituent pas un modèle réaliste ou scientifique.

**Ressource graphique :**
- `graphics/dessin.npy` : tableau NumPy créé manuellement par l'équipe, encodant l'identifiant de l'État américain pour chaque pixel de la carte. Ce fichier est une création originale de l'équipe.

---

## 3. Exploitation de codes existants

Aucun extrait de code source externe n'a été copié dans le projet. Les algorithmes implémentés (propagation par 8-voisinage, transmission aérienne par tirage aléatoire, calcul de population par `np.bincount`, rendu par palette indexée avec `surfarray.blit_array`, interpolation exponentielle pour les animations) ont été écrits intégralement par l'équipe, en s'appuyant sur la compréhension des mécanismes documentés dans les bibliothèques utilisées.

---

## 4. Modalités d'utilisation de l'intelligence artificielle

L'utilisation de l'IA a été **limitée, ponctuelle et justifiée**. Elle n'a jamais porté sur la conception ou l'architecture du projet, mais exclusivement sur des problèmes techniques précis rencontrés en cours de développement.

### Cas d'usage 1 — Optimisation du moteur épidémique

**Contexte :** la première version du moteur de propagation utilisait une boucle Python explicite sur chaque pixel infecté. Dès que l'infection s'étendait, le temps de traitement par tick atteignait plusieurs secondes, rendant le jeu injouable.

**Usage de l'IA :** nous avons décrit le problème à une IA générative et lui avons demandé comment remplacer la boucle par des opérations NumPy. Elle a suggéré d'utiliser `np.roll` pour décaler la grille dans les 8 directions et d'appliquer une indexation booléenne pour cibler les seuls pixels candidats à l'infection.

**Ce que l'équipe a fait :** nous avons compris le principe proposé, vérifié son fonctionnement sur un exemple minimal, puis l'avons adapté à notre structure de données (`status_grid` de type `uint8`, valeurs 0/1/2/3 pour sain/infecté/mort/frontière). Le code final est entièrement écrit par l'équipe.

### Cas d'usage 2 — Pré-calcul des pixels par État

**Contexte :** lors de la gestion de la famine, nous recalculions à chaque tick la liste des coordonnées de pixels appartenant à chaque État via `np.argwhere`, ce qui était coûteux.

**Usage de l'IA :** lors d'une session de débogage de performances, l'IA a suggéré de stocker ces coordonnées dès l'initialisation dans un dictionnaire `state_pixels`, une seule fois pour toute la partie.

**Ce que l'équipe a fait :** nous avons évalué la suggestion, vérifié qu'elle ne posait pas de problème si des pixels mouraient (la liste reste valide — on filtre ensuite par `status_grid`), et l'avons intégrée dans `brbr_continent.py`.

### Cas d'usage 3 — Correction d'un bug d'ordre dans les exportations

**Contexte :** dans une première version, un État pouvait recevoir de la nourriture d'un voisin et la réexporter dans le même tick, créant de la nourriture ex nihilo.

**Usage de l'IA :** nous avons décrit le bug à l'IA, qui a identifié qu'il provenait d'un problème d'ordre de traitement (lecture et écriture sur le même dictionnaire dans la même passe).

**Ce que l'équipe a fait :** nous avons compris la cause identifiée et implémenté nous-mêmes la solution : séparer la phase de calcul (combien chaque État exporte) de la phase d'application (mise à jour des réserves), en deux passes distinctes à chaque tick.

### Ce que l'IA n'a pas fait

L'IA n'a pas :
- Conçu l'architecture du projet ni suggéré le découpage en modules.
- Défini les mécaniques de jeu (propagation, confinement, famine, score).
- Écrit les fonctions de rendu graphique (menu animé, panneaux, animations lerp).
- Rédigé la documentation.

L'ensemble du code livré a été écrit, compris et validé par les membres de l'équipe.
