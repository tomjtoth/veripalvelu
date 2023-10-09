# Verenluovutus-sovellus

Yksinkertainen sovellus Helsingin Yliopiston [tsoha](https://hy-tsoha.github.io/materiaali/) kurssille, jossa käyttäjät saattaa rekisteröidä itseänne, sekä erillisiä käyntejä verenluovutuspaikoilla, joiden yhteydessä saavat merkata mitkä kaikkea ne ovat syöneet/juoneet, myös jättää vapaamuotoista kommenttia halutessaan. Erikoisuutena `FUN` ja `DARK` moodit.

## Nykytilanne

Tässä saavutukset tuoreimmista vanhempiin:

- XSS haavoittuvuus paikattu
- CSRF otettu käyttöön
- arbitrary rajoitukset tehty syötteiden pituuksiin
- fun mode lisätty
    - hiiren vasemmalla purskahtaa ruudulle satunnaiset emojit
    - jos jotain menee pieleen, ja renderöidään `error.html`, siinä sateilee tasan 50kpl pellettä
- dark mode lisätty
    - plotly kaavio ei tue css muuttujia, joten vähän oli pakko toi punainen font-color
- TLS otettu käyttöön tuotannossa
- loader lisätty
    - kaaviot latautuvat melko hitaasti
    - aika hyödyllinen myös näkymän vaihdossa
- `plotly` toimii
    - TODO: pitää vielä säätää kyselyjä taustalla
- feikki tietojen populointi toimii
    - (käyttäjä ei pääse noihin insert lausekkeihin, joten on turvallista rakentaa täällä tavalla)
- luovutuksen rekisteröinti toimii
- rekisteröinti, kirjautuminen toimii
- Vaatimusmäärittelystä karsittu turhan vaikeat osat
    - 5op:een ei mahdu kunnon sovellus...
- README:n luonnos tehty

## Tuotantoversio

[Täältä](https://oracle.ttj.hu:55599) pääsee kokeilemaan `prod` haaran tureimman version
- 5 minuutin sisällä pitäisi hoitua deploymentin systemd timer:in toimesta
- domain nimi ostettu Unkarista
    - `eduroam` tai Oodin langattomasta verkosta ei pääse siihen käsiksi
    - jossain vaiheessa perehdyn siihenkin, miksei :)
- [Oraclen](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm) palvelin pyörii Ruotsissa
- palvelimen aiheuttamat poikkeukset:
    - `psycopg2` paketin asennus ei onnistunut
        - `psycopg2-binary` on käytössä
    - systemd [.service](./systemd/verenluovutus-sovellus.service) tiedosto pyörittää kaiken peruskäyttäjänä
        - with `user lingering enabled`
    - [main.sh](./main.sh) helpottaa ylläpitohommia palvelimessa


## Pää- / Kehitysversio

- Kloonaa repo komennolla `git clone https://github.com/tomjtoth/verenluovutus-sovellus`
- Vaihda äsken syntyneen hakemistoon komennolla `cd verenluovutus-sovellus`
- Asenna virtuaaliympäristö projektille ja aktivoi sitä
    - `python3 -m venv venv`
    - `source venv/bin/activate`
- Asenna projektin riippuvuudet virtuaaliympäristöön alla komennolla
    - `pip install -r requirements.txt`
- käynnistä:
    - `flask run` komennolla
    - `.env` tiedosto ja tietokanta tulee luoduksi ekalla käynnistyksellä
        - olettaen että `v12.15` postgresql pyörii testaajan koneessa
        - muuten testaaja joutuu:
            - käsin luoda kantaa komennolla `createdb jotain`
            - alustaa sitä `psql jotain < schema.sql`
            - ja syöttää `DATABASE_URL=postgresql:///jotain` tiedostoon `.env`

## Toiminnan kuvaus

Tässä käyttäjiin liittyvät toiminnat:

- rekisteröimisen yhteydessä tallennetaan:
    - etunimet
    - sukunimet
    - veriryhmää
    - sukupuolta
- kirjautuminen
- verenluovutuksen rekisteröminen
    - 10 kpl eri luovutuspaikassa
    - voi valita monesta eri syötävästä/juotavasta, kappalemäärä rajoittamatta
- luovuttajat mahdollisesti saavat julkaista:
    - kommentteja vapaamuotoisena tekstinä
    - ~~kuvia luovutuksista~~

Kirjautumatta voi katsoa:

- tilastoja päivämäärien mukaan ja
    - veriryhmän,
    - ja luovutuspaikan perusteella.

- luovutuksen yhteydessä jätetyt kommentit, joista näkyy myös
    - päivämäärä
    - luovuttajan etu ja sukunimien alkukirjaimet

## Jatkokehitysideat

Tänne niitä joita voisikin toteuttaa, muttei mahdu aikarajoitteen takia kurssiin.

- reaaliset [rajoitteet](https://www.veripalvelu.fi/verenluovutus/luovutusedellytykset/) 2 luovutuksen väliin:
    > Suosittelemme verenluovutusta yli 25-vuotiaille naisille enintään 2–3 kertaa vuodessa ja 18-25 v. naisille enintään kerran vuodessa. Miehille suosittelemme enintään 3–4 verenluovutusta vuodessa. Sallitut minimivälit kokoverenluovutuksille ovat naisille 91 ja miehille 61 vuorokautta. Voit laskea laskurilla​, onko minimiväli kohdallasi jo täyttynyt.

- admin käyttäjätunnus (?)
- tilastot siitä paljonko consumable on mennyt, samalla tavalla, kuin index.html:ssa
    - sukupuolen perusteella
    - veriryhmän perusteella
    - luovutuspaikan perusteella
- flexbox, joku siedättävämmännäköinen ulkoasu...
