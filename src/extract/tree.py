import functools

from treelib import Tree

from extract.utils import section_names


class MetadataTree(Tree):
    def __init__(self, metadata):
        self.tree = Tree()
        self.create_node("root", "root")
        for header in section_names(metadata):
            self.__build_tree(header, metadata[header], "root")

    # breaks with typechecking
    def __getattr__(self, attr):
        return getattr(self.tree, attr)

    def __build_tree(self, header, data, parent):
        images = data["images"] if "images" in data else []
        self.create_node(header, header, data=images, parent=parent)
        for key in section_names(data):
            self.__build_tree(key, data[key], header)

    def get_keyword_images(self, header):
        leaves = self.leaves(header)
        return list(set(functools.reduce(lambda a, b: a + b.data, leaves, [])))

    def to_dict(self, nid=None):
        """Transform the whole tree into a dict."""

        nid = self.root if (nid is None) else nid
        ntag = self[nid].tag
        tree_dict = {"name": ntag, "children": []}

        if self[nid].expanded:
            queue = self.children(nid)

            for elem in queue:
                tree_dict["children"].append(self.to_dict(elem.identifier))

            return tree_dict
