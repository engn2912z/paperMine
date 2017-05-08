import requests
import re
# import feedparser
import os
import multiprocessing
import pdfminerToText
import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt

try:
    f=open('.email')
    email=f.read().split('\n')[0]
    f.close()
except:
    email=input('email address:')
    with open('.email','w') as f1:
        f1.write(email)

try:
    f=open('.foldername')
    foldername=f.read().split('\n')[0]
    f.close()
except:
    foldername=input('PDF folder path:')
    with open('.foldername','w') as f1:
        f1.write(foldername)

def parseDOI(DOI: str):
    URL = 'https://api.crossref.org/works/'+DOI
    response=requests.get(URL).json()
    if response['status']=="ok":
        return response['message']

# def parseArxiv(arXiv: str):
#     URL='https://export.arxiv.org/api/query'
#     response=requests.get(URL,params={'id_list':arXiv})
#     feed=feedparser.parse(response.content)
#     return feed['entries'][0]
#
# def parsePubmed(pubMed: str):
#     URL='https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/'
#     response=requests.get(URL,params={'ids':pubMed})
#     feed=feedparser.parse(response.content)
#     return feed['feed']

#
# def searchArxiv(searchQuery: str, maxResults=10,sortBy='submittedDate',sortOrder='descending'):
#     URL='https://export.arxiv.org/api/query'
#     response=requests.get(URL,params={'search_query':searchQuery,'max_results':maxResults,'sortBy':sortBy,'sortOrder':sortOrder})
#     feed=feedparser.parse(response.content)
#     return feed['entries']
#

# foldername='/Users/rashidzia/Google Drive/Izzy UTRA /PSC Papers Sample'
# downloads=os.listdir(foldername)
# pdfs=[foldername+filename for filename in downloads if filename.endswith('.pdf')]
# len(pdfs)

# email = 'rashid_zia@brown.edu'
# foldername = '/Users/rashidzia/Google Drive/Izzy UTRA /PSC Papers Sample'

print('searching recursively through ',foldername,' for all *.pdf files')
pdfs=[os.path.join(dp, f) for dp, dn, fn in os.walk(foldername) for f in fn if f.endswith('.pdf')]
print('found ', len(pdfs),' files')


def getFirstPage(pdfFilename):
    return pdfminerToText.convert(pdfFilename,[0])

timeout=2
dois=[]
# texts=[]
for pdf in pdfs: # Example showing first 5
    pool=multiprocessing.Pool(1)
    res = pool.apply_async(getFirstPage, [pdf])
    try:
        text=res.get(timeout)
    except multiprocessing.TimeoutError:
        text=''
    except:
        text=''
    pool.terminate()
#     texts.append(text)
    doi=re.search('10\.\d\S+',text)
    print(pdf, doi)
    if doi:
        dois.append(doi.group())
    else:
        dois.append(None)

info=[]
for nn in range(len(dois)):
    doi=dois[nn]
    if doi is not None:
        if doi.endswith('.'): doi = doi[:-1]
        # print(doi)
        try:
            inf=parseDOI(doi)
            if inf is not None:
#                 inf['text']=texts[nn]
                info.append(inf)
        except:
                print('hmm')

from submitDOIs import submitDOIS,requestDOIS
finalDOIs=[inf['DOI'] for inf in info]

submitDOIS(email,finalDOIs)
import pickle
with open(email.split('@')[0]+'_doiInfo.pickle','wb') as f1:
     pickle.dump(info,f1)


# email = 'rashid_zia@brown.edu'
# foldername = '/Users/rashidzia/Google Drive/Izzy UTRA /PSC Papers Sample'
# scrapeDoisFromPdf(foldername,email)
