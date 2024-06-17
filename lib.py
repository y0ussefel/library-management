import customtkinter as ctk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import mysql.connector
import re
import datetime
import os

win = ctk.CTk()
win.geometry('1250x768')
win.title('Library Management')
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')
dark_mode = True


def switch():
    global dark_mode
    if dark_mode:
        ctk.set_appearance_mode('light')
    else:
        ctk.set_appearance_mode('dark')
    dark_mode = not dark_mode

s = ctk.CTkSwitch(win, fg_color='#bbbbbb', command=switch)
s.place(relx=0, rely=0.05)
header = ctk.CTkLabel(win, text='Library Management System', font=(
    'Century Gothic', 30, 'bold'), padx=20, pady=20, width=900)
header.place(relx=0.1, rely=0.02)
# Acuiell


def homePage():
    def validate_date(date):
        try:
            date_obj = datetime.datetime.strptime(date, '%d-%m-%Y')
            return date_obj
        except ValueError:
            messagebox.showerror(
                "Erreur", "Veuillez saisir une date au format JJ-MM-AAAA")

    def validate_two():
        de = validate_date(deDate.get())
        a = validate_date(ADate.get())
        if de and a:
            if de < a:
                return True
            else:
                messagebox.showerror(
                    "Erreur", "La date de l,emprunter doit être inferieur a la date de retour dùn livre.")
                return False
        return False

    def clear():
        affTitre.delete(0, 'end')
        affClient.delete(0, 'end')
        deDate.delete(0, 'end')
        ADate.delete(0, 'end')
        methodBox.set('')

    def emp():
        con = None
        cur = None
        try:
            con = mysql.connector.connect(
                host='localhost', user='root', password='1972', database='library')
            cur = con.cursor()
            if methodBox.get() == 'Emprunter' and validate_two():
                cur.execute("SELECT * FROM livres WHERE titre = %s",
                            (affTitre.get(),))
                livres_rows = cur.fetchall()
                if len(livres_rows) == 0:
                    messagebox.showerror(
                        "Erreur", "Livre non trouvé avec ce titre")
                    return
                cur.execute("SELECT * FROM clients WHERE cin = %s",
                            (affClient.get(),))
                clients_rows = cur.fetchall()
                if len(clients_rows) == 0:
                    messagebox.showerror(
                        "Erreur", "Client non trouvé avec ce CIN")
                    return
                cur.execute("INSERT INTO emprunter (titre_book, cin_client, date_emp, date_ret) VALUES (%s, %s, %s, %s)", (
                    affTitre.get(), affClient.get(), deDate.get(), ADate.get()))
                con.commit()
                messagebox.showinfo("Succès", "Emprunt réussi")

                cur.execute("SELECT * FROM livres WHERE titre = %s",
                            (affTitre.get(),))
                livres_rows = cur.fetchall()

                for row in livres_rows:
                    cmp = row[9] + 1
                    cur.execute(
                        "UPDATE livres SET nb_emp = %s WHERE titre = %s", (cmp, affTitre.get()))
                    con.commit()

                afficher_emp()
                clear()

            elif methodBox.get() == 'Retour':
                cur.execute("SELECT * FROM emprunter WHERE titre_book = %s AND cin_client = %s",
                            (affTitre.get(), affClient.get()))
                emprunter_rows = cur.fetchall()
                if len(emprunter_rows) == 0:
                    messagebox.showerror(
                        "Erreur", "Aucun livre trouvé avec ces informations")
                    return
                cur.execute("INSERT INTO retourner (titreBook, cinClient, date_emp, date_ret) VALUES (%s, %s, %s, %s)", (
                    affTitre.get(), affClient.get(), deDate.get(), ADate.get()))
                cur.execute("DELETE FROM emprunter WHERE titre_book = %s AND cin_client = %s", (
                    affTitre.get(), affClient.get()))
                con.commit()
                messagebox.showinfo("Succès", "Retour de livre réussi")
                afficher_emp()
                clear()

        except mysql.connector.Error as e:
            messagebox.showerror(
                "Erreur", f"Erreur de connexion à la base de données: {e}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur: {e}")
        finally:
            if cur:
                cur.close()
            if con and con.is_connected():
                con.close()

    # def affichage():

    def afficher_emp():
        con = mysql.connector.connect(
            host='localhost', user='root', password='1972', database='library')
        cur = con.cursor()
        cur.execute(
            "select titre_book, cin_client, date_emp, date_ret from emprunter ")
        rows = cur.fetchall()
        if (len(rows) != 0):
            tableAff.delete(*tableAff.get_children())
            for row in rows:
                tableAff.insert("", END, value=row)
            con.commit()
            con.close()
    frameHome = ctk.CTkFrame(win, width=1000, height=670)
    frameHome.grid(row=0, column=1)

    affTitre = ctk.CTkEntry(frameHome, width=175, height=38,
                            placeholder_text='Le Titre du Livre', font=('Arial', 18, 'bold'))
    affTitre.place(relx=0.02, rely=0.05)

    affClient = ctk.CTkEntry(frameHome, width=175, height=38,
                             placeholder_text='CIN Client', font=('Arial', 18, 'bold'))
    affClient.place(relx=0.2, rely=0.05)

    labelParBox = ctk.CTkLabel(
        frameHome, text='Par', font=('Arial', 20, 'bold'))
    labelParBox.place(relx=0.655, rely=0.06)
    methodBox = ctk.CTkComboBox(frameHome, width=145, height=38,
                                values=['Emprunter', 'Retour'], font=('Arial', 18, 'bold'), state='readonly')
    methodBox.place(relx=0.70, rely=0.05)
    deDate = ctk.CTkEntry(frameHome, width=130, height=38,
                          placeholder_text='De', font=('Arial', 16, 'bold'))
    deDate.place(relx=0.38, rely=0.05)
    ADate = ctk.CTkEntry(frameHome, width=130, height=38,
                         placeholder_text='A', font=('Arial', 16, 'bold'))
    ADate.place(relx=0.516, rely=0.05)

    addBtn = ctk.CTkButton(frameHome, text='Ajouter', width=140, height=38, font=(
        'Arial', 20, 'bold'), fg_color='#4a4a4a', hover_color='#696969', command=emp)
    addBtn.place(relx=0.85, rely=0.05)

    # table
    frameAff = ctk.CTkFrame(frameHome, width=1000, height=530)
    frameAff.place(relx=0, rely=0.15)

    style = ttk.Style()

    style.theme_use('default')

    style.configure("Treeview",
                    background="gray10",
                    foreground="white",
                    rowheight=40,
                    fieldbackground="gray10",
                    bordercolor="gray30",
                    borderwidth=1)
    style.map("Treeview",
              background=[('selected', '#dce4ee')],
              foreground=[('selected', 'gray10')])

    style.configure("Treeview.Heading",
                    background="gray20",
                    foreground="#dce4ee",
                    font=('Arial', 13, 'bold'),
                    bordercolor="gray30",
                    borderwidth=1)

    style.map("Treeview.Heading",
              background=[('active', '#9e9e9e')])
    # tableAff = ttk.Treeview(frameAff, columns=col, show='headings', height=552)

    style.configure("Treeview.Heading", padding=[5, 5, 5, 5])
    col = [
        'Livre Nom',
        'Cin Client ',
        'De',
        "à"
    ]

    tableAff = ttk.Treeview(frameAff, columns=col,
                            show='headings', height=552,)
    for column in col:
        tableAff.heading(column, text=column)
        tableAff.column(column, width=249, anchor='center')
    tableAff.place(rely=0)
    afficher_emp()

# LIVRE FUNCTION


def livreTabs():
    # homePage().destroy()
    frameBook = ctk.CTkFrame(win, width=1000, height=670)
    frameBook.grid(row=0, column=1)
    tabView = ctk.CTkTabview(frameBook, width=1000, height=680)
    tabView.place(relx=0, rely=0)
    tabView.add('Ajoute Livre')
    tabView.add('Tout Livres')
    tabView.add('Modifier/supprimer')


# AJOUTER LIVRE TAB

    def validate_date():
        try:
            user_input = PUBLICITE.get()
            date_obj = datetime.datetime.strptime(user_input, '%d-%m-%Y')
            return True
        except ValueError:
            messagebox.showerror(
                "Erreur", "Veuillez saisir une date au format JJ-MM-AAAA")

    def verify_prix():
        try:
            float_value = float(PRIX.get())
            return True
        except ValueError:
            messagebox.showerror(
                "Erreur", "Veuillez entrer le champ prix corectement.")

    def verify_stock():
        try:
            float_value = float(STOCK.get())
            return True
        except ValueError:
            messagebox.showerror(
                "Erreur", "Veuillez entrer le champ stock corectement.")

    def verify_code():
        try:
            float_value = float(CODE.get())
            return True
        except ValueError:
            messagebox.showerror(
                "Erreur", "Veuillez entrer le champ code corectement.")

    def code_repeter():
        code = CODE.get()  # Assuming CODE is a variable holding the code to check

        try:
            con = mysql.connector.connect(
                host='localhost', user='root', password='1972', database='library')
            cur = con.cursor()
            cur.execute("SELECT code FROM livres WHERE code = %s", (code,))
            row = cur.fetchone()
            if row:
                messagebox.showerror("Message d'erreur",
                                     "Ce code de livre existe déjà")
                return False  # Code already exists
            else:
                return True  # Code is unique
        except mysql.connector.Error as e:
            messagebox.showerror(
                "Erreur de connexion à la base de données", str(e))
            return False  # Database error
        except Exception as e:
            messagebox.showerror("Erreur", str(e))
            return False
        finally:
            if cur:
                cur.close()
            if con and con.is_connected():
                con.close()

    def add_book():
        con = mysql.connector.connect(
            host='localhost', user='root',  password='1972', database='library')
        cur = con.cursor()
        if (TITRE.get() and AUTEUR.get() and CATEGORIE.get() and PRIX.get != int() and STATUT.get() and PUBLICITE.get() and STOCK.get()):
            if (code_repeter() == True and verify_prix() == True and verify_stock() == True and verify_code() == True and validate_date() == True):
                cur.execute("INSERT INTO livres(code,titre,auteur,categorie,prix,statut,publicite,description,stock) VALUES (%s,%s, %s,%s,%s,%s,%s,%s,%s)", (
                    CODE.get(), TITRE.get(), AUTEUR.get(), CATEGORIE.get(), PRIX.get(
                    ), STATUT.get(), PUBLICITE.get(), description.get("0.0", END), STOCK.get()
                ))
                con.commit()

                con.close()

                messagebox.showinfo("Message info", "livre added")
                CATEGORIE.set('')
                PRIX.set('')
                AUTEUR.set('')
                STATUT.set('')
                PUBLICITE.set('')
                TITRE.set('')
                description.delete(0.0, "end")
                CODE.set('')
                STOCK.set('')
        else:
            messagebox.showerror("Message d'erreur",
                                 "Tous les champs sont obligatoires")
        afficher()

    def afficher():
        con = mysql.connector.connect(
            host='localhost', user='root',  password='1972', database='library')
        cur = con.cursor()
        cur.execute("select code, titre, categorie, auteur, prix  from livres")
        rows = cur.fetchall()
        if (len(rows) != 0):
            table.delete(*table.get_children())
            for row in rows:
                table.insert("", END, value=row)
            con.commit()
            con.close()

    def search():
        if (title2.get() and category2.get()):

            code = title2.get()
            category = category2.get()
            con = mysql.connector.connect(
                host='localhost', user='root',  password='1972', database='library')
            cur = con.cursor()
            cur.execute(
                "select code, titre, categorie, auteur, prix  from livres where titre=%s and categorie=%s ", (code, category,))
            rows = cur.fetchall()
            if (len(rows) != 0):
                table.delete(*table.get_children())
                for row in rows:
                    table.insert("", END, value=row)
                con.commit()
                con.close()

                TITRE.set('')
                CATEGORIE.set('')

            else:
                messagebox.showerror("Message d'erreur",
                                     "il n'ya pas ce livre")
                TITRE.set('')
                CATEGORIE.set('')
        else:
            messagebox.showerror("Message d'erreur",
                                 "les deux champs sont obligatoire")

    def search2_book():
        code = code2.get()
        con = mysql.connector.connect(
            host='localhost', user='root',  password='1972', database='library')
        cur = con.cursor()
        cur.execute(
            "select titre, auteur,categorie, prix,statut,publicite,description,stock  from livres where code=%s", (code,))
        rows = cur.fetchall()
        print(rows)
        if (len(rows) != 0):
            for row in rows:
                TITRE.set(row[0])
                AUTEUR.set(row[1])
                CATEGORIE.set(row[2])
                PRIX.set(row[3])
                STATUT.set(row[4])
                PUBLICITE.set(row[5])
                # description.delete(1.0, "end")
                description2.insert("end", row[6])
                STOCK.set(row[7])
            con.commit()
            con.close()
        else:
            messagebox.showerror("Message d'erreur", "il n'ya pas ce livre")

    def update_book():
        code = code2.get()
        if (verify_prix() == True and verify_stock() == True):
            con = mysql.connector.connect(
                host='localhost', user='root',  password='1972', database='library')
            cur = con.cursor()

            cur.execute(
                "UPDATE livres SET titre=%s, auteur=%s, categorie=%s, prix=%s, statut=%s, publicite=%s, description=%s, stock=%s WHERE code=%s",
                (
                    TITRE.get(), AUTEUR.get(), CATEGORIE.get(
                    ), PRIX.get(), STATUT.get(), PUBLICITE.get(),
                    description2.get("1.0", END).strip(), STOCK.get(), code,
                )
            )

        con.commit()
        con.close()

        CODE.set('')
        TITRE.set('')
        AUTEUR.set('')
        CATEGORIE.set('')
        PRIX.set('')
        STATUT.set('')
        STOCK.set('')
        PUBLICITE.set('')
        description2.delete(0.0, "end")
        messagebox.showinfo("Message info", "effectué avec succès ")
        afficher()

    def delete_book():
        con = mysql.connector.connect(
            host='localhost', user='root',  password='1972', database='library')
        cur = con.cursor()
        cur.execute("delete from  livres where  code= %s", (CODE.get(),))
        con.commit()
        CODE.set('')
        TITRE.set('')
        PUBLICITE.set('')
        STOCK.set('')
        AUTEUR.set('')
        CATEGORIE.set('')
        description2.delete(0.0, "end")
        STATUT.set('')
        PRIX.set('')
        messagebox.showinfo("Message info", "effectué avec succès ")
        afficher()
    # variable utilise dans les fontions
    TITRE = StringVar()
    AUTEUR = StringVar()
    CATEGORIE = StringVar()
    PRIX = StringVar()
    STATUT = StringVar()
    STOCK = StringVar()
    PUBLICITE = StringVar()
    CODE = StringVar()

    frameright = ctk.CTkFrame(tabView.tab(
        'Ajoute Livre'), width=480, height=470)
    frameright.place(relx=0.5, rely=0.1)

    labelCategory = ctk.CTkLabel(
        frameright, text='Category', font=('Arial', 20, 'bold'))
    labelCategory.place(relx=0.15, rely=0.05)
    category = ctk.CTkEntry(frameright, width=250,
                            height=35, textvariable=CATEGORIE)
    category.place(relx=0.45, rely=0.05)

    labelPrice = ctk.CTkLabel(frameright, text='Price',
                              font=('Arial', 20, 'bold'))
    labelPrice.place(relx=0.15, rely=0.15)
    price = ctk.CTkEntry(frameright, width=250, height=35, textvariable=PRIX)
    price.place(relx=0.45, rely=0.15)

    labelCode = ctk.CTkLabel(frameright, text='Code',
                             font=('Arial', 20, 'bold'))
    labelCode.place(relx=0.15, rely=0.25)
    code = ctk.CTkEntry(frameright, width=250, height=35, textvariable=CODE)
    code.place(relx=0.45, rely=0.25)

    labelAuthor = ctk.CTkLabel(
        frameright, text='Author', font=('Arial', 20, 'bold'))
    labelAuthor.place(relx=0.15, rely=0.45)
    author = ctk.CTkEntry(frameright, width=250,
                          height=35, textvariable=AUTEUR)
    author.place(relx=0.45, rely=0.45)

    labelStatus = ctk.CTkLabel(
        frameright, text='Status', font=('Arial', 20, 'bold'))
    labelStatus.place(relx=0.15, rely=0.55)
    status = ctk.CTkComboBox(frameright, width=250, height=35, values=[
        'Neuf ', ' Utilisé'], justify='center', font=('Arial', 15, 'bold'), state='readonly', variable=STATUT)
    status.place(relx=0.45, rely=0.55)

    labelStock = ctk.CTkLabel(frameright, text='Stock',
                              font=('Arial', 20, 'bold'))
    labelStock.place(relx=0.15, rely=0.75)
    stock = ctk.CTkEntry(frameright, width=250, height=35, textvariable=STOCK)
    stock.place(relx=0.45, rely=0.75)

    labelPubl = ctk.CTkLabel(
        frameright, text='Publisher', font=('Arial', 20, 'bold'))
    labelPubl.place(relx=0.15, rely=0.85)
    publisher = ctk.CTkEntry(frameright, width=250,
                             height=35, textvariable=PUBLICITE)
    publisher.place(relx=0.45, rely=0.85)

    frameleft2 = ctk.CTkFrame(tabView.tab(
        'Ajoute Livre'), width=480, height=470)
    frameleft2.place(relx=0, rely=0.1)

    labeltitle = ctk.CTkLabel(
        frameleft2, text='Livre Titre', font=('Arial', 20, 'bold'))
    labeltitle.place(relx=0.02, rely=0.06)
    title = ctk.CTkEntry(frameleft2, width=350, height=38, textvariable=TITRE)
    title.place(relx=0.26, rely=0.05)

    labelDescr = ctk.CTkLabel(
        frameleft2, text='Description', font=('Arial', 20, 'bold'))
    labelDescr.place(relx=0.02, rely=0.33)
    description = ctk.CTkTextbox(frameleft2, width=350, height=200,)
    description.place(relx=0.26, rely=0.19)

    addLivreBtn = ctk.CTkButton(tabView.tab(
        'Ajoute Livre'), text='Ajouter', width=200, height=45, font=('Arial', 20, 'bold'), fg_color='#696969', hover_color='#4a4a4a', command=add_book)
    addLivreBtn.place(relx=0.5, rely=0.93, anchor=ctk.CENTER)

# AFFICHIER ET RECHERCHER LIVRE TAB

    frameUp = ctk.CTkFrame(tabView.tab('Tout Livres'), width=980, height=85)
    frameUp.pack(fill='both')

    title2 = ctk.CTkEntry(frameUp, width=350, height=38,
                          placeholder_text='Titre livre', font=('Arial', 18, 'bold'), textvariable=TITRE)
    title2.place(relx=0.02, rely=0.27)

    labelCategory2 = ctk.CTkLabel(
        frameUp, text='Category', font=('Arial', 20, 'bold'))
    labelCategory2.place(relx=0.42, rely=0.32)
    category2 = ctk.CTkEntry(frameUp, width=225, height=38,
                             placeholder_text='Category', font=('Arial', 18, 'bold'), textvariable=CATEGORIE)
    category2.place(relx=0.52, rely=0.27)

    searchLivreBtn = ctk.CTkButton(frameUp, text='Rechercher', width=180, height=38, font=(
        'Arial', 20, 'bold'), fg_color='#4a4a4a', hover_color='#696969', command=search)
    searchLivreBtn.place(relx=0.8, rely=0.27)

    frameTable = ctk.CTkFrame(tabView.tab(
        'Tout Livres'), width=980, height=530)
    frameTable.pack(fill='both', expand=True)
    style = ttk.Style()

    style.theme_use('default')

    style.configure("Treeview",
                    background="gray10",
                    foreground="white",
                    rowheight=40,
                    fieldbackground="gray10",
                    bordercolor="gray30",
                    borderwidth=1)
    style.map("Treeview",
              background=[('selected', '#dce4ee')],
              foreground=[('selected', 'gray10')])

    style.configure("Treeview.Heading",
                    background="gray20",
                    foreground="#dce4ee",
                    font=('Arial', 15, 'bold'),
                    bordercolor="gray30",
                    borderwidth=1)

    style.map("Treeview.Heading",
              background=[('active', '#9e9e9e')])

    style.configure("Treeview.Heading", padding=[10, 10, 10, 10])
    col = ['code livre', 'titre livre',
           'category livre', 'autheur livre', 'prix livre',]

    table = ttk.Treeview(frameTable, columns=col, show='headings', height=552,)
    table.heading('code livre', text='Code Livre')
    table.heading('titre livre', text='Titre Livre')
    table.heading('category livre', text='Category Livre')
    table.heading('autheur livre', text='Autheur Livre')
    table.heading('prix livre', text='Prix Liver')
    table.place(rely=0)
    afficher()
# Update AND Delete Livre
    frameright2 = ctk.CTkFrame(tabView.tab(
        'Modifier/supprimer'), width=480, height=470)
    frameright2.place(relx=0.5, rely=0.15)

    frameUp2 = ctk.CTkFrame(tabView.tab(
        'Modifier/supprimer'), width=970, height=90)
    frameUp2.place(relx=0, rely=0.0)

    labelCategory3 = ctk.CTkLabel(
        frameright2, text='Category', font=('Arial', 20, 'bold'))
    labelCategory3.place(relx=0.15, rely=0.05)
    category3 = ctk.CTkEntry(frameright2, width=250,
                             height=35, textvariable=CATEGORIE)
    category3.place(relx=0.45, rely=0.05)

    labelPrice2 = ctk.CTkLabel(frameright2, text='Price',
                               font=('Arial', 20, 'bold'))
    labelPrice2.place(relx=0.15, rely=0.15)
    price2 = ctk.CTkEntry(frameright2, width=250, height=35, textvariable=PRIX)
    price2.place(relx=0.45, rely=0.15)

    labelCode2 = ctk.CTkLabel(frameUp2, text='Code',
                              font=('Arial', 20, 'bold'))
    labelCode2.place(relx=0.02, rely=0.35)
    code2 = ctk.CTkEntry(frameUp2, width=250, height=35, textvariable=CODE)
    code2.place(relx=0.1, rely=0.3)

    cherLivreBtn = ctk.CTkButton(frameUp2, text='Rechercher', width=200,
                                 height=35, font=('Arial', 18, 'bold'), fg_color='#696969', hover_color='#4a4a4a', command=search2_book)
    cherLivreBtn.place(relx=0.8, rely=0.5, anchor="center")

    labelAuthor2 = ctk.CTkLabel(
        frameright2, text='Auteur', font=('Arial', 20, 'bold'))
    labelAuthor2.place(relx=0.15, rely=0.45)
    author2 = ctk.CTkEntry(frameright2, width=250,
                           height=35, textvariable=AUTEUR)
    author2.place(relx=0.45, rely=0.45)

    labelStatus2 = ctk.CTkLabel(
        frameright2, text='Status', font=('Arial', 20, 'bold'))
    labelStatus2.place(relx=0.15, rely=0.55)
    status2 = ctk.CTkComboBox(frameright2, width=250, height=35, values=[
        'Neuf ', ' Utilisé'], justify='center', font=('Arial', 15, 'bold'), state='readonly', variable=STATUT)
    status2.place(relx=0.45, rely=0.55)

    labelStock2 = ctk.CTkLabel(frameright2, text='Stock',
                               font=('Arial', 20, 'bold'))
    labelStock2.place(relx=0.15, rely=0.75)
    stock2 = ctk.CTkEntry(frameright2, width=250,
                          height=35, textvariable=STOCK)
    stock2.place(relx=0.45, rely=0.75)

    labelPubl2 = ctk.CTkLabel(
        frameright2, text='Publisher', font=('Arial', 20, 'bold'))
    labelPubl2.place(relx=0.15, rely=0.85)
    publisher2 = ctk.CTkEntry(frameright2, width=250,
                              height=35, textvariable=PUBLICITE)
    publisher2.place(relx=0.45, rely=0.85)

    frameleft3 = ctk.CTkFrame(tabView.tab(
        'Modifier/supprimer'), width=480, height=470)
    frameleft3.place(relx=0, rely=0.15)

    labeltitle3 = ctk.CTkLabel(
        frameleft3, text='Livre Titre', font=('Arial', 20, 'bold'))
    labeltitle3.place(relx=0.02, rely=0.06)
    title3 = ctk.CTkEntry(frameleft3, width=350, height=38, textvariable=TITRE)
    title3.place(relx=0.26, rely=0.05)

    labelDescr2 = ctk.CTkLabel(
        frameleft3, text='Description', font=('Arial', 20, 'bold'))
    labelDescr2.place(relx=0.02, rely=0.33)
    description2 = ctk.CTkTextbox(frameleft3, width=350, height=200)
    description2.place(relx=0.26, rely=0.19)

    updLivreBtn = ctk.CTkButton(tabView.tab('Modifier/supprimer'), text='Modifier', width=200,
                                height=45, font=('Arial', 20, 'bold'), fg_color='#696969', hover_color='#4a4a4a', command=update_book)
    updLivreBtn.place(relx=0.935, rely=0.93, anchor="ne")

    delLivreBtn = ctk.CTkButton(tabView.tab('Modifier/supprimer'), text='Supprimer', width=200,
                                height=45, font=('Arial', 20, 'bold'), fg_color='#696969', hover_color='#4a4a4a', command=delete_book)
    delLivreBtn.place(relx=0.08, rely=0.93, anchor="nw")

# CLIENT FUNCTION


def clientTbs():

    frameClient = ctk.CTkFrame(win, width=1000, height=680)
    frameClient.grid(row=0, column=1, pady=87, padx=20)

    tabView = ctk.CTkTabview(frameClient, width=1000, height=679)
    tabView.place(relx=0, rely=0)
    tabView.add('Ajoute Client')
    tabView.add('Tout Clients')
    tabView.add('Modifier/Supprimer')

# Ajouter client tab
    def verification():
        cin_regex = re.compile(r'^\d{5}$')  # Two letters followed by digits
        email_regex = re.compile(
            # Email format
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        phone_regex = re.compile(r'^\d{10}$')  # 10 digits for phone number

        if cin.get() and name.get() and prenom.get() and mail.get() and phone.get():
            if not cin_regex.match(cin.get()):
                messagebox.showerror(
                    "Message d'erreur", "il faut que la valeur de CIN cmpose de 5 nombres")
                return False
            if not email_regex.match(mail.get()):
                messagebox.showerror("Message d'erreur",
                                     "Le format de l'email est invalide")
                return False
            if not phone_regex.match(phone.get()):
                messagebox.showerror(
                    "Message d'erreur", "il faut que la valeur de tele compose de 10 nombres")
                return False
            return True
        else:
            messagebox.showerror("Message d'erreur",
                                 "Tous les champs sont obligatoires")
            return False

    def add_client():
        if verification():
            try:
                con = mysql.connector.connect(
                    host='localhost', user='root', password='1972', database='library')
                cur = con.cursor()
                now = datetime.datetime.today()
                cur.execute("INSERT INTO clients(cin, nom, prenom, email, phone,date) VALUES (%s, %s, %s, %s, %s,%s)", (
                    cin.get(), name.get(), prenom.get(), mail.get(), phone.get(), now
                ))
                con.commit()
                con.close()
                messagebox.showinfo(
                    "Message info", "Client ajouté avec succès")

                # Clearing the Entry widgets
                cin.delete(0, 'end')
                name.delete(0, 'end')
                prenom.delete(0, 'end')
                mail.delete(0, 'end')
                phone.delete(0, 'end')
                afficher_client()
            except Exception as e:
                messagebox.showerror("Message d'erreur",
                                     f"Erreur lors de l'ajout du client: {e}")
    labelcin = ctk.CTkLabel(tabView.tab('Ajoute Client'),
                            text='Client CIN ', font=('Arial', 20, 'bold'))
    labelcin.place(relx=0.35, rely=0.2, anchor="center")
    cin = ctk.CTkEntry(tabView.tab('Ajoute Client'), width=250, height=40)
    cin.place(relx=0.65, rely=0.2, anchor="center")

    labelName = ctk.CTkLabel(tabView.tab(
        'Ajoute Client'), text='Client Nom ', font=('Arial', 20, 'bold'))
    labelName.place(relx=0.35, rely=0.32, anchor="center")
    name = ctk.CTkEntry(tabView.tab('Ajoute Client'), width=250, height=40)
    name.place(relx=0.65, rely=0.32, anchor="center")

    labelPrenom = ctk.CTkLabel(tabView.tab(
        'Ajoute Client'), text='Client Prenom ', font=('Arial', 20, 'bold'))
    labelPrenom.place(relx=0.35, rely=0.44, anchor="center")
    prenom = ctk.CTkEntry(tabView.tab('Ajoute Client'), width=250, height=40)
    prenom.place(relx=0.65, rely=0.44, anchor="center")

    labelMail = ctk.CTkLabel(tabView.tab(
        'Ajoute Client'), text='Client Email ', font=('Arial', 20, 'bold'))
    labelMail.place(relx=0.35, rely=0.56, anchor="center")
    mail = ctk.CTkEntry(tabView.tab('Ajoute Client'), width=250, height=40)
    mail.place(relx=0.65, rely=0.56, anchor="center")

    labelPhone = ctk.CTkLabel(tabView.tab(
        'Ajoute Client'), text='Client Phone ', font=('Arial', 20, 'bold'))
    labelPhone.place(relx=0.35, rely=0.68, anchor="center")
    phone = ctk.CTkEntry(tabView.tab('Ajoute Client'), width=250, height=40)
    phone.place(relx=0.65, rely=0.68, anchor="center")

    addClientBtn = ctk.CTkButton(tabView.tab('Ajoute Client'), text='Ajouter Client', width=250,
                                 height=50, font=('Arial', 18, 'bold'), fg_color='#696969', hover_color='#4a4a4a', command=add_client)
    addClientBtn.place(relx=0.5, rely=0.9, anchor="center")

# Affichire Tout Clients
    def afficher_client():
        con = mysql.connector.connect(
            host='localhost', user='root', password='1972', database='library')
        cur = con.cursor()
        cur.execute("select *  from clients")
        rows = cur.fetchall()
        if (len(rows) != 0):
            table.delete(*table.get_children())
            for row in rows:
                table.insert("", END, value=row)
            con.commit()
            con.close()

    def search1_client():
        if (clientBox.get() == "Prenom"):
            con = mysql.connector.connect(
                host='localhost', user='root', password='1972', database='library')
            cur = con.cursor()
            cur.execute("SELECT * FROM clients WHERE prenom=%s",
                        (clientData.get(),))
            rows = cur.fetchall()
            if (len(rows) != 0):
                table.delete(*table.get_children())
                for row in rows:
                    table.insert("", END, value=row)
                    con.commit()
                    con.close()

            else:
                messagebox.showerror("Message d'erreur",
                                     "ce client n a pas existe")

        elif (clientBox.get() == "CIN"):
            con = mysql.connector.connect(
                host='localhost', user='root', password='1972', database='library')
            cur = con.cursor()
            cur.execute("SELECT * FROM clients WHERE cin=%s",
                        (clientData.get(),))
            rows = cur.fetchall()
            if (len(rows) != 0):
                table.delete(*table.get_children())
                for row in rows:
                    table.insert("", END, value=row)
                    con.commit()
                    con.close()

            else:
                messagebox.showerror("Message d'erreur",
                                     "ce client n a pas existe")

        elif (clientBox.get() == "Phone"):
            con = mysql.connector.connect(
                host='localhost', user='root', password='1972', database='library')
            cur = con.cursor()
            cur.execute("SELECT * FROM clients WHERE phone=%s",
                        (clientData.get(),))
            rows = cur.fetchall()
            if (len(rows) != 0):
                table.delete(*table.get_children())
                for row in rows:
                    table.insert("", END, value=row)
                    con.commit()
                    con.close()

            else:
                messagebox.showerror("Message d'erreur",
                                     "ce client n a pas existe")
    clientData = ctk.CTkEntry(tabView.tab('Tout Clients'), width=350, height=38,
                              placeholder_text='Client Data', font=('Arial', 18, 'bold'))
    clientData.place(relx=0.02, rely=0.05)

    labelClientBox = ctk.CTkLabel(tabView.tab(
        'Tout Clients'), text='Par', font=('Arial', 20, 'bold'))
    labelClientBox.place(relx=0.42,  rely=0.06)
    clientBox = ctk.CTkComboBox(tabView.tab('Tout Clients'), width=225, height=38,
                                values=['Prenom', 'CIN', 'Phone',], font=('Arial', 18, 'bold'), state='readonly')
    clientBox.place(relx=0.52,  rely=0.05)

    searchLivreBtn = ctk.CTkButton(tabView.tab('Tout Clients'), text='Rechercher', width=180, height=38, font=(
        'Arial', 20, 'bold'), fg_color='#4a4a4a', hover_color='#696969', command=search1_client)
    searchLivreBtn.place(relx=0.8,  rely=0.05)

    # table
    frameTable = ctk.CTkFrame(tabView.tab(
        'Tout Clients'), width=980, height=530)
    frameTable.place(relx=0,  rely=0.15)
    style = ttk.Style()

    style.theme_use('default')

    style.configure("Treeview",
                    background="gray10",
                    foreground="white",
                    rowheight=40,
                    fieldbackground="gray10",
                    bordercolor="gray30",
                    borderwidth=1)
    style.map("Treeview",
              background=[('selected', '#dce4ee')],
              foreground=[('selected', 'gray10')])

    style.configure("Treeview.Heading",
                    background="gray20",
                    foreground="#dce4ee",
                    font=('Arial', 13, 'bold'),
                    bordercolor="gray30",
                    borderwidth=1)

    style.map("Treeview.Heading",
              background=[('active', '#9e9e9e')])

    style.configure("Treeview.Heading", padding=[5, 5, 5, 5])
    col = [
        'Client CIN',
        'Client Nom',
        'Client Prenom',
        'Client Email',
        'Client Phone',
        "Date d'adhésion"

    ]

    table = ttk.Treeview(frameTable, columns=col, show='headings', height=552,)
    for column in col:
        table.heading(column, text=column)
        table.column(column, width=162, anchor='center')
    table.place(rely=0)
    afficher_client()


# Update and Delete Client

    def searchForclient():
        criteria = {
            "Prenom": "prenom",
            "CIN": "cin",
            "Phone": "phone"
        }
        selected_criteria = clientBox2.get()

        if selected_criteria not in criteria:
            messagebox.showerror("Message d'erreur",
                                 "Critère de recherche invalide")
            return
        field = criteria[selected_criteria]
        search_value = clientData2.get()

        if not search_value:
            messagebox.showerror("Message d'erreur",
                                 "Veuillez entrer une valeur de recherche")
            return
        try:
            con = mysql.connector.connect(
                host='localhost', user='root', password='1972', database='library')
            cur = con.cursor()
            query = f"SELECT * FROM clients WHERE {field}=%s"
            cur.execute(query, (search_value,))
            rows = cur.fetchall()

            if rows:
                row = rows[0]
                cin2.delete(0, 'end')
                cin2.insert(0, row[0])
                name2.delete(0, 'end')
                name2.insert(0, row[1])
                prenom2.delete(0, 'end')
                prenom2.insert(0, row[2])
                mail2.delete(0, 'end')
                mail2.insert(0, row[3])
                phone2.delete(0, 'end')
                phone2.insert(0, row[4])
            else:
                messagebox.showerror("Message d'erreur",
                                     "Ce client n'existe pas")

        except Exception as e:
            messagebox.showerror("Message d'erreur",
                                 f"Erreur lors de la recherche: {e}")

        finally:
            con.close()

    def update_verification(cin, name, prenom, email, phone):
        cin_regex = re.compile(r'^\d{5}$')  # CIN format: 5 digits
        email_regex = re.compile(
            # Email format
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        phone_regex = re.compile(r'^\d{10}$')  # Phone format: 10 digits

        if not cin_regex.match(cin):
            return False, "Le CIN doit être composé de 5 chiffres."
        if not email_regex.match(email):
            return False, "Le format de l'email est invalide."
        if not phone_regex.match(phone):
            return False, "Le numéro de téléphone doit être composé de 10 chiffres."

        return True, None

    def update_client():
        cin_regex = re.compile(r'^\d{5}$')  # CIN format: 5 digits
        email_regex = re.compile(
            # Email format
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        phone_regex = re.compile(r'^\d{10}$')  # Phone format: 10 digits

        if not cin_regex.match(cin2.get()):
            messagebox.showerror("Message d'erreur",
                                 "Le CIN doit être composé de 5 chiffres.")
            return
        if not email_regex.match(mail2.get()):
            messagebox.showerror("Message d'erreur",
                                 "Le format de l'email est invalide.")
            return
        if not phone_regex.match(phone2.get()):
            messagebox.showerror(
                "Message d'erreur", "Le numéro de téléphone doit être composé de 10 chiffres.")
            return

        try:
            con = mysql.connector.connect(
                host='localhost', user='root', password='1972', database='library')
            cur = con.cursor()
            if clientBox2.get() == "Prenom":
                cur.execute("update clients set cin=%s, nom=%s, prenom=%s, email=%s, phone=%s where prenom=%s", (
                    cin2.get(), name2.get(), prenom2.get(), mail2.get(), phone2.get(), clientData2.get(),))
            elif clientBox2.get() == "CIN":
                cur.execute("update clients set cin=%s, nom=%s, prenom=%s, email=%s, phone=%s where cin=%s", (
                    cin2.get(), name2.get(), prenom2.get(), mail2.get(), phone2.get(), clientData2.get(),))
            elif clientBox2.get() == "Phone":
                cur.execute("update clients set cin=%s, nom=%s, prenom=%s, email=%s, phone=%s where phone=%s", (
                    cin2.get(), name2.get(), prenom2.get(), mail2.get(), phone2.get(), clientData2.get(),))

            con.commit()
            con.close()
            afficher_client()
            messagebox.showinfo("Message info", "Effectué avec succès ")

            # Clearing entry fields and variables after successful update
            cin2.delete(0, 'end')
            name2.delete(0, 'end')
            prenom2.delete(0, 'end')
            mail2.delete(0, 'end')
            phone2.delete(0, 'end')
            clientData2.delete(0, 'end')
            clientBox2.set('')
        except Exception as e:
            messagebox.showerror(
                "Message d'erreur", f"Erreur lors de la mise à jour du client: {e}")

    def delete_client():
        client_type = clientBox2.get()
        client_data = clientData2.get()
        try:
            con = mysql.connector.connect(
                host='localhost', user='root', password='1972', database='library')
            cur = con.cursor()

            if client_type == "Prenom":
                cur.execute(
                    "DELETE FROM clients WHERE prenom = %s", (client_data,))
            elif client_type == "CIN":
                cur.execute("DELETE FROM clients WHERE cin = %s",
                            (client_data,))
            elif client_type == "Phone":
                cur.execute("DELETE FROM clients WHERE phone = %s",
                            (client_data,))

            con.commit()
            con.close()
            afficher_client()
            messagebox.showinfo("Message info", "Effectué avec succès ")

            cin2.delete(0, 'end')
            name2.delete(0, 'end')
            prenom2.delete(0, 'end')
            mail2.delete(0, 'end')
            phone2.delete(0, 'end')
            clientData2.delete(0, 'end')
            clientBox2.set('')
        except Exception as e:
            messagebox.showerror(
                "Message d'erreur", f"Erreur lors de la suppression du client : {e}")

    clientData2 = ctk.CTkEntry(tabView.tab('Modifier/Supprimer'), width=350, height=38,
                               placeholder_text='Client Data', font=('Arial', 18, 'bold'))
    clientData2.place(relx=0.02, rely=0.05)

    labelClientBox2 = ctk.CTkLabel(tabView.tab(
        'Modifier/Supprimer'), text='Par', font=('Arial', 20, 'bold'))
    labelClientBox2.place(relx=0.42,  rely=0.06)
    clientBox2 = ctk.CTkComboBox(tabView.tab('Modifier/Supprimer'), width=225, height=38,
                                 values=['Prenom', 'CIN', 'Phone'], font=('Arial', 18, 'bold'), state='readonly')
    clientBox2.place(relx=0.52,  rely=0.05)

    searchLivreBtn2 = ctk.CTkButton(tabView.tab('Modifier/Supprimer'), text='Rechercher', width=180, height=38, font=(
        'Arial', 20, 'bold'), fg_color='#4a4a4a', hover_color='#696969', command=searchForclient)
    searchLivreBtn2.place(relx=0.8,  rely=0.05)

    labelcin2 = ctk.CTkLabel(tabView.tab(
        'Modifier/Supprimer'), text='Client CIN ', font=('Arial', 20, 'bold'))
    labelcin2.place(relx=0.35, rely=0.28, anchor="center")
    cin2 = ctk.CTkEntry(tabView.tab('Modifier/Supprimer'),
                        width=250, height=40)
    cin2.place(relx=0.65, rely=0.28, anchor="center")

    labelName2 = ctk.CTkLabel(tabView.tab(
        'Modifier/Supprimer'), text='Client Nom ', font=('Arial', 20, 'bold'))
    labelName2.place(relx=0.35, rely=0.38, anchor="center")
    name2 = ctk.CTkEntry(tabView.tab(
        'Modifier/Supprimer'), width=250, height=40)
    name2.place(relx=0.65, rely=0.38, anchor="center")

    labelPrenom2 = ctk.CTkLabel(tabView.tab(
        'Modifier/Supprimer'), text='Client Prenom ', font=('Arial', 20, 'bold'))
    labelPrenom2.place(relx=0.35, rely=0.48, anchor="center")
    prenom2 = ctk.CTkEntry(tabView.tab(
        'Modifier/Supprimer'), width=250, height=40)
    prenom2.place(relx=0.65, rely=0.48, anchor="center")

    labelMail2 = ctk.CTkLabel(tabView.tab(
        'Modifier/Supprimer'), text='Client Email ', font=('Arial', 20, 'bold'))
    labelMail2.place(relx=0.35, rely=0.58, anchor="center")
    mail2 = ctk.CTkEntry(tabView.tab(
        'Modifier/Supprimer'), width=250, height=40)
    mail2.place(relx=0.65, rely=0.58, anchor="center")

    labelPhone2 = ctk.CTkLabel(tabView.tab(
        'Modifier/Supprimer'), text='Client Phone ', font=('Arial', 20, 'bold'))
    labelPhone2.place(relx=0.35, rely=0.68, anchor="center")
    phone2 = ctk.CTkEntry(tabView.tab(
        'Modifier/Supprimer'), width=250, height=40)
    phone2.place(relx=0.65, rely=0.68, anchor="center")

    updClientBtn = ctk.CTkButton(tabView.tab('Modifier/Supprimer'), text='Enregistre', width=250,
                                 height=50, font=('Arial', 18, 'bold'), fg_color='#696969', hover_color='#4a4a4a', command=update_client)
    updClientBtn.place(relx=0.75, rely=0.9, anchor="center")

    delClientBtn = ctk.CTkButton(tabView.tab('Modifier/Supprimer'), text='Supprimer', width=250,
                                 height=50, font=('Arial', 18, 'bold'), fg_color='#696969', hover_color='#4a4a4a', command=delete_client)
    delClientBtn.place(relx=0.25, rely=0.9, anchor="center")

# EMPLOYER FUNCTION


def employer():

    frameEmployer = ctk.CTkFrame(win, width=1000, height=680)
    frameEmployer.place(relx=0.18, rely=0.11)
    tabView = ctk.CTkTabview(frameEmployer, width=1000, height=680)
    tabView.place(relx=0, rely=0)
    tabView.add('Ajoute Employe')
    tabView.add('Modifier Employe')
    tabView.add('Permission')
# AJOUTER EMPLOYER

    def verifie_cin():
        cin_pattern = re.compile(r'^\d{5}$')  # CIN format: 5 chiffres
        if cin_pattern.match(cinE.get()):
            return True
        else:
            messagebox.showerror(
                "Message d'erreur", "Le format du CIN est invalide. Il doit être composé de 5 chiffres.")
            return False

    def verifie_password():
        # 10 caractères, lettres et chiffres
        password_pattern = re.compile(r'^[a-zA-Z0-9]{10}$')
        if password_pattern.match(passeE.get()):
            return True
        else:
            messagebox.showerror(
                "Message d'erreur", "Le format du mot de passe est invalide. Il doit être composé de 10 caractères, lettres et chiffres.")
            return False

    def add_employe():
        con = mysql.connector.connect(
            host='localhost', user='root', password='1972', database='library')
        cur = con.cursor()

        if cinE.get() and nameE.get() and prenomE.get() and loginE.get() and passeE.get():
            if verifie_cin() and verifie_password():
                cur.execute("INSERT INTO employers(cin, nom, prenom, login, password) VALUES (%s, %s, %s, %s, %s)",
                            (cinE.get(), nameE.get(), prenomE.get(), loginE.get(), passeE.get()))
                con.commit()
                con.close()
                messagebox.showinfo("Message info", "Admin ajouté")
                cinE.delete(0, 'end')
                nameE.delete(0, 'end')
                prenomE.delete(0, 'end')
                passeE.delete(0, 'end')
                loginE.delete(0, 'end')
        else:
            messagebox.showerror("Message d'erreur",
                                 "Tous les champs sont obligatoires")

    labelcinE = ctk.CTkLabel(tabView.tab(
        'Ajoute Employe'), text='Employe CIN ', font=('Arial', 20, 'bold'))
    labelcinE.place(relx=0.35, rely=0.2, anchor="center")
    cinE = ctk.CTkEntry(tabView.tab('Ajoute Employe'), width=250, height=40)
    cinE.place(relx=0.65, rely=0.2, anchor="center")

    labelNameE = ctk.CTkLabel(tabView.tab(
        'Ajoute Employe'), text='Employe Nom ', font=('Arial', 20, 'bold'))
    labelNameE.place(relx=0.35, rely=0.32, anchor="center")
    nameE = ctk.CTkEntry(tabView.tab('Ajoute Employe'), width=250, height=40)
    nameE.place(relx=0.65, rely=0.32, anchor="center")

    labelPrenomE = ctk.CTkLabel(tabView.tab(
        'Ajoute Employe'), text='Employe Prenom ', font=('Arial', 20, 'bold'))
    labelPrenomE.place(relx=0.35, rely=0.44, anchor="center")
    prenomE = ctk.CTkEntry(tabView.tab('Ajoute Employe'), width=250, height=40)
    prenomE.place(relx=0.65, rely=0.44, anchor="center")

    labelLoginE = ctk.CTkLabel(tabView.tab(
        'Ajoute Employe'), text='Employe Login ', font=('Arial', 20, 'bold'))
    labelLoginE.place(relx=0.35, rely=0.56, anchor="center")
    loginE = ctk.CTkEntry(tabView.tab('Ajoute Employe'), width=250, height=40)
    loginE.place(relx=0.65, rely=0.56, anchor="center")

    labelPasseE = ctk.CTkLabel(tabView.tab(
        'Ajoute Employe'), text='Employe M.passe ', font=('Arial', 20, 'bold'))
    labelPasseE.place(relx=0.35, rely=0.68, anchor="center")
    passeE = ctk.CTkEntry(tabView.tab('Ajoute Employe'), width=250, height=40)
    passeE.place(relx=0.65, rely=0.68, anchor="center")

    addClientBtnE = ctk.CTkButton(tabView.tab('Ajoute Employe'), text='Ajoute Employe', width=250,
                                  height=50, font=('Arial', 18, 'bold'), fg_color='#696969', hover_color='#4a4a4a', command=add_employe)
    addClientBtnE.place(relx=0.5, rely=0.9, anchor="center")

# MODIJIER EMPLOYER
    def search_employe():
        con = mysql.connector.connect(
            host='localhost', user='root', password='1972', database='library')
        cur = con.cursor()
        cur.execute("select cin, prenom,login,password  from employers where nom=%s and password=%s ",
                    (checkNameE.get(), checkPassE.get(),))
        rows = cur.fetchall()
        if (len(rows) != 0):
            for row in rows:
                cinE2.delete(0, 'end')
                cinE2.insert(0, row[0])
                prenomE2.delete(0, 'end')
                prenomE2.insert(0, row[1])
                loginE2.delete(0, 'end')
                loginE2.insert(0, row[2])
                passeE2.delete(0, 'end')
                passeE2.insert(0, row[3])
                con.commit()
                con.close()
        else:
            messagebox.showerror("Message d'erreur", "il n'ya pas ce employer")

    def update_employe():
        try:
            con = mysql.connector.connect(
                host='localhost', user='root', password='1972', database='library')
            cur = con.cursor()

            cur.execute("UPDATE employers SET cin=%s, prenom=%s, login=%s, password=%s WHERE nom=%s AND password=%s",
                        (cinE2.get(), prenomE2.get(), loginE2.get(), passeE2.get(), checkNameE.get(), checkPassE.get()))

            con.commit()
            cinE2.delete(0, 'end')
            checkNameE.delete(0, 'end')
            loginE2.delete(0, 'end')
            passeE2.delete(0, 'end')
            prenomE2.delete(0, 'end')
            checkPassE.delete(0, 'end')
            messagebox.showinfo("Success", "Update successful")

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database error: {err}")

    nameCheckE = ctk.CTkLabel(tabView.tab(
        'Modifier Employe'), text='Employe Nom ', font=('Arial', 20, 'bold'))
    nameCheckE.place(relx=0.35, rely=0.04, anchor="center")
    checkNameE = ctk.CTkEntry(tabView.tab(
        'Modifier Employe'), width=250, height=40)
    checkNameE.place(relx=0.65, rely=0.04, anchor="center")

    passCheckE = ctk.CTkLabel(tabView.tab(
        'Modifier Employe'), text='Mode de Passe ', font=('Arial', 20, 'bold'))
    passCheckE.place(relx=0.35, rely=0.14, anchor="center")
    checkPassE = ctk.CTkEntry(tabView.tab(
        'Modifier Employe'), width=250, height=40)
    checkPassE.place(relx=0.65, rely=0.14, anchor="center")

    checkBtnE = ctk.CTkButton(tabView.tab('Modifier Employe'), text='Check', width=150,
                              height=35, font=('Arial', 18, 'bold'), fg_color='#696969', hover_color='#4a4a4a', command=search_employe)
    checkBtnE.place(relx=0.5, rely=0.26, anchor="center")

    labelcinE2 = ctk.CTkLabel(tabView.tab(
        'Modifier Employe'), text='Employe CIN ', font=('Arial', 20, 'bold'))
    labelcinE2.place(relx=0.35, rely=0.38, anchor="center")
    cinE2 = ctk.CTkEntry(tabView.tab('Modifier Employe'), width=250, height=40)
    cinE2.place(relx=0.65, rely=0.38, anchor="center")

    labelPrenomE2 = ctk.CTkLabel(tabView.tab(
        'Modifier Employe'), text='Employe Prenom ', font=('Arial', 20, 'bold'))
    labelPrenomE2.place(relx=0.35, rely=0.5, anchor="center")
    prenomE2 = ctk.CTkEntry(tabView.tab(
        'Modifier Employe'), width=250, height=40)
    prenomE2.place(relx=0.65, rely=0.5, anchor="center")

    labelLoginE2 = ctk.CTkLabel(tabView.tab(
        'Modifier Employe'), text='Employe Login ', font=('Arial', 20, 'bold'))
    labelLoginE2.place(relx=0.35, rely=0.62, anchor="center")
    loginE2 = ctk.CTkEntry(tabView.tab(
        'Modifier Employe'), width=250, height=40)
    loginE2.place(relx=0.65, rely=0.62, anchor="center")

    labelPasseE2 = ctk.CTkLabel(tabView.tab(
        'Modifier Employe'), text='Employe M.passe ', font=('Arial', 20, 'bold'))
    labelPasseE2.place(relx=0.35, rely=0.74, anchor="center")
    passeE2 = ctk.CTkEntry(tabView.tab(
        'Modifier Employe'), width=250, height=40)
    passeE2.place(relx=0.65, rely=0.74, anchor="center")

    addClientBtnE2 = ctk.CTkButton(tabView.tab('Modifier Employe'), text='Modifier Employe', width=250,
                                   height=50, font=('Arial', 18, 'bold'), fg_color='#696969', hover_color='#4a4a4a', command=update_employe)
    addClientBtnE2.place(relx=0.5, rely=0.9, anchor="center")


def gestionLivres():
    def top_livres():
        con = mysql.connector.connect(
            host='localhost', user='root', password='1972', database='library')
        cur = con.cursor()
        seuil = 3
        cur.execute(
            "select code, titre, categorie, prix  from livres where nb_emp > %s", (seuil,))
        rows = cur.fetchall()
        if (len(rows) != 0):
            tableAff.delete(*tableAff.get_children())
            for row in rows:
                tableAff.insert("", END, value=row)
            con.commit()
            con.close()

    def less_livre():
        con = mysql.connector.connect(
            host='localhost', user='root', password='1972', database='library')
        cur = con.cursor()
        seuil = 2
        cur.execute(
            "select code, titre, categorie, prix  from livres where nb_emp < %s", (seuil,))
        rows = cur.fetchall()
        if (len(rows) != 0):
            tableButt.delete(* tableButt.get_children())
            for row in rows:
                tableButt.insert("", END, value=row)
            con.commit()
            con.close()

    def select_livre(ev):
        cursor_row = tableButt.focus()
        col = tableButt.item(cursor_row)
        row = col['values']
        titreBuut.delete(0, 'end')
        titreBuut.insert(0, row[1])
        prixBuut.delete(0, 'end')
        prixBuut.insert(0, row[3])

    def promotion(taux):
        try:
            prix = float(prixBuut.get())
            dis_prix = (prix * taux) / 100
            messagebox.showinfo("promption", f"noveau prix apres {
                                taux}% promtion: {dis_prix}")
            return dis_prix
        except ValueError:
            messagebox.showerror("Invalid La valeur de prix")

    def update_prix():
        con = mysql.connector.connect(
            host='localhost', user='root', password='1972', database='library')
        cur = con.cursor()
        if titreBuut.get() and prixBuut.get():
            promo = promotion(20)
            cur.execute("UPDATE livres SET prix = %s WHERE titre = %s",
                        (promo, titreBuut.get()))
            con.commit()
            titreBuut.delete(0, 'end')
            prixBuut.delete(0, 'end')
        less_livre()

    frameGestion = ctk.CTkFrame(win, width=1000, height=670)
    frameGestion.grid(row=0, column=1)
    frameTop = ctk.CTkFrame(frameGestion, width=1000, height=335)
    frameTop.place(relx=0.01, rely=0)
    labTop = ctk.CTkLabel(frameTop, text='TOP LIVRES ', font=(
        'Arial', 22, 'bold'), text_color='gray')
    labTop.place(relx=0.4, rely=0.01)
    # table
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",
                    background="gray10",
                    foreground="white",
                    rowheight=40,
                    fieldbackground="gray10",
                    bordercolor="gray30",
                    borderwidth=1)
    style.map("Treeview",
              background=[('selected', '#dce4ee')],
              foreground=[('selected', 'gray10')])

    style.configure("Treeview.Heading",
                    background="gray20",
                    foreground="#dce4ee",
                    font=('Arial', 13, 'bold'),
                    bordercolor="gray30",
                    borderwidth=1)

    style.map("Treeview.Heading",
              background=[('active', '#9e9e9e')])

    style.configure("Treeview.Heading", padding=[5, 5, 5, 5])
    col = [
        'Livre Code',
        'Livre Titre ',
        'category',
        "Prix"
    ]

    tableAff = ttk.Treeview(frameTop, columns=col, show='headings', height=552)
    for column in col:
        tableAff.heading(column, text=column)
        tableAff.column(column, anchor='center', width=247)
    tableAff.place(relx=0, rely=0.1)
    top_livres()

    # buttom table
    frameButt = ctk.CTkFrame(frameGestion, width=1000, height=335)
    frameButt.place(relx=0, rely=0.505)
    labButt = ctk.CTkLabel(frameButt, text='LESS LIVRES ', font=(
        'Arial', 22, 'bold'), text_color='gray')
    labButt.place(relx=0.4, rely=0.0)

    titreBuut = ctk.CTkEntry(frameButt, width=350, height=40, placeholder_text='Titre Livre', font=(
        'Arial', 18, 'bold'))
    titreBuut.place(relx=0.8, rely=0.2, anchor="center")

    prixBuut = ctk.CTkEntry(frameButt, width=350, height=40, placeholder_text='Prix Livre', font=(
        'Arial', 18, 'bold'))
    prixBuut.place(relx=0.8, rely=0.45, anchor="center")

    buttonBuut = ctk.CTkButton(frameButt, width=350, height=40, text="Promotion", font=(
        'Arial', 18, 'bold'), command=update_prix, fg_color='#bbbbbb', text_color="black", hover_color="gray")
    buttonBuut.place(relx=0.8, rely=0.7, anchor="center")

    # table
    style = ttk.Style()
    style.theme_use('default')
    style.configure("Treeview",
                    background="gray10",
                    foreground="white",
                    rowheight=40,
                    fieldbackground="gray10",
                    bordercolor="gray30",
                    borderwidth=1)
    style.map("Treeview",
              background=[('selected', '#dce4ee')],
              foreground=[('selected', 'gray10')])

    style.configure("Treeview.Heading",
                    background="gray20",
                    foreground="#dce4ee",
                    font=('Arial', 13, 'bold'),
                    bordercolor="gray30",
                    borderwidth=1)

    style.map("Treeview.Heading",
              background=[('active', '#9e9e9e')])

    style.configure("Treeview.Heading", padding=[5, 5, 5, 5])
    col = [
        'Livre Code',
        'Livre Titre ',
        'category',
        "Prix"
    ]

    tableButt = ttk.Treeview(frameButt, columns=col,
                             show='headings', height=552)
    for column in col:
        tableButt.heading(column, text=column)
        tableButt.column(column, anchor='center', width=150)
    tableButt.place(relx=0, rely=0.1)
    less_livre()
    tableButt.bind("<ButtonRelease-1>", select_livre)


homePage()
file_path = os.path.dirname(os.path.realpath(__file__))
img1 = ctk.CTkImage(Image.open(file_path + "/home.png"), size=(35, 35))
img2 = ctk.CTkImage(Image.open(file_path + "/book.png"), size=(35, 35))
img3 = ctk.CTkImage(Image.open(file_path + "/client.png"), size=(35, 35))
img4 = ctk.CTkImage(Image.open(file_path + "/emp.png"), size=(35, 35))
img5 = ctk.CTkImage(Image.open(file_path + "/setting.png"), size=(35, 35))

# Buttons frame
leftFrame = ctk.CTkFrame(win, width=170, height=670)
leftFrame.grid(row=0, column=0, pady=87, padx=20)

homeBtn = ctk.CTkButton(leftFrame, text="Page D'accueil",
                        height=50, command=homePage, image=img1, compound="left", fg_color='#bbbbbb', hover_color='#dfd7d4', text_color='black')
homeBtn.place(relx=0.1, rely=0.15)

livreBtn = ctk.CTkButton(leftFrame, text='LIVRE', height=50,
                         command=livreTabs, image=img2, compound="left", anchor="ew", fg_color='#bbbbbb', hover_color='#dfd7d4', text_color='black')
livreBtn.place(relx=0.1, rely=0.3)

clientBtn = ctk.CTkButton(leftFrame, text='Client',
                          height=50, command=clientTbs, image=img3, compound="left", anchor="ew", fg_color='#bbbbbb', hover_color='#dfd7d4', text_color='black')
clientBtn.place(relx=0.1, rely=0.45)

anotherBtn = ctk.CTkButton(
    leftFrame, text='les Employes', height=50, command=employer, image=img4, fg_color='#bbbbbb', hover_color='#dfd7d4', text_color='black')
anotherBtn.place(relx=0.1, rely=0.6)

ooBtn = ctk.CTkButton(leftFrame, text='Gestion Livres',
                      height=50, command=gestionLivres, image=img5, fg_color='#bbbbbb', hover_color='#dfd7d4', text_color='black')
ooBtn.place(relx=0.1, rely=0.75)

win.mainloop()
