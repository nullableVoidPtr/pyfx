from loguru import logger
from pyfx.error import PyfxException

from pyfx.view.json_lib.array.array_node import ArrayNodeCreator
from pyfx.view.json_lib.object.object_node import ObjectNodeCreator
from pyfx.view.json_lib.primitive import StringNode
from pyfx.view.json_lib.primitive.boolean import BooleanNodeCreator
from pyfx.view.json_lib.primitive.integer import IntegerNodeCreator
from pyfx.view.json_lib.primitive.null import NullNodeCreator
from pyfx.view.json_lib.primitive.numeric import NumericNodeCreator
from pyfx.view.json_lib.primitive.string import StringNodeCreator


class JSONNodeFactory:
    """
    Factory to create
    :py:class:`pyfx.view.json_lib.json_simple_node.JSONSimpleNode`.
    """

    def __init__(self):
        # The order in the list is important, it determines the order of
        # precedence for types.
        # default creator order:
        #    null -> bool -> integer -> numeric -> string -> object -> array
        self._default_node_creators = [
            NullNodeCreator(), BooleanNodeCreator(), IntegerNodeCreator(),
            NumericNodeCreator(), StringNodeCreator(), ObjectNodeCreator(self),
            ArrayNodeCreator(self)]
        self._node_creators = self._default_node_creators

    def register(self, node_creator):
        """
        Register an implementation of `JSONNodeCreator` to create a node for
        certain value.

        `node_creator`: An implementation of `JSONNodeCreator`.
        """
        logger.info(f"Register {node_creator} in JSON node factory")
        # prioritize node_creator over default_node_creator
        node_creators = list()
        node_creators.append(node_creator)
        node_creators.extend(self._node_creators)
        self._node_creators = node_creators

    def create_root_node(self, value):
        """
        Create a root node.
        """
        return self.create_node("", value, display_key=False)

    def create_node(self, key, value, **kwargs):
        """
        Create the real `JSONSimpleNode` implementation based on the value.
        """
        # noinspection PyBroadException
        try:
            for node_creator in self._node_creators:
                node = node_creator.create_node(key, value, **kwargs)
                if node is not None:
                    return node
            # No JSONSimpleNode implementation has been found based on the type
            # of value
            raise PyfxException("Failed to find JSONSimpleNode implementation "
                                f"for {value}.")
        except Exception as e:
            # As a final resort, use StringNode to serialize the value.
            logger.opt(exception=e) \
                .warning(f"NodeFactory Error: {e}. Use StringNode by default.")
            return StringNode(key, value, **kwargs)
