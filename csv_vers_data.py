#!/usr/bin/env python3
"""NoobToRoot / OldToRoot : convertit les banques de questions (Excel ou Google Sheets) en fichiers .js.

Utilisation :
  - Depuis Excel :  python3 csv_vers_data.py NoobToRoot.xlsx   (nécessite openpyxl)
      onglet « questions »  → data.js      (NoobToRoot)
      onglet « OldToRoot »  → data_old.js  (OldToRoot)
  - Depuis Google Sheets : Fichier > Télécharger > .csv, puis
      python3 csv_vers_data.py questions.csv       → data.js
      python3 csv_vers_data.py questions_old.csv   → data_old.js   (tout fichier dont le nom contient « old »)
  Les fichiers .js sont regénérés à côté des pages : il suffit de recharger.

Colonnes attendues (ligne d'en-tête) :
  id, langage, difficulte, question, reponse1 … reponse6, leurre1, leurre2, indice, explication
  - langage : shell, python, html (NoobToRoot) ; basic, msdos, cobol, pascal, fortran (OldToRoot)
  - difficulte : 1 (Noob), 2 (Geek) ou 3 (Elite)
  - reponse1 est la réponse affichée comme correction ; les suivantes sont des variantes acceptées
  - une réponse qui commence par re: est une expression régulière
  - dans l'explication, le code se met entre `backticks`
"""
import csv
import json
import sys
from pathlib import Path

BANKS = {
    "noob": {"langs": {"shell", "python", "html"}, "out": "data.js", "var": "NTR_QUESTIONS", "name": "NoobToRoot"},
    "old": {"langs": {"basic", "msdos", "cobol", "pascal", "fortran"}, "out": "data_old.js", "var": "OTR_QUESTIONS", "name": "OldToRoot"},
}


def sheet_rows(ws):
    it = ws.iter_rows(values_only=True)
    head = [str(h or "") for h in next(it)]
    for row in it:
        yield {h: ("" if v is None else str(v)) for h, v in zip(head, row)}


def csv_rows(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        yield from csv.DictReader(f)


def convert(rows_iter, bank: dict, out_path: Path, source: str) -> bool:
    rows, errors = [], []
    for n, r in enumerate(rows_iter, start=2):
        r = {k.strip().lower(): (v or "").strip() for k, v in r.items() if k}
        if not r.get("question"):
            continue
        answers = [r[k] for k in sorted(r) if k.startswith("reponse") and r[k]]
        decoys = [r.get("leurre1", ""), r.get("leurre2", "")]
        lang = r.get("langage", "").lower()
        try:
            diff = int(float(r.get("difficulte", "1")))
        except ValueError:
            diff = 0
        if lang not in bank["langs"]:
            errors.append(f"ligne {n} : langage inconnu « {lang} » (attendu : {', '.join(sorted(bank['langs']))})")
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
        print(f"{source} : corrige ces lignes :\n  " + "\n  ".join(errors))
        return False
    body = ",\n".join(json.dumps(q, ensure_ascii=False) for q in rows)
    out_path.write_text(
        f"// {bank['name']} : banque de questions (générée par csv_vers_data.py)\n"
        f"window.{bank['var']} = [\n{body}\n];\n", encoding="utf-8")
    counts = {l: sum(q["lang"] == l for q in rows) for l in sorted(bank["langs"])}
    print(f"{source} : {len(rows)} questions écrites dans {out_path.name} {counts}")
    return True


if __name__ == "__main__":
    src = Path(sys.argv[1] if len(sys.argv) > 1 else "NoobToRoot.xlsx")
    here = Path(__file__).parent
    ok = True
    if src.suffix.lower() in (".xlsx", ".xlsm"):
        import openpyxl
        wb = openpyxl.load_workbook(src, read_only=True, data_only=True)
        for ws in wb.worksheets:
            key = "old" if "old" in ws.title.lower() else "noob"
            if key == "noob" and ws is not wb.worksheets[0]:
                continue  # seuls le premier onglet et l'onglet OldToRoot sont convertis
            bank = BANKS[key]
            ok &= convert(sheet_rows(ws), bank, here / bank["out"], f"onglet « {ws.title} »")
    else:
        bank = BANKS["old" if "old" in src.name.lower() else "noob"]
        ok = convert(csv_rows(src), bank, here / bank["out"], src.name)
    sys.exit(0 if ok else 1)
