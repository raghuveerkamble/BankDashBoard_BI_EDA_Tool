import pandas as pd 
from dplython import (DplyFrame, X, diamonds, select, sift, sample_n,
                      sample_frac, head, arrange, mutate, group_by,
                      summarize, DelayFunction)
#from .data.MoonStoneData import MoonStoneData
csv_file = "data/Dec22a.csv"
csv_data = pd.read_csv(csv_file)
table = pd.DataFrame(csv_data)

MoonStoneData = DplyFrame(table)

diamondsSmall = (MoonStoneData >> 
                select(X.Portfolio, X.Vertical, X.Segment, X.Status, X.Amt, X.Product, X.DEC_22_CL_BKT, X.Nature_of_Business, X.Constitution) >>
                sift(X.DEC_22_CL_BKT != 'closed', X.Vertical == 'Retail', X.Nature_of_Business != '')
)
#print(diamondsSmall.head(5))
table1 = pd.pivot_table(data=diamondsSmall, values=['Amt'],
                       index=['Portfolio'], columns=['Status'], 
                       aggfunc=len, margins=True, 
                       dropna=True, fill_value=0)

#print(table1)
table1.columns = table1.columns.droplevel(0)
#table1.columns = table1.columns.droplevel(0)

#print(table1)
Query4 = pd.pivot_table(data=diamondsSmall,
                       index=['Portfolio'], columns=['Status'],
                       values=['Amt'], aggfunc=['count'], #{diamondsSmall['Status']:np.count_nonzero,'Amt':np.sum},
                       margins = True, margins_name='Total')
Query4.columns = Query4.columns.droplevel(0)
Query4.columns = Query4.columns.droplevel(0)

#print(Query4)
Q4 = Query4.drop(columns=["Closed","Live"]) # inplace=True)
#print(Q4)
Query5 = round (Q4.div( Q4.iloc[:,-1], axis=0 ) * 100, 2)
#print(Query5)
#keep_same = {'Id', 'Name'}
Query5.columns = ['{}{}'.format(c, '_PerCent') for c in Query5.columns]
#print(Query5)

result = pd.concat([Q4, Query5], axis=1, join='outer', sort=True)

result1 = pd.DataFrame(result)
Name_order = ['Restructuring', 'Restructuring_PerCent', 'Settlement', 'Settlement_PerCent', 'Write-off', 'Write-off_PerCent', 'Total']
print(result1)
df = result1[Name_order]
#df2 = df.drop('Total_old')
#df = result[sorted(result.columns)]
#print(result.columns)
#df = df[sorted(df.columns)]
print(df)

