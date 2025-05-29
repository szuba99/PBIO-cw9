import argparse
from Bio import Entrez, SeqIO
import pandas as pd, matplotlib.pyplot as plt
p = argparse.ArgumentParser()
p.add_argument('--email', required=True)
p.add_argument('--api_key', required=True)
p.add_argument('--taxid', required=True)
p.add_argument('--min_len', type=int, default=0)
p.add_argument('--max_len', type=int, default=10 ** 9)
args = p.parse_args()
Entrez.email, Entrez.api_key = args.email, args.api_key
handle = Entrez.esearch(db="nucleotide", term=f"txid{args.taxid}[Organism]", retmax=100000)
ids = Entrez.read(handle)["IdList"]
records = []
fetch_handle = Entrez.efetch(db="nucleotide", id=ids, rettype="gb", retmode="text")
for r in SeqIO.parse(fetch_handle, "gb"):
    l = len(r.seq)
    if args.min_len <= l <= args.max_len:
        records.append((r.id, l, r.description))
df = pd.DataFrame(records, columns=['accession', 'length', 'description'])
df.to_csv('report.csv', index=False)
df = df.sort_values('length', ascending=False)
plt.plot(df['accession'], df['length'])
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig('plot.png')