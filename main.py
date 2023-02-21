import easyocr
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.toast import toast
from kivymd.uix.filemanager import MDFileManager



class MainWindow(Screen):
    pass


class CamWindow(Screen):
    def on_enter(self):
        self.ids.camera.play = True

    def capture(self):
        camera = self.ids['camera']
        global image
        image = "img.png"
        camera.export_to_png(image)
        self.manager.current ='conf_w'



class UploadWindow(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.manager_open = False
        self.file_manager = MDFileManager(exit_manager=self.exit_manager,
                                          select_path=self.select_path,
                                          preview=True,
                                          ext=[".png", ".jpg", ".jpeg"])

    def file_manager_open(self):
        self.file_manager.show("/")  # output manager to the screen
        self.manager_open = True

    def select_path(self, path):
        global image
        image = path
        if image.endswith(('.png', '.jpg', '.jpeg'))==True:
            self.exit_manager()
            self.manager.current ='conf_w'
        else:
            pass
            

    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()



class ConfirmImage(Screen):
    def on_enter(self):
        print(image)
        self.ids.img.source=image


class TextDetection(Screen):
    def on_enter(self):
        lang=['en']
        print(image)
        path=image.replace("\\","/")
        print(path)
        reader = easyocr.Reader(lang)
        result = reader.readtext(path)
        final_text=''

        for detection in result:
            final_text += detection[1]+ '\n'
        
        self.ids.textresult.text=final_text
    pass


class WindowManager(ScreenManager):
    pass


Builder.load_file('main.kv')


class MainApp(MDApp):

    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainWindow(name='main_w'))
        sm.add_widget(CamWindow(name='cam_w'))
        sm.add_widget(UploadWindow(name='upload_w'))
        sm.add_widget(ConfirmImage(name='conf_w'))
        sm.add_widget(TextDetection(name='det_w'))

        return sm


if __name__ == "__main__":
    MainApp().run()




