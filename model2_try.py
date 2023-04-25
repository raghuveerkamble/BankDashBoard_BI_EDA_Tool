from sklearn.model_selection import train_test_split
import lightgbm as lgb
import shap
import pandas as pd
from dplython import (DplyFrame, X, diamonds, select, sift, sample_n,
                      sample_frac, head, arrange, mutate, group_by,
                      summarize, DelayFunction)

from sklearn.ensemble import RandomForestClassifier
from explainerdashboard.datasets import titanic_survive, titanic_names
from explainerdashboard import ClassifierExplainer, ExplainerDashboard

csv_file = "data/Dec22a.csv"
csv_data = pd.read_csv(csv_file)
table = pd.DataFrame(csv_data)
MoonStoneData = DplyFrame(table)

#X_train, y_train, X_test, y_test = titanic_survive()
train_names, test_names = titanic_names()


model = RandomForestClassifier(n_estimators=50, max_depth=5)
model.fit(X_train, y_train)

explainer = ClassifierExplainer(model, X_test, y_test)

#db = ExplainerDashboard(explainer, title="Moon Stone")
#db.run()


ExplainerDashboard(explainer, title="Moon Stone",
                        importances=True,
                        model_summary=True,  
                        contributions=True,
                        whatif=True,
                        shap_dependence=True,
                        shap_interaction=True,
                        decision_trees=True).run()

"""

explainer = ClassifierExplainer(model, X_test, y_test, 
                                    cats=['Sex', 'Deck'],
                                    idxs=test_names, 
                                    labels=['Queenstown', 'Southampton', 'Cherbourg'],
                                    pos_label='Southampton')
X_train.head()
print(explainer)
#ExplainerDashboard(explainer).run()
#ExplainerDashboard(ClassifierExplainer(RandomForestClassifier().fit(X_train, y_train), X_test, y_test)).run()



shap.initjs()X,y = shap.datasets.adult()
X_display,y_display = shap.datasets.adult(display=True)# create a train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=7)
d_train = lgb.Dataset(X_train, label=y_train)
d_test = lgb.Dataset(X_test, label=y_test)# create a simple model
params = {
    "max_bin": 512,
    "learning_rate": 0.05,
    "boosting_type": "gbdt",
    "objective": "binary",
    "metric": "binary_logloss",
    "num_leaves": 10,
    "verbose": -1,
    "min_data": 100,
    "boost_from_average": True
}model = lgb.train(params, d_train, 10000, valid_sets=[d_test], early_stopping_rounds=50, verbose_eval=1000)# explain the model

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X)# visualize the impact of each features
shap.summary_plot(shap_values, X)
"""