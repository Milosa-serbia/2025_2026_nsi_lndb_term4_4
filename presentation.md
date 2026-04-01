# BRBR Virus — Présentation du projet

## 1. Présentation globale du projet

### Naissance de l'idée

L'idée de BRBR Virus est née d'une question : que se passerait-il si on simulait une pandémie non pas avec des équations différentielles abstraites, mais pixel par pixel, sur une vraie carte géographique ? Nous voulions un jeu où chaque décision de santé publique a un coût réel et immédiat — et où l'économie peut tuer autant que le virus lui-même.

Le nom complet du pathogène est **Beta-Respiratory-Bacterial-Resistant Virus** : un virus respiratoire fictif, à transmission aérienne et par contact, résistant aux antibiotiques classiques — ce qui justifie qu'un vaccin spécifique soit la seule issue possible.

### Problématique initiale

Comment modéliser de façon convaincante et jouable la tension entre deux systèmes interdépendants — une épidémie et une économie alimentaire — dans un contexte géographique réel, en Python ?

### Objectifs

- Créer un moteur épidémique pixel par pixel fonctionnant en temps réel sur une carte des États-Unis encodée sous forme de tableau NumPy.
- Coupler ce moteur à un système économique d'alimentation par État, avec production, consommation, échanges commerciaux et famine.
- Proposer une interface jouable où le joueur prend des décisions sanitaires à fort impact stratégique (confinements, fermetures de frontières, exportations).
- Calculer un score final basé sur la proportion de population survivante à la découverte du vaccin.

---

## 2. Organisation du travail

### Présentation de l'équipe

L'équipe BRBR Virus est composée de [NOMBRE] élèves de [Première / Terminale] en spécialité NSI.

- **[Prénom Nom 1]**
- **[Prénom Nom 2]**
- *(+ autres membres si applicable)*

### Rôle de chacun et répartition des tâches

| Membre | Domaines techniques pris en charge |
|---|---|
| [Prénom Nom 1] | Moteur épidémique (`brbr_infection.py`), vectorisation NumPy, optimisation des performances |
| [Prénom Nom 2] | Interface graphique (`brbr_ui.py`, `brbr_menu.py`), effets visuels Pygame, animations |
| [Prénom Nom 3 si applicable] | Logique économique (`brbr_continent.py`), données des États (`brbr_data.py`), équilibrage du jeu |
| [Prénom Nom 4 si applicable] | Menu et page des règles, gestion des événements, intégration finale |

La documentation, les tests et le débogage ont été menés collectivement. Chaque membre a réalisé au moins une partie technique du projet.

### Temps passé sur le projet

Le projet a été développé sur environ [X] semaines, pour un total estimé de [X] heures par élève. Les grandes phases ont été :

- Conception et maquettage : [X] h
- Développement du moteur épidémique : [X] h
- Développement du moteur économique : [X] h
- Interface graphique et menu : [X] h
- Intégration, tests et débogage : [X] h
- Documentation : [X] h

---

## 3. Étapes du projet

### Phase 1 — Conception (idée → architecture)

La première étape a été de définir le format de la carte. Plutôt que d'utiliser une image raster classique, nous avons choisi d'encoder chaque pixel de la carte des États-Unis sous forme d'un tableau NumPy (`graphics/dessin.npy`) où la valeur de chaque pixel représente l'identifiant de l'État américain auquel il appartient. Ce choix a permis d'effectuer toutes les opérations géographiques (quel État est touché ? combien de pixels vivent dans cet État ?) par de simples opérations vectorisées sur tableaux, sans aucune boucle Python.

Nous avons ensuite défini les deux moteurs du jeu et leurs interactions : le moteur épidémique (propagation pixel par pixel, transmission aérienne, mortalité) et le moteur économique (production alimentaire, exportations, famine).

### Phase 2 — Développement du moteur épidémique

La propagation de l'épidémie repose sur deux vecteurs :

- **Transmission par contact** : à chaque tick, chaque pixel infecté tente d'infecter ses 8 voisins directs (probabilité 2/15 par voisin). Ce front progresse de façon organique sur la carte.
- **Transmission aérienne** : avec une probabilité de 1/50 par tick, un nouveau foyer apparaît dans un rayon de 175 pixels, pouvant créer des foyers secondaires loin du front principal.

La difficulté principale a été de rendre ce calcul assez rapide pour tourner en temps réel. La solution a été d'éliminer toutes les boucles Python explicites et de traiter tous les pixels infectés simultanément par des opérations NumPy vectorisées (indexation booléenne, `np.roll`, comptage de voisins par convolution).

### Phase 3 — Développement du moteur économique

Chaque État produit de la nourriture proportionnellement à sa population vivante, pondérée par son taux d'obésité réel (source : CDC). Le joueur configure des routes d'exportation entre États. Si un État épuise ses réserves, la famine s'enclenche (jusqu'à 10 pixels meurent par tick, indépendamment de l'infection).

Le couplage entre les deux moteurs est la vraie difficulté stratégique du jeu : confiner un État réduit la propagation mais aussi sa production alimentaire d'un tiers, risquant de déclencher une famine.

### Phase 4 — Interface graphique et menu

L'interface a été développée entièrement avec Pygame. Le menu principal dispose d'effets visuels animés (grille de fond défilante, particules flottantes, effet vignette, halo pulsant sur le titre). L'interface en jeu comprend un panneau latéral de gestion par État, un sélecteur d'exportation, une barre de progression du vaccin et des icônes de statut sur la carte. Toutes les animations utilisent une interpolation exponentielle (lerp) pour un rendu fluide.

### Phase 5 — Intégration et équilibrage

La dernière phase a consisté à assembler les modules, équilibrer les paramètres (probabilités de contagion, vitesse du vaccin, réserves initiales des États) et tester de nombreuses parties pour s'assurer que le jeu soit difficile mais pas impossible.

---

## 4. Opérationnalité du projet

### État d'avancement au moment du dépôt

Le projet est **complet et fonctionnel** dans son ensemble :

- Les trois niveaux de difficulté (Facile, Moyen, Difficile) sont opérationnels.
- Les deux mécaniques principales (épidémie + économie) fonctionnent et interagissent correctement.
- L'interface graphique est complète : menu animé, page des règles, panneau de jeu, écran de fin avec score.
- Le score est calculé et affiché à la fin de chaque partie.

Fonctionnalités non implémentées faute de temps : sauvegarde de parties, historique des scores, sons (intentionnellement exclus pour des raisons de compatibilité multiplateforme).

### Vérification de l'absence de bugs

- Tests manuels sur plusieurs dizaines de parties complètes sur différents niveaux de difficulté.
- Vérification des cas limites : État avec population zéro, exportation depuis un État en famine, confinement et frontières actifs simultanément.
- Vérification que la commande `pip install -r requirements.txt` puis `python brbr_main.py` suffit à lancer le jeu.

### Difficultés rencontrées et solutions

**Performances du moteur épidémique** : la première version utilisait des boucles Python pour traiter chaque pixel infecté, rendant le jeu injouable dès que l'infection s'étendait (plusieurs secondes par tick). La solution a été de vectoriser toutes les opérations avec NumPy, passant de plusieurs secondes à quelques millisecondes par tick.

**Bug d'ordre dans les exportations** : dans une première version, un État pouvait recevoir de la nourriture d'un voisin et la réexporter dans le même tick, créant de la nourriture ex nihilo. La solution a été de séparer la phase de calcul (combien chaque État produit et exporte) de la phase d'application (mise à jour effective des réserves), en deux passes distinctes à chaque tick.

**Équilibrage des paramètres** : trouver les bonnes valeurs de probabilité de contagion, de mortalité et de durée du vaccin pour que le jeu soit difficile mais pas injuste a nécessité de nombreuses itérations de test.

---

## 5. Ouverture

### Idées d'amélioration

- **Mutations virales** : introduire des variantes du virus avec des propriétés différentes (plus contagieux mais moins mortel, ou résistant au confinement).
- **Événements aléatoires** : tempêtes, crises économiques, découvertes scientifiques accélérant le vaccin.
- **Multijoueur coopératif** : deux joueurs gèrent chacun une moitié du territoire.
- **Mode analyse** : graphiques en temps réel de l'évolution de l'épidémie par État (courbes SIR).
- **Sons** : effets sonores et musique de fond, sous réserve de compatibilité multiplateforme.

### Analyse critique

Le projet atteint ses objectifs : la tension entre épidémie et économie fonctionne et crée des situations stratégiques intéressantes. La simulation n'est pas un modèle épidémiologique valide — les paramètres sont calibrés pour le jeu, pas pour la réalité — et ce choix est assumé.

Le principal point faible est la lisibilité de la situation en cours de partie : il est difficile de détecter une famine naissante dans un État éloigné du focus actuel du joueur. Des alertes visuelles sur la carte elle-même (clignotement, icône de famine) amélioreraient significativement l'expérience.

### Compétences développées

- Programmation orientée objet avancée en Python (composition, séparation des responsabilités).
- Manipulation de tableaux NumPy multidimensionnels et vectorisation.
- Développement d'une interface graphique avec Pygame (gestion d'événements, rendu, animations).
- Modélisation et équilibrage de systèmes couplés (épidémique + économique).
- Travail en équipe sur un projet multi-fichiers avec des interfaces claires entre modules.

### Démarche d'inclusion

Les données démographiques réelles intégrées au projet (populations, productions agricoles, taux d'obésité par État) mettent en lumière des inégalités structurelles entre États américains. Dans le jeu, certains États sont structurellement déficitaires en nourriture — pas par hasard, mais parce que leurs données réelles le reflètent. Cette dimension permet au jeu d'aborder, de façon fictive et pédagogique, des questions de justice alimentaire et d'équité dans la gestion de crise.
