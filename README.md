project:
  name: "Packet vs Circuit Switching Analysis"
  author: "Albena Veseli"
  date: "17-10-2025"
  version: "1.0"
  description: >
    Ky projekt akademik trajton krahasimin mes dy paradigmave kryesore të rrjetëzimit –
    packet-switching (ku të dhënat ndahen në paketa të pavarura dhe transmetohen në mënyrë asinkrone)
    dhe circuit-switching (ku krijohet një qark i dedikuar për çdo sesion komunikimi). Projektimi
    përdor shpërndarjen binomiale për të simuluar aktivitetin e rastësishëm të përdoruesve dhe
    përllogarit probabilitetin e mbingarkesës P(X > k).

objectives:
  main_goal: >
    Demonstrohet se packet-switching ofron efikasitet më të lartë se circuit-switching në skenarë
    me aktivitet të ulët (p.sh., p=0.1), por rrezikon mbingarkesë kur numri i përdoruesve (N) rritet.
  secondary_goals:
    - Analizë e tail probabilities për N=1..200 dhe vlera të ndryshme të probabilitetit p.
    - Krahasim mes rezultateve teorike, aproximimit normal dhe simulimeve Monte Carlo.
    - Gjenerimi i grafikëve dhe raporteve për interpretim akademik.

structure:
  main_script: "packet_vs_circuit_improved.py"
  outputs:
    - "tail_vs_n_log.png"
    - "pmf_n_10.png"
    - "pmf_n_35.png"
    - "pmf_n_50.png"
    - "pmf_n_100.png"
    - "heatmap.png"
    - "tail_summary.csv"
    - "packet_vs_circuit_report_basic.pdf"
  requirements: "Python 3.12.3, NumPy, Pandas, SciPy, Matplotlib"
  directories:
    - "outputs/"

methodology:
  tools_used:
    - Python 3.12.3
    - NumPy: "Llogaritje numerike dhe gjenerim numrash të rastësishëm"
    - Pandas: "Menaxhim i të dhënave dhe eksport në CSV"
    - SciPy: "Shpërndarje binomiale dhe normale"
    - Matplotlib: "Vizualizim, ruajtje PNG dhe PDF"
    - OS & Time: "Menaxhim direktorish dhe matja e kohës së ekzekutimit"
  implementation_steps:
    - Caktimi i parametrave kryesorë: LINK_CAPACITY_MBPS=1000, USER_RATE_MBPS=100, THRESHOLD_USERS=10, DEFAULT_P=0.1
    - Funksionet utility: circuit_switching_capacity, binomial_pmf, binomial_tail_prob, normal_approx_tail, monte_carlo_tail
    - Analizat e larta: compute_tail_for_range, varied_p_analysis
    - Gjenerimi grafikësh: plot_tail_vs_n, plot_pmf_for_n, plot_heatmap
    - Verifikimi: verify_theoretical_vs_montecarlo
    - Ruajtja e rezultateve: CSV, PNG, PDF

results:
  tail_probability_vs_n:
    file: "tail_vs_n_log.png"
    description: >
      Linja të P(X>10) për N=1..200 dhe p=[0.01,0.05,0.1,0.2,0.3]. Shkalla logaritmike y
      thekson probabilitetet e vogla. Për p të ulët, mbingarkesa pothuajse zero; për p të lartë,
      probabiliteti rritet ndjeshëm.
  pmf_figures:
    - file: "pmf_n_10.png"
      N: 10
      description: "PMF e N=10, P(X>10)=0, skenar ideal për packet-switching"
    - file: "pmf_n_35.png"
      N: 35
      description: "PMF e N=35, bishti i kuq minimal, P(X>10)=4.24e-4"
    - file: "pmf_n_50.png"
      N: 50
      description: "PMF e N=50, P(X>10)=9.36e-3, rreziku rritet lehtësisht"
    - file: "pmf_n_100.png"
      N: 100
      description: "PMF e N=100, P(X>10)=0.417, rrezik i konsiderueshëm për packet-switching"
  heatmap:
    file: "heatmap.png"
    description: >
      Heatmap 2D P(X>10) mbi N=1..200 dhe p=0.01..0.3. Zona blu: probabilitet i ulët, zona
      e verdhë/purpuri: probabilitet i lartë. Tregon kufirin e sigurt për dimensionimin e rrjetit.
  verification_table:
    description: >
      Krahasim teorik vs Monte Carlo vs normal approximation për N=[35,50,100], p=0.1.
    table:
      - N: 35
        theoretical: 0.000424
        monte_carlo: 0.000425
        normal_approx: 0.0000405
      - N: 50
        theoretical: 0.009355
        monte_carlo: 0.009585
        normal_approx: 0.004761
      - N: 100
        theoretical: 0.416844
        monte_carlo: 0.415705
        normal_approx: 0.433816

conclusions:
  summary: >
    Packet-switching është superior për rrjete me aktivitet të ulët (p<0.1), duke lejuar më shumë
    përdorues se circuit-switching me probabilitet mbingarkese <1%. Për p>0.2 ose N të mëdha,
    rreziku rritet ndjeshëm. Verifikimi tregon se modeli binomial është i besueshëm (devijim <1%
    nga Monte Carlo). Analizat vizuale (PMF, tail vs N, heatmap) ilustrojnë kufijtë dhe avantazhet
    e secilës paradigmë.
  future_work:
    - Integrimi i shpërndarjeve të tjera (Poisson)
    - Simulime në rrjete reale (p.sh., NS-3)
    - Mekanizma QoS dhe prioritizimi në rrjete me N të larta
