import matplotlib.pyplot as plt


def plot_2D(x_data, y_data, names, fmt='-', markersize=12):
    """
    names: should be a list [Title, x-axis, y-axis]
    """
    fig = plt.figure()
    plt.plot(x_data, y_data, fmt, markersize=markersize)
    plt.title(names[0])
    plt.xlabel(names[1])
    plt.ylabel(names[2])
    plt.show(block=False)

def plot_2Ds(x_data, y_datas, names, legends):
    """
    y_datas : should be a list of list!
    """
    fig = plt.figure()
    for i in range(len(y_datas)):
        plt.plot(x_data, y_datas[i])
    plt.title(names[0])
    plt.xlabel(names[1])
    plt.ylabel(names[2])
    plt.legend(legends)
    plt.show(block=False)

def plot_bar(x_data, y_data, names):
    """
    names: should be a list [Title, x-axis, y-axis]
    """
    fig = plt.figure()
    plt.bar(x_data, y_data)
    plt.title(names[0])
    plt.xlabel(names[1])
    plt.ylabel(names[2])
    plt.show(block=False)