# Runbook de monitoreo e incidentes

**INF-8239 Ciencia de Datos II · Unidad 04 · Ejercicio 08** · Alexis De La Cruz · 100805370

Un runbook convierte una alerta en acciones trazables. Si hay que pensar qué hacer cuando
suena, no sirve.

## 1. Monitoreo: qué se vigila y cuándo

| Señal | Umbral | Frecuencia | Quién mide | Qué dispara |
|---|---|---|---|---|
| Brecha de recall entre grupos | **> 0.16** | Mensual | ML Engineer | **Retiro inmediato** |
| Recall global | **< 0.68** | Mensual | ML Engineer | **Retiro inmediato** |
| Brecha de FPR entre grupos | > 0.16 | Mensual | ML Engineer | Revisión en 5 días hábiles |
| Tasa de selección por grupo | Variación > 10 puntos respecto del mes anterior | Mensual | Data Scientist | Revisión del umbral |
| Coincidencia operador-sistema | **> 95 %** | Mensual | Product Owner | Revisión del proceso: indica sesgo de automatización |
| Casos marcados sin revisión humana | **> 0** | Continuo | ML Engineer | Incidente: el sistema está actuando solo |
| Apelaciones recibidas y resueltas | Cualquier apelación sin respuesta en plazo | Mensual | Legal | Escalado al Institutional Owner |
| Uso fuera de alcance | Cualquier caso documentado | Continuo | Institutional Owner | **Retiro inmediato** |

Los tres umbrales en negrita que disparan retiro son los mismos de `configs/governance.yml`
y de la condición de retiro de `student_inputs/lab11_impact.yml`. No son cifras de este
documento: salen del archivo de configuración, de modo que cambiar el umbral obliga a
cambiar el código y deja rastro en Git.

**Limitación del monitoreo que conviene declarar:** vigilar la brecha mensualmente sobre una
ventana de unos 160 casos reproduce el problema de soporte de la auditoría original. Una
brecha medida sobre pocos casos es inestable, así que la alerta debe leerse como *revisar*,
no como *demostrado*. El retiro es inmediato de todas formas, porque ante la duda se apaga.

## 2. Detección y clasificación

| Severidad | Qué la define | Respuesta |
|---|---|---|
| **Alta** | El sistema actuó sin revisión humana, o hubo uso prohibido, o la brecha de recall superó 0.16 | Contención inmediata, sin esperar reunión |
| **Media** | Brecha de FPR por encima del techo, o coincidencia operador-sistema por encima del 95 % | Revisión documentada en 5 días hábiles |
| **Baja** | Deriva de la tasa de selección sin superar ninguna compuerta | Se anota en la reauditoría del mes |

Quien detecta puede ser cualquiera: el operador, el equipo de datos, una persona afectada a
través de una apelación, o la alerta automática. **El canal no cambia la clasificación.**

## 3. Autoridad de contención

El **Institutional Owner** puede detener el sistema. No requiere consenso técnico, reunión
previa ni aprobación de nadie más. El **ML Engineer** ejecuta la contención y está
autorizado a hacerlo antes de localizar al Institutional Owner si la severidad es alta.

Esta es la regla que hace que el resto del expediente valga algo: si detener el sistema
exigiera convencer a quien lo defiende, nunca se detendría.

## 4. Preservación de evidencia

Antes de tocar nada:

1. Copiar `reports/lab12/` y `reports/lab13/` de la ejecución afectada.
2. Conservar el `models/*.joblib` de la versión en uso y su etiqueta de Git.
3. Registrar los `case_id` afectados y la fecha y hora de detección en UTC.
4. Exportar el registro de decisiones del operador del periodo afectado.

La evidencia se conserva **2 años** desde el retiro de esa versión, igual que el resto de
los artefactos de auditoría. Sin ella no se puede atender una apelación sobre un caso
marcado por una versión que ya no está en uso.

## 5. Comunicación

| A quién | Quién comunica | Plazo | Qué se dice |
|---|---|---|---|
| Equipo operativo | ML Engineer | Inmediato | Que el sistema está detenido y que la cola vuelve a la regla manual |
| Institutional Owner | ML Engineer | Inmediato en severidad alta | Qué pasó, a cuántos casos afecta, qué se contuvo |
| Personas afectadas | Institutional Owner, con apoyo legal | Antes de cerrar el postmortem | Qué ocurrió, si su caso se vio afectado y cómo pedir una nueva revisión |
| Dirección de la institución | Institutional Owner | Con el postmortem | Causa, alcance y acciones correctivas con fechas |

Comunicar a las personas afectadas no es opcional ni posterior: es la parte que convierte la
apelación en un derecho ejercitable y no en una posibilidad teórica.

## 6. Reversión y base segura

La base segura **no es la versión anterior del modelo**: es la **regla manual no
predictiva** —ordenar por fecha de recepción y atender primero a quien supera la mediana de
incidentes previos— documentada en `student_inputs/lab11_impact.yml`.

Esa elección tiene un motivo medido: la regla manual alcanza recall 0.898 en G1 frente a
0.653 del modelo, de modo que volver a ella **no degrada** la atención al grupo que se
eligió proteger. Su costo es marcar más casos, lo que carga al equipo operativo pero no a
las personas. Volver a una versión anterior del modelo, en cambio, reintroduciría el mismo
tipo de riesgo que se acaba de materializar.

## 7. Postmortem

Se redacta en `reports/lab13/INCIDENT_POSTMORTEM.md` dentro de los **5 días hábiles**
siguientes al cierre del incidente, con responsable y fecha por cada acción correctiva. Es
**sin culpables**: busca la condición que permitió el fallo, no la persona que lo ejecutó.

`scripts/simulate_incident.py` genera la plantilla y **no sobrescribe** un postmortem ya
redactado.

## 8. Simulacro

El simulacro ejecutado el 26 de octubre de 2026 está documentado en
`reports/lab13/INCIDENT_POSTMORTEM.md`, con las seis etapas de este runbook recorridas:
detección, clasificación, contención, preservación, comunicación y reversión.
