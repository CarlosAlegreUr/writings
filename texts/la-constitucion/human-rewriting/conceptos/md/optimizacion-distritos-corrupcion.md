# Optimización de Distritos por Coste de Corrupción (Algoritmo P25)

## Definición

Algoritmo económico para determinar tamaño óptimo de distritos electorales, maximizando el coste mínimo estructural de corrupción.

**Objetivo:** Maximizar el coste para capturar un distrito bajo condiciones realistas.

**Método:**
1. Peor caso asumido: Capturar distrito requiere influir en ~25% de población (relacionado con umbral 75%)
2. Proxy económico: Percentil 25 (P25) de renta/salario del distrito = "precio" del tramo más vulnerable
3. Partir de provincias (respeto histórico-cultural)
4. Dividir en sectores de ~100.000 habitantes
5. Calcular P25 de cada sector
6. Heurística: Maximizar Σ P25_i de todos los distritos

**Constraints:**
- No romper provincias
- Continuidad geográfica
- Tamaño variable permitido: 95k-120k habitantes

## Contexto

Mejora sobre propuesta de Trevijano (~100.000 habitantes basado en estudios lingüísticos):

> "Problema de Trevijano: Fijó ~100.000 habitantes basándose en estudios lingüísticos (supervivencia de lenguas). Esto es arbitrario y no es universal."
> — Notas de Sesión 1

**Ventajas del algoritmo:**
- No es caprichoso (lógica económica defensiva)
- Se adapta a cambios económicos y demográficos
- Dificulta ingeniería demográfica (tarda 21 años en actualizarse)

## Relaciones

**Depende de:** [[representacion-responsable]]
**Usado en:** Partes 3, 4
**Relacionado con:** [[actualizacion-distrital-21-anos]]
**Fuentes:** Notas de Sesión 0

---
*Última actualización: 2026-01-06*
