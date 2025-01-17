import unittest

from urwid.compat import B

from pyfx.view.json_lib.json_node_factory import JSONNodeFactory


class ArrayNodeTest(unittest.TestCase):
    """
    unit tests for :py:class:`pyfx.view.json_lib.array.array_node.ArrayNode`
    """

    def setUp(self):
        self._node_factory = JSONNodeFactory()

    def test_empty_list(self):
        """ test rendering of an empty JSON object"""
        data = []

        # act
        node = self._node_factory.create_root_node(data)
        widget = node.get_widget()

        contents = []
        while widget is not None:
            node = widget.get_node()
            if not node.is_expanded():
                node.toggle_expanded()
            widget = node.get_widget()
            contents.append(widget.render((18,)).content())
            widget = widget.next_inorder()

        # restart and scan from the end
        node = self._node_factory.create_root_node(data)
        widget = node.get_end_node().get_widget()
        contents_from_end = []
        while widget is not None:
            contents_from_end.append(widget.render((18,)).content())
            widget = widget.prev_inorder()

        texts = [[[t[2] for t in row] for row in content]
                 for content in contents]
        texts_from_end = [[[t[2] for t in row]
                           for row in content] for content in contents_from_end]
        texts_from_end.reverse()

        # verify
        self.assertEqual(2, len(texts))
        expected = [
            [[B("[                 ")]],
            [[B("]                 ")]],
        ]
        self.assertEqual(expected, texts)
        self.assertEqual(expected, texts_from_end)

    def test_simple_array(self):
        """
        test rendering a not-nested array
        """

        data = [
            1,
            2,
            "str"
        ]

        # act
        node = self._node_factory.create_root_node(data)
        widget = node.get_widget()

        contents = []
        while widget is not None:
            node = widget.get_node()
            if not node.is_expanded():
                node.toggle_expanded()
            widget = node.get_widget()
            contents.append(widget.render((18,)).content())
            widget = widget.next_inorder()

        texts = [[[t[2] for t in row] for row in content]
                 for content in contents]

        # verify
        self.assertEqual(5, len(texts))
        expected = [
            [[B("[                 ")]],
            [[B("   "), B('1'), B('              ')]],
            [[B("   "), B('2'), B('              ')]],
            [[B("   "), B('"str"'), B('          ')]],
            [[B("]                 ")]]
        ]
        self.assertEqual(expected, texts)

    def test_nested_array(self):
        """
        test rendering a nested array
        """

        data = [
            1,
            2,
            [
                "str",
                True
            ]
        ]

        # act
        node = self._node_factory.create_root_node(data)
        widget = node.get_widget()

        contents = []
        while widget is not None:
            node = widget.get_node()
            if not node.is_expanded():
                node.toggle_expanded()
            widget = node.get_widget()
            contents.append(widget.render((18,)).content())
            widget = widget.next_inorder()

        texts = [[[t[2] for t in row] for row in content]
                 for content in contents]

        # verify
        self.assertEqual(8, len(texts))
        expected = [
            [[B("[                 ")]],
            [[B("   "), B('1'), B('              ')]],
            [[B("   "), B('2'), B('              ')]],
            [[B("   "), B("[              ")]],
            [[B("      "), B('"str"'), B('       ')]],
            [[B("      "), B('true'), B('        ')]],
            [[B("   "), B("]              ")]],
            [[B("]                 ")]]
        ]
        self.assertEqual(expected, texts)

    def test_array_with_object_child(self):
        """
        test rendering an array with object as a child
        """

        data = [
            1,
            2,
            {
                "test": True
            }
        ]

        # act
        node = self._node_factory.create_root_node(data)
        widget = node.get_widget()

        contents = []
        while widget is not None:
            node = widget.get_node()
            if not node.is_expanded():
                node.toggle_expanded()
            widget = node.get_widget()
            contents.append(widget.render((18,)).content())
            widget = widget.next_inorder()

        texts = [[[t[2] for t in row] for row in content]
                 for content in contents]

        # verify
        self.assertEqual(7, len(texts))
        expected = [
            [[B("[                 ")]],
            [[B("   "), B('1'), B('              ')]],
            [[B("   "), B('2'), B('              ')]],
            [[B("   "), B("{              ")]],
            [[B("      "), B('"test"'), B(": "), B("true")]],
            [[B("   "), B("}              ")]],
            [[B("]                 ")]]
        ]
        self.assertEqual(expected, texts)

    def test_prev_order(self):
        data = [
            1,
            2
        ]

        node = self._node_factory.create_root_node(data)
        # start from the end
        widget = node.get_end_node().get_widget()

        contents = []
        while widget is not None:
            contents.append(widget.render((18,)).content())
            widget = widget.prev_inorder()

        texts = [[[t[2] for t in row] for row in content]
                 for content in contents]
        texts.reverse()

        # verify
        self.assertEqual(4, len(texts))
        expected = [
            [[B("[                 ")]],
            [[B("   "), B('1'), B('              ')]],
            [[B("   "), B('2'), B('              ')]],
            [[B("]                 ")]]
        ]
        self.assertEqual(expected, texts)
