import pandas as pd

from submitDOIs import requestDOIS

dataset,columns=requestDOIS(  )
pd.DataFrame(dataset,columns=columns.split(','))
