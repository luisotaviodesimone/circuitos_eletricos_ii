import os
import trab3luisotaviodesimone as t3
from plot import plot_bode_duo
import numpy as np


def executeAC(netlist_file, current_type, desired_nodes, params, enable_print=False):
    frequencies, desired_nodes_modules, desired_nodes_phases = t3.main(
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
    voltage_matrix = t3.main(
        f"{os.getcwd()}\\testesDC\\{netlist_file}",
        current_type,
        desired_nodes,
        params,
        enable_print,
    )

    return voltage_matrix


def compareDC(execution, result):
    print(
        f"{execution} == {result} \n",
        np.allclose(execution, result, rtol=1e-03, atol=1e-03),
        "\n",
    )


def continuous_current():
    print("teste1.txt")
    compareDC(
        executeDC("teste1.txt", "DC", [1, 2], [1e-10, [0, 0.1, 0.1]]), [2.0, 1.30491003]
    )

    print("teste2.txt")
    compareDC(executeDC("teste2.txt", "DC", [2], [1e-14, [0, 3, 3]]), [0.73068013])

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


# continuous_current()


def estampaResistor(a, b, R, G):
    G[a, a] = G[a, a] + 1 / R
    G[a, b] = G[a, b] - 1 / R
    G[b, a] = G[b, a] - 1 / R
    G[b, b] = G[b, b] + 1 / R
    return G


def estampaFonteInd(a, b, Iin, I):
    """Considera o sentido da corrente de a para b"""
    I[a] = I[a] - Iin
    I[b] = I[b] + Iin
    return I


def estampaResistorQuadratico(a, b, e, G, I):
    """Considera que a é o nó positivo e b é o nó negativo"""
    v = e[a] - e[b]
    G0 = 2 * v
    I0 = v**2 - G0 * v
    G = estampaResistor(a, b, 1 / G0, G)
    I = estampaFonteInd(a, b, I0, I)
    return G, I


def testeFernanda():
    k = 0

    tol = 1e-12

    e0 = np.array([0, 1])

    Gref = np.zeros([2, 2])

    Iref = np.zeros(2)

    Gref = estampaResistor(0, 1, 2, Gref)

    Iref = estampaFonteInd(0, 1, 1 / 2, Iref)

    while k < 100:
        # print(Gref)
        # print(Iref)
        Gn, In = estampaResistorQuadratico(1, 0, e0, Gref.copy(), Iref.copy())
        # print(Gn)
        # print(In)

        Gn = Gn[1:, 1:]
        In = In[1:]
        e = np.linalg.solve(Gn, In)

        if np.max(np.abs(e - e0[1:])) < tol:
            break

        print("e", e)
        input("-------------------------------------------")
        e0 = np.hstack((np.array([0]), e))
        print("e0", e0)

        k = k + 1


testeFernanda()

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
