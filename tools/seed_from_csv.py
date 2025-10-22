import sys, os, csv
from util import write_pl_list, read_pl_list, canonical_name

DATA = os.path.join(os.path.dirname(__file__),'..','data','pl_list.txt')

def main(csv_path: str):
    names = read_pl_list(DATA)
    with open(csv_path, newline='', encoding='utf-8') as f:
        r = csv.DictReader(f)
        for row in r:
            name = row.get('canonical_name') or row.get('name') or ''
            if name:
                names.append(canonical_name(name))
    write_pl_list(DATA, names)
    print(f"Seeded {len(names)} names into data/pl_list.txt")

if __name__ == '__main__':
    if len(sys.argv)<2:
        print('Usage: python3 tools/seed_from_csv.py /path/to/languages_master.csv'); sys.exit(1)
    main(sys.argv[1])
