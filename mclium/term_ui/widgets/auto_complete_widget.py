from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Header, Button, Static,TextArea,Input
from mclium.api.search.search_engine import SearchEngine

class AutoCompleteWidget(Vertical):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.plugin_names = [
            "@clone",
            "@get-server-info",
            "@port-scan"
        ]
        self.trie = SearchEngine()
        for name in self.plugin_names:
            self.trie.insert(name)

        # TODO: hoàn thành auto complete với ui sau khi done thằng loader + loader manager

    def update_suggestions(self, current_input: str) -> None:
        self.query("*").remove()

        if not current_input.strip():
            return

        matches = self.trie.search(current_input)
        if matches:
            for value in matches:
                self.mount(Static(f"[#66a1ff] {value} [/#66a1ff]"))
