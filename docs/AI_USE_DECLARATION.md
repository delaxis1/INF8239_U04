# Declaración de uso de IA

**INF-8239 Ciencia de Datos II · Unidad 04 · Ejercicio 07** · Alexis De La Cruz · 100805370

El mandato permite que la IA apoye estructura, pruebas o redacción, pero **no que decida
los valores del análisis ni invente evidencia**. Esta declaración detalla dónde estuvo la
línea y cómo se respetó.

## Herramienta

**Claude Opus 5 (Anthropic)**, mediante Claude Code, con acceso al proyecto local y al aula
virtual para leer el mandato, la rúbrica y los capítulos LAB11, LAB12 y LAB13.

## Prompts relevantes

| Prompt | Para qué se usó |
|---|---|
| "vamos a hacer los ejercicios de la unidad 4, el 07 y 08, vamos a comenzar con el 07" | Leer el mandato y los capítulos, instalar el proyecto base y ejecutar la auditoría |
| "tráeme los 8 escenarios de riesgo redactados" | Redactar los ocho riesgos a partir de la evidencia medida, para mi revisión |
| "R01, que G1 quede sin revisar" | **Mi decisión del daño prioritario**, de la que se derivan la métrica, la tolerancia y la recomendación |
| "dame el pdf para enviar la práctica" | Verificar el mandato, completar lo que faltaba y generar el informe |

## Qué decidí yo y qué no podía decidir el asistente

| Decisión | Quién |
|---|---|
| Daño prioritario: que G1 quede sin revisar, por encima del sobre-marcado de G2 | **Yo** |
| Métrica primaria y tolerancia de 0.16 | Yo, sobre el umbral ya preinscrito en `governance.yml` |
| Decisión final: limitar | **Yo**, después de ver que la regla manual gana al modelo |
| Dueños de cada riesgo | Yo, sobre los roles de `raci.csv` |
| Interpretación normativa del apartado legal | **Mía**, y queda marcada como pendiente de verificación |
| Cifras de la auditoría | Ninguno de los dos: salen de ejecutar los scripts |

El asistente me planteó explícitamente la elección entre R01 y R02 en lugar de rellenarla,
y cuando la evidencia posterior contradijo la recomendación que ya estaba redactada, me lo
dijo y volvió a preguntar antes de escribir el informe.

## Qué hizo el asistente

- Ejecutó `lab12_audit.py` con los dos modelos y ordenó la evidencia resultante.
- Escribió `scripts/compare_alternatives.py` para añadir la línea base y la tabla Green AI
  que pedía la rúbrica de LAB12 y que el proyecto base no incluye.
- Redactó los ocho escenarios de riesgo, los campos de impacto y los borradores de este
  documento, del `DECISION_RECORD.md` y del `MARCO_NORMATIVO.md`, siguiendo mis decisiones.
- Detectó y corrigió dos errores de sintaxis del proyecto base.
- Montó el generador del informe reutilizando el formato de mis entregas anteriores.

## Qué verifiqué

- **Todas las cifras provienen de ejecutar los scripts** en este equipo. No hay ningún
  número escrito a mano en el informe ni en los artefactos.
- **El soporte de cada celda interseccional**, contando positivos y negativos uno por uno:
  tres celdas tienen 2 o 3 casos negativos y por eso no se interpretan.
- **Que la regla manual no usa las etiquetas de prueba.** Su umbral es la mediana de
  `previous_incidents` en el conjunto de entrenamiento, y está registrado en
  `reports/lab12/umbral_regla_manual.json`.
- **Que `marcar_todo` pasa las cinco compuertas**, que es lo que revela el hueco del marco
  de gobernanza.
- **Las pruebas**: `uv run pytest -q` pasa las diez.

## Errores detectados y correcciones

1. **El asistente redactó primero un "GO condicionado".** Al medir la línea base quedó
   claro que la regla manual atiende mejor a G1 que el modelo, de modo que ese GO
   contradecía mi propio daño prioritario. Se corrigió a **limitar** y la contradicción
   queda documentada en lugar de borrada.
2. **Dos scripts del proyecto base no compilaban.** `lab11_impact.py` y
   `simulate_incident.py` abren cadenas de varias líneas con una sola comilla. Se verificó
   que el error estaba en el commit del proyecto intacto antes de tocar nada, y el arreglo
   es de comillas, sin cambiar el texto.
3. **`lab11_impact.py` sobrescribía `DECISION_RECORD.md`** en cada ejecución. Se le añadió
   un guardia para que solo cree la plantilla si el archivo no existe.
4. **Un primer intento de crear el repositorio por API fue bloqueado** por la protección de
   credenciales del propio asistente. No se buscó la vuelta: el repositorio se creó desde
   el formulario de GitHub con mi sesión.
5. **La regla manual con `previous_incidents >= 1` marcaba al 95 % de los casos** y no
   servía como referencia. Se reformuló con la mediana del entrenamiento, dejando constancia
   de que el umbral no sale de las etiquetas.

## Responsabilidad

El código, los datos, las referencias, la interpretación normativa y las conclusiones son
responsabilidad mía. Puedo explicar cualquier fragmento del proyecto y defender cada
decisión de valor, empezando por la que ordena todas las demás: cuál de los dos daños
elegí evitar primero y por qué.
