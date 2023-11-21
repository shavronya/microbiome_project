from scholarly import scholarly, ProxyGenerator
pg = ProxyGenerator()
success = pg.SingleProxy(http = "57.128.12.85:80", https = "187.102.217.12:999")
from paperscraper.pubmed import get_and_dump_pubmed_papers
a = ['Microbiota', 'Microbiome']
b = ['Alteration', 'Dismicrobism', 'Change', 'Dysbiosis']
c = ['Lifestyle', 'Western']
query = [a, b, c]

get_and_dump_pubmed_papers(query, output_filepath = 'microbiota_pubmed_2.jsonl')

from paperscraper.scholar import get_and_dump_scholar_papers
topic = 'Disappearing microbiota hypothesis Bacteria loss'
get_and_dump_scholar_papers(topic, output_filepath = 'microbiota_3_scholar.jsonl')
import pandas as pd
df = pd.read_json('microbiota_pubmed_2.jsonl', lines=True)
df.to_csv('microbiota_pubmed_2.csv')
import pandas as pd
df = pd.read_json('microbiota_scholar.jsonl', lines=True)
df.to_csv('microbiota_3_scholar.csv')
