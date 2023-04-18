"""
Wrapper over treelib.Tree that outputs a normalized dictionary with to_dict
and has some utility functions.
"""
import functools
from typing import Any, Dict
from typeguard import typechecked

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

    @typechecked
    def __build_tree(self, header: str, data: Dict[str, Any], parent: str):
        """
        Recursively builds the tree from a metadata dictionary.

        :param header: The name of the section to add.
        :param data: The object associated with the section
        (i.e., its children and images)
        :param parent: The parent of the node that will be inserted
        into the tree.
        """
        images = data["images"] if "images" in data else []

        # will raise duplicate node error
        self.create_node(header, header, data=images, parent=parent)
        for key in section_names(data):
            self.__build_tree(key, data[key], header)

    @typechecked
    def get_keyword_images(self, header: str):
        """
        Gets the images for a keyword from its children.

        :param header: The name of the keyword.
        """
        leaves = self.leaves(header)
        return list(set(functools.reduce(lambda a, b: a + b.data, leaves, [])))

    @typechecked
    def to_dict(self, nid=None) -> Dict[str, Any]:
        """
        Transforms the whole tree into a normalized dict.

        :param nid: Optional, the node to use as root for the dict.
        :returns: A normalized nested dictionary of {name, children}.
        """

        nid = self.root if (nid is None) else nid
        ntag = self[nid].tag
        tree_dict = {"name": ntag, "children": []}

        if self[nid].expanded:
            queue = self.children(nid)

            for elem in queue:
                tree_dict["children"].append(self.to_dict(elem.identifier))

        return tree_dict
