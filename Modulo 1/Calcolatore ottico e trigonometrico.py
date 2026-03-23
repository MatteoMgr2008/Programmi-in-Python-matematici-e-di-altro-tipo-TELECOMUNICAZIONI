import math
 
def gradi(radianti):
    return radianti*180/math.pi
 
def radianti(gradi):
    return gradi*math.pi/180
 
def input_float(prompt, valore_min=None, valore_max=None):
    """Richiede un input numerico con controlli"""
    while True:
        try:
            valore_scelto=input(prompt)
            valore_scelto=float(valore_scelto)
            if valore_min is not None and valore_scelto < valore_min:
                print(f"Il valore immesso è troppo piccolo, questo perchè deve essere >= rispetto a {valore_min}")
                continue
            if valore_max is not None and valore_scelto > valore_max:
                print(f"Il valore immesso è troppo grande, questo perchè deve essere <= rispetto a {valore_max}")
                continue
            return valore_scelto
        except ValueError:
            print("Inserisci un numero intero o decimale valido, non è possibile inserire caratteri o altro. Sarà comunque possibile riselezionale il valore")
 
def funzioni_trigonometriche():
    while True:
        print("\n--- Menù delle funzioni trigonometriche ---")
        print("1) sin(x)")
        print("2) cos(x)")
        print("3) tan(x)")
        print("4) arcsin(x)")
        print("5) arccos(x)")
        print("6) arctan(x)")
        print("0) Torna indietro al menù principale")
        print()
        scelta_funzione_trigonometrica=input("Inserisci dal menù il numero correlato della funzione trigonometrica che si desidera calcolare: ")
 
        if scelta_funzione_trigonometrica=="0":
            print("È stata scelta la funzione 0 per tornare indietro al menù principale, tra non molto si verrà reindirizzati al precedente menù")
            print()
            break
 
        if scelta_funzione_trigonometrica in ["1", "2", "3"]:
            x_gradi=input_float("Inserisci il valore dell'angolo (in gradi): ")
            x_radianti=radianti(x_gradi)
            if scelta_funzione_trigonometrica=="1":
                print(f"sin({x_gradi}°) = {math.sin(x_radianti):.6f}")
            elif scelta_funzione_trigonometrica=="2":
                print(f"cos({x_gradi}°) = {math.cos(x_radianti):.6f}")
            elif scelta_funzione_trigonometrica=="3":
                cos_val=math.cos(x_radianti)
                if abs(cos_val)<1e-12:
                    print("La tangente non è definita per questo angolo. Riprovare con altri valori differenti")
                else:
                    print(f"tan({x_gradi}°) = {math.tan(x_radianti):.6f}")
 
        elif scelta_funzione_trigonometrica in ["4", "5", "6"]:
            if scelta_funzione_trigonometrica in ["4"]:
                valore_scelto=input_float("Inserisci il valore dell'arcsin (compreso -1 e 1): ", -1, 1)
            elif scelta_funzione_trigonometrica in ["5"]:
                valore_scelto=input_float("Inserisci il valore dell'arcos (compreso -1 e 1): ", -1, 1)
            else:
                valore_scelto=input_float("Inserisci il valore dell'arctan: ")
 
            if scelta_funzione_trigonometrica=="4":
                print(f"arcsin({valore_scelto}) = {gradi(math.asin(valore_scelto)):.6f}°")
            elif scelta_funzione_trigonometrica=="5":
                print(f"arccos({valore_scelto}) = {gradi(math.acos(valore_scelto)):.6f}°")
            elif scelta_funzione_trigonometrica=="6":
                print(f"arctan({valore_scelto}) = {gradi(math.atan(valore_scelto)):.6f}°")
        else:
            print("Il tool selezionato non è esistente poichè non è associato al numero immesso.")
 
def legge_snell():
    print("\n--- Calcolo della formula della legge di Snell ---")
    print()
    print("La formula della legge di Snell è la seguente: n1*sin(θ1) = n2*sin(θ2)")
    print()
    print("NB: è necessario NON scrivere il dato che è incognito")
 
    def input_optional_float(prompt):
        valore_scelto=input(prompt)
        if valore_scelto.strip()=="":
            return None
        try:
            return float(valore_scelto)
        except ValueError:
            print(" Inserisci un numero valido o lascia vuoto.")
            return input_optional_float(prompt)
 
    n1=input_optional_float("n1: ")
    n2=input_optional_float("n2: ")
    theta1=input_optional_float("θ1 (in gradi): ")
    theta2=input_optional_float("θ2 (in gradi): ")
 
    try:
        if n1 and n2 and theta1 and not theta2:
            valore_scelto=(n1/n2)*math.sin(radianti(theta1))
            if abs(valore_scelto) > 1:
                print("L'angolo di rifrazione non esiste (riflessione interna totale).")
            else:
                theta2=gradi(math.asin(valore_scelto))
                print(f"θ2 = {theta2:.4f}°")
 
        elif n1 and n2 and theta2 and not theta1:
            valore_scelto=(n2/n1)*math.sin(radianti(theta2))
            if abs(valore_scelto) > 1:
                print("L'angolo di incidenza non è possibile.")
            else:
                theta1=gradi(math.asin(valore_scelto))
                print(f"θ1 = {theta1:.4f}°")
 
        elif n2 and theta1 and theta2 and not n1:
            n1=n2*math.sin(radianti(theta2))/math.sin(radianti(theta1))
            print(f"n1 = {n1:.4f}")
 
        elif n1 and theta1 and theta2 and not n2:
            n2=n1*math.sin(radianti(theta1))/math.sin(radianti(theta2))
            print(f"n2 = {n2:.4f}")
        else:
            print("Dati immessi insufficienti o sono stati inseriti troppi valori noti.")
    except Exception as e:
        print(" Errore nel calcolo:", e)
 
def angolo_critico():
    print("\n--- Angolo critico ---")
    n1=input_float("n1 (mezzo incidente): ", 0)
    n2=input_float("n2 (mezzo rifratto): ", 0)
 
    if n1 <= n2:
        print("Non esiste angolo critico (n1 deve essere maggiore di n2).")
        return
 
    theta_c=gradi(math.asin(n2/n1))
    print(f"→ θc={theta_c:.4f}°")
 
def menu():
    while True:
        print("\n=== CALCOLATORE OTTICO E TRIGONOMETRICO ===")
        print("1. Funzioni trigonometriche")
        print("2. Legge di Snell")
        print("3. Angolo critico")
        print("0. Esci")
        scelta=input("Scegli un'opzione tra le seguenti per avviare un tool: ")
 
        if scelta=="1":
            funzioni_trigonometriche()
        elif scelta=="2":
            legge_snell()
        elif scelta=="3":
            angolo_critico()
        elif scelta=="0":
            print("Uscita dal programma in corso...")
            break
        else:
            print("Scelta immessa non valida.")
 
if __name__=="__main__":
    menu()