# Postmortem del simulacro de incidente

**INF-8239 Ciencia de Datos II · Unidad 04 · Ejercicio 08** · Alexis De La Cruz · 100805370

> **Esto es un simulacro.** No ocurrió ningún incidente real. El escenario lo genera
> `scripts/simulate_incident.py` para recorrer el runbook de principio a fin y comprobar
> que cada etapa tiene responsable, plazo y evidencia. Los datos son sintéticos.

| | |
|---|---|
| Detectado | 2026-10-26T05:31:16Z |
| Señal | Brecha de recall entre grupos protegidos por encima del techo |
| Severidad | **Alta** |
| Estado | Cerrado · contenido con base segura |
| Generado por | `scripts/simulate_incident.py` |

## 1. Detección

La reauditoría mensual mide la brecha de recall entre G1 y G2 sobre la ventana más reciente
y la compara con el techo de 0.16 de `configs/governance.yml`. En el simulacro la brecha lo
supera.

El punto importante no es la cifra sino **quién se entera**: la alerta llega al ML Engineer,
que mide, y no al equipo que construyó el modelo. Si el aviso dependiera de que alguien
revisara un informe por iniciativa propia, el incidente seguiría abierto.

## 2. Clasificación

**Severidad alta**, según el runbook: la brecha de recall por encima de 0.16 está en la
lista de señales que disparan retiro inmediato. No se clasifica como media «mientras se
investiga»: el umbral se fijó antes de medir, precisamente para no negociarlo ahora.

## 3. Contención

El ML Engineer detiene el uso del modelo sin esperar a localizar al Institutional Owner,
que es lo que el runbook autoriza en severidad alta. La cola de revisión pasa a la **base
segura**.

**La base segura es la regla manual no predictiva**, no la versión anterior del modelo. Esa
elección está medida: la regla alcanza recall 0.898 en G1 frente a 0.653 del modelo, de modo
que revertir **no degrada** la atención al grupo que se eligió proteger. Su costo es marcar
el 71 % de los casos en lugar del 53 %, es decir más carga de revisión para el equipo y
ningún daño adicional para las personas. Volver a una versión anterior del modelo habría
reintroducido el mismo tipo de riesgo que se acaba de materializar.

## 4. Preservación de evidencia

| Qué | Dónde |
|---|---|
| Métricas de la ejecución afectada | `reports/lab12/logistic/` y `reports/lab13/deployment_decision.json` |
| Versión del modelo | `models/logistic.joblib` y la etiqueta de Git correspondiente |
| Configuración de compuertas vigente | `configs/governance.yml` en el commit en uso |
| Fecha y hora de detección | En este documento, en UTC |

Se conserva **2 años** desde el retiro de la versión, según `docs/INVENTARIO_DATOS.md`. Sin
esta evidencia no se podría atender la apelación de alguien marcado por una versión que ya
no está en uso, que es exactamente el tipo de caso que un incidente genera.

## 5. Comunicación

| A quién | Quién | Cuándo | Qué |
|---|---|---|---|
| Equipo operativo | ML Engineer | Inmediato | El sistema está detenido; la cola vuelve a la regla manual |
| Institutional Owner | ML Engineer | Inmediato | Qué señal se disparó, cuántos casos abarca la ventana, qué se contuvo |
| **Personas afectadas** | Institutional Owner con apoyo legal | Antes de cerrar este postmortem | Qué ocurrió, si su caso estuvo en la ventana afectada y cómo pedir una nueva revisión |
| Dirección | Institutional Owner | Con este documento | Causa, alcance y acciones correctivas con fecha |

La fila que más fácil se omite es la tercera. Un incidente de equidad significa que algunas
personas fueron tratadas peor que otras por el sistema; informarles es lo que convierte la
apelación en un derecho ejercitable.

## 6. Causa y condición que lo permitió

Este es un simulacro, así que no hay causa técnica que diagnosticar. Lo que sí revela el
ejercicio es una **condición real del sistema**: el modelo operaba con una brecha de 0.138
contra un techo de 0.16, es decir con un margen de 0.022 medido sobre una sola partición de
160 casos y sin intervalos de confianza. Un margen así no distingue bien entre «por debajo
del techo» y «por encima del techo»: basta la variación normal entre meses para cruzarlo.

El incidente no sería una sorpresa. Sería el resultado previsible de desplegar con ese
margen, y está anticipado en el registro de decisión como riesgo R01.

## 7. Acciones correctivas

| # | Acción | Responsable | Fecha límite |
|---|---|---|---|
| 1 | Añadir a `configs/governance.yml` una compuerta de FPR máximo y otra de precisión mínima, porque hoy el marco aprueba la regla trivial de marcar a todo el mundo | Data Scientist | 10 días hábiles |
| 2 | Calcular intervalos de confianza de la brecha por remuestreo y publicarlos junto a la cifra puntual | Data Scientist | 15 días hábiles |
| 3 | Elevar el soporte mínimo por celda interseccional o declarar formalmente que ese nivel no se audita | Data Scientist | 15 días hábiles |
| 4 | Verificar que el registro de decisiones del operador permite reconstruir qué casos se revisaron realmente durante la ventana afectada | Product Owner | 5 días hábiles |
| 5 | Repetir el simulacro con el equipo completo, cronometrando el tiempo hasta la contención | ML Engineer | 1 mes |

## 8. Qué aprendió el simulacro

1. **La autoridad de contención funciona sin reunión.** El ML Engineer puede detener el
   sistema antes de localizar a nadie. Es la única forma de que un umbral tenga efecto.
2. **La base segura estaba elegida de antemano y medida.** No hubo que decidir a dónde
   revertir en medio del incidente.
3. **La comunicación a las personas afectadas tiene responsable y plazo**, no es un
   «se evaluará».
4. **El margen de 0.022 es el verdadero hallazgo.** Un incidente de este tipo es probable
   mientras se opere así, y eso refuerza la decisión de **limitar** en lugar de desplegar.
