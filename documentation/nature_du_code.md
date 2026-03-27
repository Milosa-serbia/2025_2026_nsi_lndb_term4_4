# Nature du code — BRBR Virus

---

## 1. Originalité du projet

**BRBR Virus est une création entièrement originale.**

Le projet a été conçu et développé intégralement par l'équipe dans le cadre des Trophées NSI. Ni l'architecture, ni les algorithmes, ni l'interface graphique ne proviennent d'un projet existant. L'idée de coupler une simulation épidémique pixel par pixel avec un moteur économique alimentaire par État est propre au projet.

Les seuls éléments non originaux sont :

- **Pygame** (LGPL v2.1) : bibliothèque de rendu graphique et de gestion d'événements.
- **NumPy** (BSD 3-Clause) : bibliothèque de calcul vectoriel sur tableaux.
- **Données démographiques et agricoles** : populations (US Census Bureau 2020), productions agricoles (USDA), taux d'obésité (CDC) — utilisées à titre pédagogique dans une simulation fictive.
- **La carte** (`graphics/dessin.npy`) : tableau NumPy créé manuellement, où chaque pixel encode l'identifiant de l'État américain auquel il appartient.

---

## 2. Recours à l'Intelligence Artificielle

Une IA générative a été utilisée ponctuellement, dans les situations suivantes :

- **Optimisation de la propagation vectorisée** : la méthode `neighbor_count` dans `brbr_infection.py` a bénéficié de suggestions pour remplacer des boucles Python explicites par des opérations NumPy batch, afin de passer d'un temps de traitement de plusieurs secondes par tick à quelques millisecondes.
- **Pré-calcul des pixels par État** : l'idée de stocker dans `self.state_pixels` les coordonnées de chaque État dès l'initialisation (plutôt que de recalculer `np.argwhere` à chaque tick lors de la gestion de la famine) a été suggérée par l'IA lors d'une session de débogage de performances.
- **Gestion des effets de bord des exportations** : lors de la conception de la mécanique de transfert alimentaire entre États, l'IA a aidé à identifier un bug d'ordre de traitement (un État pouvait recevoir de la nourriture et la réexporter dans le même tick, créant de la nourriture ex nihilo).

Dans tous les cas, les suggestions ont été comprises, discutées et adaptées par l'équipe. L'architecture du projet, les choix de conception des mécaniques de jeu, et l'intégralité du rendu graphique ont été réalisés sans assistance IA.

---

## 3. Architecture générale du projet

Le projet est organisé en 6 modules Python à responsabilités clairement séparées :

```
brbr_main.py        →  Point d'entrée, boucle principale Pygame
brbr_menu.py        →  Écran titre, règles du jeu, sélecteur de difficulté
brbr_continent.py   →  Coordinateur central : grille, économie, orchestration
brbr_infection.py   →  Moteur épidémique : propagation, mortalité, rendu carte
brbr_data.py        →  Données statiques des États + classe KinderState
brbr_ui.py          →  Tous les composants d'interface graphique
```

Les dépendances entre modules forment un graphe orienté acyclique : `brbr_main` instancie `MainMenu` et `Continent` ; `Continent` instancie `Infection` et `UI` ; `UI` et `Infection` dépendent de `brbr_data`. Il n'y a aucune dépendance circulaire.

La communication entre `Continent`, `Infection` et `UI` se fait par passage de références aux tableaux NumPy partagés (`status_grid`, `state_grid`) et au dictionnaire d'états (`infos`). Cela évite toute copie inutile de données volumineuses à chaque frame.

---

## 4. Description détaillée module par module

---

### 4.1 `brbr_main.py` — Point d'entrée

Ce module est volontairement minimal. Il contient la classe `Simulation` qui :

1. Initialise Pygame et crée une fenêtre de **1500 × 850 pixels**.
2. Instancie `MainMenu` pour la phase de menu.
3. Dès que `menu.is_done()` retourne `True` (le joueur a cliqué sur "Jouer"), instancie `Continent` en lui passant `menu.get_time_between_updates()` — la fréquence de tick choisie selon la difficulté.
4. Tourne à **60 FPS** via `self.clock.tick(60)`.

La séparation entre la phase menu et la phase jeu est gérée par la condition `if self.continent is None`. Cette approche évite une machine à états explicite tout en restant lisible. La liste `events` est collectée une seule fois par frame puis transmise aux sous-systèmes, évitant que plusieurs composants vident indépendamment la file d'événements Pygame.

---

### 4.2 `brbr_menu.py` — Menu principal et écran des règles

Ce module gère deux écrans distincts : le **menu principal** (`MainMenu`) et la **page des règles** (`RulesPage`), avec un ensemble de classes utilitaires pour les effets visuels.

#### Effets visuels de fond

Quatre couches superposées créent l'ambiance "terminal de commandement" :

**`BackgroundGrid`** — grille animée en défilement diagonal. À chaque frame, `self.scroll_offset` avance de 0,3 pixel. Les lignes horizontales et verticales sont tracées sur une surface SRCALPHA (transparence). L'offset est appliqué modulo la taille d'une cellule (60 px), créant l'illusion d'un défilement infini sans jamais dépasser cette valeur.

```python
self.scroll_offset = (self.scroll_offset + 0.3) % self.cell_size
x = -self.cell_size + (self.scroll_offset % self.cell_size)
```

**`Particle`** — 80 particules flottantes remontant vers le haut. Chaque particule a une vitesse (`0.2` à `0.8` px/frame), un rayon (`0.5` à `2.0` px) et une transparence (`30` à `120`) aléatoires. Leur couleur est un mélange interpolé entre le cyan `C_ACCENT` et le vert mint `C_ACCENT2` via `lerp_color`. Quand une particule sort par le haut, elle réapparaît en bas avec de nouvelles caractéristiques aléatoires.

**`draw_scanlines`** — lignes horizontales semi-transparentes (alpha = 18) espacées de 4 pixels, simulant l'effet CRT d'un écran à tube cathodique. Tracées sur une surface SRCALPHA et apposées en une seule opération `blit`.

**Vignette** — assombrissement progressif des bords par 80 itérations de rectangles concentriques dont l'alpha suit une loi quadratique décroissante : `alpha = int(160 × (1 − i/80)²)`. Le résultat est un fondu doux vers le noir sur les bords sans calcul de flou coûteux.

#### Animation du titre

Le titre "BRBR Virus" est rendu en deux passes :
1. Un **halo pulsant** : le même texte est rendu avec un alpha oscillant (`80 + sin(t×2)×30`) et blitté plusieurs fois avec de légers décalages `(±2px)` pour simuler une lueur floue sans vrai algorithme de flou gaussien.
2. Le **titre net** par-dessus, interpolé entre `C_ACCENT` et blanc à 15%.

La ligne décorative sous le titre s'étend progressivement depuis le centre : `accent_half_width = int((title_line_width/2) × min(1.0, frame/40))`. Cela crée une animation de révélation à l'ouverture du menu.

#### `MenuButton` — Bouton animé

Chaque bouton maintient une valeur `hover_animation` entre `0.0` et `1.0` qui converge vers `1.0` si la souris le survole, vers `0.0` sinon, à raison de 15% de l'écart par frame :

```python
self.hover_animation += (hover_target - self.hover_animation) * 0.15
```

Cette technique d'interpolation exponentielle ("lerp frame-rate indépendant") produit une animation fluide sans recourir à des timers explicites. Elle est utilisée partout dans le projet (boutons, tooltips, vignette). À chaque frame, la couleur du fond, de la bordure, du texte et la hauteur de la barre d'accent verticale sont recalculées depuis cette valeur.

#### Sélecteur de difficulté

Trois niveaux correspondent à trois valeurs de `time_between_updates` (en ms) :

| Difficulté | Intervalle de tick | Effet |
|---|---|---|
| FACILE | 750 ms | L'infection et l'économie se mettent à jour lentement |
| MOYEN | 500 ms | Réglage par défaut |
| DIFFICILE | 300 ms | Propagation très rapide, peu de temps pour réagir |

#### `RulesPage` — Page des règles scrollable

La page des règles implémente un scroll fluide avec deux valeurs distinctes : `scroll_target` (mise à jour instantanément par la molette souris) et `scroll_y` (qui converge vers `scroll_target` à 15% par frame). Le contenu est dessiné avec un clipping Pygame (`screen.set_clip`) pour ne pas déborder de la zone de contenu. Une scrollbar verticale est calculée proportionnellement : `scrollbar_height = max(40, int(area_height² / total_content_height))`.

---

### 4.3 `brbr_data.py` — Données et modèle de données

#### Dictionnaire `STATES`

`STATES` est un dictionnaire Python indexé par l'identifiant numérique de l'État (101 à 146). Chaque entrée contient :

- `ui_pos` : coordonnées en pixels de l'icône de l'État sur la carte (pour afficher les icônes de confinement/frontières).
- `population` : population réelle (source : Census Bureau 2020).
- `vegetable_production` : production alimentaire annuelle en unités arbitraires (source : USDA), calibrée pour que les États agricoles (Texas, Illinois, Californie) soient excédentaires et d'autres structurellement déficitaires.
- `obesity_rate` : taux d'obésité réel (source : CDC), qui multiplie la consommation alimentaire par habitant.
- `importations` / `exportations` : listes initialement vides, remplies dynamiquement par le joueur en jeu.

Les identifiants spéciaux `100` (mer) et `255` (frontière) sont aussi dans `STATES` avec des valeurs nulles, pour que le code puisse itérer sur `STATES.keys()` sans planter sur ces cas.

#### Classe `KinderState`

`KinderState` encapsule l'état **dynamique** d'un État. Elle est instanciée une fois par État au lancement de la simulation et mise à jour à chaque tick.

Attributs clés :
- `population_per_px` : ratio `population_réelle / nombre_de_pixels_de_l_état`. Calculé à l'initialisation via `np.argwhere(state_grid == id)`. Permet de convertir un comptage de pixels en population réelle à chaque tick.
- `food_ressources` : stock alimentaire courant. Initialisé aléatoirement entre `population × 30` et `population × 80` pour introduire de la variance entre parties.
- `alive_population` : population vivante courante, recalculée à chaque tick.
- `is_starving` : booléen passant à `True` quand `food_ressources == 0`, utilisé par l'UI pour afficher l'alerte dans le tooltip.
- `closed_border` / `lockdown` : booléens reflétant les mesures sanitaires actives.
- `exportations` : liste de 4 slots `[[id_dest, pct], [id_dest, pct], ...]`, modifiable par le joueur.

---

### 4.4 `brbr_infection.py` — Moteur épidémique

C'est le module le plus algorithmiquement dense du projet. Il implémente la propagation du BRBR Virus avec trois mécanismes distincts, tous traités de façon vectorisée par NumPy.

#### Encodage de la grille

La grille `status_grid` est un tableau NumPy `uint8` de taille `(850, 1500)`. Chaque cellule peut valoir :

| Valeur | Signification |
|---|---|
| 101–146 | Pixel sain appartenant à l'État N |
| 1 | Pixel infecté |
| 2 | Pixel mort |
| 100 | Mer (infranchissable) |
| 255 | Frontière entre États |

Ce choix d'encodage permet d'identifier l'appartenance à un État ET le statut sanitaire en une seule valeur, au prix de devoir traiter les pixels infectés (valeur `1`) et morts (valeur `2`) séparément de l'identifiant d'État (stocké dans `state_grid`, immuable).

#### Palette de couleurs

La palette `self.palette` est un tableau NumPy `(256, 3)` qui associe à chaque valeur possible une couleur RGB. Ce tableau permet de convertir toute la grille `status_grid` en image RGB en une seule opération :

```python
rgb = self.palette[status_grid]   # (850, 1500, 3) — indexation fantaisie NumPy
rgb = np.transpose(rgb, (1, 0, 2))  # Pygame attend (width, height, 3)
pygame.surfarray.blit_array(screen, rgb)
```

Cette technique, dite "indexed color" ou "palette rendering", est fondamentale pour les performances : elle remplace une double boucle Python sur 1,275 million de pixels par une seule opération NumPy.

#### Propagation par contact : `neighbor_count`

C'est l'algorithme central de la simulation. Il calcule, pour chaque pixel infecté, quels pixels voisins sont candidats à l'infection.

**Étape 1 — Récupérer tous les pixels infectés :**
```python
infected_positions = np.argwhere(status_grid == 1)
ys = infected_positions[:, 0]
xs = infected_positions[:, 1]
```
`np.argwhere` retourne un tableau `(N, 2)` de coordonnées `(y, x)`. On le découpe immédiatement en deux tableaux 1D `ys` et `xs` pour vectoriser les opérations suivantes.

**Étape 2 — Pour chacune des 8 directions, calculer les voisins :**
```python
neigh_ys = ys + dy   # décalage vectorisé sur tous les pixels infectés
neigh_xs = xs + dx
neighbors_values = status_grid[neigh_ys, neigh_xs]
safe_mask = ~np.isin(neighbors_values, invalid_statues)
candidates_ys.append(neigh_ys[safe_mask])
candidates_xs.append(neigh_xs[safe_mask])
```
Si 10 000 pixels sont infectés, cette opération calcule en une ligne les 10 000 voisins dans la direction `(dy, dx)`, lit leurs valeurs dans `status_grid`, et filtre ceux qui sont éligibles. Le tout sans boucle Python.

**Étape 3 — Le saut de frontière :**

Quand un voisin direct vaut `255` (frontière entre États), et que la direction est cardinale (haut, bas, gauche, droite — pas en diagonale), on tente de "sauter" 5 pixels plus loin dans la même direction :

```python
if (dy == 0) or (dx == 0):   # direction cardinale uniquement
    border = (neighbors_values == 255)
    if np.any(border):
        neigh_ys = ys[border] + 5 * dy
        neigh_xs = xs[border] + 5 * dx
        neighbors_values = status_grid[neigh_ys, neigh_xs]
        safe_mask = ~np.isin(neighbors_values, invalid_statues_behind_border)
        candidates_ys.append(neigh_ys[safe_mask])
        candidates_xs.append(neigh_xs[safe_mask])
```

`invalid_statues_behind_border` est la liste des statuts invalides **plus** les identifiants des États ayant leurs frontières fermées. Si l'État de destination est dans `closed_border_states`, son ID d'État (par exemple `112` pour le Dakota du Nord) est présent dans cette liste étendue, et le saut est bloqué.

La limitation aux directions cardinales est délibérée : un saut en diagonale permettrait à l'infection de contourner une frontière en "zigzaguant", ce qui serait visuellement incohérent.

**Étape 4 — Tirage aléatoire et infection :**
```python
random_selection = self.rng.random(size=len(neighbors_candidates), dtype=np.float32)
px_to_infect = neighbors_candidates[random_selection < self.contact_infect_probability]
ys, xs = np.transpose(px_to_infect)
status_grid[ys, xs] = 1
```
Chaque pixel candidat reçoit un tirage indépendant. Ceux sous le seuil de `2/15 ≈ 13.3%` sont infectés d'un coup via l'indexation NumPy.

Le générateur aléatoire utilisé est `numpy.random.default_rng()` (générateur PCG64), plus robuste statistiquement que `random.random()` de la bibliothèque standard et entièrement compatible avec les opérations vectorisées.

#### Transmission aérienne : `air_transmission`

```python
if self.rng.random() < self.air_infect_probability:   # 1/50 = 2% de chance par tick
    infected_ref = infected_positions[rng.integers(0, len(infected_positions))]
    while True:
        dy = rng.integers(-175, 176)
        dx = rng.integers(-175, 176)
        target_y, target_x = infected_ref_y + dy, infected_ref_x + dx
        if dans_les_bornes and status_grid[target_y, target_x] not in invalides:
            status_grid[target_y, target_x] = 1
            break
```

Un pixel source est choisi aléatoirement parmi tous les infectés. Le nouveau foyer tente d'apparaître dans un carré de ±175 px autour de lui. La boucle `while True` rejette les positions invalides (mer, frontière, déjà infecté, État confiné) jusqu'à en trouver une valide.

Ce mécanisme est désactivé pour les États confinés : `lockdowned_states` contient les IDs de ces États, et ils sont inclus dans la liste des cibles invalides.

#### Mortalité : `update_dead_number`

```python
infected_px_coords = np.argwhere(status_grid == 1)
random_selection = self.rng.random(size=len(infected_px_coords), dtype=np.float32)
px_to_kill = infected_px_coords[random_selection < self.death_probability]   # 1/15 ≈ 6.7%
ys, xs = np.transpose(px_to_kill)
status_grid[ys, xs] = 2
```

Chaque pixel infecté tire indépendamment un nombre aléatoire. Ceux sous `1/15` passent à l'état `2` (mort). La structure est identique à l'infection par contact, ce qui témoigne de la cohérence de l'approche vectorisée.

#### Rendu de la carte : `draw`

```python
rgb = self.palette[status_grid].copy()
# Effet de survol : assombrir l'État sous la souris
if not menu_open:
    state_id = state_grid[mouse_y, mouse_x]
    if 101 <= state_id <= 147:
        rgb[state_grid == state_id] = (rgb[state_grid == state_id] * 0.8).astype(np.uint8)
rgb = np.transpose(rgb, (1, 0, 2))
pygame.surfarray.blit_array(screen, rgb)
```

L'effet de survol multiplie tous les pixels de l'État par `0.8` (assombrissement de 20%) en une opération NumPy, sans boucle. La transposition `(1, 0, 2)` convertit le format `(height, width, 3)` de NumPy au format `(width, height, 3)` attendu par `pygame.surfarray`.

---

### 4.5 `brbr_continent.py` — Coordinateur central

#### Initialisation : construction de la grille

```python
self.status_grid = np.load('graphics/dessin.npy')
self.state_grid = self.status_grid.copy()
```

`state_grid` est une copie figée de la carte originale, utilisée uniquement en lecture pour connaître l'État d'appartenance d'un pixel. `status_grid` est la copie dynamique où l'infection modifie les valeurs.

**Calcul de `population_per_px` :**
```python
round(STATES[id]['population'] / len(np.argwhere(self.state_grid == id)), 5)
```
Pour chaque État, on compte le nombre de pixels qui lui appartiennent (`np.argwhere`), et on divise la population réelle par ce compte. Ce ratio permet de convertir un décompte de pixels vivants en population réelle à chaque tick. Le résultat est arrondi à 5 décimales pour éviter une accumulation d'erreurs flottantes sur des milliers de ticks.

**Choix du pixel zéro :**

L'épidémie démarre dans un pixel aléatoire parmi 13 États centraux (Wyoming, Utah, Colorado, Dakota du Sud, Nebraska, Kansas, Oklahoma, Iowa, Missouri, Arkansas, Wisconsin, Illinois, Mississippi). Ce choix assure que l'épidémie a le temps de se propager dans plusieurs directions avant d'atteindre les côtes, rendant chaque partie différente mais toujours stratégiquement intéressante.

**Pré-calcul `state_pixels` :**

```python
self.state_pixels = {}
for state_id in range(101, 147):
    coords = np.argwhere(self.state_grid == state_id)
    self.state_pixels[state_id] = (coords[:, 0], coords[:, 1])
```

Ce dictionnaire stocke, pour chaque État, les tableaux `ys` et `xs` de tous ses pixels. Il est calculé une seule fois à l'initialisation. Sans cela, la gestion de la famine (qui doit tuer des pixels dans un État spécifique à chaque tick) nécessiterait un `np.argwhere` par État par tick, soit jusqu'à 46 × plusieurs millisecondes = ralentissement massif.

#### Gestion des inputs : `handle_input`

La logique de clic est à trois niveaux :

1. **Aucun menu ouvert** : un clic gauche lit `state_grid[y, x]` pour identifier l'État cliqué. Si c'est un État valide (pas la mer, pas une frontière, pas déjà infecté), le panneau de cet État s'ouvre.
2. **Menu 1 ouvert, menu 2 fermé** : un clic en dehors du panneau ferme le menu 1.
3. **Menu 1 et 2 ouverts** : un clic en dehors des deux panneaux ferme les deux ; un clic dans le menu 1 uniquement ferme le menu 2.

Le clic droit ferme immédiatement tout menu ouvert, quelle que soit la configuration.

#### Mise à jour économique : `update_infos`

Cette méthode est le cœur du moteur économique. Elle s'exécute à chaque tick en 4 passes séquentielles.

**Passe 1 — Comptage de population et production :**

```python
flat = self.status_grid.ravel()
counts = np.bincount(flat, minlength=256)
```

`ravel()` aplatit la grille 2D en tableau 1D. `np.bincount` compte le nombre d'occurrences de chaque valeur entière en une seule opération, retournant un tableau de 256 éléments. `counts[id]` donne directement le nombre de pixels vivants de l'État `id` (les pixels infectés ayant la valeur `1`, pas l'ID d'État, ne sont pas comptés ici — ce qui est correct : un pixel infecté est vivant tant qu'il n'est pas passé à `2`).

Attentivement : la population vivante est calculée sur les pixels dont la valeur dans `status_grid` est encore l'identifiant d'État (non modifiée, donc ni infectée ni morte). Les pixels infectés (`1`) et morts (`2`) ne sont plus comptabilisés dans `counts[id]`.

La production est ensuite ajustée par les mesures sanitaires :

```python
factor = 1
if state.lockdown:     factor -= 1/3
if state.closed_border: factor -= 1/3
state.vegetable_production = base_production * factor
```

Un État avec les deux mesures actives conserve donc `1/3` de sa capacité de production.

**Passe 2 — Exportations :**

Pour chaque slot d'export de chaque État, la quantité transférée est :

```python
wanted = state.initial_vegetable_production * export_part
sent = min(wanted, state.food_ressources)
state.food_ressources -= sent
dest.food_ressources += sent
```

Deux subtilités importantes : la base de calcul est `initial_vegetable_production` (production à pleine capacité), pas la production courante. Cela signifie qu'un État appauvri par le confinement continue de promettre les mêmes volumes d'export, mais ne peut envoyer que ce qu'il a en stock (`min(wanted, available)`). Si son stock est épuisé, il cesse d'exporter (`if available <= 0: break`).

**Passe 3 — Sécurité et détection de famine :**

```python
state.is_starving = (state.food_ressources == 0)
```

Le booléen `is_starving` déclenche l'affichage de l'alerte dans le tooltip de survol de l'État.

**Passe 4 — Mortalité par famine :**

```python
ys_all, xs_all = self.state_pixels[state_id]
status_sub = self.status_grid[ys_all, xs_all]
alive_mask = (status_sub != 2)
ys_alive = ys_all[alive_mask]
xs_alive = xs_all[alive_mask]
n_to_kill = min(10, ys_alive.size)
idx = self.infection.rng.integers(0, ys_alive.size, size=n_to_kill)
self.status_grid[ys_alive[idx], xs_alive[idx]] = 2
```

Grâce au pré-calcul `state_pixels`, on accède instantanément aux pixels de l'État. On filtre ceux qui ne sont pas encore morts (`status != 2`), on en choisit jusqu'à 10 aléatoirement, et on les passe à `2`. Cette mortalité par famine est **indépendante** de la mortalité épidémique et s'applique simultanément.

#### Boucle principale : `update_and_draw`

```python
current_time = pygame.time.get_ticks()
if current_time - self.time_last_update >= self.time_between_updates:
    self.vaccine_progression += 0.115
    self.time_last_update = current_time
    self.infection.update(...)
    self.update_infos()
self.infection.draw(...)
self.ui.draw(...)
```

Le rendu s'effectue à chaque frame (60 FPS), mais les mises à jour logiques (épidémie, économie) ne se produisent qu'à intervalles fixes définis par `time_between_updates`. Ce découplage est standard en game development : il évite que la vitesse du jeu soit liée aux performances de la machine.

La progression du vaccin avance de `0.115%` par tick. À `time_between_updates = 500ms`, cela représente 2 ticks/seconde, soit `0.23%/s`, pour une durée totale de `100 / 0.23 ≈ 435 secondes ≈ 7 min 15 s` en mode Moyen.

#### Fin de partie : `end_game`

```python
alive_total = int(sum(
    st.alive_population for sid, st in self.infos.items() if 101 <= sid <= 146
))
total_initial = sum(STATES[id]['population'] for id in STATES if 101 <= id <= 146)
score = int(round((alive_total / total_initial) * 100))
```

Le score est un pourcentage de survie de la population totale initiale des 46 États. L'écran de fin superpose un overlay semi-transparent sur la carte (qui reste visible en arrière-plan), puis affiche un panneau style tableau de bord avec le score en grand, une barre de progression, et les statistiques de survivants/victimes. La couleur du score et le verdict varient selon la performance (vert pour ≥75%, jaune pour ≥50%, orange pour ≥25%, rouge sinon).

---

### 4.6 `brbr_ui.py` — Interface graphique

#### Primitives de dessin

Trois fonctions utilitaires sont utilisées partout dans le projet :

- **`draw_rounded_rect(surface, color, rect, radius, alpha)`** : dessine un rectangle arrondi. Quand `alpha < 255`, elle crée une surface temporaire SRCALPHA pour appliquer la transparence, puis la blit sur la surface cible. Sans ce mécanisme, Pygame ne supporte pas la transparence par alpha sur les formes dessinées directement.
- **`draw_border_rect`** : wrapper de `pygame.draw.rect` avec `width > 0` pour dessiner uniquement le contour.
- **`lerp_color(color_a, color_b, t)`** : interpolation linéaire composante par composante. `t=0` retourne `color_a`, `t=1` retourne `color_b`. Utilisée pour toutes les animations de survol.

#### Palette de couleurs globale

```python
C_BG       = (12,  14,  20)    # fond le plus sombre
C_PANEL    = (18,  22,  32)    # fond des panneaux
C_SURFACE  = (26,  32,  46)    # surfaces internes
C_SURFACE2 = (32,  40,  58)    # surfaces légèrement plus claires
C_BORDER   = (48,  60,  90)    # bordures subtiles
C_ACCENT   = (56, 189, 248)    # cyan vif — accent principal
C_ACCENT2  = (99, 235, 167)    # vert mint — succès, vivant
C_DANGER   = (248,  82,  82)   # rouge danger
C_WARNING  = (251, 189,  35)   # orange/jaune avertissement
C_TEXT     = (220, 228, 245)   # texte principal
C_TEXT_DIM = (100, 115, 150)   # texte secondaire
```

Cette palette est définie dans `brbr_ui.py` et recopiée à l'identique dans `brbr_menu.py` (pour autonomie du module menu). Elle garantit la cohérence visuelle entre tous les écrans.

#### `Button` — Bouton de sélection d'export

Chaque bouton de slot d'exportation (4 par État) affiche le nom de l'État destinataire courant et une flèche `›`. L'animation de survol repose sur la même technique lerp que dans `brbr_menu.py`. Le bouton affiche un état "actif" (fond cyan, texte sombre) quand le menu 2 correspondant est ouvert.

#### `ToggleButton` — Bouton de mesure sanitaire

Affiche une "pilule" (rectangle arrondi) avec un point qui se déplace à droite si actif. Les couleurs basculent entre un schéma neutre (gris) et un schéma actif (fond vert sombre, texte et point verts) selon l'état du toggle. La limite de 4 États simultanés par mesure est gérée dans les callbacks `change_border_statue` / `change_lockdown_statue`.

#### `ScrollablePanel` — Liste scrollable d'États

Panneau avec liste d'items scrollable par la molette souris, utilisé dans le menu 2 pour choisir l'État destinataire d'une exportation. Le clipping Pygame (`screen.set_clip`) est essentiel ici pour que les items qui débordent verticalement ne soient pas dessinés en dehors du panneau. Le scroll est instantané (pas de lerp) pour répondre précisément aux événements molette.

```python
old_clip = screen.get_clip()
screen.set_clip(self.rect.inflate(-2, -2))
# ... dessin des items ...
screen.set_clip(old_clip)
```

La sauvegarde et la restauration du clipping précédent (`old_clip`) est une bonne pratique indispensable quand plusieurs composants imbriqués utilisent le clipping.

#### `PercentSelector` — Sélecteur de pourcentage

Rangée de 11 boutons (0%, 10%, ..., 100%) permettant de choisir le volume d'export. Chacun maintient sa propre `hover_animation`. Le bouton sélectionné est affiché avec un fond cyan et du texte sombre (inversion de contraste).

#### Barre de vaccination : `_draw_vaccine_bar`

Affichée en permanence en haut à droite de l'écran. La largeur du remplissage est `int((bar_width - 56) × vaccine_progression / 100)`. L'icône du scientifique (image PNG chargée et redimensionnée à 48×48) est affichée à gauche.

#### Icônes sur la carte : `_draw_state_icons`

Les icônes de confinement (cadenas) et de frontières fermées (éclair) sont positionnées aux coordonnées `ui_pos` de chaque État. Si un État a les deux mesures actives, une icône combinée (troisième image PNG) remplace les deux icônes séparées. La logique utilise une copie de `remaining_closed_borders` pour marquer les États déjà traités et éviter de les compter deux fois.

#### Tooltip de survol : `_draw_hover_tooltip`

Affiché en bas de l'écran (centré) quand la souris survole un État valide et qu'aucun menu n'est ouvert. Il indique le nom de l'État et, si `is_starving == True`, une alerte rouge "FAMINE — les habitants meurent de faim". La largeur du tooltip s'adapte dynamiquement au contenu le plus long entre le nom et le message de statut.

#### Vignette : `_make_vignette`

Calculée une seule fois à l'initialisation et stockée dans `self.vignette_surface`. Elle est blittée à chaque frame en première opération de `draw`, avant tout autre élément d'UI. La formule quadratique `alpha = int(120 × (1 − i/60)²)` assure un fondu doux non linéaire.

---

## 5. Récapitulatif des techniques et notions mobilisées

| Technique / Notion | Module | Détail |
|---|---|---|
| Tableaux NumPy multidimensionnels | `brbr_infection.py`, `brbr_continent.py` | Grille 850×1500 d'`uint8` |
| Indexation booléenne NumPy | `brbr_infection.py` | Filtrage des pixels candidats à l'infection |
| Indexation fantaisie (fancy indexing) | `brbr_infection.py` | `palette[status_grid]` pour le rendu |
| Vectorisation (élimination des boucles Python) | `brbr_infection.py` | `neighbor_count`, `update_dead_number` |
| Mémoïsation / pré-calcul | `brbr_continent.py` | `state_pixels` calculé une fois à l'init |
| `np.bincount` pour comptage rapide | `brbr_continent.py` | Population vivante par État en O(N) |
| Programmation orientée objet | Tous modules | `Continent`, `Infection`, `UI`, `KinderState`… |
| Héritage et composition | `brbr_ui.py` | `UI` compose `ScrollablePanel`, `PercentSelector`… |
| Clipping Pygame | `brbr_ui.py`, `brbr_menu.py` | `screen.set_clip` pour les panneaux scrollables |
| Rendu par palette (indexed color) | `brbr_infection.py` | `palette[status_grid]` + `surfarray.blit_array` |
| Interpolation exponentielle (lerp) | `brbr_ui.py`, `brbr_menu.py` | Animations de survol fluides |
| Découplage rendu / logique | `brbr_continent.py` | 60 FPS rendu, tick variable selon difficulté |
| Gestion d'événements Pygame | Tous modules | File d'événements transmise en cascade |
| Transparence SRCALPHA | `brbr_ui.py`, `brbr_menu.py` | Surfaces temporaires pour alpha sur formes |
| Générateur aléatoire PCG64 | `brbr_infection.py` | `numpy.random.default_rng()` |
| Structures de données imbriquées | `brbr_data.py` | Dict de dicts + listes de listes pour exportations |
