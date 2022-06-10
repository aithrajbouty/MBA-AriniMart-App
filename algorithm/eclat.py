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

def cari_freq_itemset(data, basket, minTrx, minValue, maxComb):
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
        max_combination=maxComb,
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
    frequent_itemsets.sort_values('support', ascending = False, inplace = True)

    # reset index
    frequent_itemsets = frequent_itemsets.reset_index(drop=True)

    # ubah bentuk frequent itemset jadi forzenset
    for i in frequent_itemsets.index:
        frequent_itemsets['itemsets'][i] = frozenset(frequent_itemsets['itemsets'][i].split(" ; "))
        
    return frequent_itemsets

def cari_assoc_rules(freq_itemset, minconf):    
    # cari association rules
    rules = association_rules(freq_itemset, metric="lift", min_threshold=1)
    rules.sort_values('confidence', ascending = False, inplace = True)
    rules = rules.loc[rules['confidence'] >= minconf]

    # ubah dari frozenset ke string
    rules["antecedents"] = rules["antecedents"].apply(lambda x: ', '.join(list(x))).astype("unicode")
    rules["consequents"] = rules["consequents"].apply(lambda x: ', '.join(list(x))).astype("unicode")

    # reset index
    rules = rules.reset_index(drop=True)

    return rules

def buat_pola_belanja(rules):
    pola_belanja_konsumen = pd.DataFrame(columns = ['aturan', 'confidence'])
    antecedent = rules['antecedents']
    consequent = rules['consequents']
    confidence = round((rules['confidence'] * 100), 2)

    for i in range(len(rules)):
        ant = antecedent[i].replace(", ", " dan ")
        cons = consequent[i]
        conf = (f"{confidence[i]}{'%'}")
        pola_belanja = 'Jika membeli ' + ant + ' maka membeli ' + cons
        pola_belanja_konsumen = pola_belanja_konsumen.append({'aturan': pola_belanja, 'confidence': conf}, ignore_index=True)

    return(pola_belanja_konsumen)