from typing import Union

from overrides import overrides

from pyfx.view.json_lib.models import node_factory
from pyfx.view.json_lib.models.json_composite_node import JSONCompositeNode
from pyfx.view.json_lib.widgets.object_widget import ObjectWidget


class ObjectNode(JSONCompositeNode):
    """
    implementation of JSON `object` type node
    aside from fields in a JSONNode, it contains the following elements:
    * value: dict
    * children: dict to store correspondent node
    * sorted_children_key_list: internal type to keep track of a sorted key list and
                                thus keep track of the next, previous node of each child
    * sorted_children_key_list_size: size of key
    """

    def __init__(self,
                 key: str,
                 value: dict,
                 parent: Union["ObjectNode", "array_node", None] = None,
                 display_key: bool = True
                 ):
        super().__init__(key, value, parent, display_key)
        self._children = {}
        self._sorted_children_key_list = sorted(value.keys())
        # avoid re-calculation
        self._sorted_children_key_list_size = len(self._sorted_children_key_list)

    @overrides
    def has_children(self) -> bool:
        return self._sorted_children_key_list_size != 0

    def get_child_node(self, key):
        if not self.has_children():
            return None
        elif key not in self._children:
            self._children[key] = self.load_child_node(key)
        return self._children[key]

    def load_child_node(self, key):
        value = self.get_value()[key]
        return node_factory.NodeFactory.create_node(key, value, self, True)

    @overrides
    def get_first_child(self) -> Union["JSONSimpleNode", None]:
        if not self.has_children():
            return None
        return self.get_child_node(self._sorted_children_key_list[0])

    @overrides
    def get_last_child(self) -> Union["JSONSimpleNode", None]:
        if not self.has_children():
            return None
        return self.get_child_node(self._sorted_children_key_list[self._sorted_children_key_list_size - 1])

    def prev_child(self, key):
        index = self._sorted_children_key_list.index(key)
        if index == 0:
            return None
        return self.get_child_node(self._sorted_children_key_list[index - 1])

    def next_child(self, key):
        index = self._sorted_children_key_list.index(key)
        if index == self._sorted_children_key_list_size - 1:
            return None
        return self.get_child_node(self._sorted_children_key_list[index + 1])

    # =================================================================================== #
    # ui                                                                                  #
    # =================================================================================== #

    @overrides
    def load_widget(self):
        return ObjectWidget(self, self._display_key)