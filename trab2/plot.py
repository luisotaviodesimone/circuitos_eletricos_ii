from matplotlib import pyplot


def plot_bode_duo(freqs, modulos, fases):
    pyplot.subplot(1, 2, 1)
    pyplot.title("Módulo")
    pyplot.plot(freqs, modulos)
    pyplot.xscale("log")

    pyplot.subplot(1, 2, 2)
    pyplot.title("Fase")
    pyplot.plot(freqs, fases)
    pyplot.xscale("log")
    pyplot.show()


def plot_bode_uni(freqs, modules, phases):
    fig, ax1 = pyplot.subplots()
    ax1.semilogx(freqs, modules)
    ax2 = ax1.twinx()
    ax2.semilogx(freqs, phases, "r--")
    pyplot.show()
