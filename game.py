import tkinter as tk
from pathlib import Path
import random

path=Path(__file__).parent #el path al directorio con los subdirectorios palabras_todas, hardest, easiest, favorites, etc.
mode="hardest"; #selecciona un subdirectorio.

files=[f.stem for f in (path/mode).iterdir() if f.is_file()] #agrega las palabras leídas dentro de una carpeta con accesos directos a una lista.
random.shuffle(files); #revuelve las palabras para que salgan al azar.

words_data=[]; #precarga todas las palabras y definiciones para evitar leer archivos durante la partida.

for word in files:
    word_path=path/"palabras_todas"/word;
    with word_path.open("r",encoding="utf-8") as w_file:
        content=w_file.read().replace(" \x08",""); #fix formatting error in rae files.
    words_data.append({
        "word":word,
        "content":content
    });

word_number=0;
palabra=[];
label_word=[];

def load_word(index):
    global palabra,label_word;

    content=words_data[index]["content"];

    print(repr(content)); #muestra todo el archivo en la terminal.

    definitions=[];
    found_first_1=False; #usado como llave para evitar definiciones compuestas.

    for line in content.splitlines(): #divide el archivo en líneas.
        if(not line or not line.split(".",1)[0].isdigit()): #ignora las líneas que no contienen una definición válida.
            continue;

        number=int(line.split(".",1)[0]); #toma el número de la definición.

        if(number==1): #evita que el programa lea definiciones compuestas después de las principales (1,2,...,9).
            if(found_first_1):
                break;
            found_first_1=True;

        definitions.append(line); #añade las líneas al listado de definiciones.

    def_label.config(text="\n".join(definitions)); #el label une todas las definiciones en un solo texto.

    palabra=list(words_data[index]["word"]); #se convierte a lista para poder comparar y revelar letras individualmente.
    label_word=["_"]*len(palabra); #placeholder.

    word_label.config(text=" ".join(label_word)); #label_word es la palabra interna, word_label es la que se ve en el GUI.

    print("Actual word:",words_data[index]["word"]);


def handle_enter(event):
    global word_number;

    user_text=entry.get().strip().lower(); #conserva la entrada ingresada por el ususario.
    entry.delete(0,tk.END); #borra la entrada ingresada por el usuario.

    for i in range(min(len(palabra),len(user_text))): #compara ambas palabras; si son diferentes, compara la menor sin salirse del rango.
        if(palabra[i].lower()==user_text[i]):
            label_word[i]=palabra[i];

    word_label.config(text=" ".join(label_word)); #actualiza el label de la palabra.

    if(palabra==label_word): #si la palabra ingresada coincide con la esperada.
        print("Bien!");

        word_number+=1;

        if(word_number<len(files)): #pasa a la siguiente palabra.
            load_word(word_number);
        else:
            def_label.config(text="¡Muy bien!");
            word_label.config(text=";)");
            entry.config(state="disabled");


# ---------------- GUI ----------------

root=tk.Tk();
root.geometry("400x600");
root.title("Adivina la palabra");

canvas=tk.Canvas(root,bg="#F218CE");
canvas.pack(fill="both",expand=True);

#Bomb
canvas.create_oval(
    150,100,
    250,200,
    fill="black",
    outline="blue",
    width=2
);

#Definition box
def_frame=tk.Frame(canvas,bg="white",bd=2,relief="solid");
canvas.create_window((200,260),window=def_frame);

def_label=tk.Label(
    def_frame,
    wraplength=350,
    justify="left",
    font=("Tahoma",10)
);
def_label.pack(padx=10,pady=10);

#Score label
player_frame=tk.Frame(canvas,bg="white",bd=2,relief="solid");
canvas.create_window((370,30),window=player_frame);

player_label=tk.Label(
    player_frame,
    wraplength=350,
    justify="left",
    font=("Tahoma",10)
);
player_label.pack(padx=10,pady=10);

#Word display
word_label=tk.Label(
    root,
    text="",
    font=("Arial Unicode MS",20,"bold")
);

canvas.create_window((200,470),window=word_label);

#Entry
entry=tk.Entry(
    root,
    width=30,
    font=("Segoe UI",12)
);

canvas.create_window((200,540),window=entry);

entry.bind("<Return>",handle_enter);
entry.focus_set(); #hace que el foco esté en el input del programa.

#Load first word
load_word(word_number);

root.mainloop();