# Verenluovutus-sovellus

Yksinkertainen sovellus [tsoha](https://hy-tsoha.github.io/materiaali/) harjoitustyöksi.

## käyttäjään liittyvät perustoiminnat:

- rekisteröivät `user:pass:blood_type`
    - `salasana` tallennetaan `md5sum` muodossa
- käyttäjät tunnistautuvat
- käyttäjällä `/[AB0][+-]/` veriryhmä jonain `int` muodossa
- käyttäjä saa olla admin myös
    - jolloin näkee kaiken tiedon rajoituksetta
- käyttäjä saa rekisteröidä verenluovutuskäynnin X kpl eri luovutuspaikassa
    - luovutuksen yhteydessä saa ruksittaa checkboxeja joissa up to 64 eri keksi/kahvi/teeta/Elovenakeksi/karkki/emt/ym. ruksittavissa
- käyttäjä saa suostua laittaa kommentit julkkiseksi alla muodossa, jonk jälkeen:
    - luovutuksen kommentit vapaamuotoisena tekstinä
    - käyttäjä saa myös ladata kuvia luovutuksista, joita `blob` -beina tallennetaan

## luovutuspaikan perustoiminnat:

- user kommentit saa bongata "`<pvm>`: 'oli mukava luovuttaa, bla bla bla...' - `<user_name>`"
- tiettynä pvm:nä montako kpl mies/nainen on käynyt
- tiettynä pvm:nä montako kuvia otettiin

## loput

keksin ne myöhemmin, jos kerkeän
