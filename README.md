# ComfyUI Automated Video Generator 🎬

Narzędzie do zautomatyzowanego generowania filmów przez API ComfyUI z obsługą tranzycji, sekwencji I2V i zaawansowanego przetwarzania.

[![GitHub](https://img.shields.io/badge/GitHub-abork75%2Fcomfyui--video--generator-blue)](https://github.com/abork75/comfyui-video-generator)

---

## 📋 Spis treści

- [Architektura](#-architektura)
- [Struktura projektu](#-struktura-projektu)
- [Instalacja](#-instalacja)
- [Szybki start](#-szybki-start)
- [Przykład użycia](#-przykład-użycia)
- [Dodawanie nowych backendów](#-dodawanie-nowych-backendów)
- [Troubleshooting](#-troubleshooting)
- [TODO](#-todo)

---

## 🏗️ Architektura

```
┌─────────────────────────────────────────────────────────────┐
│                     RUNS/projekt.py                          │
│              (Punkt wejścia użytkownika)                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                 batch_validator.py                           │
│            (Główny orkiestrator procesu)                     │
└──┬────────────────┬────────────────┬────────────────────────┘
   │                │                │
   ▼                ▼                ▼
┌──────────┐  ┌──────────┐   ┌──────────────┐
│  flow_   │  │ config_  │   │  workflow_   │
│ parser   │  │validator │   │    base      │
└────┬─────┘  └────┬─────┘   └──────┬───────┘
     │             │                 │
     └─────────────┴─────────────────┘
                   │
         ┌─────────┴──────────┐
         ▼                    ▼
   ┌───────────┐      ┌──────────────┐
   │ Backend   │      │ Workflows    │
   │ (local/   │      │ (JSON/YAML)  │
   │ cloud)    │      │              │
   └─────┬─────┘      └──────┬───────┘
         │                   │
         └─────────┬─────────┘
                   ▼
         ┌──────────────────┐
         │   ComfyUI API    │
         └─────────┬────────┘
                   ▼
         ┌──────────────────┐
         │  Postprocessing  │
         │  (merge, copy)   │
         └──────────────────┘
```

### Przepływ danych:

1. **Użytkownik** uruchamia skrypt z `RUNS/`
2. **batch_validator** orkiestruje cały proces
3. **flow_parser** sprawdza poprawność plików i struktury
4. **config_validator** waliduje materiały (formaty, proporcje)
5. **workflow_base** przygotowuje workflow z configów YAML
6. **Backend** (local/cloud) wysyła requesty do ComfyUI
7. **Postprocessing** łączy i przetwarza wygenerowane filmy

---

## 📁 Struktura projektu

```
comfyui-video-generator/
│
├── RUNS/                       # 🎯 Punkty wejścia dla projektów
│   ├── projekt_przyklad.py     # Przykładowy skrypt uruchomieniowy
│   └── ...                     # Twoje projekty
│
├── workflows/                  # 📄 Workflow ComfyUI (JSON)
│   ├── i2v_basic.json          # Podstawowy Image-to-Video
│   ├── transition_flow.json    # Workflow z tranzycjami
│   └── ...
│
├── workflow_configs/           # ⚙️ Konfiguracje workflow (YAML)
│   ├── i2v_config.yaml
│   └── transition_config.yaml
│
├── backends/                   # 🔌 Implementacje backendów
│   ├── local/                  # Backend lokalny
│   │   ├── __init__.py
│   │   └── local_backend.py
│   └── replicate/              # (TODO) Backend Replicate
│
├── helpers/                    # 🛠️ Funkcje pomocnicze
│   ├── file_utils.py
│   ├── video_utils.py
│   └── ...
│
├── postprocessing/             # 🎞️ Postprocessing wideo
│   ├── merge_videos.py
│   ├── copy_outputs.py
│   └── ...
│
├── utils/                      # 🔧 Narzędzia dodatkowe
│
├── logs/                       # 📋 Logi aplikacji (git-ignorowane)
│
├── batch_validator.py          # 🎼 Główny orkiestrator
├── flow_parser.py              # ✅ Walidacja flow i plików
├── workflow_base.py            # 🏗️ Bazowa klasa workflow
├── config_validator.py         # 🔍 Walidacja materiałów
│
├── .gitignore                  # 🚫 Ignorowane pliki
└── README.md                   # 📖 Ta dokumentacja
```

---

## 🚀 Instalacja

### Wymagania:

- Python 3.8+
- ComfyUI (uruchomiony lokalnie lub dostęp do API)
- ffmpeg (dla postprocessingu wideo)

### Instalacja zależności:

```bash
# Klonuj repozytorium
git clone https://github.com/abork75/comfyui-video-generator.git
cd comfyui-video-generator

# Zainstaluj zależności Python
pip install -r requirements.txt

# (Opcjonalnie) Utwórz virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# LUB
.\venv\Scripts\activate   # Windows
```

---

## ⚡ Szybki start

### 1. Przygotuj materiały wejściowe

```
projekty/moj_projekt/
├── images/
│   ├── frame_001.png
│   ├── frame_002.png
│   └── ...
└── videos/
    └── source_video.mp4
```

### 2. Utwórz skrypt w `RUNS/`

```python name=RUNS/moj_projekt.py
"""
Przykładowy skrypt generowania sekwencji wideo
"""
from batch_validator import BatchValidator

# Konfiguracja projektu
config = {
    "project_name": "moj_projekt",
    "input_dir": "D:/projekty/moj_projekt/images",
    "output_dir": "D:/output/moj_projekt",
    "workflow": "i2v_basic",
    "backend": "local",
    "settings": {
        "resolution": "1024x576",
        "fps": 24,
        "duration": 3
    }
}

# Uruchom walidację i generowanie
validator = BatchValidator(config)
validator.run()
```

### 3. Uruchom generowanie

```bash
python RUNS/moj_projekt.py
```

### 4. Zobacz wyniki

Wygenerowane filmy znajdziesz w `output_dir` z konfiguracji.

---

## 📚 Przykład użycia

### Scenariusz: Generowanie sekwencji I2V z tranzycjami

**Cel:** Wygenerować film z 10 obrazów z płynnymi tranzycjami między nimi.

#### Krok 1: Struktura katalogów

```
D:/projekty/sekwencja_01/
├── images/
│   ├── 001.png  (1024x576)
│   ├── 002.png  (1024x576)
│   └── ...      (10 plików)
```

#### Krok 2: Skrypt uruchomieniowy

```python name=RUNS/sekwencja_tranzycje.py
from batch_validator import BatchValidator

config = {
    "project_name": "sekwencja_01",
    "input_dir": "D:/projekty/sekwencja_01/images",
    "output_dir": "D:/output/sekwencja_01",
    
    # Workflow z tranzycjami
    "workflow": "transition_flow",
    "workflow_config": "workflow_configs/transition_config.yaml",
    
    # Backend
    "backend": "local",
    "comfyui_url": "http://127.0.0.1:8188",
    
    # Ustawienia
    "settings": {
        "resolution": "1024x576",
        "fps": 24,
        "transition_frames": 16,  # 16 klatek tranzycji
        "video_duration": 3,       # 3 sekundy na segment
    },
    
    # Postprocessing
    "postprocess": {
        "merge_videos": True,
        "output_filename": "sekwencja_final.mp4"
    }
}

# Walidacja materiałów
print("🔍 Walidacja materiałów...")
validator = BatchValidator(config)

if validator.validate_materials():
    print("✅ Materiały poprawne!")
    
    # Uruchom generowanie
    print("🎬 Rozpoczynam generowanie...")
    validator.run()
    
    print("✨ Gotowe!")
else:
    print("❌ Błędy w materiałach!")
    validator.print_errors()
```

#### Krok 3: Uruchomienie

```bash
python RUNS/sekwencja_tranzycje.py
```

#### Krok 4: Rezultat

```
✅ Materiały poprawne!
🎬 Rozpoczynam generowanie...
   [1/10] Generowanie segmentu 001-002... ✓
   [2/10] Generowanie segmentu 002-003... ✓
   ...
   [10/10] Generowanie segmentu 009-010... ✓
🎞️ Łączenie segmentów...
✨ Gotowe! Film zapisany: D:/output/sekwencja_01/sekwencja_final.mp4
```

---

## 🔌 Dodawanie nowych backendów

Generator jest zaprojektowany z myślą o rozszerzalności. Możesz łatwo dodać nowe backendy (Replicate, RunPod, Vast.ai, itp.).

### Krok 1: Utwórz katalog backendu

```
backends/
└── mojbackend/
    ├── __init__.py
    └── mojbackend_backend.py
```

### Krok 2: Implementuj bazową klasę

```python name=backends/mojbackend/mojbackend_backend.py
from backends.base_backend import BaseBackend

class MojBackendBackend(BaseBackend):
    """
    Backend dla MojBackend API
    """
    
    def __init__(self, config):
        super().__init__(config)
        self.api_key = config.get('api_key')
        self.endpoint = config.get('endpoint', 'https://api.mojbackend.com')
    
    def send_workflow(self, workflow_json, inputs):
        """
        Wysyła workflow do MojBackend API
        
        Args:
            workflow_json: Dict z workflow ComfyUI
            inputs: Dict z inputami (obrazy, parametry)
            
        Returns:
            job_id: ID zadania w kolejce
        """
        # Twoja implementacja
        response = requests.post(
            f"{self.endpoint}/run",
            json={
                "workflow": workflow_json,
                "inputs": inputs
            },
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        
        return response.json()['job_id']
    
    def check_status(self, job_id):
        """
        Sprawdza status zadania
        
        Returns:
            status: 'pending', 'running', 'completed', 'failed'
        """
        response = requests.get(
            f"{self.endpoint}/status/{job_id}",
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        
        return response.json()['status']
    
    def download_result(self, job_id, output_path):
        """
        Pobiera wynik generowania
        """
        # Implementacja pobierania
        pass
```

### Krok 3: Zarejestruj backend

```python name=backends/__init__.py
from backends.local.local_backend import LocalBackend
from backends.mojbackend.mojbackend_backend import MojBackendBackend

BACKENDS = {
    'local': LocalBackend,
    'mojbackend': MojBackendBackend,
}

def get_backend(backend_name, config):
    """
    Factory function dla backendów
    """
    if backend_name not in BACKENDS:
        raise ValueError(f"Unknown backend: {backend_name}")
    
    return BACKENDS[backend_name](config)
```

### Krok 4: Użyj nowego backendu

```python
config = {
    "backend": "mojbackend",
    "backend_config": {
        "api_key": "twoj-api-key",
        "endpoint": "https://api.mojbackend.com"
    },
    # ... reszta konfiguracji
}
```

### Wymagane metody w backendzie:

| Metoda | Opis | Wymagana? |
|--------|------|-----------|
| `__init__(config)` | Inicjalizacja backendu | ✅ TAK |
| `send_workflow(workflow, inputs)` | Wysyłanie workflow | ✅ TAK |
| `check_status(job_id)` | Sprawdzanie statusu | ✅ TAK |
| `download_result(job_id, path)` | Pobieranie wyniku | ✅ TAK |
| `validate_connection()` | Testowanie połączenia | ⚠️ Opcjonalne |
| `estimate_cost(workflow)` | Szacowanie kosztów | ⚠️ Opcjonalne |

---

## 🔧 Troubleshooting

### Problem: `FileNotFoundError: No such file or directory`

**Przyczyna:** Ścieżki do plików są nieprawidłowe lub pliki nie istnieją.

**Rozwiązanie:**
1. Sprawdź ścieżki w konfiguracji:
   ```python
   import os
   print(os.path.exists("D:/projekty/moj_projekt/images"))
   ```
2. Użyj bezwzględnych ścieżek (nie relatywnych)
3. Upewnij się że separatory katalogów są poprawne (Windows: `/` lub `\\`)

---

### Problem: `Invalid resolution: expected 16:9, got 4:3`

**Przyczyna:** Obrazy wejściowe mają niepoprawne proporcje.

**Rozwiązanie:**
```bash
# Sprawdź proporcje obrazów
python config_validator.py --check-aspect-ratio

# Automatyczne przycinanie
python helpers/resize_images.py --aspect-ratio 16:9 --input images/
```

---

### Problem: `ComfyUI connection timeout`

**Przyczyna:** ComfyUI nie jest uruchomiony lub jest niedostępny.

**Rozwiązanie:**
1. Sprawdź czy ComfyUI działa:
   ```bash
   curl http://127.0.0.1:8188/system_stats
   ```
2. Uruchom ComfyUI:
   ```bash
   cd ComfyUI
   python main.py
   ```
3. Sprawdź firewall/porty

---

### Problem: `Memory error during generation`

**Przyczyna:** Za mało pamięci GPU/RAM.

**Rozwiązanie:**
1. Zmniejsz rozdzielczość:
   ```python
   "settings": {
       "resolution": "768x432",  # zamiast 1024x576
   }
   ```
2. Zmniejsz batch size
3. Użyj backendu cloud zamiast local

---

### Problem: Workflow nie działa poprawnie

**Przyczyna:** Niekompatybilna wersja ComfyUI lub brakujące custom nodes.

**Rozwiązanie:**
1. Sprawdź wymagane custom nodes:
   ```python
   python flow_parser.py --check-nodes workflow.json
   ```
2. Zaktualizuj ComfyUI:
   ```bash
   cd ComfyUI
   git pull
   ```
3. Zainstaluj brakujące nodes przez ComfyUI Manager

---

### Debugowanie krok po kroku

```bash
# 1. Walidacja materiałów
python config_validator.py --config RUNS/moj_projekt.py

# 2. Test połączenia z backend
python backends/test_connection.py --backend local

# 3. Uruchom z verbose logging
python RUNS/moj_projekt.py --verbose --log-level DEBUG

# 4. Zobacz szczegółowe logi
tail -f logs/batch_validator.log
```

---

## 📊 Logi i monitoring

Wszystkie logi są zapisywane w katalogu `logs/`:

```
logs/
├── batch_validator.log      # Główny log orkiestratora
├── flow_parser.log          # Log walidacji flow
├── backend_local.log        # Log backendu
└── YYYY-MM-DD_projekt.log   # Logi konkretnych runów
```

**Format logów:**
```
[2026-02-19 14:23:45] [INFO] batch_validator: Starting generation for project: moj_projekt
[2026-02-19 14:23:46] [DEBUG] flow_parser: Validating 10 input files
[2026-02-19 14:23:47] [INFO] local_backend: Sending workflow to ComfyUI at http://127.0.0.1:8188
```

---

## 🎯 TODO

### Backlendy do dodania:
- [ ] Replicate backend
- [ ] RunPod backend  
- [ ] Vast.ai backend

### Features:
- [ ] WebUI do zarządzania projektami
- [ ] Kolejkowanie zadań (job queue)
- [ ] Automatyczne resume po błędzie
- [ ] Szacowanie czasu i kosztów generowania
- [ ] Export do różnych formatów (MP4, WebM, GIF)

### Postprocessing:
- [ ] Automatyczna stabilizacja wideo
- [ ] Color grading
- [ ] Upscaling (RealESRGAN, Topaz)
- [ ] Audio synchronization

### Dokumentacja:
- [ ] Tutorial wideo
- [ ] Przykładowe projekty
- [ ] API documentation (Sphinx)

---

## 📞 Kontakt i wsparcie

- **Issues:** [github.com/abork75/comfyui-video-generator/issues](https://github.com/abork75/comfyui-video-generator/issues)
- **Discussions:** [github.com/abork75/comfyui-video-generator/discussions](https://github.com/abork75/comfyui-video-generator/discussions)

---

## 📄 Licencja

[Dodaj licencję jeśli potrzebna, np. MIT]

---

**Utworzone z ❤️ dla automatyzacji ComfyUI**