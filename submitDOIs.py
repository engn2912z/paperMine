import requests
import pickle
# import pandas as pd
url='http://rashidzia.pythonanywhere.com/'


def submitDOIS(email,doiList):
    submission={'dois':doiList,
        'email':email}
    submissionPickle=pickle.dumps(submission,protocol=3)
    files={'file':('submission.pickle',submissionPickle, 'application/octet-stream')}
    submissionResponse=requests.post(url+'post_doi',files=files)
    return submissionResponse.text

def requestDOIS(id=0):
    params={}
    if id > 0:
        params['id']=id
    response=requests.get(url+'get_doi',stream=True,params=params)
    columnNames=response.headers['columns']
    dataset=pickle.loads(response.content)
    with open('dataset.pickle','wb') as f2: f2.write(pickle.dumps(dataset,protocol=3))
    return dataset, columnNames
    # dois=[data[0] for data in dataset]
    # emails=[data[1] for data in dataset]
    # return dois,emails

# submitDOIS('rashid_zia@brown.edu',['aa','bb','ccc','adfsdsfa'])
# dataset,columns=requestDOIS(  )
# pd.DataFrame(dataset,columns=columns.split(','))
