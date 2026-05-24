from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Header, Button, Static,TextArea,Input
from mclium.api.search.search_engine import SearchEngine
from mclium.manager.plugin_manager import PluginManager

from mclium.api.plugin import UiPlugin
class AutoCompleteWidget(Vertical):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.plugin_obj = PluginManager().get_plugins()
        self.trie = SearchEngine()
        for pl in self.plugin_obj:
            pl: UiPlugin
            pl_name: UiPlugin = pl.name
            if not pl_name.__str__().startswith("@"):
                pl_name = f"@{pl_name}"
            self.trie.insert(pl_name)

        # TODO: hoàn thành auto complete với ui sau khi done thằng loader + loader manager

    def update_suggestions(self, current_input: str) -> None:
        self.query("*").remove()

        if not current_input.strip():
            return

        matches = self.trie.search(current_input)
        if matches:
            for value in matches:
                self.mount(Static(f"[#66a1ff] {value} [/#66a1ff]"))
