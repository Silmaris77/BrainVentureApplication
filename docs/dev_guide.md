# BrainVenture - Dokumentacja dla deweloperów

## Wprowadzenie

BrainVenture to aplikacja edukacyjna stworzona dla neuroliderów, która łączy wiedzę z neurobiologii z praktycznymi umiejętnościami przywódczymi. Aplikacja została zbudowana przy użyciu frameworka Streamlit.

## Architektura aplikacji

### Struktura katalogów

```
├── app.py                      # Główny plik aplikacji
├── config/                     # Konfiguracja aplikacji
│   ├── app_config.py           # Podstawowa konfiguracja
│   ├── content_config.py       # Konfiguracja zawartości edukacyjnej
│   └── security_config.py      # Ustawienia bezpieczeństwa
├── core/                       # Podstawowe funkcjonalności
│   ├── auth/                   # System uwierzytelniania
│   ├── data/                   # Zarządzanie danymi
│   └── analytics/              # System analityki
├── components/                 # Komponenty UI wielokrotnego użytku
│   ├── navigation.py           # Nawigacja aplikacji
│   └── ...
├── pages/                      # Strony aplikacji
│   ├── dashboard.py            # Strona główna
│   ├── neuroleader_test.py     # Test Neuroliderstwa
│   ├── lessons.py              # Strona lekcji
│   └── profile.py              # Profil użytkownika
├── modules/                    # Moduły funkcjonalne
│   ├── gamification/           # System gamifikacji
│   ├── learning/               # System nauki
│   └── communication/          # System komunikacji
├── utils/                      # Narzędzia pomocnicze
│   ├── ui.py                   # Narzędzia UI
│   ├── validators.py           # Walidacja formularzy
│   ├── helpers.py              # Funkcje pomocnicze
│   └── logger.py               # System logowania
├── static/                     # Pliki statyczne
│   ├── images/                 # Obrazy
│   ├── css/                    # Style CSS
│   └── js/                     # Skrypty JavaScript
├── data/                       # Dane aplikacji
│   ├── content/                # Zawartość kursów
│   ├── logs/                   # Logi aplikacji
│   └── user_files/             # Pliki użytkowników
```

## Jak działa aplikacja

1. `app.py` jest głównym punktem wejścia aplikacji
2. Konfiguracja ładowana jest z katalogu `config/`
3. Strony aplikacji znajdują się w katalogu `pages/`
4. Komponenty UI wielokrotnego użytku znajdują się w katalogu `components/`
5. Narzędzia pomocnicze znajdują się w katalogu `utils/`

## Funkcje i moduły

### System uwierzytelniania (przyszła implementacja)

System uwierzytelniania będzie znajdował się w katalogu `core/auth/` i będzie odpowiedzialny za:
- Rejestrację użytkowników
- Logowanie użytkowników
- Zarządzanie sesjami
- Autoryzację dostępu do zasobów

### System nauki (przyszła implementacja)

System nauki będzie znajdował się w katalogu `modules/learning/` i będzie odpowiedzialny za:
- Zarządzanie kursami
- Śledzenie postępów użytkownika
- Adaptacyjne uczenie się
- Quizy i testy

### System gamifikacji (przyszła implementacja)

System gamifikacji będzie znajdował się w katalogu `modules/gamification/` i będzie odpowiedzialny za:
- Przyznawanie punktów
- Zarządzanie odznakami
- Tabele wyników
- Wyzwania

## Jak uruchomić aplikację

### Wymagania

- Python 3.8+
- Streamlit 1.32.0+
- Pozostałe zależności wymienione w `requirements.txt`

### Uruchamianie aplikacji

```bash
# Zainstaluj zależności
pip install -r requirements.txt

# Uruchom aplikację
streamlit run app.py
```

## Rozwój aplikacji

### Dodawanie nowej strony

1. Utwórz nowy plik w katalogu `pages/` (np. `pages/new_page.py`)
2. Zaimplementuj funkcję `show_new_page()`, która będzie odpowiedzialna za wyświetlanie strony
3. Dodaj import i wywołanie funkcji w `app.py`
4. Dodaj stronę do menu nawigacyjnego w `components/navigation.py`

### Dodawanie nowej funkcjonalności

1. Zastanów się, do którego modułu powinna należeć nowa funkcjonalność
2. Utwórz odpowiednie pliki w odpowiednim katalogu
3. Zaimplementuj funkcjonalność
4. Zaktualizuj dokumentację

## Dobre praktyki

- Używaj typowania statycznego (type hints) w Pythonie
- Pisz testy dla nowych funkcjonalności
- Komentuj kod, szczególnie skomplikowane fragmenty
- Używaj jednolitego stylu kodowania
- Trzymaj się struktury katalogów

## Zasoby

- [Dokumentacja Streamlit](https://docs.streamlit.io/)
- [Dokumentacja Pandas](https://pandas.pydata.org/docs/)
- [Dokumentacja Matplotlib](https://matplotlib.org/stable/contents.html)
