# PAG — Polish Armaments Group (Vexa)

![Rozwój wartości aktywów PAG](pag-chart.png)

![Wszystkie wypłacone dywidendy](pag-dividend-payouts-summary.png)

![Wartość aktywów wraz z wypłaconymi dywidendami](pag-value-incl-dividends-2026-11-15.png)

[Interaktywny wykres](pag-growth.html) · [Eksport HTML](pag-chart.html) · [Historia danych](history.json) · [Spółka w Vexa](https://vexa.e-sim.org/stockCompany.html?id=45)

Ostatni odczyt widocznej strony Vexa: **23 listopada 2026, 22:50 czasu polskiego** — wyświetlana szacowana wartość **9 966,50 Gold**, **2 976 akcji**, **13 udziałowców** i **24 firmy**. Leandro Daniels ma **2 422 akcje (81,38%)**. Wyświetlana wartość aktywów na akcję: **3,35 Gold**. Odczyt wykonano bez odświeżania raportu.

Względem poprzedniego odczytu z 20 listopada o 05:36: wartość wzrosła o **97,11 Gold (+0,98%)**. Liczba akcji, akcje i udział Leandro, liczba udziałowców oraz firm pozostały bez zmian.

Historia zachowuje **38 pomiarów** do 23 listopada, w tym trzy odczyty z 15 listopada. Logi Vexa potwierdzają **975 Gold w siedmiu wypłatach**: 200 Gold (13 października), 275 Gold w czterech przelewach (30 października) i 500 Gold w dwóch przelewach (13–14 listopada). Kolejne rundy wypłat wzrosły o **37,50%** oraz **81,82%**. Odstępy wyniosły około 17 dni, a potem 14–15 dni; statut określa plan dwutygodniowy, nie gwarantowaną regularność.

The chart now shows **TOTAL DIVIDENDS PAID: 975 GOLD**, **DIVIDENDS PER CURRENTLY ISSUED SHARE: 0.3276 GOLD / SHARE**, and **CUMULATIVE RETURN ON 5 GOLD ISSUE PRICE: 6.55%**. The calculation is 0.3276 Gold in recorded dividends per currently issued share ÷ 5 Gold issue price. It is a distribution metric for a share bought at the original 5 Gold issue price, not a market price, future yield or individual shareholder return.

Najnowsze **9 966,50 Gold wartości aktywów + 975 Gold wcześniej wypłaconych dywidend = 10 941,50 Gold** to miara skumulowana do porównania. Nie oznacza aktywów pozostających w spółce, zysku PAG ani stopy zwrotu akcjonariusza. Wycena aktywów obejmuje zmiany kapitału i cen.

## Źródła i statusy

- Odczyty Vexa pochodzą z widocznej strony spółki; czas pomiaru jest zapisany w polu observed_at. Raportu nie odświeżano, a wyświetlana wartość pozostaje szacunkiem Vexa.
- Wiersz imienny Leandro Daniels jest źródłem jego liczby akcji; pole factories przechowuje liczbę firm widoczną na stronie spółki.
- Szacunki brakujących dni 10 i 12 października są oznaczone jako estimated_missing_day; nie są pomiarami.
- Zapis UI z 22 października ma status saved_ui_refresh_unverified; odświeżenie wyceny nie zostało niezależnie potwierdzone.
- Dane z 9–22 października pochodzą z raportu graficznego przekazanego przez użytkownika. Oznaczenia zachowują wskazane źródło, nie stanowią niezależnej weryfikacji.
- Brak pomiarów z 23–27 października. Linie na wykresie łączą zapisane obserwacje i nie dodają pomiarów.
- Dywidendy są odrębnymi zapisami z logów i nie są dodawane do historycznej wyceny aktywów. Wykres skorygowany pomija 13 października, bo ten odczyt nie ma godziny; odczyt 14 listopada poprzedzał wypłatę o 23:53:58.

## Aktualizacja

history.json jest źródłem danych. Zachowuj wcześniejsze wpisy i dopisuj odczyty z czasem, źródłem i statusem; wartości nieznane zapisuj jako null. Standardowy generator python build.py wymaga Pythona 3 i Pillow. Po zmianie sprawdź historię, wygenerowane PNG i pliki HTML przed publikacją. Nie zapisuj lokalnych notatek w repozytorium.
