# Dataset Card · territorial_risk_synthetic

**INF-8239 Ciencia de Datos II · Unidad 04** · Alexis De La Cruz · 100805370

> **Advertencia del proyecto base, que mantengo tal cual.** Conjunto sintético generado con
> una semilla educativa fija. **No contiene personas, lugares, tasas ni estadísticas
> oficiales reales de la República Dominicana.** Sirve únicamente para practicar contratos
> de datos, evaluación temporal, auditoría por subgrupos y gobernanza. Queda prohibido
> usarlo para perfilado operativo o para inferir nada sobre poblaciones reales.

## Procedencia

| | |
|---|---|
| Origen | Generado por el proyecto base del curso (autor: Edwin Ramón José Nolasco) |
| Archivo | `data/territorial_risk_synthetic.csv` |
| Tamaño | 640 filas × 9 columnas |
| Versionado | Dentro del repositorio, porque es sintético y pequeño; con datos reales **no** se versionaría |
| Contrato | `src/inf8239_u04/data.py` · `validate_schema` |

## Composición

| | |
|---|---|
| Variable objetivo | `target` binaria · 55.2 % positivos, 44.8 % negativos |
| Grupos protegidos | G1 con 396 casos, G2 con 244 |
| Tramos de edad | 18-29, 30-44, 45-59, 60+ |
| Zonas | Norte, Sur, Este, Oeste, entre 155 y 164 casos cada una |
| Rango temporal | 2026-01-01 a 2026-12-27 |

El desbalance de la variable objetivo es moderado pero suficiente para que la exactitud
global sea insuficiente como métrica única: por eso la auditoría usa recall, FPR y tasa de
selección **por grupo**.

## Inventario, minimización y retención

El detalle columna por columna, con sensibilidad, justificación y plazo, está en
[`INVENTARIO_DATOS.md`](INVENTARIO_DATOS.md). Lo esencial:

- **Sin identificadores directos.** Nombre, documento, correo y teléfono están prohibidos
  por contrato y `tests/test_privacy.py` comprueba el rechazo.
- **Edad en tramos**, no exacta.
- **`protected_group` nunca entra al modelo**: se conserva solo para auditar.
- **Retención de 2 años** desde el cierre del caso, con responsable de borrado asignado en
  el RACI.

## Particiones

Cronológica, no aleatoria: 480 casos hasta 2026-09-24 para entrenar y 160 desde 2026-09-25
para probar. Evalúa con datos posteriores a los de entrenamiento, que es como se comportaría
el sistema en uso.

## Sesgos conocidos y límites

- **Es sintético.** No representa ninguna población real, y ninguna conclusión de esta
  auditoría se traslada a datos reales.
- **El soporte interseccional es insuficiente.** Al cruzar grupo y tramo de edad, siete de
  las ocho celdas del conjunto de prueba quedan por debajo de 30 casos y dos tienen solo 2
  casos negativos. No permite auditar a ese nivel.
- **Quitar el atributo sensible no elimina el sesgo.** `zone`, `age_band` y el historial de
  incidentes pueden correlacionar con el grupo protegido.
- **Las etiquetas vienen de un proceso que no se observa.** Con datos reales, `target`
  reflejaría decisiones humanas previas y podría arrastrar sus sesgos; el modelo aprendería
  a reproducirlos. Con datos sintéticos esto no se puede comprobar.

## Mantenimiento

| | |
|---|---|
| Responsable del contrato de datos | Data Engineer, con el Product Owner como aprobador |
| Verificación | `uv run python scripts/check_environment.py` y `tests/test_data.py` |
| Cambios de esquema | Rompen `tests/test_inventory.py` si no se documentan en el inventario |

## Licencia y uso

Material académico del curso INF-8239. El conjunto pertenece al proyecto base y se usa aquí
con fines didácticos.
