from common import *
from sklearn.linear_model import ElasticNet
from sklearn.datasets import make_regression


X, y = make_regression(n_features=2, random_state=0)
X[:, 0] *= 50
if 1:
    print "shape X, y = ", np.shape(X), np.shape(y)
    plt.scatter(X[:, 0], y, label="feat0")
    plt.scatter(X[:, 1], y, label="feat1")
    plt.legend()
    if 1:
        plt.show()
        #exit(0)

if 0:
    from sklearn.preprocessing import StandardScaler

    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    if 1:
        print "shape X, y = ", np.shape(X), np.shape(y)
        plt.scatter(X[:, 0], y, label="feat0")
        plt.scatter(X[:, 1], y, label="feat1")
        plt.legend()
        if 1:
            plt.show()
            #exit(0)
regr = ElasticNet(random_state=0)
print regr
regr.fit(X, y)
print regr
#ElasticNet(alpha=1.0, copy_X=True, fit_intercept=True, l1_ratio=0.5,
#      max_iter=1000, normalize=False, positive=False, precompute=False,
#      random_state=0, selection='cyclic', tol=0.0001, warm_start=False)
print(regr.coef_)
#[18.83816048 64.55968825]

print(regr.intercept_)
#1.451...
print(regr.predict([[0, 0]]))
#[1.451...]
print regr.score(X, y)


#get elastic net score
