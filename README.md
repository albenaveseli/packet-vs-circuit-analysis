# Packet vs Circuit Switching Analysis

---

## Përshkrimi i Projektit

Ky projekt trajton krahasimin mes dy paradigmave kryesore të rrjetëzimit – **packet-switching** (ku të dhënat ndahen në paketa të pavarura dhe transmetohen në mënyrë asinkrone) dhe **circuit-switching** (ku krijohet një qark i dedikuar për çdo sesion komunikimi).  

Projektimi përdor **shpërndarjen binomiale** për të simuluar aktivitetin e rastësishëm të përdoruesve dhe përllogarit probabilitetin e mbingarkesës **P(X > k)**.

---

## Objektivat e Projektit

**Qëllimi Kryesor:**  
- Demonstrohet se packet-switching ofron efikasitet më të lartë se circuit-switching në skenarë me aktivitet të ulët (p.sh., p=0.1), por rrezikon mbingarkesë kur numri i përdoruesve (N) rritet.

**Qëllime Sekondare:**  
- Analizë e probabiliteteve të bishtit për N=1..200 dhe vlera të ndryshme të probabilitetit p.  
- Krahasim mes rezultateve teorike, aproximimit normal dhe simulimeve Monte Carlo.  
- Gjenerimi i grafikëve dhe raporteve për interpretim akademik.

---

## Struktura e Projektit

- **Main script:** `packet_vs_circuit_improved.py`  
- **Outputs dhe Figurat:**  
  - Tail Probability vs N: `outputs/tail_vs_n_log.png`  
  - PMF N=10: `outputs/pmf_n_10.png`  
  - PMF N=35: `outputs/pmf_n_35.png`  
  - PMF N=50: `outputs/pmf_n_50.png`  
  - PMF N=100: `outputs/pmf_n_100.png`  
  - Heatmap: `outputs/heatmap.png`  

---

## Tail Probability vs N

### Figura 1: $\mathbf{P(X > 10) \text{ vs } N \text{ for different } p}$

Kjo figurë tregon rritjen e probabilitetit të mbingarkesës $P(X>10)$ ndërsa rritet numri i përdoruesve ($N$) për pesë vlera të ndryshme të probabilitetit të aktivitetit ($p$).

![Tail Probability vs N](outputs/tail_vs_n_log.png)

**Analiza e Kurbave:**  
- **Rrezik i Lartë ($p=0.2, 0.3$):** Kurbat ngjyrë vjollcë/kuqe rriten shumë shpejt; sistemi bëhet i mbingarkuar me përdorues të pakët.  
- **Rasti Tipik ($p=0.1$):** Kurba portokalli rritet gradualisht; P(X>10) kalon $10^{-3}$ rreth $N \approx 55$. Për $N=35$, P≈0.0004 — PS fiton 3.5 herë kapacitet më shumë se Circuit Switching.  
- **Rrezik Minimal ($p=0.01$):** Vija blu ngadalë; për $N=200$, P≈10⁻⁵. PS mund të mbajë shumë përdorues aktivë pa rrezik.

> Ky grafik shërben si udhëzues për **planifikimin e kapacitetit**, duke treguar rrezikun për çdo $N$ dhe $p$.

---

## PMF - Analiza e Shpërndarjes Binomiale

### Figura 2: $\mathbf{Binomial \text{ PMF } n=10, p=0.100 \text{ -- } P(X > 10) = 0}$

Kjo figurë, e gjeneruar nga `plot_pmf_for_n(10)`, tregon PMF për $N=10$ përdorues totalë, që përputhet me kapacitetin e **Komutimit të Qarqeve (CS)**. Probabiliteti i konjestionit është teorikisht zero.

![PMF N=10](outputs/pmf_n_10.png)

**Analiza:**  
- **P(X > 10) = 0:** Numri i përdoruesve është i barabartë me kapacitetin, nuk mund të ketë mbingarkesë.  
- **Pritshmëria Matematike ($E[X]$):** $E[X] = N \cdot p = 10 \cdot 0.1 = 1$ aktiv, rreth 73% të kohës rrjeti është nën kapacitet.  
- **Konkluzioni:** CS rezervon të gjithë kapacitetin edhe kur përdoruesit janë të pakët, duke e bërë rrjetin joefikas.  

**Lidhja me PS:**  
- Me PS dhe $N=35$, $P(X>10)=0.000424$, duke treguar fitimin e kapacitetit dhe përdorimin më efikas të rrjetit.

---

### Figura 3: $\mathbf{Binomial \text{ PMF } n=35, p=0.100 \text{ -- } P(X > 10) = 4.242976e-04}$

Kjo figurë, e gjeneruar nga `plot_pmf_for_n(35)`, paraqet vlerësimin e probabilitetit të mbingarkesës kur rrjeti operon me 35 përdorues në Komutimin e Paketave (PS).

| Element | Vlera | Konkluzioni |
| :--- | :--- | :--- |
| **Numri Total ($N$)** | 35 | Numri total i përdoruesve në PS |
| **Probabiliteti ($p$)** | 0.100 | Probabiliteti që çdo përdorues është aktiv |
| **Threshold** | 10 | Kapaciteti maksimal i përdoruesve aktivë |
| **Probabiliteti i Konjestionit** | 4.242976e-04 | Konfirmon rrezikun shumë të ulët (≈0.0004) |

![PMF N=35](outputs/pmf_n_35.png)

**Analiza:**  
- **Pritshmëria ($E[X]$):** $E[X] = 35 \cdot 0.1 = 3.5$; shiritat blu tregojnë përdorim mesatar ~35% të kapacitetit.  
- **Kufiri i Rrezikut:** Threshold = 10; shiritat e kuq pothuajse nuk duken, duke treguar probabilitet shumë të ulët të mbingarkesës.  
- **Konkluzioni:** PS lejon 35 përdorues, 3.5 herë më shumë se CS, me probabilitet të pranueshëm të dështimit. Pikë optimale operative.

---

## PMF për N të tjera

- **N=50:** `outputs/pmf_n_50.png` — P(X>10)=9.36e-3, rreziku rritet lehtësisht  
![PMF N=50](outputs/pmf_n_50.png)

- **N=100:** `outputs/pmf_n_100.png` — P(X>10)=0.417, rrezik i konsiderueshëm për packet-switching  
![PMF N=100](outputs/pmf_n_100.png)

---

## Heatmap

- **File:** `outputs/heatmap.png` — Heatmap 2D P(X>10) mbi N=1..200 dhe p=0.01..0.3  
- **Interpretimi:** Zona blu: probabilitet i ulët, zona e verdhë/purpuri: probabilitet i lartë.  
![Heatmap](outputs/heatmap.png)

---

## Tabela Verifikuese

Krahasim teorik vs Monte Carlo vs normal approximation për N=[35,50,100], p=0.1:

| N   | Theoretical | Monte Carlo | Normal Approx |
|-----|------------|------------|---------------|
| 35  | 0.000424   | 0.000425   | 0.0000405     |
| 50  | 0.009355   | 0.009585   | 0.004761      |
| 100 | 0.416844   | 0.415705   | 0.433816      |

---

## Metodologjia

**Veglat e përdorura:**  
- Python 3.12.3, NumPy, Pandas, SciPy, Matplotlib, OS & Time  

**Hapat e Implementimit:**  
1. Parametrat kryesorë: `LINK_CAPACITY_MBPS=1000`, `USER_RATE_MBPS=100`, `THRESHOLD_USERS=10`, `DEFAULT_P=0.1`  
2. Funksionet utility: `circuit_switching_capacity`, `binomial_pmf`, `binomial_tail_prob`, `normal_approx_tail`, `monte_carlo_tail`  
3. Analizat: `compute_tail_for_range`, `varied_p_analysis`  
4. Gjenerimi grafikësh: `plot_tail_vs_n`, `plot_pmf_for_n`, `plot_heatmap`  
5. Verifikimi: `verify_theoretical_vs_montecarlo`  
6. Ruajtja e rezultateve: CSV, PNG, PDF  

---

## Përfundimet

- **Packet-switching** superior për rrjete me aktivitet të ulët (p<0.1), duke lejuar më shumë përdorues se circuit-switching me probabilitet mbingarkese <1%.  
- Për **p>0.2** ose N të mëdha, rreziku rritet ndjeshëm.  
- Verifikimi tregon se modeli binomial është i besueshëm (devijim <1% nga Monte Carlo).  
- Analizat vizuale (PMF, tail vs N, heatmap) ilustrojnë kufijtë dhe avantazhet e secilës paradigmë.
