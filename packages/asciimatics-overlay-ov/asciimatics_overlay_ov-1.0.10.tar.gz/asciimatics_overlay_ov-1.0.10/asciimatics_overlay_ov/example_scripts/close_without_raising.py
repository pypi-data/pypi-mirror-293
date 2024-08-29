"""
File in charge of closing the scene without raising an error
"""


import asciimatics.widgets as WIG
from asciimatics.event import Event
from asciimatics.exceptions import NextScene
from asciimatics_overlay_ov import AsciiMaticsOverlayMain
from asciimatics_overlay_ov.widgets import FrameNodes


class CloseWithoutRaisingChild(WIG.Frame, AsciiMaticsOverlayMain, FrameNodes):
    """ A demo of a window allowing you to gather it's data """

    def __init__(self, screen):
        super(CloseWithoutRaisingChild, self).__init__(
            screen,
            screen.height,
            screen.width,
            has_border=True,
            title="Hello World"
        )
        self.child_input = None
        self.usr_input = ""
        self.child_destination = None
        self.frame_node = FrameNodes()
        self.asciimatics_overlay = AsciiMaticsOverlayMain(Event, screen)
        self.layout = WIG.Layout([1, 1])  # Define a layout with three columns
        self.add_layout(self.layout)
        self.layout2 = WIG.Layout([1, 1])  # Define a layout with three columns
        self.add_layout(self.layout2)
        self.place_content_on_screen()
        self.fix()

    def place_content_on_screen(self) -> None:
        """ Create the welcome screen """
        self.layout.add_widget(
            self.add_label(
                "This is what you entered in the child window:",
                align=self.frame_node.label_center,
                name=None
            ),
            0
        )
        self.child_input = self.add_input(
            label="Sample input:",
            on_change=self._get_usr_input,
            name="text"
        )
        self.layout.add_widget(
            self.child_input,
            0
        )
        self.layout2.add_widget(
            self.add_label(
                "This is what you entered in the child window:",
                align=self.frame_node.label_center,
                name=None
            ),
            0
        )
        self.child_destination = self.add_label(
            "This is what you entered in the child window:",
            align=self.frame_node.label_center,
            name="usr_input"
        )
        self.layout2.add_widget(
            self.child_destination,
            1
        )
        self.layout.add_widget(
            self.add_button(
                text="Confirm",
                on_click=self._exit,
                name=None
            ),
            0
        )

    def _get_usr_input(self) -> None:
        """ Get the user input """
        self.usr_input = self.get_text_input(self.child_input)
        self.apply_text_to_display(self.child_destination, self.usr_input)

    def _exit(self) -> str:
        """ The exit function in charge of gathering data """
        self.screen.close()
        return self.usr_input


class CloseWithoutRaising(WIG.Frame, AsciiMaticsOverlayMain, FrameNodes):
    """ A demo of a window allowing you to gather it's data """

    def __init__(self, screen):
        super(CloseWithoutRaising, self).__init__(
            screen,
            screen.height,
            screen.width,
            has_border=True,
            title="Hello World"
        )
        self.frame_node = FrameNodes()
        self.usr_input = ""
        self.usr_input_label = None
        self.asciimatics_overlay = AsciiMaticsOverlayMain(Event, screen)
        self.layout = WIG.Layout([1, 1])  # Define a layout with three columns
        self.add_layout(self.layout)
        self.layout2 = WIG.Layout([1, 1])  # Define a layout with three columns
        self.add_layout(self.layout2)
        self.place_content_on_screen()
        self.fix()

    def place_content_on_screen(self) -> None:
        """ Create the welcome screen """
        self.layout.add_widget(
            self.add_label(
                "The next window will close without raising an error.",
                align=self.frame_node.label_center,
                name=None
            ),
            0
        )
        self.layout.add_widget(
            self.add_label(
                "This will allow this widow to see the return of your input.",
                align=self.frame_node.label_center,
                name=None
            ),
            0
        )
        self.layout.add_widget(
            self.add_button(
                text="Test the window",
                on_click=self._exit,
                name=None
            ),
            0
        )
        self.layout2.add_widget(
            self.add_label(
                "This is what you entered in the child window:",
                align=self.frame_node.label_center,
                name=None
            ),
            0
        )
        self.usr_input_label = self.add_label(
            "This is what you entered in the child window:",
            align=self.frame_node.label_center,
            name="usr_input"
        )
        self.layout2.add_widget(self.usr_input_label, 1)
        self.layout.add_widget(
            self.add_button(
                text="Exit",
                on_click=self._exit,
                name=None
            ),
            0
        )

    def _spawn_and_get_content(self) -> None:
        """ Create the welcome screen """
        data = CloseWithoutRaisingChild(screen=self.screen)
        self.usr_input = data
        if self.usr_input is None:
            self.usr_input = data.usr_input
        self.apply_text_to_display(self.usr_input_label, self.usr_input)

    def _exit(self):
        raise NextScene("Main")
