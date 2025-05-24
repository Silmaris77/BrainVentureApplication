# BrainVenture - Aplikacja dla Neuroliderów

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
