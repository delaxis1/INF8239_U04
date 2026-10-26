# Model Card · DSS territorial sintético

**INF-8239 Ciencia de Datos II · Unidad 04 · Ejercicio 08** · Alexis De La Cruz · 100805370

| | |
|---|---|
| Modelo | Regresión logística con `class_weight="balanced"`, semilla 42 |
| Preprocesamiento | `OneHotEncoder` para `zone` y `age_band`; `StandardScaler` para las tres numéricas |
| Versión | Etiqueta `u04-lab13` del repositorio |
| Artefacto | `models/logistic.joblib`, 3.56 KB |
| Construido por | `src/inf8239_u04/model.py`, ejecutado por `scripts/lab12_audit.py` |
| Fecha de evaluación | 26 de octubre de 2026 |
| Responsable final | Institutional Owner del área de revisión territorial |

## Uso previsto

**Ordenar casos para revisión humana.** El modelo produce una prioridad; la decisión de
revisar, intervenir o archivar la toma siempre una persona, y queda registrada junto a la
propuesta del sistema.

## Usos fuera de alcance

Prohibidos en `configs/governance.yml` y verificables ahí:

- **Intervención automática.** Ninguna acción puede dispararse sin revisión humana.
- **Decisión de elegibilidad.** El modelo no determina si alguien tiene derecho a algo.
- **Declaratoria de emergencia.**
- **Evaluar a una persona fuera del ciclo de revisión**, construir listas persistentes o
  justificar una decisión ya tomada por otra vía.

## Datos y partición

| | |
|---|---|
| Conjunto | `data/territorial_risk_synthetic.csv` · 640 filas · **sintético** |
| Ficha de datos | `docs/DATASET_CARD.md` · inventario en `docs/INVENTARIO_DATOS.md` |
| Entrenamiento | 480 casos, 2026-01-01 a 2026-09-24 |
| Prueba | 160 casos, 2026-09-25 a 2026-12-27 |
| Partición | **Cronológica**, no aleatoria: no evalúa el pasado con el futuro |
| Variables | `zone`, `age_band`, `previous_incidents`, `infrastructure_score`, `exposure` |
| Excluidas | `case_id`, `received_date`, `protected_group`, `target` |

`protected_group` se conserva **solo para auditar** y nunca entra al modelo.

## Evaluación global y por subgrupo

| Métrica | Global | G1 (n=101) | G2 (n=59) | Brecha | Techo |
|---|---|---|---|---|---|
| Exactitud | 0.719 | 0.703 | 0.746 | 0.043 | — |
| Recall | 0.717 | 0.653 | 0.791 | **0.138** | 0.16 |
| Precisión | 0.776 | 0.711 | 0.850 | 0.139 | — |
| FPR | 0.279 | 0.250 | 0.375 | 0.125 | 0.16 |
| Tasa de selección | 0.531 | 0.446 | 0.678 | 0.232 | — |

Trazabilidad: `reports/lab12/logistic/global_metrics.json` y `fairness_by_group.csv`,
generados por `scripts/lab12_audit.py --model logistic`.

**Interseccional:** siete de las ocho celdas de grupo × tramo de edad quedan por debajo
del soporte mínimo declarado de 30 casos; dos tienen solo 2 casos negativos. **No se
interpretan.** La lectura válida es que falta dato para auditar a ese nivel.

## Evidencia Green AI

| Alternativa | Exactitud | Recall | FPR | Selección | Brecha recall | Entrenamiento | Tamaño |
|---|---|---|---|---|---|---|---|
| Regla manual (incidentes ≥ 3) | 0.675 | 0.837 | 0.544 | 0.713 | 0.131 | 0 s | 0 KB |
| Marcar todo | 0.575 | 1.000 | 1.000 | 1.000 | 0.000 | 0 s | 0 KB |
| **Logística (elegida)** | **0.719** | 0.717 | 0.279 | 0.531 | 0.138 | 0.050 s | 3.56 KB |
| Árbol de decisión | 0.706 | 0.717 | 0.309 | 0.544 | 0.181 | 0.014 s | 7.87 KB |

Trazabilidad: `reports/lab12/comparison.csv`, generado por
`scripts/compare_alternatives.py`.

A esta escala el costo computacional no decide nada: el modelo más pesado ocupa 7.87 KB. El
costo que sí decide es humano, y se mide en la columna de selección: 53 % de casos marcados
frente al 71 % de la regla manual son unas 29 revisiones menos por cada 100 casos.

## Limitaciones, supervisión humana y apelación

- **La alternativa no predictiva atiende mejor al grupo que se eligió proteger.** La regla
  manual alcanza recall 0.898 en G1 frente a 0.653 del modelo. La única ventaja del modelo
  es marcar menos casos. Por eso la decisión es **limitar** y no desplegar.
- **Las compuertas de `governance.yml` aprueban la regla trivial de marcar a todo el
  mundo**, porque no acotan FPR ni precisión. Es un hueco del marco, declarado, con
  propuesta de cierre.
- **La brecha de 0.138 viene de una sola partición de 160 casos**, sin intervalos ni
  repetición con otras semillas.
- **Una brecha no prueba discriminación causal**; indica dónde investigar.
- **Los datos son sintéticos.** Nada de esto estima el comportamiento sobre población real.
- **Supervisión humana:** revisión obligatoria de cada caso marcado, con la decisión del
  operador registrada junto a la del sistema y la tasa de coincidencia medida cada mes.
- **Apelación:** derecho a conocer el motivo, corregir un dato y pedir una segunda revisión
  humana distinta de la primera, conservando la versión del modelo y los datos que
  produjeron la marca.

## Monitoreo

Señales, umbrales y frecuencia están en `docs/RUNBOOK.md`. El resumen: brecha de recall por
encima de 0.16 o recall global por debajo de 0.68 disparan retiro inmediato.

## Decisión de despliegue

**Limitar.** Usar el modelo **solo si la capacidad de revisión es el límite real de la
institución**, declarado por escrito por el responsable institucional. Si no lo es, la
decisión correcta es no utilizarlo y quedarse con la regla manual.

`reports/lab13/deployment_decision.json` registra que las cinco compuertas automáticas dan
**GO**. La decisión gobernada es **más estricta que la máquina**, y esa diferencia es
deliberada: pasar una compuerta no demuestra que el sistema sea necesario.

## Fecha de revisión

Reauditoría mensual sobre la ventana más reciente. Revisión completa de esta ficha en cada
reentrenamiento o cambio de umbral, y en todo caso antes del 26 de octubre de 2027.
