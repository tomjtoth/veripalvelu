# Verenluovutus-sovellus

Yksinkertainen sovellus [tsoha](https://hy-tsoha.github.io/materiaali/) harjoitustyöksi, jossa käyttäjät saattaa rekisteröidä itseänne, sekä erillisiä käyntejä verenluovutuspaikoilla, joiden yhteydessä saavat ruksittaa mitkä kaikkea ne ovat syöneet/juoneet, myös jättää vapaamuotoista kommenttia halutessaan.

## Nykytilanne

Kronologisesti väärinpain:

- feikki tietojen populointi toimii
    - (käyttäjä ei pääse noihin insert lausekkeihin, joten on turvallista rakentaa täällä tavalla)
- luovutuksen rekisteröinti toimii
- rekisteröinti, kirjautuminen toimii
- Vaatimusmäärittelystä karsittu turhan vaikeat osat
    - 5op:een ei mahdu kunnon sovellus...
- README:n luonnos tehty

## Käyttöönotto

- Asenna virtuaaliympäristö projektille ja aktivoi sitä
    - `python3 -m venv venv`
    - `source venv/bin/activate`
- Asenna projektin riippuvuudet virtuaaliympäristöön alla komennolla
    - `pip install flask flask-sqlalchemy psycopg2 python-dotenv`
- `.env`:ssa säädä `GEN_RAND_DATA=false` arvoon ennen ensikäyttöä jos haluat paljaan kannan
    - en suosittele

## Käynnistys

Tapahtuu virtuaaliympäristössä komennolla `flask run`.

## Kehitys / kokeilu

[Ohjeen](https://code.visualstudio.com/docs/python/tutorial-flask) perusteella luo `.vscode/launch.json` jotta pääsisit edes `debug` -gaamaan + muuntaa itsellesi sopivaksi alla arvot:

## Toiminnan kuvaus

Sovelluksessa sekä perus, että admin käyttäjät, erikoisuutena muutamaa luovutuspaikka.

### käyttäjään liittyvät perustoiminnat:

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

### luovutuspaikan perustoiminnat:

Tunnistautumatta pystyy kysellä myös luovutuspaikkojen tilastot:

- user kommentit saa bongata "`<pvm>`: 'oli mukava luovuttaa, bla bla bla...' - `<user_name>`"
- tiettynä pv:nä montako kpl mies/nainen on käynyt
- ~~tiettynä pv:nä montako kuvia otettiin~~

