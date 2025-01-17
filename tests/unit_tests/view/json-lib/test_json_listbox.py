import unittest

from urwid.compat import B

from pyfx.view.json_lib.json_listbox import JSONListBox
from pyfx.view.json_lib.json_listwalker import JSONListWalker
from pyfx.view.json_lib.json_node_factory import JSONNodeFactory


class JSONListBoxTest(unittest.TestCase):

    def setUp(self):
        self._node_factory = JSONNodeFactory()

    def test_toggle_expanded_on_end_widget_mouse(self):
        """
        test listbox collapse expandable widgets on end widget with mouse event.
        """
        data = [
            'item'
        ]

        # act
        walker = JSONListWalker(data)
        listbox = JSONListBox(walker)

        # set to end widget
        listbox.set_focus(listbox.get_focus()[1].get_end_node())
        _, cur_node = listbox.get_focus()
        self.assertTrue(cur_node.is_end_node())

        listbox.mouse_event((18, 18), 'mouse press', 1, 0, 0, True)
        listbox.mouse_event((18, 18), 'mouse release', 0, 0, 0, True)
        collapse_content = [[t[2] for t in row]
                            for row in listbox.render((18, 1)).content()]

        # verify
        expected_collapse_content = [[B('[\xe2\x80\xa6]               ')]]
        self.assertEqual(expected_collapse_content, collapse_content)

    def test_toggle_expanded_on_end_widget(self):
        """
        test listbox collapse expandable widgets on end widget
        """
        data = [
            'item'
        ]

        # act
        walker = JSONListWalker(data)
        listbox = JSONListBox(walker)

        # set to end widget
        listbox.set_focus(listbox.get_focus()[1].get_end_node())
        _, cur_node = listbox.get_focus()
        self.assertTrue(cur_node.is_end_node())

        listbox.keypress((18, 18), 'enter')
        collapse_content = [[t[2] for t in row]
                            for row in listbox.render((18, 1)).content()]

        # verify
        expected_collapse_content = [[B('[\xe2\x80\xa6]               ')]]
        self.assertEqual(expected_collapse_content, collapse_content)

    def test_toggle_expanded_on_start_widget_mouse(self):
        """
        test listbox collapse expandable widgets on start widget
        """
        data = [
            'item'
        ]

        # act
        walker = JSONListWalker(data)
        listbox = JSONListBox(walker)

        listbox.mouse_event((18, 18), 'mouse press', 1, 0, 0, True)
        listbox.mouse_event((18, 18), 'mouse release', 0, 0, 0, True)
        collapse_content = [[t[2] for t in row]
                            for row in listbox.render((18, 1)).content()]

        # verify
        expected_collapse_content = [[B('[\xe2\x80\xa6]               ')]]
        self.assertEqual(expected_collapse_content, collapse_content)

    def test_toggle_expanded_on_start_widget(self):
        """
        test listbox collapse expandable widgets on start widget
        """
        data = [
            'item'
        ]

        # act
        walker = JSONListWalker(data)
        listbox = JSONListBox(walker)

        listbox.keypress((18, 18), 'enter')
        collapse_content = [[t[2] for t in row]
                            for row in listbox.render((18, 1)).content()]

        # verify
        expected_collapse_content = [[B('[\xe2\x80\xa6]               ')]]
        self.assertEqual(expected_collapse_content, collapse_content)

    def test_list_box_with_simple_object(self):
        """
        test listbox rendering simple object with collapse pressing key `enter`
        and moving focus with pressing key `ctrl n`.
        """
        data = {
            'key': 'value'
        }

        # act
        walker = JSONListWalker(data)
        listbox = JSONListBox(walker)

        contents_until_moving_to_end = []
        prev_widget = None
        cur_widget, cur_node = listbox.get_focus()
        while prev_widget != cur_widget:
            if not cur_node.is_expanded():
                listbox.keypress((18, 18), 'enter')
                cur_widget, cur_node = listbox.get_focus()
            contents_until_moving_to_end.append(
                cur_widget.render((18,)).content())
            listbox.keypress((18, 18), 'down')
            prev_widget = cur_widget
            cur_widget, cur_node = listbox.get_focus()

        texts_until_moving_to_end = [[[t[2] for t in row] for row in content]
                                     for content in
                                     contents_until_moving_to_end]

        # moving up until the start and collapse all expanded widgets
        contents_until_moving_to_start = []
        prev_widget = None
        cur_widget, cur_node = listbox.get_focus()
        while prev_widget != cur_widget:
            if cur_node.is_expanded():
                listbox.keypress((18, 18), 'enter')
                cur_widget, cur_node = listbox.get_focus()
            listbox.keypress((18, 18), 'up')
            prev_widget = cur_widget
            cur_widget, cur_node = listbox.get_focus()

        contents_until_moving_to_start.append(
            listbox.render((18, 1)).content()
        )
        texts_until_moving_to_start = [[[t[2] for t in row] for row in content]
                                       for content in
                                       contents_until_moving_to_start]

        # verify
        # verify that after moving to the end, all the expandable lines have
        # been expanded
        self.assertEqual(3, len(texts_until_moving_to_end))
        expected = [
            [[B('{                 ')]],
            [[B('   '), B('"key"'), B(': '), B('"value"'), B(' ')]],
            [[B('}                 ')]],
        ]
        self.assertEqual(expected, texts_until_moving_to_end)

        # verify that after moving to the start, all the expanded lines is
        # collapsed
        self.assertEqual(1, len(texts_until_moving_to_start))
        expected = [[[B('{\xe2\x80\xa6}               ')]]]
        self.assertEqual(expected, texts_until_moving_to_start)

    def test_list_box_with_nested_object(self):
        """
        test listbox rendering nested object with collapse pressing key `enter`
        and moving focus with pressing key `ctrl n`.
        """
        data = {
            "key": {
                "key": 'val'
            }
        }

        # act
        walker = JSONListWalker(data)
        listbox = JSONListBox(walker)

        # moving down until the end and expand all expandable widgets
        contents_until_moving_to_end = []
        prev_widget = None
        cur_widget, cur_node = listbox.get_focus()
        while prev_widget != cur_widget:
            if not cur_node.is_expanded():
                listbox.keypress((18, 18), 'enter')
                cur_widget, cur_node = listbox.get_focus()
            listbox.keypress((18, 18), 'down')
            prev_widget = cur_widget
            cur_widget, cur_node = listbox.get_focus()

        contents_until_moving_to_end.append(listbox.render((18, 5)).content())
        texts_until_moving_to_end = [[[t[2] for t in row] for row in content]
                                     for content in
                                     contents_until_moving_to_end]

        # moving up until the start and collapse all expanded widgets
        contents_until_moving_to_start = []
        prev_widget = None
        cur_widget, cur_node = listbox.get_focus()
        while prev_widget != cur_widget:
            if cur_node.is_expanded():
                listbox.keypress((18, 18), 'enter')
                cur_widget, cur_node = listbox.get_focus()
            listbox.keypress((18, 18), 'up')
            prev_widget = cur_widget
            cur_widget, cur_node = listbox.get_focus()

        contents_until_moving_to_start.append(
            listbox.render((18, 1)).content()
        )
        texts_until_moving_to_start = [[[t[2] for t in row] for row in content]
                                       for content in
                                       contents_until_moving_to_start]

        # verify
        # verify that after moving to the end, all the expandable lines have
        # been expanded
        self.assertEqual(1, len(texts_until_moving_to_end))
        expected = [[
            [B("{                 ")],
            [B("   "), B('"key"'), B(": "), B("{       ")],
            [B("      "), B('"key"'), B(": "), B('"val"')],
            [B("   "), B("}              ")],
            [B("}                 ")]
        ]]
        self.assertEqual(expected, texts_until_moving_to_end)

        # verify that after moving to the start, all the expanded lines is
        # collapsed
        self.assertEqual(1, len(texts_until_moving_to_start))
        expected = [[[B("{\xe2\x80\xa6}               ")]]]
        self.assertEqual(expected, texts_until_moving_to_start)

    def test_expand_all_from_start_node(self):
        """
        test listbox expand all nested nodes when press key `e`.
        """
        data = {
            "key": {
                "key": 'val'
            }
        }

        # act
        walker = JSONListWalker(data)
        listbox = JSONListBox(walker)

        listbox.keypress((18, 5), 'e')

        content = [[t[2] for t in row] for row in
                   listbox.render((18, 5)).content()]

        # verify
        expected = [
            [B("{                 ")],
            [B("   "), B('"key"'), B(": "), B("{       ")],
            [B("      "), B('"key"'), B(": "), B('"val"')],
            [B("   "), B("}              ")],
            [B("}                 ")]
        ]
        self.assertEqual(expected, content)

    def test_expand_all_from_middle_node(self):
        """
        test listbox expand all nested nodes when press key `e` and focus is at
        the middle of a node.
        """
        data = [
            {
                "key": [
                    "1",
                    "2"
                ]
            },
            {
                "key": [
                    "2"
                ]
            }
        ]

        # act
        walker = JSONListWalker(data)
        listbox = JSONListBox(walker)
        size = (18, 13)  # 13 rows after expanded in total

        # move to focus to the second item, thus move down twice, as the view
        # should be expanded at the first level
        listbox.move_focus_to_next_line(size)
        listbox.move_focus_to_next_line(size)

        listbox.keypress(size, 'e')

        content = [[t[2] for t in row] for row in
                   listbox.render(size).content()]

        # verify
        expected = [
            [B("[                 ")],
            [B("   "), B("{              ")],
            [B("      "), B('"key"'), B(": "), B("[    ")],
            [B("         "), B('"1"'), B('      ')],
            [B("         "), B('"2"'), B('      ')],
            [B("      "), B("]           ")],
            [B("   "), B("}              ")],
            [B("   "), B("{              ")],
            [B("      "), B('"key"'), B(": "), B("[    ")],
            [B("         "), B('"2"'), B('      ')],
            [B("      "), B("]           ")],
            [B("   "), B("}              ")],
            [B("]                 ")]
        ]
        self.assertEqual(expected, content)

    def test_collapse_all_from_start_node(self):
        """
        test listbox collapse all nested nodes when press key `c`.
        """
        data = {
            "key": {
                "key": 'val'
            }
        }

        # act
        walker = JSONListWalker(data)
        listbox = JSONListBox(walker)
        size = (18, 5)

        listbox.keypress(size, 'c')

        content = [[t[2] for t in row] for row in
                   listbox.render(size).content()]

        # verify
        expected = [
            [B("{\xe2\x80\xa6}               ")],
            [B("                  ")],
            [B("                  ")],
            [B("                  ")],
            [B("                  ")]
        ]
        self.assertEqual(expected, content)

    def test_collapse_all_from_middle_node(self):
        """
        test listbox collapse all nested nodes when press key `c`.
        """
        data = [
            {
                "key": [
                    "1",
                    "2"
                ]
            },
            {
                "key": [
                    "2"
                ]
            }
        ]

        # act
        walker = JSONListWalker(data)
        listbox = JSONListBox(walker)
        size = (18, 13)  # 13 rows after expanded in total

        # move to focus to the second item, thus move down twice, as the view
        # should be expanded at the first level
        listbox.move_focus_to_next_line(size)
        listbox.move_focus_to_next_line(
            size)  # move to the second item in the list
        listbox.toggle_collapse_on_focused_parent(
            size)  # expand the second item
        listbox.move_focus_to_next_line(
            size)  # move to the first child of the object
        listbox.toggle_collapse_on_focused_parent(size)  # expand the object
        listbox.move_focus_to_next_line(
            size)  # move to the first child of the object

        listbox.keypress(size, 'c')

        content = [[t[2] for t in row] for row in
                   listbox.render((18, 2)).content()]

        # verify
        expected = [
            [B("[\xe2\x80\xa6]               ")],
            [B("                  ")]
        ]
        self.assertEqual(expected, content)

    def test_expand_after_collapse_all(self):
        """
        test listbox will collapse all nested nodes after keypress 'c'
        """
        """
        test listbox collapse all nested nodes when press key `c`.
        """
        data = [
            {
                "key": [
                    "1",
                    "2"
                ]
            },
            {
                "key": [
                    "2"
                ]
            }
        ]

        # act
        walker = JSONListWalker(data)
        listbox = JSONListBox(walker)
        size = (18, 13)  # 13 rows after expanded in total

        listbox.expand_all(size)  # expand all first to expand all nodes

        listbox.keypress(size, "c")  # collapse all

        listbox.toggle_collapse_on_focused_parent(size)

        content = [[t[2] for t in row] for row in
                   listbox.render((18, 4)).content()]

        # verify
        expected = [
            [B("[                 ")],
            [B("   "), B("{\xe2\x80\xa6}            ")],
            [B("   "), B("{\xe2\x80\xa6}            ")],
            [B("]                 ")]
        ]
        self.assertEqual(expected, content)
