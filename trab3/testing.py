import os
import trab2luisotaviodesimone as t2
from plot import plot_bode_duo
import numpy as np


def executeAC(netlist_file, current_type, desired_nodes, params, enable_print=False):
    frequencies, desired_nodes_modules, desired_nodes_phases = t2.main(
        f"{os.getcwd()}\\netlists\\{netlist_file}",
        current_type,
        desired_nodes,
        params,
        enable_print,
    )

    for i in range(len(desired_nodes)):
        plot_bode_duo(
            frequencies,
            desired_nodes_modules[i],
            desired_nodes_phases[i],
            netlist_file,
            desired_nodes[i],
        )


def executeDC(netlist_file, current_type, desired_nodes, params, enable_print=False):
    voltage_matrix = t2.main(
        f"{os.getcwd()}\\netlists\\{netlist_file}",
        current_type,
        desired_nodes,
        params,
        enable_print,
    )

    return voltage_matrix



"""
main(nomeArquivo, "DC" ou "TRANS", [lista de nós desejados], [lista de parâmetros])

lista de parâmetros (DC):
[0]: float -> representando o valor da tolerância de Newton-Raphson (NR)
[1]: list -> lista de valores iniciais para cada nó da netlist que devem ser usados como aproximação inicial para o NR (ignorar caso a netlist não possua componentes não-lineares)

lista de parâmetros (TRANS):
[0]: float -> tempo total da simulação (em segundos) de 0 ao T dado
[1]: float -> passo da simulação (em segundos)
[3]: float -> tolerância de NR
[4]: 
"""
