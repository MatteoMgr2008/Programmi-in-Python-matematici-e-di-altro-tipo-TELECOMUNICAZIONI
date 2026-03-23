import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from scipy.io.wavfile import read
from scipy.signal import butter, lfilter
import os
from colorama import Fore, Style
import tkinter as tk
from tkinter import filedialog
import time
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.live import Live
from rich.console import Group
import random
import matplotlib.pyplot as plt 
from scipy.signal import resample
from scipy.fft import fft, fftfreq
import textwrap
import matplotlib.font_manager as fm
import warnings

# Verifica la disponibilità del font Arial sul dispositivo
font_disponibili_device=[font.name for font in fm.fontManager.ttflist]

# Imposta Arial come font principale se disponibile nel dispositivo
if "Arial" in font_disponibili_device:
    plt.rcParams["font.family"]="Arial"
# Altrimenti usa il font DejaVu Sans come prima alternativa
elif "DejaVu Sans" in font_disponibili_device:
    plt.rcParams["font.family"]="DejaVu Sans"
# Se nessuno dei due font è disponibile nel dispositivo, matplotlib sceglierà automaticamente un font sans-serif
else:
    plt.rcParams["font.family"]="sans-serif"

# Salva il font effettivamente utilizzato per i grafici
font_grafici_utilizzato=plt.rcParams["font.family"]

# Configura le dimensioni dei testi nei grafici matplotlib
plt.rcParams["font.size"]=18 # Testo generale
plt.rcParams["axes.titlesize"]=20 # Grandezza titolo grafico
plt.rcParams["axes.titleweight"]="medium" # Grandezza titolo grafico
plt.rcParams["axes.titlecolor"]="#4d4d4d" # Colore titolo grafico
plt.rcParams["axes.labelsize"]=14 # Etichette assi X e Y
plt.rcParams["xtick.labelsize"]=12 # Numeri asse X
plt.rcParams["ytick.labelsize"]=12 # Numeri asse Y

# Crea un'istanza di Console per output formattati con colori e stili (per la libreria rich)
output_terminale=Console()

def introduzione_programma():
    print(Fore.RED+"Benvenuto nella dimostrazione di una pipeline di un sistema di telecomunicazione digitale!"+Style.RESET_ALL)
    print("In questo programma è possibile visualizzare un esempio di pipeline di un sistema di telecomunicazione digitale!")
    elementi_pipeline_sistema_tel=[
        "[blue bold]Sorgente[/blue bold]",
        "[green bold]Codifica di sorgente[/green bold]",
        "[cyan bold]Codifica di canale[/cyan bold]",
        "[magenta bold]Modulazione[/magenta bold]",
        "[yellow bold]Trasmissione[/yellow bold]"
    ]
    colori_elem_pipeline_sist_tel=["blue", "green", "cyan", "magenta", "yellow"]
    print("In generale i passaggi principali della pipeline di un sistema di telecomunicazione digitale sono i seguenti:")
    for i, elemento_pipeline_sistema_tel in enumerate(elementi_pipeline_sistema_tel, 1):
        colore_elem_pipeline_sist_tel=colori_elem_pipeline_sist_tel[i-1]
        output_terminale.print(f"[{colore_elem_pipeline_sist_tel} bold]{i})[/{colore_elem_pipeline_sist_tel} bold] {elemento_pipeline_sistema_tel}")
    print()
    print(f"Per prima cosa è necessario registrare un segnale audio tramite un {Fore.GREEN}microfono di tipo WASAPI in modalità esclusiva.{Style.RESET_ALL}")
    print(f"{Fore.RED}=== Perché WASAPI in modalità esclusiva? ==={Style.RESET_ALL} {Fore.BLUE}W{Fore.MAGENTA}A{Fore.YELLOW}S{Fore.GREEN}API{Style.RESET_ALL} ({Fore.BLUE}Windows {Fore.MAGENTA}Audio {Fore.YELLOW}Session {Fore.GREEN}API{Style.RESET_ALL}) è l'interfaccia audio di Windows. La {Fore.GREEN}modalità ESCLUSIVA{Style.RESET_ALL} permette l'accesso diretto al microfono, bypassando il mixer audio di Windows. Questo garantisce: audio completamente grezzo e non processato, latenza minima e nessuna alterazione del segnale da parte del sistema. Ideale per analisi di segnali in telecomunicazioni!")

def mostra_lista_microfoni_wasapi():
    # Mostra solo i microfoni di tipo WASAPI disponibili nel device
    print()
    print("Sono dispobili i seguenti microfoni di tipo WASAPI nel device e perciò utilizzabili da questo programma:")
    print()
    
    lista_microfoni_wasapi=[]
    dizionario_colori_device={}
    api_host_disponibii=sd.query_hostapis() # Ottiene le API host disponibili
    
    # Trova l'indice dell'host API WASAPI
    indice_wasapi_hostapi=None # Indice dell'host API WASAPI
    for i, api in enumerate(api_host_disponibii):
        if "WASAPI" in api["name"]:
            indice_wasapi_hostapi=i # Salva l'indice trovato
            break
    
    # Condizione in cui non è stato trovato alcun host API WASAPI nel device
    if indice_wasapi_hostapi is None:
        print("Nessun microfono di tipo WASAPI disponibile su questo dispositivo!")
        print("È altamente consigliato provare ad utilizzare un microfono esterno o a ravviare il dispositivo se non viene riconosciuto un microfono del device.")
        esci_o_ricomincia()
        
        return [], {}
    
    device_disponibili=sd.query_devices() # Ottiene tutti i microfoni disponibili nel device
    colori_disponibili=["red", "green", "yellow", "blue", "magenta", "cyan", "white", "bright_black", "bright_red", "bright_green", "bright_yellow", "bright_blue", "bright_magenta", "bright_cyan", "bright_white"]
    for i, device in enumerate(device_disponibili):
        # Verifica se è un microfono di tipo WASAPI (cioè con input con host API WASAPI)
        if device["max_input_channels"]>0 and device["hostapi"]==indice_wasapi_hostapi:
            lista_microfoni_wasapi.append((i, device))
            device_default=("Device di default: " if i==sd.default.device[0]
                              else "  ")
            colore_random_device=random.choice(colori_disponibili)
            dizionario_colori_device[i]=colore_random_device
            output_terminale.print(f"{device_default}[{colore_random_device} bold]ID {i:2d}[/{colore_random_device} bold] - {device["name"]}")
    
    return lista_microfoni_wasapi, dizionario_colori_device

def creazione_directory_salvataggio_file_wav(titolo_finestra_salvataggio, nome_file, directory_file, tipologia_segnale_audio):
    # Aggiunge un delay di 0,5 secondi per dare un po' di tempo all'utente al fine di leggere il messaggio 
    # precedente prima di indicare dove salvare il file della registrazione del segnale audio
    time.sleep(0.5)
    # Crea l'istanza principale della finestra tkinter 
    # (necessaria per aprire la finestra di salvataggio del file della registrazione del segnale audio)
    root=tk.Tk()
    # Nasconde la finestra principale di tkinter all'utente 
    # (mostra solo la finestra di salvataggio del file della registrazione del segnale audio)
    root.withdraw()
    # Tenta di impostare le nuove dimensioni della finestra di salvataggio del file della registrazione
    root.geometry("1000x700")
    # Tenta di mantenere la finestra sempre in primo piano rispetto ad altri programmi aperti
    root.attributes("-topmost", True)
    # Tenta di portare la finestra in primo piano rispetto ad altri programmi aperti
    root.lift()
    directory_registrazioni_segnali_audio=os.path.expanduser(
        f"~/Documents/Registrazioni di suoni/{directory_file}"
        )
    os.makedirs(directory_registrazioni_segnali_audio, exist_ok=True)
    timestamp_registrazione=datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    path_file_segnale_audio=filedialog.asksaveasfilename(
        defaultextension=".wav",
        filetypes=[("File WAV", "*.wav"), ("Tutti i file", "*.*")],
        title=titolo_finestra_salvataggio,
        initialfile=f"{nome_file}_{timestamp_registrazione}.wav",
        initialdir=directory_registrazioni_segnali_audio,
        confirmoverwrite=True # Chiede conferma prima di sovrascrivere il file della registrazione 
                              # (di default è True)
    )
    root.destroy()
    
    if not path_file_segnale_audio:
        print()
        print(Fore.RED+textwrap.dedent(f"""\
            La selezione della directory per il salvataggio del segnale audio
            {tipologia_segnale_audio} è stata annullata!
            """).replace("\n", " ").strip()+Style.RESET_ALL)
        esci_o_ricomincia()
    else:
        print()
        print(Fore.GREEN+textwrap.dedent(f"""\
            La directory per il salvataggio del segnale audio
            {tipologia_segnale_audio} è stata indicata correttamente!
            """).replace("\n", " ").strip()+Style.RESET_ALL)
        print()
    
    return path_file_segnale_audio, tipologia_segnale_audio

# Funzione principale per la registrazione del segnale audio
def registra_segnale_audio():
    # Mostra microfoni di tipo WASAPI disponibili nel device
    microfoni, colori_device=mostra_lista_microfoni_wasapi()
    print()
    
    # Selezione del microfono di tipo WASAPI da utilizzare
    print("È innanzitutto necessario scegliere quale microfono di tipo WASAPI utilizzare.")
    scelta_microfono=input(textwrap.dedent(f"""\
                                           Inserire il numero del dispositivo che si desidera utilizzare
                                           {Fore.CYAN}(premere INVIO per selezionare il primo microfono
                                           della lista){Style.RESET_ALL}:                                           
                                           """).replace("\n", " ").strip()+" ")
    if scelta_microfono:
        id_device=int(scelta_microfono)
        nome_device=None
        for id_microfono, info_microfono in microfoni:
            if id_microfono==id_device:
                nome_device=info_microfono["name"]
                break
    else:
        id_device=microfoni[0][0]
        nome_device=microfoni[0][1]["name"] # Salva il nome del primo microfono della lista     
                                            # (selezionato di default)

    colore_device=colori_device.get(id_device, "white") # Recupera il colore casuale del dispositivo
    output_terminale.print(textwrap.dedent(f"""\
                           Il dispositivo selezionato è il seguente: [bold]{nome_device}[/bold] [{colore_device}
                           bold](ID: {id_device})[/{colore_device} bold]
                           """).replace("\n", " ").strip())
    print()
        
    # Selezione del valore della frequenza di campionamento
    print("Dopo è necessario scegliere quale frequenza di campionamento si desidera utlizzare")
    scelta_freq_campionamento=input(textwrap.dedent(f"""\
                                                    Inserire il valore in Hz della frequenza di campionamento
                                                    che si desidera utilizzare {Fore.CYAN}(premere INVIO per
                                                    inserire il valore di default pari a 48000 Hz ovvero a
                                                    48 kHz){Style.RESET_ALL}:
                                                    """).replace("\n", " ").strip()+" ")
    if scelta_freq_campionamento:
        valore_freq_campionamento=int(scelta_freq_campionamento)
    else:
        freq_campionamento_default=48000
        valore_freq_campionamento=freq_campionamento_default
    print()
    
    # Selezione dei canali audio (mono o stereo)
    print("Successivamente è necessario scegliere quale canale audio si desidera utilizzare")
    scelta_canali_audio=input(textwrap.dedent(f"""\
                                              Inserire il valore 1 per selezionare il canale mono oppure
                                              inserire il valore 2 per selezionare il canale stereo
                                              {Fore.CYAN}(premere INVIO per inserire il valore di default
                                              pari a 2, ovvero per selezionare il canale stereo){Style.RESET_ALL}:
                                              """).replace("\n", " ").strip()+" ")
    if scelta_canali_audio:
        canali_audio=int(scelta_canali_audio)
    else:
        canali_audio_default=2
        canali_audio=canali_audio_default
    print()
    
    # Selezione della durata della registrazione
    print(textwrap.dedent(f"""\
                          Poi, è necessario inserire la durata in secondi che si desidera applicare
                          alla registrazione del segnale audio
                          """).replace("\n", " ").strip())
    scelta_durata_registrazione=input(textwrap.dedent(f"""\
                                            Inserire la durata della registrazione in secondi
                                            {Fore.CYAN}(premere INVIO per inserire il valore di default
                                            pari a 5 secondi){Style.RESET_ALL}:
                                            """).replace("\n", " ").strip()+" ")
    if scelta_durata_registrazione:
        durata_registrazione=float(scelta_durata_registrazione)
    else:
        durata_registrazione_default=5
        durata_registrazione=durata_registrazione_default
    print()
    
    # Salvataggio del file audio in formato WAV della registrazione finale
    print(textwrap.dedent(f"""\
                          Infine è necessario salvare la registrazione in formato WAV nel device
                          o in un supporto d'archiviazione esterno
                          """).replace("\n", " ").strip())
    path_file_registrazione_non_processato,\
    tipologia_segnale_audio=creazione_directory_salvataggio_file_wav(
        titolo_finestra_salvataggio="Salvataggio del segnale audio non processato",
        nome_file="registrazione_segnale_audio_non_processato",
        directory_file="Registrazioni di segnali audio non processati",
        tipologia_segnale_audio="non processato"
    )
    
    # Riepilogo di tutti i parametri inseriti per la registrazione del segnale audio
    print("Ecco infine il riepilogo di tutti i parametri inseriti per la registrazione del segnale audio:")
    print()
    table=Table(show_header=False, border_style="red", padding=(0, 2), show_lines=True)
    table.add_column("Parametro", style="bold", no_wrap=True)
    table.add_column("Valore")
    table.add_row("[cyan]Microfono (dispositivo)[/cyan]",
                  f"{nome_device} [{colore_device} bold](ID: {id_device})[/{colore_device} bold]")
    table.add_row("[magenta]Modalità[/magenta]", "WASAPI ESCLUSIVO (audio grezzo non processato)")
    table.add_row("[yellow]Frequenza di campionamento[/yellow]", f"{valore_freq_campionamento} Hz")
    table.add_row("[green]Canali audio[/green]", 
                  f"{"Mono" if canali_audio==1 else "Stereo"} ({canali_audio} canali audio)")
    table.add_row("[blue]Durata della registrazione[/blue]", f"{durata_registrazione} secondi")
    table.add_row("[red]Directory file audio[/red]", path_file_registrazione_non_processato)
    output_terminale.print(table)
    print()
    
    # Input necessario per l'inizio della registrazione del segnale audio
    print()
    output_terminale.print(
        textwrap.dedent(f"""\
                        [bright_cyan bold on blue]Premere INVIO per iniziare la registrazione
                        del segnale audio ([bright_yellow]{durata_registrazione} secondi[/bright_yellow])
                        [/bright_cyan bold on blue]
                        """).replace("\n", " ").strip()+" ",
        justify="center"
    )
    input()
    print()
    
    # Settaggi per la registrazione effettiva del segnale audio
    try:
        wasapi_settings=sd.WasapiSettings(exclusive=True)
        segnale_audio=sd.rec(
            round(durata_registrazione*valore_freq_campionamento),
            samplerate=valore_freq_campionamento,
            channels=canali_audio,
            dtype="int16",
            device=id_device,
            extra_settings=wasapi_settings
        )
        
        # Messaggio di inizio registrazione del segnale audio con countdown
        with Live(refresh_per_second=30) as live:
            for sec_rimanenti_countdown in range(int(durata_registrazione), -1, -1):
                if sec_rimanenti_countdown==1:
                    dicitura_secondi="SECONDO"
                else:
                    dicitura_secondi="SECONDI"
                elementi_pannello_countdown_reg=Group(  
                    Align.center("[red bold]🔴 REGISTRAZIONE DEL SEGNALE AUDIO IN CORSO 🔴[/red bold]"),
                    Align.center(textwrap.dedent(f"""\
                                                 [yellow bold]TEMPO RIMANENTE: {sec_rimanenti_countdown}
                                                 {dicitura_secondi}[/yellow bold]
                                                 """).replace("\n", " ").strip())
                )
                pannello_countdown_registrazione=Panel(
                    elementi_pannello_countdown_reg,
                    style="bold red on black",
                    expand=True
                )
                live.update(pannello_countdown_registrazione)
                time.sleep(1)
        
        # Aspetta che la registrazione del segnale audio termini
        sd.wait()
        print()
        print()
        
        # Salva il file nella path indicata in precedenza dall'utente
        write(path_file_registrazione_non_processato, valore_freq_campionamento, segnale_audio)
        
        # Messaggio di conferma del completamento della registrazione del segnale audio e del salvataggio
        print(textwrap.dedent(f"""\
            {Fore.GREEN}La registrazione del segnale audio è avvenuta con successo!{Style.RESET_ALL}
            Il file audio in formato WAV {tipologia_segnale_audio} della registrazione del segnale audio
            è stato salvato, come indicato in precedenza, nella seguente directory con successo:
            {Fore.RED}{path_file_registrazione_non_processato}{Style.RESET_ALL}
            """).replace("\n", " ").strip())

    # Gestione degli errori durante la registrazione del segnale audio
    except Exception as e:
        print(f"Non è stato possibile registrare il segnale audio della durata di {durata_registrazione} secondi a causa del seguente errore: {e}")

    return path_file_registrazione_non_processato

def processing_audio(path_file_segnale_audio):
    # Carica il file del segnale audio salvato in WAV e restituisce la frequenza 
    # di campionamento e i campioni del segnale audio
    frequenza_campionamento_audio, dati_audio=importa_file_wav(path_file_segnale_audio)
    
    # Normalizza il segnale audio in "float32" nell'intervallo [-1, 1] se necessario
    if dati_audio.dtype!=np.float32:
        dati_audio=dati_audio.astype(np.float32)/np.max(np.abs(dati_audio))
    
    # Applica un filtro di tipo band-pass (passa-banda) tra 1000 e 4000 Hz
    frequenza_bassa=1000/(frequenza_campionamento_audio/2)
    frequenza_alta=4000/(frequenza_campionamento_audio/2)
    
    # Crea un filtro di tipo "Butterworth" passa-banda di ordine 4
    # (Butterworth significa che la banda utile è piatta, quindi è senza la presenza di ondine)
    coeff_numeratore, coeff_denominatore=butter(4, [frequenza_bassa, frequenza_alta], btype="band")
    segnale_filtrato_passa_banda=lfilter(coeff_numeratore, coeff_denominatore, dati_audio)
    
    # Applica un guadagno al segnale filtrato (amplificazione di 10 dB)
    guadagno=10**(10/20) # È pari a ≈ 3,16
    banda_amplificata=segnale_filtrato_passa_banda*guadagno
    
    # Somma il segnale amplificato al segnale audio originale
    segnale_audio_uscita=dati_audio+banda_amplificata
    
    # Limita l'ampiezza del segnale per evitare il fenomeno di distorsione del segnale audio (clipping)
    segnale_audio_uscita=np.clip(segnale_audio_uscita, -1.0, 1.0)
    
    # Salva il segnale audio processato in formato WAV
    path_file_registrazione_processato,\
    tipologia_segnale_audio=creazione_directory_salvataggio_file_wav(
        titolo_finestra_salvataggio="Salvataggio del segnale audio processato",
        nome_file="registrazione_segnale_audio_processato",
        directory_file="Registrazioni di segnali audio processati",
        tipologia_segnale_audio="processato"
    )
    write(path_file_registrazione_processato, frequenza_campionamento_audio, segnale_audio_uscita)
    
    # Messaggio di conferma del completamento dell'elaborazione del segnale audio e del salvataggio
    print(textwrap.dedent(f"""\
        {Fore.GREEN}Il segnale audio della registrazione è stato processato con successo!{Style.RESET_ALL}
        Il file audio in formato WAV {tipologia_segnale_audio} del segnale audio è stato salvato,
        come indicato in precedenza, nella seguente directory con successo:
        {Fore.RED}{path_file_registrazione_processato}{Style.RESET_ALL}
        """).replace("\n", " ").strip())
    
def importa_file_wav(path_file_segnale_audio):
    frequenze_campionamento, dati_audio=read(path_file_segnale_audio)
    
    return frequenze_campionamento, dati_audio

def ricampionamento_audio(path_file_segnale_audio, frequenza_camp_nuova):
    # Importa il file audio del segnale audio originale
    frequenza_camp_originale, dati_audio=importa_file_wav(path_file_segnale_audio)
    
    # Calcola il numero di campioni nel segnale campionato
    num_campioni_segnale_camp=int(len(dati_audio)*frequenza_camp_nuova/frequenza_camp_originale)
    
    # Ricampiona il segnale audio
    dati_audio_ricampionati=resample(dati_audio, num_campioni_segnale_camp)
    
    # Salva il segnale ricampionato in un nuovo file WAV
    path_file_segnale_audio_ricampionato,\
    tipologia_segnale_audio=creazione_directory_salvataggio_file_wav(
        titolo_finestra_salvataggio="Salvataggio del segnale audio ricampionato",
        nome_file="registrazione_segnale_audio_ricampionato",
        directory_file="Registrazioni di segnali audio ricampionati",
        tipologia_segnale_audio="ricampionato"
    )
    write(path_file_segnale_audio_ricampionato, 
          frequenza_camp_nuova, 
          dati_audio_ricampionati.astype(np.int16))
    
    # Messaggio di conferma del completamento dell'elaborazione del segnale audio e del salvataggio
    print(textwrap.dedent(f"""\
        {Fore.GREEN}Il segnale audio è stato ricampionato con successo!{Style.RESET_ALL}
        Il file audio in formato WAV {tipologia_segnale_audio} della registrazione del segnale
        audio è stato salvato, come indicato in precedenza, nella seguente directory con successo:
        {Fore.RED}{path_file_segnale_audio_ricampionato}{Style.RESET_ALL}
        """).replace("\n", " ").strip())
    
    return path_file_segnale_audio_ricampionato, frequenza_camp_nuova, dati_audio_ricampionati

# Amplifica un segnale audio in dB senza distorsione e supporta i segnali mono e stereo
def amplificazione_audio(dati_audio, fattore_db=10):
    # Normalizza in float [-1,1]
    if dati_audio.dtype!=np.float32:
        dati_audio=dati_audio.astype(np.float32)
        dati_audio/=np.max(np.abs(dati_audio))
    
    # Converte il guadagno in scala lineare
    guadagno_lineare=10**(fattore_db/20)
    
    # Applica il guadagno al segnale audio da amplificare
    segnale_audio_amplificato=dati_audio*guadagno_lineare
    
    # Se qualche valore dovesse superare [-1,1], normalizza tutto per evitare 
    # il fenomeno di distorsione
    valore_massimo=np.max(np.abs(segnale_audio_amplificato))
    if valore_massimo>1.0:
        segnale_audio_amplificato/=valore_massimo
    
    return segnale_audio_amplificato

# Esegue una modulazione AM sul file audio dato, supporta segnali 
# mono/stereo e restituisce il percorso del file salvato
def modulazione_am(path_file_audio, freq_campionamento):
    
    # Importa il file audio del segnale audio originale
    frequenza_campionamento_originale, dati_audio=importa_file_wav(path_file_audio)
    
    # Normalizza i dati audio in formato float nell'intervallo [-1, 1]
    if dati_audio.dtype!=np.float32:
        dati_audio=dati_audio.astype(np.float32)
        dati_audio/=np.max(np.abs(dati_audio))
    
    # Calcola il numero totale di campioni del segnale audio
    num_campioni_segnale_audio=dati_audio.shape[0]
    
    # Crea l'array temporale per la modulazione
    array_tempo=np.arange(num_campioni_segnale_audio)/frequenza_campionamento_originale # (N,) indica un array monodimensionale con N elementi
    
    # Definisce la frequenza (segnale del coseno) della portante per la modulazione AM (in questo caso 20 kHz = 20000 Hz)
    frequenza_portante=20000
    
    # Calcola il segnale modulato AM applicando la portante
    # Se il segnale è stereo, trasforma array_tempo in colonna per il broadcasting
    # corretto (broadcasting = operazione automatica di NumPy che adatta le dimensioni
    # degli array per permettere operazioni elemento per elemento)
    if len(dati_audio.shape)>1:
        segnale_audio_modulato=(1+dati_audio)*np.cos(2*np.pi*frequenza_portante*array_tempo)[:, None]
    else:
        segnale_audio_modulato=(1+dati_audio)*np.cos(2*np.pi*frequenza_portante*array_tempo)
    
    # Limita l'ampiezza del segnale modulato nell'intervallo [-1, 1] per evitare il fenomeno di distorsione (clipping)
    segnale_audio_modulato=np.clip(segnale_audio_modulato, -1.0, 1.0)
    
    # Salva il segnale audio modulato AM in un nuovo file WAV
    path_file_segnale_audio_modulato, tipologia_segnale_audio=creazione_directory_salvataggio_file_wav(
        titolo_finestra_salvataggio="Salvataggio del segnale audio modulato AM",
        nome_file="registrazione_segnale_audio_modulato_AM",
        directory_file="Registrazioni di segnali audio modulati",
        tipologia_segnale_audio="modulato AM"
    )
    
    # Converte il segnale audio modulato in formato int16 e lo scrive nel file
    write(path_file_segnale_audio_modulato, frequenza_campionamento_originale, (segnale_audio_modulato*32767).astype(np.int16))
    
    # Messaggio di conferma del completamento della modulazione del segnale audio e del salvataggio
    print(f"{Fore.GREEN}Il segnale audio è stato modulato in AM con successo!{Style.RESET_ALL} Il file audio in formato WAV {tipologia_segnale_audio} della registrazione del segnale audio è stato salvato, come indicato in precedenza, nella seguente directory con successo: {Fore.RED}{path_file_segnale_audio_modulato}{Style.RESET_ALL}")    
    
    print(textwrap.dedent(f"""\
        {Fore.GREEN}Il segnale audio è stato modulato in AM con successo!{Style.RESET_ALL}
        Il file audio in formato WAV {tipologia_segnale_audio} della registrazione del segnale
        audio è stato salvato, come indicato in precedenza, nella seguente directory con successo:
        {Fore.RED}{path_file_segnale_audio_modulato}{Style.RESET_ALL}
        """).replace("\n", " ").strip())
    
    return path_file_segnale_audio_modulato

def massimizza_grandezza_finestra_grafici():
    try:
        manager_grafico=plt.get_current_fig_manager()
        backend_grafico=plt.get_backend()
        if backend_grafico=="TkAgg":
            manager_grafico.window.state("zoomed") # Casistica per Windows
        elif backend_grafico=="wxAgg":
            manager_grafico.frame.Maximize(True)
        elif backend_grafico=="Qt5Agg" or backend_grafico=="QtAgg":
            manager_grafico.window.showMaximized()
        elif backend_grafico=="GTK3Agg":
            manager_grafico.window.maximize()
        else:
            # Alternativa: imposta manualmente le dimensioni massime della finestra
            manager_grafico.resize(*manager_grafico.window.maxsize())
    except:
        # Se fallisce, non esegue nulla
        pass

def plot_waveform(dati_audio, freq_campionamento_audio, titolo_grafico="Rappresentazione del segnale audio registrato"):
    array_tempo=np.arange(len(dati_audio))/freq_campionamento_audio
    plt.figure(figsize=(12, 4))
    # Imposta il titolo della finestra del grafico (al posto del titolo di default ovvero "Figure 1")
    plt.gcf().canvas.manager.set_window_title(titolo_grafico)
    # Massimizza automaticamente la finestra del grafico a schermo intero (compatibile con tutti i backend)
    massimizza_grandezza_finestra_grafici()
    plt.plot(array_tempo, dati_audio, color="blue")
    plt.xlabel("Tempo [s]")
    plt.ylabel("Ampiezza [-]")
    plt.title(titolo_grafico)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_spectrogram(dati_audio, freq_campionamento_audio, titolo_grafico="Spettrogramma del segnale audio registrato"):
    # Se il segnale è stereo, estrae solo il primo canale per il calcolo dello spettrogramma
    if len(dati_audio.shape)>1:
        dati_audio=dati_audio[:, 0]

    # Normalizza i dati audio in formato float nell'intervallo [-1, 1] se necessario
    if dati_audio.dtype!=np.float32:
        dati_audio=dati_audio.astype(np.float32)
        # Normalizza i valori nell'intervallo [-1, 1] dividendo per il valore massimo assoluto
        dati_audio/=np.max(np.abs(dati_audio))
    
    # Visualizza lo spettrogramma del segnale audio con asse delle frequenze in scala lineare e ampiezza in dB
    plt.figure(figsize=(12, 4))
    # Imposta il titolo della finestra del grafico (al posto del titolo di default ovvero "Figure 1")
    plt.gcf().canvas.manager.set_window_title(titolo_grafico)
    # Massimizza automaticamente la finestra del grafico a schermo intero (compatibile con tutti i backend)
    massimizza_grandezza_finestra_grafici()
    # Sopprime il warning "divide by zero in log10" di matplotlib.specgram:
    # alcuni bin di frequenza hanno potenza nulla (log10(0) = -inf), causando
    # un RuntimeWarning innocuo che può essere ignorato senza problemi
    with warnings.catch_warnings():
        # Sopprime il warning "divide by zero encountered in log10" (divisione per zero rilevata in log10)
        warnings.filterwarnings("ignore", message="divide by zero encountered in log10")
        plt.specgram(dati_audio, Fs=freq_campionamento_audio, NFFT=1024, noverlap=512, cmap="inferno")
    plt.xlabel("Tempo [s]")
    plt.ylabel("Frequenza [Hz]")
    plt.title(titolo_grafico)
    plt.colorbar(label="Intensità [dB]")
    plt.tight_layout()
    plt.show()
    
def plot_spectrum(dati_audio, freq_campionamento, titolo_grafico="Spettro in frequenza con ampiezza in dB"):
    # Visualizza lo spettro in frequenza del segnale audio con ampiezza in dB
    # e asse delle frequenze in scala logaritmica; supporta segnali mono e stereo
    plt.figure(figsize=(12, 4))
    # Imposta il titolo della finestra del grafico (al posto del titolo di default ovvero "Figure 1")
    plt.gcf().canvas.manager.set_window_title(titolo_grafico)
    # Massimizza automaticamente la finestra del grafico a schermo intero (compatibile con tutti i backend)
    massimizza_grandezza_finestra_grafici()
    num_campioni=dati_audio.shape[0]

    # Se il segnale è stereo, estrae solo il primo canale per il calcolo dello spettro
    if len(dati_audio.shape)>1:
        dati_plot=dati_audio[:,0]
    else:
        dati_plot=dati_audio
    
    # Calcola la trasformata di Fourier (FFT) e conserva solo le frequenze positive
    # (ovvero la prima metà dello spettro)
    ampiezze_fft=np.abs(fft(dati_plot)[:num_campioni//2])
    frequenze_fft=fftfreq(num_campioni, 1/freq_campionamento)[:num_campioni//2]
    
    # Converte l'ampiezza in dB
    ampiezze_db=20*np.log10(ampiezze_fft/np.max(ampiezze_fft)+1e-12) # Aggiunge inoltre "1e-12" per evitare il logaritmo di zero
                                                # (log(0) = -inf)
                                                
    # Disegna lo spettro in frequenza con asse delle frequenze in scala logaritmica
    plt.plot(frequenze_fft, ampiezze_db)
    plt.title(titolo_grafico)
    plt.xlabel("Frequenza [Hz] (in scala logaritmica)")
    plt.ylabel("Ampiezza [dB]")
    plt.xscale("log")
    plt.grid(True, which="both", ls="--")
    plt.show()
    
def esci_o_ricomincia():
    pulsante_premuto=input("Premere Q o E per uscire, altrimenti premere qualsiasi altro pulsante per rieseguire il programma dall'inizio: ").upper()
    if pulsante_premuto=="E" or pulsante_premuto=="Q":
        print("Il programma verrà chiuso a momenti...")
        time.sleep(2)
        exit()
    else:
        print("Tra poco il programma verrà eseguito nuovamente!")
        time.sleep(2)
        print()
        main()

def main():
    introduzione_programma()
    path_file_audio_registrato=registra_segnale_audio()
    # Pipeline di elaborazione del segnale audio:
    # Acquisizione -> Filtraggio passa-banda -> Amplificazione -> Modulazione AM -> Trasmissione
    
    # Importa il file audio registrato e converte i campioni in formato float nell'intervallo [-1, 1]
    # per poter eseguire correttamente le operazioni di visualizzazione grafica
    freq_originale, dati_originali=importa_file_wav(path_file_audio_registrato)
    if dati_originali.dtype!=np.float32:
        dati_originali=dati_originali.astype(np.float32)/np.max(np.abs(dati_originali))
    
    # Permette di visualizzare i seguenti grafici del segnale audio originale NON processato:
    # forma d'onda temporale, spettrogramma e spettro in frequenza
    plot_waveform(dati_originali, freq_originale, titolo_grafico="Rappresentazione temporale del segnale audio registrato non processato")
    plot_spectrogram(dati_originali, freq_originale, titolo_grafico="Spettrogramma del segnale audio registrato non processato")
    plot_spectrum(dati_originali, freq_originale, titolo_grafico="Spettro in frequenza del segnale audio registrato non processato")
    
    # Applica il filtraggio passa-banda (1000–4000 Hz) e l'amplificazione di 10 dB al segnale audio originale
    processing_audio(path_file_audio_registrato)
    
    # Ricampiona il segnale audio a 8000 Hz: in questo modo vengono mantenute soltanto
    # le frequenze fino a 4000 Hz (teorema di Nyquist), coerentemente con il filtraggio applicato
    frequenza_camp_nuova=8000 # Il valore 8000 Hz è fisso e non viene richiesto alcun input all'utente
    path_file_ricampionato, freq_ricampionata, dati_ricampionati=ricampionamento_audio(path_file_audio_registrato, frequenza_camp_nuova)
    
    # Amplifica il segnale ricampionato di 5 dB senza distorsione
    dati_amplificati=amplificazione_audio(dati_ricampionati, fattore_db=5) # Amplifica di 5 dB
    
    # Salva il segnale audio amplificato in un nuovo file WAV
    path_file_amplificato, _=creazione_directory_salvataggio_file_wav(
        titolo_finestra_salvataggio="Salvataggio audio amplificato",
        nome_file="registrazione_segnale_audio_amplificato",
        directory_file="Registrazioni di segnali audio amplificati",
        tipologia_segnale_audio="amplificato"
    )
    write(path_file_amplificato, freq_ricampionata, (dati_amplificati*32767).astype(np.int16))
    
    # Applica la modulazione AM al segnale audio amplificato con portante a 20 kHz
    path_file_modulato=modulazione_am(path_file_amplificato, freq_ricampionata)
    
    # Permette di visualizzare i seguenti grafici del segnale audio dopo l'intera pipeline di elaborazione:
    # forma d'onda temporale, spettrogramma e spettro in frequenza
    plot_waveform(dati_amplificati, freq_ricampionata, titolo_grafico="Rappresentazione temporale del segnale audio elaborato")
    plot_spectrogram(dati_amplificati, freq_ricampionata, titolo_grafico="Spettrogramma del segnale audio elaborato")
    plot_spectrum(dati_amplificati, freq_ricampionata, titolo_grafico="Spettro in frequenza del segnale audio elaborato")
    
    # Messaggio finale di ringraziamento e invito a rieseguire il programma
    print()
    esci_o_ricomincia()

# Esegue la funzione main()
if __name__=="__main__":
    main()