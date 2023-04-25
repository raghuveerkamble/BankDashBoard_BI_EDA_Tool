from dfply import *
import pandas as pd
import numpy as np
from dplython import (DplyFrame, X, diamonds, select, sift, sample_n,
                      sample_frac, head, arrange, mutate, group_by,
                      summarize, DelayFunction)
from IPython.display import display
from dfply import *

# load packages
#from dplython import select, DplyFrame, X, arrange, count, sift, head, summarize, group_by, tail, mutate, sum
#import pandas as pd

# read in data
#state_df = pd.read_csv("state_info.txt")

csv_file = "data/Dec22.csv"
csv_data = pd.read_csv(csv_file)
table = pd.DataFrame(csv_data)
#print(table.columns[1])

diamonds = DplyFrame(table)
diamondsSmall = diamonds >> select(X.Portfolio, X.Vertical, X.Segment, X.Status, X.Amt, X.Branch, X.DEC_22_CL_BKT, X.Nature_of_Business, X.Constitution)
#print(diamondsSmall).head()
"""
Query4 = pd.pivot_table(data=diamondsSmall,
                       index=['Portfolio'], columns=['Status'],
                       values=['Amt'], aggfunc= ['count', 'sum'],
                       margins = True, margins_name='Total')

#print(Query4)

Query5 = pd.pivot_table(data=diamondsSmall,
                       index=['Portfolio'], columns=['Status'],
                        aggfunc= ['count', 'sum'], #values=['Amt'],
                       margins = True, margins_name='Total')
#print(Query5)

@dfpipe
def crosstab(df, index, columns):
    return pd.crosstab(index, columns)

"""
Query6 = (diamondsSmall >> 
         
#        mutate(carat_bin=X.carat.round()) >> 
         group_by( X.Status) >>
         sift(X.Portfolio == 'New Book') >>
         summarize(count=X.Status.count(), amt=np.sum(X.Amt)) 
         
         
         #arrange(X.Portfolio) 
         #crosstab(X.Portfolio, X.Status)   
)

#Query6.append(Query6.sum(numeric_only=True), ignore_index=True)
#df.loc['Column_Total']= df.sum(numeric_only=True, axis=0)
#df.loc[:,'Row_Total'] = df.sum(numeric_only=True, axis=1)

#Query6.loc['Column_Total']= Query6.sum(numeric_only=True, axis=0)


print(Query6)

Query7 = (Query6 >>
            mutate(countpercent = round((Query6['count'] / Query6['count'].sum()) * 100, 2),
                amtpercent = round((Query6['amt'] / Query6['amt'].sum()) * 100, 2),
            )
        )
print(Query7)


Query4 = pd.pivot_table(data=diamondsSmall,
                       index=['Status'], columns=['Portfolio'],
                       values=['Amt'], aggfunc= ['count', 'sum'],
                       margins = True, margins_name='Total')
print(Query4)
print(Query4.columns)

Query4.columns = ['_'.join(col) for col in Query4.columns.values]

print(Query4.columns)
print(Query4)

#Query8 = Query4 >> select(X.Portfolio, X.Vertical, X.Segment, X.Status, X.Amt, X.Branch, X.DEC_22_CL_BKT)

Query8 = (diamondsSmall >> 
         group_by( X.Status) >>
         sift(X.Portfolio == 'Old Book') >>
         summarize(count=X.Status.count(), amt=np.sum(X.Amt)))
print(Query8)

Query9 = (Query8 >>
            mutate(countpercent = round((Query8['count'] / Query8['count'].sum()) * 100, 2),
                amtpercent = round((Query8['amt'] / Query8['amt'].sum()) * 100, 2),
            )
        )
print(Query9)

#Query10 = (Query8 >> inner_join(Query9, by='Status'))

#print(Query10)

result = pd.concat([Query7, Query9], axis=1, join='inner')
print(result)
print(result.columns)
#result.append(result.sum(numeric_only=True), ignore_index=True)


Query11 = (diamondsSmall >> 
         
#        mutate(carat_bin=X.carat.round()) >> 
         group_by( X.Nature_of_Business) >>
         #sift(X.Portfolio == 'New Book') >>
         summarize(count=X.Status.count(), amt=np.sum(X.Amt)) 
         
         
         #arrange(X.Portfolio) 
         #crosstab(X.Portfolio, X.Status)   
)
print(Query11)
Query12 = (Query11 >>
            mutate(countpercent = round((Query11['count'] / Query11['count'].sum()) * 100, 2),
                amtpercent = round((Query11['amt'] / Query11['amt'].sum()) * 100, 2),
            )
        )
print(Query12)
Query13 = Query12 >> select(X.Nature_of_Business, X.count, X.countpercent, X.amt, X.amtpercent)
print(Query13)
"""
Query7 = (Query6 >>
        mutate(kpercent=(X.count / np.sum(X.count)))
)
"""


"""

Query7 = pd.pivot_table(data=Query6,
                       index=['Status'], columns=['Portfolio'],
                       aggfunc= ['sum'], #values=['Amt'],
                       margins = True, margins_name='Total')

print(Query7)
"""
df = diamondsSmall

def age_bucket(age):
    if age <= 18:
        return "<18"
    else:
        return ">18"
  
df['Age Group'] = df['Age'].apply(age_bucket)
  
# calculating gender percentage
gender = pd.DataFrame(df.Gender.value_counts(normalize=True)*100).reset_index()
gender.columns = ['Gender', '%Gender']
df = pd.merge(left=df, right=gender, how='inner', on=['Gender'])
  
# creating pivot table
table = pd.pivot_table(df, index=['Gender', '%Gender', 'Age Group'], 
                       values=['Name'], aggfunc={'Name': 'count',})
  
# display table
print("Table")
print(table)

#----------------

# importing required libraries
import pandas as pd
import matplotlib.pyplot as plt

# creating dataframe
df = pd.DataFrame({
	'Name': ['John', 'Emily', 'Smith', 'Joe'],
	'Gender': ['Male', 'Female', 'Male', 'Female'],
	'Salary(in $)': [20, 40, 35, 28]})

print("Dataset")
print(df)
print("-"*40)

# creating pivot table
table = pd.pivot_table(df, index=['Gender', 'Name'])

# calculating percentage
table['% Income'] = (table['Salary(in $)']/table['Salary(in $)'].sum())*100

# display table
print("Pivot Table")
print(table)


#----
df['percent'] = df.groupby(level=0).transform(lambda x: (x / x.sum()).round(2))



"""

#df.columns = ['_'.join(col) for col in df.columns.values]
#df.columns = df.columns.str.replace('Amt_', '')
#df.mul(100, axis=1)
#print(df)
#df['Current'] = df['Current'].applymap(lambda x: "{0:.2f}%".format(x*100))
#print(df)     
#list1 = df.columns
#print(list1)   
#print(diamondsSmall['DEC_22_CL_BKT'].unique())

#print(df)        

rankings_pd = rankings_pd.add_prefix('col_')
rankings_pd = rankings_pd.add_suffix('_1')

#list1 = df['DEC_22_CL_BKT']
#df['Current'] = df['Current'].applymap(lambda x: "{0:.2f}%".format(x*100))

Query11 = (diamondsSmall >> 
         
#        mutate(carat_bin=X.carat.round()) >> 
         group_by( X.Nature_of_Business) >>
         #sift(X.Portfolio == 'New Book') >>
         summarize(count=X.Status.count(), amt=np.sum(X.Amt)) 
         
         #arrange(X.Portfolio) 
         #crosstab(X.Portfolio, X.Status)   
)
#print(Query11)
Query12 = (Query11 >>
            mutate(countpercent = round((Query11['count'] / Query11['count'].sum()) * 100, 2),
                amtpercent = round((Query11['amt'] / Query11['amt'].sum()) * 100, 2),
            )
        )
#print(Query12)
Query13 = Query12 >> select(X.Nature_of_Business, X.count, X.countpercent, X.amt, X.amtpercent)
print(Query13)
df = diamondsSmall
Query14 = pd.pivot_table(data=diamondsSmall,
                       index=['Nature_of_Business'], columns=['DEC_22_CL_BKT'],
                       values=['Amt'], aggfunc= ['count'],
                       margins = True, margins_name='Total')
print(Query14)
"""



"""
#print("Table 2")
#print(table2)
#print(table2.columns[1])
#display(table2)
#table2.apply(lambda x: map(lambda x:'{:.2f}%'.format(x),x),axis=1)
#print(table2)
#table2[Current].style.format('{:,.3f}')
#


df2 = pd.crosstab(index= df.Nature_of_Business, columns= df.DEC_22_CL_BKT, values= df.Amt, aggfunc = np.count_nonzero
            ,margins=True,margins_name='Total',normalize= 'index')

print(df2)


table = pd.pivot_table(df, index=['Nature_of_Business'], columns=['DEC_22_CL_BKT'], margins = True, margins_name='Total')
print(table)
#table['% Income'] = (table['Salary(in $)']/table['Salary(in $)'].sum())*100


"""