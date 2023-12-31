import requests
import json
import threading
import tkinter
import tkinter.messagebox
import customtkinter as ctk

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Products Notifier")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Products Notifier", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = ctk.CTkButton(self.sidebar_frame, text="Subito", command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = ctk.CTkButton(self.sidebar_frame, text="Mercatino", command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = ctk.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
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

        # create main entry and button
        self.entry = ctk.CTkEntry(self, placeholder_text="CTkEntry")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = ctk.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create textbox
        # self.textbox = ctk.CTkTextbox(self, width=250)
        # self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # create tabview
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=1, columnspan=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.tabview.add("Subito")
        self.tabview.add("Mercatino")
        self.tabview.tab("Subito").grid_columnconfigure((0,1,2), weight=1)  # configure grid of individual tabs
        self.tabview.tab("Mercatino").grid_columnconfigure(0, weight=1)

        #Sezione di ricerca su Subito
        self.subito_keyword_label = ctk.CTkLabel(self.tabview.tab("Subito"), text="Cosa cerchi?", anchor="w", font=("Calibri",17))
        self.subito_keyword_label.grid(row=0, column=0, padx=20, pady=(10, 0))
        self.subito_keyword = ctk.CTkEntry(self.tabview.tab("Subito"), placeholder_text="Tastiera, Chitarra, Microfono", width=200, height=30)
        self.subito_keyword.grid(row=1, column=0, padx=20)

        self.subito_category_label = ctk.CTkLabel(self.tabview.tab("Subito"), text="In quale categoria?", anchor="w", font=("Calibri",17))
        self.subito_category_label.grid(row=0, column=1, padx=20, pady=(10, 0))
        self.subito_category = ctk.CTkComboBox(self.tabview.tab("Subito"), values=list(S_CATEGORIE.keys()))
        self.subito_category.grid(row=1, column=1, padx=20)
        self.subito_category.bind('<KeyRelease>', self.autocomplete)

        self.subito_region_label = ctk.CTkLabel(self.tabview.tab("Subito"), text="Dove?", anchor="w", font=("Calibri",17))
        self.subito_region_label.grid(row=0, column=2, padx=20, pady=(10, 0))
        self.subito_region = ctk.CTkOptionMenu(self.tabview.tab("Subito"), dynamic_resizing=True,
                                                 values=list(S_REGIONI.keys()))
        self.subito_region.grid(row=1, column=2, padx=20)

        self.subito_shipping_label = ctk.CTkLabel(self.tabview.tab("Subito"), text="Spedizione", anchor="w", font=("Calibri",17))
        self.subito_shipping_label.grid(row=3, column=0, padx=20, pady=(25, 0))
        self.subito_shipping = ctk.CTkSwitch(self.tabview.tab("Subito"), text="Solo annunci con \nspedizione disponibile")
        self.subito_shipping.grid(row=4, column=0, padx=20)

        self.subito_titlesearch_label = ctk.CTkLabel(self.tabview.tab("Subito"), text="Restringi ricerca", anchor="w", font=("Calibri",17))
        self.subito_titlesearch_label.grid(row=3, column=1, padx=20, pady=(25, 0))
        self.subito_titlesearch = ctk.CTkSwitch(self.tabview.tab("Subito"), text="Cerca solo nel titolo")
        self.subito_titlesearch.grid(row=4, column=1, padx=20)

        self.subito_type_label = ctk.CTkLabel(self.tabview.tab("Subito"), text="Tipo di annuncio", anchor="w", font=("Calibri",17))
        self.subito_type_label.grid(row=3, column=2, padx=20, pady=(25, 0))
        self.subito_type = ctk.CTkOptionMenu(self.tabview.tab("Subito"), dynamic_resizing=True,
                                             values=list(S_TYPE.keys()))
        self.subito_type.grid(row=4, column=2, padx=20)


        # self.optionmenu_1 = ctk.CTkOptionMenu(self.tabview.tab("CTkTabview"), dynamic_resizing=False,
        #                                                 values=["Value 1", "Value 2", "Value Long Long Long"])
        # self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        # self.combobox_1 = ctk.CTkComboBox(self.tabview.tab("CTkTabview"),
        #                                             values=["Value 1", "Value 2", "Value Long....."])
        # self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
        # self.string_input_button = ctk.CTkButton(self.tabview.tab("CTkTabview"), text="Open CTkInputDialog",
        #                                                    command=self.open_input_dialog_event)
        # self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))
        # self.label_tab_2 = ctk.CTkLabel(self.tabview.tab("Tab 2"), text="CTkLabel on Tab 2")
        # self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

        # create radiobutton frame
        # self.radiobutton_frame = ctk.CTkFrame(self)
        # self.radiobutton_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        # self.radio_var = tkinter.IntVar(value=0)
        # self.label_radio_group = ctk.CTkLabel(master=self.radiobutton_frame, text="CTkRadioButton Group:")
        # self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        # self.radio_button_1 = ctk.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=0)
        # self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        # self.radio_button_2 = ctk.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=1)
        # self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")
        # self.radio_button_3 = ctk.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=2)
        # self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")

        # create slider and progressbar frame
        self.slider_progressbar_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
        self.seg_button_1 = ctk.CTkSegmentedButton(self.slider_progressbar_frame)
        self.seg_button_1.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.progressbar_1 = ctk.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_1.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.progressbar_2 = ctk.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_2.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_1 = ctk.CTkSlider(self.slider_progressbar_frame, from_=0, to=1, number_of_steps=4)
        self.slider_1.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_2 = ctk.CTkSlider(self.slider_progressbar_frame, orientation="vertical")
        self.slider_2.grid(row=0, column=1, rowspan=5, padx=(10, 10), pady=(10, 10), sticky="ns")
        self.progressbar_3 = ctk.CTkProgressBar(self.slider_progressbar_frame, orientation="vertical")
        self.progressbar_3.grid(row=0, column=2, rowspan=5, padx=(10, 20), pady=(10, 10), sticky="ns")

        # create scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="CTkScrollableFrame")
        self.scrollable_frame.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches = []
        for i in range(100):
            switch = ctk.CTkSwitch(master=self.scrollable_frame, text=f"CTkSwitch {i}")
            switch.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.scrollable_frame_switches.append(switch)

        # create checkbox and switch frame
        self.checkbox_slider_frame = ctk.CTkFrame(self)
        self.checkbox_slider_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.checkbox_1 = ctk.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_2 = ctk.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_3 = ctk.CTkCheckBox(master=self.checkbox_slider_frame)
        self.checkbox_3.grid(row=3, column=0, pady=20, padx=20, sticky="n")

        # set default values
        self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
        self.checkbox_3.configure(state="disabled")
        self.checkbox_1.select()
        self.scrollable_frame_switches[0].select()
        self.scrollable_frame_switches[4].select()
        # self.radio_button_3.configure(state="disabled")
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        # self.optionmenu_1.set("CTkOptionmenu")
        # self.combobox_1.set("CTkComboBox")
        self.slider_1.configure(command=self.progressbar_2.set)
        self.slider_2.configure(command=self.progressbar_3.set)
        self.progressbar_1.configure(mode="indeterminnate")
        self.progressbar_1.start()
        # self.textbox.insert("0.0", "CTkTextbox\n\n" + "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.\n\n" * 20)
        self.seg_button_1.configure(values=["CTkSegmentedButton", "Value 2", "Value 3"])
        self.seg_button_1.set("Value 2")

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

    def autocomplete(self, event):
        typed_text = self.subito_category.get()  # Ottieni il testo digitato nel Combobox
        matching_options = [option for option in list(S_CATEGORIE.keys()) if typed_text.lower() in option.lower()]

        # Se ci sono corrispondenze, mostra l'autocompletamento
        if matching_options:
            self.subito_category['values'] = matching_options


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
    global richieste, s_requests, m_requests
    with open("richieste.json", "r") as f:
        richieste = json.load(f)
    # s_requests = richieste['subito']
    # m_requests = richieste['mercatino']


def save_requests():
    # richieste['subito'] = s_requests
    # richieste['mercatino'] = m_requests
    with open("richieste.json", "w") as f:
        json.dump(richieste, f, indent=4)


def delete_request(id):
    del richieste[id]


# def delete_m_request(id):
#     for req in m_requests:
#         if req.get('id') == id:
#             m_requests.remove(req)
#             break 

def add_request(params, website):
    if richieste:
        id = max(richieste.keys()) + 1
    else:
        id = 0
    new_req = True
    for req in richieste:
        if req['params'] == params and req['website'] == website:
            new_req = False
    if new_req:
        richieste[id] = {'params': params, 'website': website, 'active': True}


def toggle_request_track(id):
    richieste[id]['active'] = not richieste[id]['active']


if __name__ == "__main__":
    load_mappings()
    app = App()
    app.mainloop()