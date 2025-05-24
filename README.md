# BrainVenture - Program dla Neuroliderów

## Opis projektu

BrainVenture to aplikacja edukacyjna zbudowana w Streamlit, która skupia się na nauczaniu zasad neuroprzywództwa. Platforma oferuje interaktywne lekcje, testy oraz materiały edukacyjne z dziedziny neurobiologii i przywództwa.

## Funkcjonalności

- **Dashboard** - Przegląd postępów i aktualności
- **Test Neuroliderstwa** - Test oceniający umiejętności neuroprzywódcze
- **Lekcje** - Interaktywne materiały edukacyjne podzielone na moduły
- **Profil użytkownika** - Dane użytkownika, postępy, certyfikaty i ustawienia

## Struktura projektu

```
BrainVentureApp/
├── Home.py                  # Strona główna aplikacji
├── pages/                   # Podstrony aplikacji
│   ├── 1_Dashboard.py       # Dashboard z przeglądem kursu
│   ├── 2_Neuroleader_Test.py# Test Neuroliderstwa
│   ├── 3_Lekcje.py          # Strona z lekcjami
│   └── 4_Profil.py          # Profil użytkownika
├── components/              # Komponenty UI
├── config/                  # Pliki konfiguracyjne
├── data/                    # Dane aplikacji
│   └── content/             # Zawartość kursu w JSON
├── static/                  # Zasoby statyczne
│   ├── css/                 # Style CSS
│   └── images/              # Obrazy
└── utils/                   # Funkcje pomocnicze
```

## Nawigacja

Aplikacja wykorzystuje centralizowany system nawigacji z dwoma głównymi elementami:

1. **Pasek boczny (Sidebar)** - Zawiera główne menu nawigacyjne oraz opcjonalne filtry dla konkretnych stron
2. **Menu kontekstowe** - Pojawia się na wybranych stronach, udostępniając dodatkowe filtry i opcje

System nawigacji jest zarządzany przez moduł `utils/navigation.py`, który zapewnia spójny interfejs na wszystkich stronach.

## Wymagania

Zainstaluj wymagane pakiety:

```
pip install -r requirements.txt
```

## Uruchomienie aplikacji

```
streamlit run Home.py
```

## Rozwój projektu

Aplikacja jest w fazie MVP (Minimum Viable Product). Planowane rozszerzenia:
- System autentykacji użytkowników
- Rozbudowana gamifikacja (odznaki, poziomy)
- System analityki użytkownika
- Integracja z zewnętrznymi zasobami edukacyjnymi

## Licencja

© 2025 BrainVenture. Wszelkie prawa zastrzeżone. - Aplikacja dla Neuroliderów

BrainVenture to kompleksowa aplikacja kursowa stworzona dla osób pragnących rozwijać swoje umiejętności w zakresie neuroprzywództwa. Aplikacja łączy wiedzę z neurobiologii z praktycznymi umiejętnościami przywódczymi.

## Funkcjonalności

- **Test Neuroliderstwa** - ocenia obecne umiejętności i sugeruje obszary do rozwoju
- **Struktura kursu** - 150 lekcji zgrupowanych w 15 modułów i 5 bloków tematycznych
- **Interaktywne lekcje** - z materiałami wideo, quizami i ćwiczeniami
- **Profil użytkownika** - śledź swój postęp i zdobywaj odznaki
- **Spersonalizowana ścieżka nauki** - dostosowana do wyników testu

## Uruchamianie aplikacji

### Wymagania

- Python 3.8+
- Streamlit 1.32.0+
- Pozostałe zależności wymienione w `requirements.txt`

### Instalacja

1. Sklonuj repozytorium lub pobierz pliki
2. Zainstaluj wymagane pakiety:

```
pip install -r requirements.txt
```

3. Uruchom aplikację:

```
streamlit run app.py
```

## Struktura projektu

```
├── app.py                      # Główny plik aplikacji
├── config/                     # Konfiguracja aplikacji
├── core/                       # Podstawowe funkcjonalności
├── components/                 # Komponenty UI wielokrotnego użytku
├── pages/                      # Strony aplikacji
├── modules/                    # Moduły funkcjonalne
├── utils/                      # Narzędzia pomocnicze
├── static/                     # Pliki statyczne (obrazy, CSS, JS)
├── data/                       # Dane aplikacji
└── docs/                       # Dokumentacja
```

## Wersja MVP

Obecna wersja to MVP (Minimum Viable Product) zawierający:
- Test Neuroliderstwa
- Pierwszą przykładową lekcję
- Pełną strukturę kursu
- Profil użytkownika

## Rozwój aplikacji

Planowane rozszerzenia:
- System logowania i rejestracji użytkowników
- Pełny zestaw lekcji z materiałami multimedialnymi
- Interaktywne ćwiczenia
- Rozbudowany system gamifikacji
- Śledzenie postępów i system raportowania
- Funkcjonalności społecznościowe

## Autor

BrainVenture © 2025
