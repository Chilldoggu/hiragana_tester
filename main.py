# from kivy.uix.boxlayout import BoxLayout

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup

from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.core.window import Window

from pathlib import Path
from random import choice

Window.clearcolor = (0.3, 0.3, 1, 1)


class Tester(Screen):
    currImg = ObjectProperty(None)
    myTextInput = ObjectProperty(None)
    myLabel = ObjectProperty(None)
    checkLabel = ObjectProperty(None)
    # Path is being initialized in ChooseFile.load()
    path = ObjectProperty(None)

    def __init__(self, **kwargs):
        self.clear_widgets()
        super(Tester, self).__init__(**kwargs)

    def screenSwipe(self):
        print(self.path)
        self.images = [
            p.name for p in self.path.glob("*.png")
        ]
        Clock.schedule_once(lambda dt: self.set_img())

    def set_img(self):
        if not len(self.images):
            self.__init__()
            self.screenSwipe()
        self.rngImage = choice(self.images)
        self.currImg.source = str(self.path.joinpath(self.rngImage))
        self.myLabel.text = "hiraganas left: " + str(len(self.images))

    def clear_handler(self):
        self.checkLabel.text = ''
        self.set_img()

    def check_hiragana(self, input):
        self.myTextInput.text = ''
        if input == self.rngImage[:-4] and self.rngImage in self.images:
            self.images.remove(self.rngImage)
            self.myLabel.text = "hiraganas left: " + str(len(self.images))
            self.checkLabel.color = [0, 1, 0, 1]
            self.checkLabel.text = 'Good!'
            Clock.schedule_once(lambda dt: self.clear_handler(), .5)
        else:
            self.checkLabel.color = [1, 0, 0, 1]
            self.checkLabel.text = f'Bad!\nCorrect romaji: {self.rngImage[:-4]}'
            Clock.schedule_once(lambda dt: self.clear_handler(), 3)


class LoadFile(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class ChooseFile(Screen):
    def show_load(self):
        content = LoadFile(cancel=self.dismiss_popup, load=self.load)
        self._popup = Popup(title="Load Folder", content=content, size_hint=(.9, .9))
        self._popup.open()

    def dismiss_popup(self):
        self._popup.dismiss()

    def load(self, selection):
        self._popup.dismiss()
        selectedPath = Path(selection[0])
        tester = self.manager.get_screen('MainTester')
        tester.path = selectedPath
        self.manager.current = 'MainTester'


class JapaneseManager(ScreenManager):
    ...


class HiraganaApp(App):
    def build(self):
        japaneseApp = JapaneseManager()
        return japaneseApp


if __name__ == "__main__":
    app = HiraganaApp()
    app.run()
