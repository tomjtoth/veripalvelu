# Verenluovutus-sovellus

Yksinkertainen sovellus [tsoha](https://hy-tsoha.github.io/materiaali/) harjoitustyöksi.

## Nykytilanne

Kronologisesti väärinpain:

- Vaatimusmäärittelystä karsittu turhan vaikeat osat
    - 5op:een ei mahdu kunnon sovellus...
- README:n luonnos tehty

## Kokeilu

placeholder

## Toiminnan kuvaus

Sovelluksessa sekä perus, että admin käyttäjät, erikoisuutena muutamaa luovutuspaikka.

### käyttäjään liittyvät perustoiminnat:

- rekisteröidä `user:pass:role`
    - `salasana` tallennetaan `md5sum` muodossa
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

