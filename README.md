# Verenluovutus-sovellus

Yksinkertainen sovellus [tsoha](https://hy-tsoha.github.io/materiaali/) harjoitustyöksi.

## käyttäjään liittyvät perustoiminnat:

Käyttäjät saavat:

- rekisteröidä `user:pass:role`
    - `salasana` tallennetaan `md5sum` muodossa
    - `role` kuvaa perus luovuttajan/hoitajan/adminin
        - admin näkee kaiken tiedon
        - hoitaja näkee nykyisen potilaansa kaiken tiedot
    - luovuttajat lisäksi tallentaa `veriryhmänsä`
        - `/(?:AB|[AB0])[+-]/` 1 int lukuna
- tunnistautua
- rekisteröidä verenluovutuskäynnin X kpl eri luovutuspaikassa
    - luovutuksen yhteydessä saa ruksittaa checkboxeja joissa erilaiset keksi/kahvi/teeta/Eloveena-keksi/karkki/emt/ym. ruksittavissa
- luovuttajat saavat julkaista:
    - kommentteja vapaamuotoisena tekstinä
    - kuvat luovutuksista

## luovutuspaikan perustoiminnat:

Tunnistautumatta myös:
- user kommentit saa bongata "`<pvm>`: 'oli mukava luovuttaa, bla bla bla...' - `<user_name>`"
- tiettynä pvm:nä montako kpl mies/nainen on käynyt
- tiettynä pvm:nä montako kuvia otettiin

## loput

keksin ne myöhemmin, jos kerkeän
