from mclium.api.search.entities.trie_node import TrieNode
class SearchEngine(object):
    def __init__(self):
        self.root = TrieNode()

    def insert(self,prefix):
        node = self.root
        for char in prefix:
            if char not in self.root.children:
                self.root.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def inserts(self,prefixes):
        node = self.root
        for prefix in prefixes:
            for char in prefix:
                if char not in self.root.children:
                    self.root.children[char] = TrieNode()
                node = node.children[char]
            node.is_end = True

    def _find_node(self,prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def _dfs(self,node,path,result):
        if node.is_end:
            result.append("".join(path))

        for char,child in node.children.items():
            path.append(char)
            self._dfs(child,path,result)
            path.pop()

    def search(self,prefix):
        node = self._find_node(prefix)
        if node is None:
            return None
        result = []
        self._dfs(node,list(prefix),result)
        return result
