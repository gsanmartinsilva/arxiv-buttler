import arxiv
import pandas as pd
from datetime import datetime as dt
import pickle
from utils import Config


def formatPaper(d, cat = ''):
    D = {}
    id_version = d['id'].split('abs/')[-1].split('v')
    D['id'] = id_version[0]
    D['version'] = 0 if len(id_version) == 0 else int(id_version[1])
    D['cat'] = cat.split('.')[0]
    D['subcat'] = cat.split('.')[1]
    D['title'] = repr(d['title'])
    D['abstract'] = repr(d['summary'])
    D['updated'] = dt.strptime(d['updated'], "%Y-%m-%dT%H:%M:%SZ")
    D['author'] = d['author']
    D['authors'] = str(d['authors'])
    D['arxiv_url'] = d['arxiv_url']
    D['pdf_url'] = d['pdf_url']
    return D

cfg = Config()



# EXTRACT
try:
    db = pickle.load(open(cfg.dbPath, 'rb'))
    print(f'Database loaded from {cfg.dbPath}')
    print(f"Database contains {len(db['df_papers'])} papers")
except Exception as e:
    print(e)
    print('Starting from an empty database')
    db = {}
    
totalPapers = {}
for cat in cfg.categories:
    print(f"Processing {cat}...")
    r = arxiv.query(query=f"cat:{cat}",
                    id_list=[],
                    max_results=3,
                    start = 0,
                    sort_by="lastUpdatedDate",
                    sort_order="descending",
                    prune=True,
                    iterative=False,
                    max_chunk_results=100)
    totalPapers[cat] = r
    print(f"{len(r)} papers retrieved in category {cat}\n")
    
    
# TRANSFORM
D = []
for cat, papersList in totalPapers.items():
    for paper in papersList:
        D.append(formatPaper(paper, cat=cat))
    
df = pd.DataFrame(D)
print(f"Total papers retrieved: {len(df)}")


# LOAD
# save into pickle
if 'df_papers' not in db.keys():
    db['df_papers'] = df
    print(f"Papers uploaded to db: {len(db['df_papers'])}")
else:
    df_old = db['df_papers']
    df_j = pd.concat([df_old, df_old, df])
    df_new = df_j.drop_duplicates(subset=['id', 'version'], keep=False)
    db['df_papers'] = pd.concat([df_old, df_new])
    print(f"Papers uploaded to db: {len(df_new)}")

with open(cfg.dbPath, 'wb') as handle:
    pickle.dump(db, handle, protocol=4)