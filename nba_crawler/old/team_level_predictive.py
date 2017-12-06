import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
# import datetime

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
# from itertools import combinations
# from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.linear_model import ElasticNet


dfTG = pd.read_csv('team_game_final.csv')
dfTG_scaled = dfTG[[c for c in dfTG.columns if 'cum' not in c]].copy()
dfTG_scaled = dfTG_scaled[dfTG_scaled.mp_prior > 0]
omit_cols = ['season', 'mp', 'pts', 'pts_opp', 'pts_net']
cols_to_scale = [c for c in dfTG_scaled.columns.tolist() if (c not in omit_cols) & ((isinstance(dfTG_scaled[c].values[0], int)) | (isinstance(dfTG_scaled[c].values[0], float)))]

# Scale columns, ignore each team's first game (mp_prior == 0)
dfTG_scaled.loc[:, cols_to_scale] = dfTG_scaled.loc[:, cols_to_scale].apply(lambda c: (c - c.mean())/c.std(), axis = 0)


prior_cols = [c for c in dfTG_scaled.columns if 'prior' in c]
prior_net = [c for c in prior_cols if 'net' in c]
net_cols = [c for c in cols_to_scale if ('net' in c) & ('prior' not in c)]
win_corr = dfTG_scaled[['result_win'] + prior_net].corr()
dfcorr = pd.DataFrame(win_corr['result_win'])
dfcorr['abs_corr'] = abs(dfcorr['result_win'])
dfcorr.sort('abs_corr', ascending = False, inplace = True)

test_cols = dfcorr.loc[dfcorr.abs_corr > .15, ].index.tolist()
target_col = 'result_win'
X = dfTG_scaled[test_cols]
y = dfTG_scaled[target_col]
Xtrain, Xtest, ytrain, ytest = train_test_split(X, y)


degree = 5
a = 1
model = LogisticRegression
# clf = make_pipeline(PolynomialFeatures(degree), model(alpha = a))
# clf = make_pipeline(PolynomialFeatures(degree), model(C = 10))
clf = LogisticRegression(C = 10)
clf.fit(Xtrain, ytrain)

print clf.score(Xtrain, ytrain)
print clf.score(Xtest, ytest)
ypred = clf.predict(Xtest)


cm = pd.crosstab(ytest, ypred, rownames=["Actual"], colnames=["Predicted"])
cm


def mae_mse(ytrue, yhat):
	mae = np.mean([abs(yh - yt) for yt, yh in zip(ytrue, yhat)])
	mse = np.mean([pow((yh - yt), 2) for yt, yh in zip(ytrue, yhat)])
	return mae, mse

# Continuous Target
test_cols = dfcorr.loc[dfcorr.abs_corr > .15, ].index.tolist()
target_col = 'pts_net'
X = dfTG_scaled[test_cols]
y = dfTG_scaled[target_col].map(float)
Xtrain, Xtest, ytrain,ste ytest = train_test_split(X, y)

lnRidge = Ridge()
lnRidge.fit(Xtrain, ytrain)

print lnRidge.score(Xtrain, ytrain)
print lnRidge.score(Xtest, ytest)

yhat_train = lnRidge.predict(Xtrain)
yhat = lnRidge.predict(Xtest)
print 'MSE: {:.4f} (train)'.format(mae_mse(ytrain, yhat_train)[1])
print 'MSE: {:.4f} (test)'.format(mae_mse(ytest, yhat)[1])


# Lasso
lnLasso = Lasso(alpha = .000001)
lnLasso.fit(Xtrain, ytrain)

print lnLasso.score(Xtrain, ytrain)
print lnLasso.score(Xtest, ytest)

yhat_train = lnLasso.predict(Xtrain)
yhat = lnLasso.predict(Xtest)
print 'MSE: {:.4f} (train)'.format(mae_mse(ytrain, yhat_train)[1])
print 'MSE: {:.4f} (test)'.format(mae_mse(ytest, yhat)[1])


# ElasticNet
lnElastic = ElasticNet(alpha = .0000001)
# lnElastic = make_pipeline(PolynomialFeatures(degree), ElasticNet(alpha = 0.00001))
lnElastic.fit(Xtrain, ytrain)

print lnElastic.score(Xtrain, ytrain)
print lnElastic.score(Xtest, ytest)

yhat_train = lnElastic.predict(Xtrain)
yhat = lnElastic.predict(Xtest)
print 'MSE: {:.4f} (train)'.format(mae_mse(ytrain, yhat_train)[1])
print 'MSE: {:.4f} (test)'.format(mae_mse(ytest, yhat)[1])
