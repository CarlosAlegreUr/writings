# AOCD — Simulación con Datos Reales de España

**Estado: Boceto inicial. Primera iteración funcional con limitaciones conocidas.**

Este directorio contiene la simulación del Algoritmo de Optimización de la Corruptibilidad de Distritos (AOCD) aplicado a datos reales de España. El AOCD está descrito en el Artículo 14 de la Constitución Democrática.

## Resultado

![Mapa de distritos electorales](output/aocd_mapa_espana.png)

- **8.131 municipios** procesados
- **48.583.241 habitantes** (Padrón 2024)
- **928 distritos** generados (objetivo constitucional: ~452)
- **P25 mínimo: 7.779€** (renta neta media por persona)

## Estructura

```
aocd/
├── data/                          # Datasets de entrada
│   ├── poblacion_municipios_2024.csv   # INE Padrón 2024 (8.132 municipios)
│   ├── renta_municipios_2022.csv       # INE Atlas de Renta 2022 (8.064 municipios)
│   └── spain_municipios_full.geojson   # Geometría municipal (OpenDataSoft, 72MB)
├── scripts/                       # Scripts del pipeline
│   ├── aocd_preparar_datos.py     # Cruza los 3 datasets → JSON unificado
│   ├── aocd_simulacion.py         # Algoritmo AOCD (partición + recocido simulado)
│   └── aocd_mapa.py               # Genera mapa coloreado con geopandas
├── output/                        # Resultados
│   ├── aocd_resultado_espana.json # Asignación municipio → distrito
│   ├── aocd_resultado_sintetico.json  # Resultado con datos sintéticos (referencia)
│   └── aocd_mapa_espana.png       # Mapa de distritos
└── README.md                      # Este archivo
```

## Ejecución

```bash
cd aocd/scripts

# 1. Preparar datos (cruza población + renta + geometría)
python3 aocd_preparar_datos.py

# 2. Ejecutar AOCD (partición inicial + recocido simulado)
python3 aocd_simulacion.py

# 3. Generar mapa
python3 aocd_mapa.py
```

Dependencias: `pip install geopandas matplotlib shapely numpy`

## Fuentes de datos

| Dato | Fuente | Año | Cobertura |
|------|--------|-----|-----------|
| Población por municipio | INE — Cifras Oficiales del Padrón (tabla 29005) | 2024 | 8.132 municipios |
| Renta media por persona | INE — Atlas de Distribución de Renta (tablas 30824+) | 2022 | 8.064 municipios (52 provincias) |
| Geometría municipal | OpenDataSoft — georef-spain-municipio | 2022 | 8.223 features |

Para los 68 municipios sin datos de renta directa, se usó la media provincial correspondiente.

## Lo que funciona

- **Cruce de datos**: los 3 datasets se cruzan correctamente por código municipal INE (5 dígitos). 8.131 municipios con los 3 datos disponibles.
- **Adyacencia geográfica real**: calculada desde los polígonos del GeoJSON en 2 segundos. Media de 6 vecinos por municipio.
- **Partición inicial**: agrupa municipios contiguos empezando por los más poblados. Completada en <1 segundo.
- **Recocido simulado optimizado**: evaluación incremental (solo recalcula los 2 distritos afectados por cada movimiento). 100.000 iteraciones en 15 segundos.
- **Mapa**: España reconocible con distritos coloreados, separación península/Canarias.

## Limitaciones conocidas (primera iteración)

### 1. Demasiados distritos (928 vs ~452)
La partición inicial crea un distrito por cada semilla que no puede expandirse más. España tiene miles de municipios rurales de <100 habitantes que quedan como distritos diminutos. **El algoritmo no tiene fase de fusión**: el recocido solo mueve municipios entre fronteras, no fusiona distritos enteros.

### 2. 680 distritos fuera del rango constitucional (95.000-120.000 hab)
Consecuencia directa del punto anterior. La mayoría son distritos rurales con <10.000 habitantes.

### 3. El recocido simulado no mejora el objetivo (0 mejoras)
Con 928 distritos fragmentados, mover un municipio individual no cambia el P25 mínimo global. El mínimo está en distritos rurales diminutos que el recocido no puede fusionar.

### 4. 7 municipios sin vecinos geográficos
Formentera, Llívia (enclave en Francia), Isla de Arousa, Ceuta, Melilla, y 2 de Burgos. Forman distritos solitarios por la excepción geográfica del Art 14.

### 5. Datos de renta a nivel municipal (no individual)
El P25 se calcula con la renta media municipal ponderada por población, no con distribuciones individuales de renta. Esto suaviza las diferencias reales dentro de cada municipio.

### 6. Geometría de 2022 (no 2024)
El GeoJSON de OpenDataSoft es de 2022. Puede haber fusiones/segregaciones municipales entre 2022 y 2024.

### 7. No se respetan fronteras comarcales
El algoritmo no tiene datos de comarcas. La Constitución (Art 14) exige que la delimitación respete fronteras provinciales, municipales o comarcales. En esta iteración, los distritos pueden partir comarcas: por ejemplo, la comarca del Matarraña (Teruel) tiene municipios repartidos en distintos distritos en vez de mantenerse unida. Esto contradice el principio de coherencia histórico-cultural.

### 8. Distritos que cruzan varias provincias de forma sospechosa
Algunos distritos abarcan municipios de 5-6 provincias distintas (ej: Distrito #404 con municipios de Teruel, Castellón, Guadalajara, Soria, Zaragoza y Tarragona). Esto sugiere problemas en la verificación de contigüidad geográfica real — un distrito que va de Castellón a Soria no es geográficamente coherente.

## Mejoras para una versión de producción

### Siguiente iteración recomendada: granularidad comarcal híbrida

La mejora más impactante sería usar comarcas como unidad base en zonas rurales y municipios en comarcas urbanas grandes:

- **Comarcas pequeñas** (<95.000 hab): tratar la comarca como unidad indivisible y agrupar comarcas vecinas hasta alcanzar el rango constitucional. Esto respeta automáticamente las fronteras comarcales.
- **Comarcas grandes** (>120.000 hab): mantener la granularidad municipal dentro de la comarca y subdividir internamente.

Esto reduciría las unidades de ~8.131 municipios a ~300-400 comarcas, haciendo el algoritmo más rápido y los resultados más realistas. Requiere un dataset que asigne cada municipio a su comarca.

### Otras mejoras

1. **Fase de fusión pre-recocido**: unir distritos contiguos pequeños hasta alcanzar el rango de 95.000-120.000 antes de optimizar.
2. **Movimientos agresivos**: mover grupos de municipios o fusionar/dividir distritos completos durante el recocido.
3. **Datos de renta por sección censal**: el INE tiene datos más granulares que permitirían un P25 más preciso.
4. **Geometría oficial del IGN**: más precisa que OpenDataSoft, con fronteras exactas.
5. **Coloración de grafos**: asignar colores evitando que distritos vecinos compartan color.
6. **Verificación de contigüidad más estricta**: limitar distritos a máximo 2-3 provincias para evitar resultados geográficamente absurdos.

## Conclusión

Esta simulación es un boceto inicial que demuestra la viabilidad del AOCD con datos reales: el cruce de datos funciona, la adyacencia se calcula, y el mapa se genera. El resultado no es óptimo — los distritos son demasiados, no respetan comarcas, y algunos cruzan provincias de forma inverosímil — pero valida que el algoritmo constitucional es implementable con datos públicos del INE y geometría abierta. La siguiente iteración con granularidad comarcal híbrida debería producir resultados significativamente más realistas.
