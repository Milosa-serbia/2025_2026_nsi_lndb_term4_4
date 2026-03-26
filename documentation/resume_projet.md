# Résumé du projet — BRBR Virus

## Concept

BRBR Virus est un jeu de simulation de crise sanitaire en temps réel. Une épidémie éclate aléatoirement aux États-Unis et se propage de pixel en pixel sur une carte interactive. Le joueur dispose d'un arsenal limité de mesures sanitaires et d'un système de gestion économique pour tenter de sauver le maximum d'habitants — le tout contre la montre, en attendant la découverte d'un vaccin.

La simulation repose sur deux moteurs couplés et interdépendants : un **moteur épidémique** (propagation, mortalité) et un **moteur économique** (production alimentaire, commerce entre États, famine). La vraie difficulté du jeu tient à la tension permanente entre ces deux systèmes : les mesures qui ralentissent l'épidémie dégradent l'économie, et un État affamé perd sa population même si l'infection ne l'a pas encore atteint.

---

## Mécaniques de jeu

### La propagation de l'épidémie

L'épidémie se propage selon deux vecteurs distincts et simultanés.

La **transmission par contact** est locale et progressive : à chaque tick, chaque pixel infecté tente d'en contaminer ses 8 voisins directs avec une probabilité de 2/15 par voisin. Ce front de contamination progresse de façon organique sur la carte, en épousant la forme des États.

La **transmission aérienne** est plus imprévisible et potentiellement dévastatrice : à chaque tick, avec une probabilité de 1/50, un nouveau foyer d'infection "saute" à une distance aléatoire pouvant atteindre 175 pixels d'un pixel déjà infecté. Ce mécanisme peut créer des foyers secondaires très loin du front principal, rendant toute stratégie purement défensive vulnérable.

Enfin, les **frontières** entre États jouent un rôle clé dans la propagation : en conditions normales, la maladie peut les franchir par un "saut" de 5 pixels. Fermer les frontières d'un État bloque ce passage — mais pas la transmission aérienne.

### Les mesures sanitaires

Le joueur dispose de deux leviers pour chaque État, accessibles en cliquant sur sa région sur la carte :

**Fermer les frontières** bloque la propagation par contact entre États voisins (saut de frontière impossible). En contrepartie, la production alimentaire de l'État est réduite d'un tiers. Cette mesure est efficace pour contenir un foyer dans une région, mais elle isole aussi l'État de ses partenaires commerciaux.

**Le confinement** désactive la transmission aérienne dans l'État confiné : aucun nouveau foyer aérien ne peut s'y créer, et l'État confiné ne peut pas non plus servir de source de transmission aérienne. La production alimentaire est également réduite d'un tiers. Le confinement est redoutablement efficace contre les foyers aériens, mais son coût économique est identique à la fermeture des frontières — et les deux effets sont cumulatifs.

**Contrainte capitale** : le joueur ne peut appliquer chaque mesure qu'à un maximum de 4 États simultanément. Il est donc impossible de confiner ou d'isoler l'ensemble du territoire — tout l'enjeu est de choisir quels États protéger en priorité.

### L'économie alimentaire

Chaque État produit de la nourriture à chaque tick, proportionnellement à sa population vivante. Cette production est consommée par la même population, avec un surplus qui s'accumule en réserves. La consommation est pondérée par le **taux d'obésité** de l'État, une donnée réelle (source : CDC) : un État avec un taux d'obésité de 39 % comme le Mississippi consomme 39 % de nourriture de plus par habitant qu'un État "neutre", ce qui crée des déficits structurels.

Le joueur peut configurer des **routes d'exportation** depuis chaque État : 4 slots disponibles par État, chacun permettant de désigner un État destinataire et un pourcentage de la production initiale à lui transférer. Ces flux s'exécutent automatiquement à chaque tick. La logique d'export utilise la **production initiale** comme base de calcul (et non la production courante), ce qui signifie qu'un État appauvri par le confinement continue d'honorer ses engagements d'exportation s'il possède encore des stocks — au risque de s'épuiser lui-même.

Si les réserves d'un État tombent à zéro, la **famine** s'enclenche : jusqu'à 10 pixels meurent par tick, indépendamment de l'infection. La famine est silencieuse et difficile à détecter : la barre de réserves alimentaires dans le panneau de l'État passe progressivement au rouge, mais sans alerte visuelle sur la carte elle-même.

### Le vaccin et le score

La progression du vaccin avance de façon automatique et linéaire (+0,115 % par tick), sans que le joueur puisse l'influencer. Elle est affichée en permanence en haut de l'écran. La partie se termine lorsqu'elle atteint 100 %.

Le score est calculé sur la **proportion de la population initiale encore en vie** : `(population vivante / population initiale) × 100`. La population vivante est comptée pixel par pixel et pondérée par le ratio population réelle / nombre de pixels de chaque État — les données démographiques réelles sont donc intégrées au calcul final.

---

## Subtilités stratégiques

### Asymétrie des États

Les 46 États modélisés ne sont pas équivalents. Certains sont structurellement déficitaires en nourriture (forte population, faible production agricole, obésité élevée) : la Louisiane, le Mississippi, l'Alabama sont des exemples typiques. D'autres sont d'importants excédentaires : Texas, Illinois, New York, Californie. Construire des routes commerciales des États riches vers les États pauvres dès les premières minutes est une priorité souvent négligée par les joueurs débutants, qui se concentrent uniquement sur l'épidémie.

### Le dilemme confinement / production

Confiner ou fermer les frontières d'un État lui fait perdre un tiers de sa production par mesure. Un État doublement confiné (frontières fermées ET confinement) voit sa production alimentaire chuter des deux tiers. Si cet État était lui-même un exportateur, ses partenaires commerciaux se retrouvent soudainement privés d'approvisionnement. Une cascade de famines peut alors se déclencher sans lien direct avec l'épidémie, détruisant une population déjà fragilisée.

Il faut donc réserver les mesures les plus restrictives aux États déjà bien approvisionnés en réserves — et éviter d'appliquer les deux mesures simultanément sur un même État sauf urgence épidémique absolue.

### La transmission aérienne est la vraie menace

Les joueurs qui focalisent leur stratégie uniquement sur la fermeture des frontières sont régulièrement surpris par l'apparition de foyers secondaires loin du front principal. La transmission aérienne n'est pas bloquée par les frontières fermées : seul le confinement y fait obstacle. Dans les parties à difficulté élevée (ticks fréquents), des foyers aériens peuvent se multiplier plus vite que les mesures sanitaires ne peuvent être déployées.

### Le foyer initial est aléatoire mais contraint

L'épidémie commence toujours dans la bande centrale des États-Unis (Wyoming, Colorado, Iowa, Missouri, etc.). Cela signifie que les côtes Est et Ouest ont systématiquement quelques ticks de répit au début — mais aussi que les États du centre sont les premiers touchés et les premiers à perdre leur production.

### Les réserves initiales sont aléatoires

Chaque État démarre avec des réserves alimentaires entre 30 et 80 fois sa population. Cette variance introduit une part d'incertitude dans chaque partie : un État stratégiquement important peut se retrouver avec de faibles stocks initiaux, ce qui rend la mise en place d'une chaîne d'approvisionnement urgente.

### Les exportations utilisent la production initiale comme base

Un piège classique : configurer des exportations depuis un État qui a perdu beaucoup de population. Sa production courante a chuté (elle est proportionnelle à la population vivante), mais le volume d'export est calculé sur la production initiale. Si les deux valeurs divergent trop, l'État exporte plus qu'il ne produit et finit par épuiser ses réserves jusqu'à la famine — se condamnant lui-même en essayant d'aider ses voisins.

### La mortalité par famine est cumulable à la mortalité épidémique

Un État peut perdre sa population sous l'effet combiné de l'infection ET de la famine. Ces deux sources de mortalité sont indépendantes et s'appliquent simultanément à chaque tick. Dans les scénarios catastrophes (État confiné, épidémie présente, réserves épuisées), la dépopulation peut être extrêmement rapide.

---

## Ce qui rend le problème d'optimisation difficile

Trouver la stratégie optimale dans BRBR Virus est un problème réellement complexe, pour plusieurs raisons :

1. **L'espace de décision est vaste** : 46 États × (frontières ouvertes/fermées) × (confinement actif/inactif) × (4 routes d'export par État) × (11 niveaux de pourcentage possible) représente un espace de configurations astronomique.

2. **Les effets sont différés** : une décision d'exportation prise au tick 10 peut déclencher une famine au tick 200. La relation de causalité n'est pas immédiatement visible.

3. **Les deux moteurs interagissent de façon non linéaire** : réduire l'infection dans un État (en le confinant) peut provoquer sa famine (si sa production chute trop), ce qui cause plus de morts que l'infection elle-même n'en aurait causé.

4. **L'aléatoire est fondamental** : la transmission aérienne, les stocks initiaux, le pixel de départ de l'épidémie introduisent une variance irréductible. Une stratégie optimale en moyenne peut échouer sur une partie spécifique à cause d'un foyer aérien mal placé.

5. **La contrainte des 4 États maximum** par mesure force des choix douloureux : protéger l'Est ou l'Ouest ? Les États les plus peuplés ou les plus stratégiques économiquement ? Le joueur doit constamment arbitrer entre sauver des vies à court terme et préserver les capacités productives à long terme.
