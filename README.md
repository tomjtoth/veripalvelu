![CI Badge](https://github.com/tomjtoth/veripalvelu/actions/workflows/deploy.yml/badge.svg?branch=main)

# Veripalvelu

Yksinkertainen sovellus Helsingin Yliopiston [tsoha](https://hy-tsoha.github.io/materiaali/) kurssille. Erikoisuutena _Fun_, _Dark_ moodit, _animaatiot_ ja _äänitehosteet_. [Täältä](https://apps.ttj.hu/veripalvelu) pääsee kokeilemaan.

## Käyttöönotto

Yhteinen askel:

```shell
# kloonaa repo
git clone https://github.com/tomjtoth/veripalvelu

# vaihda äsken syntyneen hakemistoon
cd veripalvelu

# luo .env tiedosto jossa repo:sta riippumattomat uuid tunnukset
./setup.sh
```

Tässä vaiheessa pitäisi katsoa läpi `.env` tiedoston sisällön.

### Vaihtoehto 1 (via pip)

Tässä oletetaan, että `v12.5` postgres pyörii koneessa.

```sh
# asenna virtuaaliympäristö projektille ja aktivoi sitä
python3 -m venv venv
source venv/bin/activate

# asenna projektin riippuvuudet virtuaaliympäristöön
pip install -r requirements.txt

# alusta tietokanta
psql < schema.sql

# käynnistä sovellus
flask run # --host=0.0.0.0
```

 ### Vaihtoehto 2 (docker)

Tässä otetaan yhteyttä tietokantaan (ei välttämättä postgres:iin).

```sh
source .env
docker run -d -p $APP_PORT:80 --rm \
    -e "DATABASE_URL=$DATABASE_URL" \
    # ...
    tomjtoth/veripalvelu
```

### Vaihtoehto 3 (docker-compose)

Käynnistä `docker-compose up`.

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

## Jatkokehitysideat

Tänne niitä joita voisikin toteuttaa, muttei mahdu aikarajoitteen takia kurssiin.

- admin käyttäjätunnus
- JS ja CSS tiedostojen isosiivous/yhdistely selkeyden vuoksi
