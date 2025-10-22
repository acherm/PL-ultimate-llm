import os, json, argparse, re, csv
from schema import Proposal
from util import read_pl_list, code_hash, now_iso

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
CATALOG = os.path.join(DATA_DIR, "catalog.csv")
PL_LIST = os.path.join(DATA_DIR, "pl_list.txt")


def line_count(code: str) -> int:
    return len(code.splitlines())


def validate_proposal(p: dict, max_code_lines=200) -> Proposal:
    prop = Proposal.model_validate(p)
    assert prop.language.name.strip(), "Empty language name"
    assert prop.program.code.strip(), "Empty code"
    assert line_count(prop.program.code) <= max_code_lines, "Code too long"
    assert re.match(r"^\.[a-zA-Z0-9]+$", prop.program.filename_ext), "Bad filename_ext"
    # normalize extension
    ext = prop.program.filename_ext.strip()
    if not ext.startswith("."):
        ext = "." + ext
        prop.program.filename_ext = ext
    assert re.match(r"^\.[a-zA-Z0-9]+$", prop.program.filename_ext), "Bad filename_ext"
    return prop


def check_membership(name: str) -> bool:
    existing = {n.lower() for n in read_pl_list(PL_LIST)}
    return name.lower() in existing


def refresh_catalog():
    if not os.path.exists(CATALOG):
        with open(CATALOG, "w", encoding="utf-8", newline="") as f:
            f.write("timestamp,language,program_title,origin_url,code_sha256,folder\n")


def append_catalog_row(
    language: str, program_title: str, origin_url: str, sha: str, folder: str
):
    with open(CATALOG, "a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow([now_iso(), language, program_title, origin_url, sha, folder])


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh-catalog", action="store_true")
    args = ap.parse_args()
    if args.refresh_catalog:
        refresh_catalog()
        print("[validate] refreshed catalog.csv")
