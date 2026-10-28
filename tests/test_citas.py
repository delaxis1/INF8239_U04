"""Las cinco citas legales que estaban mal no pueden volver.

La verificación contra fuente primaria de `docs/MARCO_NORMATIVO.md` §4 corrigió cinco
errores. Una corrección que vive solo en la prosa reaparece en cuanto alguien reescribe el
párrafo o regenera el informe desde una copia antigua. Estas pruebas la convierten en una
propiedad del repositorio: si una de las cinco vuelve, la suite falla.

Se comprueban los tres sitios donde se citan las normas: el documento normativo y los dos
generadores de informe, que son los que acaban en el PDF que se entrega.

La §4 del documento normativo queda fuera del control a propósito: ahí es donde se cita el
error para explicarlo, y prohibir la palabra también en el sitio que la corrige sería
impedir documentar la corrección.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
MARCO = RAIZ / "docs" / "MARCO_NORMATIVO.md"
GENERADORES = (RAIZ / "herramientas" / "informe_contenido.py",
               RAIZ / "herramientas" / "generar_informe_e08.py")
FUENTES = (MARCO, *GENERADORES)
TITULO_SECCION_4 = "## 4. Verificación de las citas contra fuente primaria"

# Cada entrada es (fragmento prohibido, por qué está mal).
ERRORES_CORREGIDOS = [
    ("26 de enero de 2010",
     "la Constitución de 2010 quedó derogada por la de 2015 y esta por la de 2024"),
    ("Ley Orgánica sobre Protección de Datos",
     "la Ley 172-13 no se declara orgánica y ese no es su título oficial"),
    ("10.1787/cc2e1d3e-en",
     "ese DOI no resuelve; la Recomendación de la OCDE es OECD/LEGAL/0449"),
    ("proporcionalidad de la Ley 172-13",
     "la palabra «proporcional» no aparece en la Ley 172-13"),
    ("hacer suprimir",
     "el hábeas data del art. 70 concede confidencialidad, no supresión"),
]


def plano(ruta: Path) -> str:
    """El texto citable del archivo, sin el cuerpo de la §4 y sin las costuras del código.

    De `MARCO_NORMATIVO.md` se quita solo el cuerpo de la §4 y se conservan las referencias
    que vienen después, porque es justo ahí donde viven las citas corregidas.

    En los generadores una cita se parte en varios literales de Python, así que `"` ... `"`
    adyacentes se eliminan antes de buscar: lo que importa es la frase que se imprime en el
    informe, no cómo quedó cortada en el fuente.
    """
    texto = ruta.read_text(encoding="utf-8")
    if ruta == MARCO:
        antes, _, resto = texto.partition(TITULO_SECCION_4)
        texto = antes + resto.partition("## Referencias")[2]
    return " ".join(re.sub(r'"\s*"', "", texto).split())


@pytest.mark.parametrize("ruta", FUENTES, ids=lambda p: p.name)
@pytest.mark.parametrize("fragmento,motivo", ERRORES_CORREGIDOS,
                         ids=[f[0][:22] for f in ERRORES_CORREGIDOS])
def test_el_error_no_vuelve(ruta: Path, fragmento: str, motivo: str) -> None:
    assert fragmento not in plano(ruta), f"{ruta.name}: {motivo}"


@pytest.mark.parametrize("ruta", FUENTES, ids=lambda p: p.name)
def test_la_constitucion_citada_es_la_vigente(ruta: Path) -> None:
    assert "27 de octubre de 2024" in plano(ruta)


@pytest.mark.parametrize("ruta", FUENTES, ids=lambda p: p.name)
def test_la_ocde_se_cita_por_su_instrumento(ruta: Path) -> None:
    assert "OECD/LEGAL/0449" in plano(ruta)


@pytest.mark.parametrize("ruta", FUENTES, ids=lambda p: p.name)
def test_la_ley_172_13_lleva_su_titulo_oficial(ruta: Path) -> None:
    """El del encabezado de la Gaceta Oficial 10737, no el que se usa coloquialmente."""
    assert ("que tiene por objeto la protección integral de los datos personales "
            "asentados en archivos") in plano(ruta)


@pytest.mark.parametrize("ruta", FUENTES, ids=lambda p: p.name)
def test_no_queda_una_verificacion_prometida(ruta: Path) -> None:
    """Ya no se vale la advertencia cómoda: la verificación está hecha."""
    assert "pendiente de verificación" not in plano(ruta)
    assert "sujeta a verificación" not in plano(ruta)


def test_la_seccion_de_verificacion_sigue_en_su_sitio() -> None:
    """Es la evidencia de que las citas se comprobaron, con sus dos gacetas."""
    contenido = MARCO.read_text(encoding="utf-8")
    assert TITULO_SECCION_4 in contenido
    assert "Gaceta Oficial No. 11170" in contenido
    assert "Gaceta Oficial No. 10737" in contenido


def test_la_seccion_de_verificacion_cita_los_cinco_errores() -> None:
    """Los cinco fragmentos prohibidos tienen que aparecer ahí, explicados."""
    cuerpo = MARCO.read_text(encoding="utf-8").partition(TITULO_SECCION_4)[2]
    seccion = " ".join(cuerpo.partition("## Referencias")[0].split())
    faltan = [f for f, _ in ERRORES_CORREGIDOS if f not in seccion]
    assert not faltan, f"la §4 no documenta: {faltan}"
