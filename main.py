import requests
import json
import threading
import time
import asyncio
import tkinter as tk
import tkinter.messagebox
import customtkinter as ctk
from headers import SUBITO_HEADERS, SUBITO_URL
from telegram import Bot
from my_token import TOKEN, CHAT_ID

bot = Bot(token=TOKEN)
chat_id = CHAT_ID
#TODO ? Prendere da file di testo il chat_id, aprendo una finestra nel caso in cui non esista il file, e facendolo inserire all'utente dando istruzioni

def load_mappings():
    global M_BRANDS, M_CATEGORIE, M_ORDINE, M_REPARTO, M_TIPO, M_ZONA, S_CATEGORIE, S_REGIONI, S_TYPE
    with open("mercatino_mapping\\brands_mapping_mc.json", 'r') as f:
        M_BRANDS = json.load(f)
    with open("mercatino_mapping\\categorie_mapping_ct.json", "r") as f:
        M_CATEGORIE = json.load(f)
    with open("mercatino_mapping\\ordine_mapping_ob.json", "r") as f:
        M_ORDINE = json.load(f)
    with open("mercatino_mapping\\reparto_mapping_rp.json", "r") as f:
        M_REPARTO = json.load(f)
    with open("mercatino_mapping\\tipo_mapping_gp.json", "r") as f:
        M_TIPO = json.load(f)
    with open("mercatino_mapping\\zona_mapping__rgpv.json", "r") as f:
        M_ZONA = json.load(f)
    with open("subito_mapping\\categories_mapping.json", "r") as f:
        S_CATEGORIE = json.load(f)
    with open("subito_mapping\\regions_mapping.json", "r") as f:
        S_REGIONI = json.load(f)
    with open("subito_mapping\\type_mapping.json", "r") as f:
        S_TYPE = json.load(f)


def load_requests():
    global richieste
    with open("richieste.json", "r") as f:
        richieste = json.load(f)
    # s_requests = richieste['subito']
    # m_requests = richieste['mercatino']


def save_requests():
    # richieste['subito'] = s_requests
    # richieste['mercatino'] = m_requests
    with open("richieste.json", "w") as f:
        json.dump(richieste, f, indent=4)


ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Products Notifier")
        self.geometry(f"{1400}x{900}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0), weight=0)
        self.grid_rowconfigure((1), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Products Notifier", font=ctk.CTkFont(size=20, weight="bold"))
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
        self.searchview.tab("Subito").grid_columnconfigure((0,1,2), weight=1)  # configure grid of individual tabs
        self.searchview.tab("Mercatino").grid_columnconfigure(0, weight=1)

        #Sezione di ricerca su Subito
        self.subito_keyword_label = ctk.CTkLabel(self.searchview.tab("Subito"), text="Cosa cerchi?", anchor="w", font=("Calibri",17))
        self.subito_keyword_label.grid(row=0, column=0, padx=20, pady=(10, 0))
        self.subito_keyword = ctk.CTkEntry(self.searchview.tab("Subito"), placeholder_text="Tastiera, Chitarra, Microfono", width=200, height=30)
        self.subito_keyword.grid(row=1, column=0, padx=20)

        self.subito_category_label = ctk.CTkLabel(self.searchview.tab("Subito"), text="In quale categoria?", anchor="w", font=("Calibri",17))
        self.subito_category_label.grid(row=0, column=1, padx=20, pady=(10, 0))
        self.subito_category = ctk.CTkComboBox(self.searchview.tab("Subito"), width=200, values=list(S_CATEGORIE.keys()))
        self.subito_category.grid(row=1, column=1, padx=20)
        self.subito_category.bind('<KeyRelease>', self.autocomplete)

        self.subito_region_label = ctk.CTkLabel(self.searchview.tab("Subito"), text="Dove?", anchor="w", font=("Calibri",17))
        self.subito_region_label.grid(row=0, column=2, padx=20, pady=(10, 0))
        self.subito_region = ctk.CTkOptionMenu(self.searchview.tab("Subito"), width=200,
                                                 values=list(S_REGIONI.keys()))
        self.subito_region.grid(row=1, column=2, padx=20)

        self.subito_shipping_label = ctk.CTkLabel(self.searchview.tab("Subito"), text="Spedizione", anchor="w", font=("Calibri",17))
        self.subito_shipping_label.grid(row=3, column=0, padx=20, pady=(25, 0))
        self.subito_shipping = ctk.CTkSwitch(self.searchview.tab("Subito"), text="Solo annunci con \nspedizione disponibile")
        self.subito_shipping.grid(row=4, column=0, padx=20)

        self.subito_titlesearch_label = ctk.CTkLabel(self.searchview.tab("Subito"), text="Restringi ricerca", anchor="w", font=("Calibri",17))
        self.subito_titlesearch_label.grid(row=3, column=1, padx=20, pady=(25, 0))
        self.subito_titlesearch = ctk.CTkSwitch(self.searchview.tab("Subito"), text="Cerca solo nel titolo")
        self.subito_titlesearch.grid(row=4, column=1, padx=20)

        self.subito_type_label = ctk.CTkLabel(self.searchview.tab("Subito"), text="Tipo di annuncio", anchor="w", font=("Calibri",17))
        self.subito_type_label.grid(row=3, column=2, padx=20, pady=(25, 0))
        self.subito_type = ctk.CTkOptionMenu(self.searchview.tab("Subito"), width=200,
                                             values=list(S_TYPE.keys()))
        self.subito_type.grid(row=4, column=2, padx=20)

        self.subito_search_button = ctk.CTkButton(self.searchview.tab("Subito"), text="Cerca", font=("Calibri", 20),
                                                  command=self.open_subito_search_confirmation)
        self.subito_search_button.grid(row=5, column=2, padx=60, pady=40)


        #Lista delle richieste SUBITO
        self.listview = ctk.CTkTabview(self)
        self.listview.grid(row=1, column=1, columnspan=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.listview.add("Subito")
        self.listview.add("Mercatino")
        self.listview.tab("Subito").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.listview.tab("Subito").grid_rowconfigure(0, weight=1)
        self.listview.tab("Mercatino").grid_columnconfigure(0, weight=1)


        self.subito_list = ctk.CTkScrollableFrame(self.listview.tab("Subito"), label_text="Tracking prodotti Subito.it")
        self.subito_list.grid(row=0, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.subito_list.grid_columnconfigure((1,2,3,4,5), weight=1)
        self.subito_list.grid_columnconfigure(0, weight=0)






        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
   
        self.reload_subito_listing()
        #Threading
        self.thread = threading.Thread(target=self.make_requests)
        self.thread.daemon = True
        self.thread.start()

    def open_input_dialog_event(self):
        dialog = ctk.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())


    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)


    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)


    def sidebar_button_event(self):
        print("sidebar_button click")


    def toggle_request_track(self, id: str):
        richiesta_attiva = richieste[id]['active']
        richieste[id]['active'] = 1 - richiesta_attiva
        save_requests()
        load_requests()


    def add_request(self, params, website, beauty):
        if richieste:
            id = str(max((int(x) for x in richieste.keys())) + 1)
        else:
            id = str(0)
        new_req = True
        for req in richieste.keys():
            if richieste[req]['params'] == params and richieste[req]['website'] == website:
                print("Stai già tracciando lo stesso prodotto")
                new_req = False
        if new_req:
            richieste[id] = {'params': params, 'website': website, 'active': 1, 'products': [], 'beauty': beauty}
            print("Richiesta aggiunta")
            save_requests()




    def open_delete_confirmation(self, id: str):
        self.delete_confirmation = ctk.CTkToplevel()
        self.delete_confirmation.title("Conferma eliminazione")
        confirmation_label = ctk.CTkLabel(self.delete_confirmation, text="La cancellazione è irreversibile\nPerderai ogni traccia di questo prodotto", font=("Calibri",20))
        confirmation_label.grid(row=0, column=0, columnspan=2, padx=(20, 20), pady=(20, 20))
        confirm_button = ctk.CTkButton(self.delete_confirmation, text="CONFERMA", fg_color="red", anchor="center", font=("Calibri",15), width=100)
        confirm_button.configure(command=lambda id=id: self.delete_request_track(id))
        confirm_button.grid(row=1, column=0, padx=(20, 20), pady=(10, 20))
        abort_button = ctk.CTkButton(self.delete_confirmation, text="ANNULLA", anchor="center", font=("Calibri",15), width=100)
        abort_button.configure(command=self.delete_confirmation.destroy)
        abort_button.grid(row=1, column=1, padx=(20, 20), pady=(10, 20))
        self.delete_confirmation.focus_force()


    def delete_request_track(self, id: str):
        website = richieste[id]["website"]
        del richieste[id]
        self.delete_confirmation.destroy()
        save_requests()
        if website == 'subito':
            self.reload_subito_listing()
        else:
            pass
            #TODO
            #self.reload_mercatino_listing()


    def load_subito_listing_headers(self):
        subito_listing_active_label = ctk.CTkLabel(self.subito_list, text="ON/OFF", anchor="center", font=("Calibri",25))
        subito_listing_active_label.grid(row=0, column=0, padx=10, pady=(0,0))
        subito_listing_keyword_label = ctk.CTkLabel(self.subito_list, text="OGGETTO", anchor="center", font=("Calibri",25))
        subito_listing_keyword_label.grid(row=0, column=1, padx=10, pady=(0,0))
        subito_listing_category_label = ctk.CTkLabel(self.subito_list, text="CATEGORIA", anchor="center", font=("Calibri",25))
        subito_listing_category_label.grid(row=0, column=2, padx=10, pady=(0,0))
        subito_listing_region_label = ctk.CTkLabel(self.subito_list, text="REGIONE", anchor="center", font=("Calibri",25))
        subito_listing_region_label.grid(row=0, column=3, padx=10, pady=(0,0))
        subito_listing_type_label = ctk.CTkLabel(self.subito_list, text="TIPO", anchor="center", font=("Calibri",25))
        subito_listing_type_label.grid(row=0, column=4, padx=10, pady=(0,0))


    def reload_subito_listing(self, id: str=None):
        print("Dopo check")
        for widget in self.subito_list.winfo_children():
            widget.destroy()
        print("Dopo reset widgets")

        self.load_subito_listing_headers()    
        self.subito_list_switches = []
        for id in (req for req in richieste.keys() if richieste[req]['website']=='subito'):
            subito_header_separator = tk.ttk.Separator(self.subito_list, orient="horizontal")
            subito_header_separator.grid(row=len(self.subito_list_switches)+1, column=0, columnspan=6, padx=(20,20), pady=(30,10), sticky="ew")

            switch_var = ctk.IntVar(value=richieste[id]['active'])
            switch = ctk.CTkSwitch(master=self.subito_list, variable=switch_var, text="")
            switch.grid(row=len(self.subito_list_switches)+2, column=0, padx=(60,0), pady=(0, 20), sticky='ns')
            switch.configure(command=lambda id=id: self.toggle_request_track(id))
            self.subito_list_switches.append((switch, id))

            keyword = ctk.CTkLabel(self.subito_list, text=richieste[id]['beauty']['keyword'], anchor="center", font=("Calibri",15))
            keyword.grid(row=len(self.subito_list_switches)+1, column=1, padx=10, pady=(0, 20), sticky='ns')
            category = ctk.CTkLabel(self.subito_list, text=richieste[id]['beauty']['category'], anchor="center", font=("Calibri",15))
            category.grid(row=len(self.subito_list_switches)+1, column=2, padx=10, pady=(0, 20), sticky='ns')
            region = ctk.CTkLabel(self.subito_list, text=richieste[id]['beauty']['region'], anchor="center", font=("Calibri",15))
            region.grid(row=len(self.subito_list_switches)+1, column=3, padx=10, pady=(0, 20), sticky='ns')
            tipo = ctk.CTkLabel(self.subito_list, text=richieste[id]['beauty']['type'], anchor="center", font=("Calibri",15))
            tipo.grid(row=len(self.subito_list_switches)+1, column=4, padx=10, pady=(0, 20), sticky='ns')
            delete = ctk.CTkButton(self.subito_list, text="ELIMINA", anchor="center", font=("Calibri",20), fg_color="red", width=85)
            delete.configure(command=lambda id=id: self.open_delete_confirmation(id))
            delete.grid(row=len(self.subito_list_switches)+1, column=5, padx=10, pady=(0, 20), sticky='ns')
        self.subito_list.update()



    def autocomplete(self, event):
        typed_text = self.subito_category.get()  # Ottieni il testo digitato nel Combobox
        matching_options = [option for option in list(S_CATEGORIE.keys()) if option.lower().startswith(typed_text.lower())]

        # Aggiorna le opzioni del Combobox
        self.subito_category['values'] = matching_options  # Aggiorna le nuove opzioni

        # Forza il Combobox a visualizzare le nuove opzioni
        self.subito_category.event_generate("<FocusOut>")  # Genera un evento di uscita focus
        self.subito_category.event_generate("<FocusIn>")  # Genera un evento di entrata focus


        # Se ci sono corrispondenze, mostra l'autocompletamento
        # if matching_options:
        #     # self.subito_category['values'] = matching_options
        #     # self.subito_category.event_generate("<<ComboboxSelected>>")
        #     self.subito_category.set("")  # Resetta il valore del Combobox
        #     self.subito_category['values'] = matching_options  # Aggiorna le nuove opzioni

        #     if matching_options:
        #         self.subito_category.set(matching_options[0])
        #     # Forza il Combobox a visualizzare le nuove opzioni
        #     self.subito_category.event_generate("<FocusOut>")  # Genera un evento di uscita focus
        #     self.subito_category.event_generate("<FocusIn>")  # Genera un evento di entrata focus

    def open_subito_search_confirmation(self):
        keyword = self.subito_keyword.get()
        if keyword:
            self.subito_search_confirmation = None
            self.validate_subito()
        else:
            self.subito_search_confirmation = ctk.CTkToplevel()
            self.subito_search_confirmation.title("Conferma ricerca")
            confirmation_label = ctk.CTkLabel(self.subito_search_confirmation, text="Stai provando a fare una ricerca senza\nspecificare alcun prodotto.\nConfermi?", font=("Calibri",20))
            confirmation_label.grid(row=0, column=0, columnspan=2, padx=(20, 20), pady=(20, 20))
            confirm_button = ctk.CTkButton(self.subito_search_confirmation, text="CONFERMA", fg_color="green", anchor="center", font=("Calibri",15), width=100)
            confirm_button.configure(command=self.validate_subito)
            confirm_button.grid(row=1, column=1, padx=(20, 20), pady=(10, 20))
            abort_button = ctk.CTkButton(self.subito_search_confirmation, text="ANNULLA", anchor="center", font=("Calibri",15), width=100)
            abort_button.configure(command=self.subito_search_confirmation.destroy)
            abort_button.grid(row=1, column=0, padx=(20, 20), pady=(10, 20))
            self.subito_search_confirmation.focus_force()


    def open_wrong_category(self, category: str):
        self.wrong_category = ctk.CTkToplevel()
        self.wrong_category.title("Categoria incorretta")
        wrong_label = ctk.CTkLabel(self.wrong_category, text=f"La categoria \"{category}\" che hai inserito,\nnon è presente nella lista", font=("Calibri",20))
        wrong_label.grid(row=0, column=0, padx=(20, 20), pady=(20, 20))       
        abort_button = ctk.CTkButton(self.wrong_category, text="CHIUDI", anchor="center", font=("Calibri",15), width=100)
        abort_button.configure(command=self.wrong_category.destroy)
        abort_button.grid(row=1, column=0, padx=(20, 20), pady=(10, 20))
        self.wrong_category.focus_force()


    def validate_subito(self):
        if self.subito_search_confirmation:
            self.subito_search_confirmation.destroy()
        keyword = self.subito_keyword.get()
        category = self.subito_category.get()
        region = self.subito_region.get()
        shipping = self.subito_shipping.get() #1 checked, 0 not checked
        title = self.subito_titlesearch.get()
        tipo = self.subito_type.get()
        if category in S_CATEGORIE.keys():
            params = {
                'q': keyword,
                'c': str(S_CATEGORIE.get(category)),
                't': str(S_TYPE.get(tipo)),
                'r': str(S_REGIONI.get(region)),
                'qso': str(bool(title)).lower(), #cerca solo nel titolo (true/false)
                'shp': str(bool(shipping)).lower(), #spedizione disponibile (ture/false)
                'urg': 'false', #annunci urgenti (true/false)
                'sort': 'datedesc', #(relevance/datadesc/priceasc/pricedesc) priceasc = dal meno caro
                'lim': '30',
                'start': '0',
            }            
            beauty = {
                'keyword': keyword,
                'category': category,
                'type': tipo,
                'region': region
            }
            self.add_request(params, 'subito', beauty)
            self.reload_subito_listing()
        else:
            self.open_wrong_category(category)


    async def telegram_message(self, message):
        await bot.send_message(chat_id=chat_id, text=message)


    def make_requests(self):
        while True:
            print("Inizio richieste")
            for req in richieste.keys():
                if richieste[req]['active']:
                    if richieste[req]['website'] == 'subito':
                        response = requests.get(SUBITO_URL, params=richieste[req]['params'], headers=SUBITO_HEADERS)
                        j_response = response.json()
                        old_products = richieste[req].get("products")
                        for product in j_response['ads']:
                            if product['urn'] not in old_products:
                                #TODO send_message()
                                keyword = richieste[req]["beauty"]["keyword"]
                                category = richieste[req]["beauty"]["category"]
                                region = richieste[req]["beauty"]["region"]
                                title = product['subject']
                                price_elem = next((elem for elem in product['features'] if elem.get('label')=="Prezzo"), None)
                                url = product["urls"]["mobile"]
                                if price_elem:
                                    price = price_elem['values'][0]['key']
                                    message = f'Trovato nuovo prodotto per -{keyword}/{category}- in {region}!\n{title}\n{price}€\n{url}'
                                else:
                                    message = f'Trovato nuovo prodotto per -{keyword}/{category}- in {region}!\n{title}\n{url}'
                                print(message)
                                self.telegram_message(message)
                                # bot.send_message(chat_id=chat_id, text=message)

                                richieste[req]['products'].append(product['urn'])
                        if len(richieste[req]['products']) > 150:
                            richieste[req]['products'] = richieste[req]['products'][30:]    
                    else:
                        pass
                        #TODO parte di mercatino
            print("Fine richieste")
            time.sleep(30) 

        

if __name__ == "__main__":
    load_mappings()
    load_requests()
    app = App()
    app.mainloop()
    save_requests()