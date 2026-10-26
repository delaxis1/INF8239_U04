# Registro de decisión · Ejercicio 07 (LAB11 + LAB12)

**INF-8239 Ciencia de Datos II · Unidad 04** · Alexis De La Cruz · 100805370

Sistema auditado: DSS territorial sintético que **ordena** casos para revisión humana. No
interviene, no decide elegibilidad y no declara emergencias; eso está prohibido en
`configs/governance.yml`.

## Decisión final

**LIMITAR.** De las cuatro opciones del mandato —desplegar, modificar, limitar o no
utilizar— esta es la que sostiene la evidencia.

El modelo logístico se usa **solo si la capacidad de revisión es el límite real de la
institución**, y esa condición la declara por escrito el responsable institucional antes de
cualquier despliegue. Si la capacidad de revisión no es el cuello de botella, la decisión
correcta es **no utilizar** el modelo y quedarse con la regla manual.

La razón es incómoda y es el hallazgo principal del ejercicio: **para el daño que prioricé,
la alternativa no predictiva le gana al modelo.**

| Para G1 (n=101) | Regla manual | Logística |
|---|---|---|
| Recall | **0.898** | 0.653 |
| Casos sin marcar por cada 100 | **10** | 35 |
| FPR | 0.519 | 0.250 |
| Casos marcados en total | 71.3 % | 53.1 % |

La regla manual incluso tiene una brecha de recall menor, 0.131 frente a 0.138. Lo único
que compra el modelo es **proporcionalidad**: marca 18 puntos menos de casos y casi reduce
a la mitad los falsos positivos. Eso es capacidad de revisión ahorrada, no menos daño para
G1. Un modelo que usa más datos y más cómputo para atender *peor* al grupo que dije querer
proteger no pasa el test de necesidad, salvo que lo que escasee sea precisamente la
capacidad de revisar.

Entre los dos modelos recomiendo la **logística** y descarto el **árbol**: viola dos
compuertas de equidad —brecha de recall 0.181 y brecha de FPR 0.168, ambas por encima del
techo de 0.16— y además es menos exacto, 0.706 frente a 0.719. No hay nada que ganar
aceptándolo.

## Daño prioritario

Que una persona del grupo G1 cuyo caso **sí** requiere revisión quede sin marcar y por
tanto sin atención.

Lo elijo por encima del sobre-marcado de G2 porque el sistema solo ordena una cola: un
falso positivo cuesta una revisión de más, que el operador descarta en minutos, mientras un
falso negativo cuesta un caso desatendido que nadie vuelve a mirar. Los dos daños existen,
los dos están medidos y **no se pueden minimizar a la vez con el mismo umbral**. Esta
elección es mía y es la que ordena todo lo demás: la métrica, la tolerancia, la línea base
contra la que se compara y la decisión final.

## Evidencia

Generada por `scripts/lab12_audit.py` y `scripts/compare_alternatives.py` sobre los 160
casos de prueba de la partición cronológica (25 sep – 27 dic de 2026, entrenando con 480
casos del 1 ene al 24 sep). Ninguna cifra está escrita a mano.

### Por grupo protegido · regresión logística

| Métrica | G1 (n=101) | G2 (n=59) | Brecha | Techo |
|---|---|---|---|---|
| Recall | 0.653 | 0.791 | **0.138** | 0.16 |
| FPR | 0.250 | 0.375 | 0.125 | 0.16 |
| Tasa de selección | 0.446 | 0.678 | 0.232 | — |
| Precisión | 0.711 | 0.850 | 0.139 | — |
| Exactitud | 0.703 | 0.746 | 0.043 | — |

Recall global 0.717 (mínimo 0.68) · 0.014 ms por caso · 3.56 KB. Las cinco compuertas
pasan: `reports/lab12/logistic/global_metrics.json`.

### Comparación con líneas base · Green AI

| Alternativa | Exactitud | Recall | FPR | Selección | Brecha recall | Entrenamiento | Tamaño | Compuertas |
|---|---|---|---|---|---|---|---|---|
| Regla manual (`previous_incidents >= 3`) | 0.675 | 0.837 | 0.544 | 0.713 | 0.131 | 0 s | 0 KB | Pasa |
| Marcar todo | 0.575 | 1.000 | 1.000 | 1.000 | 0.000 | 0 s | 0 KB | **Pasa** |
| **Logística** | **0.719** | 0.717 | 0.279 | 0.531 | 0.138 | 0.050 s | 3.56 KB | Pasa |
| Árbol | 0.706 | 0.717 | 0.309 | 0.544 | 0.181 | 0.014 s | 7.87 KB | **Falla 2** |

Lectura Green AI: el modelo más costoso de los cuatro cuesta 3.56 KB y 50 milésimas de
segundo. **El costo computacional no es el criterio que decide aquí**; a esta escala es
irrelevante, y pretender lo contrario sería inventar una justificación. Lo que sí decide es
el costo *humano*: 71 % de casos marcados frente a 53 % son 29 revisiones más por cada 100
casos, y eso lo paga el equipo operativo.

## Incertidumbre

Cuatro cosas que la evidencia **no** permite afirmar, declaradas para que nadie lea esta
auditoría como un sello de aprobación:

1. **Las compuertas aprueban marcar a todo el mundo.** `marcar_todo` obtiene recall 1.0 y
   brechas 0.0, así que pasa las cinco. Las compuertas de `governance.yml` fijan un recall
   mínimo y brechas máximas, pero **no acotan FPR ni precisión**. Es un hueco del marco de
   gobernanza, no un detalle: significa que pasar las compuertas no demuestra nada por sí
   solo. Propongo añadir una compuerta de FPR máximo y otra de precisión mínima.
2. **El desglose interseccional no es interpretable en tres de las ocho celdas.**
   G2 | 30-44 y G2 | 45-59 tienen 2 casos negativos, y G2 | 18-29 tiene 3. El FPR de 1.000
   que aparece ahí en el árbol son **dos casos de dos**: un solo caso mueve la cifra 50
   puntos. Declaro un soporte mínimo de 30 casos por celda y no concluyo nada por debajo.
   La conclusión válida es que **falta dato para auditar a ese nivel**.
3. **La brecha de 0.138 viene de una sola partición de 160 casos**, sin intervalo de
   confianza ni repetición con otras semillas. La distancia real al techo de 0.16 es más
   incierta que lo que sugiere un margen de 0.022.
4. **Una brecha observada no prueba discriminación causal.** Indica dónde investigar: puede
   venir del muestreo, de la relación entre las variables disponibles y el grupo, o del
   propio proceso que generó las etiquetas. Con datos sintéticos no es posible distinguirlo,
   y los datos son sintéticos, así que nada de esto estima el comportamiento real.

## Responsables

| Qué | Quién |
|---|---|
| Aprueba, condiciona o suspende el uso | Responsable institucional del área de revisión territorial |
| Declara por escrito si la capacidad de revisión es el límite real | Responsable institucional |
| Operación diaria y umbral | Product Owner |
| Auditoría de equidad en cada reentrenamiento | Data Scientist |
| Reauditoría mensual y alerta de compuertas | ML Engineer |
| Apelaciones | Responsable institucional, con apoyo legal |

En un despliegue real estos campos deben constar con nombre, cargo y correo. Aquí son roles
tomados de `student_inputs/raci.csv`, no una asignación institucional real.

## Condiciones del uso limitado

1. **Declaración previa por escrito** de que la capacidad de revisión es el límite real. Sin
   ella la decisión es no utilizar el modelo.
2. **Revisión humana obligatoria de cada caso marcado**, sin ninguna acción automática. La
   decisión del operador se registra junto a la propuesta del sistema.
3. **Añadir a `governance.yml` una compuerta de FPR máximo y otra de precisión mínima**,
   porque sin ellas el marco aprueba marcar a todo el mundo.
4. **Reauditoría mensual de la brecha de recall** sobre la ventana más reciente, con
   **retiro inmediato si supera 0.16** o si el recall global baja de 0.68. El retiro lo
   ejecuta el responsable institucional y no requiere consenso técnico.
5. **Publicación de la auditoría completa**, incluidas las celdas sin soporte marcadas como
   tales.
6. **Mecanismo de apelación operativo antes del primer caso real.** Es el único riesgo de
   impacto 4 sin control efectivo (R07), y si los datos fueran reales sería además un
   incumplimiento legal, no solo un riesgo ético.

Si alguna de las seis no se cumple, la decisión deja de ser "limitar" y pasa a **no
utilizar**.

## Tres riesgos prioritarios

De los ocho de `reports/lab11/risk_register_scored.csv`:

| | Riesgo | P×I | Control |
|---|---|---|---|
| **R02** | Sobre-marcado de G2: 68 de cada 100 marcados frente a 45 de G1, con 37.5 % de falsos positivos | 9 | Compuerta de brecha de FPR y revisión trimestral de la tasa de selección |
| **R01** | Déficit de recall en G1: 35 de cada 100 casos reales sin marcar frente a 21 en G2 | 8 · alto | Compuerta de brecha de recall ≤ 0.16 y auditoría por grupo en cada reentrenamiento |
| **R07** | Persona marcada sin vía para conocer el motivo, corregir un dato ni pedir segunda revisión | 8 · alto | Mecanismo de apelación documentado y conservación de la versión del modelo y los datos |

R01 y R02 son el mismo compromiso visto desde los dos lados. Están los dos porque los dos
existen, pero solo uno puede ser el prioritario, y elegí R01.
