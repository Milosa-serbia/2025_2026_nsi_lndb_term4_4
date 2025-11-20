# Projet de Roman, Gregoire et Eliott

# Concept
Étude scientifique et expérimentale se déroulant aux États-Unis.  
Un virus est apparu et menace de décimer la population américaine.  
Le joueur doit prendre des décisions pour limiter sa propagation tout en maintenant l’ordre et l’équilibre alimentaire du pays.  
Chaque simulation est unique grâce aux différentes variables aléatoires du virus et de l’économie.

---

# Fonctionnement général
- La carte des USA est convertie en tableau NumPy.
- Chaque pixel correspond à :
  - **0** : zone saine  
  - **1** : infectée  
  - **2** : morte  
  - **100** : mer  
  - **255** : frontière  
  - **101 → 146** : identifiants des états US

Chaque État possède :
- Une population
- Une production végétale
- Un taux d’obésité
- Des exportations & importations
- Des ressources alimentaires qui évoluent pendant la partie
- Une position d’affichage dans l’UI

---

# Gameplay actuel

### ✔ Virus
- Propagation par contact  
- Propagation aérienne  
- Pixels morts  
- Propagation fluide (NumPy, vectorisation)  
- Passage « au-dessus » des frontières dans certains cas

### ✔ Interface/UI
- Menu détaillé par État (population vivante, morts, production, ressources…)  
- Fermeture des frontières (max 4 États)  
- Confinement (max 4 États)  
- Modification des exportations via un second menu  
- Icônes affichées sur la carte (border, lockdown, les deux)

### ✔ Ressources alimentaires
- Chaque État produit, consomme et échange de la nourriture  
- Famine possible si mauvaise gestion  
- Les échanges suivent les pourcentages d’exportation définis dans les data

---

# To-do list
- Map :
  - Sauvegarder la Map USA (option avancée)
- Virus :
  - Ajouter une barre de progression du vaccin
  - Régler définitivement la question des survivants
- Menu :
  - Ajouter un bouton *Play*
  - Ajouter des niveaux de difficulté
  - Tutoriel intégré
- Gameplay :
  - Barre de stabilité politique
  - Événements aléatoires influençant la partie
  - Conditions de défaite
  - Conditions de victoire définitives

---

# Did list
- Map :
  - Sauvegarder un dessin grâce à NumPy
  - Trouver une map USA
  - Rendre la map utilisable avec le virus
- Virus :
  - Propagation du virus
  - Propagation sans lag
  - Cellules mortes
  - Transmission aérienne

---

# Installation

## 📦 Modules nécessaires
Assurez-vous d’installer les modules Python suivants :

```
pip install pygame numpy
```

C'est tout — aucun autre module externe n’est nécessaire.

---

# Lancement de la simulation

Assurez-vous que tous les fichiers du projet sont dans le même dossier :  
- `brbr_main.py`  
- `brbr_continent.py`  
- `brbr_infection.py`  
- `brbr_ui.py`  
- `brbr_data.py`  
- `dessin.npy`  
- Les images : `Enter.png`, `Locked.png`, `Power.png`  
- Ce fichier README

Puis lance simplement :

```
python brbr_main.py
```

Une fenêtre Pygame s’ouvrira avec la simulation.

---

# Notes finales
Le projet évolue constamment.  
N’hésitez pas à tester différentes stratégies : fermeture des frontières, confinement ciblé, redirection des exportations…  
Votre mission : sauver le pays — ou le regarder brûler, selon votre niveau de talent.