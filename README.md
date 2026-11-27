# PAG — Polish Armaments Group (Vexa)

![Rozwój wartości aktywów PAG](pag-chart.png)

![Wszystkie wypłacone dywidendy](pag-dividend-payouts-summary.png)

![Wartość aktywów wraz z wypłaconymi dywidendami](pag-value-incl-dividends-2026-11-15.png)

[Interaktywny wykres](pag-growth.html) · [Eksport HTML](pag-chart.html) · [Historia danych](history.json) · [Spółka w Vexa](https://vexa.e-sim.org/stockCompany.html?id=45)

Ostatni odczyt widocznej strony Vexa: **27 listopada 2026, 20:12 czasu polskiego** — wyświetlana szacowana wartość **11 401,35 Gold**, **3 235 akcji**, **14 udziałowców** i **26 firm**. Leandro Daniels ma **2 524 akcje (78,02%)**. Wyświetlana wartość aktywów na akcję: **3,52 Gold**. Odczyt wykonano bez odświeżania raportu.

Względem wcześniejszego odczytu z 27 listopada o 14:28: wartość zmniejszyła się o **36,04 Gold (-0,32%)**; pozostałe monitorowane dane pozostały bez zmian.

Historia zachowuje **43 pomiary** do 27 listopada, w tym dwa odczyty tego dnia, dwa odczyty z 25 listopada i trzy odczyty z 15 listopada. Logi Vexa potwierdzają **1 195 Gold w ośmiu wypłatach**: 200 Gold (13 października), 275 Gold w czterech przelewach (30 października), 500 Gold w dwóch przelewach (13–14 listopada) oraz **220 Gold 26 listopada**. Statut określa plan dwutygodniowy, nie gwarantowaną regularność.

The chart now shows **TOTAL DIVIDENDS PAID: 1,195 GOLD**, **DIVIDENDS PER CURRENTLY ISSUED SHARE: 0.3694 GOLD / SHARE**, and **CUMULATIVE RETURN ON 5 GOLD ISSUE PRICE: 7.39%**. The calculation is 0.3694 Gold in recorded dividends per currently issued share ÷ 5 Gold issue price. It is a distribution metric for a share bought at the original 5 Gold issue price, not a market price, future yield or individual shareholder return.

Najnowsze **11 401,35 Gold wartości aktywów + 1 195 Gold wcześniej wypłaconych dywidend = 12 596,35 Gold** to miara skumulowana do porównania. Nie oznacza aktywów pozostających w spółce, zysku PAG ani stopy zwrotu akcjonariusza. Wycena aktywów obejmuje zmiany kapitału i cen.

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
