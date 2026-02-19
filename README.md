# ComfyUI Automated Video Generator

Narzędzie do zautomatyzowanego generowania filmów przez API ComfyUI z obsługą tranzycji i sekwencji I2V.

## 📁 Struktura projektu

```
.
├── RUNS/                  # Punkty wejścia dla konkretnych projektów
├── workflows/             # Workflow ComfyUI (JSON)
├── workflow_configs/      # Konfiguracje workflow (YAML)
├── backends/              # Implementacje dla różnych backendów
│   └── local/            # Backend lokalny
├── helpers/               # Funkcje pomocnicze
├── postprocessing/        # Funkcje postprocessingu
├── utils/                 # Narzędzia dodatkowe
├── logs/                  # Logi aplikacji (git-ignorowane)
├── batch_validator.py     # Główny orkiestrator
├── flow_parser.py         # Parsowanie i walidacja flow
├── workflow_base.py       # Bazowa klasa workflow
└── config_validator.py    # Walidacja konfiguracji i materiałów
```

## 🚀 Główne komponenty

- **batch_validator** - Główny orkiestrator całego procesu
- **flow_parser** - Sprawdzanie poprawności plików i flow
- **config_validator** - Walidacja materiałów (pliki, formaty, proporcje)
- **workflow_base** - Bazowa implementacja workflow

## 💡 Jak używać

1. Przygotuj skrypt w katalogu `RUNS/`
2. Uruchom walidację: `python config_validator.py`
3. Wykonaj generowanie: `python batch_validator.py`

## 🔧 Wymagania

- Python 3.x
- ComfyUI
- [Dodaj inne zależności]

## 📝 TODO

- [ ] Dodać obsługę kolejnych backendów
- [ ] Rozbudować postprocessing
- [ ] Dodać testy automatyczne