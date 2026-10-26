"""El inventario de datos y el RACI tienen que seguir siendo ciertos.

Un documento de gobernanza que nadie comprueba se desactualiza en el primer cambio de
esquema. Estas pruebas convierten `docs/INVENTARIO_DATOS.md` y `student_inputs/raci.csv`
en artefactos verificables.
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd
import pytest

from inf8239_u04.data import load_data

RAIZ = Path(__file__).resolve().parents[1]
INVENTARIO = RAIZ / "docs" / "INVENTARIO_DATOS.md"
RACI = RAIZ / "student_inputs" / "raci.csv"


def columnas_inventariadas() -> set[str]:
    """Las columnas citadas como `nombre` en la tabla del inventario."""
    texto = INVENTARIO.read_text(encoding="utf-8")
    tabla = texto.split("## Inventario por columna", 1)[1].split("## Minimización", 1)[0]
    return {m for linea in tabla.splitlines() if linea.startswith("| `")
            for m in re.findall(r"^\| `([^`]+)`", linea)}


def test_todas_las_columnas_estan_inventariadas():
    faltan = set(load_data().columns) - columnas_inventariadas()
    assert not faltan, f"Columnas sin documentar en el inventario: {sorted(faltan)}"


def test_el_inventario_no_documenta_columnas_inexistentes():
    sobran = columnas_inventariadas() - set(load_data().columns)
    assert not sobran, f"El inventario documenta columnas que ya no existen: {sorted(sobran)}"


def test_el_grupo_protegido_no_entra_al_modelo():
    from inf8239_u04.data import features
    assert "protected_group" not in features(load_data()).columns


def test_la_retencion_esta_declarada_con_plazo():
    texto = INVENTARIO.read_text(encoding="utf-8")
    assert "## Retención" in texto
    assert re.search(r"\*\*\d+ años?\*\*", texto), "Falta un plazo de retención explícito"


def test_cada_actividad_tiene_exactamente_un_aprobador():
    raci = pd.read_csv(RACI)
    multiples = raci[raci.A.str.contains(" and ", na=False)]
    assert multiples.empty, (
        f"Actividades con más de un Accountable: {list(multiples.activity)}")


def test_ningun_rol_se_aprueba_o_se_consulta_a_si_mismo():
    raci = pd.read_csv(RACI)
    conflicto = raci[(raci.R.str.strip() == raci.A.str.strip())
                     | (raci.R.str.strip() == raci.C.str.strip())]
    assert conflicto.empty, f"RACI inconsistente en: {list(conflicto.activity)}"


@pytest.mark.parametrize("actividad", [
    "Respuesta a incidentes y rollback",
    "Atencion de apelaciones",
    "Borrado por fin de retencion",
    "Traspaso entre responsables",
])
def test_las_actividades_criticas_tienen_responsable(actividad):
    """Las promesas del expediente necesitan a alguien encargado de cumplirlas."""
    raci = pd.read_csv(RACI)
    assert actividad in set(raci.activity), f"El RACI no cubre: {actividad}"
