import pandas as pd
from pyECLAT import ECLAT
from mlxtend.frequent_patterns import association_rules

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

def cari_freq_itemset(data, basket, minTrx, minValue):
    if(minTrx==True):
        minTransaction = minValue
        totalTransactions = len(basket.index)
        minSupport = minTransaction/totalTransactions
    else:
        minSupport = minValue
    # print('Nilai support minimum: ', round(minSupport*100, 4), '%')
    
    eclat_indexes, eclat_supports = data.fit(
        min_support=minSupport,
        min_combination=1,
        max_combination=2,
        separator=' ; ',
        verbose=True
    )
    
    return (eclat_indexes, eclat_supports)

def reshape_freq_itemset(eclat_support):
    frequent_itemsets = pd.DataFrame.from_dict(eclat_support, 
                                 orient='index',
                                 columns=["support"])

    frequent_itemsets['itemsets'] = list(frequent_itemsets.index)
    frequent_itemsets.index = range(len(frequent_itemsets.index))
        
    return frequent_itemsets

def cari_assoc_rules(frequent_itemsets, minconf):
    for i in frequent_itemsets.index:
        frequent_itemsets['itemsets'][i] = frozenset(frequent_itemsets['itemsets'][i].split(" ; "))
    
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
    rules.sort_values('confidence', ascending = False, inplace = True)
    rules = rules.loc[rules['confidence'] >= minconf]
    return rules