import pandas as pd
from pyECLAT import ECLAT

def reshape_dataset(dataset, kolom):
    dataset.kolom = dataset[kolom].apply(str)
    transactions = dataset.groupby('PENJUALAN_ID')[kolom].apply(lambda x: x.tolist()).reset_index()
    del transactions['PENJUALAN_ID']
    
    s = transactions.unstack()
    transactions = pd.DataFrame(s.values.tolist())
    
    return(transactions)

def eclat_basket(data_trx):
    eclat = ECLAT(data=data_trx, verbose=True)
    basket = eclat.df_bin
    return(eclat, basket)