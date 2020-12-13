import pickle
import os
import sys
from utils import Config, paper_to_filename
import numpy as np
import arxiv
import os

cfg = Config()

# load pickle and get list of all ids
try:
    db = pickle.load(open(cfg.dbPath, 'rb'))
    df_papers = db['df_papers']
    ids = (df_papers['id'] + 'v' + df_papers['version'].astype('str')).tolist()
except Exception as e:
    print(e)
    sys.exit(1)
    

    
# get list of existing pdf's
existingTXT = []
for i in os.listdir(cfg.txtPath):
    existingTXT.append(i.split('.txt')[0])
    
print(f"Total # of existing txts:{len(existingTXT)}")


# get ids of papers that have not been downloaded
download_list = np.setdiff1d(ids, existingTXT)
print(f"Total # of papers to download: {len(download_list)}")


# download pdf's and name them correctly
r = arxiv.query(id_list = download_list)
for n, paper in enumerate(r):
    print(f"Downloading paper {n+1}/{len(r)}")
    filename = paper_to_filename(paper)
    arxiv.download(paper, dirpath=cfg.txtPath, slugify=paper_to_filename)
    # create text
    cmd = f"pdftotext {os.path.join(cfg.txtPath, filename+'.pdf')} {os.path.join(cfg.txtPath, filename+'.txt')}"
    try:
        os.system(cmd)
    except:
        print(f'Unable to convert {filename}. Creating empty file instead.')
        ps.system(f"touch {os.path.join(cfg.txtPath, filename+'.txt')}")
    # remove pdf
    os.remove(os.path.join(cfg.txtPath, filename+'.pdf'))
    