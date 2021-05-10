from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDFlatButton, MDFillRoundFlatIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, TwoLineAvatarIconListItem, ImageLeftWidget, IconRightWidget
from kivymd.uix.menu import MDDropdownMenu
from modules.database import *
import datetime


class OsobaContent(BoxLayout):
    def __init__(self, id, *args, **kwargs):
        super().__init__(**kwargs)

        if id:
            person = vars(app.seznam.database.read_by_id(id))
        else:
            person = {"id":"", "jmeno":"", "vakciny_id":"Vyber vakcínu", "povolani_id":"Vyber povolání", "pocet_davek_aktualne":"0"}

        self.ids.person_name.text = person['jmeno']
        self.ids.pocet_davek_aktualne.text = str(person['pocet_davek_aktualne'])


        vakciny = app.seznam.database.read_vakciny()
        menu_items = [{"viewclass": "OneLineListItem", "text": f"{vakcina.nazev_firmy}", "on_release": lambda x=f"{vakcina.id}": self.set_item(x)} for vakcina in vakciny]
        self.menu_vakciny = MDDropdownMenu(
            caller=self.ids.vakcina,
            items=menu_items,
            position="center",
            width_mult=5,
        )
        self.ids.vakcina.set_item(str(person['vakciny_id']))


        spovolani = app.seznam.database.read_povolani()
        menu_items2 = [{"viewclass": "OneLineListItem", "text": f"{povolani.nazev_povolani}", "on_release": lambda x=f"{povolani.id}": self.set_item2(x)} for povolani in spovolani]
        self.menu_povolani = MDDropdownMenu(
            caller=self.ids.povolani,
            items=menu_items2,
            position="center",
            width_mult=5,
        )

        self.ids.povolani.set_item(str(person['povolani_id']))


    def set_item(self, text_item):
        self.ids.vakcina.set_item(text_item)
        self.ids.vakcina.text = text_item
        self.menu_vakciny.dismiss()

    def set_item2(self, text_item):
        self.ids.povolani.set_item(text_item)
        self.ids.povolani.text = text_item
        self.menu_povolani.dismiss()


class PersonDialog(MDDialog):
    def __init__(self, id, *args, **kwargs):
        super(PersonDialog, self).__init__(
            type="custom",
            content_cls=OsobaContent(id=id),
            title='Záznam osoby',
            size_hint=(.8, 1),
            buttons=[
                MDFlatButton(text='Uložit', on_release=self.save_dialog),
                MDFlatButton(text='Zrušit', on_release=self.cancel_dialog)
            ]
        )
        self.id = id

    def save_dialog(self, *args):
        person = {}
        person['jmeno'] = self.content_cls.ids.person_name.text
        person['vakciny_id'] = self.content_cls.ids.vakcina.text
        person['povolani_id'] = self.content_cls.ids.povolani.text
        person['pocet_davek_aktualne'] = self.content_cls.ids.pocet_davek_aktualne.text

        if self.id:
            person["id"] = self.id
            self.database = Database(dbtype='sqlite', dbname='ockovani.db')
            app.seznam.update(person)


        else:
            osoba = Ockovani()
            osoba.jmeno = person['jmeno']
            osoba.vakciny_id = person['vakciny_id']
            osoba.povolani_id = person['povolani_id']
            osoba.pocet_davek_aktualne = person['pocet_davek_aktualne']
            db = Database(dbtype='sqlite', dbname='ockovani.db')
            db.create_ockovani(osoba)

        app.seznam.rewrite_list()
        self.dismiss()

    def cancel_dialog(self, *args):
        self.dismiss()


class PridaniVakciny(BoxLayout):
    pass

class VakcinaDialog(MDDialog):
    def __init__(self, id, *args, **kwargs):
        super(VakcinaDialog, self).__init__(
            type="custom",
            content_cls=PridaniVakciny(),
            title='Záznam vakcíny',
            size_hint=(.8, 1),
            buttons=[
                MDFlatButton(text='Uložit', on_release=self.save_dialog),
                MDFlatButton(text='Zrušit', on_release=self.cancel_dialog)
            ]
        )
        self.id = id

    def save_dialog(self, *args):
        vakcina = Vakcina()
        vakcina.nazev_firmy = self.content_cls.ids.pridani_vakciny.text
        vakcina.pocet_davek = self.content_cls.ids.pridani_vakciny_davky.text
        self.database = Database(dbtype='sqlite', dbname='ockovani.db')
        self.database.create_vakcina(vakcina)

        app.seznam.rewrite_list()
        self.dismiss()

    def cancel_dialog(self, *args):
        self.dismiss()


class PridaniPovolani(BoxLayout):
    pass

class PovolaniDialog(MDDialog):
    def __init__(self, id, *args, **kwargs):
        super(PovolaniDialog, self).__init__(
            type="custom",
            content_cls=PridaniPovolani(),
            title='Záznam povolání',
            size_hint=(.8, 1),
            buttons=[
                MDFlatButton(text='Uložit', on_release=self.save_dialog),
                MDFlatButton(text='Zrušit', on_release=self.cancel_dialog)
            ]
        )
        self.id = id

    def save_dialog(self, *args):
        self.db = Database(dbtype='sqlite', dbname='ockovani.db')
        povolani = Povolani()
        povolani.nazev_povolani = self.content_cls.ids.pridani_povolani.text
        self.db.create_povolani(povolani)

        app.seznam.rewrite_list()
        self.dismiss()

    def cancel_dialog(self, *args):
        self.dismiss()

class MyItem(TwoLineAvatarIconListItem):
    def __init__(self, item, *args, **kwargs):
        super(MyItem, self).__init__()
        self.id = item['id']
        self.database = Database(dbtype='sqlite', dbname='ockovani.db')
        self.text = f"{item['jmeno']} ({self.database.read_povolani_id(item['povolani_id']).nazev_povolani})"
        self.secondary_text = f"{self.database.read_vakciny_id(item['vakciny_id']).nazev_firmy}, počet dávek aktuálně: {item['pocet_davek_aktualne']}/{self.database.read_vakciny_id(item['vakciny_id']).pocet_davek}"
        self.icon = IconRightWidget(icon="delete", on_release=self.on_delete)
        self.add_widget(self.icon)

    def on_press(self):
        self.dialog = PersonDialog(id=self.id)
        self.dialog.open()

    def on_delete(self, *args):
        yes_button = MDFlatButton(text='Ano', on_release=self.yes_button_release)
        no_button = MDFlatButton(text='Ne', on_release=self.no_button_release)
        self.dialog_confirm = MDDialog(type="confirmation", title='Smazání záznamu', text="Chcete opravdu smazat tento záznam?", buttons=[yes_button, no_button])
        self.dialog_confirm.open()

    def yes_button_release(self, *args):
        app.seznam.delete(self.id)
        self.dialog_confirm.dismiss()

    def no_button_release(self, *args):
        self.dialog_confirm.dismiss()


class Seznam(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(Seznam, self).__init__(orientation="vertical")
        global app
        app = App.get_running_app()
        scrollview = ScrollView()
        self.list = MDList()
        self.database = Database(dbtype='sqlite', dbname='ockovani.db')
        self.rewrite_list()
        scrollview.add_widget(self.list)
        self.add_widget(scrollview)
        button_box = BoxLayout(orientation='horizontal', size_hint_y=0.1)

        new_osoba_btn = MDFillRoundFlatIconButton()
        new_osoba_btn.text = "Nová osoba"
        new_osoba_btn.icon = "plus"
        new_osoba_btn.icon_color = [0.9, 0.9, 0.9, 1]
        new_osoba_btn.text_color = [0.9, 0.9, 0.9, 1]
        new_osoba_btn.md_bg_color = [0.0235294117647059, 0.7607843137254902, 0.3450980392156863, 1]
        new_osoba_btn.font_style = "Button"
        new_osoba_btn.pos_hint = {"center_x": .5}
        new_osoba_btn.pos_hint = {"center_y": .5}
        new_osoba_btn.on_release = self.on_create_osoba
        button_box.add_widget(new_osoba_btn)

        new_vakcina_btn = MDFillRoundFlatIconButton()
        new_vakcina_btn.text = "Nová vakcína"
        new_vakcina_btn.icon = "plus"
        new_vakcina_btn.icon_color = [0.9, 0.9, 0.9, 1]
        new_vakcina_btn.text_color = [1, 0.9, 0.9, 1]
        new_vakcina_btn.md_bg_color = [0.0235294117647059, 0.7607843137254902, 0.3450980392156863, 1]
        new_vakcina_btn.font_style = "Button"
        new_vakcina_btn.pos_hint = {"center_x": .7}
        new_vakcina_btn.pos_hint = {"center_y": .5}
        new_vakcina_btn.on_release = self.on_create_vakcina
        button_box.add_widget(new_vakcina_btn)

        new_povolani_btn = MDFillRoundFlatIconButton()
        new_povolani_btn.text = "Nové povolání"
        new_povolani_btn.icon = "plus"
        new_povolani_btn.icon_color = [0.9, 0.9, 0.9, 1]
        new_povolani_btn.text_color = [0.9, 0.9, 0.9, 1]
        new_povolani_btn.md_bg_color = [0.0235294117647059, 0.7607843137254902, 0.3450980392156863, 1]
        new_povolani_btn.font_style = "Button"
        new_povolani_btn.pos_hint = {"center_x": .9}
        new_povolani_btn.pos_hint = {"center_y": .5}
        new_povolani_btn.on_release = self.on_create_povolani
        button_box.add_widget(new_povolani_btn)

        self.add_widget(button_box)


    def rewrite_list(self):
        self.list.clear_widgets()
        seznam = self.database.read_all()

        for osoba in seznam:
            self.list.add_widget(MyItem(item=vars(osoba)))


    def on_create_osoba(self, *args):
        self.dialog = PersonDialog(id=None)
        self.dialog.open()


    def on_create_vakcina(self, *args):
        self.dialog = VakcinaDialog(id=None)
        self.dialog.open()

    def on_create_povolani(self, *args):
        self.dialog = PovolaniDialog(id=None)
        self.dialog.open()

    def update(self, person):
        update_person = self.database.read_by_id(person['id'])
        update_person.jmeno = person['jmeno']
        update_person.vakciny_id = person['vakciny_id']
        update_person.povolani_id = person['povolani_id']
        update_person.pocet_davek_aktualne = person['pocet_davek_aktualne']
        self.database.update()
        self.rewrite_list()

    def delete(self, id):
        self.database.delete(id)
        self.rewrite_list()