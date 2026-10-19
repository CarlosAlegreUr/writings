# AOCD v2 — Informe de ejecución

- Entrada: `data/secciones_unificadas.json` (36554 unidades, 49.128.297 hab.)
- Rango: 95.000–120.000 hab. | semilla 42 | holgura de transferencia 0 hab./distrito | peso compacidad 100.0 €/km | tau 250.0 €
- Tiempo de ejecución: 303.3 s

## Distritos

- Distritos: **469** (objetivo teórico 49.128.297/107.500 ≈ 457)
- En rango [95.000, 120.000]: **457**
- Fuera de rango: **12**, por motivo:
  - 12 — Territorio aislado (isla, Ceuta, Melilla): imposibilidad geográfica
- Distritos sin contar ciudades que requieren subdivisión: 469; de ellos en rango 457 (97.4 %)
- Población en distritos en rango: 48.360.087 (98.4 %)

## Diámetros (km, máxima distancia entre centroides de unidades)

- Mínimo 2.3 | P25 7.7 | mediana 18.6 | P75 52.1 | P90 90.5 | máximo 204.1
- Distritos con diámetro > 100 km: 40; > 150 km: 12; > 200 km: 1
- Distritos con diámetro > 150 km (todos listados):
  - #457 50 Zaragoza 1: 204.1 km, 116.369 hab., 197 unidades, elongación 3.12
  - #040 06 Badajoz 5: 190.4 km, 110.326 hab., 118 unidades, elongación 2.52
  - #455 49 Zamora 1: 189.7 km, 95.004 hab., 207 unidades, elongación 2.21
  - #113 09 Burgos T1 2: 183.8 km, 99.366 hab., 255 unidades, elongación 1.93
  - #406 44 Teruel: 179.9 km, 119.428 hab., 267 unidades, elongación 1.98
  - #205 24 León 4: 174.0 km, 119.913 hab., 161 unidades, elongación 1.28
  - #141 13 Ciudad Real T1 5: 167.5 km, 100.142 hab., 105 unidades, elongación 4.05
  - #180 19 Guadalajara 2: 163.3 km, 95.787 hab., 277 unidades, elongación 1.48
  - #117 10 Cáceres B1 3: 161.8 km, 95.825 hab., 121 unidades, elongación 1.88
  - #160 16 Cuenca 1: 158.1 km, 106.240 hab., 199 unidades, elongación 1.79
  - #138 13 Ciudad Real T1 2: 157.6 km, 95.577 hab., 91 unidades, elongación 2.1
  - #397 42 Soria: 153.9 km, 95.158 hab., 222 unidades, elongación 1.97

## Cruces de frontera provincial

- Distritos con unidades de más de una provincia: **14**
  - #002 01 Araba/Álava 3 (01, 09, 48, 111.946 hab.): 48 Bizkaia T2 (4.243 hab., 3 unidades: Urduña/Orduña sección 01001, Urduña/Orduña sección 01002, Urduña/Orduña sección 02001) se une a 01 Araba/Álava (341.961 hab.): el bloque 48 Bizkaia T2 (4.243 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce provincial dentro de la misma comunidad, estrictamente necesario; opción de mínima población movida) | 09 Burgos T2 (2.034 hab., 2 unidades: Condado de Treviño sección 01001, Puebla de Arganzón, La sección 01001) se une a 01 Araba/Álava (346.204 hab.): el bloque 09 Burgos T2 (2.034 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce entre comunidades autónomas, estrictamente necesario; opción de mínima población movida)
  - #034 05 Ávila 1 (05, 37, 95.016 hab.): 05 Ávila recibe 29.281 hab. (60 unidades: Alaraz sección 01001, Alba de Tormes sección 01001, Alba de Tormes sección 01002, Alba de Tormes sección 01003, Aldeaseca de Alba sección 01001, Aldeatejada sección 01001 … (+54)) de 37 Salamanca: el bloque 05 Ávila (160.738 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce provincial dentro de la misma comunidad, estrictamente necesario; opción de mínima población movida)
  - #113 09 Burgos T1 2 (09, 34, 99.366 hab.): 34 Palencia T3 (45 hab., 1 unidades: Berzosilla sección 01001) se une a 09 Burgos T1 (359.837 hab.): el bloque 34 Palencia T3 (45 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce provincial dentro de la misma comunidad, estrictamente necesario; opción de mínima población movida) | 34 Palencia T2 (100 hab., 1 unidades: Villodrigo sección 01001) se une a 09 Burgos T1 (359.882 hab.): el bloque 34 Palencia T2 (100 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce provincial dentro de la misma comunidad, estrictamente necesario; opción de mínima población movida)
  - #114 09 Burgos T1 3 (09, 34, 98.195 hab.): 34 Palencia T3 (45 hab., 1 unidades: Berzosilla sección 01001) se une a 09 Burgos T1 (359.837 hab.): el bloque 34 Palencia T3 (45 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce provincial dentro de la misma comunidad, estrictamente necesario; opción de mínima población movida) | 34 Palencia T2 (100 hab., 1 unidades: Villodrigo sección 01001) se une a 09 Burgos T1 (359.882 hab.): el bloque 34 Palencia T2 (100 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce provincial dentro de la misma comunidad, estrictamente necesario; opción de mínima población movida)
  - #160 16 Cuenca 1 (16, 46, 106.240 hab.): 46 Valencia/València T2 (2.158 hab., 7 unidades: Ademuz sección 01001, Casas Altas sección 01001, Casas Bajas sección 01001, Castielfabib sección 01001, Puebla de San Miguel sección 01001, Torrebaja sección 01001 … (+1)) se une a 16 Cuenca (199.859 hab.): el bloque 46 Valencia/València T2 (2.158 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce entre comunidades autónomas, estrictamente necesario; opción de mínima población movida)
  - #332 34 Palencia T1 1 (09, 34, 95.004 hab.): 09 Burgos T1 cede 792 hab. (1 unidades: Castrojeriz sección 01001) a 34 Palencia T1: el bloque 09 Burgos T1 (360.629 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce provincial dentro de la misma comunidad, estrictamente necesario; opción de mínima población movida) | 34 Palencia T1 recibe 30.665 hab. (18 unidades: Alfoz de Quintanadueñas sección 01001, Arcos sección 01001, Balbases, Los sección 01001, Burgos sección 03003, Burgos sección 03005, Burgos sección 03006 … (+12)) de 09 Burgos T1: el bloque 34 Palencia T1 (159.349 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce provincial dentro de la misma comunidad, estrictamente necesario; opción de mínima población movida)
  - #378 40 Segovia 2 (09, 40, 95.003 hab.): 40 Segovia recibe 31.752 hab. (23 unidades: Aranda de Duero sección 01001, Aranda de Duero sección 01002, Aranda de Duero sección 01003, Aranda de Duero sección 01004, Aranda de Duero sección 01005, Aranda de Duero sección 01006 … (+17)) de 09 Burgos T1: el bloque 40 Segovia (158.251 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce provincial dentro de la misma comunidad, estrictamente necesario; opción de mínima población movida)
  - #397 42 Soria (09, 42, 95.158 hab.): 42 Soria recibe 4.975 hab. (4 unidades: Aranda de Duero sección 03004, Aranda de Duero sección 03005, Fresnillo de las Dueñas sección 01001, Santa Cruz de la Salceda sección 01001) de 09 Burgos T1: el bloque 42 Soria (90.183 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce provincial dentro de la misma comunidad, estrictamente necesario; opción de mínima población movida)
  - #413 45 Toledo 7 (13, 45, 114.609 hab.): 13 Ciudad Real T2 (265 hab., 1 unidades: Anchuras sección 01001) se une a 45 Toledo (755.081 hab.): el bloque 13 Ciudad Real T2 (265 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce provincial dentro de la misma comunidad, estrictamente necesario; opción de mínima población movida)
  - #450 48 Bizkaia T1 6 (39, 48, 117.946 hab.): 39 Cantabria T2 (249 hab., 1 unidades: Valle de Villaverde sección 01001) se une a 48 Bizkaia T1 (708.931 hab.): el bloque 39 Cantabria T2 (249 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce entre comunidades autónomas, estrictamente necesario; opción de mínima población movida)
  - #455 49 Zamora 1 (47, 49, 95.004 hab.): 47 Valladolid T2 (199 hab., 2 unidades: Quintanilla del Molar sección 01001, Roales de Campos sección 01001) se une a 49 Zamora (165.564 hab.): el bloque 47 Valladolid T2 (199 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce provincial dentro de la misma comunidad, estrictamente necesario; opción de mínima población movida) | 49 Zamora recibe 24.251 hab. (16 unidades: Alaejos sección 01001, Arroyo de la Encomienda sección 01007, Arroyo de la Encomienda sección 01008, Arroyo de la Encomienda sección 01011, Castronuño sección 01001, Medina del Campo sección 03003 … (+10)) de 47 Valladolid T1: el bloque 49 Zamora (165.763 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce provincial dentro de la misma comunidad, estrictamente necesario; opción de mínima población movida)
  - #456 49 Zamora 2 (47, 49, 95.010 hab.): 47 Valladolid T2 (199 hab., 2 unidades: Quintanilla del Molar sección 01001, Roales de Campos sección 01001) se une a 49 Zamora (165.564 hab.): el bloque 47 Valladolid T2 (199 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce provincial dentro de la misma comunidad, estrictamente necesario; opción de mínima población movida) | 49 Zamora recibe 24.251 hab. (16 unidades: Alaejos sección 01001, Arroyo de la Encomienda sección 01007, Arroyo de la Encomienda sección 01008, Arroyo de la Encomienda sección 01011, Castronuño sección 01001, Medina del Campo sección 03003 … (+10)) de 47 Valladolid T1: el bloque 49 Zamora (165.763 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce provincial dentro de la misma comunidad, estrictamente necesario; opción de mínima población movida)
  - #457 50 Zaragoza 1 (44, 50, 116.369 hab.): 44 Teruel cede 16.663 hab. (17 unidades: Albalate del Arzobispo sección 01001, Albalate del Arzobispo sección 01002, Alcañiz sección 03001, Alcañiz sección 03004, Alcañiz sección 03005, Alcañiz sección 04002 … (+11)) a 50 Zaragoza: el bloque 44 Teruel (136.091 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce provincial dentro de la misma comunidad, estrictamente necesario; opción de mínima población movida) | 31 Navarra T2 (29 hab., 1 unidades: Petilla de Aragón sección 01001) se une a 50 Zaragoza (316.099 hab.): el bloque 31 Navarra T2 (29 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce entre comunidades autónomas, estrictamente necesario; opción de mínima población movida)
  - #458 50 Zaragoza 2 (31, 50, 95.558 hab.): 44 Teruel cede 16.663 hab. (17 unidades: Albalate del Arzobispo sección 01001, Albalate del Arzobispo sección 01002, Alcañiz sección 03001, Alcañiz sección 03004, Alcañiz sección 03005, Alcañiz sección 04002 … (+11)) a 50 Zaragoza: el bloque 44 Teruel (136.091 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce provincial dentro de la misma comunidad, estrictamente necesario; opción de mínima población movida) | 31 Navarra T2 (29 hab., 1 unidades: Petilla de Aragón sección 01001) se une a 50 Zaragoza (316.099 hab.): el bloque 31 Navarra T2 (29 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce entre comunidades autónomas, estrictamente necesario; opción de mínima población movida)

Transferencias aplicadas (R5, mínima población movida; nivel 0 = dentro de la provincia, 1 = misma comunidad, 2 = otra comunidad):

- [nivel 0] 10 Cáceres B2 (1.727 hab., 2 unidades: Aliseda sección 01001, Aliseda sección 02001) se une a Cáceres (10 Cáceres) (96.598 hab.): el bloque 10 Cáceres B2 (1.727 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce dentro de la provincia, estrictamente necesario; opción de mínima población movida)
- [nivel 1] 13 Ciudad Real T2 (265 hab., 1 unidades: Anchuras sección 01001) se une a 45 Toledo (755.081 hab.): el bloque 13 Ciudad Real T2 (265 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce provincial dentro de la misma comunidad, estrictamente necesario; opción de mínima población movida)
- [nivel 1] 09 Burgos T1 cede 792 hab. (1 unidades: Castrojeriz sección 01001) a 34 Palencia T1: el bloque 09 Burgos T1 (360.629 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce provincial dentro de la misma comunidad, estrictamente necesario; opción de mínima población movida)
- [nivel 1] 34 Palencia T3 (45 hab., 1 unidades: Berzosilla sección 01001) se une a 09 Burgos T1 (359.837 hab.): el bloque 34 Palencia T3 (45 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce provincial dentro de la misma comunidad, estrictamente necesario; opción de mínima población movida)
- [nivel 1] 34 Palencia T2 (100 hab., 1 unidades: Villodrigo sección 01001) se une a 09 Burgos T1 (359.882 hab.): el bloque 34 Palencia T2 (100 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce provincial dentro de la misma comunidad, estrictamente necesario; opción de mínima población movida)
- [nivel 1] 47 Valladolid T2 (199 hab., 2 unidades: Quintanilla del Molar sección 01001, Roales de Campos sección 01001) se une a 49 Zamora (165.564 hab.): el bloque 47 Valladolid T2 (199 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce provincial dentro de la misma comunidad, estrictamente necesario; opción de mínima población movida)
- [nivel 1] 48 Bizkaia T2 (4.243 hab., 3 unidades: Urduña/Orduña sección 01001, Urduña/Orduña sección 01002, Urduña/Orduña sección 02001) se une a 01 Araba/Álava (341.961 hab.): el bloque 48 Bizkaia T2 (4.243 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce provincial dentro de la misma comunidad, estrictamente necesario; opción de mínima población movida)
- [nivel 1] 42 Soria recibe 4.975 hab. (4 unidades: Aranda de Duero sección 03004, Aranda de Duero sección 03005, Fresnillo de las Dueñas sección 01001, Santa Cruz de la Salceda sección 01001) de 09 Burgos T1: el bloque 42 Soria (90.183 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce provincial dentro de la misma comunidad, estrictamente necesario; opción de mínima población movida)
- [nivel 1] 44 Teruel cede 16.663 hab. (17 unidades: Albalate del Arzobispo sección 01001, Albalate del Arzobispo sección 01002, Alcañiz sección 03001, Alcañiz sección 03004, Alcañiz sección 03005, Alcañiz sección 04002 … (+11)) a 50 Zaragoza: el bloque 44 Teruel (136.091 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce provincial dentro de la misma comunidad, estrictamente necesario; opción de mínima población movida)
- [nivel 1] 49 Zamora recibe 24.251 hab. (16 unidades: Alaejos sección 01001, Arroyo de la Encomienda sección 01007, Arroyo de la Encomienda sección 01008, Arroyo de la Encomienda sección 01011, Castronuño sección 01001, Medina del Campo sección 03003 … (+10)) de 47 Valladolid T1: el bloque 49 Zamora (165.763 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce provincial dentro de la misma comunidad, estrictamente necesario; opción de mínima población movida)
- [nivel 1] 34 Palencia T1 recibe 30.665 hab. (18 unidades: Alfoz de Quintanadueñas sección 01001, Arcos sección 01001, Balbases, Los sección 01001, Burgos sección 03003, Burgos sección 03005, Burgos sección 03006 … (+12)) de 09 Burgos T1: el bloque 34 Palencia T1 (159.349 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce provincial dentro de la misma comunidad, estrictamente necesario; opción de mínima población movida)
- [nivel 1] 40 Segovia recibe 31.752 hab. (23 unidades: Aranda de Duero sección 01001, Aranda de Duero sección 01002, Aranda de Duero sección 01003, Aranda de Duero sección 01004, Aranda de Duero sección 01005, Aranda de Duero sección 01006 … (+17)) de 09 Burgos T1: el bloque 40 Segovia (158.251 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce provincial dentro de la misma comunidad, estrictamente necesario; opción de mínima población movida)
- [nivel 1] 05 Ávila recibe 29.281 hab. (60 unidades: Alaraz sección 01001, Alba de Tormes sección 01001, Alba de Tormes sección 01002, Alba de Tormes sección 01003, Aldeaseca de Alba sección 01001, Aldeatejada sección 01001 … (+54)) de 37 Salamanca: el bloque 05 Ávila (160.738 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce provincial dentro de la misma comunidad, estrictamente necesario; opción de mínima población movida)
- [nivel 2] 31 Navarra T2 (29 hab., 1 unidades: Petilla de Aragón sección 01001) se une a 50 Zaragoza (316.099 hab.): el bloque 31 Navarra T2 (29 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce entre comunidades autónomas, estrictamente necesario; opción de mínima población movida)
- [nivel 2] 39 Cantabria T2 (249 hab., 1 unidades: Valle de Villaverde sección 01001) se une a 48 Bizkaia T1 (708.931 hab.): el bloque 39 Cantabria T2 (249 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce entre comunidades autónomas, estrictamente necesario; opción de mínima población movida)
- [nivel 2] 09 Burgos T2 (2.034 hab., 2 unidades: Condado de Treviño sección 01001, Puebla de Arganzón, La sección 01001) se une a 01 Araba/Álava (346.204 hab.): el bloque 09 Burgos T2 (2.034 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce entre comunidades autónomas, estrictamente necesario; opción de mínima población movida)
- [nivel 2] 46 Valencia/València T2 (2.158 hab., 7 unidades: Ademuz sección 01001, Casas Altas sección 01001, Casas Bajas sección 01001, Castielfabib sección 01001, Puebla de San Miguel sección 01001, Torrebaja sección 01001 … (+1)) se une a 16 Cuenca (199.859 hab.): el bloque 46 Valencia/València T2 (2.158 hab.) no admite partición en [95.000, 120.000] (art. 16, restr. 3: cruce entre comunidades autónomas, estrictamente necesario; opción de mínima población movida)

## P25 de renta por distrito (estimación poblacional sobre rentas medias de unidad)

- Mínimo **8.941 €** (distrito #026 Torrevieja (03 Alicante/Alacant)) | mediana 13.373 € | máximo 27.150 €
- Mínimo entre distritos en rango: 8.941 €
- Comparación v1 (928 distritos): P25 mínimo 7.779 €

## Bloques factibles por suma sin partición contigua en rango


## Bloques municipales (municipios que caben solos, art. 16 restr. 3)

- Municipios resueltos como bloque propio: 44
  - Torrevieja (03 Alicante/Alacant): 100.470 hab., 33 unidades
  - Almería (04 Almería): 204.772 hab., 135 unidades
  - Roquetas de Mar (04 Almería): 110.054 hab., 50 unidades
  - Palma (07 Illes Balears T1): 443.196 hab., 253 unidades
  - Badalona (08 Barcelona): 230.642 hab., 149 unidades
  - Barcelona (08 Barcelona): 1.713.247 hab., 1068 unidades
  - Hospitalet de Llobregat, L' (08 Barcelona): 292.161 hab., 197 unidades
  - Sabadell (08 Barcelona): 224.589 hab., 158 unidades
  - Sant Cugat del Vallès (08 Barcelona): 97.959 hab., 52 unidades
  - Terrassa (08 Barcelona): 232.676 hab., 141 unidades
  - Cáceres (10 Cáceres): 96.598 hab., 74 unidades
  - Cádiz (11 Cádiz): 110.123 hab., 107 unidades
  - Jerez de la Frontera (11 Cádiz): 215.025 hab., 165 unidades
  - Córdoba (14 Córdoba): 324.159 hab., 257 unidades
  - Santiago de Compostela (15 A Coruña): 100.842 hab., 76 unidades
  - Girona (17 Girona): 108.352 hab., 62 unidades
  - Granada (18 Granada): 235.294 hab., 180 unidades
  - Jaén (23 Jaén): 112.119 hab., 88 unidades
  - Lugo (27 Lugo): 100.071 hab., 74 unidades
  - Alcalá de Henares (28 Madrid): 202.549 hab., 129 unidades
  - Getafe (28 Madrid): 195.628 hab., 122 unidades
  - Leganés (28 Madrid): 195.946 hab., 142 unidades
  - Madrid (28 Madrid): 3.477.497 hab., 2462 unidades
  - Móstoles (28 Madrid): 214.293 hab., 139 unidades
  - Rivas-Vaciamadrid (28 Madrid): 103.243 hab., 58 unidades
  - Rozas de Madrid, Las (28 Madrid): 99.579 hab., 50 unidades
  - San Sebastián de los Reyes (28 Madrid): 97.330 hab., 55 unidades
  - Málaga (29 Málaga): 597.173 hab., 435 unidades
  - Cartagena (30 Murcia): 220.400 hab., 182 unidades
  - Lorca (30 Murcia): 98.613 hab., 68 unidades
  - Pamplona/Iruña (31 Navarra T1): 209.676 hab., 151 unidades
  - Ourense (32 Ourense): 105.609 hab., 80 unidades
  - Oviedo (33 Asturias): 223.576 hab., 174 unidades
  - Palmas de Gran Canaria, Las (35 Las Palmas T1): 384.023 hab., 279 unidades
  - Telde (35 Las Palmas T1): 104.933 hab., 67 unidades
  - Vigo (36 Pontevedra T1): 295.735 hab., 241 unidades
  - Santa Cruz de Tenerife (38 Santa Cruz de Tenerife T1): 211.498 hab., 166 unidades
  - Sevilla (41 Sevilla): 688.714 hab., 522 unidades
  - Reus (43 Tarragona): 111.911 hab., 68 unidades
  - València (46 Valencia/València T1): 841.558 hab., 588 unidades
  - … (+4)
- Provincias reconstruidas sin bloques municipales por falta de solución: 30 Murcia

## Excepciones (art. 16, restr. 1 y 4)

- Unidades > máximo sin subunidades (requieren subdivisión por secciones): 0
- Bloques artefacto (provincia factible, resto infactible por las ciudades apartadas): 0
- Territorios aislados ó sin donante viable: 10
  - 07 Illes Balears T2: 164.265 hab. (aislado)
  - 07 Illes Balears T4: 11.690 hab. (aislado)
  - 35 Las Palmas T2: 166.878 hab. (aislado)
  - 35 Las Palmas T3: 129.080 hab. (aislado)
  - 36 Pontevedra T2: 4.813 hab. (aislado)
  - 38 Santa Cruz de Tenerife T2: 86.297 hab. (aislado)
  - 38 Santa Cruz de Tenerife T3: 22.560 hab. (aislado)
  - 38 Santa Cruz de Tenerife T4: 11.993 hab. (aislado)
  - 51 Ceuta: 83.567 hab. (aislado)
  - 52 Melilla: 87.067 hab. (aislado)

## Adyacencias artificiales (unidades sin vecinos en la geometría)

- 0915401001 Hacinas sección 01001 → 0945001001 Villanueva de Carazo sección 01001 (3.5 km)
- 0922301001 Monasterio de la Sierra sección 01001 → 0941401001 Valle de Valdelaguna sección 01001 (6.4 km)
- 1709401001 Llívia sección 01001 → 1714101002 Puigcerdà sección 01002 (5.5 km)
- 3502401010 Teguise sección 01010 → 3501001002 Haría sección 01002 (7.7 km)

## Bloques resueltos

| Bloque | Tipo | Unidades | Nodos | Población | K | Factible | Refinados | Mejoras P25 | s |
|---|---|---:|---:|---:|---:|---|---:|---:|---:|
| 01 Araba/Álava | normal | 245 | 219 | 348.238 | 3 | sí | 23 | 21 | 1.1 |
| 02 Albacete | normal | 296 | 30 | 390.751 | 4 | sí | 0 | 2 | 0.1 |
| 03 Alicante/Alacant | normal | 1205 | 332 | 1.933.096 | 18 | sí | 9 | 29 | 23.0 |
| 04 Almería | normal | 284 | 17 | 455.728 | 4 | sí | 0 | 1 | 0.0 |
| 05 Ávila | normal | 368 | 303 | 190.019 | 2 | sí | 10 | 0 | 2.0 |
| 06 Badajoz | normal | 553 | 33 | 665.155 | 6 | sí | 0 | 1 | 0.0 |
| 07 Illes Balears T1 | normal | 283 | 52 | 527.872 | 5 | sí | 0 | 21 | 0.1 |
| 07 Illes Balears T2 | aislado | 76 | 13 | 164.265 | 2 | sí | 5 | 0 | 0.2 |
| 07 Illes Balears T3 | normal | 56 | 56 | 102.821 | 1 | sí | 0 | 0 | 0.0 |
| 07 Illes Balears T4 | aislado | 6 | 6 | 11.690 | 1 | sí | 0 | 0 | 0.0 |
| 08 Barcelona | normal | 1887 | 309 | 3.168.667 | 29 | sí | 10 | 88 | 91.9 |
| 09 Burgos T1 | normal | 531 | 71 | 292.590 | 3 | sí | 0 | 5 | 0.1 |
| 10 Cáceres B1 | normal | 335 | 221 | 289.865 | 3 | sí | 10 | 2 | 1.0 |
| 11 Cádiz B1 | normal | 554 | 134 | 816.347 | 8 | sí | 17 | 16 | 1.4 |
| 11 Cádiz B2 | normal | 97 | 97 | 119.925 | 1 | sí | 0 | 0 | 0.0 |
| 12 Castellón/Castelló | normal | 447 | 42 | 627.620 | 6 | sí | 0 | 8 | 0.1 |
| 13 Ciudad Real T1 | normal | 417 | 51 | 494.583 | 5 | sí | 0 | 18 | 0.2 |
| 14 Córdoba | normal | 365 | 23 | 449.004 | 4 | sí | 0 | 4 | 0.0 |
| 15 A Coruña | normal | 802 | 78 | 1.034.781 | 10 | sí | 0 | 17 | 0.3 |
| 16 Cuenca | normal | 317 | 245 | 202.017 | 2 | sí | 8 | 58 | 0.9 |
| 17 Girona | normal | 474 | 171 | 722.077 | 7 | sí | 0 | 127 | 0.5 |
| 18 Granada | normal | 494 | 72 | 710.503 | 7 | sí | 0 | 5 | 0.1 |
| 19 Guadalajara | normal | 406 | 73 | 285.839 | 3 | sí | 0 | 25 | 0.2 |
| 20 Gipuzkoa | normal | 544 | 231 | 733.149 | 7 | sí | 23 | 59 | 1.6 |
| 21 Huelva | normal | 374 | 19 | 538.789 | 5 | sí | 0 | 0 | 0.0 |
| 22 Huesca | normal | 287 | 8 | 230.087 | 2 | sí | 0 | 0 | 0.0 |
| 23 Jaén | normal | 410 | 96 | 506.024 | 5 | sí | 9 | 14 | 0.4 |
| 24 León | normal | 444 | 39 | 448.030 | 4 | sí | 0 | 19 | 0.1 |
| 25 Lleida | normal | 387 | 45 | 458.226 | 4 | sí | 0 | 6 | 0.3 |
| 26 La Rioja | normal | 343 | 39 | 326.803 | 3 | sí | 0 | 24 | 0.1 |
| 27 Lugo | normal | 199 | 5 | 225.951 | 2 | sí | 0 | 0 | 0.0 |
| 28 Madrid | normal | 1361 | 350 | 2.527.821 | 24 | sí | 9 | 16 | 62.6 |
| 29 Málaga | normal | 657 | 269 | 1.194.010 | 11 | sí | 17 | 40 | 13.3 |
| 30 Murcia | normal | 1224 | 459 | 1.586.989 | 15 | sí | 61 | 53 | 18.6 |
| 31 Navarra T1 | normal | 430 | 273 | 474.149 | 4 | sí | 46 | 29 | 3.1 |
| 32 Ourense | normal | 176 | 91 | 199.669 | 2 | sí | 3 | 3 | 0.1 |
| 33 Asturias | normal | 652 | 140 | 791.552 | 7 | sí | 25 | 6 | 2.5 |
| 34 Palencia T1 | normal | 290 | 198 | 190.014 | 2 | sí | 9 | 0 | 1.3 |
| 35 Las Palmas T1 | normal | 243 | 243 | 386.633 | 4 | sí | 61 | 19 | 2.3 |
| 35 Las Palmas T2 | aislado | 78 | 78 | 166.878 | 2 | sí | 16 | 1 | 0.6 |
| 35 Las Palmas T3 | aislado | 56 | 56 | 129.080 | 1 | sí | 0 | 0 | 0.0 |
| 36 Pontevedra T1 | normal | 483 | 53 | 647.270 | 6 | sí | 9 | 8 | 1.0 |
| 36 Pontevedra T2 | aislado | 3 | 3 | 4.813 | 1 | sí | 0 | 0 | 0.0 |
| 37 Salamanca | normal | 470 | 71 | 299.165 | 3 | sí | 0 | 56 | 0.3 |
| 38 Santa Cruz de Tenerife T1 | normal | 436 | 35 | 754.971 | 7 | sí | 0 | 7 | 0.2 |
| 38 Santa Cruz de Tenerife T2 | aislado | 61 | 61 | 86.297 | 1 | sí | 0 | 0 | 0.0 |
| 38 Santa Cruz de Tenerife T3 | aislado | 15 | 15 | 22.560 | 1 | sí | 0 | 0 | 0.0 |
| 38 Santa Cruz de Tenerife T4 | aislado | 6 | 6 | 11.993 | 1 | sí | 0 | 0 | 0.0 |
| 39 Cantabria T1 | normal | 457 | 64 | 593.374 | 6 | sí | 0 | 8 | 1.4 |
| 40 Segovia | normal | 299 | 213 | 190.003 | 2 | sí | 4 | 0 | 0.1 |
| 41 Sevilla | normal | 855 | 70 | 1.288.950 | 12 | sí | 0 | 16 | 1.9 |
| 42 Soria | normal | 222 | 222 | 95.158 | 1 | sí | 0 | 0 | 0.0 |
| 43 Tarragona | normal | 500 | 119 | 763.619 | 7 | sí | 0 | 67 | 0.2 |
| 44 Teruel | normal | 267 | 267 | 119.428 | 1 | sí | 0 | 0 | 0.0 |
| 45 Toledo | normal | 532 | 135 | 755.346 | 7 | sí | 0 | 59 | 0.4 |
| 46 Valencia/València T1 | normal | 1235 | 214 | 1.920.280 | 18 | sí | 49 | 66 | 27.9 |
| 47 Valladolid T1 | normal | 295 | 217 | 202.396 | 2 | sí | 4 | 19 | 0.7 |
| 48 Bizkaia T1 | normal | 564 | 105 | 709.180 | 7 | sí | 19 | 0 | 2.6 |
| 49 Zamora | normal | 333 | 259 | 190.014 | 2 | sí | 9 | 0 | 0.7 |
| 50 Zaragoza | normal | 408 | 68 | 316.128 | 3 | sí | 0 | 0 | 0.2 |
| 51 Ceuta | aislado | 56 | 56 | 83.567 | 1 | sí | 0 | 0 | 0.0 |
| 52 Melilla | aislado | 44 | 44 | 87.067 | 1 | sí | 0 | 0 | 0.0 |
| Alcalá de Henares (28 Madrid) | normal | 129 | 5 | 202.549 | 2 | sí | 0 | 0 | 0.0 |
| Almería (04 Almería) | normal | 135 | 8 | 204.772 | 2 | sí | 0 | 0 | 0.0 |
| Badalona (08 Barcelona) | normal | 149 | 9 | 230.642 | 2 | sí | 0 | 0 | 0.0 |
| Barakaldo (48 Bizkaia T1) | normal | 86 | 86 | 103.084 | 1 | sí | 0 | 0 | 0.0 |
| Barcelona (08 Barcelona) | normal | 1068 | 959 | 1.713.247 | 16 | sí | 0 | 21 | 5.7 |
| Bilbao (48 Bizkaia T1) | normal | 271 | 271 | 350.975 | 3 | sí | 8 | 35 | 1.1 |
| Cáceres (10 Cáceres) | normal | 76 | 76 | 98.325 | 1 | sí | 0 | 0 | 0.0 |
| Cádiz (11 Cádiz) | normal | 107 | 107 | 110.123 | 1 | sí | 0 | 0 | 0.0 |
| Córdoba (14 Córdoba) | normal | 257 | 10 | 324.159 | 3 | sí | 0 | 1 | 0.0 |
| Getafe (28 Madrid) | normal | 122 | 122 | 195.628 | 2 | sí | 4 | 30 | 0.4 |
| Girona (17 Girona) | normal | 62 | 62 | 108.352 | 1 | sí | 0 | 0 | 0.0 |
| Granada (18 Granada) | normal | 180 | 9 | 235.294 | 2 | sí | 0 | 1 | 0.0 |
| Hospitalet de Llobregat, L' (08 Barcelona) | normal | 197 | 197 | 292.161 | 3 | sí | 6 | 70 | 0.4 |
| Jaén (23 Jaén) | normal | 88 | 88 | 112.119 | 1 | sí | 0 | 0 | 0.0 |
| Jerez de la Frontera (11 Cádiz) | normal | 165 | 10 | 215.025 | 2 | sí | 0 | 3 | 0.0 |
| Leganés (28 Madrid) | normal | 142 | 7 | 195.946 | 2 | sí | 0 | 0 | 0.0 |
| Lugo (27 Lugo) | normal | 74 | 74 | 100.071 | 1 | sí | 0 | 0 | 0.0 |
| Madrid (28 Madrid) | normal | 2462 | 2202 | 3.477.497 | 32 | sí | 0 | 444 | 8.9 |
| Málaga (29 Málaga) | normal | 435 | 173 | 597.173 | 6 | sí | 0 | 104 | 0.6 |
| Móstoles (28 Madrid) | normal | 139 | 4 | 214.293 | 2 | sí | 0 | 0 | 0.0 |
| Ourense (32 Ourense) | normal | 80 | 80 | 105.609 | 1 | sí | 0 | 0 | 0.0 |
| Oviedo (33 Asturias) | normal | 174 | 16 | 223.576 | 2 | sí | 0 | 0 | 0.0 |
| Palma (07 Illes Balears T1) | normal | 253 | 159 | 443.196 | 4 | sí | 0 | 21 | 0.3 |
| Palmas de Gran Canaria, Las (35 Las Palmas T1) | normal | 279 | 279 | 384.023 | 4 | sí | 5 | 110 | 0.6 |
| Pamplona/Iruña (31 Navarra T1) | normal | 151 | 8 | 209.676 | 2 | sí | 0 | 0 | 0.0 |
| Reus (43 Tarragona) | normal | 68 | 68 | 111.911 | 1 | sí | 0 | 0 | 0.0 |
| Rivas-Vaciamadrid (28 Madrid) | normal | 58 | 58 | 103.243 | 1 | sí | 0 | 0 | 0.0 |
| Roquetas de Mar (04 Almería) | normal | 50 | 50 | 110.054 | 1 | sí | 0 | 0 | 0.0 |
| Rozas de Madrid, Las (28 Madrid) | normal | 50 | 50 | 99.579 | 1 | sí | 0 | 0 | 0.0 |
| Sabadell (08 Barcelona) | normal | 158 | 7 | 224.589 | 2 | sí | 0 | 0 | 0.0 |
| San Sebastián de los Reyes (28 Madrid) | normal | 55 | 55 | 97.330 | 1 | sí | 0 | 0 | 0.0 |
| Sant Cugat del Vallès (08 Barcelona) | normal | 52 | 52 | 97.959 | 1 | sí | 0 | 0 | 0.0 |
| Santa Cruz de Tenerife (38 Santa Cruz de Tenerife T1) | normal | 166 | 12 | 211.498 | 2 | sí | 0 | 0 | 0.0 |
| Santiago de Compostela (15 A Coruña) | normal | 76 | 76 | 100.842 | 1 | sí | 0 | 0 | 0.0 |
| Sevilla (41 Sevilla) | normal | 522 | 522 | 688.714 | 6 | sí | 11 | 120 | 2.5 |
| Telde (35 Las Palmas T1) | normal | 67 | 67 | 104.933 | 1 | sí | 0 | 0 | 0.0 |
| Terrassa (08 Barcelona) | normal | 141 | 7 | 232.676 | 2 | sí | 0 | 0 | 0.0 |
| Torrevieja (03 Alicante/Alacant) | normal | 33 | 33 | 100.470 | 1 | sí | 0 | 0 | 0.0 |
| Valladolid (47 Valladolid T1) | normal | 252 | 13 | 301.798 | 3 | sí | 0 | 0 | 0.0 |
| València (46 Valencia/València T1) | normal | 588 | 588 | 841.558 | 8 | sí | 19 | 2 | 2.7 |
| Vigo (36 Pontevedra T1) | normal | 241 | 241 | 295.735 | 3 | sí | 9 | 71 | 0.8 |
| Zaragoza (50 Zaragoza) | normal | 502 | 103 | 699.007 | 7 | sí | 0 | 3 | 0.2 |

## Verificación

- Unidades asignadas exactamente una vez: sí
- Distritos no contiguos (BFS sobre `vecinos`): []
- Suma de poblaciones de distritos = población total: sí
