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
- **Outputs dhe Figurët:**  

### Tail Probability vs N
- **File:** `outputs/tail_vs_n_log.png`  
- **Përshkrimi:** ## Figura e Analizuar: $\mathbf{P(X > 10) \text{ vs } N \text{ for different } p}$

Kjo figurë, e gjeneruar nga funksioni `plot_tail_vs_n`, është thelbi i vlerësimit të **skalabilitetit** dhe **menaxhimit të rrezikut** në Packet Switching (PS). Ajo krahason sesa shpejt rritet rreziku i konjestionit $P(X > 10)$ ndërsa rritet numri i përdoruesve ($N$), për pesë skenarë të ndryshëm të sjelljes së përdoruesit ($p$).

---

## 1. Kuptimi i Boshteve dhe Shkallës Logaritmike

| Elementi | Përshkrimi Akademik | Kuptimi Inxhinierik |
| :--- | :--- | :--- |
| **Boshti X ($N$)** | Numri i Provave Binomiale (Përdoruesit Totalë) | Tregon numrin e përdoruesve që tentojmë t'i mbajmë në rrjet. |
| **Boshti Y (Log Scale)** | Probabiliteti i Mbetur (Tail Probability): $\mathbf{P(X > 10)}$ | Mat rrezikun e **Dështimit të QoS** (Konjestionit). Vlera $10^{-3}$ shpesh shërben si kufi i pranueshëm. |
| **$N$ nga 1 deri në 10** | **Zona e Dështimit Të PS:** $\mathbf{P(X > 10) = 0}$ | Kjo zonë është deterministike, pasi është e pamundur që më shumë se $N$ përdorues të jenë aktivë. Linjat fillojnë nga $N=11$. |

---

## 2. Analiza Detajuar e Kurbave dhe Skalabiliteti

Çdo kurbë tregon efikasitetin e PS në varësi të natyrës së trafikut ($p$). Kujtojmë se rasti i studimit është $p=0.1$ (kurba portokalli).

### A. Kurbat me Rrezik të Lartë ($\mathbf{p=0.2}$ dhe $\mathbf{p=0.3}$)

* **Përshkrimi:** Kurbat vjollcë dhe e kuqe tregojnë një rritje **shumë të shpejtë** të rrezikut, pothuajse vertikale, menjëherë pas $N=20$.  
* **Implikimi Inxhinierik:** Mesatarja e përdoruesve aktivë ($N \cdot p$) arrin kapacitetin 10 shumë shpejt (p.sh., në $N=34$ për $p=0.3$), dhe sistemi bëhet i mbingarkuar me një numër minimal përdoruesish. Packet Switching është **joefikas** për këtë sjellje të trafikut.

### B. Kurba e Rastit të Studimit ($\mathbf{p=0.1}$)

* **Përshkrimi (Kurba Portokalli):** Rritet shumë më gradualisht dhe kalon kufirin $\mathbf{10^{-3}}$ (QoS i pranueshëm) rreth $\mathbf{N \approx 55}$.  
* **Pika Kryesore ($N=35$):** Bie në zonën midis $10^{-4}$ dhe $10^{-5}$ në grafik, duke konfirmuar vlerën e llogaritur $0.0004$ dhe duke justifikuar **fitimin 3.5 herë të kapacitetit**.  
* **Konkluzioni:** Për trafikun tipik të internetit ($p=0.1$), PS ofron efikasitet maksimal, por duhet të menaxhohet me kujdes nga inxhinieri (të mos kalojë $N \approx 55$).

### C. Kurba me Rrezik Minimal ($\mathbf{p=0.01}$ - Vija Blu)

* **Përshkrimi:** Rritet shumë ngadalë. Për $\mathbf{N=200}$, rreziku mbetet në një nivel jashtëzakonisht të ulët ($\approx 10^{-5}$).  
* **Konkluzioni:** Kjo demonstron fuqinë maksimale të Packet Switching. Kur përdoruesit janë shumë pasivë, sistemi mund të pranojë $\mathbf{20 \text{ herë më shumë }}$ përdorues se Circuit Switching, sepse probabiliteti që ata të aktivizohen njëkohësisht është i papërfillshëm.

---

## 3. Përfundimi Strategjik

Ky grafik konfirmon dy parime themelore të rrjeteve:

1. **Rritja Eksponenciale e Rrezikut:** Sapo sistemi i Komutimit të Paketave fillon të funksionojë në mënyrë jo-ideale (duke kaluar mesataren $N \cdot p \approx 5$), çdo përdorues i ri shton një rrezik relativisht më të madh se i mëparshmi, duke çuar në rritjen e shpejtë dhe të pakontrollueshme të $P(X > 10)$.  
2. **Varësia nga Statistikat:** Suksesi i PS është i varur drejtpërdrejt nga natyra e trafikut. Inxhinierët duhet të operojnë në **zonën vjollcë/blu** (trafik pasiv) dhe të shmangin zonën e lartë, ku PS nuk arrin të ofrojë QoS të pranueshme.
 
- **Figura:**
![Tail Probability vs N](outputs/tail_vs_n_log.png)

### PMF për N të ndryshme
- **N=10:** `outputs/pmf_n_10.png` — PMF e N=10, **P(X>10)=0**, skenar ideal për packet-switching  
![PMF N=10](outputs/pmf_n_10.png)

- **N=35:** `outputs/pmf_n_35.png` — Bishti i kuq minimal, **P(X>10)=4.24e-4**  
![PMF N=35](outputs/pmf_n_35.png)

- **N=50:** `outputs/pmf_n_50.png` — P(X>10)=9.36e-3, rreziku rritet lehtësisht  
![PMF N=50](outputs/pmf_n_50.png)

- **N=100:** `outputs/pmf_n_100.png` — P(X>10)=0.417, rrezik i konsiderueshëm për packet-switching  
![PMF N=100](outputs/pmf_n_100.png)

### Heatmap
- **File:** `outputs/heatmap.png` — Heatmap 2D P(X>10) mbi N=1..200 dhe p=0.01..0.3  
- **Interpretimi:** Zona blu: probabilitet i ulët, zona e verdhë/purpuri: probabilitet i lartë. Tregon kufirin e sigurt për dimensionimin e rrjetit.  
![Heatmap](outputs/heatmap.png)

---

## Tabela verfikuese

- Krahasim teorik vs Monte Carlo vs normal approximation për N=[35,50,100], p=0.1:

| N   | Theoretical | Monte Carlo | Normal Approx |
|-----|------------|------------|---------------|
| 35  | 0.000424   | 0.000425   | 0.0000405     |
| 50  | 0.009355   | 0.009585   | 0.004761      |
| 100 | 0.416844   | 0.415705   | 0.433816      |

---

## Metodologjia

**Veglat e përdorura:**  
- Python 3.12.3  
- NumPy: Llogaritje numerike dhe gjenerim numrash të rastësishëm  
- Pandas: Menaxhim i të dhënave dhe eksport në CSV  
- SciPy: Shpërndarje binomiale dhe normale  
- Matplotlib: Vizualizim, ruajtje PNG dhe PDF  
- OS & Time: Menaxhim direktorish dhe matja e kohës së ekzekutimit  

**Hapat e Implementimit:**  
1. Caktimi i parametrave kryesorë: `LINK_CAPACITY_MBPS=1000`, `USER_RATE_MBPS=100`, `THRESHOLD_USERS=10`, `DEFAULT_P=0.1`  
2. Funksionet utility: `circuit_switching_capacity`, `binomial_pmf`, `binomial_tail_prob`, `normal_approx_tail`, `monte_carlo_tail`  
3. Analizat e larta: `compute_tail_for_range`, `varied_p_analysis`  
4. Gjenerimi i grafikëve: `plot_tail_vs_n`, `plot_pmf_for_n`, `plot_heatmap`  
5. Verifikimi: `verify_theoretical_vs_montecarlo`  
6. Ruajtja e rezultateve: CSV, PNG, PDF  

---

## Përfundimet

- **Packet-switching** është superior për rrjete me aktivitet të ulët (p<0.1), duke lejuar më shumë përdorues se circuit-switching me probabilitet mbingarkese <1%.  
- Për **p>0.2** ose N të mëdha, rreziku rritet ndjeshëm.  
- Verifikimi tregon se modeli binomial është i besueshëm (devijim <1% nga Monte Carlo).  
- Analizat vizuale (PMF, tail vs N, heatmap) ilustrojnë kufijtë dhe avantazhet e secilës paradigmë.





