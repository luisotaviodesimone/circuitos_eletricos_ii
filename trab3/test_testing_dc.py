import os
import trab3luisotaviodesimone as t3
from lotdsformatting import color
from plot import plot_bode_duo, plot_tran
import numpy as np


def executeDC(netlist_file, current_type, desired_nodes, params, enable_print=False):
    voltage_matrix = t3.main(
        f"{os.getcwd()}/testesDC/{netlist_file}",
        current_type,
        desired_nodes,
        params,
    )

    return voltage_matrix


def compareDC(execution, result):
    print(
        f"{execution} == {result} \n",
        color(f"{np.allclose(execution, result, rtol=1e-03, atol=1e-03)}", "blue"),
        "\n",
    )
    assert np.allclose(execution, result, rtol=1e-03, atol=1e-03)


def test_continuous_current():
    print(color("teste1.txt", "green"))
    compareDC(
        executeDC("teste1.txt", "DC", [1, 2], [1e-10, [0, 0.1, 0.1]]),
        [2.0, 1.30491003],
    )

    # Does not converge
    print(color("teste2.txt", "green"))
    compareDC(executeDC("teste2.txt", "DC", [2], [1e-14, [0, 3, 3]]), [0.73068013])

    # Does not converge
    print(color("teste3.txt", "green"))
    compareDC(executeDC("teste3.txt", "DC", [2], [1e-12, [0, 0, 2]]), [2])

    print(color("teste4.txt", "green"))
    compareDC(executeDC("teste4.txt", "DC", [2], [1e-12, [0, 0, 2]]), [1.9])

    print(color("teste5.txt", "green"))
    compareDC(executeDC("teste5.txt", "DC", [1, 2], [1e-12, [0, 1, 2]]), [5, 4.2781936])

    print(color("teste6.txt", "green"))
    compareDC(
        executeDC("teste6.txt", "DC", [1, 2, 3], [1e-14, [0, 5, 1, -5]]),
        [5, 4.2781936, -5],
    )

    print(color("teste7.txt", "green"))
    compareDC(
        executeDC("teste7.txt", "DC", [1, 2, 3], [1e-14, [0, -5, 4, 5]]),
        [-5, 4.2781936, 5],
    )

test_continuous_current()
