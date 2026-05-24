import json

from textual.app import App, ComposeResult
from textual.widgets import Input, Static
from textual.containers import Vertical, Horizontal

from mclium.api.plugin import UiPlugin
from mclium.term_ui.widgets.auto_complete_widget import AutoCompleteWidget
from mclium.manager.plugin_manager import PluginManager
from mclium.utils import Path


class TermUi(App):

    main_style_path = Path.join_path("setting","term_style","main_ui.css")

    with open(main_style_path, 'r') as f:
        style = f.read()
    CSS = style

    def __init__(self):
        super().__init__()

        self.plugins = PluginManager().get_plugins()
        self.plugin_name_and_callback = {}
        for plugin in self.plugins:
            plugin: UiPlugin
            if str(plugin.name).startswith("@"):
                if plugin.name not in self.plugin_name_and_callback:
                    self.plugin_name_and_callback[str(plugin.name).replace("@","")] = plugin.callback
            else:
                continue
        #metadata
        mclium_current_path = Path.join_path("setting","mclium-current.json")
        with open(mclium_current_path, 'r') as f:
            self.mclium_current_data = json.load(f)

    def compose(self) -> ComposeResult:
        lines = [
            "[#616161]███╗   ███╗ ██████╗██╗     ██╗██╗   ██╗███╗   ███╗[/#616161]",
            "[#616161]████╗ ████║██╔════╝██║     ██║██║   ██║████╗ ████║[/#616161]",
            "[#616161]██╔████╔██║██║     ██║     ██║██║   ██║██╔████╔██║[/#616161]",
            "[#616161]██║╚██╔╝██║██║     ██║     ██║██║   ██║██║╚██╔╝██║[/#616161]",
            "[#616161]██║ ╚═╝ ██║╚██████╗███████╗██║╚██████╔╝██║ ╚═╝ ██║[/#616161]",
            "",
            f"[#66a1ff]•[/#66a1ff] [#ff6666]McLium[/#ff6666] - {self.mclium_current_data.get('version', 'unknown')}",
            "[#66a1ff]•[/#66a1ff] Join discord: [#4f8dff]https://dsc.gg/McLium[/#4f8dff]",
            "",
            "[#ff6666]-[/#ff6666] Help",
            "[#66a1ff]•[/#66a1ff] For download a plugin using: @clone + url",
            "[#403f3f]> Example: @clone https://github.com/notkenftr/port-scan[/#403f3f]",
            "[#66a1ff]•[/#66a1ff] To use the plugin, type @ + plugin name and press enter.",
            "[#403f3f]> Example: @get-server-info",
            "[#66a1ff]•[/#66a1ff] To exit, press Ctrl + Q.",
            "",
        ]

        with Vertical(id="box"):
            for line in lines:
                yield Static(line)

            yield AutoCompleteWidget(id="auto_complete_box")

            with Vertical(classes="input-area"):
                yield Static(
                    f"[#a9fa8c]ϟ[/#a9fa8c] Loaded [#fc5672]{len(self.plugins)}[/#fc5672] plugins"
                )
                yield Input(
                    placeholder='> Select plugin "@". Example: @get-server-info'
                )
    def on_input_changed(self, event: Input.Changed) -> None:
        try:
            auto_box = self.query_one("#auto_complete_box")
            auto_box.update_suggestions(event.value)
        except Exception:
            pass

    def plugin_handler(self,value):
        if value.replace("@","") in self.plugin_name_and_callback:
            callback = self.plugin_name_and_callback[value.replace("@","")]
            callback()

    def on_input_submitted(self, event: Input.Submitted):
        value = event.value

        if value.lower().startswith("@"):
            self.plugin_handler(value)




#test
if __name__ == '__main__':
    TermUi().run()
