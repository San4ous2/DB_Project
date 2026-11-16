# AI Provider Platform

Vienkārša darbvirsmas lietotne AI pakalpojumu platformas datu pārvaldībai. Projekts izmanto Python, Tkinter un SQLite, un tajā ir 10 savstarpēji saistītas datubāzes tabulas.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)
![Interface](https://img.shields.io/badge/Interface-Tkinter-2E8B57)

## Iespējas

- Apskatīt platformas datus tabulās.
- Meklēt ierakstus un izvēlēties meklēšanas lauku.
- Pievienot, labot un dzēst ierakstus.
- Pārvaldīt lietotājus, abonementus, maksājumus, API atslēgas, modeļus, sarunas, uzvednes, datu kopas un apmācības darbus.
- Uzturēt datu integritāti ar SQLite ārējām atslēgām.

## Tehnoloģijas

| Tehnoloģija | Izmantojums |
| --- | --- |
| Python 3 | Lietotnes loģika |
| Tkinter | Grafiskā lietotāja saskarne |
| SQLite | Datu glabāšana un vaicājumi |

Papildu Python pakotnes nav nepieciešamas; izmantotas Python standarta bibliotēkas.

## Palaišana

Nepieciešams Python 3 ar pieejamu Tkinter moduli.

1. Atver projekta mapi terminālī.
2. Ja datubāze tiek veidota pirmo reizi, izveido tabulas un ievieto piemēra datus:

   ```powershell
   python -c "import sqlite3; db=sqlite3.connect('AI_Provider_Platform.db'); db.executescript(open('dbcreate.sql', encoding='utf-8').read()); db.close()"
   ```

3. Palaid lietotni:

   ```powershell
   python app.py
   ```

Datubāze `AI_Provider_Platform.db` tiek glabāta projekta mapē. `dbcreate.sql` izmanto `CREATE TABLE IF NOT EXISTS` un `INSERT OR IGNORE`, tāpēc inicializācijas komandu var palaist atkārtoti, nedublējot sākotnējos ierakstus.

## Datubāzes struktūra

<img width="1097" height="830" alt="Ekrānuzņēmums 2026-10-16 110615" src="https://github.com/user-attachments/assets/afe033f8-e8b5-4687-be16-3d8532a4d40f" />

## Piemēra datu grafiki

Grafiki attēlo ierakstus, kas tiek ievietoti no `dbcreate.sql`.

### Abonementu plāni

```mermaid
pie showData
	title Abonementu skaits pēc plāna
	"Premium" : 2
	"Standard" : 2
	"Free" : 1
```

### Maksājumu veidi

```mermaid
pie showData
	title Maksājumu ieraksti pēc veida
	"Payment" : 5
	"Refund" : 1
```

### Apmācības darbu statusi

```mermaid
pie showData
	title Apmācības darbu skaits pēc statusa
	"Completed" : 1
	"Running" : 1
	"Failed" : 1
	"Queued" : 1
```

## Projekta faili

```text
DB_Project/
├── app.py                       # Tkinter lietotne
├── funcitons.py                 # SQLite savienojums un datu funkcijas
├── dbcreate.sql                 # Tabulu shēma un sākotnējie dati
├── AI_Provider_Platform.db      # SQLite datubāzes fails
└── README.md                    # Projekta dokumentācija
```

## Datu dzēšanas ierobežojumi

Saistītu ierakstu nevar dzēst, kamēr to izmanto cits ieraksts. Piemēram, pirms lietotāja dzēšanas ir jāizdzēš ar šo lietotāju saistītie abonementi, maksājumi, API atslēgas, sarunas un uzvednes. Tas palīdz saglabāt datu konsekvenci.