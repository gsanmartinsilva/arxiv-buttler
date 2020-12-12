# Configuration class

class Config:
    def __init__(self):
        self.categories = ['stat.ML',
                           'cs.CV',
                           'cs.LG',
                           'cs.AI']
        self.dbPath = 'data/db.p'
        self.logPath = 'logs/log.txt'
        self.txtPath = 'data/txt/'
        
        
def paper_to_filename(paper: dict) -> str:
    # paper id
    ids = paper['arxiv_url'].split('/')[-1]
    return ids