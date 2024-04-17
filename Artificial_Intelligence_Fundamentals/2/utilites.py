import numpy as np
import matplotlib.pyplot as plt


def visualize_classifier(classifier, X, y):
    # Определение для Х и У минимального и максимального
    # значений, которые будут использоваться при построении сетки
    min_x, max_x = X[:, 0].min() - 1.0, X[:, 0].max() + 1.0
    min_y, max_y = X[:, 1].min() - 1.0, X[:, 1].max() + 1.0

    # Определение величины шага для построения сетки
    mesh_step_size = 0.01
    # Определение сетки для значений Х и У
    x_vals, y_vals = np.meshgrid(np.arange(min_x, max_y, mesh_step_size), np.arange(min_y, max_y, mesh_step_size))

    # Вьmолнение классификатора на сетке данных
    output = classifier.predict(np.c_[x_vals.ravel(), y_vals.ravel()])

    # Переформирование выходного массива
    output = output.reshape(x_vals.shape)

    # Создание графика
    plt.figure()

    plt.pcolormesh(x_vals, y_vals, output, cmap=plt.cm.gray)

    plt.scatter(X[:, 0], X[:, 1], c=y, s=75, edgecolors='black', linewidths=1, cmap=plt.cm.Paired)

    # Определение границ графика
    plt.xlim(x_vals.min(), x_vals.max())
    plt.ylim(y_vals.min(), y_vals.max())

    # Определение делений на осях Х и У
    plt.xticks((np.arange(int(X[:, 0].min() - 1), int(X[:, 0].max() + 1), 1.0)))
    plt.yticks((np.arange(int(X[:, 1].min() - 1), int(X[:, 1].max() + 1), 1.0)))

    plt.show()