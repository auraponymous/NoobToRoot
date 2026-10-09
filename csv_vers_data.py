#!/usr/bin/env python3
"""NoobToRoot : convertit la banque de questions (Excel ou Google Sheets) en data.js.

Utilisation :
  - Depuis Excel :         python3 csv_vers_data.py NoobToRoot.xlsx   (nécessite openpyxl)
  - Depuis Google Sheets : Fichier > Télécharger > .csv, puis python3 csv_vers_data.py questions.csv
  data.js est regénéré à côté d'index.html : il suffit de recharger la page.

Colonnes attendues (ligne d'en-tête) :
  id, langage, difficulte, question, reponse1 … reponse6, leurre1, leurre2, indice, explication
  - langage : shell, python ou html
  - difficulte : 1, 2 ou 3
  - reponse1 est la réponse affichée comme correction ; les suivantes sont des variantes acceptées
  - une réponse qui commence par re: est une expression régulière
  - dans l'explication, le code se met entre `backticks`
"""
import csv
import json
import sys
from pathlib import Path

LANGS = {"shell", "python", "html"}


def read_rows(path: Path):
    """Renvoie les lignes sous forme de dictionnaires, depuis un .csv ou un .xlsx (premier onglet)."""
    if path.suffix.lower() in (".xlsx", ".xlsm"):
        import openpyxl
        ws = openpyxl.load_workbook(path, read_only=True, data_only=True).worksheets[0]
        it = ws.iter_rows(values_only=True)
        head = [str(h or "") for h in next(it)]
        for row in it:
            yield {h: ("" if v is None else str(v)) for h, v in zip(head, row)}
    else:
        with path.open(encoding="utf-8-sig", newline="") as f:
            yield from csv.DictReader(f)


def convert(csv_path: Path, out_path: Path) -> None:
    rows, errors = [], []
    if True:
        for n, r in enumerate(read_rows(csv_path), start=2):
            r = {k.strip().lower(): (v or "").strip() for k, v in r.items() if k}
            if not r.get("question"):
                continue
            answers = [r[k] for k in sorted(r) if k.startswith("reponse") and r[k]]
            decoys = [r.get("leurre1", ""), r.get("leurre2", "")]
            lang = r.get("langage", "").lower()
            try:
                diff = int(r.get("difficulte", "1"))
            except ValueError:
                diff = 0
            if lang not in LANGS:
                errors.append(f"ligne {n} : langage inconnu « {lang} »")
            if diff not in (1, 2, 3):
                errors.append(f"ligne {n} : difficulté doit valoir 1, 2 ou 3")
            if not answers:
                errors.append(f"ligne {n} : aucune réponse")
            if not all(decoys):
                errors.append(f"ligne {n} : il faut deux leurres pour le mode Pick")
            rows.append({
                "id": r.get("id") or f"Q-{n}", "lang": lang, "d": diff, "q": r["question"],
                "a": answers, "x": decoys, "h": r.get("indice", ""), "e": r.get("explication", ""),
            })
    if errors:
        print("Corrige ces lignes dans le Sheet :\n  " + "\n  ".join(errors))
        sys.exit(1)
    body = ",\n".join(json.dumps(q, ensure_ascii=False) for q in rows)
    out_path.write_text(
        "// NoobToRoot : banque de questions (générée par csv_vers_data.py)\n"
        f"window.NTR_QUESTIONS = [\n{body}\n];\n", encoding="utf-8")
    counts = {l: sum(q["lang"] == l for q in rows) for l in sorted(LANGS)}
    print(f"{len(rows)} questions écrites dans {out_path.name} : {counts}")


if __name__ == "__main__":
    src = Path(sys.argv[1] if len(sys.argv) > 1 else "NoobToRoot.xlsx")
    convert(src, Path(__file__).with_name("data.js"))
