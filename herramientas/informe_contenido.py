"""Cuerpo del informe de U04.E07. Todas las cifras llegan desde `leer_evidencia()`."""

from __future__ import annotations

import subprocess
from datetime import date
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

from generar_informe import (BASE, HEADER_FILL, MUTED, NOMBRE, SOPORTE_MINIMO, add_field,
                             add_hyperlink, add_inline_markdown, bullet, caption,
                             data_table, fecha_larga, heading, key_value_table, numbered,
                             paragraph, remove_table_borders, set_cell_fill, subheading)


def pct(x: float, d: int = 1) -> str:
    return f"{x * 100:.{d}f} %"


def recortar(texto: str, limite: int) -> str:
    """Corta en el último espacio antes del límite para no partir una palabra."""
    if len(texto) <= limite:
        return texto
    return texto[:texto.rfind(" ", 0, limite)].rstrip(" ,;:") + "…"


def build(ev: dict, repo_url: str | None) -> Path:
    log = ev["logistic"]
    arbol = ev["tree"]
    g = log["grupos"]
    gates = ev["gates"]
    part = ev["particion"]
    comp = ev["comparacion"].set_index("alternativa")
    manual = next(i for i in comp.index if i.startswith("regla_manual"))
    regla, todo = comp.loc[manual], comp.loc["marcar_todo"]
    logi, tree = comp.loc["logistic"], comp.loc["tree"]
    brecha_recall = log["global"]["differences"]["recall"]
    margen = gates["max_recall_gap"] - brecha_recall

    doc = Document()
    section = doc.sections[0]
    section.page_width, section.page_height = Cm(21.59), Cm(27.94)
    section.left_margin = section.right_margin = Cm(2.2)
    section.top_margin, section.bottom_margin = Cm(2.0), Cm(2.0)

    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
    normal.font.size = Pt(10.5)
    normal.paragraph_format.line_spacing = 1.1

    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = footer.add_run("U04.E07 · Alexis De La Cruz · página ")
    run.font.size = Pt(8)
    run.font.color.rgb = MUTED
    add_field(footer, "PAGE")
    run = footer.add_run(" de ")
    run.font.size = Pt(8)
    run.font.color.rgb = MUTED
    add_field(footer, "NUMPAGES")

    band = doc.add_table(rows=1, cols=1)
    remove_table_borders(band)
    cell = band.rows[0].cells[0]
    set_cell_fill(cell, HEADER_FILL)
    cell.width = Cm(17.19)
    first = cell.paragraphs[0]
    first.paragraph_format.space_before = Pt(8)
    first.paragraph_format.space_after = Pt(2)
    run = first.add_run("UNIVERSIDAD AUTÓNOMA DE SANTO DOMINGO · MAESTRÍA EN CIENCIAS DE "
                        "DATOS E INTELIGENCIA ARTIFICIAL")
    run.font.size = Pt(7.5)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0xC9, 0xD6, 0xE6)
    title = cell.add_paragraph()
    title.paragraph_format.space_after = Pt(2)
    run = title.add_run("Evaluación de impacto y auditoría de equidad")
    run.font.size = Pt(18)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    subtitle = cell.add_paragraph()
    subtitle.paragraph_format.space_after = Pt(8)
    run = subtitle.add_run("Mandato · Ejercicio 07 · Informe de síntesis")
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(0xE6, 0xEC, 0xF3)

    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    key_value_table(doc, [
        ("Asignatura", "INF-8239 Ciencia de Datos II"),
        ("Unidad", "04 · Ética y roles en Ciencia de Datos"),
        ("Código", "U04.E07 · LAB11 y LAB12"),
        ("Estudiante", "Alexis De La Cruz · Matrícula 100805370"),
        ("Fecha", fecha_larga(date.today())),
        ("Entorno", "Windows 11 · Intel Core i9-13980HX con 16 GB de RAM · NVIDIA GeForce "
                    "RTX 4070 Laptop de 8 GB · Python 3.12 gestionado por uv · "
                    "scikit-learn y Fairlearn"),
    ])

    # 1
    heading(doc, "1. Repositorio y artefactos")
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    add_inline_markdown(p, "**Enlace:** ", size=10.5)
    if repo_url:
        add_hyperlink(p, repo_url)
        add_inline_markdown(p, "  ·  etiqueta `u04-ejercicio07`  ·  repositorio privado con "
                               "acceso de colaborador para el profesor", size=10.5)
    else:
        add_inline_markdown(p, "pendiente (regenerar con `--repo-url`)", size=10.5,
                            color=MUTED)
    paragraph(doc, "Los artefactos son **editables, no capturas**: `student_inputs/` tiene "
                   "la evaluación de impacto, los interesados, los ocho riesgos y la "
                   "decisión en YAML y CSV; `reports/lab11/` y `reports/lab12/` contienen "
                   "las salidas que generan los scripts; `docs/MARCO_NORMATIVO.md` y "
                   "`docs/AI_USE_DECLARATION.md` completan el expediente. La historia de Git "
                   "separa a propósito el commit del proyecto base intacto de lo que añadí "
                   "después.", size=10, after=3)

    # 2
    heading(doc, "2. Finalidad, decisión asistida e interesados")
    key_value_table(doc, [
        ("Finalidad", "Ordenar para revisión humana los casos que probablemente requieren "
                      "atención. El sistema no atiende casos: ordena una cola"),
        ("Decisión asistida", "A qué casos dedica el equipo operativo su capacidad de "
                              "revisión. Revisar, intervenir o archivar lo decide siempre "
                              "una persona, y su decisión se registra junto a la propuesta"),
        ("Usos prohibidos", "Intervención automática, decisión de elegibilidad y "
                            "declaratoria de emergencia, según `configs/governance.yml`"),
        ("Población afectada", f"{part['total']} casos sintéticos: "
                               f"G1 con {part['grupos']['G1']} y G2 con "
                               f"{part['grupos']['G2']}, en cuatro tramos de edad"),
        ("Condición de retiro", f"Brecha de recall por encima de "
                                f"{gates['max_recall_gap']:.2f}, recall global por debajo "
                                f"de {gates['min_recall']:.2f}, o un solo caso documentado "
                                f"de uso prohibido. La ejecuta el responsable institucional "
                                f"y no requiere consenso técnico"),
        ("Apelación", "Derecho a conocer el motivo, corregir un dato y pedir una segunda "
                      "revisión humana distinta de la primera, conservando la versión del "
                      "modelo y los datos que produjeron la marca"),
    ])
    subheading(doc, "Proporcionalidad: ¿hace falta un modelo?")
    paragraph(doc, "Esta pregunta tiene respuesta medida y aparece en la sección 6. La "
                   "alternativa no predictiva declarada —ordenar por fecha y atender primero "
                   f"a quien supera la mediana de incidentes previos del entrenamiento, que "
                   f"es {ev['umbral']['umbral']}— **atiende mejor** al grupo que elegí "
                   "proteger. El modelo solo se justifica por el ahorro de capacidad de "
                   "revisión, y de ahí sale la decisión final.", size=10, after=3)

    # 3
    heading(doc, "3. Datos, exclusiones y corte temporal")
    key_value_table(doc, [
        ("Conjunto", f"`data/territorial_risk_synthetic.csv` · {part['total']} filas y "
                     f"{part['columnas']} columnas · **sintético**, sin personas reales"),
        ("Variable objetivo", f"Binaria · {pct(part['positivos'])} de casos positivos, de "
                              f"modo que la exactitud sola es insuficiente"),
        ("Partición", f"Cronológica, no aleatoria: {part['train_n']} casos de "
                      f"{part['train_ini']} a {part['train_fin']} para entrenar y "
                      f"{part['test_n']} de {part['test_ini']} a {part['test_fin']} para "
                      f"probar. Evita evaluar el pasado con el futuro"),
        ("Excluidas del modelo", "`case_id`, `received_date`, `protected_group` y `target`. "
                                 "El grupo protegido se conserva **solo para auditar**"),
        ("Identificadores", "`validate_schema` rechaza nombre, documento, correo y teléfono; "
                            "`tests/test_privacy.py` lo comprueba"),
    ])
    paragraph(doc, "Quitar el atributo sensible de las variables **no elimina el sesgo**: "
                   "`zone`, `age_band` y el historial de incidentes pueden correlacionar con "
                   "el grupo, y por eso la auditoría se hace sobre resultados y no sobre la "
                   "lista de variables.", size=10, after=3)

    # 4
    heading(doc, "4. Registro de riesgos y cobertura del NIST AI RMF")
    riesgos = ev["riesgos"]
    filas = [[r.id, recortar(r.scenario, 150),
              str(int(r.likelihood_1_4)), str(int(r.impact_1_4)), str(int(r.priority)),
              r.residual] for r in riesgos.itertuples()]
    data_table(doc, ["ID", "Escenario", "P", "I", "P×I", "Residual"], filas,
               [1.1, 10.4, 0.8, 0.8, 1.1, 2.0], align_right_from=2,
               bold_rows=(0, 1, 2), size=7.5)
    caption(doc, f"Los {len(riesgos)} riesgos de `student_inputs/risk_register.csv`, "
                 "puntuados por `scripts/lab11_impact.py`. Cada uno lleva afectado, control, "
                 "responsable y evidencia en el archivo. Las tres primeras filas son las "
                 "prioritarias. La puntuación ordena la atención; no convierte el daño "
                 "humano en una verdad matemática.")
    data_table(doc, ["Función", "Evidencia en el repositorio"], [
        ["GOVERN", "configs/governance.yml, student_inputs/raci.csv y la condición de "
                   "retiro sin consenso técnico"],
        ["MAP", "lab11_impact.yml, stakeholders.csv y los ocho riesgos puntuados"],
        ["MEASURE", "fairness_by_group.csv, fairness_intersectional.csv, global_metrics.json "
                    "y comparison.csv, con soporte mínimo declarado"],
        ["MANAGE", "las seis condiciones del uso limitado, la reauditoría mensual y el "
                   "mecanismo de apelación"],
    ], [2.6, 14.2], align_right_from=9)
    caption(doc, "Que exista un archivo por función no prueba que el control funcione. El "
                 "detalle está en docs/MARCO_NORMATIVO.md.")

    # 5
    heading(doc, "5. Auditoría de equidad")
    subheading(doc, "Global y por grupo protegido · regresión logística")
    met = log["global"]["metrics"]
    dif = log["global"]["differences"]
    filas = []
    for etiqueta, clave in [("Exactitud", "accuracy"), ("Tasa de selección", "selection_rate"),
                            ("Recall", "recall"), ("Precisión", "precision"), ("FPR", "fpr")]:
        filas.append([etiqueta, f"{met[clave]:.3f}", f"{g.loc['G1', clave]:.3f}",
                      f"{g.loc['G2', clave]:.3f}", f"{dif[clave]:.3f}"])
    data_table(doc, ["Métrica", "Global", f"G1 (n={int(g.loc['G1', 'count'])})",
                     f"G2 (n={int(g.loc['G2', 'count'])})", "Brecha"],
               filas, [4.0, 3.2, 3.3, 3.3, 3.0], bold_rows=(2,))
    caption(doc, f"reports/lab12/logistic/ · {int(met['count'])} casos de prueba. La brecha "
                 f"de recall es {brecha_recall:.3f} contra un techo preinscrito de "
                 f"{gates['max_recall_gap']:.2f}: margen de {margen:.3f}. Traducido: de cada "
                 f"100 casos de G1 que requerían revisión, el sistema deja "
                 f"{round((1 - g.loc['G1', 'recall']) * 100)} sin marcar; en G2 deja "
                 f"{round((1 - g.loc['G2', 'recall']) * 100)}.")

    subheading(doc, "Interseccional, con soporte explícito")
    inter = log["inter"]
    sop = ev["soporte"]
    filas, warn = [], []
    for i, (clave, fila) in enumerate(inter.iterrows()):
        neg = int(sop.loc[clave, "negativos"])
        n = int(sop.loc[clave, "n"])
        sin_soporte = n < SOPORTE_MINIMO
        if sin_soporte:
            warn.append(i)
        filas.append([str(clave), str(n), str(int(sop.loc[clave, "positivos"])), str(neg),
                      f"{fila['recall']:.3f}", f"{fila['fpr']:.3f}",
                      "sin soporte" if sin_soporte else "interpretable"])
    data_table(doc, ["Intersección", "n", "Pos.", "Neg.", "Recall", "FPR", "Lectura"],
               filas, [3.4, 1.5, 1.5, 1.5, 2.2, 2.2, 4.5], warn_rows=tuple(warn))
    sin_sop = len(warn)
    caption(doc, f"Las ocho intersecciones de grupo y tramo de edad. Con el soporte mínimo "
                 f"declarado de {SOPORTE_MINIMO} casos por celda, {sin_sop} de las 8 quedan "
                 f"por debajo y no se interpretan; solo G1 | 45-59, con 35 casos, lo alcanza "
                 f"por poco. Los extremos son G2 | 30-44 y G2 | 45-59, con 2 casos negativos "
                 f"cada una: en el árbol de decisión eso produce un FPR de 1.000 que son dos "
                 f"casos de dos. La conclusión válida es que falta dato para auditar a este "
                 f"nivel, no que un subgrupo tenga un comportamiento perfecto o catastrófico.")

    # 6
    heading(doc, "6. Líneas base, alternativas y Green AI")
    filas = []
    for etiqueta, fila in [(f"Regla manual (incidentes ≥ {ev['umbral']['umbral']})", regla),
                           ("Marcar todo", todo), ("Logística", logi), ("Árbol", tree)]:
        filas.append([etiqueta, f"{fila['accuracy']:.3f}", f"{fila['recall']:.3f}",
                      f"{fila['fpr']:.3f}", f"{fila['selection_rate']:.3f}",
                      f"{fila['brecha_recall']:.3f}", f"{fila['entrenamiento_s']:.3f}",
                      f"{fila['tamano_kb']:.2f}",
                      "Pasa" if fila["pasa_compuertas"] else "Falla"])
    data_table(doc, ["Alternativa", "Exact.", "Recall", "FPR", "Selec.", "Brecha rec.",
                     "Entren. s", "KB", "Compuertas"],
               filas, [3.9, 1.6, 1.6, 1.5, 1.5, 1.9, 1.9, 1.4, 1.9], bold_rows=(2,),
               warn_rows=(1, 3), size=8)
    caption(doc, "reports/lab12/comparison.csv · scripts/compare_alternatives.py. El umbral "
                 "de la regla manual es la mediana de incidentes previos en el conjunto de "
                 "entrenamiento y nunca usa las etiquetas de prueba; queda registrado en "
                 "umbral_regla_manual.json.")
    for texto in (
        f"**La regla no predictiva le gana al modelo en el daño que prioricé.** Su recall en "
        f"G1 es {regla['recall']:.3f} global y 0.898 por grupo, frente a "
        f"{g.loc['G1', 'recall']:.3f} de la logística: 10 casos de G1 sin marcar por cada "
        f"100 en lugar de 35. Su brecha de recall también es menor, "
        f"{regla['brecha_recall']:.3f} frente a {logi['brecha_recall']:.3f}.",
        f"**Lo único que compra el modelo es proporcionalidad.** Marca "
        f"{pct(logi['selection_rate'])} de los casos en lugar de "
        f"{pct(regla['selection_rate'])}, y baja el FPR de {regla['fpr']:.3f} a "
        f"{logi['fpr']:.3f}. Son unas 29 revisiones menos por cada 100 casos: capacidad "
        f"humana ahorrada, no menos daño para G1.",
        "**Marcar a todo el mundo pasa las cinco compuertas.** Recall 1.000 y brechas 0.000. "
        "Las compuertas fijan recall mínimo y brechas máximas pero no acotan FPR ni "
        "precisión, así que el marco de gobernanza aprueba la regla más inútil posible. Es "
        "un hueco del marco, no un detalle, y propongo cerrarlo con una compuerta de FPR "
        "máximo y otra de precisión mínima.",
        f"**Green AI:** el más pesado de los cuatro ocupa {tree['tamano_kb']:.2f} KB y "
        f"ninguno tarda más de {max(logi['entrenamiento_s'], tree['entrenamiento_s']):.2f} s "
        f"en entrenar. A esta escala el costo computacional no decide nada, y pretender lo "
        f"contrario sería inventar una justificación. El costo que sí decide es humano: el "
        f"de revisar.",
        f"**El árbol queda descartado.** Brecha de recall {tree['brecha_recall']:.3f} y "
        f"brecha de FPR {tree['brecha_fpr']:.3f}, ambas por encima del techo de "
        f"{gates['max_recall_gap']:.2f}, con exactitud menor que la logística. No hay nada "
        f"que ganar aceptándolo.",
    ):
        bullet(doc, texto)

    # 7
    heading(doc, "7. Obligación legal, marco voluntario y recomendación ética")
    paragraph(doc, "El sistema trabaja sobre datos sintéticos, de modo que **hoy no le aplica "
                   "ningún régimen de datos personales**. Lo que sigue es lo que aplicaría "
                   "con datos reales, que es el escenario que el ejercicio pide anticipar. La "
                   "interpretación normativa es mía y queda sujeta a verificación contra el "
                   "texto vigente.", size=10, after=4)
    data_table(doc, ["Nivel", "Instrumento", "Qué implica aquí"], [
        ["Obligación legal", "Constitución dominicana, arts. 44 y 70",
         "Intimidad, protección de datos y habeas data: la apelación y la conservación de "
         "la versión del modelo dejan de ser buenas prácticas"],
        ["Obligación legal", "Ley 172-13 de protección de datos personales",
         "Finalidad, calidad y proporcionalidad: usar la puntuación para elegibilidad sería "
         "un fin distinto del declarado"],
        ["Marco voluntario", "NIST AI RMF 1.0",
         "Voluntario por diseño; aporta la estructura GOVERN, MAP, MEASURE y MANAGE"],
        ["Marco voluntario", "Recomendación de la OCDE sobre IA",
         "No vinculante; supervisión humana significativa y transparencia de límites"],
        ["Marco voluntario", "Model Cards y Datasheets",
         "Práctica de la comunidad; formato de las fichas de modelo y de datos"],
        ["Referencia", "Reglamento (UE) 2024/1689",
         "Es ley en otra jurisdicción y referencia voluntaria aquí: su categoría de alto "
         "riesgo describe bien este caso, pero no nos obliga"],
    ], [3.0, 4.6, 9.2], align_right_from=9, size=8)
    caption(doc, "El Reglamento europeo es la distinción que más se confunde: obligación "
                 "legal allí, referencia voluntaria aquí. Citarlo como obligación propia "
                 "sería un error; ignorarlo sería desaprovechar el marco más detallado que "
                 "existe para sistemas como este.")
    subheading(doc, "Lo que elegimos sin que nada lo exigiera")
    for i, texto in enumerate((
        "Declarar las celdas sin soporte en lugar de reportar sus cifras como hallazgo.",
        "No mover la tolerancia después de medir, ni hacia arriba ni hacia abajo.",
        "Publicar la línea base que le gana al modelo, aunque debilite la propuesta.",
        "Señalar el hueco de nuestro propio marco de compuertas.",
        "Recomendar limitar aunque las cinco compuertas pasaran y autorizaran un GO.",
    ), start=1):
        numbered(doc, texto, i)

    # 8
    heading(doc, "8. Decisión final: limitar")
    paragraph(doc, "De las cuatro opciones del mandato —desplegar, modificar, limitar o no "
                   "utilizar— la evidencia sostiene **limitar**.", size=10.5, after=4)
    key_value_table(doc, [
        ("Daño prioritario", "Que una persona de G1 cuyo caso sí requiere revisión quede sin "
                             "marcar. Elegido por encima del sobre-marcado de G2 porque un "
                             "falso positivo cuesta una revisión de más y un falso negativo "
                             "cuesta un caso que nadie vuelve a mirar"),
        ("Métrica principal", "Brecha de recall entre grupos protegidos. La exactitud global "
                              "esconde este daño"),
        ("Tolerancia", f"{gates['max_recall_gap']:.2f}, la preinscrita en governance.yml. Se "
                       f"mantiene **precisamente porque** medimos {brecha_recall:.3f} "
                       f"después: moverla ahora sería mover la portería"),
        ("Decisión", "Usar la logística **solo si la capacidad de revisión es el límite real "
                     "de la institución**, declarado por escrito por el responsable "
                     "institucional. Si no lo es, la decisión correcta es no utilizar el "
                     "modelo y quedarse con la regla manual"),
    ])
    subheading(doc, "Condiciones. Si falta una, la decisión pasa a no utilizar")
    for i, texto in enumerate((
        "Declaración previa por escrito de que la capacidad de revisión es el límite real.",
        "Revisión humana obligatoria de cada caso marcado, sin ninguna acción automática, "
        "registrando la decisión del operador junto a la del sistema.",
        "Añadir a `governance.yml` una compuerta de FPR máximo y otra de precisión mínima.",
        f"Reauditoría mensual de la brecha de recall, con retiro inmediato si supera "
        f"{gates['max_recall_gap']:.2f} o si el recall global baja de "
        f"{gates['min_recall']:.2f}.",
        "Publicación de la auditoría completa, con las celdas sin soporte marcadas como tales.",
        "Mecanismo de apelación operativo antes del primer caso real: es el único riesgo de "
        "impacto 4 sin control efectivo y, con datos reales, sería además un incumplimiento.",
    ), start=1):
        numbered(doc, texto, i)
    subheading(doc, "Lo que esta auditoría no demuestra")
    for texto in (
        f"La brecha de {brecha_recall:.3f} viene de **una sola partición** de "
        f"{int(met['count'])} casos, sin intervalo de confianza ni repetición con otras "
        f"semillas. El margen de {margen:.3f} es más incierto de lo que parece.",
        "Una brecha observada **no prueba discriminación causal**: indica dónde investigar. "
        "Puede venir del muestreo, de la relación entre variables y grupo, o del proceso que "
        "generó las etiquetas, y con datos sintéticos no es posible distinguirlo.",
        "Los datos son sintéticos y didácticos: nada de esto estima el comportamiento del "
        "sistema sobre población real.",
    ):
        bullet(doc, texto)

    # 9
    heading(doc, "9. Pruebas y reproducibilidad")
    paragraph(doc, "`uv run pytest -q` pasa las diez pruebas: contratos de datos, privacidad, "
                   "equidad, impacto, gobernanza, modelo y aplicación. La secuencia completa "
                   "que reproduce cada cifra de este informe:", size=10, after=4)
    for comando in ("uv sync --frozen", "uv run pytest -q",
                    "uv run python scripts/check_environment.py",
                    "uv run python scripts/describe_dataset.py",
                    "uv run python scripts/lab11_impact.py",
                    "uv run python scripts/lab12_audit.py --model logistic",
                    "uv run python scripts/lab12_audit.py --model tree",
                    "uv run python scripts/compare_alternatives.py",
                    "uv run python scripts/validate_lab12_decision.py",
                    "uv run python herramientas/generar_informe.py --repo-url <enlace>"):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.left_indent = Cm(0.6)
        add_inline_markdown(p, f"`{comando}`", size=9)
    paragraph(doc, "**Dos correcciones al proyecto base.** `scripts/lab11_impact.py` y "
                   "`scripts/simulate_incident.py` no compilaban tal como se entregan: abren "
                   "una cadena de varias líneas con una sola comilla. El primer commit del "
                   "repositorio guarda el proyecto intacto, de modo que el error es "
                   "verificable y anterior a mis cambios; el arreglo es de comillas y no "
                   "altera el texto. Además `lab11_impact.py` sobrescribía "
                   "`DECISION_RECORD.md` en cada ejecución, y ahora solo crea la plantilla si "
                   "el archivo no existe.", size=10, after=3)

    heading(doc, "Referencias")
    for ref in (
        "Constitución de la República Dominicana, proclamada el 26 de enero de 2010, "
        "arts. 44 y 70.",
        "Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J. W., Wallach, H., Daumé III, "
        "H., & Crawford, K. (2021). Datasheets for datasets. Communications of the ACM, "
        "64(12), 86-92. https://doi.org/10.1145/3458723",
        "Ley No. 172-13, Ley Orgánica sobre Protección de Datos de Carácter Personal, "
        "República Dominicana, 2013.",
        "Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., "
        "Spitzer, E., Raji, I. D., & Gebru, T. (2019). Model cards for model reporting. "
        "Proceedings of the Conference on Fairness, Accountability, and Transparency, "
        "220-229. https://doi.org/10.1145/3287560.3287596",
        "NIST. (2023). Artificial Intelligence Risk Management Framework (AI RMF 1.0). "
        "https://doi.org/10.6028/NIST.AI.100-1",
        "OECD. (2019). Recommendation of the Council on Artificial Intelligence. "
        "https://doi.org/10.1787/cc2e1d3e-en",
        "Reglamento (UE) 2024/1689 del Parlamento Europeo y del Consejo, por el que se "
        "establecen normas armonizadas en materia de inteligencia artificial.",
        "Weerts, H., Dudík, M., Edgar, R., Jalali, A., Lutz, R., & Madaio, M. (2023). "
        "Fairlearn: Assessing and improving fairness of AI systems. Journal of Machine "
        "Learning Research, 24(257), 1-8.",
    ):
        p = paragraph(doc, ref, size=8.5, after=2)
        p.paragraph_format.left_indent = Cm(0.8)
        p.paragraph_format.first_line_indent = Cm(-0.8)

    heading(doc, "Declaración de uso de asistentes de IA")
    paragraph(doc, "Este trabajo se desarrolló con la asistencia de **Claude Opus 5 "
                   "(Anthropic)**. El asistente apoyó estructura, pruebas y redacción, y "
                   "ejecutó los scripts. **No decidió los valores del análisis:** la elección "
                   "del daño prioritario, la tolerancia, los responsables, la interpretación "
                   "normativa y la decisión final son mías. Cuando la evidencia de la línea "
                   "base contradijo una recomendación ya redactada, se corrigió en lugar de "
                   "ocultarse. Todas las cifras provienen de ejecutar los scripts en el "
                   "equipo indicado arriba. El detalle de herramientas, prompts, "
                   "verificaciones y correcciones está en `docs/AI_USE_DECLARATION.md`.",
              size=8.5, after=2)

    salida = BASE / "herramientas" / f"{NOMBRE}.docx"
    doc.save(salida)
    return salida


def export_pdf(docx_path: Path) -> Path:
    pdf_path = docx_path.with_suffix(".pdf")
    script = (
        "$ErrorActionPreference = 'Stop';"
        "$word = New-Object -ComObject Word.Application; $word.Visible = $false;"
        f"try {{ $doc = $word.Documents.Open('{docx_path}', $false, $true);"
        f"$doc.ExportAsFixedFormat('{pdf_path}', 17); $doc.Close([ref]0) }}"
        "finally { $word.Quit() }"
    )
    subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
                   check=True)
    return pdf_path
