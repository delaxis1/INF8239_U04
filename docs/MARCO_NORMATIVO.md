# Marco normativo: qué obliga, qué se adopta y qué se elige

**INF-8239 Ciencia de Datos II · Unidad 04 · Ejercicio 07** · Alexis De La Cruz · 100805370

El mandato pide diferenciar tres cosas que suelen mezclarse: lo que la ley **obliga**, lo
que un marco voluntario **recomienda** y lo que uno **elige** por criterio ético aunque
nada lo exija. La distinción importa porque cada nivel se defiende de otra manera: lo
primero con la norma, lo segundo con la adhesión declarada, lo tercero con argumentos.

> **Advertencia previa.** Este sistema trabaja sobre `data/territorial_risk_synthetic.csv`,
> un conjunto sintético sin personas reales. **Hoy no le aplica ningún régimen de datos
> personales**, porque no hay datos personales. Lo que sigue describe qué aplicaría si el
> sistema se alimentara de datos reales de personas, que es el escenario que el ejercicio
> pide anticipar. Las citas están verificadas contra fuente primaria —el detalle y los
> cinco errores que corrigió esa verificación están en la §4—, pero **la lectura de qué
> obliga cada norma a este sistema es mía**, no un dictamen legal.

## 1. Obligación legal

Lo que una institución dominicana **no puede elegir** si el sistema usara datos reales.

| Norma | Qué obliga | Dónde impacta este sistema |
|---|---|---|
| Constitución de la República Dominicana (texto vigente, proclamado el 27 de octubre de 2024), art. 44, numeral 2 | Derecho a la intimidad y al honor personal. El numeral 2 reconoce el acceso a los datos propios y al destino y uso que se les dé; exige que su tratamiento respete los principios de calidad, licitud, lealtad, seguridad y finalidad; y permite pedir **ante la autoridad judicial competente** la actualización, la oposición al tratamiento, la rectificación o la destrucción de lo que afecte ilegítimamente los derechos del titular | La Constitución manda al titular a un juez. El mecanismo de apelación de `lab11_impact.yml` es la vía administrativa que le evita ese camino: no sustituye al derecho, lo hace ejercible sin pleito |
| Constitución, art. 70 | Acción de *hábeas data*: conocer la existencia de los datos propios y acceder a ellos y, **solo en caso de falsedad o discriminación**, exigir su suspensión, rectificación, actualización y confidencialidad | Obliga a conservar la versión del modelo y los datos que produjeron cada marca, o la acción es imposible de atender: sin ese rastro no se puede ni acreditar ni desmentir una falsedad |
| Ley No. 172-13 (2013) | Su art. 5 enumera ocho principios: licitud, calidad, derecho de información, consentimiento, seguridad, deber de secreto, lealtad y **finalidad**. El de finalidad exige datos «adecuados, pertinentes y no excesivos» respecto del fin declarado. Los arts. 10 y 14 reconocen el derecho de acceso y los de rectificación y cancelación | `purpose` y `out_of_scope_use` dejan de ser documentación interna y pasan a delimitar el tratamiento lícito: usar la puntuación para decidir elegibilidad sería un fin distinto del declarado |

**Un límite de la Ley 172-13 que conviene no esconder.** Su art. 2 la hace aplicable a
cualquier banco de datos susceptible de tratamiento, público o privado, de modo que el
capítulo general sí alcanza a un sistema como este. Pero el segundo objeto declarado en su
art. 1 es regular las Sociedades de Información Crediticia, y la mayor parte de sus
artículos hablan de burós de crédito. Citarla como si fuera un régimen general de IA al
estilo del reglamento europeo la sobreinterpreta. Lo que de ella se invoca aquí son los
principios del art. 5 y los derechos de los arts. 10 y 14, que son de la parte general.

Consecuencia concreta para nuestra decisión: el riesgo **R07** (persona marcada sin vía de
apelación) no es solo un riesgo ético de impacto 4. Si los datos fueran reales, sería un
incumplimiento. Por eso está como condición previa al primer caso real y no como mejora
posterior.

## 2. Marco voluntario

Lo que adoptamos porque decidimos adherirnos, no porque nos obliguen.

| Marco | Naturaleza | Qué tomamos |
|---|---|---|
| NIST AI RMF 1.0 (NIST AI 100-1) | **Voluntario por diseño**; el propio documento lo dice | Las cuatro funciones GOVERN, MAP, MEASURE y MANAGE como estructura del expediente |
| Recomendación del Consejo de la OCDE sobre IA (OECD/LEGAL/0449, 2019, enmendada el 3 de mayo de 2024) | Instrumento no vinculante: compromiso de los países adherentes, no obligación directa sobre una institución | Supervisión humana significativa y transparencia sobre los límites del sistema |
| Model Cards (Mitchell et al., 2019) y Datasheets (Gebru et al., 2021) | Práctica de la comunidad científica | El formato de `MODEL_CARD.md` y `DATASET_CARD.md` |
| Documentación de Fairlearn | Herramienta y guía metodológica | `MetricFrame`, métricas por grupo e interseccionales y la advertencia de soporte insuficiente |
| Reglamento de IA de la Unión Europea (2024/1689) | **Es ley, pero de otra jurisdicción** | Referencia voluntaria: su anexo III, punto 5, letra a) clasifica como de alto riesgo los sistemas que las autoridades públicas usan para evaluar la elegibilidad de personas físicas a prestaciones y servicios de asistencia pública esenciales. Describe este caso con precisión, aunque no nos obligue |

Esa última fila es la distinción que más fácil se confunde: el Reglamento europeo es
obligación legal **allí** y referencia voluntaria **aquí**. Citarlo como si nos obligara
sería un error; ignorarlo porque no nos obliga sería desaprovechar el marco más detallado
que existe para sistemas como este.

### Cómo se cubre el NIST AI RMF

| Función | Qué pide | Evidencia en este repositorio |
|---|---|---|
| **GOVERN** | Responsables, política y autoridad para detener | `configs/governance.yml` con usos prohibidos, columnas prohibidas y compuertas; `student_inputs/raci.csv`; y la condición de retiro de `lab11_impact.yml`, que no requiere consenso técnico |
| **MAP** | Contexto, finalidad, interesados y riesgos | `lab11_impact.yml`, `stakeholders.csv` y los ocho riesgos de `risk_register.csv`, puntuados en `reports/lab11/risk_register_scored.csv` |
| **MEASURE** | Medición desagregada con sus límites | `reports/lab12/*/fairness_by_group.csv`, `fairness_intersectional.csv`, `global_metrics.json` y `comparison.csv`, más el soporte mínimo declarado de 30 casos por celda |
| **MANAGE** | Priorizar, mitigar, monitorear y responder | Las cinco condiciones del uso limitado en `lab12_decision.yml`, la reauditoría mensual, el mecanismo de apelación y, para LAB13, el runbook de incidentes |

`reports/lab11/rmf_summary.json` lo genera el script del proyecto base y es
deliberadamente escueto; la tabla de arriba es la lectura completa. Que exista un archivo
por función no prueba que el control funcione, y el propio manual lo advierte.

## 3. Recomendación ética

Lo que elegimos sin que ninguna norma ni marco lo pidiera. Es el nivel que más hay que
defender con argumentos, porque nadie puede exigirlo.

1. **Declarar las celdas sin soporte en lugar de reportarlas.** Tres de las ocho
   intersecciones tienen 2 o 3 casos negativos. Nada impedía publicar ese FPR de 1.000
   como hallazgo. Elegimos escribir que **falta dato para auditar a ese nivel**, porque un
   número con dos observaciones detrás no es evidencia, es ruido con decimales.
2. **No mover la tolerancia después de medir.** Medimos 0.138 contra un techo de 0.16.
   Bajarlo para reprobar al modelo o subirlo para aprobarlo habría sido mover la portería.
   Se mantiene el 0.16 preinscrito y se declara que el margen es estrecho.
3. **Publicar la línea base que le gana al modelo.** La regla manual no predictiva atiende
   mejor al grupo que elegimos proteger: recall 0.898 en G1 frente a 0.653. Era más cómodo
   no medirla. Está medida, publicada en `reports/lab12/comparison.csv` y es la razón por
   la que la decisión final es **limitar** y no desplegar.
4. **Señalar el hueco de nuestro propio marco de gobernanza.** Las compuertas de
   `governance.yml` aprueban la regla trivial de marcar a todo el mundo, porque fijan
   recall mínimo y brechas máximas pero no acotan FPR ni precisión. Lo declaramos y
   proponemos añadir esas dos compuertas, aunque nos deje en evidencia.
5. **Recomendar "limitar" aunque las cinco compuertas pasen.** El marco autorizaba un GO.
   Elegimos no tomarlo, porque pasar una compuerta no es lo mismo que haber demostrado que
   el sistema es necesario.

## 4. Verificación de las citas contra fuente primaria

La primera versión de este documento llevaba una advertencia honesta pero cómoda: que la
interpretación normativa quedaba «pendiente de verificación». Una advertencia no es una
verificación. Esto es la verificación.

**Procedimiento.** Descargar el texto de cada norma de su publicador oficial, extraerlo y
leer el artículo citado completo; resolver cada DOI contra el registro de Crossref en lugar
de confiar en que el enlace parezca correcto.

| Afirmación | Fuente primaria consultada | Resultado |
|---|---|---|
| Art. 44 reconoce intimidad, honor y acceso a los datos propios | Constitución 2024, PDF de la Gaceta Oficial 11170 alojado por el Banco Central; contrastado con la Constitución 2015 del portal de la Presidencia | ✅ Literal, incluidos los cinco principios del tratamiento |
| Art. 70 establece el *hábeas data* | Las dos mismas ediciones | ⚠️ **Corregido**: el artículo existe y se titula así, pero no otorga supresión |
| Arts. 44 y 70 conservan número y redacción | Comparación palabra por palabra entre 2015 y 2024 | ✅ Idénticos en ambas ediciones |
| Edición de la Constitución citada | Portada de cada PDF | ❌ **Corregido**: se citaba una edición derogada |
| Título de la Ley 172-13 | Texto de la ley publicado por el MIDE y por el INVI, con su encabezado de Gaceta Oficial | ❌ **Corregido**: el título citado no existe |
| «Principio de proporcionalidad» de la Ley 172-13 | Art. 5 completo, y búsqueda de la raíz «proporcional» en todo el texto | ❌ **Corregido**: cero coincidencias en la ley |
| Derechos de acceso y rectificación en la Ley 172-13 | Arts. 10 y 14 | ✅ Existen, con esos títulos |
| Anexo III, punto 5, letra a) del Reglamento (UE) 2024/1689 | Reproducción del anexo en artificialintelligenceact.eu | ✅ Coincide (fuente secundaria: EUR-Lex no respondió a la consulta automatizada) |
| DOI del NIST AI RMF 1.0 | Crossref, y resolución del DOI | ✅ Resuelve al PDF de NIST |
| Páginas de Mitchell et al. (2019): 220-229 | Crossref | ✅ Coincide |
| Páginas de Gebru et al. (2021): 64(12), 86-92 | Crossref | ✅ Coincide |
| Fairlearn en JMLR 24(257), 1-8, 2023 | Página del artículo en jmlr.org | ✅ Coincide |
| DOI de la Recomendación de la OCDE | Crossref y búsqueda del identificador | ❌ **Corregido**: el DOI no resuelve |

### Los cinco errores que encontró

1. **La Constitución citada estaba derogada.** Se citaba la proclamada el 26 de enero de
   2010. El texto vigente es el proclamado por la Asamblea Nacional el **27 de octubre de
   2024** (Gaceta Oficial 11170 del 31 de octubre de 2024), que sustituyó al de 2015, que a
   su vez sustituyó al de 2010. Comparé los arts. 44 y 70 entre las ediciones de 2015 y
   2024 y son idénticos en número, título y redacción, así que el fondo de lo que afirmaba
   el documento no cambia. Lo que estaba mal era la cita, y una cita a un texto derogado es
   un error aunque acierte el contenido. No comparé contra la edición de 2010.

2. **«Ley Orgánica sobre Protección de Datos de Carácter Personal» no es el título de la
   Ley 172-13.** El oficial, tal como aparece en su encabezado, es *Ley No. 172-13 que
   tiene por objeto la protección integral de los datos personales asentados en archivos,
   registros públicos, bancos de datos u otros medios técnicos de tratamiento de datos
   destinados a dar informes, sean estos públicos o privados* (Gaceta Oficial 10737 del 15
   de diciembre de 2013). La ley no se declara orgánica en ninguna parte; la única
   aparición de la palabra es el rótulo «Disposiciones orgánicas» de un capítulo sobre la
   constitución de los burós de crédito.

3. **La Ley 172-13 no tiene un principio de proporcionalidad.** El informe del Ejercicio
   08 hablaba del «principio de proporcionalidad de la Ley 172-13». Busqué la raíz
   «proporcional» en el texto íntegro: **cero coincidencias**. Los ocho principios del
   art. 5 son licitud, calidad, derecho de información, consentimiento, seguridad, deber de
   secreto, lealtad y finalidad. La sustancia de la proporcionalidad sí está, pero dentro
   del principio de finalidad, que exige datos «adecuados, pertinentes y no excesivos».
   Nombrar un principio que la ley no nombra es atribuirle algo que no dice, y es el tipo
   de error que un lector con el texto delante detecta de inmediato.

4. **El *hábeas data* no permite hacer suprimir los datos.** El documento decía «conocer,
   actualizar o hacer suprimir datos propios». El art. 70 concede conocer la existencia de
   los datos y acceder a ellos y, **solo en caso de falsedad o discriminación**, exigir su
   suspensión, rectificación, actualización y **confidencialidad**. La supresión no está, y
   la condición de falsedad o discriminación tampoco estaba recogida. La destrucción sí
   aparece, pero en el art. 44.2 y por vía judicial, que es otro artículo y otra vía.

5. **El DOI de la Recomendación de la OCDE no resuelve.** Se citaba
   `10.1787/cc2e1d3e-en`; Crossref devuelve 404 y no corresponde a ningún documento
   localizable. La Recomendación no es una publicación con DOI: es un instrumento legal
   identificado como **OECD/LEGAL/0449**, adoptado el 22 de mayo de 2019 y **enmendado el 3
   de mayo de 2024**. Citar «(2019)» sin la enmienda también estaba incompleto.

### Qué no cubre esta verificación

- **Los textos se tomaron de portales oficiales, no de la Gaceta Oficial impresa.** El de
  la Constitución de 2024 es el PDF de la Gaceta 11170 que aloja el Banco Central; el de
  2015, el del portal de la Presidencia; el de la Ley 172-13, los que publican el MIDE y el
  INVI, coincidentes entre sí.
- **No consulté EUR-Lex directamente**: no respondió a la consulta automatizada, así que el
  anexo III se contrastó contra una reproducción de terceros.
- **Esto verifica las citas, no la interpretación.** Que el art. 44.2 diga lo que digo que
  dice está comprobado. Que de ahí se siga que el mecanismo de apelación de este sistema
  sea obligatorio y no opcional es mi lectura, y un abogado podría discutirla.

## Referencias

- Constitución de la República Dominicana, votada y proclamada por la Asamblea Nacional el 27 de octubre de 2024, arts. 44 y 70. Gaceta Oficial No. 11170 del 31 de octubre de 2024.
- Ley No. 172-13 que tiene por objeto la protección integral de los datos personales asentados en archivos, registros públicos, bancos de datos u otros medios técnicos de tratamiento de datos destinados a dar informes, sean estos públicos o privados. República Dominicana, 13 de diciembre de 2013. Gaceta Oficial No. 10737 del 15 de diciembre de 2013.
- Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J. W., Wallach, H., Daumé III, H., & Crawford, K. (2021). Datasheets for datasets. *Communications of the ACM, 64*(12), 86-92. https://doi.org/10.1145/3458723
- Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., Spitzer, E., Raji, I. D., & Gebru, T. (2019). Model cards for model reporting. *Proceedings of the Conference on Fairness, Accountability, and Transparency*, 220-229. https://doi.org/10.1145/3287560.3287596
- NIST. (2023). *Artificial Intelligence Risk Management Framework (AI RMF 1.0)*. https://doi.org/10.6028/NIST.AI.100-1
- OECD. (2019, enmendada el 3 de mayo de 2024). *Recommendation of the Council on Artificial Intelligence*, OECD/LEGAL/0449. https://legalinstruments.oecd.org/en/instruments/OECD-LEGAL-0449
- Reglamento (UE) 2024/1689 del Parlamento Europeo y del Consejo, por el que se establecen normas armonizadas en materia de inteligencia artificial. https://eur-lex.europa.eu/eli/reg/2024/1689/oj
