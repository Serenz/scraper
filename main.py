import requests
import json
import threading
import time
import re
import os
import copy
import tkinter as tk
import customtkinter as ctk
from pathlib import Path
from bs4 import BeautifulSoup as bs
from utils.headers import *
from utils.my_token import TOKEN, DEV_ID
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

def load_mappings():
    global M_BRANDS, M_CATEGORIE, M_ORDINE, M_REPARTO, M_TIPO, M_ZONA, S_CATEGORIE, S_REGIONI, S_TYPE
    current = Path(os.getcwd())
    mercatino = current / "mercatino_mapping"
    subito = current / "subito_mapping"
    with open(mercatino / "brands_mapping_mc.json", 'r') as f:
        M_BRANDS = json.load(f)
    with open(mercatino  / "categorie_mapping_ct.json", "r") as f:
        M_CATEGORIE = json.load(f)
    with open(mercatino  / "ordine_mapping_ob.json", "r") as f:
        M_ORDINE = json.load(f)
    with open(mercatino  / "reparto_mapping_rp.json", "r") as f:
        M_REPARTO = json.load(f)
    with open(mercatino  / "tipo_mapping_gp.json", "r") as f:
        M_TIPO = json.load(f)
    with open(mercatino  / "zona_mapping__rgpv.json", "r") as f:
        M_ZONA = json.load(f)
    with open(subito / "categories_mapping.json", "r") as f:
        S_CATEGORIE = json.load(f)
    with open(subito / "regions_mapping.json", "r") as f:
        S_REGIONI = json.load(f)
    with open(subito / "type_mapping.json", "r") as f:
        S_TYPE = json.load(f)

def load_mercatino_requests():
    global richieste_mercatino
    req_path = Path(os.getcwd()) / "utils" / "richieste_mercatino.json"
    with open(req_path, "r") as f:
        richieste_mercatino = json.load(f)

def load_subito_requests():
    global richieste_subito
    req_path = Path(os.getcwd()) / "utils" / "richieste_subito.json"
    with open(req_path, "r") as f:
        richieste_subito = json.load(f)

def load_ebay_requests():
    global richieste_ebay
    req_path = Path(os.getcwd()) / "utils" / "richieste_ebay.json"
    with open(req_path, "r") as f:
        richieste_ebay = json.load(f)

def load_reverb_requests():
    global richieste_reverb
    req_path = Path(os.getcwd()) / "utils" / "richieste_reverb.json"
    with open(req_path, "r") as f:
        richieste_reverb = json.load(f)

def load_requests():
    load_subito_requests()
    load_mercatino_requests()
    load_ebay_requests()
    load_reverb_requests()

def save_subito_requests():
    req_path = Path(os.getcwd()) / "utils" / "richieste_subito.json"
    with open(req_path, "w") as f:
        json.dump(richieste_subito, f, indent=4)

def save_mercatino_requests():
    req_path = Path(os.getcwd()) / "utils" / "richieste_mercatino.json"
    with open(req_path, "w") as f:
        json.dump(richieste_mercatino, f, indent=4)

def save_ebay_requests():
    req_path = Path(os.getcwd()) / "utils" / "richieste_ebay.json"
    with open(req_path, "w") as f:
        json.dump(richieste_ebay, f, indent=4)

def save_reverb_requests():
    req_path = Path(os.getcwd()) / "utils" / "richieste_reverb.json"
    with open(req_path, "w") as f:
        json.dump(richieste_reverb, f, indent=4)

def save_all():
    save_subito_requests()
    save_mercatino_requests()
    save_ebay_requests()
    save_reverb_requests()


ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Products Notifier")
        self.geometry(f"{1400}x{900}")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0), weight=0)
        self.grid_rowconfigure((1), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Products Notifier",
                                       font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                             command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = ctk.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                     command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create tabview for searching products
        self.searchview = ctk.CTkTabview(self)
        self.searchview.grid(row=0, column=1, columnspan=3, padx=(20, 20), pady=(20, 0), sticky="new")
        self.searchview.add("Subito")
        self.searchview.add("Mercatino")
        self.searchview.tab("Subito").grid_columnconfigure((0, 1, 2), weight=1)
        self.searchview.tab("Mercatino").grid_columnconfigure((0, 1, 2), weight=1)

        self.listview = ctk.CTkTabview(self)
        self.listview.grid(row=1, column=1, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.listview.add("Subito")
        self.listview.add("Mercatino")
        self.listview.add("Ebay")
        self.listview.add("Reverb")
        self.listview.tab("Subito").grid_columnconfigure(0, weight=1)
        self.listview.tab("Subito").grid_rowconfigure(0, weight=1)
        self.listview.tab("Mercatino").grid_columnconfigure(0, weight=1)
        self.listview.tab("Mercatino").grid_rowconfigure(0, weight=1)
        self.listview.tab("Ebay").grid_columnconfigure(0, weight=1)
        self.listview.tab("Ebay").grid_rowconfigure(0, weight=1)
        self.listview.tab("Reverb").grid_columnconfigure(0, weight=1)
        self.listview.tab("Reverb").grid_rowconfigure(0, weight=1)

        self.subito_list = ctk.CTkScrollableFrame(self.listview.tab("Subito"), label_text="Tracking prodotti Subito.it")
        self.subito_list.grid(row=0, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.subito_list.grid_columnconfigure((1, 2, 3, 4, 5), weight=1)
        self.subito_list.grid_columnconfigure(0, weight=0)

        self.mercatino_list = ctk.CTkScrollableFrame(self.listview.tab("Mercatino"), label_text="Tracking prodotti Mercatino Musicale")
        self.mercatino_list.grid(row=0, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.mercatino_list.grid_columnconfigure((1, 2, 3, 4, 5), weight=1)
        self.mercatino_list.grid_columnconfigure(0, weight=0)

        self.ebay_list = ctk.CTkScrollableFrame(self.listview.tab("Ebay"), label_text="Tracking prodotti Ebay")
        self.ebay_list.grid(row=0, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.ebay_list.grid_columnconfigure((0, 1), weight=0)

        self.reverb_list = ctk.CTkScrollableFrame(self.listview.tab("Reverb"), label_text="Tracking prodotti Reverb")
        self.reverb_list.grid(row=0, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.reverb_list.grid_columnconfigure((0, 1), weight=0)

        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

        # Set up Chrome options
        self.chrome_options = Options()
        self.chrome_options.add_argument("--start-minimized")  # Start the browser minimized
        self.chrome_options.add_argument("--disable-infobars")  # Disable Chrome's info bars
        self.chrome_options.add_argument("--disable-notifications")  # Disable notifications
        self.chrome_options.add_argument("--disable-popup-blocking")  # Disable popup blocking

        # To prevent focus, set window size and position (optional)
        self.chrome_options.add_argument("--window-size=800,600")
        self.chrome_options.add_argument("--window-position=3000,2000")  # Move off-screen

        self.load_chat_id()
        self.send_to_dev(f"{CHAT_ID} started the program")
        
    def load_subito_threading(self):
        self.subito_thread = threading.Thread(target=self.make_subito_requests)
        self.subito_thread.daemon = True
        self.subito_thread.start()


    def load_mercatino_threading(self):
        self.mercatino_thread = threading.Thread(target=self.make_mercatino_requests)
        self.mercatino_thread.daemon = True
        self.mercatino_thread.start()

    def load_ebay_threading(self):
        self.ebay_thread = threading.Thread(target=self.make_ebay_requests)
        self.ebay_thread.daemon = True
        self.ebay_thread.start()

    def load_reverb_threading(self):
        self.reverb_thread = threading.Thread(target=self.make_reverb_requests)
        self.reverb_thread.daemon = True
        self.reverb_thread.start()
    
    def load_threading(self):
        self.load_subito_threading()
        self.load_mercatino_threading()
        self.load_ebay_threading()
        self.load_reverb_threading()

    def load_all(self):
        self.load_subito_search()
        self.reload_subito_listing()
        self.load_mercatino_search()
        self.reload_mercatino_listing()
        self.reload_ebay_listing()
        self.reload_reverb_listing()
        self.load_threading()

    def open_chat_id_event(self):
        dialog = ctk.CTkInputDialog(text="Inserisci il tuo Chat ID:", title="Chat ID")
        return dialog.get_input()

    def load_chat_id(self):
        global CHAT_ID
        CHAT_ID = None
        file_path = Path(os.getcwd()) / "utils" / "chat_id.txt"
        if not os.path.exists(file_path):
            while CHAT_ID == None:
                CHAT_ID = self.open_chat_id_event()
            with open(file_path, "w") as f:
                f.write(CHAT_ID)
            self.send_to_dev(f"{CHAT_ID} Ha avviato il programma per la prima volta!")
        else:
            with open(file_path, "r") as f:
                CHAT_ID = f.readline()
        self.chat_id_label = ctk.CTkLabel(self.sidebar_frame, text=f"CHAT_ID: {CHAT_ID}",
                                    font=ctk.CTkFont(size=20, weight="bold"))
        self.chat_id_label.grid(row=1, column=0, padx=20, pady=(20, 10))
        self.load_all()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)

    def toggle_request_track(self, id: str, website: str):
        if website == "subito":
            active = richieste_subito[id]["active"]
            richieste_subito[id]["active"] = 1 - active
            save_subito_requests()
        elif website == "mercatino":
            active = richieste_mercatino[id]["active"]
            richieste_mercatino[id]["active"] = 1 - active
            save_mercatino_requests()
        elif website == "ebay":
            active = richieste_ebay[id]["active"]
            richieste_ebay[id]["active"] = 1 - active
            save_ebay_requests()
        elif website == "reverb":
            active = richieste_reverb[id]["active"]
            richieste_reverb[id]["active"] = 1 - active
            save_reverb_requests()

    def check_new(self, richieste, beauty):
        for req in richieste.keys():
            if richieste[req]['beauty'] == beauty:
                return False
        return True

    def add_subito_request(self, params, beauty, url):
        if richieste_subito:
            id = str(max((int(x) for x in richieste_subito.keys())) + 1)
        else:
            id = str(0)
        if self.check_new(richieste_subito, beauty):
            richieste_subito[id] = {'params': params, 'active': 1, 'products': [], 'beauty': beauty, 'url': url}
            save_subito_requests()

    def add_mercatino_request(self, params, beauty):
        if richieste_mercatino:
            id = str(max((int(x) for x in richieste_mercatino.keys())) + 1)
        else:
            id = str(0)
        if self.check_new(richieste_mercatino, beauty):
            richieste_mercatino[id] = {'params': params, 'active': 1, 'products': [], 'beauty': beauty}
            save_mercatino_requests()

    def open_delete_confirmation(self, id: str, website: str):
        self.delete_confirmation = ctk.CTkToplevel()
        self.delete_confirmation.title("Conferma eliminazione")
        confirmation_label = ctk.CTkLabel(self.delete_confirmation,
                                          text="La cancellazione è irreversibile\nPerderai ogni traccia di questo prodotto",
                                          font=("Calibri", 20))
        confirmation_label.grid(row=0, column=0, columnspan=2, padx=(20, 20), pady=(20, 20))
        confirm_button = ctk.CTkButton(self.delete_confirmation, text="CONFERMA", fg_color="red", anchor="center",
                                       font=("Calibri", 15), width=100)
        confirm_button.configure(command=lambda id=id, website=website: self.delete_request_track(id, website))
        confirm_button.grid(row=1, column=0, padx=(20, 20), pady=(10, 20))
        abort_button = ctk.CTkButton(self.delete_confirmation, text="ANNULLA", anchor="center", font=("Calibri", 15),
                                     width=100)
        abort_button.configure(command=self.delete_confirmation.destroy)
        abort_button.grid(row=1, column=1, padx=(20, 20), pady=(10, 20))
        self.delete_confirmation.focus_force()

    def delete_request_track(self, id: str, website: str):
        if website == "subito":
            del richieste_subito[id]
            self.reload_subito_listing()
        else:
            del richieste_mercatino[id]
            self.reload_mercatino_listing()
        self.delete_confirmation.destroy()

    def load_subito_listing_headers(self):
        subito_listing_active_label = ctk.CTkLabel(self.subito_list, text="ON/OFF", anchor="center",
                                                   font=("Calibri", 25))
        subito_listing_active_label.grid(row=0, column=0, padx=10, pady=(0, 0))
        subito_listing_keyword_label = ctk.CTkLabel(self.subito_list, text="OGGETTO", anchor="center",
                                                    font=("Calibri", 25))
        subito_listing_keyword_label.grid(row=0, column=1, padx=10, pady=(0, 0))
        subito_listing_category_label = ctk.CTkLabel(self.subito_list, text="CATEGORIA", anchor="center",
                                                     font=("Calibri", 25))
        subito_listing_category_label.grid(row=0, column=2, padx=10, pady=(0, 0))
        subito_listing_region_label = ctk.CTkLabel(self.subito_list, text="REGIONE", anchor="center",
                                                   font=("Calibri", 25))
        subito_listing_region_label.grid(row=0, column=3, padx=10, pady=(0, 0))
        subito_listing_type_label = ctk.CTkLabel(self.subito_list, text="TIPO", anchor="center", font=("Calibri", 25))
        subito_listing_type_label.grid(row=0, column=4, padx=10, pady=(0, 0))

    def reload_subito_listing(self, id: str = None):
        for widget in self.subito_list.winfo_children():
            widget.destroy()

        self.load_subito_listing_headers()
        self.subito_list_switches = []
        for id in richieste_subito.keys():
            subito_header_separator = tk.ttk.Separator(self.subito_list, orient="horizontal")
            subito_header_separator.grid(row=len(self.subito_list_switches) + 1, column=0, columnspan=6, padx=(20, 20),
                                         pady=(30, 10), sticky="ew")

            switch_var = ctk.IntVar(value=richieste_subito[id]['active'])
            switch = ctk.CTkSwitch(master=self.subito_list, variable=switch_var, text="")
            switch.grid(row=len(self.subito_list_switches) + 2, column=0, padx=(60, 0), pady=(0, 20), sticky='ns')
            switch.configure(command=lambda id=id: self.toggle_request_track(id, website="subito"))
            self.subito_list_switches.append((switch, id))

            keyword = ctk.CTkLabel(self.subito_list, text=richieste_subito[id]['beauty']['keyword'], anchor="center",
                                   font=("Calibri", 15))
            keyword.grid(row=len(self.subito_list_switches) + 1, column=1, padx=10, pady=(0, 20), sticky='ns')
            category = ctk.CTkLabel(self.subito_list, text=richieste_subito[id]['beauty']['category'], anchor="center",
                                    font=("Calibri", 15))
            category.grid(row=len(self.subito_list_switches) + 1, column=2, padx=10, pady=(0, 20), sticky='ns')
            region = ctk.CTkLabel(self.subito_list, text=richieste_subito[id]['beauty']['region'], anchor="center",
                                  font=("Calibri", 15))
            region.grid(row=len(self.subito_list_switches) + 1, column=3, padx=10, pady=(0, 20), sticky='ns')
            tipo = ctk.CTkLabel(self.subito_list, text=richieste_subito[id]['beauty']['type'], anchor="center",
                                font=("Calibri", 15))
            tipo.grid(row=len(self.subito_list_switches) + 1, column=4, padx=10, pady=(0, 20), sticky='ns')
            delete = ctk.CTkButton(self.subito_list, text="ELIMINA", anchor="center", font=("Calibri", 20),
                                   fg_color="red", width=85)
            delete.configure(command=lambda id=id: self.open_delete_confirmation(id, website="subito"))
            delete.grid(row=len(self.subito_list_switches) + 1, column=5, padx=10, pady=(0, 20), sticky='ns')
        self.subito_list.update()

    def load_mercatino_listing_headers(self):
        mercatino_listing_active_label = ctk.CTkLabel(self.mercatino_list, text="ON/OFF", anchor="center",
                                                        font=("Calibri", 25))
        mercatino_listing_active_label.grid(row=0, column=0, padx=10, pady=(0, 0))
        mercatino_listing_keyword_label = ctk.CTkLabel(self.mercatino_list, text="OGGETTO", anchor="center",
                                                        font=("Calibri", 25))
        mercatino_listing_keyword_label.grid(row=0, column=1, padx=10, pady=(0, 0))
        mercatino_listing_brand_label = ctk.CTkLabel(self.mercatino_list, text="BRAND", anchor="center",
                                                        font=("Calibri", 25))
        mercatino_listing_brand_label.grid(row=0, column=2, padx=10, pady=(0, 0))
        mercatino_listing_reparto_label = ctk.CTkLabel(self.mercatino_list, text="REPARTO", anchor="center",
                                                        font=("Calibri", 25))
        mercatino_listing_reparto_label.grid(row=0, column=3, padx=10, pady=(0, 0))
        mercatino_listing_category_label = ctk.CTkLabel(self.mercatino_list, text="CATEGORIA", anchor="center",
                                                        font=("Calibri", 25))
        mercatino_listing_category_label.grid(row=0, column=4, padx=10, pady=(0, 0))
        mercatino_listing_region_label = ctk.CTkLabel(self.mercatino_list, text="REGIONE", anchor="center",
                                                        font=("Calibri", 25))
        mercatino_listing_region_label.grid(row=0, column=5, padx=10, pady=(0, 0))
        mercatino_listing_type_label = ctk.CTkLabel(self.mercatino_list, text="TIPO", anchor="center", font=("Calibri", 25))
        mercatino_listing_type_label.grid(row=0, column=6, padx=10, pady=(0, 0))

    def reload_mercatino_listing(self, id: str = None):
        for widget in self.mercatino_list.winfo_children():
            widget.destroy()

        self.load_mercatino_listing_headers()
        self.mercatino_list_switches = []
        for id in richieste_mercatino.keys():
            mercatino_header_separator = tk.ttk.Separator(self.mercatino_list, orient="horizontal")
            mercatino_header_separator.grid(row=len(self.mercatino_list_switches) + 1, column=0, columnspan=8, padx=(20, 20),
                                         pady=(30, 10), sticky="ew")

            switch_var = ctk.IntVar(value=richieste_mercatino[id]['active'])
            switch = ctk.CTkSwitch(master=self.mercatino_list, variable=switch_var, text="")
            switch.grid(row=len(self.mercatino_list_switches) + 2, column=0, padx=(60, 0), pady=(0, 20), sticky='ns')
            switch.configure(command=lambda id=id: self.toggle_request_track(id, website="mercatino"))
            self.mercatino_list_switches.append((switch, id))

            keyword = ctk.CTkLabel(self.mercatino_list, text=richieste_mercatino[id]['beauty']['keyword'], anchor="center",
                                   font=("Calibri", 15))
            keyword.grid(row=len(self.mercatino_list_switches) + 1, column=1, padx=10, pady=(0, 20), sticky='ns')
            brand = ctk.CTkLabel(self.mercatino_list, text=richieste_mercatino[id]['beauty']['brand'], anchor="center",
                                    font=("Calibri", 15))
            brand.grid(row=len(self.mercatino_list_switches) + 1, column=2, padx=10, pady=(0, 20), sticky='ns')
            reparto = ctk.CTkLabel(self.mercatino_list, text=richieste_mercatino[id]['beauty']['reparto'], anchor="center",
                                  font=("Calibri", 15))
            reparto.grid(row=len(self.mercatino_list_switches) + 1, column=3, padx=10, pady=(0, 20), sticky='ns')
            category = ctk.CTkLabel(self.mercatino_list, text=richieste_mercatino[id]['beauty']['category'], anchor="center",
                                font=("Calibri", 15))
            category.grid(row=len(self.mercatino_list_switches) + 1, column=4, padx=10, pady=(0, 20), sticky='ns')
            region = ctk.CTkLabel(self.mercatino_list, text=richieste_mercatino[id]['beauty']['region'], anchor="center",
                                font=("Calibri", 15))
            region.grid(row=len(self.mercatino_list_switches) + 1, column=5, padx=10, pady=(0, 20), sticky='ns')
            tipo = ctk.CTkLabel(self.mercatino_list, text=richieste_mercatino[id]['beauty']['type'], anchor="center",
                                font=("Calibri", 15))
            tipo.grid(row=len(self.mercatino_list_switches) + 1, column=6, padx=10, pady=(0, 20), sticky='ns')
            delete = ctk.CTkButton(self.mercatino_list, text="ELIMINA", anchor="center", font=("Calibri", 20),
                                   fg_color="red", width=85)
            delete.configure(command=lambda id=id: self.open_delete_confirmation(id, website="mercatino"))
            delete.grid(row=len(self.mercatino_list_switches) + 1, column=7, padx=10, pady=(0, 20), sticky='ns')
        self.mercatino_list.update()

    def load_ebay_listing_headers(self):
        ebay_listing_active_label = ctk.CTkLabel(self.ebay_list, text="ON/OFF", anchor="center",
                                                        font=("Calibri", 25))
        ebay_listing_active_label.grid(row=0, column=0, padx=10, pady=(0, 0))
        ebay_listing_category_label = ctk.CTkLabel(self.ebay_list, text="CATEGORIA", anchor="center",
                                                        font=("Calibri", 25))
        ebay_listing_category_label.grid(row=0, column=1, padx=10, pady=(0, 0))

    def reload_ebay_listing(self, id: str = None):
        for widget in self.ebay_list.winfo_children():
            widget.destroy()

        self.load_ebay_listing_headers()
        self.ebay_list_switches = []
        for id in richieste_ebay.keys():
            ebay_header_separator = tk.ttk.Separator(self.ebay_list, orient="horizontal")
            ebay_header_separator.grid(row=len(self.ebay_list_switches) + 1, column=0, columnspan=6, padx=(20, 20),
                                         pady=(30, 10), sticky="ew")

            switch_var = ctk.IntVar(value=richieste_ebay[id]['active'])
            switch = ctk.CTkSwitch(master=self.ebay_list, variable=switch_var, text="")
            switch.grid(row=len(self.ebay_list_switches) + 2, column=0, padx=(60, 0), pady=(0, 20), sticky='ns')
            switch.configure(command=lambda id=id: self.toggle_request_track(id, website="ebay"))
            self.ebay_list_switches.append((switch, id))

            category = ctk.CTkLabel(self.ebay_list, text=richieste_ebay[id]['category'], anchor="center",
                                    font=("Calibri", 15))
            category.grid(row=len(self.ebay_list_switches) + 1, column=1, padx=10, pady=(0, 20), sticky='ns')
        self.ebay_list.update()

    def load_reverb_listing_headers(self):
        reverb_listing_active_label = ctk.CTkLabel(self.reverb_list, text="ON/OFF", anchor="center",
                                                        font=("Calibri", 25))
        reverb_listing_active_label.grid(row=0, column=0, padx=10, pady=(0, 0))
        reverb_listing_category_label = ctk.CTkLabel(self.reverb_list, text="CATEGORIA", anchor="center",
                                                        font=("Calibri", 25))
        reverb_listing_category_label.grid(row=0, column=1, padx=10, pady=(0, 0))

    def reload_reverb_listing(self, id: str = None):
        for widget in self.reverb_list.winfo_children():
            widget.destroy()

        self.load_reverb_listing_headers()
        self.reverb_list_switches = []
        for id in richieste_reverb.keys():
            reverb_header_separator = tk.ttk.Separator(self.reverb_list, orient="horizontal")
            reverb_header_separator.grid(row=len(self.reverb_list_switches) + 1, column=0, columnspan=6, padx=(20, 20),
                                         pady=(30, 10), sticky="ew")

            switch_var = ctk.IntVar(value=richieste_reverb[id]['active'])
            switch = ctk.CTkSwitch(master=self.reverb_list, variable=switch_var, text="")
            switch.grid(row=len(self.reverb_list_switches) + 2, column=0, padx=(60, 0), pady=(0, 20), sticky='ns')
            switch.configure(command=lambda id=id: self.toggle_request_track(id, website="reverb"))
            self.reverb_list_switches.append((switch, id))

            category = ctk.CTkLabel(self.reverb_list, text=richieste_reverb[id]['category'], anchor="center",
                                    font=("Calibri", 15))
            category.grid(row=len(self.reverb_list_switches) + 1, column=1, padx=10, pady=(0, 20), sticky='ns')
        self.reverb_list.update()

    def autocomplete_subito_category(self, event):
        typed_text = self.subito_category.get()  # Ottieni il testo digitato nel Combobox
        matching_options = [option for option in list(S_CATEGORIE.keys()) if
                            option.lower().startswith(typed_text.lower())]
        self.subito_category.configure(values=matching_options)

    def open_subito_search_confirmation(self):
        keyword = self.subito_keyword.get()
        if keyword:
            self.subito_search_confirmation = None
            self.validate_subito()
        else:
            self.subito_search_confirmation = ctk.CTkToplevel()
            self.subito_search_confirmation.title("Conferma ricerca")
            confirmation_label = ctk.CTkLabel(self.subito_search_confirmation,
                                              text="Stai provando a fare una ricerca senza\nspecificare alcun prodotto.\nConfermi?",
                                              font=("Calibri", 20))
            confirmation_label.grid(row=0, column=0, columnspan=2, padx=(20, 20), pady=(20, 20))
            confirm_button = ctk.CTkButton(self.subito_search_confirmation, text="CONFERMA", fg_color="green",
                                           anchor="center", font=("Calibri", 15), width=100)
            confirm_button.configure(command=self.validate_subito)
            confirm_button.grid(row=1, column=1, padx=(20, 20), pady=(10, 20))
            abort_button = ctk.CTkButton(self.subito_search_confirmation, text="ANNULLA", anchor="center",
                                         font=("Calibri", 15), width=100)
            abort_button.configure(command=self.subito_search_confirmation.destroy)
            abort_button.grid(row=1, column=0, padx=(20, 20), pady=(10, 20))
            self.subito_search_confirmation.focus_force()

    def open_wrong_category(self, category: str):
        self.wrong_category = ctk.CTkToplevel()
        self.wrong_category.title("Categoria incorretta")
        wrong_label = ctk.CTkLabel(self.wrong_category,
                                   text=f"La categoria \"{category}\" che hai inserito,\nnon è presente nella lista",
                                   font=("Calibri", 20))
        wrong_label.grid(row=0, column=0, padx=(20, 20), pady=(20, 20))
        abort_button = ctk.CTkButton(self.wrong_category, text="CHIUDI", anchor="center", font=("Calibri", 15),
                                     width=100)
        abort_button.configure(command=self.wrong_category.destroy)
        abort_button.grid(row=1, column=0, padx=(20, 20), pady=(10, 20))
        self.wrong_category.focus_force()

    def open_wrong_brand(self, brand: str):
        self.wrong_brand = ctk.CTkToplevel()
        self.wrong_brand.title("Marca incorretta")
        wrong_label = ctk.CTkLabel(self.wrong_brand,
                                   text=f"La marca \"{brand}\" che hai inserito,\nnon è presente nella lista",
                                   font=("Calibri", 20))
        wrong_label.grid(row=0, column=0, padx=(20, 20), pady=(20, 20))
        abort_button = ctk.CTkButton(self.wrong_brand, text="CHIUDI", anchor="center", font=("Calibri", 15),
                                     width=100)
        abort_button.configure(command=self.wrong_brand.destroy)
        abort_button.grid(row=1, column=0, padx=(20, 20), pady=(10, 20))
        self.wrong_brand.focus_force()

    def validate_subito(self):
        if self.subito_search_confirmation:
            self.subito_search_confirmation.destroy()
        keyword = self.subito_keyword.get()
        category = self.subito_category.get()
        region = self.subito_region.get()
        tipo = self.subito_type.get()
        url_category = str(S_CATEGORIE.get(category))
        url = SUBITO_URL + url_category + "/"
        params = {
            'q': keyword,
            'sort': 'datedesc',  # (relevance/datadesc/priceasc/pricedesc) priceasc = dal meno caro
        }
        beauty = {
            'keyword': keyword,
            'category': category.strip(),
            'type': tipo,
            'region': region
        }
        self.add_subito_request(params, beauty, url)
        self.reload_subito_listing()
        self.subito_keyword.delete(0, "end")

    def validate_mercatino(self):
        if self.mercatino_search_confirmation:
            self.mercatino_search_confirmation.destroy()
        keyword = self.mercatino_keyword.get()
        reparto = self.mercatino_reparto.get()
        category = self.mercatino_category.get()       
        brand = self.mercatino_brand.get()
        region = self.mercatino_region.get()
        tipo = self.mercatino_type.get()
        if brand in M_BRANDS.keys():
            params = {
                'ns': '1',
                'kw': keyword,
                'mc': str(M_BRANDS.get(brand)),
                'rp': str(M_REPARTO.get(reparto)),
                'gp': str(M_TIPO.get(tipo)),
                '_rgpv': str(M_ZONA.get(region)),
                'ob': 'data',
            }
            if params["rp"]:
                params['ct'] = str(M_CATEGORIE.get(M_REPARTO.get(reparto)).get(category, ""))
            else:
                params['ct'] = ""
            if category == "Seleziona la categoria":
                category = "---"
            beauty = {
                'keyword': keyword,
                'reparto': reparto,
                'category': category,
                'brand': brand,
                'type': tipo,
                'region': region.replace("     ", "")
            }
            self.add_mercatino_request(params, beauty)
            self.reload_mercatino_listing()
            self.mercatino_keyword.delete(0, "end")
        else:
            self.open_wrong_brand(brand)

    def open_mercatino_search_confirmation(self):
        keyword = self.mercatino_keyword.get()
        if keyword:
            self.mercatino_search_confirmation = None
            self.validate_mercatino()
        else:
            self.mercatino_search_confirmation = ctk.CTkToplevel()
            self.mercatino_search_confirmation.title("Conferma ricerca")
            confirmation_label = ctk.CTkLabel(self.mercatino_search_confirmation,
                                              text="Stai provando a fare una ricerca senza\nspecificare alcun prodotto.\nConfermi?",
                                              font=("Calibri", 20))
            confirmation_label.grid(row=0, column=0, columnspan=2, padx=(20, 20), pady=(20, 20))
            confirm_button = ctk.CTkButton(self.mercatino_search_confirmation, text="CONFERMA", fg_color="green",
                                           anchor="center", font=("Calibri", 15), width=100)
            confirm_button.configure(command=self.validate_mercatino)
            confirm_button.grid(row=1, column=1, padx=(20, 20), pady=(10, 20))
            abort_button = ctk.CTkButton(self.mercatino_search_confirmation, text="ANNULLA", anchor="center",
                                         font=("Calibri", 15), width=100)
            abort_button.configure(command=self.mercatino_search_confirmation.destroy)
            abort_button.grid(row=1, column=0, padx=(20, 20), pady=(10, 20))
            self.mercatino_search_confirmation.focus_force()

    def autocomplete_mercatino_brand(self, event):
        typed_text = self.mercatino_brand.get()  # Ottieni il testo digitato nel Combobox
        matching_options = [option for option in list(M_BRANDS.keys()) if option.lower().startswith(typed_text.lower())]
        self.mercatino_brand.configure(values=matching_options)

    def on_reparto_selected(self, event):
        selected_reparto = self.mercatino_reparto.get()
        selected_reparto_value = M_REPARTO.get(selected_reparto)
        if selected_reparto_value:
            self.mercatino_category.configure(state="normal", values=list(M_CATEGORIE[selected_reparto_value].keys()))

        else:
            self.mercatino_category.destroy()
            self.mercatino_category = ctk.CTkOptionMenu(self.searchview.tab("Mercatino"), width=200, state="disabled",
                                                        values=[''.join(M_CATEGORIE['0'])])
            self.mercatino_category.grid(row=1, column=2, padx=20)

    def load_subito_search(self):
            self.subito_keyword_label = ctk.CTkLabel(self.searchview.tab("Subito"), text="Cosa cerchi?", anchor="w",
                                                    font=("Calibri", 17))
            self.subito_keyword_label.grid(row=0, column=0, padx=20, pady=(10, 0))
            self.subito_keyword = ctk.CTkEntry(self.searchview.tab("Subito"),
                                            placeholder_text="Tastiera, Chitarra, Microfono", width=200, height=30)
            self.subito_keyword.grid(row=1, column=0, padx=20)

            self.subito_category_label = ctk.CTkLabel(self.searchview.tab("Subito"), text="In quale categoria?", anchor="w",
                                                    font=("Calibri", 17))
            self.subito_category_label.grid(row=0, column=1, padx=20, pady=(10, 0))
            self.subito_category = ctk.CTkComboBox(self.searchview.tab("Subito"), width=200,
                                                values=list(S_CATEGORIE.keys()))
            self.subito_category.grid(row=1, column=1, padx=20)
            self.subito_category.bind('<KeyRelease>', self.autocomplete_subito_category)

            self.subito_region_label = ctk.CTkLabel(self.searchview.tab("Subito"), text="Dove?", anchor="w",
                                                    font=("Calibri", 17))
            self.subito_region_label.grid(row=0, column=2, padx=20, pady=(10, 0))
            self.subito_region = ctk.CTkOptionMenu(self.searchview.tab("Subito"), width=200,
                                                values=list(S_REGIONI.keys()), state="disabled")
            self.subito_region.grid(row=1, column=2, padx=20)

            self.subito_shipping_label = ctk.CTkLabel(self.searchview.tab("Subito"), text="Spedizione", anchor="w",
                                                    font=("Calibri", 17))
            self.subito_shipping_label.grid(row=3, column=0, padx=20, pady=(25, 0))
            self.subito_shipping = ctk.CTkSwitch(self.searchview.tab("Subito"),
                                                text="Solo annunci con \nspedizione disponibile")
            self.subito_shipping.grid(row=4, column=0, padx=20)

            self.subito_titlesearch_label = ctk.CTkLabel(self.searchview.tab("Subito"), text="Restringi ricerca",
                                                        anchor="w", font=("Calibri", 17))
            self.subito_titlesearch_label.grid(row=3, column=1, padx=20, pady=(25, 0))
            self.subito_titlesearch = ctk.CTkSwitch(self.searchview.tab("Subito"), text="Cerca solo nel titolo")
            self.subito_titlesearch.grid(row=4, column=1, padx=20)

            self.subito_type_label = ctk.CTkLabel(self.searchview.tab("Subito"), text="Tipo di annuncio", anchor="w",
                                                font=("Calibri", 17))
            self.subito_type_label.grid(row=3, column=2, padx=20, pady=(25, 0))
            self.subito_type = ctk.CTkOptionMenu(self.searchview.tab("Subito"), width=200,
                                                values=list(S_TYPE.keys()), state="disabled")
            self.subito_type.grid(row=4, column=2, padx=20)

            self.subito_search_button = ctk.CTkButton(self.searchview.tab("Subito"), text="Cerca", font=("Calibri", 20),
                                                    command=self.open_subito_search_confirmation)
            self.subito_search_button.grid(row=5, column=2, padx=60, pady=40)

    def load_mercatino_search(self):
        self.mercatino_keyword_label = ctk.CTkLabel(self.searchview.tab("Mercatino"), text="Cosa cerchi?", anchor="w",
                                                    font=("Calibri", 17))
        self.mercatino_keyword_label.grid(row=0, column=0, padx=20, pady=(10, 0))
        self.mercatino_keyword = ctk.CTkEntry(self.searchview.tab("Mercatino"),
                                              placeholder_text="Tastiera, Chitarra, Microfono", width=200, height=30)
        self.mercatino_keyword.grid(row=1, column=0, padx=20)

        self.mercatino_reparto_label = ctk.CTkLabel(self.searchview.tab("Mercatino"), text="Reparto:", anchor="w",
                                                    font=("Calibri", 17))
        self.mercatino_reparto_label.grid(row=0, column=1, padx=20, pady=(10, 0))
        self.mercatino_reparto = ctk.CTkOptionMenu(self.searchview.tab("Mercatino"), width=200,
                                                   values=list(M_REPARTO.keys()), command=self.on_reparto_selected)
        self.mercatino_reparto.grid(row=1, column=1, padx=20)

        self.mercatino_category_label = ctk.CTkLabel(self.searchview.tab("Mercatino"), text="Categoria:", anchor="w",
                                                     font=("Calibri", 17))
        self.mercatino_category_label.grid(row=0, column=2, padx=20, pady=(10, 0))
        self.mercatino_category = ctk.CTkOptionMenu(self.searchview.tab("Mercatino"), width=200, state="disabled",
                                                    values=[''.join(M_CATEGORIE['0'])])
        self.mercatino_category.grid(row=1, column=2, padx=20)

        self.mercatino_brand_label = ctk.CTkLabel(self.searchview.tab("Mercatino"), text="Marca:", anchor="w",
                                                  font=("Calibri", 17))
        self.mercatino_brand_label.grid(row=2, column=0, padx=20, pady=(10, 0))
        self.mercatino_brand = ctk.CTkComboBox(self.searchview.tab("Mercatino"), width=200,
                                               values=list(M_BRANDS.keys()))
        self.mercatino_brand.grid(row=3, column=0, padx=20)
        self.mercatino_brand.bind("<KeyRelease>", self.autocomplete_mercatino_brand)

        self.mercatino_region_label = ctk.CTkLabel(self.searchview.tab("Mercatino"), text="Zona:", anchor="w",
                                                   font=("Calibri", 17))
        self.mercatino_region_label.grid(row=2, column=1, padx=20, pady=(10, 0))
        self.mercatino_region = ctk.CTkOptionMenu(self.searchview.tab("Mercatino"), width=200,
                                                  values=list(M_ZONA.keys()))
        self.mercatino_region.grid(row=3, column=1, padx=20)

        self.mercatino_type_label = ctk.CTkLabel(self.searchview.tab("Mercatino"), text="Tipo annuncio", anchor="w",
                                                 font=("Calibri", 17))
        self.mercatino_type_label.grid(row=2, column=2, padx=20, pady=(25, 0))
        self.mercatino_type = ctk.CTkOptionMenu(self.searchview.tab("Mercatino"), width=200,
                                                values=list(M_TIPO.keys()))
        self.mercatino_type.grid(row=3, column=2, padx=20)

        self.mercatino_search_button = ctk.CTkButton(self.searchview.tab("Mercatino"), text="Cerca",
                                                     font=("Calibri", 20),
                                                     command=self.open_mercatino_search_confirmation)
        self.mercatino_search_button.grid(row=4, column=2, padx=60, pady=40)

        self.searchview.tab("Mercatino").update()

    def telegram_message(self, message):
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
        requests.get(url)

    def send_to_dev(self, message):
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={DEV_ID}&text={message}"
        requests.get(url)
        
    def send_file_to_dev(self, file_path):
        url = f"https://api.telegram.org/bot{TOKEN}/sendDocument"
        files = {"document": open(file_path, "rb")}
        data = {"chat_id": DEV_ID}
        
        response = requests.post(url, data=data, files=files)
        return response.json()  # To check for success or errors

    def make_subito_requests(self):
        send = False
        while True:
            attuale = copy.deepcopy(richieste_subito)
            for req in attuale.keys():
                if attuale[req]['active']:
                    try:
                        response = requests.get(attuale[req]["url"], params=attuale[req]['params'], headers=SUBITO_HEADERS)
                        soup = bs(response.text, "html.parser")
                        datas = soup.find('script', id='__NEXT_DATA__')
                        json_text = datas.string
                        data = json.loads(json_text)
                        items_list = data["props"]["pageProps"]["initialState"]["items"]["list"]
                        old_products = attuale[req].get("products", [])
                        for item in items_list:
                            urn = item["item"]["urn"]
                            if urn not in old_products:
                                keyword = attuale[req]["beauty"]["keyword"]
                                category = attuale[req]["beauty"]["category"]
                                region = attuale[req]["beauty"]["region"]
                                title = item["item"]["subject"]
                                date = item["item"]["date"].split()[1]
                                price = item["item"]["features"].get("/price", None)
                                if price:
                                    price = price["values"][0]["key"]
                                url = item["item"]["urls"]["default"]
                                message = f'Trovato nuovo prodotto su Subito:\nOggetto: {keyword}\nCategoria: {category}\nRegione: {region}\nPubblicato alle: {date}\n{title}\n{price}€\n{url}'
                                attuale[req]['products'].append(urn)
                                if send:
                                    self.telegram_message(message)
                    except:
                        self.send_to_dev("Subito ha problemi con le richieste")
                    if len(attuale[req]['products']) > 2500:
                        attuale[req]['products'] = attuale[req]['products'][30:]
            send = True
            [richieste_subito[req].update({'products': attuale[req]['products']}) for req in richieste_subito.keys() if req in attuale.keys()]
            time.sleep(30)

    def make_mercatino_requests(self):
        send = False
        while True:
            attuale = copy.deepcopy(richieste_mercatino)
            for req in attuale.keys():
                if attuale[req]['active']:
                    try:
                        response = requests.get(MERCATINO_URL, params=attuale[req]['params'], headers=MERCATINO_HEADERS)
                        soup = bs(response.text, "html.parser")
                        items = soup.find('div', id='search_result').find_all('div', class_='box_prod box_prod_linked')
                        old_products = attuale[req].get("products", [])
                        for item in items:
                            link = item.find('a', class_='box_prod_link')
                            href = link.attrs['href']
                            match = re.search(MERCATINO_ID_PATTERN, href)
                            url = 'https://www.mercatinomusicale.com' + href
                            listing_id = match.group(1)
                            if listing_id not in old_products:
                                keyword = attuale[req]["beauty"]["keyword"]
                                category = attuale[req]["beauty"]["category"]
                                region = attuale[req]["beauty"]["region"]
                                reparto = attuale[req]["beauty"]["reparto"]
                                brand = attuale[req]["beauty"]["brand"]
                                title_span = item.find('span', class_='tit')
                                title = title_span.text
                                opt_span = item.find('span', class_='prz')
                                price = opt_span.text
                                message = f'Trovato nuovo prodotto su Mercatino:\nOggetto: {keyword}\nReparto: {reparto}\nCategoria: {category}\nBrand: {brand}\nRegione: {region}\n{title}\n{price}\n{url}'
                                attuale[req]['products'].append(listing_id)
                                if send:
                                    self.telegram_message(message)                            
                    except:
                        self.telegram_message("Mercatino è in timeout! Cambia la VPN!")
                        self.send_to_dev("Something went wrong with Mercatino!! (Probably IP timeout)")
                    finally:
                        time.sleep(30)
                    if len(attuale[req]['products']) > 2500:
                        attuale[req]['products'] = attuale[req]['products'][30:]      
            else:
                send = True
                if len(attuale) == 0:
                    time.sleep(30)
            [richieste_mercatino[req].update({'products': attuale[req]['products']}) for req in richieste_mercatino.keys() if req in attuale.keys()]

    def make_ebay_requests(self):
        send = False
        while True:
            attuale = copy.deepcopy(richieste_ebay)
            for req in attuale.keys():
                if attuale[req]['active']:                    
                    try:
                        response = requests.get(attuale[req]["url"], params=EBAY_PARAMS, headers=EBAY_HEADERS)
                        soup = bs(response.text, "html.parser")
                        items = soup.find('ul', class_='brwrvr__item-results brwrvr__item-results--list').find_all('li', class_='brwrvr__item-card brwrvr__item-card--list')
                        old_products = attuale[req].get("products", [])
                        for item in items:
                            link = item.find('a', class_='brwrvr__item-card__image-link')
                            url = link.attrs['href']
                            title = item.find('h3').text.strip("New Listing")
                            price = item.find('span', class_="textual-display bsig__price bsig__price--displayprice").text
                            shipping = item.find('span', class_="textual-display bsig__price bsig__price--displayprice").text
                            match = re.search(r'/(?:itm|p)/(\d+)\?', url)
                            listing_id = match.group(1)
                            if listing_id not in old_products:
                                message = f'Trovato nuovo prodotto su Ebay nella categoria {attuale[req]["category"]}\n{title}\nPrezzo: {price}\nSpedizione: {shipping}\n{url}'
                                attuale[req]['products'].append(listing_id)
                                if send:
                                    self.telegram_message(message)
                    except:
                        # self.telegram_message("Ebay è in timeout! Cambia la VPN!")
                        self.send_to_dev(f"Something wrong with Ebay")
                        ebay_error_path = Path(os.getcwd()) / "tmp" / "ebay_error.html"
                        with open(ebay_error_path, "w", encoding="utf-8") as f:
                            f.write(response.text)
                        error_message_response = self.send_file_to_dev(ebay_error_path)
                        self.send_to_dev(error_message_response)
                        self.toggle_request_track(req, "ebay")
                    finally:
                        # ebay_try_path = Path(os.getcwd()) / "tmp" / "ebay_try.html"
                        # with open(ebay_try_path, "w", encoding="utf-8") as f:
                        #     f.write(response.text)
                        # try_message = self.send_file_to_dev(ebay_try_path)
                        # self.send_to_dev(try_message)
                        time.sleep(30)
                    if len(attuale[req]['products']) > 2500:
                        attuale[req]['products'] = attuale[req]['products'][30:]      
            else:
                send = True
                if len(attuale) == 0:
                    time.sleep(30)
            [richieste_ebay[req].update({'products': attuale[req]['products']}) for req in richieste_ebay.keys() if req in attuale.keys()]

    def make_reverb_requests(self):
        send = False
        while True:
            attuale = copy.deepcopy(richieste_reverb)
            for req in attuale.keys():
                if attuale[req]['active']:    
                    driver = webdriver.Chrome(options=self.chrome_options)
                    try:
                        url = attuale[req]["url"]
                        driver.get(url)
                        time.sleep(10)
                        WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "rc-listing-grid__item"))
                        )
                        products = driver.find_elements(By.CLASS_NAME, "rc-listing-grid__item")
                        old_products = attuale[req].get("products", [])
                        for product in products:
                            try:
                                title_element = product.find_element(By.CLASS_NAME, "rc-listing-card__title")
                                title = title_element.text
                                price_element = product.find_element(By.CLASS_NAME, "rc-price-block__price")
                                price = price_element.text
                                link_element = product.find_element(By.CLASS_NAME, "rc-listing-card__title-link")
                                link = link_element.get_attribute("href")
                                match = re.search(r'/item/(\d+)', link)
                                if match:
                                    item_id = match.group(1)
                                    if item_id not in old_products:
                                        message = f'Trovato nuovo prodotto su Reverb nella categoria {attuale[req]["category"]}\n{title}\nPrezzo: {price}\n{link}'
                                        attuale[req]['products'].append(item_id)
                                        if send:
                                            self.telegram_message(message)
                            except:
                                print("Dettagli del prodotto non trovati")
                    except:
                        print("Qualcosa è andato storto con Reverb")
                    finally:
                        driver.quit()
                        time.sleep(30)
                    if len(attuale[req]['products']) > 2500:
                        attuale[req]['products'] = attuale[req]['products'][30:]      
            else:
                send = True
                if len(attuale) == 0:
                    time.sleep(30)
            [richieste_reverb[req].update({'products': attuale[req]['products']}) for req in richieste_reverb.keys() if req in attuale.keys()]

if __name__ == "__main__":
    load_mappings()
    load_requests()
    app = App()
    app.mainloop()
    save_all()
