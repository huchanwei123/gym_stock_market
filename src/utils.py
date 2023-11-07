import matplotlib.pyplot as plt


def plot_2D(x_data, y_data, names):
    """
    names: should be a list [Title, x-axis, y-axis]
    """
    plt.plot(x_data, y_data)
    plt.title(names[0])
    plt.xlabel(names[1])
    plt.ylabel(names[2])
    plt.show()
