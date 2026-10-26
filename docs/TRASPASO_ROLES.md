# Roles, RACI y traspaso entre responsables

**INF-8239 Ciencia de Datos II · Unidad 04 · Ejercicio 08** · Alexis De La Cruz · 100805370

El RACI dice quién responde por cada actividad. Este documento añade lo que un RACI no
dice: **qué pasa cuando esa persona cambia.**

## Los cinco roles

| Rol | Qué decide | Qué no puede decidir |
|---|---|---|
| **Institutional Owner** | Aprueba el uso, fija la tolerancia, ordena el retiro y responde las apelaciones | No puede ajustar métricas ni umbrales técnicos sin el Data Scientist |
| **Product Owner** | Operación diaria, umbral operativo y prioridad del trabajo | No puede aprobar un despliegue que viole una compuerta |
| **Data Scientist** | Métricas, auditoría de equidad y límites de interpretación | No puede decidir cuál de los daños es prioritario: eso es institucional |
| **ML Engineer** | Despliegue, versionado, monitoreo y contención | No puede cambiar el modelo en producción sin auditoría previa |
| **Data Engineer** | Contrato de datos, calidad, inventario y borrado por retención | No puede añadir una columna sin documentarla en el inventario |

Las **personas afectadas** no son un rol del RACI porque no trabajan en el sistema, pero
aparecen como *Informed* en nueve de las trece actividades y tienen derecho de apelación
individual. `student_inputs/stakeholders.csv` documenta que hoy su participación es nula y
propone una mesa de representantes.

## El RACI completo

`student_inputs/raci.csv` cubre **13 actividades**, desde el inventario de datos hasta el
borrado por fin de retención. Cada una tiene exactamente un *Accountable* y al menos un
*Responsible*, y `tests/test_inventory.py` lo comprueba: también verifica que ningún rol
figure a la vez como responsable y aprobador de su propio trabajo, ni se consulte a sí
mismo.

Cuatro actividades que no estaban en el RACI del proyecto base y que añadí porque el
expediente promete cosas que sin ellas no tendrían a nadie encargado:

| Actividad | Por qué hace falta |
|---|---|
| Atención de apelaciones | El mecanismo de apelación es el único control del riesgo R07, de impacto 4 |
| Borrado por fin de retención | Una política de retención sin ejecutor es una política que no existe |
| Retiro del sistema | La condición de retiro necesita alguien autorizado a ejecutarla sin consenso |
| Traspaso entre responsables | Es el objeto de este documento |

## Traspaso entre roles

Un sistema gobernado sobrevive al cambio de las personas que lo gobiernan. El traspaso es
una actividad del RACI, con el Product Owner como responsable y el Institutional Owner
como aprobador, y tiene lista de comprobación.

### Qué se entrega

| Artefacto | Dónde | Qué debe poder hacer quien lo recibe |
|---|---|---|
| Evaluación de impacto | `student_inputs/lab11_impact.yml` | Decir qué decisión asiste el sistema y bajo qué condición se apaga |
| Registro de riesgos | `student_inputs/risk_register.csv` | Nombrar los tres riesgos prioritarios y su control |
| Decisión y su justificación | `student_inputs/lab12_decision.yml` y `reports/lab11/DECISION_RECORD.md` | Explicar **por qué** la decisión es limitar y no desplegar |
| Auditoría vigente | `reports/lab12/` | Reproducirla con un comando y obtener las mismas cifras |
| Fichas | `docs/MODEL_CARD.md` y `docs/DATASET_CARD.md` | Responder qué hace el modelo y con qué datos |
| Inventario y retención | `docs/INVENTARIO_DATOS.md` | Decir qué se conserva, por qué y hasta cuándo |
| Runbook | `docs/RUNBOOK.md` | Actuar ante una alerta sin preguntar a nadie |
| Último simulacro | `reports/lab13/INCIDENT_POSTMORTEM.md` | Saber qué falló la última vez y qué quedó pendiente |

### Lista de comprobación del traspaso

1. **Reproducir la auditoría.** Quien recibe ejecuta `uv sync --frozen`, `uv run pytest -q`
   y la secuencia de scripts, y **obtiene las mismas cifras** que el informe vigente. Si no
   coinciden, el traspaso no está completo.
2. **Explicar la decisión con sus propias palabras**, incluida la parte incómoda: que la
   alternativa no predictiva atiende mejor al grupo priorizado y que el modelo solo se
   justifica por la capacidad de revisión.
3. **Localizar los tres umbrales de retiro** en `configs/governance.yml` y saber quién los
   puede ejecutar.
4. **Recorrer el runbook** con un caso hipotético de severidad alta, sin consultar a quien
   entrega.
5. **Revisar las acciones correctivas abiertas** del último postmortem y asumir sus fechas.
6. **Firmar el acta**: quien entrega, quien recibe y el Institutional Owner, con fecha.
7. **Actualizar el RACI** en el mismo commit en que cambia la persona, de modo que Git
   deje rastro de desde cuándo responde cada quien.

### Qué invalida un traspaso

- Que quien recibe no pueda reproducir las cifras.
- Que el traspaso ocurra **durante** un incidente abierto: primero se cierra el incidente.
- Que queden acciones correctivas sin dueño después del cambio.
- Que el único que entendía una decisión de valor sea quien se va. Por eso las decisiones
  están escritas con su razonamiento y no solo con su resultado.

## Sobre los nombres

Todo lo anterior usa **roles, no personas**. En un despliegue real cada rol debe constar
con nombre, cargo y correo, y el acta de traspaso es el documento que los cambia. Aquí se
mantienen como roles porque no existe una asignación institucional real que documentar, y
afirmar lo contrario sería inventar evidencia.
