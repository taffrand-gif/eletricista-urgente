# EU P0 — réconciliation du comptage des frais hérités

- Baseline publique : `499de0064e89f56faa0d1ad93b330f0dec4072b0` ; manifeste : 116 pages.
- Référence initiale : **52 résultats de couche** sur 32 URL, soit **35 visibles + 17 JSON-LD**. Ce sont des apparitions au niveau des couches, pas 52 pages distinctes.
- Doublons visibles/JSON-LD : **8 paires** de même route et formulation normalisée apparaissent dans les deux couches. Le dédoublonnage par route + formulation donne **44 groupes**; 9 occurrences JSON-LD de référence n’ont pas de paire visible.
- Reclassification du parseur renforcé : un titre auparavant classé comme texte visible est maintenant correctement classé en métadonnée. Le scanner de référence conserve donc les 52 correspondances par route/formulation; le pré-scan renforcé les classe **34 visibles + 17 JSON-LD + 1 métadonnée**, et détecte en plus **10 copies/mentions de métadonnées** non comptées dans les 52 de référence.
- Recouvrement HTML brut : **53 matches bruts** recoupent exactement des résultats de couche; **9** formulations supplémentaires ne sont visibles qu’après extraction du texte, car des balises inline interrompent la chaîne brute. Le scan brut n’est pas additionné aux couches comme s’il s’agissait de nouvelles mentions.
- Correctifs auxiliaires distincts des 52 frais : 8 libellés de zones tarifaires, 8 anciens totaux de première heure et 9 attributs `data-zone` obsolètes retirés. Les 9 attributs ont été vérifiés comme non utilisés par CSS/JavaScript/inline et proviennent de l’ancien système de zones.
- Après correction locale : scanner renforcé sur **116/116 pages, zéro résultat, zéro erreur**. Le contrôle Preview reste à exécuter.
