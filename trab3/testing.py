import os
import trab3luisotaviodesimone as t3
from lotdsformatting import color
from plot import plot_bode_duo
import numpy as np


def executeAC(netlist_file, current_type, desired_nodes, params, enable_print=False):
    frequencies, desired_nodes_modules, desired_nodes_phases = t3.main(
        f"{os.getcwd()}/netlists/{netlist_file}",
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
    voltage_matrix = t3.main(
        f"{os.getcwd()}/testesDC/{netlist_file}",
        current_type,
        desired_nodes,
        params,
        enable_print,
    )

    return voltage_matrix


def executeTRAN(netlist_file, current_type, desired_nodes, params, enable_print=False):
    voltage_matrix = t3.main(
        f"{os.getcwd()}/testesTRAN/{netlist_file}",
        current_type,
        desired_nodes,
        params,
        enable_print,
    )

    return voltage_matrix


def compareDC(execution, result):
    print(
        f"{execution} == {result} \n",
        color(f"{np.allclose(execution, result, rtol=1e-03, atol=1e-03)}", "blue"),
        "\n",
    )


def continuous_current():
    print("teste1.txt")
    compareDC(
        executeDC("teste1.txt", "DC", [1, 2], [1e-10, [0, 0.1, 0.1]]),
        [2.0, 1.30491003],
    )

    # Does not converge
    print("teste2.txt")
    compareDC(executeDC("teste2.txt", "DC", [2], [1e-14, [0, 3, 3]]), [0.73068013])

    # Does not converge
    print("teste3.txt")
    compareDC(executeDC("teste3.txt", "DC", [2], [1e-12, [0, 0, 2]]), [2])

    print("teste4.txt")
    compareDC(executeDC("teste4.txt", "DC", [2], [1e-12, [0, 0, 2]]), [1.9])

    print("teste5.txt")
    compareDC(executeDC("teste5.txt", "DC", [1, 2], [1e-12, [0, 1, 2]]), [5, 4.2781936])

    print("teste6.txt")
    compareDC(
        executeDC("teste6.txt", "DC", [1, 2, 3], [1e-14, [0, 5, 1, -5]]),
        [5, 4.2781936, -5],
    )

    print("teste7.txt")
    compareDC(
        executeDC("teste7.txt", "DC", [1, 2, 3], [1e-14, [0, -5, 4, 5]]),
        [-5, 4.2781936, 5],
    )


continuous_current()


def transient_regime():
    print("teste1.txt")
    executeTRAN("teste1.txt", "DC", [1, 2], [1e-10, [0, 0.1, 0.1]])


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
[3]: float -> tolerância de NR
[4]: 
"""
