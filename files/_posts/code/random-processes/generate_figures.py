"""Generate figures for the 'Random Processes' blog post.

Outputs PNGs to images/random_processes/ at the repository root.
Run with a Python environment that has matplotlib and numpy installed:

    python generate_figures.py
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Ellipse, FancyArrowPatch

REPO_ROOT = Path(__file__).resolve().parents[4]
OUT_DIR = REPO_ROOT / "images" / "random_processes"
OUT_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams.update(
    {
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
        "font.size": 12,
        "axes.titlesize": 13,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "savefig.dpi": 150,
        "savefig.bbox": "tight",
    }
)

BLUE = "#1f6feb"
CRIMSON = "#c0392b"
GOLD = "#e1a92a"
GREY = "#9aa0a6"


def save(fig, name):
    path = OUT_DIR / name
    fig.savefig(path)
    plt.close(fig)
    print(f"wrote {path}")


def fig_rv_mapping():
    """A random variable as a function from outcomes to numbers."""
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

    # Sample space (domain)
    ax.add_patch(
        Ellipse((2, 3), 3.0, 4.4, facecolor="#eaf1fb", edgecolor=BLUE, lw=2)
    )
    ax.text(2, 5.4, "Sample space  $\\Omega$", ha="center", va="center",
            fontsize=13, color=BLUE)
    ax.text(2, 4.65, "(the outcomes)", ha="center", va="center",
            fontsize=10, color=BLUE)
    for label, y in [("H", 3.8), ("T", 2.1)]:
        ax.plot(2, y, "o", color=BLUE, ms=9)
        ax.text(1.55, y, label, ha="right", va="center", fontsize=13,
                fontweight="bold")

    # Real number line (range)
    ax.annotate("", xy=(9.7, 3), xytext=(6.2, 3),
                arrowprops=dict(arrowstyle="-|>", color="black", lw=1.5))
    ax.text(9.75, 3, "$\\mathbb{R}$", ha="left", va="center", fontsize=13)
    for val, x in [(0, 7.2), (1, 8.7)]:
        ax.plot([x, x], [2.9, 3.1], color="black", lw=1.5)
        ax.plot(x, 3, "o", color=CRIMSON, ms=8)
        ax.text(x, 2.55, str(val), ha="center", va="center", fontsize=12)
    ax.text(7.95, 3.75, "the values $X$ can take", ha="center", va="center",
            fontsize=10, color=CRIMSON)

    # Mapping arrows H -> 1, T -> 0
    ax.add_patch(FancyArrowPatch((2.6, 3.8), (8.6, 3.08),
                 connectionstyle="arc3,rad=-0.18",
                 arrowstyle="-|>", mutation_scale=16, color="#444"))
    ax.add_patch(FancyArrowPatch((2.6, 2.1), (7.1, 2.92),
                 connectionstyle="arc3,rad=0.18",
                 arrowstyle="-|>", mutation_scale=16, color="#444"))
    ax.text(5.3, 3.95, "$X$", fontsize=15, style="italic", color="#444")
    ax.text(5.0, 4.55, "$X(H)=1,\\quad X(T)=0$", ha="center", fontsize=12)

    ax.set_title("A random variable is a rule that maps each outcome to a number",
                 pad=12)
    save(fig, "rv_mapping.png")


def fig_ensemble():
    """Many realizations of a random process over an index set."""
    rng = np.random.default_rng(7)
    t = np.linspace(0, 10, 400)
    dt = t[1] - t[0]
    n_paths = 6
    paths = np.zeros((n_paths, t.size))
    for i in range(n_paths):
        steps = rng.normal(0, np.sqrt(dt), t.size)
        paths[i] = np.cumsum(steps)

    fig, ax = plt.subplots(figsize=(8, 4.6))
    for i in range(1, n_paths):
        ax.plot(t, paths[i], color=GREY, lw=1.2, alpha=0.8)
    ax.plot(t, paths[0], color=CRIMSON, lw=2.4, label="one realization")

    t0 = 6.5
    k = int(np.argmin(np.abs(t - t0)))
    ax.axvline(t0, color=BLUE, ls="--", lw=1.4)
    ax.plot(np.full(n_paths, t0), paths[:, k], "o", color="black", ms=6, zorder=5)
    ax.annotate(
        "$X(t_0)$: a random variable\n(its value differs across realizations)",
        xy=(t0, paths[:, k].max()),
        xytext=(2.4, paths[:, k].max() + 1.6),
        fontsize=10.5, color=BLUE, ha="center",
        arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.2),
    )

    ax.set_xlabel("index  $t$  (e.g., time)")
    ax.set_ylabel("$X(t)$")
    ax.set_title("A random process: a whole family of realizations over an index set")
    ax.legend(loc="lower left", frameon=False)
    save(fig, "ensemble_sample_paths.png")


def fig_imu_noise():
    """Accelerometer reading at constant velocity: noise around zero."""
    rng = np.random.default_rng(1)
    t = np.linspace(0, 5, 600)
    ax_signal = rng.normal(0, 0.05, t.size)

    fig, ax = plt.subplots(figsize=(8, 3.6))
    ax.plot(t, ax_signal, color=BLUE, lw=1.0)
    ax.axhline(0, color=CRIMSON, ls="--", lw=1.6, label="true value $= 0$")
    ax.set_xlabel("time  $t$  (s)")
    ax.set_ylabel("$a_x(t)$  (m/s$^2$)")
    ax.set_title("Accelerometer at constant velocity: measured $a_x(t)$ is noise about zero")
    ax.legend(loc="upper right", frameon=False)
    save(fig, "imu_noise.png")


def fig_stock_price():
    """Daily stock price as one realization of a random process."""
    rng = np.random.default_rng(42)
    days = np.arange(0, 251)
    returns = rng.normal(0.0004, 0.011, days.size)
    price = 100 * np.cumprod(1 + returns)

    fig, ax = plt.subplots(figsize=(8, 3.8))
    ax.plot(days, price, color=BLUE, lw=1.4)
    ax.set_xlabel("Day")
    ax.set_ylabel("Price")
    ax.set_title("Daily stock price: one realization of a random process")
    save(fig, "stock_price.png")


def fig_spatial_coins():
    """A coin flip at each of four locations (spatial indexing)."""
    outcomes = ["H", "T", "H", "H"]
    fig, ax = plt.subplots(figsize=(8, 2.9))
    ax.set_xlim(0.3, 4.7)
    ax.set_ylim(0, 2.2)
    ax.set_aspect("equal")
    ax.axis("off")

    ax.annotate("", xy=(4.75, 0.55), xytext=(0.25, 0.55),
                arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.3))
    ax.text(0.10, 0.35, "location", ha="left", va="center", color=GREY, fontsize=10)

    for i, out in enumerate(outcomes, start=1):
        ax.add_patch(Circle((i, 1.3), 0.34, facecolor=GOLD, edgecolor="#8a6d19", lw=1.6))
        ax.text(i, 1.3, out, ha="center", va="center", fontsize=15, fontweight="bold",
                color="#3a2e08")
        ax.plot([i, i], [0.5, 0.6], color=GREY, lw=1.3)
        ax.text(i, 0.32, f"$t={i}$", ha="center", va="center", fontsize=12)

    ax.set_title("Spatial indexing: an independent coin flip at each location "
                 "$T=\\{1,2,3,4\\}$", pad=10)
    save(fig, "spatial_coins.png")


def fig_discrete_vs_continuous():
    """Discrete RV (PMF) beside a continuous RV (PDF)."""
    fig, (axl, axr) = plt.subplots(1, 2, figsize=(9, 3.8))

    # Discrete: coin
    axl.bar([0, 1], [0.5, 0.5], width=0.3, color=BLUE, edgecolor="black")
    axl.set_xticks([0, 1])
    axl.set_ylim(0, 0.62)
    axl.set_xlabel("value  $x$")
    axl.set_ylabel("probability  $P(X=x)$")
    axl.set_title("Discrete RV (coin): PMF")
    for x in (0, 1):
        axl.text(x, 0.52, "0.5", ha="center", fontsize=11)

    # Continuous: a height-like distribution on (0, inf)
    x = np.linspace(140, 200, 400)
    mu, sigma = 170, 8
    pdf = np.exp(-0.5 * ((x - mu) / sigma) ** 2) / (sigma * np.sqrt(2 * np.pi))
    axr.plot(x, pdf, color=CRIMSON, lw=2)
    mask = (x >= 165) & (x <= 180)
    axr.fill_between(x[mask], pdf[mask], color=CRIMSON, alpha=0.2)
    axr.set_ylim(0, 0.066)
    axr.set_xlabel("value  $x$  (e.g., height in cm)")
    axr.set_ylabel("density  $f(x)$")
    axr.set_title("Continuous RV (height): PDF")
    axr.annotate("area = $P(165 \\leq X \\leq 180)$", xy=(172, 0.016),
                 xytext=(142, 0.060), fontsize=10, color=CRIMSON, ha="left",
                 arrowprops=dict(arrowstyle="-|>", color=CRIMSON, lw=1.1))

    fig.suptitle("Two kinds of random variable", y=1.02, fontsize=13)
    save(fig, "discrete_vs_continuous.png")


def main():
    fig_rv_mapping()
    fig_ensemble()
    fig_imu_noise()
    fig_stock_price()
    fig_spatial_coins()
    fig_discrete_vs_continuous()
    print(f"\nAll figures written to {OUT_DIR}")


if __name__ == "__main__":
    main()
