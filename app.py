"""Tablero del DSS gobernado.

Muestra lo que exige LAB13: propósito, límites, métricas, grupos, puertas, recomendación y
acción humana. Añade a la versión del proyecto base la distinción entre lo que deciden las
compuertas automáticas y lo que decide la gobernanza, que aquí no coinciden: las compuertas
dan GO y la decisión documentada es LIMITAR.
"""

from pathlib import Path

import pandas as pd
import streamlit as st

from inf8239_u04.data import load_data
from inf8239_u04.governance import load_config
from inf8239_u04.pipeline import run

RAIZ = Path(__file__).resolve().parent
COMPARACION = RAIZ / "reports" / "lab12" / "comparison.csv"

st.set_page_config(page_title="Governed Green DSS", layout="wide")
st.title("DSS territorial sintético · Gobernanza y Green AI")
st.warning("Demostración educativa con datos sintéticos. No autoriza decisiones "
           "automáticas ni representa estadísticas reales.")

cfg = load_config()
result = run(load_data(), cfg["gates"])
gates = cfg["gates"]

st.subheader("Propósito y autoridad")
st.write(cfg["purpose"])
st.write("**Usos prohibidos:**", ", ".join(cfg["prohibited_uses"]))
st.caption("El sistema ordena una cola para revisión humana. No interviene, no decide "
           "elegibilidad y no declara emergencias.")

st.subheader("Decisión")
izquierda, derecha = st.columns([1, 2])
izquierda.metric("Compuertas automáticas", result["decision"]["status"])
izquierda.metric("Decisión gobernada", "LIMITAR")
derecha.error(
    "**Las compuertas dicen GO y la decisión documentada es LIMITAR.** La diferencia es "
    "deliberada: pasar una compuerta no demuestra que el sistema sea necesario.\n\n"
    "Usar el modelo **solo si la capacidad de revisión es el límite real de la "
    "institución**, declarado por escrito por el responsable institucional. Si no lo es, "
    "la decisión correcta es no utilizarlo y quedarse con la regla manual."
)

st.subheader("Métricas globales")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Exactitud", f"{result['metrics']['accuracy']:.3f}")
c2.metric("Recall", f"{result['metrics']['recall']:.3f}",
          delta=f"mínimo {gates['min_recall']:.2f}", delta_color="off")
c3.metric("Brecha de recall", f"{result['gaps']['recall_gap']:.3f}",
          delta=f"techo {gates['max_recall_gap']:.2f}", delta_color="off")
c4.metric("Brecha de FPR", f"{result['gaps']['fpr_gap']:.3f}",
          delta=f"techo {gates['max_fpr_gap']:.2f}", delta_color="off")
st.caption(f"El margen de la brecha de recall contra su techo es "
           f"{gates['max_recall_gap'] - result['gaps']['recall_gap']:.3f}, medido sobre una "
           f"sola partición de {len(result['test'])} casos y sin intervalos de confianza.")

st.subheader("Métricas por grupo protegido")
st.dataframe(result["by_group"], use_container_width=True)
st.caption("El grupo protegido se usa solo para auditar y nunca entra al modelo. De cada "
           "100 casos de G1 que requerían revisión, el sistema deja 35 sin marcar; en G2 "
           "deja 21. Ese es el daño priorizado.")

st.subheader("Puertas de calidad")
st.json(result["decision"])

st.subheader("Límites: lo que este tablero no demuestra")
st.markdown(
    "- **Siete de las ocho celdas interseccionales no tienen soporte.** Dos tienen 2 casos "
    "negativos, así que un FPR de 1.000 son dos casos de dos. No se interpretan.\n"
    "- **Las compuertas aprueban marcar a todo el mundo.** Fijan recall mínimo y brechas "
    "máximas, pero no acotan FPR ni precisión.\n"
    "- **La alternativa no predictiva atiende mejor al grupo priorizado.** La regla manual "
    "alcanza recall 0.898 en G1 frente a 0.653 del modelo.\n"
    "- **Una brecha no prueba discriminación causal**; indica dónde investigar.\n"
    "- **Los datos son sintéticos.** Nada de esto estima el comportamiento real."
)

if COMPARACION.exists():
    st.subheader("Alternativas y Green AI")
    st.dataframe(pd.read_csv(COMPARACION), use_container_width=True, hide_index=True)
    st.caption("reports/lab12/comparison.csv · la regla manual no usa modelo ni el grupo "
               "protegido, y es la base segura del runbook.")

st.subheader("Acción humana")
st.info("Revisar cada caso marcado antes de actuar, registrar la decisión del operador "
        "junto a la del sistema, documentar la revisión y activar apelación o reversión "
        "cuando corresponda. La reversión no vuelve a una versión anterior del modelo: "
        "vuelve a la regla manual.")
st.caption("Expediente completo: docs/MODEL_CARD.md, docs/DATASET_CARD.md, "
           "docs/INVENTARIO_DATOS.md, docs/RUNBOOK.md, docs/TRASPASO_ROLES.md y "
           "reports/lab13/INCIDENT_POSTMORTEM.md")
