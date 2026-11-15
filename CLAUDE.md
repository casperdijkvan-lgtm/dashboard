# Dashboard

Persoonlijk dashboard voor iPhone én Mac: https://casperdijkvan-lgtm.github.io/dashboard/

Het leest (alleen lezen, nooit schrijven):
- Dropbox `/Apps/Scores/Scores.csv`, `WorkScores.csv`, `MorningScores.csv`: geschreven door de
  score-apps in de **andere repository** `casperdijkvan-lgtm/dagscore`.
- Dropbox `/Apps/HRV4Training`: het nieuwste exportbestand (rMSSD, rusthartslag).
- intervals.icu: uren, belasting, fitness, vermoeidheid, vorm. De API-sleutel en athlete-ID vult de
  gebruiker zelf in bij Instellingen; die blijven in `localStorage` op het apparaat.

## Zo werkt deze repository

- **Bron:** `bron/dashboard.html` (alles in één bestand: HTML, CSS en JS met een eigen SVG-grafiekmotor).
- **Gebouwd:** `index.html` en `apple-touch-icon.png` in de hoofdmap. **Nooit met de hand aanpassen.**
- **Online zetten:** GitHub Pages serveert de hoofdmap van `main`; na een push staat het binnen ~1 minuut online.

### Een aanpassing doen (altijd deze stappen)

1. Pas `bron/dashboard.html` aan.
2. Bouw: `python3 bron/build_dashboard.py` (vanuit de hoofdmap). Pillow is optioneel; zonder Pillow
   blijft het bestaande icoon staan.
3. Commit **zowel de bron als de gebouwde bestanden** en push naar `main`.
4. Controleer na een minuut dat de live pagina dezelfde `<meta name="dashboard-versie">` heeft als de
   gebouwde `index.html`. Het dashboard ververst zichzelf bij een nieuwe versie.

## Opbouw van de code

- `CFG`: paden in Dropbox, Dropbox app key, aantal dagen intervals.icu.
- `M`: register van alle metrieken (kolomnaam `col`, bron `src`, schaal `min`/`max`, `good` up/down,
  `zero: true` als 0 een echte waarde is, `zero: 'after-first'` als nullen vóór de eerste ingevulde dag
  "nog niet gevraagd" betekenen).
- `buildModel()`: zet de CSV's en metingen om naar één record per datum.
- `TimeChart` (line/bar/div/strip, week/dag, crosshair, zoom, tabelweergave), `ScatterChart`
  (verbanden met vertraging), `CalendarChart` (heatmap). Tegels, bevindingen (Pearson r), dagboek,
  instellingen en periodeknoppen 7D/30D/90D/6M/1J/Alles.
- Kleuren staan als tokens op `:root`, met een donkere variant.

**Het dashboard rekent waarden niet om**: het toont precies wat in de bestanden staat. Klopt een schaal
niet, pas dan de bestanden aan (via een eenmalige omzetting in de score-apps), niet de weergave.

## Samenhang met de score-apps

Kolomnamen en schalen moeten overeenkomen met de vragen in `casperdijkvan-lgtm/dagscore`
(`bron/dagscore.html` en `bron/build_site.py`). Huidige schalen: Happiness/Energie/Levenscontentheid/
Unclenched/Workload/Slaap/Gevoel 1–10, Privestress en werk-Stress 0–5, Ziek en Drugs 0–3, Alcohol 0–10,
Wakker 0–4 (halve punten). Verandert daar iets, pas dan `M` en de grafieken hier aan.

## Wensen van de gebruiker

- Alles in het **Nederlands**.
- Werkt en ziet er goed uit op iPhone (aanraken: scrubben, tikken voor details) én op de Mac (hover,
  slepen om in te zoomen). Licht en donker.
- Niets op een server; alleen de browser praat met Dropbox en intervals.icu.

## Dropbox

Dropbox-app **DagScoresDashboard**, app key `jvqh2qs61dyyqnp` (niet geheim; PKCE), toegang: Full
Dropbox, scopes `files.metadata.read` en `files.content.read`. Redirect-URI:
`https://casperdijkvan-lgtm.github.io/dashboard/`.

## Testen

Geen testsuite. `window.__dash` biedt testhaakjes (`setRaw`, `data()`, `M`, `parseDelimited`). Test met
een nagebootste `window.fetch` en nep-inlog in `localStorage['dashboard.dropbox.v1']`. Zet
testbestanden nooit in de repository.

## Veiligheid

Deze repository is openbaar. Zet er nooit sleutels of wachtwoorden in, vooral niet de intervals.icu-sleutel.
