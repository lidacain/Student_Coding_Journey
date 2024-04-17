import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches

from sklearn import datasets
from sklearn.mixture import GaussianMixture
from sklearn.model_selection import StratifiedKFold

iris = datasets.load_iris()
indicies = StratifiedKFold(n_splits=5).split(iris.data, iris.target)

train_index, test_index = next(iter(indicies))

X_train = iris.data[train_index]
y_train = iris.target[train_index]

X_test = iris.data[test_index]
y_test = iris.target[test_index]

num_clusters = len(np.unique(y_train))

gmm = GaussianMixture(n_components=num_clusters, covariance_type='full')
gmm.means_ = np.array([X_train[y_train == i].mean(axis=0) for i in range(num_clusters)])
gmm.fit(X_train)

plt.figure()
colors = 'bgr'
for i, color in enumerate(colors):
    eigenvalues, eigenvectors = np.linalg.eigh(gmm.covariances_[i][:2, :2])
    norm_vec = eigenvectors[0] / np.linalg.norm(eigenvectors[0])
    angle = np.arctan2(norm_vec[1], norm_vec[0])
    angle = 180 * angle / np.pi
    eigenvalues *= 8
    ell = patches.Ellipse(gmm.means_[i, :2], eigenvalues[0], eigenvalues[1], 180 + angle, color=color)
    axis_handle = plt.subplot(1, 1, 1)
    ell.set_clip_box(axis_handle.bbox)
    ell.set_alpha(0.6)
    axis_handle.add_artist(ell)

for i, color in enumerate(colors):
    cur_data = iris.data[iris.target == i]
    plt.scatter(cur_data[:,0], cur_data[:,1], marker='o', facecolors='none', edgecolors=color, s=40, label = iris.target_names[i])
    test_data = X_test[y_test == i]
    plt.scatter(test_data[:,0], test_data[:,1], marker='s', facecolors='none', edgecolors=color, s=40, label = iris.target_names[i])

y_train_pred = gmm.predict(X_train)
train_accuracy = np.mean(y_train_pred.ravel() == y_train.ravel()) * 100
print('Точность на обучающей выборке: ', train_accuracy)

y_test_pred = gmm.predict(X_test)
test_accuracy = np.mean(y_test_pred.ravel() == y_test.ravel()) * 100
print('Точность на тестовой выборке: ', test_accuracy)

plt.title('GMM-классификатор')
plt.xticks(())
plt.yticks(())
plt.show()