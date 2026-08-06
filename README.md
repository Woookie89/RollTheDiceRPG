# RollTheDiceRPG

Webowy stół RPG dla wielu systemów: karta postaci, kampanie, rzuty kością i lekki silnik przygód.

## Stack

- Django 4.2 + Django REST Framework
- Django templates jako główny frontend
- HTMX dla dynamicznych fragmentów UI
- SQLite na start

## Uruchomienie lokalne

```powershell
python3.12 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe manage.py migrate
.venv\Scripts\python.exe manage.py runserver
```

Aplikacja startuje pod `http://localhost:8000/`.

## Kierunek produktu

Projekt rozwija się jako system-agnostic RPG workspace. Wspólny rdzeń obsługuje użytkowników, kampanie, postacie, dziennik i historię rzutów, a poszczególne systemy RPG są definiowane przez rulesety.

Pierwsze wspierane rulesety:

- Dungeons & Dragons 5E
- Call of Cthulhu
- Year Zero / Tajemnice Pętli i Powodzi
- Warhammer Fantasy Roleplay 4E
- Vampire: The Masquerade 5E
- Kult: Divinity Lost

## Mapa rozwoju

1. Gracz MVP: karta postaci, dashboard, szybkie rzuty, dziennik.
2. Panel Mistrza Gry: planowanie kampanii, prywatne notatki, cele sesji.
3. Przygody i sceny: statusy scen, stawki, konsekwencje, podsumowanie sesji.
4. NPC, frakcje i powiązania: siatka relacji, motywacje, sekrety, lokacje.
5. Sesja na żywo: wspólny log stołu, ujawnione materiały i szybkie akcje.
