# Programmi in Python matematici e di altro tipo - Telecomunicazioni

🇮🇹 [Italiano](#italiano) | 🇬🇧 [English](#english)

<a id="italiano"></a>

## 🇮🇹 Italiano

### 📡 Descrizione

Raccolta di programmi in **Python** realizzati per la materia scolastica **Telecomunicazioni**, organizzati per moduli. Si va da un calcolatore da terminale per trigonometria e ottica (legge di Snell, angolo critico) fino a una dimostrazione interattiva della pipeline di un sistema di telecomunicazione digitale, applicata a un segnale audio registrato dal microfono.

### 📂 Contenuto

| Percorso | Descrizione |
|---|---|
| `Modulo 1/Calcolatore ottico e trigonometrico.py` | Calcolatore da terminale con menù: funzioni trigonometriche (sin, cos, tan in gradi e arcsin, arccos, arctan), legge di Snell `n1·sin(θ1) = n2·sin(θ2)` (calcola il dato mancante, lasciato vuoto) e angolo critico tra due mezzi. |
| `Modulo 1/requirements.txt` | Indica che lo script non richiede librerie esterne. |
| `Modulo 2/Pipeline di un sistema di telecomunicazione digitale.py` | Dimostrazione della pipeline di un sistema di telecomunicazione digitale (vedi sotto). |
| `Modulo 2/requirements.txt` | Dipendenze del Modulo 2: `colorama`, `matplotlib`, `numpy`, `rich`, `scipy`, `sounddevice`. |

**Cosa fa il programma del Modulo 2:**
1. Elenca i microfoni **WASAPI** disponibili e registra un segnale audio in **modalità esclusiva** (audio grezzo), con frequenza di campionamento, canali (mono/stereo) e durata scelti dall'utente (default: 48 kHz, stereo, 5 s).
2. Mostra forma d'onda, spettrogramma e spettro in frequenza (FFT) del segnale originale.
3. Applica un **filtro passa-banda Butterworth** (1000-4000 Hz) con amplificazione della banda di 10 dB.
4. **Ricampiona** a 8000 Hz la registrazione originale (coerente con il teorema di Nyquist) e la **amplifica** di 5 dB senza distorsione.
5. Esegue una **modulazione AM** del segnale amplificato con portante a 20 kHz.
6. Mostra i grafici del segnale elaborato (ricampionato e amplificato).

Ogni passaggio viene salvato come file `.wav` tramite una finestra di salvataggio (la cartella proposta è `Documenti/Registrazioni di suoni/...`).

### 🛠️ Tecnologie utilizzate

- **Python 3** (modulo `math` per il Modulo 1)
- **NumPy** e **SciPy** (filtri, ricampionamento, FFT, file WAV)
- **sounddevice** (registrazione audio via WASAPI)
- **Matplotlib** (grafici)
- **rich** e **colorama** (output colorato nel terminale)
- **tkinter** (finestra di salvataggio dei file)

### ▶️ Come eseguire

**Modulo 1** (nessuna dipendenza esterna):
```bash
cd "Modulo 1"
python "Calcolatore ottico e trigonometrico.py"
```

**Modulo 2:**
```bash
cd "Modulo 2"
pip install -r requirements.txt
python "Pipeline di un sistema di telecomunicazione digitale.py"
```

### 📋 Requisiti

- Python 3 (per il Modulo 2 è consigliato **Python 3.12 o superiore**, dato che il codice usa f-string con virgolette annidate)
- Per il Modulo 2: **Windows** con un microfono compatibile **WASAPI** (il programma usa la modalità esclusiva WASAPI) e `tkinter` disponibile (incluso di norma nell'installazione standard di Python)

### 👤 Autore

Realizzato da [MatteoMgr2008](https://github.com/MatteoMgr2008).

---

<a id="english"></a>

## 🇬🇧 English

### 📡 Description

A collection of **Python** programs written for the school subject **Telecommunications** (*Telecomunicazioni*), organised by module. It ranges from a terminal calculator for trigonometry and optics (Snell's law, critical angle) to an interactive demonstration of a digital telecommunication system pipeline, applied to an audio signal recorded from the microphone. The programs' interface and comments are in Italian.

### 📂 Contents

| Path | Description |
|---|---|
| `Modulo 1/Calcolatore ottico e trigonometrico.py` | Menu-driven terminal calculator: trigonometric functions (sin, cos, tan in degrees, and arcsin, arccos, arctan), Snell's law `n1·sin(θ1) = n2·sin(θ2)` (computes the missing value, left blank) and the critical angle between two media. |
| `Modulo 1/requirements.txt` | States that the script needs no external libraries. |
| `Modulo 2/Pipeline di un sistema di telecomunicazione digitale.py` | Demonstration of a digital telecommunication system pipeline (see below). |
| `Modulo 2/requirements.txt` | Module 2 dependencies: `colorama`, `matplotlib`, `numpy`, `rich`, `scipy`, `sounddevice`. |

**What the Module 2 program does:**
1. Lists the available **WASAPI** microphones and records an audio signal in **exclusive mode** (raw audio), with user-chosen sample rate, channels (mono/stereo) and duration (defaults: 48 kHz, stereo, 5 s).
2. Shows the waveform, spectrogram and frequency spectrum (FFT) of the original signal.
3. Applies a **Butterworth band-pass filter** (1000-4000 Hz) with a 10 dB boost of that band.
4. **Resamples** the original recording to 8000 Hz (consistent with the Nyquist theorem) and **amplifies** it by 5 dB without distortion.
5. Performs **AM modulation** of the amplified signal with a 20 kHz carrier.
6. Shows the plots of the processed (resampled and amplified) signal.

Each step is saved as a `.wav` file through a save dialog (the suggested folder is `Documents/Registrazioni di suoni/...`).

### 🛠️ Technologies used

- **Python 3** (`math` module for Module 1)
- **NumPy** and **SciPy** (filters, resampling, FFT, WAV files)
- **sounddevice** (audio recording via WASAPI)
- **Matplotlib** (plots)
- **rich** and **colorama** (coloured terminal output)
- **tkinter** (file save dialog)

### ▶️ How to run

**Module 1** (no external dependencies):
```bash
cd "Modulo 1"
python "Calcolatore ottico e trigonometrico.py"
```

**Module 2:**
```bash
cd "Modulo 2"
pip install -r requirements.txt
python "Pipeline di un sistema di telecomunicazione digitale.py"
```

### 📋 Requirements

- Python 3 (for Module 2 **Python 3.12 or later** is recommended, since the code uses f-strings with nested quotes)
- For Module 2: **Windows** with a **WASAPI**-compatible microphone (the program uses WASAPI exclusive mode) and `tkinter` available (normally included in the standard Python installation)

### 👤 Author

Made by [MatteoMgr2008](https://github.com/MatteoMgr2008).
