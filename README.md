# Verenluovutus-sovellus

Yksinkertainen sovellus [tsoha](https://hy-tsoha.github.io/materiaali/) harjoitustyöksi, jossa käyttäjät saattaa rekisteröidä itseänne, sekä erillisiä käyntejä verenluovutuspaikoilla, joiden yhteydessä saavat ruksittaa mitkä kaikkea ne ovat syöneet/juoneet, myös jättää vapaamuotoista kommenttia halutessaan.

## Tuotantoversio

[Täältä](http://oracle.ttj.hu:55599) pääsee kokeilemaan [24.9.2023](https://github.com/tomjtoth/tsoha-harjoitustyo/commit/b55f528bc501ad8f3ab8194c16a0bb260d92d88b) palautuksen version. Domain ostettu halvalla kotimaasta. Ilmainen palvelin [Oraclelta](https://docs.oracle.com/en-us/iaas/Content/FreeTier/freetier_topic-Always_Free_Resources.htm) pyörii Ruotsissa.

## Nykytilanne

Kronologisesti väärinpain:

- `plotly` toimii
    - pitää vielä säätää kyselyjä taustalla
- feikki tietojen populointi toimii
    - (käyttäjä ei pääse noihin insert lausekkeihin, joten on turvallista rakentaa täällä tavalla)
- luovutuksen rekisteröinti toimii
- rekisteröinti, kirjautuminen toimii
- Vaatimusmäärittelystä karsittu turhan vaikeat osat
    - 5op:een ei mahdu kunnon sovellus...
- README:n luonnos tehty

## Käyttöönotto / käynnistys

- Asenna virtuaaliympäristö projektille ja aktivoi sitä
    - `python3 -m venv venv`
    - `source venv/bin/activate`
- Asenna projektin riippuvuudet virtuaaliympäristöön alla komennolla
    - `pip install -r requirements.txt`
- käynnistä:
    - `flask run` komennolla
    - `.env` tiedosto ja tietokanta tulee luoduksi ekalla käynnistyksellä

## Toiminnan kuvaus

Sovelluksessa sekä perus, että admin käyttäjät, erikoisuutena muutamaa luovutuspaikka.

### Käyttäjään liittyvät perustoiminnat:

- rekisteröidä `user:pass:role`
    - `salasana` tallennetaan/luetaan `werkzeug.security` avulla
    - `role` kuvaa perus luovuttajan/~~hoitajan~~/adminin
        - admin näkee kaiken tiedon
        - ~~hoitaja näkee nykyisen potilaansa kaiken tiedot~~
    - luovuttajat lisäksi tallentaa `veriryhmänsä`
        - `/(?:AB|[AB0])[+-]/` 1 int lukuna
- tunnistautua
- rekisteröidä verenluovutuskäynnin X kpl eri luovutuspaikassa
    - luovutuksen yhteydessä saa ruksittaa checkboxeja joissa erilaiset keksi/kahvi/teeta/Eloveena-keksi/karkki/emt/ym. ruksittavissa
- luovuttajat saavat julkaista:
    - kommentteja vapaamuotoisena tekstinä
    - ~~kuvia luovutuksista~~

### Luovutuspaikan perustoiminnat:

Tunnistautumatta pystyy kysellä myös luovutuspaikkojen tilastot:

- user kommentit saa bongata "`<pvm>`: 'oli mukava luovuttaa, bla bla bla...' - `<user_name>`"
- tiettynä pv:nä montako kpl mies/nainen on käynyt
- ~~tiettynä pv:nä montako kuvia otettiin~~

## Jatkokehitysideat

Tänne niitä joita voisikin toteuttaa, muttei mahdu aikarajoitteen takia kurssiin.

- reaaliset [rajoitteet](https://www.veripalvelu.fi/verenluovutus/luovutusedellytykset/) 2 luovutuksen väliin:
    > Suosittelemme verenluovutusta yli 25-vuotiaille naisille enintään 2–3 kertaa vuodessa ja 18-25 v. naisille enintään kerran vuodessa. Miehille suosittelemme enintään 3–4 verenluovutusta vuodessa. Sallitut minimivälit kokoverenluovutuksille ovat naisille 91 ja miehille 61 vuorokautta. Voit laskea laskurilla​, onko minimiväli kohdallasi jo täyttynyt.
