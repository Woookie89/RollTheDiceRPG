# RollTheDiceRPG

Webowy stol RPG dla wielu systemow: karta postaci, kampanie, rzuty koscia i lekki silnik przygod.

## Stack

- Django 4.2 + Django REST Framework
- Django templates jako glowny frontend
- HTMX dla dynamicznych fragmentow UI
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

Projekt rozwija sie jako system-agnostic RPG workspace. Wspolny rdzen obsluguje uzytkownikow, kampanie, postacie i historie rzutow, a poszczegolne systemy RPG sa definiowane przez rulesety.

Pierwsze wspierane rulesety:

- Dungeons & Dragons 5E
- Call of Cthulhu
- Year Zero / Tajemnice Petli i Powodzi
- Warhammer Fantasy Roleplay 4E
- Vampire: The Masquerade 5E
- Kult: Divinity Lost
