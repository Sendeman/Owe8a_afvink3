import itertools
from Bio import Entrez, Medline

Entrez.email = "SRP.Geurts@student.han.nl"
terms = ["Endocrine Disruption", "organelle", "ossification", "canine", "central artery", "central nervous system"]
terms_to_articles = {}
for combination in itertools.combinations(terms, 2):
    query = str(combination)[2:-2].replace("\', \'", " AND ")
    retmax = 0

    handle = Entrez.egquery(term=query)
    record = Entrez.read(handle)

    for row in record["eGQueryResult"]:
        if "pubmed" == row["DbName"]:
            retmax = int(row["Count"])
            terms_to_articles[combination] = retmax

highest_count = 0
for key, value in terms_to_articles.items():
    print(key, " : ", value)
    if value > highest_count:
        highest_count = value


for key, value in terms_to_articles.items():
    if value == highest_count:
        query = str(key)[2:-2].replace("\', \'", " AND ")
        handle = Entrez.esearch(db="pubmed", term=query, retmax=value)
        record = Entrez.read(handle)

        PMIDs = record["IdList"]
        for i in range(0, 10):

            PMID = PMIDs[i]
            handle = Entrez.efetch(db="Pubmed", id=PMID, rettype="medline", retmode="text")
            record = Medline.read(handle)
            print(key, " : ", record["AU"], "\n", record["AB"])