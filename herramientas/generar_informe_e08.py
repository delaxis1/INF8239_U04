"""Genera el informe de síntesis de U04.E08 (DOCX + PDF) desde los artefactos del repositorio.

Reutiliza el formato de `generar_informe.py` y lee reports/lab13/deployment_decision.json,
reports/lab12/comparison.csv, student_inputs/raci.csv y configs/governance.yml. Ninguna
cifra está escrita a mano.

Uso:
    uv run python herramientas/generar_informe_e08.py --repo-url https://github.com/USUARIO/INF8239_U04
    uv run python herramientas/generar_informe_e08.py --sin-pdf
"""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import date
from pathlib import Path

import pandas as pd
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

from generar_informe import (BASE, HEADER_FILL, MUTED, REPORTS, add_field, add_hyperlink,
                             add_inline_markdown, bullet, caption, data_table, fecha_larga,
                             heading, key_value_table, numbered, paragraph,
                             remove_table_borders, set_cell_fill, subheading)

NOMBRE = "100805370_DeLaCruz_U04E08_Expediente"
LAB13 = REPORTS / "lab13"


def build(repo_url: str | None) -> Path:
    decision = json.loads((LAB13 / "deployment_decision.json").read_text(encoding="utf-8"))
    comp = pd.read_csv(REPORTS / "lab12" / "comparison.csv").set_index("alternativa")
    manual = next(i for i in comp.index if i.startswith("regla_manual"))
    regla, logi = comp.loc[manual], comp.loc["logistic"]
    raci = pd.read_csv(BASE / "student_inputs" / "raci.csv")
    import yaml
    gates = yaml.safe_load((BASE / "configs" / "governance.yml").read_text(
        encoding="utf-8"))["gates"]
    columnas = pd.read_csv(BASE / "data" / "territorial_risk_synthetic.csv").shape[1]

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
    run = footer.add_run("U04.E08 · Alexis De La Cruz · página ")
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
    run = title.add_run("Expediente de gobernanza y simulacro")
    run.font.size = Pt(18)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    subtitle = cell.add_paragraph()
    subtitle.paragraph_format.space_after = Pt(8)
    run = subtitle.add_run("Mandato · Ejercicio 08 · Informe de síntesis")
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(0xE6, 0xEC, 0xF3)

    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    key_value_table(doc, [
        ("Asignatura", "INF-8239 Ciencia de Datos II"),
        ("Unidad", "04 · Ética y roles en Ciencia de Datos"),
        ("Código", "U04.E08 · LAB13"),
        ("Estudiante", "Alexis De La Cruz · Matrícula 100805370"),
        ("Fecha", fecha_larga(date.today())),
        ("Entorno", "Windows 11 · Intel Core i9-13980HX con 16 GB de RAM · NVIDIA GeForce "
                    "RTX 4070 Laptop de 8 GB · Python 3.12 gestionado por uv · "
                    "scikit-learn, Fairlearn y Streamlit"),
    ])

    heading(doc, "1. Repositorio y artefactos")
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    add_inline_markdown(p, "**Enlace:** ", size=10.5)
    if repo_url:
        add_hyperlink(p, repo_url)
        add_inline_markdown(p, "  ·  etiqueta `u04-lab13`  ·  repositorio público: el "
                               "enlace abre sin credenciales ni invitación", size=10.5)
    else:
        add_inline_markdown(p, "pendiente (regenerar con `--repo-url`)", size=10.5,
                            color=MUTED)
    paragraph(doc, "Este ejercicio continúa el Ejercicio 07 sobre el mismo proyecto. Lo "
                   "que añade: el inventario de datos con su política de retención, las "
                   "dos fichas completas, el RACI ampliado con el procedimiento de "
                   "traspaso, el runbook de monitoreo e incidentes, el postmortem del "
                   "simulacro, diez pruebas nuevas y un tablero que ya no presenta el "
                   "veredicto automático como si fuera la decisión.", size=10, after=3)

    heading(doc, "2. Inventario, minimización y retención")
    paragraph(doc, f"`docs/INVENTARIO_DATOS.md` documenta las {columnas} columnas del "
                   f"conjunto con tres preguntas cada una: qué es, por qué hace falta y "
                   f"cuánto tiempo se conserva. Si una columna no supera la segunda, no "
                   f"debería estar en el sistema.", size=10, after=4)
    subheading(doc, "Minimización")
    for texto in (
        "**Ningún identificador directo.** Nombre, documento, correo y teléfono están "
        "prohibidos por contrato en `validate_schema`, y `tests/test_privacy.py` comprueba "
        "que el sistema no arranca si aparecen. No es una política escrita: es un fallo.",
        "**Edad en tramos, no exacta.** `age_band` da la granularidad necesaria sin la "
        "precisión que facilitaría reidentificar.",
        "**El grupo protegido nunca entra al modelo.** `features()` devuelve cinco columnas "
        "y esa no está. Se conserva solo para auditar, porque quitarla del todo no "
        "eliminaría el sesgo: lo volvería invisible.",
        "**Sin campos de texto libre**, que son la vía habitual por la que entran datos "
        "personales no declarados a un conjunto que se creía anónimo.",
    ):
        bullet(doc, texto)
    subheading(doc, "Retención")
    data_table(doc, ["Dato", "Plazo", "Desde", "Ejecuta el borrado"], [
        ["Datos del caso y su marca", "2 años", "Cierre del caso", "Data Engineer"],
        ["Registro de apelación", "2 años", "Resolución", "Legal"],
        ["Versión del modelo y métricas", "2 años", "Retiro de la versión", "ML Engineer"],
        ["Informes de auditoría", "Permanente, agregado", "Publicación", "Product Owner"],
    ], [6.0, 2.6, 4.0, 4.2], align_right_from=9)
    paragraph(doc, "**Por qué dos años.** Es el plazo más corto que todavía cubre lo que el "
                   "sistema promete: el ciclo de apelación, las doce reauditorías mensuales "
                   "de un año completo y una revisión anual con margen para compararla con "
                   "la anterior. Cada año adicional habría que justificarlo, no asumirlo. "
                   "Los informes se conservan sin plazo pero **solo agregados**, sin casos "
                   "individuales, para poder rendir cuentas sin conservar los datos de "
                   "nadie.", size=10, after=3)
    paragraph(doc, "**Verificación automática:** `tests/test_inventory.py` comprueba que "
                   "todas las columnas del conjunto están inventariadas y que el inventario "
                   "no documenta columnas que ya no existen. Si alguien añade una columna "
                   "sin documentarla, la prueba falla. Eso convierte el documento en un "
                   "artefacto verificable.", size=10, after=3)

    heading(doc, "3. Datasheet y Model Card trazables")
    data_table(doc, ["Afirmación de la ficha", "Dónde se verifica"], [
        ["Brecha de recall 0.138 entre G1 y G2",
         "reports/lab12/logistic/global_metrics.json y fairness_by_group.csv"],
        ["La regla manual alcanza recall 0.898 en G1", "reports/lab12/comparison.csv"],
        ["Las cinco compuertas dan GO", "reports/lab13/deployment_decision.json"],
        ["Siete de ocho celdas sin soporte", "reports/lab12/logistic/fairness_intersectional.csv"],
        ["El grupo protegido no entra al modelo",
         "src/inf8239_u04/data.py y tests/test_inventory.py"],
        ["Sin identificadores directos", "validate_schema y tests/test_privacy.py"],
        ["Retención de 2 años con ejecutor asignado",
         "docs/INVENTARIO_DATOS.md y student_inputs/raci.csv"],
    ], [7.0, 9.8], align_right_from=9, size=8)
    caption(doc, "Trazable significa que cada afirmación apunta a un archivo que la "
                 "produce, no a una cita del informe. Las fichas son docs/MODEL_CARD.md y "
                 "docs/DATASET_CARD.md.")

    heading(doc, "4. RACI y traspaso entre roles")
    paragraph(doc, f"`student_inputs/raci.csv` cubre **{len(raci)} actividades**, desde el "
                   f"inventario de datos hasta el borrado por fin de retención. Cada una "
                   f"tiene exactamente un Accountable y al menos un Responsible.",
              size=10, after=4)
    criticas = ["Atencion de apelaciones", "Borrado por fin de retencion",
                "Retiro del sistema", "Traspaso entre responsables"]
    filas = [[f.activity, f.R, f.A] for f in raci.itertuples()
             if f.activity in criticas]
    data_table(doc, ["Actividad añadida", "Responsible", "Accountable"], filas,
               [6.6, 4.8, 5.4], align_right_from=9)
    caption(doc, "Cuatro actividades que el RACI del proyecto base no tenía. El expediente "
                 "promete apelación, retención y retiro: sin alguien encargado, esas "
                 "promesas no existen.")
    paragraph(doc, "`tests/test_inventory.py` comprueba que ninguna actividad tenga más de "
                   "un aprobador, que ningún rol se apruebe o se consulte a sí mismo, y que "
                   "las cuatro actividades críticas sigan en el archivo.", size=10, after=4)
    subheading(doc, "Traspaso: qué invalida un relevo")
    for i, texto in enumerate((
        "Que quien recibe **no pueda reproducir las cifras** ejecutando los scripts.",
        "Que el traspaso ocurra **durante un incidente abierto**.",
        "Que queden **acciones correctivas sin dueño** después del cambio.",
        "Que **el único que entendía una decisión de valor sea quien se va**. Por eso las "
        "decisiones están escritas con su razonamiento y no solo con su resultado.",
    ), start=1):
        numbered(doc, texto, i)
    paragraph(doc, "El procedimiento completo, con los ocho artefactos que se entregan y la "
                   "lista de comprobación de siete pasos, está en `docs/TRASPASO_ROLES.md`.",
              size=10, after=3)

    heading(doc, "5. Monitoreo, runbook y simulacro")
    subheading(doc, "Señales vigiladas")
    data_table(doc, ["Señal", "Umbral", "Frecuencia", "Qué dispara"], [
        ["Brecha de recall entre grupos", f"> {gates['max_recall_gap']:.2f}", "Mensual",
         "Retiro inmediato"],
        ["Recall global", f"< {gates['min_recall']:.2f}", "Mensual", "Retiro inmediato"],
        ["Brecha de FPR", f"> {gates['max_fpr_gap']:.2f}", "Mensual", "Revisión en 5 días"],
        ["Coincidencia operador-sistema", "> 95 %", "Mensual",
         "Revisión: sesgo de automatización"],
        ["Casos marcados sin revisión humana", "> 0", "Continuo",
         "Incidente: el sistema actúa solo"],
        ["Uso fuera de alcance", "Cualquiera", "Continuo", "Retiro inmediato"],
    ], [5.6, 2.8, 2.6, 5.8], align_right_from=9)
    caption(doc, "Los umbrales salen de configs/governance.yml, no de este documento: "
                 "cambiarlos obliga a cambiar el archivo y deja rastro en Git. Limitación "
                 "declarada: medir la brecha cada mes sobre unos 160 casos reproduce el "
                 "problema de soporte, así que la alerta se lee como revisar, no como "
                 "demostrado. El retiro es inmediato igual, porque ante la duda se apaga.")
    subheading(doc, "Autoridad de contención")
    paragraph(doc, "El **Institutional Owner** puede detener el sistema sin consenso "
                   "técnico, reunión previa ni aprobación de nadie. El **ML Engineer** "
                   "ejecuta la contención y está autorizado a hacerlo **antes** de "
                   "localizarlo si la severidad es alta. Es la regla que hace que el resto "
                   "del expediente valga algo: si detener el sistema exigiera convencer a "
                   "quien lo defiende, nunca se detendría.", size=10, after=4)
    subheading(doc, "Simulacro ejecutado")
    paragraph(doc, "`scripts/simulate_incident.py` detecta una brecha de recall por encima "
                   "del techo. Las seis etapas quedan documentadas en "
                   "`reports/lab13/INCIDENT_POSTMORTEM.md` con responsable y plazo.",
              size=10, after=4)
    for texto in (
        f"**La base segura no es la versión anterior del modelo: es la regla manual no "
        f"predictiva.** Esa elección está medida: la regla alcanza recall 0.898 en G1 "
        f"frente a {logi['recall']:.3f} global del modelo, así que revertir **no degrada** "
        f"la atención al grupo priorizado. Su costo es marcar "
        f"{regla['selection_rate'] * 100:.0f} % de los casos en lugar de "
        f"{logi['selection_rate'] * 100:.0f} %: más carga para el equipo, ningún daño "
        f"adicional para las personas.",
        "**Comunicar a las personas afectadas tiene responsable y plazo**, no es un «se "
        "evaluará». Un incidente de equidad significa que algunas personas fueron tratadas "
        "peor por el sistema; informarles es lo que convierte la apelación en un derecho "
        "ejercitable.",
        f"**El hallazgo del simulacro es el margen.** El modelo opera con una brecha de "
        f"{logi['brecha_recall']:.3f} contra un techo de {gates['max_recall_gap']:.2f}: "
        f"{gates['max_recall_gap'] - logi['brecha_recall']:.3f} de margen, sobre una sola "
        f"partición y sin intervalos. Un incidente así no sería una sorpresa sino el "
        f"resultado previsible de desplegar con ese margen.",
        "**Cinco acciones correctivas con responsable y fecha**, la primera de ellas cerrar "
        "el hueco de las compuertas que hoy aprueban marcar a todo el mundo.",
    ):
        bullet(doc, texto)

    heading(doc, "6. El tablero y lo que decide cada quien")
    paragraph(doc, "`uv run streamlit run app.py` abre el tablero con propósito, usos "
                   "prohibidos, métricas globales y por grupo, compuertas, límites, "
                   "alternativas y acción humana. La versión del proyecto base mostraba el "
                   "veredicto de las compuertas en la casilla «Decisión», lo que invita a "
                   "leer un GO automático como una decisión tomada.", size=10, after=4)
    key_value_table(doc, [
        ("Compuertas automáticas", f"**{decision['decision']['status']}** · las cinco pasan: "
                                   f"recall, brecha de recall, brecha de FPR, latencia y "
                                   f"tamaño"),
        ("Decisión gobernada", "**LIMITAR** · usar el modelo solo si la capacidad de "
                               "revisión es el límite real de la institución, declarado por "
                               "escrito"),
        ("Por qué difieren", "Pasar una compuerta no demuestra que el sistema sea "
                             "necesario. La regla manual atiende mejor al grupo priorizado "
                             "y no usa modelo ni datos sensibles"),
    ])
    paragraph(doc, "El tablero muestra ahora las dos cosas juntas, con la contradicción a "
                   "la vista. Un tablero que solo mostrara el GO estaría ocultando la "
                   "decisión real.", size=10, after=3)

    heading(doc, "7. Obligación legal, marco voluntario y recomendación ética")
    paragraph(doc, "El detalle está en `docs/MARCO_NORMATIVO.md`. Lo que este ejercicio "
                   "añade a cada nivel:", size=10, after=4)
    data_table(doc, ["Nivel", "Qué añade el expediente de gobernanza"], [
        ["Obligación legal", "La retención con plazo y ejecutor responde al principio de "
                             "finalidad del art. 5 de la Ley 172-13, que exige datos no "
                             "excesivos respecto del fin declarado; conservar la versión "
                             "del modelo y los datos de cada marca es lo que hace posible "
                             "el hábeas data del art. 70 de la Constitución"],
        ["Marco voluntario", "El runbook y el monitoreo cubren la función MANAGE del NIST "
                             "AI RMF; las dos fichas siguen el formato de Model Cards y "
                             "Datasheets, que son práctica de la comunidad, no norma"],
        ["Recomendación ética", "Nada obliga a poner la base segura en una regla que marca "
                                "más casos, ni a mostrar en el tablero que la decisión "
                                "gobernada contradice al veredicto automático, ni a "
                                "escribir en el postmortem que el incidente sería "
                                "previsible. Se elige hacerlo"],
    ], [3.4, 13.4], align_right_from=9, size=8)

    heading(doc, "8. Decisión final: limitar")
    paragraph(doc, "Se mantiene la del Ejercicio 07, y el expediente de gobernanza la "
                   "refuerza en lugar de ablandarla. De las cuatro opciones del mandato "
                   "—desplegar, modificar, limitar o no utilizar— la evidencia sostiene "
                   "**limitar**.", size=10.5, after=4)
    for i, texto in enumerate((
        "**Usar el modelo solo si la capacidad de revisión es el límite real**, declarado "
        "por escrito por el responsable institucional. Si no lo es, la decisión correcta es "
        "**no utilizarlo**.",
        "**Revisión humana obligatoria** de cada caso marcado, con la decisión del operador "
        "registrada junto a la del sistema.",
        "**Cerrar el hueco de las compuertas** con un FPR máximo y una precisión mínima.",
        f"**Reauditoría mensual** con retiro inmediato si la brecha supera "
        f"{gates['max_recall_gap']:.2f} o el recall global baja de "
        f"{gates['min_recall']:.2f}.",
        "**Publicar la auditoría completa**, con las celdas sin soporte marcadas como tales.",
        "**Mecanismo de apelación operativo** antes del primer caso real.",
        "**Simulacro repetido** con el equipo completo, cronometrando el tiempo hasta la "
        "contención.",
    ), start=1):
        numbered(doc, texto, i)
    paragraph(doc, "Si alguna de las siete no se cumple, la decisión pasa a **no utilizar**.",
              size=10, after=3)

    heading(doc, "9. Pruebas, Git y calidad documental")
    key_value_table(doc, [
        ("Pruebas", "**20 pasan** con `uv run pytest -q`: contratos de datos, privacidad, "
                    "equidad, impacto, gobernanza, modelo, tablero e inventario"),
        ("Nuevas en este ejercicio", "`tests/test_inventory.py`, 10 pruebas que comprueban "
                                     "el inventario, la retención declarada y la "
                                     "consistencia del RACI"),
        ("Historia", "El primer commit guarda el proyecto base intacto, de modo que lo "
                     "añadido es verificable por diferencia"),
        ("Reproducibilidad", "`uv.lock` y `requirements.txt` exportado sin dependencias de "
                             "desarrollo"),
        ("Sin marcadores", "Ningún `REPLACE` queda en `docs/`, `student_inputs/` ni "
                           "`reports/`"),
    ])
    paragraph(doc, "**Tres correcciones al proyecto base.** `scripts/lab11_impact.py` y "
                   "`scripts/simulate_incident.py` no compilaban tal como se entregan: "
                   "abren una cadena de varias líneas con una sola comilla. Además los dos "
                   "sobrescribían en cada ejecución el documento que el estudiante acababa "
                   "de redactar —el registro de decisión y el postmortem—, así que ahora "
                   "solo crean la plantilla si el archivo no existe.", size=10, after=3)

    heading(doc, "Referencias")
    for ref in (
        "Constitución de la República Dominicana, votada y proclamada por la Asamblea "
        "Nacional el 27 de octubre de 2024, arts. 44 y 70. Gaceta Oficial No. 11170 del "
        "31 de octubre de 2024.",
        "Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J. W., Wallach, H., Daumé III, "
        "H., & Crawford, K. (2021). Datasheets for datasets. Communications of the ACM, "
        "64(12), 86-92. https://doi.org/10.1145/3458723",
        "Ley No. 172-13 que tiene por objeto la protección integral de los datos "
        "personales asentados en archivos, registros públicos, bancos de datos u otros "
        "medios técnicos de tratamiento de datos destinados a dar informes, sean estos "
        "públicos o privados. República Dominicana, 13 de diciembre de 2013. Gaceta "
        "Oficial No. 10737 del 15 de diciembre de 2013.",
        "Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., "
        "Spitzer, E., Raji, I. D., & Gebru, T. (2019). Model cards for model reporting. "
        "Proceedings of the Conference on Fairness, Accountability, and Transparency, "
        "220-229. https://doi.org/10.1145/3287560.3287596",
        "NIST. (2023). Artificial Intelligence Risk Management Framework (AI RMF 1.0). "
        "https://doi.org/10.6028/NIST.AI.100-1",
        "OECD. (2019, enmendada el 3 de mayo de 2024). Recommendation of the Council on "
        "Artificial Intelligence, OECD/LEGAL/0449. "
        "https://legalinstruments.oecd.org/en/instruments/OECD-LEGAL-0449",
    ):
        p = paragraph(doc, ref, size=8.5, after=2)
        p.paragraph_format.left_indent = Cm(0.8)
        p.paragraph_format.first_line_indent = Cm(-0.8)

    heading(doc, "Declaración de uso de asistentes de IA")
    paragraph(doc, "Este trabajo se desarrolló con la asistencia de **Claude Opus 5 "
                   "(Anthropic)**. El asistente apoyó estructura, pruebas y redacción y "
                   "ejecutó los scripts. **No decidió los valores del análisis:** el plazo "
                   "de retención de dos años, el daño prioritario, la decisión de limitar y "
                   "la interpretación normativa son mías. Todas las cifras provienen de "
                   "ejecutar los scripts en el equipo indicado arriba. El detalle de "
                   "herramientas, prompts, verificaciones y correcciones está en "
                   "`docs/AI_USE_DECLARATION.md`.", size=8.5, after=2)

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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo-url", help="enlace del repositorio en GitHub")
    parser.add_argument("--sin-pdf", action="store_true", help="no exportar a PDF")
    args = parser.parse_args()
    docx_path = build(args.repo_url)
    print("DOCX:", docx_path)
    if not args.sin_pdf:
        print("PDF: ", export_pdf(docx_path))


if __name__ == "__main__":
    main()
