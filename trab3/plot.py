from matplotlib import pyplot as plt


def plot_bode_duo(freqs, modulos, fases, netlist_file, desired_node):
    plt.figure(num=f"{netlist_file}-Node {desired_node}")

    plt.subplot(1, 2, 1)
    plt.title("Módulo")
    plt.plot(freqs, modulos)
    plt.xscale("log")

    plt.subplot(1, 2, 2)
    plt.title("Fase")
    plt.plot(freqs, fases)
    plt.xscale("log")
    plt.show()


def plot_bode_uni(freqs, modules, phases):
    fig, ax1 = plt.subplots()
    ax1.semilogx(freqs, modules)
    ax2 = ax1.twinx()
    ax2.semilogx(freqs, phases, "r--")
    plt.show()


def plot_tran(tempo, result, netlist_file, desired_node):
    plt.figure(num=f"{netlist_file}-Node {desired_node}")

    plt.plot(tempo, result)
    plt.show()
