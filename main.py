from tkinter import *
from tkinter import messagebox
import string
import random
import pyperclip
import json

FONT_NAME="Arial"
FONT_SIZE=10

# ---------------------------- SLAPTAŽODŽIO GENERATORIUS ------------------------------- #
#funkcija, kurios pagalba iš lotyniškų raidžių, skaičių ir sibmolių parenkamas atsitiktine tvarka bei atsitiktinis
# skaičius elementų, kurie sudedami į atskirus sąrašus (list), jie sudedami į vieną sąrašą, sąraše sumaišomi bei
# sujungiami į tekstą.

def password_generator():

    raides = list(string.ascii_letters)
    skaiciai = list(string.digits)
    simboliai = list(string.punctuation)

    password_raides = [random.choice(raides) for n in range(random.randint(8, 10))]
    password_simboliai = [random.choice(simboliai) for n in range(random.randint(2, 6))]
    password_skaiciai = [random.choice(skaiciai) for n in range(random.randint(2, 6))]

    password_list = password_raides + password_simboliai + password_skaiciai
    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, string=password)

# ---------------------------- SLAPTAŽODŽIO IŠSAUGOJIMAS ------------------------------- #

def save():
    website=website_entry.get()
    email=email_entry.get()
    password=password_entry.get()
    new_data={website:{'email':email,
                       'password':password}}

    # tikrinama ar įvesti į laukus duomenys
    if len(website)==0 or len(email)==0 or len(password)==0:
        messagebox.showinfo(message='Nepakanka informacijos.\nPrašome užpildyti tuščius laukus.')
    else:

    # pateikiami įvedamui duomenys peržiūrai, patvirtinimui įrašyti arba įrašymo nutraukimui
        is_ok=messagebox.askokcancel(title=website,message=f'Sekanti informacija bus išsaugota: '
                                                     f'\nTinklapis: {website} '
                                                     f'\nE-paštas: {email} '
                                                     f'\nSlaptažodis: {password} '
                                                     f'\nPaspauskite OK ir patvirtinkite arba '
                                                           f'Cancel ir sustabdykite įvedimą.')

        if is_ok:
            try:
                with open('data.json', 'r') as data_file:
                # perskaitomi seni duomenys
                    data=json.load(data_file)

            except FileNotFoundError:
                # jei json failo nėra, jis sukuriamas
                with open('data.json', 'w') as data_file:
                    json.dump(new_data,data_file,indent=4)

            else:
                # papildomi seni duomenys naujais
                data.update(new_data)

                with open('data.json', 'w') as data_file:
                    # atnaujinti duomenys išsaugomi
                    json.dump(data,data_file,indent=4)

            finally:
                # iš tinklalapio ir slaptažodzio langų išvalomi duomenys
                website_entry.delete(0,END)
                password_entry.delete(0, END)

# ---------------------------- SLAPTAŽODŽIO PAIEŠKA ------------------------------- #
def find_password():
    website=website_entry.get()
    try:
        with open('data.json') as data_file:
            data=json.load(data_file)

        #jei data.json failo nėra, pateikiama informacija
    except FileNotFoundError:
        messagebox.showinfo(title='Klaida',message='Duomenų failas nerastas.')

        #jei slaptažodis yra data.json, pateikiama informacija apie įraše prie esamo tinklapio esančius el.pašto adresą
        # bei slaptažodį. Paspaudus Ctrl+V galima įvesti esamą slaptažodį.
    else:
        if website in data:
            email=data[website]['email']
            password=data[website]['password']
            messagebox.showinfo(title=website,
                                message=f'E-pašto {email}\nSlaptažodis {password}. Paspauskite Ctr+V įvesti slaptažodį.')
            pyperclip.copy(password)

        #jei nerandami įrašai susiję su įrašytu tinklapiu faile data.json, pateikiamas įspėjimas
        else:
            messagebox.showinfo(title='Klaida',message=f'Nėra informacijos apie {website} tinklapį')


# ---------------------------- UI NUSTATYMAS ------------------------------- #


window=Tk()
window.title("Slaptažodžių tvarkyklė")
window.config(padx=20,pady=20,bg='white')

#pakeičiama viršutinės juostos ikona
window.iconbitmap(r'spyna.ico')

#suformuojamas laukas (Canvas) į kurį įdedamas spynos paveiksliukas
canvas=Canvas(width=200,height=200,highlightthickness=0)
spyna_img=PhotoImage(file='logo_1.png')
canvas.create_image(100,100,image=spyna_img)    #x ir y centro pozicija canvas
canvas.grid(column=1,row=0)

#tinklapio, el. pašto, slaptažodžio užrašai (Label)
website_label = Label(text="Tinklapis:",font=(FONT_NAME,FONT_SIZE),bg='white')
website_label.grid(column=0,row=1,sticky=W)

email_label = Label(text="E-paštas/ vart. vardas:",font=(FONT_NAME,FONT_SIZE),bg='white')
email_label.grid(column=0,row=2,sticky=W)

password_label = Label(text="Slaptažodis:",font=(FONT_NAME,FONT_SIZE),bg='white')
password_label.grid(column=0,row=3,sticky=W)

#tinklapio, el. pašto, slaptažodžio įvedimo laukai (Entry)
website_entry = Entry(width=26,bd=2)
website_entry.focus()
website_entry.grid(column=1,row=1,sticky=E)

email_entry = Entry(width=45,bd=2)
email_entry.insert(0, string="gintilas.rimantas@gmail.com")
email_entry.grid(column=1,row=2,columnspan=2,sticky=E)

password_entry = Entry(width=22,text="",font=(FONT_NAME,FONT_SIZE),bd=2)
password_entry.grid(column=1,row=3,sticky=E)

#slapražodžio paieškos, slaptažodžio sukūrimo, duomenų įvedimo mygtukai (Button)
search_button = Button(width=15,text="Slaptažodžio paieška", command=find_password)
search_button.grid(column=2,row=1,sticky=W)

password_button = Button(width=15,text="Sukurkite slaptažodį", command=password_generator)
password_button.grid(column=2,row=3,sticky=W)

add_button = Button(width=38,text="Išsaugokite duomenis", command=save)
add_button.grid(column=1,row=4, columnspan=2,sticky=E)

window.mainloop()