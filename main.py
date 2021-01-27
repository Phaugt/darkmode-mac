import rumps, os, sys, subprocess
from os.path import expanduser
from easysettings import EasySettings

def resource_path(relative_path):
    """for pyinstaller/py2app"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)

dm_logo = resource_path('data/logo.png')
userfold = expanduser("~")
config = EasySettings(userfold+"/dm.conf")

try:
    firstrn = config.get("first_run")
    if firstrn == "":
        rumps.alert("Darkmode","App is loaded for the first time. You'll get promts for teminal and system access.",None,None,None,dm_logo)
        config.set("first_run", "No")
        config.save()
except Exception:
    rumps.notification("Darkmode","Error with Config file",sound=True,icon=dm_logo)

OSASCRIPT = """
tell application "System Events"
    tell appearance preferences
        set dark mode to {mode}
    end tell
end tell

tell application "Terminal"
    set default settings to settings set "{theme}"
end tell

tell application "Terminal"
    set current settings of tabs of windows to settings set "{theme}"
end tell
"""

TERMINAL_THEMES = {
    False: 'Rasta light',
    True: 'Rasta',
}


def is_dark_mode() -> bool:
    """Return the current Dark Mode status."""
    result = subprocess.run(
        ['defaults', 'read', '-g', 'AppleInterfaceStyle'],
        text=True,
        capture_output=True,
    )
    return result.returncode == 0 and result.stdout.strip() == 'Dark'


def set_interface_style(dark: bool):
    """Enable/disable dark mode."""
    mode = 'true' if dark else 'false'
    script = OSASCRIPT.format(mode=mode, theme=TERMINAL_THEMES[dark])
    result = subprocess.run(
        ['osascript', '-e', script],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result
        

class Darkmode(rumps.App):
    def __init__(self):
        super(Darkmode, self).__init__('darkmode')
        self.icon = dm_logo

    @rumps.clicked("Darkmode")
    def dmtoggle(self, sender):
        sender.state = not sender.state
        set_interface_style(not is_dark_mode())

    @rumps.clicked("About")
    def about(self, _):
        info = 'a small software that sets darkmode/lightmode on your mac \n https://github.com/Phaugt/darkmode-mac'
        rumps.alert("About Darkmode",info,icon_path=dm_logo)



if __name__ == "__main__":
    Darkmode().run()
