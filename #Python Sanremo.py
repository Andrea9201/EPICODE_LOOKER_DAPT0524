#Importazioni librerie
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
#Lettura dei file da analizzare
DCS=pd.read_excel("dati-classifica-sanremo-1951-2023.xlsx")
DSS=pd.read_excel("dati-canzoni-spotify-sanremo-1951-2023.xlsx")
DSF=pd.read_excel("dati-festival-sanremo-1951-2023.xlsx")
#Rimozione colonna non significativa
DCS.drop(columns="Colonna1",inplace=True) 
#Sostituzione dei valori non convertibili in valori nulli (NaN)
DCS.replace({"NF": np.nan}, inplace=True)
#Rimozione dei valori nulli
DCS.dropna(inplace=True)
#Rimozione colonna non significativa
DSS.drop(columns="URL immagine album", inplace=True)
#Conversione colonna numerica in una colonna numerica con max 2 cifre mobili dopo la virgola
DSS["Durata (min)"]= DSS["Durata (min)"].round(2)
#Join tabelle (INNER) su colonna "Canzone"
Tabella1=pd.merge(DCS,DSS, on="Canzone",how='left')
Tabella_Finale=pd.merge(Tabella1,DSF, on="Anno",how='inner')
#Conversione colonna "Posizione" a tipo stringa
Tabella_Finale['Posizione'] = Tabella_Finale['Posizione'].astype(str)
#Creazione variabile contenente la media di ogni singola canzone presente
media_canzoni_nonvincitori=Tabella_Finale[Tabella_Finale['Posizione'] != "1"]['Durata (min)'].mean()
media_canzoni_nonvincitori = round(media_canzoni_nonvincitori, 2)
#Creazione variabile contenente la media di ogni singola canzone che ha vinto il festival
media_canzoni_vincitrici=Tabella_Finale[Tabella_Finale['Posizione'] == "1"]['Durata (min)'].mean()
media_canzoni_vincitrici=round(media_canzoni_vincitrici,2)
#Creazione variabile contente la canzone con la lunghezza più corta
min_canzone=Tabella_Finale["Durata (min)"].min()
#Creazione variabile contente la canzone con la lunghezza più lunga
max_canzone=Tabella_Finale["Durata (min)"].max()
#Creazione variabile contenente la differenza tra la media delle canzoni vincitrici e la media di tutte le canzoni che non hanno vinto
diff_media=(media_canzoni_nonvincitori-media_canzoni_vincitrici)
diff_media=round(diff_media,2)
#Print a schermo
print("La media delle canzoni non vincitrici è:", media_canzoni_nonvincitori)
print("La media delle canzoni vincitrici è:", media_canzoni_vincitrici)
print("La canzone più lunga dura:",max_canzone)
print("La canzone più breve dura:",min_canzone)
print("La differenza tra le medie delle canzoni vincitrici e quelle non vincitrici è:",diff_media)
print(Tabella_Finale)
Tabella_Finale.to_excel("Tabella_Finale_E.xlsx")
Tabella_Finale.to_csv("Tabella_Finale_CSV")
#Tabella con distribuzione a "bolle" dove si evince la correlazione tra durata media delle canzoni e podio
sns.scatterplot(
    data=Tabella_Finale,
    x="Cantante",
    y="Posizione",
    size="Durata (min)",  # Dimensione delle bolle
    hue="Durata (min)",   # Colore basato sulla durata
    palette="cool",       # Colore gradiente
    sizes=(50, 500),      # Dimensioni minime e massime delle bolle
    legend="brief"
)
plt.show()
#2 
popolarita_per_anno = Tabella_Finale.groupby("Anno")["Popolarità"].sum().reset_index()

# Grafico a barre
plt.figure(figsize=(12, 6))
sns.barplot(
    data=popolarita_per_anno,
    x="Anno",
    y="Popolarità",
    palette="viridis"
)
plt.title("Somma della Popolarità per Anno", fontsize=16)
plt.xlabel("Anno", fontsize=14)
plt.ylabel("Somma della Popolarità", fontsize=14)
plt.xticks(rotation=45)  # Ruota le etichette di 45 gradi poiché essendoci molte date non risultavano leggibili
plt.grid(axis='y')
plt.tight_layout()
plt.show()

#3
# Grafico a dispersione con linea di regressione
plt.figure(figsize=(10, 6))
sns.regplot(
    data=Tabella_Finale,
    x="Durata (min)",
    y="Popolarità",
    scatter_kws={'color': 'blue', 's': 50},  # Personalizza i punti
    line_kws={'color': 'red'},  # Linea di regressione
    ci=None  # Nasconde la banda di confidenza
)
plt.title("Correlazione tra Durata e Popolarità", fontsize=16)
plt.xlabel("Durata (min)", fontsize=14)
plt.ylabel("Popolarità", fontsize=14)
plt.grid(True)
plt.tight_layout()
plt.show()

#4 
partecipanti_per_presentatore = Tabella_Finale.groupby("Presentatore")["Partecipanti"].sum().reset_index()
# Grafico a barre
plt.figure(figsize=(10, 6))
sns.barplot(
    data=partecipanti_per_presentatore,
    x="Presentatore", 
    y="Partecipanti", 
    hue="Presentatore",  # Impostiamo "Presentatore" come hue
    palette="Blues",     # Colore specifico per la palette
    legend=False         # Disabilitiamo la legenda
)
plt.title("Somma dei Partecipanti per Presentatore", fontsize=16)
plt.xlabel("Presentatore", fontsize=14)
plt.ylabel("Somma dei Partecipanti", fontsize=14)
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()
plt.show()