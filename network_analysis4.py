# packet_vs_circuit_improved.py
import os
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import binom, norm
from matplotlib.backends.backend_pdf import PdfPages

# ---------- Settings ----------
LINK_CAPACITY_MBPS = 1000
USER_RATE_MBPS = 100
THRESHOLD_USERS = LINK_CAPACITY_MBPS // USER_RATE_MBPS  # = 10
DEFAULT_P = 0.1

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------- Utility functions ----------
def circuit_switching_capacity(link_capacity=LINK_CAPACITY_MBPS, user_rate=USER_RATE_MBPS):
    """Deterministic capacity for circuit switching (integer)."""
    return link_capacity // user_rate

def binomial_pmf(n, k, p=DEFAULT_P):
    """Stable PMF via scipy.stats.binom."""
    return binom.pmf(k, n, p)

def binomial_tail_prob(n, k_threshold, p=DEFAULT_P):
    """P(X > k_threshold) for X ~ Binomial(n,p)."""
    if n <= k_threshold:
        return 0.0
    # cdf(k) = P(X <= k), so 1 - cdf(k) = P(X > k)
    return 1.0 - binom.cdf(k_threshold, n, p)

def normal_approx_tail(n, k_threshold, p=DEFAULT_P):
    """Continuity-corrected normal approximation for P(X > k_threshold)."""
    mu = n * p
    sigma = np.sqrt(n * p * (1-p))
    if sigma == 0:
        return 0.0 if mu <= k_threshold else 1.0
    # continuity correction: P(X > k) ≈ 1 - Phi((k + 0.5 - mu)/sigma)
    z = (k_threshold + 0.5 - mu) / sigma
    return 1.0 - norm.cdf(z)

def monte_carlo_tail(n, k_threshold, p=DEFAULT_P, trials=100_000, rng=None):
    """Monte Carlo estimate of P(X > k_threshold)."""
    if rng is None:
        rng = np.random.default_rng()
    samples = rng.binomial(n, p, size=trials)
    return float(np.mean(samples > k_threshold))

# ---------- High level analyses ----------
def compute_tail_for_range(max_n=200, p=DEFAULT_P):
    """Compute P(X > THRESHOLD_USERS) for n=1..max_n."""
    ns = np.arange(1, max_n+1)
    tails = np.array([binomial_tail_prob(n, THRESHOLD_USERS, p) for n in ns])
    return ns, tails

def varied_p_analysis(max_n=200, p_values=None):
    """Compute tail probabilities for multiple p values."""
    if p_values is None:
        p_values = [0.01, 0.05, 0.1, 0.2, 0.3]
    results = {}
    for p in p_values:
        ns, tails = compute_tail_for_range(max_n=max_n, p=p)
        results[p] = (ns, tails)
    return results

# ---------- Plots & verification ----------
def plot_tail_vs_n(results_dict, log_y=True, fname=None):
    """Plot P(X>threshold) vs N for multiple p curves."""
    plt.figure(figsize=(10,6))
    for p, (ns, tails) in results_dict.items():
        plt.plot(ns, tails, label=f"p={p}")
    if log_y:
        plt.yscale('log')
        plt.ylabel(f"P(X > {THRESHOLD_USERS}) (log scale)")
    else:
        plt.ylabel(f"P(X > {THRESHOLD_USERS})")
    plt.xlabel("N (number of users)")
    plt.title(f"P(X > {THRESHOLD_USERS}) vs N for different p")
    plt.grid(True)
    plt.legend()
    if fname:
        plt.savefig(fname, dpi=200)
    plt.show()

def plot_pmf_for_n(n, p=DEFAULT_P, fname=None):
    """Plot PMF for a given n and highlight congestion region."""
    ks = np.arange(0, n+1)
    pmf = binom.pmf(ks, n, p)
    plt.figure(figsize=(10,5))
    plt.bar(ks, pmf, color='skyblue', label='P(X=k)')
    plt.bar(ks[THRESHOLD_USERS+1:], pmf[THRESHOLD_USERS+1:], color='red', label='Congestion (k>10)')
    plt.axvline(THRESHOLD_USERS, color='k', linestyle='--', label=f"Threshold = {THRESHOLD_USERS}")
    plt.xlim(0, min(n, THRESHOLD_USERS + 25))
    plt.xlabel("k = # active users")
    plt.ylabel("P(X=k)")
    plt.title(f"Binomial PMF n={n}, p={p:.3f}  --  P(X>{THRESHOLD_USERS}) = {binomial_tail_prob(n, THRESHOLD_USERS, p):.6e}")
    plt.legend()
    plt.grid(alpha=0.3)
    if fname:
        plt.savefig(fname, dpi=200)
    plt.show()

def plot_heatmap(p_min=0.01, p_max=0.3, p_steps=30, n_max=200, fname=None):
    """Heatmap of P(X>threshold) for grid of (N,p)."""
    p_grid = np.linspace(p_min, p_max, p_steps)
    n_grid = np.arange(1, n_max+1)
    H = np.zeros((len(p_grid), len(n_grid)))
    for i, p in enumerate(p_grid):
        for j, n in enumerate(n_grid):
            H[i,j] = binomial_tail_prob(n, THRESHOLD_USERS, p)
    plt.figure(figsize=(12,5))
    im = plt.imshow(H, origin='lower', aspect='auto',
                    extent=[n_grid[0], n_grid[-1], p_grid[0], p_grid[-1]],
                    cmap='viridis')
    plt.colorbar(im, label=f"P(X > {THRESHOLD_USERS})")
    plt.xlabel("N (number of users)")
    plt.ylabel("p (activity prob)")
    plt.title(f"Heatmap of P(X>{THRESHOLD_USERS}) over (N,p)")
    if fname:
        plt.savefig(fname, dpi=200)
    plt.show()
    return p_grid, n_grid, H

# ---------- Verification and report ----------
def verify_theoretical_vs_montecarlo(selected_ns=[35,50,100], p=DEFAULT_P, trials=200_000):
    rng = np.random.default_rng(12345)
    rows = []
    for n in selected_ns:
        theo = binomial_tail_prob(n, THRESHOLD_USERS, p)
        mc = monte_carlo_tail(n, THRESHOLD_USERS, p, trials=trials, rng=rng)
        approx = normal_approx_tail(n, THRESHOLD_USERS, p)
        rows.append({'N': n, 'theoretical': theo, 'monte_carlo': mc, 'normal_approx': approx})
    df = pd.DataFrame(rows).set_index('N')
    return df

# ---------- Main: orchestration ----------
def main():
    start = time.time()
    print("Starting advanced analysis...")

    # 1) compute tails for default p and multiples
    p_values = [0.01, 0.05, 0.1, 0.2, 0.3]
    results = varied_p_analysis(max_n=200, p_values=p_values)

    # 2) save multi-curve plot (log)
    plot_tail_vs_n(results, log_y=True, fname=os.path.join(OUTPUT_DIR, "tail_vs_n_log.png"))

    # 3) pmfs for chosen Ns
    for n in [10, 35, 50, 100]:
        plot_pmf_for_n(n, p=DEFAULT_P, fname=os.path.join(OUTPUT_DIR, f"pmf_n_{n}.png"))

    # 4) heatmap
    plot_heatmap(fname=os.path.join(OUTPUT_DIR, "heatmap.png"))

    # 5) Monte Carlo verification (selected Ns)
    df_verify = verify_theoretical_vs_montecarlo([35,50,100], p=DEFAULT_P, trials=200_000)
    print("\nTheoretical vs Monte Carlo vs Normal-approximation:\n", df_verify)

    # 6) Save summary CSV
    summary_csv = os.path.join(OUTPUT_DIR, "tail_summary.csv")
    all_ns = np.arange(1,201)
    df_all = pd.DataFrame({
        'N': all_ns,
        'P_tail_p=0.01': [binomial_tail_prob(n, THRESHOLD_USERS, p=0.01) for n in all_ns],
        'P_tail_p=0.05': [binomial_tail_prob(n, THRESHOLD_USERS, p=0.05) for n in all_ns],
        'P_tail_p=0.1': [binomial_tail_prob(n, THRESHOLD_USERS, p=0.1) for n in all_ns],
        'P_tail_p=0.2': [binomial_tail_prob(n, THRESHOLD_USERS, p=0.2) for n in all_ns],
        'P_tail_p=0.3': [binomial_tail_prob(n, THRESHOLD_USERS, p=0.3) for n in all_ns],
    })
    df_all.to_csv(summary_csv, index=False)
    print(f"Saved table: {summary_csv}")

    # 7) Create a simple PDF report with key figures (optional)
    pdf_path = os.path.join(OUTPUT_DIR, "packet_vs_circuit_report_basic.pdf")
    with PdfPages(pdf_path) as pdf:
        # title page
        plt.figure(figsize=(11,8.5)); plt.axis('off')
        plt.text(0.5, 0.6, "Packet vs Circuit Switching\nAdvanced Analysis", ha='center', fontsize=20)
        plt.text(0.5, 0.45, f"Threshold users = {THRESHOLD_USERS}, user rate {USER_RATE_MBPS} Mbps, link {LINK_CAPACITY_MBPS} Mbps\nDefault p = {DEFAULT_P}", ha='center')
        pdf.savefig(); plt.close()
        # include saved PNGs
        for fname in ["tail_vs_n_log.png","pmf_n_35.png","pmf_n_50.png","pmf_n_100.png","heatmap.png"]:
            path = os.path.join(OUTPUT_DIR, fname)
            if os.path.exists(path):
                img = plt.imread(path)
                plt.figure(figsize=(11,8.5)); plt.imshow(img); plt.axis('off'); pdf.savefig(); plt.close()
    print(f"Saved basic PDF report: {pdf_path}")

    end = time.time()
    print(f"Done in {end-start:.1f}s. Outputs in folder: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
