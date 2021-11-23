import model
import constants

import numpy as np

from matplotlib import pyplot as plt


plt.style.use(
    [
        "seaborn-whitegrid",
        "seaborn-paper",
        "seaborn-muted",
        {
            "axes.spines.right": False,
            "axes.spines.top": False,
            "axes.edgecolor": "0.4",
            "axes.labelcolor": "0.0",
            "axes.titlesize": "large",
            "axes.labelsize": "medium",
            "figure.autolayout": True,
            "font.family": ["serif"],
            "font.weight": "regular",
            "font.size": 12.0,
            "grid.linestyle": "--",
            "legend.fontsize": 12.0,
            "legend.facecolor": "0.9",
            "legend.frameon": True,
            "savefig.transparent": True,
            "text.color": "0.0",
            "xtick.labelsize": "small",
            "ytick.labelsize": "small"
        }
    ]
)


def main():
    """
    Plot SEIR curves. 
    """

    data = model.seir_model()
    fig, ax = plt.subplots(figsize=(8.0, 6.0))

    ax.plot(data["t"], 100.0 * data["S"], linestyle="solid", linewidth=2, color="#4878CF", label="Suscetíveis")
    ax.plot(data["t"], 100.0 * data["E"], linestyle="solid", linewidth=2, color="#ED2139", label="Expostos")
    ax.plot(data["t"], 100.0 * data["I"], linestyle="solid", linewidth=2, color="#D9C514", label="Infecciosos")
    ax.plot(data["t"], 100.0 * data["R"], linestyle="solid", linewidth=2, color="#07A81A", label="Recuperados")

    """
    O seguinte trecho de código é a respeito da analise pedida na pergunta 3
    do roteiro, na qual é pedida uma estimativa para o número de leitos de UTI
    necessários para se lidar com o pico.

    A lista "ICU_occupation" irá representar a ocupação dos leitos. Cada
    posição da lista corresponde a um leito, e o conteúdo de cada posição
    representa o estado de ocupação de determinado leito. Portanto, se
    ICU_occupation[i] = y, então o leito i está com o estado de ocupação y.
    Um leito de UTI pode estar vazio (None) ou ocupado. Se estiver ocupado,
    pode estar ocupado há 0, 1, 2, ..., "TIME_IN_ICU" dias, onde "TIME_IN_ICU"
    representa a medianas dos tempos de UTI (estamos supondo que todos que vão
    para UTI passam a mesma quantidade de dias nos leitos). Portanto,
    y ∈ {None, 0, 1, ..., TIME_IN_ICU}.
    """

    ICU_occupation = []
    
    treated_patients = 0
    total_of_patients = 0
    
    max_ICUs = np.round(27 / 1.0e5 * constants.POPULATION)

    for t in data["t"]:
        """ 
        Para cada dia vamos calcular a demanda de novos leitos. Para isso,
        precisamos estimar, de alguma forma, o número de novos doentes que podem
        ir para UTI a cada dia. Esse número será proporcional ao fluxo diário de
        pessoas transitando de I para R, ou seja, dR/dt * "POPULATION" em que
        dR/dt = "CONSTANT_3" * I * "POPULATION". Considerando que a proporção de
        novos doentes que precisam de leito é de "ICU_DEMAND", obtemos que a demanda
        ("ICU_request") por leitos de UTI no dia t é dada pela expressão a seguir.
        """

        ICU_request = int(
            np.round(
                constants.ICU_DEMAND *
                constants.POPULATION *
                constants.CONSTANT_3 * data["I"][int(t)]
            )
        )
        
        total_of_patients += ICU_request

        """ 
        A variável "using_ICUs" representará a quantidade de leitos de UTI utilizados
        no dia t. Começamos definindo-a como sendo igual a demanda no mesmo dia.
        """

        using_ICUs = ICU_request

        """
        No próximo laço, vamos atualizar os estados dos hipotéticos leitos de UTI e
        ao mesmo tempo ir fazendo a contagem do número de ocupação ("using_ICUs").

        Fazendo uma varredura entre todos os leitos para cada dia, precisa-se ser
        verificado se o leito i está ou não vazio. Se não estiver, isso significa que
        passou-se mais um dia que um paciente ocupou esse leito, e assim ICU_occupation[i]
        deve ser incrementado. Após isso, precisa-se verificar se esse leito já chegou
        no limite de dias que pode ser ocupado ("TIME_IN_ICU"). Se chegou e ainda há
        algum paciente da demanda diária por UTI, podemos alocar esse paciente para
        esse leito ("ICU_occupation[i] = 0" e "ICU_request -= 1" ). Se chegou e não 
        há mais demanda, então apenas esvaziamos o leito ("ICU_occupation[i] = None").
        Agora, se o leito não chegou no limite de dias, apenas incrementamos nossa
        contagem de leitos sendo utilizados ("using_ICUs += 1"), já que não haviamos
        contabilizado esse leito antes. E por fim, se o leito estiver vazio e se ainda
        houver demanda ("ICU_request > 0"), então devemos ocupar esse leito 
        ("ICU_occupation[i] = 0" e "ICU_request -= 1").
        
        Perceba que se um leito já chegou no limite de dias que pode ser ocupado e ele
        representa algum dos 11.891 primeiros leitos (quantidade de leitos que o estado
        de São Paulo realmente possui), então devemos incrementar a quantidade de
        pacientes que foram devidamente tratados. A quantidade de pacientes que não
        receberam tratamento será a diferença entre o total e a quantidade de pacientes
        devidamente tratados.

        Após realizar essa varredura, repare que alocamos alguns (ou todos) dos novos
        pacientes que precisavam da UTI em leitos que já existiam no dia anterior e
        agora estavam disponíveis. Mas e se isso não for o suficiente para acomodar
        todos os pacientes? E se, após ocupar todos os leitos disponíveis, ainda houver
        demanda ("ICU-request > 0")? A resposta é simples: devemos "criar" novos leitos
        no nosso mundo fictício, ou seja, criar novas posições com 0 na lista
        "ICU_occupation" até que não haja mais demanda. Repare que aqui não precisamos
        mais mexer na variável "using_ICU", uma vez que estamos apenas adicionando novos
        pacientes a novos leitos, e eles já foram contabilizados na linha "using_ICUs = ICU_request".

        Depois de todo esse processo descrito, teremos a lista com o estado dos leitos
        atualizada e o número de leitos necessários ("using_ICUs") para o dia t. Note,
        então, que a demanda máxima por leitos de UTI será simplesmente o comprimento do
        vetor "ICU_occupation", cumprindo o que foi pedido no roteiro relativo à questão 3.
        """

        # Update occupation days
        for i in range(len(ICU_occupation)):
            if ICU_occupation[i] is not None:
                ICU_occupation[i] += 1

                if ICU_occupation[i] >= constants.TIME_IN_ICU:
                    if i < max_ICUs:
                        treated_patients += 1

                    if ICU_request > 0:
                        # Reallocates a new patient
                        ICU_occupation[i] = 0
                        ICU_request -= 1
                    else:
                        # Leave the bed empty
                        ICU_occupation[i] = None
                else:
                    # Count old sick
                    using_ICUs += 1
            else:
                if ICU_request > 0:
                    # Reallocates a new patient
                    ICU_occupation[i] = 0
                    ICU_request -= 1

        if ICU_request > 0:
            for j in range(ICU_request):
                ICU_occupation.append(0)

    print(f"O número de pacientes que não receberam tratamento é de: {total_of_patients - treated_patients}")
    print(f"O número máximo de leitos utilizados é de: {len(ICU_occupation)}")

    ax.set_xlabel("Tempo [dias]")
    ax.set_ylabel("Percentual [%]")

    ax.set_xlim((0.0, 501.0))
    ax.set_ylim((-1, 101.0))

    plt.legend(loc="center right")
    plt.savefig("images/simulation.png", dpi=200)
    plt.show()


if __name__ == "__main__":
    main()