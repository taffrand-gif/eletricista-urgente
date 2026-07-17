# Villages top-200 P1C — différenciation NAP-minimal

**Date** : 2026-07-17  
**Mission** : P1C prototype (variante B village NAP-minimal)  
**Source** : `data/localidades.json` (676 villages) + `data/concelhos.json` (34 concelhos) + `precos-zonas.json` (960 clés)

## 1. Méthode

1. Sélection des **12 concelhos top-signal GSC** (cf. `_audit/GSC-TOP12-CONCELHOS-2026-07-16.md` §5).
2. Extraction de **tous les villages** de ces 12 concelhos depuis `data/localidades.json` (676 villages totaux, sous-ensemble ici).
3. **Tri par `village_km` croissant** (km dans `data/localidades.json`, pas TomTom village-level — voir SPEC §3 avertissement).
4. Prise du **top-200** (ou moins si <200 villages dans le sous-ensemble).
5. Pour chaque village : lookup zone dans `precos-zonas.json` (exact, puis casefold).

## 2. Inventaire

- Villages totaux dans les 12 concelhos : **307**
- Top-200 retenu : **200**
- Zones résolues en `exact` : **197 / 200**
- Zones résolues en `casefold` (à valider manuellement) : **1 / 200** — Sanjurge (Chaves)
- Zones ambigües identifiées (SPEC §3, NE PAS résoudre automatiquement) : **2 / 200** — Vila Nova de Souto d'El-Rei (Lamego), Urros (Vila Nova de Foz Côa)
- Zones absentes du fichier : **0 / 200** (les 16 localités espagnoles hors-fichier ne sont pas dans le top-200)
- Zones cohérentes entre `concelhos.json` et `precos-zonas.json` : **6 / 12 concelhos** (les 6 discordants : Bragança, Murça, V. N. Foz Côa, Chaves, Tabuaço — voir SPEC §2)

Distribution par concelho :

| Concelho | District | Villages dans top-200 |
|---|---|---:|
| Mirandela | Bragança | 30 |
| Chaves | Vila Real | 24 |
| Valpaços | Vila Real | 24 |
| Mesão Frio | Vila Real | 19 |
| Lamego | Viseu | 19 |
| Tabuaço | Viseu | 18 |
| Bragança | Bragança | 18 |
| Mogadouro | Bragança | 13 |
| Murça | Vila Real | 12 |
| Montalegre | Vila Real | 10 |
| Sernancelhe | Viseu | 7 |
| Vila Nova de Foz Côa | Guarda | 6 |

## 3. Liste triée par km croissant

| # | km | Village | Concelho | District | Zone | Statut zone |
|---:|---:|---|---|---|---:|---|
| 1 | 0.5 | São Nicolau | Mesão Frio | Vila Real | Z6 | exact |
| 2 | 0.6 | Bairro Social de Alvoraçães | Lamego | Viseu | Z6 | exact |
| 3 | 1.1 | Bairro do Fundo de Fomento à Habitação | Mirandela | Bragança | Z2 | exact |
| 4 | 1.1 | Madalena | Chaves | Vila Real | Z4 | exact |
| 5 | 1.2 | Vila Jusã | Mesão Frio | Vila Real | Z6 | exact |
| 6 | 1.7 | Vila Nova de Souto d'El-Rei | Lamego | Viseu | Z6 | exact |
| 7 | 2.2 | Vila Nova das Patas | Mirandela | Bragança | Z2 | exact |
| 8 | 2.2 | Vale de Madeiro | Mirandela | Bragança | Z2 | exact |
| 9 | 2.2 | Donões | Montalegre | Vila Real | Z6 | exact |
| 10 | 2.2 | Cocanha | Chaves | Vila Real | Z4 | exact |
| 11 | 2.4 | Ferreiros de Avões | Lamego | Viseu | Z6 | exact |
| 12 | 2.5 | Vale da Madre | Mogadouro | Bragança | Z3 | exact |
| 13 | 2.6 | Avões | Lamego | Viseu | Z6 | exact |
| 14 | 2.6 | Vale de Anta | Chaves | Vila Real | Z4 | exact |
| 15 | 2.6 | Tresouras | Mesão Frio | Vila Real | Z6 | exact |
| 16 | 2.8 | Freixedinha | Mirandela | Bragança | Z2 | exact |
| 17 | 2.8 | Seixal | Chaves | Vila Real | Z4 | exact |
| 18 | 2.8 | Barcos | Tabuaço | Viseu | Z5 | exact |
| 19 | 2.9 | Barrô | Mesão Frio | Vila Real | Z6 | exact |
| 20 | 2.9 | Barqueiros | Mesão Frio | Vila Real | Z6 | exact |
| 21 | 2.9 | Teixeiró | Mesão Frio | Vila Real | Z6 | exact |
| 22 | 3.0 | Carvalhais | Mirandela | Bragança | Z2 | exact |
| 23 | 3.1 | Eiras | Chaves | Vila Real | Z4 | exact |
| 24 | 3.2 | Possacos | Valpaços | Vila Real | Z3 | exact |
| 25 | 3.2 | Desejosa | Tabuaço | Viseu | Z5 | exact |
| 26 | 3.3 | Cepões | Lamego | Viseu | Z6 | exact |
| 27 | 3.4 | Cambres | Lamego | Viseu | Z5 | exact |
| 28 | 3.4 | Távora | Tabuaço | Viseu | Z5 | exact |
| 29 | 3.4 | Chavães | Tabuaço | Viseu | Z6 | exact |
| 30 | 3.5 | Chelas | Mirandela | Bragança | Z2 | exact |
| 31 | 3.5 | Sanfins | Valpaços | Vila Real | Z3 | exact |
| 32 | 3.5 | Penajoia | Mesão Frio | Vila Real | Z5 | exact |
| 33 | 3.5 | Loivos da Ribeira | Mesão Frio | Vila Real | Z6 | exact |
| 34 | 3.5 | Gestaçô | Mesão Frio | Vila Real | Z6 | exact |
| 35 | 3.5 | Samil | Bragança | Bragança | Z2 | exact |
| 36 | 3.5 | Noura | Murça | Vila Real | Z3 | exact |
| 37 | 3.6 | Bronceda | Mirandela | Bragança | Z2 | exact |
| 38 | 3.6 | Sande | Lamego | Viseu | Z5 | exact |
| 39 | 3.6 | Outeiro Seco | Chaves | Vila Real | Z4 | exact |
| 40 | 3.9 | Penude | Lamego | Viseu | Z6 | exact |
| 41 | 3.9 | Vilar de Nantes | Chaves | Vila Real | Z4 | exact |
| 42 | 4.0 | Padroso | Montalegre | Vila Real | Z6 | exact |
| 43 | 4.0 | Vassal | Valpaços | Vila Real | Z3 | exact |
| 44 | 4.0 | Castro de Avelãs | Bragança | Bragança | Z2 | exact |
| 45 | 4.1 | Várzea de Abrunhais | Lamego | Viseu | Z6 | exact |
| 46 | 4.1 | Fiolhoso | Murça | Vila Real | Z3 | exact |
| 47 | 4.2 | Britiande | Lamego | Viseu | Z6 | exact |
| 48 | 4.2 | Faiões | Chaves | Vila Real | Z4 | exact |
| 49 | 4.2 | Valongo de Milhais | Murça | Vila Real | Z3 | exact |
| 50 | 4.3 | Pinheiros | Tabuaço | Viseu | Z6 | exact |
| 51 | 4.4 | Cambeses do Rio | Montalegre | Vila Real | Z6 | exact |
| 52 | 4.4 | Mourilhe | Montalegre | Vila Real | Z6 | exact |
| 53 | 4.4 | Samaiões | Chaves | Vila Real | Z4 | exact |
| 54 | 4.6 | Vale de Casas | Valpaços | Vila Real | Z3 | exact |
| 55 | 4.6 | Valença do Douro | Tabuaço | Viseu | Z5 | exact |
| 56 | 4.6 | Adorigo | Tabuaço | Viseu | Z5 | exact |
| 57 | 4.6 | Brunhoso | Mogadouro | Bragança | Z3 | exact |
| 58 | 4.6 | Palheiros | Murça | Vila Real | Z3 | exact |
| 59 | 4.7 | Eixes | Mirandela | Bragança | Z2 | exact |
| 60 | 4.8 | Eivados | Mirandela | Bragança | Z2 | exact |
| 61 | 4.8 | Santo Estêvão | Chaves | Vila Real | Z4 | exact |
| 62 | 4.8 | Sanjurge | Chaves | Vila Real | Z4 | casefold |
| 63 | 4.8 | São Pedro de Sarracenos | Bragança | Bragança | Z2 | exact |
| 64 | 4.9 | Frende | Mesão Frio | Vila Real | Z6 | exact |
| 65 | 4.9 | Donai | Bragança | Bragança | Z3 | exact |
| 66 | 4.9 | Vila de Rei | Mogadouro | Bragança | Z3 | exact |
| 67 | 5.0 | Gimonde | Bragança | Bragança | Z3 | exact |
| 68 | 5.0 | Ferreirim | Sernancelhe | Viseu | Z6 | exact |
| 69 | 5.1 | Vilar de Ledra | Mirandela | Bragança | Z1 | exact |
| 70 | 5.1 | Contins | Mirandela | Bragança | Z2 | exact |
| 71 | 5.1 | Crasto | Valpaços | Vila Real | Z3 | exact |
| 72 | 5.1 | Cela | Chaves | Vila Real | Z4 | exact |
| 73 | 5.1 | Curalha | Chaves | Vila Real | Z4 | exact |
| 74 | 5.1 | Castanheiro do Sul | Tabuaço | Viseu | Z5 | exact |
| 75 | 5.1 | Meixedo | Bragança | Bragança | Z3 | exact |
| 76 | 5.1 | Vale de Porco | Mogadouro | Bragança | Z3 | exact |
| 77 | 5.2 | São Salvador | Mirandela | Bragança | Z2 | exact |
| 78 | 5.2 | Sedielos | Mesão Frio | Vila Real | Z6 | exact |
| 79 | 5.2 | Azinhoso | Mogadouro | Bragança | Z3 | exact |
| 80 | 5.3 | Vale de Pareiro | Mirandela | Bragança | Z2 | exact |
| 81 | 5.3 | Padornelos | Montalegre | Vila Real | Z6 | exact |
| 82 | 5.3 | Gostei | Bragança | Bragança | Z2 | exact |
| 83 | 5.3 | Gradiz | Sernancelhe | Viseu | Z6 | exact |
| 84 | 5.4 | Bustelo | Chaves | Vila Real | Z4 | exact |
| 85 | 5.5 | Muxagata | Vila Nova de Foz Côa | Guarda | Z4 | exact |
| 86 | 5.6 | Santa Marinha do Zêzere | Mesão Frio | Vila Real | Z6 | exact |
| 87 | 5.6 | Sarzedinho | Tabuaço | Viseu | Z5 | exact |
| 88 | 5.6 | Ribeira de Goujoim | Tabuaço | Viseu | Z6 | exact |
| 89 | 5.6 | Alfaião | Bragança | Bragança | Z2 | exact |
| 90 | 5.6 | Pópulo | Murça | Vila Real | Z3 | exact |
| 91 | 5.7 | Vale de Juncal | Mirandela | Bragança | Z2 | exact |
| 92 | 5.7 | Melcões | Lamego | Viseu | Z6 | exact |
| 93 | 5.8 | Pegarinhos | Murça | Vila Real | Z3 | exact |
| 94 | 6.0 | Cedães | Mirandela | Bragança | Z2 | exact |
| 95 | 6.0 | Remondes | Mogadouro | Bragança | Z2 | exact |
| 96 | 6.1 | Rio Torto | Valpaços | Vila Real | Z2 | exact |
| 97 | 6.1 | São Pedro de Agostém | Chaves | Vila Real | Z4 | exact |
| 98 | 6.1 | Nogueira | Bragança | Bragança | Z2 | exact |
| 99 | 6.1 | Baçal | Bragança | Bragança | Z3 | exact |
| 100 | 6.2 | Vale de Lobo | Mirandela | Bragança | Z1 | exact |
| 101 | 6.3 | Miradezes | Valpaços | Vila Real | Z2 | exact |
| 102 | 6.4 | Marmelos | Mirandela | Bragança | Z2 | exact |
| 103 | 6.4 | Meijinhos | Lamego | Viseu | Z6 | exact |
| 104 | 6.4 | Peredo dos Castelhanos | Vila Nova de Foz Côa | Guarda | Z4 | exact |
| 105 | 6.4 | Vilarandelo | Valpaços | Vila Real | Z3 | exact |
| 106 | 6.4 | Água Revés | Valpaços | Vila Real | Z3 | exact |
| 107 | 6.4 | Viariz | Mesão Frio | Vila Real | Z6 | exact |
| 108 | 6.4 | Soutelo | Mogadouro | Bragança | Z2 | exact |
| 109 | 6.5 | Vale de Salgueiro | Valpaços | Vila Real | Z2 | exact |
| 110 | 6.5 | Algeriz | Valpaços | Vila Real | Z3 | exact |
| 111 | 6.5 | Fornos do Pinhal | Valpaços | Vila Real | Z3 | exact |
| 112 | 6.5 | São Martinho de Mouros | Mesão Frio | Vila Real | Z6 | exact |
| 113 | 6.5 | São João de Fontoura | Mesão Frio | Vila Real | Z6 | exact |
| 114 | 6.5 | Arnas | Sernancelhe | Viseu | Z6 | exact |
| 115 | 6.6 | Lalim | Lamego | Viseu | Z6 | exact |
| 116 | 6.6 | Mouções | Sernancelhe | Viseu | Z6 | exact |
| 117 | 6.7 | Ervões | Valpaços | Vila Real | Z3 | exact |
| 118 | 6.7 | Guilheiro | Sernancelhe | Viseu | Z5 | exact |
| 119 | 6.8 | Gouviães | Lamego | Viseu | Z6 | exact |
| 120 | 6.8 | Freixo de Numão | Vila Nova de Foz Côa | Guarda | Z4 | exact |
| 121 | 6.8 | Longa | Tabuaço | Viseu | Z6 | exact |
| 122 | 6.9 | Suçães | Mirandela | Bragança | Z2 | exact |
| 123 | 6.9 | Sezelhe | Montalegre | Vila Real | Z6 | exact |
| 124 | 6.9 | Vila Verde da Raia | Chaves | Vila Real | Z4 | exact |
| 125 | 6.9 | Granja do Tedo | Tabuaço | Viseu | Z6 | exact |
| 126 | 6.9 | Ribalonga | Murça | Vila Real | Z3 | exact |
| 127 | 7.0 | Valbom de Figos | Mirandela | Bragança | Z2 | exact |
| 128 | 7.0 | Vale de Telhas | Valpaços | Vila Real | Z2 | exact |
| 129 | 7.0 | São Julião de Montenegro | Chaves | Vila Real | Z4 | exact |
| 130 | 7.0 | Rabal | Bragança | Bragança | Z3 | exact |
| 131 | 7.1 | Vila Verde | Mirandela | Bragança | Z2 | exact |
| 132 | 7.3 | Pousadas | Mirandela | Bragança | Z1 | exact |
| 133 | 7.4 | Carragosa | Bragança | Bragança | Z3 | exact |
| 134 | 7.4 | Penas Roias | Mogadouro | Bragança | Z3 | exact |
| 135 | 7.5 | Abambres | Mirandela | Bragança | Z2 | exact |
| 136 | 7.6 | Passos | Mirandela | Bragança | Z2 | exact |
| 137 | 7.6 | São Pedro de Vale do Conde | Mirandela | Bragança | Z2 | exact |
| 138 | 7.6 | Santa Eugénia | Murça | Vila Real | Z3 | exact |
| 139 | 7.7 | Santiago da Ribeira de Alhariz | Valpaços | Vila Real | Z3 | exact |
| 140 | 7.8 | Espinhosa | Tabuaço | Viseu | Z5 | exact |
| 141 | 7.8 | Salgueiro | Mogadouro | Bragança | Z3 | exact |
| 142 | 7.9 | Gralhas | Montalegre | Vila Real | Z5 | exact |
| 143 | 7.9 | Lazarim | Lamego | Viseu | Z6 | exact |
| 144 | 7.9 | Seara Velha | Chaves | Vila Real | Z4 | exact |
| 145 | 7.9 | Valadares | Mesão Frio | Vila Real | Z6 | exact |
| 146 | 7.9 | Sarzeda | Bragança | Bragança | Z2 | exact |
| 147 | 7.9 | Cunha | Sernancelhe | Viseu | Z6 | exact |
| 148 | 8.0 | Dálvares | Lamego | Viseu | Z6 | exact |
| 149 | 8.0 | Loivos do Monte | Mesão Frio | Vila Real | Z6 | exact |
| 150 | 8.1 | Valongo das Meadas | Mirandela | Bragança | Z2 | exact |
| 151 | 8.1 | Ucanha | Lamego | Viseu | Z6 | exact |
| 152 | 8.1 | Magueija | Lamego | Viseu | Z6 | exact |
| 153 | 8.1 | Paus | Lamego | Viseu | Z6 | exact |
| 154 | 8.1 | Castelo Branco | Mogadouro | Bragança | Z3 | exact |
| 155 | 8.2 | Vila Verdinho | Mirandela | Bragança | Z1 | exact |
| 156 | 8.2 | Lilela | Mirandela | Bragança | Z2 | exact |
| 157 | 8.2 | Fonte da Urze | Mirandela | Bragança | Z2 | exact |
| 158 | 8.2 | Calvão | Chaves | Vila Real | Z4 | exact |
| 159 | 8.2 | Covas do Douro | Tabuaço | Viseu | Z5 | exact |
| 160 | 8.3 | Vila de Ala | Mogadouro | Bragança | Z3 | exact |
| 161 | 8.4 | Pinhão | Tabuaço | Viseu | Z5 | exact |
| 162 | 8.5 | Casa Nova | Bragança | Bragança | Z2 | exact |
| 163 | 8.5 | Carva | Murça | Vila Real | Z4 | exact |
| 164 | 8.6 | Touça | Vila Nova de Foz Côa | Guarda | Z4 | exact |
| 165 | 8.6 | São Tomé de Covelas | Mesão Frio | Vila Real | Z6 | exact |
| 166 | 8.6 | Jou | Murça | Vila Real | Z4 | exact |
| 167 | 8.7 | Paradela | Mirandela | Bragança | Z2 | exact |
| 168 | 8.7 | Mascarenhas | Mirandela | Bragança | Z2 | exact |
| 169 | 8.8 | Vilela do Tâmega | Chaves | Vila Real | Z4 | exact |
| 170 | 8.8 | Resende | Mesão Frio | Vila Real | Z6 | exact |
| 171 | 8.8 | Sebadelhe de Serra | Sernancelhe | Viseu | Z5 | exact |
| 172 | 8.9 | Cabanelas | Valpaços | Vila Real | Z2 | exact |
| 173 | 8.9 | Ervededo | Chaves | Vila Real | Z4 | exact |
| 174 | 9.0 | Castelo Melhor | Vila Nova de Foz Côa | Guarda | Z4 | exact |
| 175 | 9.0 | Santa Maria de Émeres | Valpaços | Vila Real | Z3 | exact |
| 176 | 9.0 | Nagosa | Tabuaço | Viseu | Z6 | exact |
| 177 | 9.1 | Negrões | Montalegre | Vila Real | Z6 | exact |
| 178 | 9.1 | Viade de Baixo | Montalegre | Vila Real | Z6 | exact |
| 179 | 9.1 | Covelães | Montalegre | Vila Real | Z6 | exact |
| 180 | 9.1 | Santa Valha | Valpaços | Vila Real | Z3 | exact |
| 181 | 9.1 | Rebordãos | Bragança | Bragança | Z2 | exact |
| 182 | 9.1 | Sampaio | Mogadouro | Bragança | Z3 | exact |
| 183 | 9.3 | Gorgoço | Valpaços | Vila Real | Z3 | exact |
| 184 | 9.3 | Nogueira da Montanha | Chaves | Vila Real | Z3 | exact |
| 185 | 9.3 | Faílde | Bragança | Bragança | Z2 | exact |
| 186 | 9.4 | Vale de Gouvinhas | Valpaços | Vila Real | Z2 | exact |
| 187 | 9.4 | Bouça | Valpaços | Vila Real | Z3 | exact |
| 188 | 9.4 | Veiga de Lila | Valpaços | Vila Real | Z3 | exact |
| 189 | 9.4 | Gouvinhas | Tabuaço | Viseu | Z5 | exact |
| 190 | 9.4 | Quinta do Souto | Mogadouro | Bragança | Z3 | exact |
| 191 | 9.5 | Vale Bom Pitez | Valpaços | Vila Real | Z2 | exact |
| 192 | 9.5 | Vilela Seca | Chaves | Vila Real | Z4 | exact |
| 193 | 9.6 | Paredes da Beira | Tabuaço | Viseu | Z5 | exact |
| 194 | 9.6 | Tresminas | Murça | Vila Real | Z4 | exact |
| 195 | 9.7 | Friões | Valpaços | Vila Real | Z3 | exact |
| 196 | 9.7 | Santo António de Monforte | Chaves | Vila Real | Z4 | exact |
| 197 | 9.8 | Urros | Vila Nova de Foz Côa | Guarda | Z4 | exact |
| 198 | 9.8 | Gondesende | Bragança | Bragança | Z3 | exact |
| 199 | 9.8 | Espinhosela | Bragança | Bragança | Z3 | exact |
| 200 | 9.8 | Franco | Murça | Vila Real | Z2 | exact |

## 4. Notes de méthode

- `village_km` = kilométrage brut dans `data/localidades.json` (champ `km`). Ce n'est **pas** un temps de trajet TomTom village-level (donnée absente).
- Statut zone `exact` = match direct dans `precos-zonas.json`. `casefold` = match insensible casse. `missing` = village absent de `precos-zonas.json` → bloc sans zone, pas de prix injecté (SPEC §5 fail closed).
- Cette liste **n'est pas** un sitemap. Aucune page n'est générée dans cette mission — seul 1 prototype est produit sur le village #1.
- 3 villages du top-200 portent un statut `casefold-AMBIGUOUS-do-not-resolve` ou `casefold` (à valider manuellement) : Vila Nova de Souto d'El-Rei (#6, Lamego), Sanjurge (#62, Chaves), Urros (#197, V. N. de Foz Côa). SPEC §3 interdit la résolution automatique pour ces cas.

## 5. Prototype — village #1 utilisé

- **Village** : São Nicolau (Mesão Frio, Vila Real), km=0.5, Z6 exact (cohérent concelhos.json Z6)
- **Page** : `villages/mesao-frio-sao-nicolau.html` (worktree `feat/p1c-villages-eletricista`)
- **Mesures GATE** : 194 mots uniques (cible 150-250) · Jaccard vs hub parent 0.247 · Jaccard vs legacy 0.181 · 0 claim interdit · 1 lien hub · canonical self-ref OK
- **Rapport complet** : `_audit/P1C-RAPPORT-2026-07-17.md`
