import json

from textual.app import App, ComposeResult
from textual.widgets import Input, Static
from textual.containers import Vertical, Horizontal
from mclium.term_ui.widgets.auto_complete_widget import AutoCompleteWidget

from mclium.utils import Path


class TermUi(App):

    main_style_path = Path.join_path("setting","term_style","main_ui.css")

    with open(main_style_path, 'r') as f:
        style = f.read()
    print(style)

    CSS = style

    def __init__(self):
        super().__init__()

        #metadata
        mclium_current_path = Path.join_path("setting","mclium-current.json")
        with open(mclium_current_path, 'r') as f:
            self.mclium_current_data = json.load(f)

    def compose(self) -> ComposeResult:
        with Vertical(id="box"):
            yield Static("[#616161]███╗   ███╗ ██████╗██╗     ██╗██╗   ██╗███╗   ███╗[/#616161]")
            yield Static("[#616161]████╗ ████║██╔════╝██║     ██║██║   ██║████╗ ████║[/#616161]")
            yield Static("[#616161]██╔████╔██║██║     ██║     ██║██║   ██║██╔████╔██║[/#616161]")
            yield Static("[#616161]██║╚██╔╝██║██║     ██║     ██║██║   ██║██║╚██╔╝██║[/#616161]")
            yield Static("[#616161]██║ ╚═╝ ██║╚██████╗███████╗██║╚██████╔╝██║ ╚═╝ ██║[/#616161]")
            yield Static("\n")
            yield Static(f"[#66a1ff]•[/#66a1ff] [#ff6666]McLium[/#ff6666]  - {self.mclium_current_data.get("version","unknown")}")
            yield Static("[#66a1ff]•[/#66a1ff] Join discord: [#4f8dff]https://dsc.gg/McLium[/#4f8dff]")
            yield Static("\n")
            yield Static("[#ff6666]-[/#ff6666] Help")
            yield Static("[#66a1ff]•[/#66a1ff] For download a plugin using: @clone + url")
            yield Static("[#403f3f]> Example: @clone https://github.com/notkenftr/port-scan[/#403f3f]")
            yield Static("[#66a1ff]•[/#66a1ff] To use the plugin, type @ + plugin name and press enter.")
            yield Static("[#403f3f]> Example: @get-server-info")
            yield Static("[#66a1ff]•[/#66a1ff] To exit, press Ctrl + Q.")
            yield Static("\n")
            yield AutoCompleteWidget(id="auto_complete_box")
            with Vertical(classes="input-area"):
                yield Static("[#a9fa8c]ϟ[/#a9fa8c] Loaded [#fc5672]1[/#fc5672] plugins")
                yield Input(placeholder='> Select plugin "@". Example: @get-server-info')

    def on_input_changed(self, event: Input.Changed) -> None:
        try:
            auto_box = self.query_one("#auto_complete_box")
            auto_box.update_suggestions(event.value)
        except Exception:
            pass
#test
if __name__ == '__main__':
    TermUi().run()
