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
- `GROUPS`: de drie doelen waarop het dashboard is ingedeeld. **Beleving** (Happiness,
  Levenscontentheid, Happiness werk, Robin, Vrienden), **Belasting** (privé- en werkstress,
  alcohol, drugs, slaap, wakker, trainingsbelasting/-uren, vermoeidheid, fitness) en **Gevolgen**
  (energie, ochtendgevoel, HRV, rusthartslag, unclenched, ziek, vorm). De tabbladen/secties heten
  Overzicht, Beleving, Belasting, Gevolgen, Inzicht; `TILE_GROUPS` geeft de tegels per doel, het
  dagdetail en de Verkenner (optgroups) volgen `GROUPS`. Nieuwe metriek? Zet hem in `M`, in `GROUPS`
  en in een grafiek op het juiste tabblad.
- `READY` / `renderReady()`: kaart **Klaar voor zwaar?** bovenaan het Overzicht. Altijd voor vandaag
  (los van de gekozen periode). Ochtendmetingen van vandaag, anders gisteren; dagscores van vandaag of
  gisteren. Per signaal groen/oranje/rood:
  - HRV, rusthartslag, slaap en ochtendgevoel tegen de eigen band (28 dagen, ± 1 sd; bij
    scores minstens ± 0,5). Buiten de band is oranje, 2 dagen op rij is rood. HRV en rusthartslag ook
    rood bij meer dan 2 sd van het gemiddelde; slaap en ochtendgevoel ook rood bij 4 of lager.
  - Slaap is in uren. Zolang er te weinig dagen zijn voor een eigen band (minder dan 10 metingen in
    28 dagen) geldt voorlopig 8 uur als normaal, dus onder 7,5 uur is oranje.
  - Ochtendgevoel: op dezelfde manier voorlopig 7 als normaal, dus onder 6,5 is oranje.
  - Vermoeidheid (ATL) tegen de eigen band: erboven oranje, meer dan 2 sd boven het gemiddelde rood.
    Geen regel "2 dagen op rij", want ATL verandert traag.
  - Vorm: onder −10 oranje, onder −30 rood.
  - Opbouw fitness: CTL nu min 7 dagen terug; meer dan 8 is oranje, meer dan 12 rood.
  - Ziek > 0 is rood.
  - Alcohol: vanaf 3 oranje, vanaf 6 rood.
  - Stress (totaal van privé en werk, 0–10; op dagen zonder werkscore alleen privé): vanaf 5 oranje,
    vanaf 8 rood.

  Oordeel: rood als er één rood signaal is of minstens 3 oranje, oranje bij 1–2 oranje, anders groen.
  Bij minder dan 3 signalen met gegevens: "nog te weinig metingen". Zijn HRV laag en rusthartslag hoog
  op dezelfde dag, dan komt er een extra regel over mogelijk ziek worden. De grenzen zijn een eerste
  keuze en mogen worden bijgesteld.

  Elk signaal heeft een balk (`drawGauge`) met rood, oranje en groen en een punt op de waarde. De zones
  zijn dezelfde grenzen als hierboven. Ziek heeft bewust geen oranje. Bij "2 dagen op rij" kan het
  rode statusbolletje bij een punt in de oranje zone staan.
  Ook het oordeel heeft zo'n balk: oranje telt 1 punt, rood 3. 0 punten is groen, 1–2 oranje, 3 of meer
  rood; hoe meer punten, hoe verder de punt naar links.
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
Unclenched/Slaap/Gevoel/Robin 1–10, Privestress en werk-Stress 0–5, Ziek, Drugs en Vrienden 0–3, Alcohol 0–10,
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
