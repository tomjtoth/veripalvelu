# Verenluovutus-sovellus

Yksinkertainen sovellus Helsingin Yliopiston [tsoha](https://hy-tsoha.github.io/materiaali/) kurssille, jossa käyttäjät saavat rekisteröidä itseänne, sekä erillisiä käyntejä verenluovutuspaikoilla, joiden yhteydessä voi merkata mitkä kaikkea ne ovat syöneet/juoneet, myös jättää vapaamuotoista kommenttia halutessaan. Erikoisuutena _Fun_, _Dark_ moodit, _animaatiot_ ja _äänitehosteet_. Animaatiot debian testingin firefoxissa ainakin vähän vilahtaa, Chromium:ssa ne ovat ihan fine.

## Tuotantoversio

[Täältä](https://oracle.ttj.hu:55599) pääsee kokeilemaan `prod` haaran tureimman version
- 5 minuutin sisällä pitäisi hoitua deploymentin systemd timer:in toimesta
- domain nimi ostettu Unkarista
    - `eduroam` :in tai Oodin langattomasta verkosta ei pääse siihen käsiksi
    - jossain vaiheessa perehdyn siihenkin, miksei :)
- [Oraclen](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm) palvelin pyörii Ruotsissa
- palvelimen aiheuttamat poikkeukset:
    - `psycopg2` paketin asennus ei onnistunut
        - `psycopg2-binary` on käytössä
    - systemd [.service](./systemd/verenluovutus-sovellus.service) tiedosto pyörittää kaiken peruskäyttäjänä
        - with `user lingering enabled`
    - [main.sh](./main.sh) helpottaa ylläpitohommia palvelimessa


## Pää- / Kehitysversio

Pakotusti käsin hoidettavat askeleet:
```shell
# kloonaa repo
git clone https://github.com/tomjtoth/verenluovutus-sovellus

# vaihda äsken syntyneen hakemistoon
cd verenluovutus-sovellus
```

Asennus ja käynnistys **JOKO** tuotantopalvelimessa käytetyllä wrapper:illa:
```shell
# tämä kyllä hoitaa kaiken
./main.sh
```

**TAI** kurssin materiaalin mukaan:
```shell
# asenna virtuaaliympäristö projektille ja aktivoi sitä
python3 -m venv venv
source venv/bin/activate

# asenna projektin riippuvuudet virtuaaliympäristöön alla komennolla
pip install -r requirements.txt

# käynnistä:
flask run
```

Molemmassa tapauksessa sovellus pysähtyy siihen, että se on luonut `.env` tiedosto, jonka sisällön kuuluisi testaajan katsoa läpi.
Tietokanta tulee luoduksi ekalla käynnistyksellä olettaen että `v12.15` postgresql pyörii testaajan koneessa. Muuten pitää käsin luoda se tietokanta ja liittää sen nimi `.env`:iin.

Kun `.env` katsottiin läpi, ja tietokanta on olemassa, käynnistetään sovelluksen vielä kerran:
- joko `flask run`
- tai `./main.sh`
komennolla.

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
    - luovutuspaikan,
    - ja sukupuolten perusteella

- luovutuksen yhteydessä jätetyt kommentit, joista näkyy myös
    - päivämäärä
    - luovuttajan etu ja sukunimien alkukirjaimet

- luovutuksen yhteydessä vedätyt naposteltavat saa myös nähdä pvm: perusteella 

## Aikajana

En ole varmaa käytettyjen tuntien määrästä, tässä saavutukset tuoreimmista vanhempiin:

- "ponnahdusikkuna" lisätty 2 hämäävämmälle "työkalulle"
- JS tiedostot, CSS rikottu moduuleihin, koska meinasin kierrettää mun yksityisprojekteissa, 
    - ois pärjännyt vähemmällä luokalla ja eventListener:llakin, meni jo...
- (lähes) tyhjä kanta antaa järkeviä tekstejä kaavioiden sijaan
- äänitehosteet lisätty
- consumption annettu takaisin sekä tauluna, että kaavioina
- front-end hiottu suht valmiiksi
- REST API:n hyödyntäen sydän kyselee palvelimelta montako luovutusta on rekisteröity
    - toisesta selaimesta kantsii rekisteröidä uusia, niin alkuperäisen ikkunan laskuri muuntuu
    - en oo testannut mitä jos vastaus ei ikinä saavu takas, sehän on olennainen osa syklistä
    - sydän saa kohtauksen jos fetch kestää yli `avg(viimeisen 10kpl roundtrip)  + 350ms`, voit triggeröidä alla tavoilla:
        - jos palvelin pyörii paikallisesti, sammuta se
        - jos kokeilet tuotannon palvelimen, katkaise nettiyhteys
        - sydänkohtauksen aikana siitä klikkaen voi elvyttää (käynnistää uuden query:n ja resetoida roundtrippien kestoa)
- dark-mode nappi animoitu
- fun-mode nappi sykkii kun aktiivinen
    - piirretään `z-index: -1;` kaikki emojit, jotta perus HTML elementit ois räplättävissä
        - ainakin debian testingin firefox:ssa tuli glitchit, chromium näyttää OK:lta
- `main.sh` hoitaa asennuksen
- luovutuksen prosessointi revisioitu
- pylint otettu käyttöön
- dokumentaatiostringit lisätty sekä JS että Python:in puolelle
- error.html:sta pääsee takas myös linkin kautta
- kuvaavampi title atrribuutti lisätty rekisteröinnin näkymässä:
    - "`sukunimet`" +  "`,`" + "`etunimet`"
- XSS haavoittuvuus paikattu
- CSRF otettu käyttöön
- arbitrary rajoitukset tehty syötteiden pituuksiin
- fun mode lisätty
    - hiiren vasemmalla purskahtaa ruudulle satunnaiset emojit
    - `error.html` sisältää yllätyksiä
- dark mode lisätty
    - plotly kaavio ei tue css muuttujia, joten vähän oli pakko toi punainen font-color
- TLS otettu käyttöön tuotannossa
- loader lisätty
    - kaaviot latautuvat melko hitaasti
    - aika hyödyllinen myös näkymän vaihdossa
- `plotly` toimii
- feikki tietojen populointi toimii
    - (käyttäjä ei pääse noihin insert lausekkeihin, joten on turvallista rakentaa täällä tavalla)
- luovutuksen rekisteröinti toimii
- rekisteröinti, kirjautuminen toimii
- Vaatimusmäärittelystä karsittu turhan vaikeat osat
- README:n luonnos tehty

## Jatkokehitysideat

Tänne niitä joita voisikin toteuttaa, muttei mahdu aikarajoitteen takia kurssiin.

- admin käyttäjätunnus (?)
    - en näe enää tässä pointtia
- JS ja CSS tiedostojen isosiivous/yhdistely selkeyden vuoksi
- Docker:in käyttöönotto
    - ehkä docker kurssien jälkeen
