import matplotlib.pyplot as plt
import numpy as np
import math
import os
from typing import Tuple
from .prepare_data import comp_tank_relative_r_phi
from sciopy.prepare_data import norm_data


def plot_potential_matrix(sample: np.lib.npyio.NpzFile) -> None:
    """
    Plot the potential matrix of a prepared sample.

    Parameters
    ----------
    sample : np.lib.npyio.NpzFile
        prepared sample
    """
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 4))
    ax1.set_title(r"$\Re\{P_m\}$")
    ax1.imshow(np.real(sample["potential_matrix"]))
    ax2.set_title(r"$\Im\{P_m\}$")
    ax2.imshow(np.imag(sample["potential_matrix"]))
    ax3.set_title(r"$|P_m|$")
    ax3.imshow(np.abs(sample["potential_matrix"]))
    fig.tight_layout()
    plt.show()


def plot_el_sign(sample: np.lib.npyio.NpzFile, norm: bool = False) -> None:
    """
    Plot the real, imaginary and absolute part of a sample.

    Parameters
    ----------
    sample : np.lib.npyio.NpzFile
        prepared sample
    norm : bool, optional
        normalization between 0 and 1, by default False
    """

    n_el = sample["config"].tolist()["n_el"]
    steps = len(sample["v_without_ext"]) / n_el

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(9, 9))
    ax1.set_title(r"Real signal part without excitation electrodes")
    ax1.set_ylabel(r"$\Re\{\phi\}$")
    ax2.set_title(r"Imaginary signal part without excitation electrodes")
    ax2.set_ylabel(r"$\Im\{\phi\}$")
    ax3.set_title(r"Absolute signal without excitation electrodes")
    ax3.set_ylabel(r"$|\phi|$")
    if norm is False:
        real = np.real(sample["v_without_ext"])
        imag = np.imag(sample["v_without_ext"])
        absol = np.abs(sample["v_without_ext"])
        ax1.stem(real)
        ax2.stem(imag)
        ax3.stem(absol)
        for el in range(n_el):
            ax1.fill_betweenx(
                (np.min(real), np.max(real)),
                el * (n_el - 2),
                (el + 1) * (n_el - 2),
                facecolor=f"C{el%2}",
                alpha=0.4,
                label=f"group {el+1}",
            )
            ax2.fill_betweenx(
                (np.min(imag), np.max(imag)),
                el * (n_el - 2),
                (el + 1) * (n_el - 2),
                facecolor=f"C{el%2}",
                alpha=0.4,
                label=f"group {el+1}",
            )
            ax3.fill_betweenx(
                (0, np.max(absol)),
                el * (n_el - 2),
                (el + 1) * (n_el - 2),
                facecolor=f"C{el%2}",
                alpha=0.4,
                label=f"group {el+1}",
            )
        # ax1.legend(bbox_to_anchor=(1.1, 1.05))
    if norm is True:
        ax1.stem(norm_data(np.real(sample["v_without_ext"])))
        ax2.stem(norm_data(np.imag(sample["v_without_ext"])))
        ax3.stem(norm_data(np.abs(sample["v_without_ext"])))
        for el in range(n_el):
            ax1.fill_betweenx(
                (0, 1),
                el * steps,
                (el + 1) * steps,
                facecolor=f"C{el%2}",
                alpha=0.4,
                label=f"group {el+1}",
            )
            ax2.fill_betweenx(
                (0, 1),
                el * steps,
                (el + 1) * steps,
                facecolor=f"C{el%2}",
                alpha=0.4,
                label=f"group {el+1}",
            )
            ax3.fill_betweenx(
                (0, 1),
                el * steps,
                (el + 1) * steps,
                facecolor=f"C{el%2}",
                alpha=0.4,
                label=f"group {el+1}",
            )
    fig.tight_layout()
    plt.show()


def plot_completeness(lpath: str) -> None:
    """
    plot_completeness shows the existing measurement points inside a directory

    Parameters
    ----------
    lpath : str
        target load directory
    """
    r = []
    phi = []

    r_empty = []
    phi_empty = []

    decide_mode_sample = np.load(lpath + os.listdir(lpath)[0], allow_pickle=True)
    if decide_mode_sample.files[0] == "config":
        for ele in np.sort(os.listdir(lpath))[
            :: decide_mode_sample["config"].tolist().burst_count
        ]:
            tmp = np.load(lpath + ele, allow_pickle=True)
            r_c, phi_c = comp_tank_relative_r_phi(tmp)
            if len(tmp["data"]) == 0:
                r_empty.append(r_c)
                phi_empty.append(math.radians(phi_c))
            else:
                r.append(r_c)
                phi.append(math.radians(phi_c))

        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(projection="polar", polar=True)
        ax.scatter(phi, r, c="green", s=20, alpha=1, label="existing points")
        if len(r_empty) != 0:
            ax.scatter(
                phi_empty,
                r_empty,
                c="red",
                s=20,
                alpha=1,
                label="missing points",
            )
        plt.title("Raw data")
        ax.legend()
        plt.tight_layout()
        print(f"\tMissing points:{len(phi_empty)}")

    if decide_mode_sample.files[0] == "potential_matrix":
        for ele in np.sort(os.listdir(lpath))[
            :: decide_mode_sample["config"].tolist()["burst_count"]
        ]:
            tmp = np.load(lpath + ele, allow_pickle=True)
            r.append(tmp["r_phi"][0])
            phi.append(math.radians(tmp["r_phi"][1]))

        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot(projection="polar", polar=True)
        ax.scatter(phi, r, c="green", s=20, alpha=1, label="existing points")
        plt.title("ML preperated measurements.")
        ax.legend()
        plt.tight_layout()


def plot_temperatur_curve(
    lpath: str,
) -> Tuple[np.ndarray, float, float, float]:
    """
    plot_temperatur_curve _summary_
    Parameters
    ----------
    lpath : str
        path to measurement directory
    Returns
    -------
    Tuple[np.ndarray, float, float, float]
        temperatures, mean(t), std(t), max(t)-min(t)
    """

    temperature = []
    date = []
    time = []
    decide_skip = np.load(lpath + os.listdir(lpath)[0], allow_pickle=True)

    if decide_skip.files[0] == "config":
        for ele in np.sort(os.listdir(lpath))[
            :: decide_skip["config"].tolist().burst_count
        ]:
            tmp = np.load(lpath + ele, allow_pickle=True)
            temperature.append(tmp["config"].tolist().temperature)
            date.append(tmp["config"].tolist().datetime.split(" ")[0])
            time.append(tmp["config"].tolist().datetime.split(" ")[1][:-3])
    else:
        print("Please insert the lpath of the original measurement directory.")

    date = np.array(date)
    time = np.array(time)
    dt_string = str(np.unique(date))

    temperature = np.array(temperature)
    mean_t = np.mean(temperature)
    std_dev = np.std(temperature)
    max_min_diff = np.max(temperature) - np.min(temperature)

    plt.figure(figsize=(8, 4))
    # enable with new data
    plt.title(f"{lpath.split('/')[-2:-1][0]}, {dt_string[2:-2]}")
    plt.grid()
    plt.plot(temperature)
    plt.ylabel("temperature °C")
    plt.xticks(
        ticks=np.arange(len(time))[:: len(time) // 8],
        labels=time[:: len(time) // 8],
    )
    plt.xlabel("time HH:MM")
    plt.show()

    print(f"mean temperature:\t {mean_t}")
    print(f"standart deviation:\t {std_dev}")
    print(f"max(t)-min(t):\t {max_min_diff}")
    return temperature, mean_t, std_dev, max_min_diff
