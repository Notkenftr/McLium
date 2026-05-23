from textual.app import App, ComposeResult
from textual.widgets import Input, Static
from textual.containers import Vertical, Horizontal


from mclium.utils import Path


class TermUi(App):
    def __init__(self):
        self.main_ui_path = Path.join_path("setting","term_style","main_ui.css")
        self.css_path = self.main_ui_path

    def compose(self) -> ComposeResult:
        with Vertical(id="box"):
            yield Static("[#616161]███╗   ███╗ ██████╗██╗     ██╗██╗   ██╗███╗   ███╗[/#616161]")
            yield Static("[#616161]████╗ ████║██╔════╝██║     ██║██║   ██║████╗ ████║[/#616161]")
            yield Static("[#616161]██╔████╔██║██║     ██║     ██║██║   ██║██╔████╔██║[/#616161]")
            yield Static("[#616161]██║╚██╔╝██║██║     ██║     ██║██║   ██║██║╚██╔╝██║[/#616161]")
            yield Static("[#616161]██║ ╚═╝ ██║╚██████╗███████╗██║╚██████╔╝██║ ╚═╝ ██║[/#616161]")
            yield Static("\n")
            yield Static("[#66a1ff]•[/#66a1ff] [#ff6666]McLium[/#ff6666]  - 1.1.0")
            yield Static("[#66a1ff]•[/#66a1ff] Join discord: [#4f8dff]https://dsc.gg/McLium[/#4f8dff]")
            yield Static("\n")
            yield Static("[#ff6666]-[/#ff6666] Help")
            yield Static("[#66a1ff]•[/#66a1ff] For download a plugin using: @clone + url")
            yield Static("[#403f3f]> Example: @clone https://github.com/notkenftr/port-scan[/#403f3f]")
            yield Static("[#66a1ff]•[/#66a1ff] To use the plugin, type @ + plugin name and press enter.")
            yield Static("[#403f3f]> Example: @get-server-info")
            yield Static("[#66a1ff]•[/#66a1ff] To exit, press Ctrl + Q.")
            yield Static("\n")
            yield AutoComplete(id="auto_complete_box")
            with Vertical(classes="input-area"):
                yield Static("[#a9fa8c]ϟ[/#a9fa8c] Loaded [#fc5672]1[/#fc5672] plugins")
                yield Input(placeholder='> Select plugin "@". Example: @get-server-info')
