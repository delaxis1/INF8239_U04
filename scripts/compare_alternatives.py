"""Compara los dos modelos con dos lineas base y produce la tabla Green AI.

La rubrica de LAB12 pide "comparacion de dos modelos y baseline" mas "tiempo, tamano
del modelo y justificacion Green AI". Este script anade a los dos modelos del proyecto
base dos referencias que no aprenden de la etiqueta:

- regla_manual: la alternativa no predictiva declarada en lab11_impact.yml. Marca el
  caso si previous_incidents alcanza la mediana del conjunto de ENTRENAMIENTO. El
  umbral sale de la distribucion de entrenamiento, nunca de las etiquetas de prueba.
- marcar_todo: marca todos los casos. Recall 1.0 y FPR 1.0; sirve para recordar que un
  recall alto sin mirar el FPR no dice nada.

Uso:
    uv run python scripts/compare_alternatives.py
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score

from inf8239_u04.data import features, load_data, temporal_split
from inf8239_u04.fairness import audit, gap
from inf8239_u04.governance import load_config
from inf8239_u04.model import build_model, fit_measure

SALIDA = Path("reports/lab12")


def fpr(y_true, y_pred) -> float:
    negativos = y_true == 0
    return float((y_pred[negativos] == 1).mean()) if negativos.any() else 0.0


def medir(nombre, y_true, y_pred, grupos, segundos, kb, latencia_ms, gates):
    _, por_grupo, _ = audit(y_true, y_pred, grupos)
    brecha_recall = gap(por_grupo, "recall")
    brecha_fpr = gap(por_grupo, "fpr")
    recall = float(recall_score(y_true, y_pred, zero_division=0))
    return {
        "alternativa": nombre,
        "accuracy": round(float(accuracy_score(y_true, y_pred)), 4),
        "recall": round(recall, 4),
        "precision": round(float(precision_score(y_true, y_pred, zero_division=0)), 4),
        "fpr": round(fpr(y_true, y_pred), 4),
        "selection_rate": round(float(y_pred.mean()), 4),
        "brecha_recall": round(brecha_recall, 4),
        "brecha_fpr": round(brecha_fpr, 4),
        "entrenamiento_s": round(segundos, 4),
        "tamano_kb": round(kb, 2),
        "latencia_ms": round(latencia_ms, 4),
        "pasa_compuertas": bool(
            recall >= gates["min_recall"]
            and brecha_recall <= gates["max_recall_gap"]
            and brecha_fpr <= gates["max_fpr_gap"]
            and latencia_ms <= gates["max_latency_ms"]
            and kb <= gates["max_model_kb"]
        ),
    }


def main() -> None:
    gates = load_config()["gates"]
    df = load_data()
    train, test = temporal_split(df)
    y = test.target.to_numpy()
    grupos = test.protected_group
    filas = []

    umbral = int(train.previous_incidents.median())
    inicio = time.perf_counter()
    pred = (test.previous_incidents.to_numpy() >= umbral).astype(int)
    latencia = (time.perf_counter() - inicio) * 1000 / len(test)
    filas.append(medir(f"regla_manual (previous_incidents >= {umbral})", y, pred,
                       grupos, 0.0, 0.0, latencia, gates))

    inicio = time.perf_counter()
    pred = np.ones(len(test), dtype=int)
    latencia = (time.perf_counter() - inicio) * 1000 / len(test)
    filas.append(medir("marcar_todo", y, pred, grupos, 0.0, 0.0, latencia, gates))

    for kind in ("logistic", "tree"):
        modelo = build_model(kind)
        recursos = fit_measure(modelo, features(train), train.target,
                               f"models/{kind}.joblib")
        inicio = time.perf_counter()
        pred = modelo.predict(features(test))
        latencia = (time.perf_counter() - inicio) * 1000 / len(test)
        filas.append(medir(kind, y, pred, grupos, recursos["training_seconds"],
                           recursos["model_kb"], latencia, gates))

    tabla = pd.DataFrame(filas)
    SALIDA.mkdir(parents=True, exist_ok=True)
    tabla.to_csv(SALIDA / "comparison.csv", index=False)
    (SALIDA / "umbral_regla_manual.json").write_text(
        json.dumps({"umbral": umbral, "origen": "mediana de previous_incidents en el "
                    "conjunto de entrenamiento", "etiquetas_usadas": False}, indent=2),
        encoding="utf-8")
    print(tabla.to_string(index=False))


if __name__ == "__main__":
    main()
