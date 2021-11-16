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
    
    ICU_occupation = []
    max_used_ICUs = None
    
    for t in data["t"]:
        # Compute the new ICU request for each day
        ICU_request = int(
            np.round(
                constants.ICU_DEMAND *
                constants.POPULATION *
                constants.CONSTANT_3 * data["I"][int(t)]
            )
        )
        
        using_ICUs = ICU_request
        
        # Update occupation days
        for i in range(len(ICU_occupation)):
            if ICU_occupation[i] is not None:
                ICU_occupation[i] += 1
                
                if ICU_occupation[i] >= constants.TIME_IN_ICU:
                    if ICU_request > 0:
                        # Reallocates a new sick
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
                    # Reallocates a new sick
                    ICU_occupation[i] = 0
                    ICU_request -= 1
        
        if ICU_request > 0:
            for j in range(ICU_request):
                ICU_occupation.append(0)
        
        # Compute the maximum of used ICUs
        if max_used_ICUs is None or using_ICUs > max_used_ICUs:
            max_used_ICUs = using_ICUs
    
    print(f"O número máximo de leitos utilizados é de: {max_used_ICUs}")
        
    ax.set_xlabel("Tempo [dias]")
    ax.set_ylabel("Percentual [%]")
    
    ax.set_xlim((0.0, 501.0))
    ax.set_ylim((-1, 101.0))
    
    plt.legend(loc="center right")
    plt.savefig("images/simulation.png", dpi=200)
    plt.show()


if __name__ == "__main__":
    main()