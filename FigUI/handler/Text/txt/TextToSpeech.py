import pyttsx3
import platform
import webbrowser

class SpeechEngine:
    def __init__(self, use_torch=False, lang='en'):
        os_name = platform.system()
        self.lang = lang
        self.device = "cpu"
        self.os_name = os_name
        self.speaker = 'lj_16khz'
        
        if os_name == "Darwin":
            self.engine = pyttsx3.init(driverName='nsss')
        elif os_name == "Windows":
            self.engine = pyttsx3.init(driverName='sapi5')
        elif os_name == "Linux":
            self.engine = pyttsx3.init()

        self.use_torch = use_torch
        if use_torch:
            try:
                import torch
            except ImportError:
                print("You need to install torch & torchaudio.")
                webbrowser.open("https://pytorch.org/hub/snakers4_silero-models_tts/")
            else:
                self.device = torch.device(device)
                model, symbols, sample_rate, example_text, apply_tts = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                                                                      model='silero_tts',
                                                                                      language=lang,
                                                                                      speaker=self.speaker)
                model.to(self.device)
                self.model = model
                self.symbols = symbols
                self.apply_tts = apply_tts
                self.sample_rate = sample_rate

    def getAudio(self, text):
        if use_torch:
            audio = self.apply_tts(texts=[text],
                                   model=self.model,
                                   sample_rate=self.sample_rate,
                                   symbols=self.symbols,
                                   device=self.device)
        else:
            pass

if __name__ == "__main__":
    import torch

    language = 'en'
    speaker = 'lj_16khz'
    device = torch.device('cpu')
    model, symbols, sample_rate, example_text, apply_tts = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                                                        model='silero_tts',
                                                                        language=language,
                                                                        speaker=speaker)
    model = model.to(device)  # gpu or cpu
    audio = apply_tts(texts=[example_text],
                    model=model,
                    sample_rate=sample_rate,
                    symbols=symbols,
                    device=device)

