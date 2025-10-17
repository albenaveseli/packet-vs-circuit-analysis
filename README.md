# Packet vs Circuit Switching Analysis

---

## Përshkrimi i Projektit

Ky projekt trajton krahasimin mes dy mënyrave kryesore të lidhjes dhe komunikimit në rrjetet kompjuterike – packet-switching, ku të dhënat ndahen në paketa të vogla dhe dërgohen në mënyrë të pavarur, dhe circuit-switching, ku për çdo sesion komunikimi krijohet një lidhje e dedikuar. 

Për të modeluar aktivitetin e rastësishëm të përdoruesve dhe për të kuptuar se kur rrjeti mund të mbingarkohet, përdoret shpërndarja binomiale, duke llogaritur probabilitetin **P(X > k)**.

---

## Objektivat e Projektit

**Qëllimi Kryesor:**  
- Demonstrohet se packet-switching ofron efikasitet më të lartë se circuit-switching në skenarë me aktivitet të ulët (p.sh., p=0.1), por rrezikon mbingarkesë kur numri i përdoruesve (N) rritet.

**Qëllime Sekondare:**  
- Analizë e probabiliteteve të ngjarjeve ekstreme (dmth probabiliteti që numri i përdoruesve aktivë tejkalon kapacitetin e rrjetit) për N=1..200 dhe vlera të ndryshme të probabilitetit p.  
- Krahasim që tregon se si rezultatet teorike përputhen me përafrimin e shpërndarjes normale dhe me rezultatet nga simulimet Monte Carlo  
- Gjenerimi i grafikëve dhe raporteve për interpretim.

---

## Struktura e Projektit

- **Kodi kryesor:** `network_analysis.py`  
- **Rezultatet dhe figurat**  
  - **Probabiliteti i mbingarkesës në funksion të N** `outputs/tail_vs_n_log.png`  
    *(Figura tregon se si probabiliteti që numri i përdoruesve aktivë tejkalon kapacitetin ndryshon me rritjen e N.)*  
  - **PMF N=10:** `outputs/pmf_n_10.png`  
    *(Kjo figurë tregon shpërndarjen e probabiliteteve për 10 përdorues, ku çdo shirit përfaqëson sa e mundshme është të ketë një numër të caktuar përdoruesish aktivë.)*  
  - **PMF N=35:** `outputs/pmf_n_35.png`  
    *(Kjo figurë tregon shpërndarjen e probabiliteteve për 35 përdorues, ku pjesa për k > 10 tregon rrezikun që rrjeti të përjetojë mbingarkesë.)*  
  - **PMF N=50:** `outputs/pmf_n_50.png`  
    *(Kjo figurë tregon shpërndarjen e probabiliteteve për 50 përdorues, ku duket se probabiliteti që numri i përdoruesve të tejkalojë kapacitetin rritet.)*  
  - **PMF N=100:** `outputs/pmf_n_100.png`  
    *(Kjo figurë tregon shpërndarjen e probabiliteteve për 100 përdorues; probabiliteti që numri i përdoruesve aktivë të tejkalojë 10 është rreth 41.7%, që tregon se rrjeti është pothuajse gjysmë i mbingarkuar.)*  
  - **Heatmap:** `outputs/heatmap.png`  
    *(Kjo hartë ngjyrash tregon probabilitetin P(X > 10) për N nga 1 deri në 200 dhe p nga 0.01 deri në 0.3, duke evidentuar zonat me rrezik të ulët dhe të lartë të mbingarkesës së rrjetit.)*  

---

## Probabiliteti i tejkalimit në varësi të N

### Figura 1: $\mathbf{P(X > 10) \text{ vs } N \text{ for different } p}$

Kjo figurë tregon rritjen e probabilitetit të mbingarkesës $P(X>10)$ ndërsa rritet numri i përdoruesve ($N$) për pesë vlera të ndryshme të probabilitetit të aktivitetit ($p$).

![Tail Probability vs N](outputs/tail_vs_n_log.png)

**Analiza e formave të grafikëve:**  
- **Rrezik i Lartë ($p=0.2, 0.3$):** Lakoret ngjyrë vjollcë/kuqe rriten shumë shpejt; sistemi bëhet i mbingarkuar me përdorues të pakët.  
- **Rasti Tipik ($p=0.1$):** Lakorja e gjelbër rritet gradualisht; Për $N=35$, $\text{P} \approx 0.0004$ — PS fiton 3.5 herë kapacitet më shumë se Circuit Switching.  
- **Rrezik Minimal ($p=0.01$):** Lakorja e kaltërt ngadalë; për $N=200$, P≈10⁻⁵. PS mund të mbajë shumë përdorues aktivë pa rrezik.

> Ky grafik shërben si udhëzues për **planifikimin e kapacitetit**, duke treguar rrezikun për çdo $N$ dhe $p$.

---

## PMF - Analiza e Shpërndarjes Binomiale

### Figura 2: $\mathbf{Binomial \text{ PMF } n=10, p=0.100 \text{ -- } P(X > 10) = 0}$

Kjo figurë, e gjeneruar nga `plot_pmf_for_n(10)`, tregon PMF për $N=10$ përdorues totalë, që përputhet me kapacitetin e **Komutimit të Qarqeve (CS)**. Probabiliteti i mbingarkesës është teorikisht zero.

![PMF N=10](outputs/pmf_n_10.png)

**Analiza:**  
- **P(X > 10) = 0:** Numri i përdoruesve është i barabartë me kapacitetin, nuk mund të ketë mbingarkesë.  
- **Pritshmëria Matematike ($E[X]$):** $E[X] = N \cdot p = 10 \cdot 0.1 = 1$ aktiv, rrjeti është gjithmonë nën kapacitet; përdorimi mesatar është 10%..  
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
| **Probabiliteti i mbingarkesës** | 4.242976e-04 | Konfirmon rrezikun shumë të ulët (≈0.0004) |

![PMF N=35](outputs/pmf_n_35.png)

**Analiza:**  
- **Pritshmëria ($E[X]$):** $E[X] = 35 \cdot 0.1 = 3.5$; shiritat blu tregojnë përdorim mesatar ~35% të kapacitetit.  
- **Kufiri i Rrezikut:** Threshold = 10; shiritat e kuq pothuajse nuk duken, duke treguar probabilitet shumë të ulët të mbingarkesës.  
- **Konkluzioni:** PS lejon 35 përdorues, 3.5 herë më shumë se CS, me probabilitet të pranueshëm të dështimit. Pikë optimale operative.

---

### Figura 4: $\mathbf{Binomial \text{ PMF } n=50, p=0.100 \text{ -- } P(X > 10) = 9.354602e-03}$

Kjo figurë, e gjeneruar nga `plot_pmf_for_n(50)`, vizualizon probabilitetin e mbingarkesës kur rrjeti ka $\mathbf{N=50}$ përdorues. Ky skenar është kritik sepse tregon pikën ku rreziku fillon të rritet ndjeshëm, duke iu afruar kufirit të tolerueshëm të Cilësisë së Shërbimit (QoS).

| Elementi | Vlera | Përshkrimi |
| :--- | :--- | :--- |
| **Numri Total ($N$)** | 50 | 5 herë më shumë përdorues se kapaciteti i CS (10) |
| **Pritshmëria ($E[X]$)** | $50 \cdot 0.1 = 5$ | Mesatarisht 5 nga 10 vendet e kapacitetit përdoren |
| **Prob. i Konjestionit** | 9.354602e-03 | Rreziku ≈0.00935 (rreth 9 në 1000 raste) |

**Analiza e Ndryshimeve (N=35 vs N=50):**  
- **Zhvendosja e Qendrës:** Krahasuar me $N=35$ ($E[X]=3.5$), qendra e shpërndarjes (shirat blu) zhvendoset djathtas, rreth $k=5$.  
- **Rritja e Zonës së Kuqe:** Kufiri $k_{\text{threshold}}=10$ mbetet i njëjtë; shiritat e kuq tani janë qartë të dukshëm, duke treguar rrezik më të lartë.  
- **Konkluzioni:** Rreziku i mbingarkesës është rritur 22 herë krahasuar me $N=35$, duke iu afruar kufirit të pranueshëm të shërbimit.

**Konkluzioni Inxhinierik:**  
- Për $N=50$, sistemi kalon kufirin e rrezikut të QoS (10⁻³).  
- PS ende ofron fitim kapaciteti 5 herë më shumë se CS, por me rrezik të rëndësishëm dështimi.  
- Kërkohet monitorim rigoroz i rrjetit për të siguruar QoS.

![PMF N=50](outputs/pmf_n_50.png)

---

### Figura 5: $\mathbf{Binomial \text{ PMF } n=100, p=0.100 \text{ -- } P(X > 10) = 4.168445e-01}$

Kjo figurë, e gjeneruar nga `plot_pmf_for_n(100)`, vizualizon skenarin ku Komutimi i Paketave (PS) është në kufirin e tij të dështimit.

![PMF N=100](outputs/pmf_n_100.png)

| Elementi | Vlera | Kuptimi |
| :--- | :--- | :--- |
| **Numri Total ($N$)** | 100 | 10 herë më shumë se kapaciteti i CS |
| **Pritshmëria ($E[X]$)** | 100 * 0.1 = 10 | Mesatarja e përdoruesve aktivë përputhet me kapacitetin |
| **Threshold** | 10 | Kapaciteti i lidhjes (vija e ndërprerë) |
| **Prob. i Konjestionit** | 0.4168445 | Mbingarkesa ndodh rreth 41.7% të kohës |

**Analiza:**  
- **Kufiri Kritik:** Vija e ndërprerë bie në qendër të shpërndarjes; pjesa blu ($P(X \le 10) \approx 58.3\%$) tregon funksionimin normal, pjesa e kuqe ($P(X > 10) \approx 41.7\%$) tregon mbingarkesën.  
- **Dështimi i QoS:** Pjesa e kuqe është e madhe dhe dominuese, rrjeti është pothuajse gjysmën e kohës i mbingarkuar.  
- **Konkluzioni:** PS nuk është më i përdorshëm në këtë skenar; QoS ka dështuar.

> Kjo figurë lidh vizualisht pikën e rrezikut të lartë në **Heatmap** dhe lakoren $p=0.1$ në grafikun logaritmik (Fig. 1).

---

## Heatmap

- **File:** `outputs/heatmap.png` — Heatmap 2D P(X>10) mbi N=1..200 dhe p=0.01..0.3  
- **Interpretimi:** Zona blu: probabilitet i ulët, zona verdhë/gjelbër e hapur: probabilitet i lartë.  
![Heatmap](outputs/heatmap.png)

**Analiza e Hartës së Nxehtësisë:**  
- **Zona e Mbingarkesës së Lartë (E Verdhë):** Përdorues të shumtë dhe aktivitet i lartë, probabiliteti i mbingarkesës afër 1.0.  
- **Zona e Mbingarkesës së Ulët (E Errët/Vjollcë):** Përdorues të pakët ose aktivitet i ulët, probabiliteti i mbingarkesës afër 0.  
- **Zona e Tranzicionit (E Gjelbër/Blu):** Numri i përdoruesve i pranueshëm me probabilitet aktiviteti të ulët; p.sh., $p\approx0.1$ dhe $N=35$–$50$ përdorues, probabiliteti mbingarkesë i kontrolluar (<0.01).  

> Harta e nxehtësisë demonstron qartë **"fitimin"** e Paket-Switching mbi Circuit-Switching, duke ilustruar kapacitetin statistikisht të pranueshëm.

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









