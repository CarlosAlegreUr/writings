# AOCD v2 — Informe de ejecución

- Entrada: `data/municipios_unificados.json` (8131 unidades, 48.583.241 hab.)
- Rango: 95.000–120.000 hab. | semilla 42 | holgura de transferencia 2.000 hab./distrito | peso compacidad 100.0 €/km | tau 250.0 €
- Tiempo de ejecución: 250.1 s

## Distritos

- Distritos: **351** (objetivo teórico 48.583.241/107.500 ≈ 452)
- En rango [95.000, 120.000]: **251**
- Fuera de rango: **100**, por motivo:
  - 56 — Unidad > máximo sin subunidades: requiere subdivisión por secciones censales
  - 20 — Bloque factible en el que el equilibrado no encontró partición en rango
  - 14 — Bloque artefacto: provincia factible, resto infactible por las ciudades apartadas
  - 10 — Territorio aislado (isla, Ceuta, Melilla): imposibilidad geográfica
- Distritos sin contar ciudades que requieren subdivisión: 295; de ellos en rango 251 (85.1 %)
- Población en distritos en rango: 26.660.234 (54.9 %)

## Diámetros (km, máxima distancia entre centroides de unidades)

- Mínimo 0.0 | P25 4.6 | mediana 24.4 | P75 60.8 | P90 106.1 | máximo 204.9
- Distritos con diámetro > 100 km: 40; > 150 km: 13; > 200 km: 1
- Distritos con diámetro > 150 km (todos listados):
  - #030 06 Badajoz B1 2: 204.9 km, 94.367 hab., 42 unidades, elongación 2.61 — excepción: Fuera de rango (94.367 hab.): el bloque 06 Badajoz B1 admite K=5 por población total, pero no se encontró partición contigua en rango con la granularidad de las unidades disponibles (desviación mínima encontrada)
  - #344 49 Zamora 2: 186.1 km, 98.179 hab., 197 unidades, elongación 2.1
  - #305 44 Teruel: 179.6 km, 117.973 hab., 233 unidades, elongación 1.85
  - #033 06 Badajoz B1 5: 179.0 km, 94.750 hab., 52 unidades, elongación 2.57 — excepción: Fuera de rango (94.750 hab.): el bloque 06 Badajoz B1 admite K=5 por población total, pero no se encontró partición contigua en rango con la granularidad de las unidades disponibles (desviación mínima encontrada)
  - #087 10 Cáceres 3: 170.2 km, 99.541 hab., 85 unidades, elongación 1.94
  - #143 19 Guadalajara 2: 169.5 km, 95.311 hab., 273 unidades, elongación 1.7
  - #347 50 Zaragoza 3: 168.8 km, 95.057 hab., 89 unidades, elongación 1.91
  - #262 37 Salamanca 1: 165.5 km, 94.009 hab., 268 unidades, elongación 1.41 — excepción: Bloque de 182.819 hab. sin partición en rango; la provincia completa (327.685 hab.) sí la admite: artefacto de las unidades sin subdividir (Salamanca). Se resolverá con secciones censales; no se cruza provincia
  - #125 16 Cuenca 2: 163.7 km, 104.407 hab., 128 unidades, elongación 1.76
  - #296 42 Soria: 161.0 km, 97.002 hab., 192 unidades, elongación 1.77
  - #166 24 León 3: 160.7 km, 101.497 hab., 122 unidades, elongación 1.45
  - #003 02 Albacete 2: 159.5 km, 119.421 hab., 45 unidades, elongación 2.16
  - #124 16 Cuenca 1: 151.7 km, 95.369 hab., 117 unidades, elongación 2.9

## Cruces de frontera provincial

- Distritos con unidades de más de una provincia: **13**
  - #000 01 Araba/Álava (01, 09, 48, 87.418 hab.): 09 Burgos T2 (2.046 hab., 2 unidades: Condado de Treviño, Puebla de Arganzón  La) se une a 01 Araba/Álava (81.169 hab.): el territorio 09 Burgos T2 (2.046 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce estrictamente necesario; opción de mínima población movida) | 48 Bizkaia T2 (4.203 hab., 1 unidades: Urduña/Orduña) se une a 01 Araba/Álava (83.215 hab.): el territorio 48 Bizkaia T2 (4.203 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce estrictamente necesario; opción de mínima población movida)
  - #028 05 Ávila 2 (05, 28, 98.240 hab.): 05 Ávila recibe 35.797 hab. (2 unidades: Guadarrama, San Lorenzo de El Escorial) de 28 Madrid: el territorio 05 Ávila (158.989 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce estrictamente necesario; opción de mínima población movida)
  - #082 09 Burgos T1 1 (09, 34, 110.957 hab.): 34 Palencia T3 (47 hab., 1 unidades: Berzosilla) se une a 09 Burgos T1 (181.007 hab.): el territorio 34 Palencia T3 (47 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce estrictamente necesario; opción de mínima población movida) | 34 Palencia T2 (96 hab., 1 unidades: Villodrigo) se une a 09 Burgos T1 (181.054 hab.): el territorio 34 Palencia T2 (96 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce estrictamente necesario; opción de mínima población movida) | 34 Palencia T1 cede 39.985 hab. (65 unidades: Alba de Cerrato, Amayuelas de Arriba, Amusco, Antigüedad, Astudillo, Baltanás … (+59)) a 09 Burgos T1: el territorio 34 Palencia T1 (157.972 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce estrictamente necesario; opción de mínima población movida)
  - #083 09 Burgos T1 2 (09, 34, 110.178 hab.): 34 Palencia T3 (47 hab., 1 unidades: Berzosilla) se une a 09 Burgos T1 (181.007 hab.): el territorio 34 Palencia T3 (47 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce estrictamente necesario; opción de mínima población movida) | 34 Palencia T2 (96 hab., 1 unidades: Villodrigo) se une a 09 Burgos T1 (181.054 hab.): el territorio 34 Palencia T2 (96 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce estrictamente necesario; opción de mínima población movida) | 34 Palencia T1 cede 39.985 hab. (65 unidades: Alba de Cerrato, Amayuelas de Arriba, Amusco, Antigüedad, Astudillo, Baltanás … (+59)) a 09 Burgos T1: el territorio 34 Palencia T1 (157.972 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce estrictamente necesario; opción de mínima población movida)
  - #125 16 Cuenca 2 (16, 46, 104.407 hab.): 46 Valencia/València T2 (2.170 hab., 7 unidades: Ademuz, Casas Altas, Casas Bajas, Castielfabib, Puebla de San Miguel, Torrebaja … (+1)) se une a 16 Cuenca (197.606 hab.): el territorio 46 Valencia/València T2 (2.170 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce estrictamente necesario; opción de mínima población movida)
  - #143 19 Guadalajara 2 (19, 28, 95.311 hab.): 19 Guadalajara recibe 12.218 hab. (2 unidades: Molar  El, Vellón  El) de 28 Madrid: el territorio 19 Guadalajara (279.860 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce estrictamente necesario; opción de mínima población movida)
  - #281 40 Segovia 1 (28, 40, 99.286 hab.): 40 Segovia recibe 39.679 hab. (3 unidades: Alpedrete, Manzanares el Real, Moralzarzal) de 28 Madrid: el territorio 40 Segovia (156.788 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce estrictamente necesario; opción de mínima población movida)
  - #296 42 Soria (42, 50, 97.002 hab.): 42 Soria recibe 6.852 hab. (9 unidades: Aniñón, Brea de Aragón, Gotor, Illueca, Jarque de Moncayo, Morés … (+3)) de 50 Zaragoza: el territorio 42 Soria (90.150 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce estrictamente necesario; opción de mínima población movida)
  - #312 45 Toledo 7 (13, 45, 110.385 hab.): 13 Ciudad Real T2 (274 hab., 1 unidades: Anchuras) se une a 45 Toledo (740.148 hab.): el territorio 13 Ciudad Real T2 (274 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce estrictamente necesario; opción de mínima población movida)
  - #335 48 Bizkaia T1 1 (39, 48, 117.663 hab.): 39 Cantabria T2 (252 hab., 1 unidades: Valle de Villaverde) se une a 48 Bizkaia T1 (803.269 hab.): el territorio 39 Cantabria T2 (252 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce estrictamente necesario; opción de mínima población movida)
  - #344 49 Zamora 2 (24, 47, 49, 98.179 hab.): 47 Valladolid T2 (212 hab., 2 unidades: Quintanilla del Molar, Roales de Campos) se une a 49 Zamora (165.832 hab.): el territorio 47 Valladolid T2 (212 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce estrictamente necesario; opción de mínima población movida) | 49 Zamora recibe 28.035 hab. (12 unidades: Benuza, Cacabelos, Camponaraya, Carracedelo, Encinedo, Fabero … (+6)) de 24 León: el territorio 49 Zamora (166.044 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce estrictamente necesario; opción de mínima población movida)
  - #345 50 Zaragoza 1 (31, 50, 95.805 hab.): 31 Navarra T2 (26 hab., 1 unidades: Petilla de Aragón) se une a 50 Zaragoza (296.553 hab.): el territorio 31 Navarra T2 (26 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce estrictamente necesario; opción de mínima población movida) | 44 Teruel cede 17.688 hab. (3 unidades: Alcañiz, Calaceite, Mazaleón) a 50 Zaragoza: el territorio 44 Teruel (135.661 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce estrictamente necesario; opción de mínima población movida)
  - #347 50 Zaragoza 3 (44, 50, 95.057 hab.): 31 Navarra T2 (26 hab., 1 unidades: Petilla de Aragón) se une a 50 Zaragoza (296.553 hab.): el territorio 31 Navarra T2 (26 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce estrictamente necesario; opción de mínima población movida) | 44 Teruel cede 17.688 hab. (3 unidades: Alcañiz, Calaceite, Mazaleón) a 50 Zaragoza: el territorio 44 Teruel (135.661 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce estrictamente necesario; opción de mínima población movida)

Transferencias aplicadas (R5, mínima población movida):

- 31 Navarra T2 (26 hab., 1 unidades: Petilla de Aragón) se une a 50 Zaragoza (296.553 hab.): el territorio 31 Navarra T2 (26 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce estrictamente necesario; opción de mínima población movida)
- 34 Palencia T3 (47 hab., 1 unidades: Berzosilla) se une a 09 Burgos T1 (181.007 hab.): el territorio 34 Palencia T3 (47 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce estrictamente necesario; opción de mínima población movida)
- 34 Palencia T2 (96 hab., 1 unidades: Villodrigo) se une a 09 Burgos T1 (181.054 hab.): el territorio 34 Palencia T2 (96 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce estrictamente necesario; opción de mínima población movida)
- 39 Cantabria T2 (252 hab., 1 unidades: Valle de Villaverde) se une a 48 Bizkaia T1 (803.269 hab.): el territorio 39 Cantabria T2 (252 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce estrictamente necesario; opción de mínima población movida)
- 13 Ciudad Real T2 (274 hab., 1 unidades: Anchuras) se une a 45 Toledo (740.148 hab.): el territorio 13 Ciudad Real T2 (274 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce estrictamente necesario; opción de mínima población movida)
- 47 Valladolid T2 (212 hab., 2 unidades: Quintanilla del Molar, Roales de Campos) se une a 49 Zamora (165.832 hab.): el territorio 47 Valladolid T2 (212 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce estrictamente necesario; opción de mínima población movida)
- 09 Burgos T2 (2.046 hab., 2 unidades: Condado de Treviño, Puebla de Arganzón  La) se une a 01 Araba/Álava (81.169 hab.): el territorio 09 Burgos T2 (2.046 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce estrictamente necesario; opción de mínima población movida)
- 48 Bizkaia T2 (4.203 hab., 1 unidades: Urduña/Orduña) se une a 01 Araba/Álava (83.215 hab.): el territorio 48 Bizkaia T2 (4.203 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce estrictamente necesario; opción de mínima población movida)
- 46 Valencia/València T2 (2.170 hab., 7 unidades: Ademuz, Casas Altas, Casas Bajas, Castielfabib, Puebla de San Miguel, Torrebaja … (+1)) se une a 16 Cuenca (197.606 hab.): el territorio 46 Valencia/València T2 (2.170 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce estrictamente necesario; opción de mínima población movida)
- 19 Guadalajara recibe 12.218 hab. (2 unidades: Molar  El, Vellón  El) de 28 Madrid: el territorio 19 Guadalajara (279.860 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce estrictamente necesario; opción de mínima población movida)
- 44 Teruel cede 17.688 hab. (3 unidades: Alcañiz, Calaceite, Mazaleón) a 50 Zaragoza: el territorio 44 Teruel (135.661 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce estrictamente necesario; opción de mínima población movida)
- 42 Soria recibe 6.852 hab. (9 unidades: Aniñón, Brea de Aragón, Gotor, Illueca, Jarque de Moncayo, Morés … (+3)) de 50 Zaragoza: el territorio 42 Soria (90.150 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce estrictamente necesario; opción de mínima población movida)
- 05 Ávila recibe 35.797 hab. (2 unidades: Guadarrama, San Lorenzo de El Escorial) de 28 Madrid: el territorio 05 Ávila (158.989 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce estrictamente necesario; opción de mínima población movida)
- 49 Zamora recibe 28.035 hab. (12 unidades: Benuza, Cacabelos, Camponaraya, Carracedelo, Encinedo, Fabero … (+6)) de 24 León: el territorio 49 Zamora (166.044 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce estrictamente necesario; opción de mínima población movida)
- 40 Segovia recibe 39.679 hab. (3 unidades: Alpedrete, Manzanares el Real, Moralzarzal) de 28 Madrid: el territorio 40 Segovia (156.788 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce estrictamente necesario; opción de mínima población movida)
- 34 Palencia T1 cede 39.985 hab. (65 unidades: Alba de Cerrato, Amayuelas de Arriba, Amusco, Antigüedad, Astudillo, Baltanás … (+59)) a 09 Burgos T1: el territorio 34 Palencia T1 (157.972 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce estrictamente necesario; opción de mínima población movida)

## P25 de renta por distrito (estimación poblacional sobre rentas medias de unidad)

- Mínimo **8.147 €** (distrito #024 04 Almería 4) | mediana 12.555 € | máximo 29.258 €
- Mínimo entre distritos en rango: 8.147 €
- Comparación v1 (928 distritos): P25 mínimo 7.779 €

## Bloques factibles por suma sin partición contigua en rango

- 06 Badajoz B1: no se encontró partición en rango (imposibilidad no demostrada)
- 08 Barcelona B1: imposibilidad demostrable — Cornellà de Llobregat (91.589), Prat de Llobregat  El (66.184) no cabe(n) en ningún distrito contiguo en rango (todos sus vecinos son demasiado grandes)
- 11 Cádiz B1: imposibilidad demostrable — San Fernando (93.645) no cabe(n) en ningún distrito contiguo en rango (todos sus vecinos son demasiado grandes)
- 28 Madrid: imposibilidad demostrable — Pozuelo de Alarcón (89.378) no cabe(n) en ningún distrito contiguo en rango (todos sus vecinos son demasiado grandes)
- 29 Málaga: imposibilidad demostrable — Fuengirola (85.859), Benalmádena (77.654) no cabe(n) en ningún distrito contiguo en rango (todos sus vecinos son demasiado grandes)
- 30 Murcia B1: imposibilidad demostrable — Águilas (37.417) no cabe(n) en ningún distrito contiguo en rango (todos sus vecinos son demasiado grandes)
- 35 Las Palmas T1: no se encontró partición en rango (imposibilidad no demostrada)
- 36 Pontevedra: no se encontró partición en rango (imposibilidad no demostrada)
- 38 Santa Cruz de Tenerife T1 B1: no se encontró partición en rango (imposibilidad no demostrada)

## Excepciones (art. 16, restr. 1 y 4)

- Unidades > máximo sin subunidades (requieren subdivisión por secciones): 56
- Bloques artefacto (provincia factible, resto infactible por las ciudades apartadas): 12
  - 01 Araba/Álava: 81.169 hab., 50 unidades; cortado por Logroño, Vitoria-Gasteiz
  - 03 Alicante/Alacant B2: 38.556 hab., 1 unidades; cortado por Elx/Elche
  - 06 Badajoz B2: 14.307 hab., 4 unidades; cortado por Badajoz
  - 06 Badajoz B3: 2.437 hab., 1 unidades; cortado por Badajoz
  - 06 Badajoz B4: 1.992 hab., 1 unidades; cortado por Badajoz
  - 08 Barcelona B2: 38.490 hab., 1 unidades; cortado por Badalona, Barcelona, Santa Coloma de Gramenet
  - 26 La Rioja: 173.235 hab., 173 unidades; cortado por Logroño
  - 30 Murcia B2: 43.547 hab., 1 unidades; cortado por Murcia
  - 30 Murcia B3: 21.153 hab., 1 unidades; cortado por Cartagena
  - 30 Murcia B4: 11.535 hab., 1 unidades; cortado por Murcia
  - 37 Salamanca: 182.819 hab., 361 unidades; cortado por Salamanca
  - 38 Santa Cruz de Tenerife T1 B2: 11.405 hab., 1 unidades; cortado por San Cristóbal de La Laguna
- Territorios aislados ó sin donante viable: 8
  - 07 Illes Balears T2: 172.033 hab. (aislado)
  - 35 Las Palmas T2: 163.467 hab. (aislado)
  - 35 Las Palmas T3: 127.043 hab. (aislado)
  - 38 Santa Cruz de Tenerife T2: 85.104 hab. (aislado)
  - 38 Santa Cruz de Tenerife T3: 22.436 hab. (aislado)
  - 38 Santa Cruz de Tenerife T4: 11.806 hab. (aislado)
  - 51 Ceuta: 83.229 hab. (aislado)
  - 52 Melilla: 85.811 hab. (aislado)

## Adyacencias artificiales (unidades sin vecinos en la geometría)

- 07024 Formentera → 07026 Eivissa (24.9 km)
- 09154 Hacinas → 09450 Villanueva de Carazo (3.4 km)
- 09223 Monasterio de la Sierra → 09414 Valle de Valdelaguna (6.0 km)
- 17094 Llívia → 17141 Puigcerdà (6.6 km)
- 36901 Illa de Arousa  A → 36006 Cambados (7.9 km)
- 51001 Ceuta: sin unidad de su provincia a menos de 30.0 km (queda aislada)
- 52001 Melilla: sin unidad de su provincia a menos de 30.0 km (queda aislada)

## Bloques resueltos

| Bloque | Tipo | Unidades | Nodos | Población | K | Factible | Refinados | Mejoras P25 | s |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| 01 Araba/Álava | artefacto | 53 | 53 | 87.418 | 1 | sí | 0 | 0 | 0.0 |
| 02 Albacete | normal | 86 | 86 | 214.462 | 2 | sí | 0 | 19 | 0.1 |
| 03 Alicante/Alacant B1 | normal | 138 | 138 | 1.350.855 | 13 | sí | 0 | 130 | 0.2 |
| 03 Alicante/Alacant B2 | artefacto | 1 | 1 | 38.556 | 1 | sí | 0 | 0 | 0.0 |
| 04 Almería | normal | 102 | 102 | 560.355 | 5 | sí | 0 | 62 | 0.2 |
| 05 Ávila | normal | 250 | 250 | 194.786 | 2 | sí | 0 | 1 | 2.8 |
| 06 Badajoz B1 | normal | 158 | 158 | 495.664 | 5 | NO | 0 | 0 | 24.7 |
| 06 Badajoz B2 | artefacto | 4 | 4 | 14.307 | 1 | sí | 0 | 0 | 0.0 |
| 06 Badajoz B3 | artefacto | 1 | 1 | 2.437 | 1 | sí | 0 | 0 | 0.0 |
| 06 Badajoz B4 | artefacto | 1 | 1 | 1.992 | 1 | sí | 0 | 0 | 0.0 |
| 07 Illes Balears T1 | normal | 52 | 52 | 517.526 | 5 | sí | 0 | 39 | 0.0 |
| 07 Illes Balears T2 | aislado | 6 | 6 | 172.033 | 2 | NO | 0 | 0 | 0.4 |
| 07 Illes Balears T3 | normal | 8 | 8 | 100.323 | 1 | sí | 0 | 0 | 0.0 |
| 08 Barcelona B1 | normal | 303 | 303 | 2.947.064 | 27 | NO | 0 | 181 | 115.1 |
| 08 Barcelona B2 | artefacto | 1 | 1 | 38.490 | 1 | sí | 0 | 0 | 0.0 |
| 09 Burgos T1 | normal | 435 | 435 | 221.135 | 2 | sí | 0 | 134 | 5.3 |
| 10 Cáceres | normal | 223 | 223 | 387.820 | 4 | sí | 0 | 53 | 0.4 |
| 11 Cádiz B1 | normal | 23 | 23 | 796.007 | 7 | NO | 0 | 0 | 2.5 |
| 11 Cádiz B2 | normal | 20 | 20 | 119.618 | 1 | sí | 0 | 0 | 0.0 |
| 12 Castellón/Castelló | normal | 134 | 134 | 435.470 | 4 | sí | 0 | 11 | 0.3 |
| 13 Ciudad Real T1 | normal | 101 | 101 | 492.366 | 5 | sí | 0 | 19 | 0.1 |
| 14 Córdoba | normal | 76 | 76 | 449.341 | 4 | sí | 0 | 19 | 0.1 |
| 15 A Coruña | normal | 92 | 92 | 879.059 | 8 | sí | 0 | 9 | 0.3 |
| 16 Cuenca | normal | 245 | 245 | 199.776 | 2 | sí | 0 | 6 | 1.5 |
| 17 Girona | normal | 221 | 221 | 822.952 | 8 | sí | 0 | 112 | 0.6 |
| 18 Granada | normal | 173 | 173 | 704.418 | 7 | sí | 0 | 96 | 0.3 |
| 19 Guadalajara | normal | 290 | 290 | 292.078 | 3 | sí | 0 | 0 | 0.1 |
| 20 Gipuzkoa | normal | 87 | 87 | 542.089 | 5 | sí | 0 | 46 | 0.1 |
| 21 Huelva | normal | 79 | 79 | 390.158 | 4 | sí | 0 | 22 | 0.0 |
| 22 Huesca | normal | 202 | 202 | 228.634 | 2 | sí | 0 | 34 | 0.9 |
| 23 Jaén | normal | 97 | 97 | 618.678 | 6 | sí | 0 | 55 | 0.1 |
| 24 León | normal | 198 | 198 | 296.167 | 3 | sí | 0 | 92 | 0.7 |
| 25 Lleida | normal | 230 | 230 | 306.458 | 3 | sí | 0 | 146 | 0.7 |
| 26 La Rioja | artefacto | 173 | 173 | 173.235 | 2 | sí | 0 | 62 | 0.7 |
| 27 Lugo | normal | 67 | 67 | 324.842 | 3 | sí | 0 | 11 | 0.0 |
| 28 Madrid | normal | 162 | 162 | 1.937.305 | 18 | NO | 0 | 26 | 33.2 |
| 29 Málaga | normal | 101 | 101 | 1.022.499 | 10 | NO | 0 | 25 | 13.3 |
| 30 Murcia B1 | normal | 40 | 40 | 801.304 | 7 | NO | 0 | 15 | 4.4 |
| 30 Murcia B2 | artefacto | 1 | 1 | 43.547 | 1 | sí | 0 | 0 | 0.0 |
| 30 Murcia B3 | artefacto | 1 | 1 | 21.153 | 1 | sí | 0 | 0 | 0.0 |
| 30 Murcia B4 | artefacto | 1 | 1 | 11.535 | 1 | sí | 0 | 0 | 0.0 |
| 31 Navarra T1 | normal | 270 | 270 | 470.535 | 4 | sí | 0 | 7 | 0.8 |
| 32 Ourense | normal | 92 | 92 | 304.592 | 3 | sí | 0 | 19 | 0.1 |
| 33 Asturias | normal | 76 | 76 | 518.924 | 5 | sí | 0 | 6 | 0.0 |
| 34 Palencia T1 | normal | 124 | 124 | 117.987 | 1 | sí | 0 | 0 | 0.0 |
| 35 Las Palmas T1 | normal | 20 | 20 | 483.507 | 5 | NO | 0 | 0 | 2.1 |
| 35 Las Palmas T2 | aislado | 7 | 7 | 163.467 | 2 | NO | 0 | 0 | 0.5 |
| 35 Las Palmas T3 | aislado | 6 | 6 | 127.043 | 1 | sí | 0 | 0 | 0.0 |
| 36 Pontevedra | normal | 60 | 60 | 651.622 | 6 | NO | 0 | 27 | 4.8 |
| 37 Salamanca | artefacto | 361 | 361 | 182.819 | 2 | sí | 0 | 4 | 3.4 |
| 38 Santa Cruz de Tenerife T1 B1 | normal | 28 | 28 | 572.041 | 5 | NO | 0 | 2 | 3.3 |
| 38 Santa Cruz de Tenerife T1 B2 | artefacto | 1 | 1 | 11.405 | 1 | sí | 0 | 0 | 0.0 |
| 38 Santa Cruz de Tenerife T2 | aislado | 14 | 14 | 85.104 | 1 | sí | 0 | 0 | 0.0 |
| 38 Santa Cruz de Tenerife T3 | aislado | 6 | 6 | 22.436 | 1 | sí | 0 | 0 | 0.0 |
| 38 Santa Cruz de Tenerife T4 | aislado | 3 | 3 | 11.806 | 1 | sí | 0 | 0 | 0.0 |
| 39 Cantabria T1 | normal | 100 | 100 | 417.210 | 4 | sí | 0 | 37 | 0.1 |
| 40 Segovia | normal | 212 | 212 | 196.467 | 2 | sí | 0 | 43 | 0.5 |
| 41 Sevilla | normal | 104 | 104 | 1.139.828 | 11 | sí | 0 | 51 | 0.1 |
| 42 Soria | normal | 192 | 192 | 97.002 | 1 | sí | 0 | 0 | 0.0 |
| 43 Tarragona | normal | 183 | 183 | 720.380 | 7 | sí | 0 | 132 | 0.5 |
| 44 Teruel | normal | 233 | 233 | 117.973 | 1 | sí | 0 | 0 | 0.0 |
| 45 Toledo | normal | 205 | 205 | 740.422 | 7 | sí | 0 | 122 | 0.5 |
| 46 Valencia/València T1 | normal | 258 | 258 | 1.881.315 | 18 | sí | 0 | 81 | 1.1 |
| 47 Valladolid T1 | normal | 222 | 222 | 224.568 | 2 | sí | 0 | 57 | 1.3 |
| 48 Bizkaia T1 | normal | 111 | 111 | 803.521 | 7 | sí | 0 | 42 | 0.4 |
| 49 Zamora | normal | 262 | 262 | 194.079 | 2 | sí | 0 | 60 | 1.4 |
| 50 Zaragoza | normal | 287 | 287 | 307.415 | 3 | sí | 0 | 195 | 1.2 |
| 51 Ceuta | aislado | 1 | 1 | 83.229 | 1 | sí | 0 | 0 | 0.0 |
| 52 Melilla | aislado | 1 | 1 | 85.811 | 1 | sí | 0 | 0 | 0.0 |

## Verificación

- Unidades asignadas exactamente una vez: sí
- Distritos no contiguos (BFS sobre `vecinos`): []
- Suma de poblaciones de distritos = población total: sí
