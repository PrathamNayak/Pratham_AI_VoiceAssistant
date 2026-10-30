from dotenv import load_dotenv
load_dotenv()
from kivy import app,clock
from prathamai import Prathamai

class PrathamAiVoiceAssistant(app.App):
    def build(self):
        prathamai=Prathamai()
        prathamai.start_listening()

        self.update_event=clock.Clock.schedule_interval(prathamai.update_circle,1/60)
        self.btn_rotation_event=clock.Clock.schedule_interval(prathamai.circle.rotate_button,1/60)

        return prathamai

if __name__=='__main__':    
    PrathamAiVoiceAssistant=PrathamAiVoiceAssistant()
    PrathamAiVoiceAssistant.run()