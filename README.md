# MMWD

Projekt na zaliczenie zajęć z Matematycznych Metod Wspomagania Decyzji.  

Autorzy:
* Aleksander Nagaj
* Jan Nęciński
* Przemysław Myśliwiec

## Użycie

Program przyjmuje plik z parametrami wejściowymi w formacie JSON
```python
{
    "objective_params":
    {
        "minf": <dolna_granica_zmiennej_decyzyjnej> : int [minf=0],
        "maxf": <gorna_granica_zmiennnej_decyzyjnej> : int [maxf=30],
        "maxl": <gorna_granica_czasu_wykladow> : int [maxl=9], //pozostalosc po pierwotnej koncepcji
        "ts_lab": <czas_na_labolatorai>: float [ts_lab=11.5],
        "td": <dostepny_czas>: int [td=330],
        "salary": <stawka_za_1h_pracy>: int [salary=25],
        "party_cost": <koszt_imprezy>: int < 0 [party_cost=-12.5],
        "min_income": <minimalny_przychod>: int [min_income=500],
        "avg_coeff": <wspolczynnik_sredniej>: int [avg_coeff=1],
        "salary_ceoff": <wspolczynnik_przychodu>: float [salary_coeff=1],
        "free_time_coeff": <wspolczynnik_czasu_wolnego>: int [free_time_coeff=1],
        "coeff1": int [coeff1=1],
        "coeff2": int [coeff2=1],
        "coeff3": int [coeff3=1],
        "max_iter": <maksymalna_dopuszczalna_liczba_iteracji_z_identyczna_wartoscia_funkcji_celu>: int [max_iter=50]
    },
    "simulation_params":
    {
        "colony_size": int [colony_size=30],
        "n_iter": <liczba_iteracji_dla_jednej_epoki> int [n_iter=5000],
        "max_trials": <maksymalna_liczba_prob_dla_pszczoly> int [max_trials=100],
        "simulations" <liczba_epok_symulacji> int [simulations=30]
    }
}
```

Wywołanie programu
```bash
python simulation.py run <plik_z_danymi.json>
```
Na przykład
```bash
python simulation.py run data.json
```

Wywołanie tuningu wpolczynnikow:
```bash
python simulation.py tune <plik_z_danymi.json> [--cpu -c <ilosc_cpu>]
```
W przypadku podania większej ilości cpu niż dostepna na urządzeniu, program wybierze największą możliwą. Identyczną funkcjonalość można uzyskać podając -1 jako argument.

Na przykład
```bash
python simulation.py tune data.json --cpu -1
```