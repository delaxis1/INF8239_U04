# Inventario de datos, minimización y retención

**INF-8239 Ciencia de Datos II · Unidad 04 · Ejercicio 08** · Alexis De La Cruz · 100805370

Tres preguntas por cada columna: **qué es**, **por qué hace falta** y **cuánto tiempo se
conserva**. Si una columna no supera la segunda pregunta, no debería estar en el sistema.

> Los datos son sintéticos y no describen personas reales. Este inventario es el que
> aplicaría si el sistema se alimentara de datos reales, y es el que el equipo tendría que
> defender ante el titular de los datos.

## Inventario por columna

| Columna | Qué es | Sensibilidad | ¿Entra al modelo? | Por qué se conserva |
|---|---|---|---|---|
| `case_id` | Identificador interno del caso | Indirecta: no identifica por sí solo, pero permite reunir todo lo de un caso | **No** | Sin él no hay apelación posible: es lo que permite reconstruir qué datos y qué versión del modelo produjeron una marca |
| `received_date` | Fecha de entrada del caso | Baja | **No** | Define el corte temporal del entrenamiento y permite detectar deriva. Fuera del modelo para no aprender el calendario |
| `zone` | Zona territorial | Indirecta: en una zona pequeña puede acercarse a identificar | Sí | Es la unidad operativa de la revisión. Riesgo R08 del registro |
| `protected_group` | Grupo protegido | **Alta** | **No, nunca** | Se conserva **exclusivamente para auditar**. Sin él no se puede medir la brecha de recall, que es la métrica que vigila el daño prioritario |
| `age_band` | Tramo de edad, no la edad exacta | Media | Sí | Ya viene minimizado en origen: tramos en lugar de fecha de nacimiento |
| `previous_incidents` | Número de incidentes previos | Media | Sí | Es la variable con más peso operativo y la base de la alternativa no predictiva |
| `infrastructure_score` | Indicador de infraestructura de la zona | Baja: describe el territorio, no a la persona | Sí | Contexto territorial, que es el objeto del sistema |
| `exposure` | Exposición estimada | Baja | Sí | Contexto territorial |
| `target` | Si el caso requería revisión | Alta en consecuencias | **No** (es la etiqueta) | Sin histórico de resultados no hay forma de medir si el sistema acierta ni de auditarlo por grupo |

## Minimización

Lo que **no** se recoge, y la razón:

- **Ningún identificador directo.** Nombre, documento, correo y teléfono están prohibidos
  por contrato: `src/inf8239_u04/data.py` los rechaza en `validate_schema` y
  `tests/test_privacy.py` comprueba que el rechazo ocurre. No es una política escrita en un
  documento que nadie lee: el sistema no arranca si aparecen.
- **Edad en tramos, no exacta.** `age_band` da la granularidad que el modelo necesita sin
  la precisión que facilitaría reidentificar a alguien.
- **El grupo protegido no entra al modelo.** `features()` devuelve cinco columnas y
  `protected_group` no está entre ellas. Se conserva solo porque **sin él no se puede
  auditar**: quitarlo del todo no elimina el sesgo, solo lo vuelve invisible.
- **Sin texto libre.** No hay campos de observaciones ni notas del operador, que son la vía
  habitual por la que entran datos personales no declarados a un conjunto que se creía
  anónimo.

La minimización tiene un límite que conviene declarar: quitar `protected_group` haría el
sistema *menos* auditable, no más justo. `zone`, `age_band` y el historial pueden
correlacionar con el grupo, de modo que el sesgo seguiría ahí sin ninguna forma de medirlo.

## Retención

| Dato | Plazo | Desde cuándo cuenta | Quién ejecuta el borrado |
|---|---|---|---|
| Datos del caso y su marca | **2 años** | Cierre del caso | Data Engineer, con el Institutional Owner como responsable final |
| Registro de apelación | **2 años** | Resolución de la apelación | Legal |
| Versión del modelo y métricas de la auditoría | 2 años | Retiro de esa versión | ML Engineer |
| Informes de auditoría publicados | Permanente, en forma agregada | Publicación | Product Owner |

**Por qué dos años.** Es el plazo más corto que todavía cubre lo que el sistema promete:
el ciclo de apelación, las doce reauditorías mensuales de un año completo y una revisión
anual con margen para compararla con la anterior. Un plazo mayor acumularía datos que ya no
sirven para ninguna de esas tres cosas, y el principio de proporcionalidad obliga a
justificar cada año adicional, no a asumirlo. Un plazo menor dejaría sin histórico la
detección de deriva.

Los informes de auditoría se conservan sin plazo, pero **solo en forma agregada**: tablas
por grupo, sin casos individuales. Eso permite rendir cuentas sobre cómo se comportó el
sistema años atrás sin conservar los datos de nadie.

La actividad «Borrado por fin de retención» está en `student_inputs/raci.csv` con
responsable y aprobador asignados, porque una política de retención que nadie tiene
encargado de ejecutar es una política que no existe.

## Verificación automática

`tests/test_inventory.py` comprueba que **todas las columnas del conjunto están
documentadas en este archivo** y que ninguna columna documentada ha desaparecido del
conjunto. Si alguien añade una columna al dataset sin inventariarla, la prueba falla. Es lo
que convierte este documento en un artefacto verificable y no en una declaración de
intenciones.
