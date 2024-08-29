"""
File in charge of containing the demo script for the ask question TUI library
"""

import asciimatics.widgets as WIG
from asciimatics.event import Event
from asciimatics.screen import Screen as SC
from asciimatics_overlay_ov.widgets import FrameNodes
from asciimatics_overlay_ov import AsciiMaticsOverlayMain
from .ask_question_tui import AskQuestionTUI


class AskQuestionTUIDemo(WIG.Frame, AsciiMaticsOverlayMain, FrameNodes):
    """ The class in charge of dislaying the demo of the library """

    def __init__(self, screen: SC = None) -> None:
        if screen is None:
            return
        super(AskQuestionTUIDemo, self).__init__(
            screen,
            screen.height,
            screen.width,
            has_border=True,
            title="Ask question (TUI version)"
        )
        self.asciimatics_overlay = AsciiMaticsOverlayMain(Event, screen)
        self.frame_node = FrameNodes()
        self.ask_question_tui = AskQuestionTUI()

    def main(self, screen: SC) -> int:
        """ The main function of the demo program """

    def run(self) -> None:
        """ Run the demo """
        SC.wrapper()


if __name__ == "__main__":
    AQTUID = AskQuestionTUIDemo()
    AQTUID.run()
