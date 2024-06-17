import customtkinter as ctk
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import mysql.connector
import os

def login():
    username = userEntry.get()
    password = passEntry.get()
    if not username or not password:
        messagebox.showerror("Erreur", "Les deux champs sont obligatoires")
        return
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1972',
            database='library'
        )
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM admins WHERE username = %s AND pass = %s', (username, password))
        result = cursor.fetchone()

        if result:
            messagebox.showinfo("Success", "Login successful")
            bib.destroy() 
            from lib import win
        else:
            messagebox.showerror("Error", "Invalid username or password")

        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error connecting to database: {err}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('green')

bib = ctk.CTk()
bib.geometry('650x440')
bib.title("Login Page")

img1 = ImageTk.PhotoImage(Image.open("dark.jpg"))

loginLab = ctk.CTkLabel(bib, image=img1)
loginLab.pack(fill='both', expand=True)

frame = ctk.CTkFrame(loginLab, height=360, width=340, corner_radius=20)
frame.place(relx=0.5, rely=0.5, anchor=CENTER)

conlab = ctk.CTkLabel(frame, text='Connectez-vous à votre compte', font=('Century Gothic', 20, 'bold'))
conlab.place(x=30, y=45)

userEntry = ctk.CTkEntry(frame, width=230, height=35, placeholder_text='Nom de Utilisateur', corner_radius=8, border_color='green')
userEntry.place(x=50, y=120)
passEntry = ctk.CTkEntry(frame, width=230, height=35, placeholder_text='Mode de Passe', corner_radius=8, border_color='green', show='*')
passEntry.place(x=50, y=180)

forgot = ctk.CTkLabel(frame, text='Mot de passe oublié', font=('Century Gothic', 13, 'bold', UNDERLINE))
forgot.place(x=170, y=220)

loginbtn = ctk.CTkButton(frame, width=230, height=35, text='Login', corner_radius=8, command=login)
loginbtn.place(x=50, y=250)

bib.mainloop()
