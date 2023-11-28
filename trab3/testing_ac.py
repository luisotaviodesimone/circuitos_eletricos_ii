import os
import trab3luisotaviodesimone as t3
from lotdsformatting import color
from plot import plot_bode_duo, plot_tran
import numpy as np


def executeAC(netlist_file, current_type, desired_nodes, params, enable_print=False):
    frequencies, desired_nodes_modules, desired_nodes_phases = t3.main(
        f"{os.getcwd()}/netlists/{netlist_file}",
        current_type,
        desired_nodes,
        params,
    )

    for i in range(len(desired_nodes)):
        plot_bode_duo(
            frequencies,
            desired_nodes_modules[i],
            desired_nodes_phases[i],
            netlist_file,
            desired_nodes[i],
        )


def executeTRAN(netlist_file, current_type, desired_nodes, params, enable_print=False):
    tempo, voltage_matrix = t3.main(
        f"{os.getcwd()}/testesTRAN/{netlist_file}",
        current_type,
        desired_nodes,
        params,
    )

    for i in range(len(desired_nodes)):
        plot_tran(tempo, voltage_matrix[i], netlist_file, desired_nodes[i])

    return tempo, voltage_matrix


def transient_regime():
    print(color("testeTran1.txt", "green"))
    executeTRAN("testeTran1.txt", "TRAN", [1, 2], [2, 0.2e-3, 1e-10, [0, 1, 0.5]])

    print(color("testeTran2.txt", "green"))
    executeTRAN("testeTran2.txt", "TRAN", [1, 2], [2, 0.2e-3, 1e-4, [0, 1, 0]])

    print(color("testeTran3.txt", "green"))
    executeTRAN("testeTran3.txt", "TRAN", [1, 2], [3, 0.2e-3, 1e-4, [0, 0, 0]])

    print(color("testeTran4.txt", "green"))
    executeTRAN("testeTran4.txt", "TRAN", [1, 2], [3, 0.2e-3, 1e-4, [0, 0, 0]])

    print(color("testeTran5.txt", "green"))
    executeTRAN("testeTran5.txt", "TRAN", [1, 2], [3, 0.2e-3, 1e-4, [0, 9.5, 0]])

    print(color("testeTran6.txt", "green"))
    executeTRAN("testeTran6.txt", "TRAN", [1, 3], [2, 0.5e-4, 1e-4, [0, 0, 0, 0]])

    print(color("testeTran7.txt", "green"))
    executeTRAN("testeTran7.txt", "TRAN", [1, 2, 3], [2, 0.5e-4, 1e-4, [0, 0, 0, 0]])

    print(color("testeTran8.txt", "green"))
    executeTRAN("testeTran8.txt", "TRAN", [1, 2, 3], [4, 0.2e-3, 1e-4, [0, 0, 0, 0]])

    print(color("testeTran9.txt", "green"))
    executeTRAN("testeTran9.txt", "TRAN", [1, 2], [4, 0.2e-3, 1e-4, [0, 1, 1]])

    print(color("testeTran10.txt", "green"))
    executeTRAN("testeTran10.txt", "TRAN", [1, 2, 3], [4, 0.2e-3, 1e-4, [0, 5, 5, 0]])


transient_regime()

"""
main(nomeArquivo, "DC" ou "TRAN", [lista de nós desejados], [lista de parâmetros])

e.g.:

main('netlist1.txt', 'DC', [1,2], [1e-9, [0,1,0]])
main('netlist1.', 'TRAN', [1,2], [1e-3, 10e-6, 1e-9, [0,1,0]]).

lista de parâmetros (DC):
[0]: float -> representando o valor da tolerância de Newton-Raphson (NR)
[1]: list -> lista de valores iniciais para cada nó da netlist que devem ser usados como aproximação inicial para o NR (ignorar caso a netlist não possua componentes não-lineares)

lista de parâmetros (TRAN):
[0]: float -> tempo total da simulação (em segundos) de 0 ao T dado
[1]: float -> passo da simulação (em segundos)
[2]: float -> tolerância de NR
[3]: list  -> lista de valores iniciais para cada nó da netlist
"""
