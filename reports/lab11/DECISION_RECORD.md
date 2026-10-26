# Registro de decisión · Ejercicio 07 (LAB11 + LAB12)

**INF-8239 Ciencia de Datos II · Unidad 04** · Alexis De La Cruz · 100805370

Sistema auditado: DSS territorial sintético que **ordena** casos para revisión humana.
No interviene, no decide elegibilidad y no declara emergencias; eso está prohibido en
`configs/governance.yml`.

## Decisión

**GO condicionado** sobre la regresión logística, con las cuatro condiciones de la última
sección. No es un GO simple y no es un REVIEW: el modelo pasa las cinco compuertas
declaradas, pero el margen con el que las pasa no sostiene un despliegue abierto.

Descarto el árbol de decisión. No es una cuestión de preferencia: viola dos compuertas de
equidad —brecha de recall 0.181 y brecha de FPR 0.168, ambas por encima del techo de
0.16— y además es menos exacto, 0.706 frente a 0.719. No hay nada que ganar aceptándolo.

## Daño prioritario

Que una persona del grupo G1 cuyo caso **sí** requiere revisión quede sin marcar y por
tanto sin atención.

Lo elijo por encima del sobre-marcado de G2 porque el sistema solo ordena una cola: un
falso positivo cuesta una revisión de más, que el operador descarta en minutos, mientras
un falso negativo cuesta un caso desatendido que nadie vuelve a mirar. Los dos daños
existen, los dos están medidos y **no se pueden minimizar a la vez con el mismo umbral**.
Esta elección es mía y es la que ordena todo lo demás: la métrica, la tolerancia y el
retiro.

## Evidencia

Generada por `scripts/lab12_audit.py` sobre los 160 casos de prueba de la partición
cronológica (25 sep – 27 dic de 2026, entrenando con 480 casos del 1 ene al 24 sep).
Ninguna cifra está escrita a mano.

| Métrica | G1 (n=101) | G2 (n=59) | Brecha | Techo |
|---|---|---|---|---|
| Recall | 0.653 | 0.791 | **0.138** | 0.16 |
| FPR | 0.250 | 0.375 | 0.125 | 0.16 |
| Tasa de selección | 0.446 | 0.678 | 0.232 | — |
| Precisión | 0.711 | 0.850 | 0.139 | — |
| Exactitud | 0.703 | 0.746 | 0.043 | — |

Recall global 0.717 (techo mínimo 0.68) · 0.014 ms por caso · 3.56 KB.
Las cinco compuertas pasan: `reports/lab12/logistic/global_metrics.json`.

Traducido a personas: de cada 100 casos de G1 que requerían revisión, el sistema deja
**35 sin marcar**; en G2 deja 21. Esa diferencia es el daño que elegí evitar, y 0.138 es
su tamaño medido.

## Incertidumbre

Tres cosas que la evidencia **no** permite afirmar, y que declaro para que nadie lea esta
auditoría como un sello de aprobación:

1. **El desglose interseccional no es interpretable en tres de las ocho celdas.**
   G2 | 30-44 y G2 | 45-59 tienen 2 casos negativos, y G2 | 18-29 tiene 3. El FPR de
   1.000 que aparece ahí en el árbol son **dos casos de dos**: un solo caso mueve la cifra
   50 puntos. Declaro un soporte mínimo de 30 casos por celda y no concluyo nada por
   debajo. La conclusión válida es que **falta dato para auditar a ese nivel**.
2. **La brecha de 0.138 viene de una sola partición de 160 casos**, sin intervalo de
   confianza ni repetición con otras semillas. La distancia real al techo de 0.16 es más
   incierta que lo que sugiere un margen de 0.022.
3. **Los datos son sintéticos y didácticos.** Nada de esto estima el comportamiento del
   sistema sobre población real, y el ejercicio no autoriza extrapolarlo.

## Responsables

| Qué | Quién |
|---|---|
| Aprueba, condiciona o suspende el uso | Responsable institucional del área de revisión territorial |
| Operación diaria y umbral | Product Owner |
| Auditoría de equidad en cada reentrenamiento | Data Scientist |
| Reauditoría mensual y alerta de compuertas | ML Engineer |
| Apelaciones | Responsable institucional, con apoyo legal |

En un despliegue real estos campos deben constar con nombre, cargo y correo. Aquí son
roles tomados de `student_inputs/raci.csv`, no una asignación institucional real.

## Condiciones del GO

1. **Revisión humana obligatoria de cada caso marcado**, sin ninguna acción automática.
   La decisión del operador se registra junto a la propuesta del sistema.
2. **Reauditoría mensual de la brecha de recall** sobre la ventana más reciente, con
   **retiro inmediato si supera 0.16** o si el recall global baja de 0.68. El retiro lo
   ejecuta el responsable institucional y no requiere consenso técnico.
3. **Publicación de la auditoría completa**, incluidas las celdas sin soporte marcadas
   como tales.
4. **Mecanismo de apelación operativo antes del primer caso real.** Hoy es el único
   riesgo de impacto 4 sin control efectivo (R07 en el registro), y mientras no exista,
   un error de datos queda fijado como decisión.

Si alguna de las cuatro no se cumple, la decisión deja de ser GO condicionado y pasa a
STOP.
