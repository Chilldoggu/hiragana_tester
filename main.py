from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.core.window import Window

from pathlib import Path
from random import choice

Window.clearcolor = (0.3, 0.3, 1, 1)

Builder.load_string(
    """
<MyLayout>
    currImg: currImg
    myTextInput: myTextInput
    myLabel: myLabel
    orientation: 'vertical'
    Image:
        id: currImg
    BoxLayout:
        orientation: 'vertical'
        padding: [20, 40, 20, 40]
        spacing: 40
        TextInput:
            id: myTextInput
            multiline: False
            text_validate_unfocus: False
            on_text_validate: root.check_hiragana(self.text)
            font_size: self.height - 25
            halign: 'center'
        Label:
            id: myLabel
            font_size: 20
"""
)


class MyLayout(BoxLayout):
    currImg = ObjectProperty(None)
    myTextInput = ObjectProperty(None)
    myLabel = ObjectProperty(None)

    def __init__(self, **kwargs):
        self.clear_widgets()
        super(MyLayout, self).__init__(**kwargs)

        self.images = [
            p.name for p in Path.cwd().joinpath("img", "hiragana").glob("*.png")
        ]
        Clock.schedule_once(lambda dt: self.set_img())

    def set_img(self):
        if not len(self.images):
            self.__init__()
        self.rngImage = choice(self.images)
        self.currImg.source = str(Path().joinpath("img", "hiragana", self.rngImage))
        self.myLabel.text = "hiraganas left: " + str(len(self.images))

    def check_hiragana(self, input):
        if input == self.rngImage[:-4]:
            self.images.remove(self.rngImage)
            self.myLabel.text = "hiraganas left: " + str(len(self.images))
            self.myTextInput.text = ""
            self.set_img()


class HiraganaApp(App):
    def build(self):
        return MyLayout()


if __name__ == "__main__":
    app = HiraganaApp()
    app.run()
