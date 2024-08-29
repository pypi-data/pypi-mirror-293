##
# EPITECH PROJECT, 2022
# Desktop_pet (Workspace)
# File description:
# ask_question.py
##

"""
The file containing the code to speed up the boiling
process that occurs when a question is asked.
This module is provided as if and without any warranty
Crediting the author is appreciated.
"""

__Version__ = "1.1.0"
__Author__ = "(c) Henry Letellier"

from typing import Union
from string import printable
import asciimatics.widgets as WIG
from asciimatics.event import Event
from asciimatics import screen as SC
from asciimatics_overlay_ov.widgets import FrameNodes
from asciimatics_overlay_ov import AsciiMaticsOverlayMain


class AskQuestionAnswerProcessing:
    """ Class in charge of processing the input of the user and saying if it is correct or not """

    def __init__(self, human_type: dict = {}, illegal_characters_nb: str = "") -> None:
        print("Warning, ask_question_tui is still being developed, this means that it is unstable.")
        self.human_type = human_type
        self.illegal_characters_nb = illegal_characters_nb
        self.author = "(c) Henry Letellier"
        self.usr_answer = ""
        self.answer_was_found = True
        self.answer_was_not_found = False
        self.illegal_characters_found = False
        self.check_load()

    def check_load(self) -> None:
        """ Check that the ressources are present """
        if self.human_type == dict():
            self.human_type = {
                "int": "whole number (-1, 0, 1, 2, 3, etc...)",
                "float": "floating number (-1.2, 0.1, 1.2, etc...)",
                "uint": "whole positive number (0, 1, 2, etc...)",
                "ufloat": "whole positive floating number (0.1, 1.2, etc ...)",
                "num": "numeric (numbers from 0 onwards)",
                "alnum": "alphanumeric (only numbers and the alphabet)",
                "isalpha": "alphabet (from a to z and A to Z)",
                "char": "alphabet (from a to z and A to Z)",
                "ascii": "ascii Table",
                "str": "string (any character you can type)",
                "version": "version (numbers seperated by '.' characters)",
                "ver": "version (numbers seperated by '.' characters)",
                "bool": "boolean (yes/True/1 or no/False/0 answer type)",
            }
        if self.illegal_characters_nb == "":
            self.illegal_characters_nb = printable.replace("-", "")
            self.illegal_characters_nb = self.illegal_characters_nb.replace(
                ".",
                ""
            )
            self.illegal_characters_nb = self.illegal_characters_nb.replace(
                ",",
                ""
            )
            self.illegal_characters_nb = self.illegal_characters_nb.replace(
                "+",
                ""
            )
            self.illegal_characters_nb = self.illegal_characters_nb.replace(
                "0123456789",
                ""
            )

    def is_empty(self, string: str) -> bool:
        """ Check if the string is not empty """
        if len(string) == 0:
            return True
        return False

    def is_version(self, string: str) -> bool:
        """ Check if the given string is a version """
        string_length = len(string)-1
        for i in enumerate(string):
            if i[1].isdigit() is False:
                if i[0] == string_length and (i[1] == '.' or i[1] == ','):
                    return False
                if i[1] != "." and i[1] != ",":
                    return False
        return True

    def is_float(self, number: str) -> bool:
        """ Check if the given string is a float """
        try:
            float(number)
            return True
        except ValueError:
            return False

    def contains_illegal_characters(self, string: str, illegal_characters: str) -> bool:
        """ Check if there are no forbidden characters in a string destined to be converted to a number """
        for i in string:
            if i in illegal_characters:
                return True
        return False

    def remove_char_overflow(self, string: str, char: str, presence_tolerance: int = 1, case_sensitive: bool = False) -> str:
        """ Remove the number of times a specific character appears in a string after the allowed number of times """
        result = ""
        for i in string:
            if case_sensitive is False:
                if i.lower() == char:
                    if presence_tolerance > 0:
                        result += i
                        presence_tolerance -= 1
                else:
                    result += i
            else:
                if i == char:
                    if presence_tolerance > 0:
                        result += i
                        presence_tolerance -= 1
                else:
                    result += i
        return result

    def clean_number(self, string: str, char: str = ".", tolerance: int = 1, case_sensitive: bool = False) -> str:
        """ Remove content that should not be in a number input """
        if " " in string:
            string = string.replace(" ", "")
        if "," in string:
            string = string.replace(",", ".")
        if string.count(char) > tolerance:
            string = self.remove_char_overflow(
                string, char, tolerance, case_sensitive)
        return string

    def _display_accordingly(self, message: str, is_tui: bool = False) -> list[str, int]:
        """ Display the message depending on is_tui """
        if is_tui is True:
            return [self.answer_was_not_found, message]
        print(message)
        return [self.answer_was_not_found, ""]

    def _process_isalnum(self, input_answer: str, answer_type: str) -> bool:
        """ Process the isalnum data """
        if input_answer.isalnum() is True and "alnum" in answer_type:
            self.usr_answer = input_answer
            return self.answer_was_found
        return self.answer_was_not_found

    def _process_isalpha(self, input_answer: str, answer_type: str) -> bool:
        """ Process the isalpha data """
        if input_answer.isalpha() is True and "char" in answer_type:
            self.usr_answer = input_answer
            return self.answer_was_found
        return self.answer_was_not_found

    def _process_isdigit(self, input_answer: str, answer_type: str) -> bool:
        """ Process the isdigit data """
        if input_answer.isdigit() is True and "num" in answer_type:
            self.usr_answer = float(input_answer)
            return self.answer_was_found
        return self.answer_was_not_found

    def _process_isascii(self, input_answer: str, answer_type: str) -> bool:
        """ Process the isascii data """
        if input_answer.isascii() is True and "ascii" in answer_type:
            self.usr_answer = input_answer
            return self.answer_was_found
        return self.answer_was_not_found

    def _process_to_up(self, input_answer: str, answer_type: str) -> bool:
        """ Process the to up data """
        if "up" in answer_type:
            self.usr_answer = input_answer.upper()
            return self.answer_was_found
        return self.answer_was_not_found

    def _process_to_low(self, input_answer: str, answer_type: str) -> bool:
        """ Process the to low data """
        if "low" in answer_type:
            self.usr_answer = input_answer.lower()
            return self.answer_was_found
        return self.answer_was_not_found

    def _process_version(self, input_answer: str, answer_type: str) -> bool:
        """ Process the version data """
        if self.is_version(input_answer) is True and "version" in answer_type or "ver" in answer_type:
            self.usr_answer = input_answer
            return self.answer_was_found
        return self.answer_was_not_found

    def _process_uint(self, input_answer: str, answer_type: str) -> bool:
        """ Process the uint data """
        if input_answer.isdigit() is True and "uint" in answer_type:
            self.usr_answer = int(input_answer)
            return self.answer_was_found
        return self.answer_was_not_found

    def _process_ufloat(self, input_answer: str, answer_type: str) -> bool:
        """ Process the ufloat data """
        if self.is_float(input_answer) is True and "ufloat" in answer_type:
            self.usr_answer = float(input_answer)
            return self.answer_was_found
        return self.answer_was_not_found

    def _process_bool(self, input_answer: str, answer_type: str) -> bool:
        """ Process the bool data """
        if "bool" in answer_type:
            input_answer = input_answer.lower()
            if "y" in input_answer or "t" in input_answer or "1" in input_answer:
                self.usr_answer = True
                return self.answer_was_found
            if "n" in input_answer or "f" in input_answer or "0" in input_answer:
                self.usr_answer = False
                return self.answer_was_found
            self.usr_answer = None
            return self.answer_was_not_found
        return self.answer_was_not_found

    def _process_int(self, input_answer: str, answer_type: str) -> bool:
        """ Process the uint data """
        if "int" in answer_type and "uint" not in answer_type and self.illegal_characters_found is False:
            input_answer = self.clean_number(input_answer, ".", 0, False)
            input_answer = self.remove_char_overflow(
                input_answer, "-", 1, False)
            try:
                self.usr_answer = int(input_answer)
                return self.answer_was_found
            except TypeError:
                self.usr_answer = ""
                return self.answer_was_not_found
            except BaseException:
                self.usr_answer = ""
                return self.answer_was_not_found
        return self.answer_was_not_found

    def _process_float(self, input_answer: str, answer_type: str) -> bool:
        """ Process the float data """
        if "float" in answer_type and "ufloat" not in answer_type and self.illegal_characters_found is False:
            input_answer = self.clean_number(input_answer, ".", 1, False)
            input_answer = self.remove_char_overflow(
                input_answer,
                "-",
                1,
                False
            )
            try:
                self.usr_answer = float(input_answer)
                return self.answer_was_found
            except TypeError:
                self.usr_answer = ""
                return self.answer_was_not_found
            except BaseException:
                self.usr_answer = input_answer
                return self.answer_was_not_found
        return self.answer_was_not_found

    def _first_chunk(self, input_answer: str, answer_type: str) -> bool:
        """ The second chunk in charge of cheking the inputted data """
        if self._process_isalnum(input_answer, answer_type) is self.answer_was_found:
            return self.answer_was_found
        if self._process_isalpha(input_answer, answer_type) is self.answer_was_found:
            return self.answer_was_found
        if self._process_isdigit(input_answer, answer_type) is self.answer_was_found:
            return self.answer_was_found
        if self._process_isascii(input_answer, answer_type) is self.answer_was_found:
            return self.answer_was_found
        if self._process_to_up(input_answer, answer_type) is self.answer_was_found:
            return self.answer_was_found
        return self.answer_was_not_found

    def _second_chunk(self, input_answer: str, answer_type: str) -> bool:
        """ The second chunk in charge of cheking the inputted data """
        if self._process_to_low(input_answer, answer_type) is self.answer_was_found:
            return self.answer_was_found
        if self._process_version(input_answer, answer_type) is self.answer_was_found:
            return self.answer_was_found
        if self._process_uint(input_answer, answer_type) is self.answer_was_found:
            return self.answer_was_found
        if self._process_ufloat(input_answer, answer_type) is self.answer_was_found:
            return self.answer_was_found
        if self._process_bool(input_answer, answer_type) is self.answer_was_found:
            return self.answer_was_found
        return self.answer_was_not_found

    def _third_chunk(self, input_answer: str, answer_type: str) -> bool:
        """ The third chunk in charge of cheking the inputted data """
        if self._process_int(input_answer, answer_type) is self.answer_was_found:
            return self.answer_was_found
        if self._process_float(input_answer, answer_type) is self.answer_was_found:
            return self.answer_was_found
        return self.answer_was_not_found

    def test_input(self, input_answer: str, answer_type: str, is_tui: bool = False) -> Union[str, int, float, bool, list]:
        """ The function in charge of ensuring that the user's response corresponds to the programmer's expectations """
        if self.is_empty(input_answer) is False and input_answer.isspace() is False and input_answer.isprintable() is True:
            self.illegal_characters_found = self.contains_illegal_characters(
                input_answer,
                self.illegal_characters_nb
            )
            status1 = self._first_chunk(input_answer, answer_type)
            if status1 == self.answer_was_found:
                return self.answer_was_found
            status2 = self._second_chunk(input_answer, answer_type)
            if status2 == self.answer_was_found:
                return self.answer_was_found
            status3 = self._third_chunk(input_answer, answer_type)
            if status3 == self.answer_was_found:
                return self.answer_was_found
            self.usr_answer = ""
            response = "Please enter a response of type '"
            response += f"{self.human_type[answer_type]}'"
            return self._display_accordingly(response, is_tui)
        self.usr_answer = ""
        response = "Response must not be empty or only contain spaces or any non visible character."
        return self._display_accordingly(response, is_tui)


class AskQuestionTUIManagement(WIG.Frame, AsciiMaticsOverlayMain, FrameNodes):
    """ The class in charge of managing the TUI """

    def __init__(self, screen: SC, ask_question_answer_processing: AskQuestionAnswerProcessing, question: str, answer_type: str, screen_width: int, screen_height: int, screen_offset_x: int, screen_offset_y: int) -> None:
        """ The globals for the class """
        final_screen_width = self._recalculate_screen_width(
            screen.width,
            screen_width,
            screen_offset_x
        )
        final_screen_height = self._recalculate_screen_height(
            screen.height,
            screen_height,
            screen_offset_y
        )

        super(AskQuestionTUIManagement, self).__init__(
            screen,
            final_screen_height,
            final_screen_width,
            has_border=True,
            title="Ask question (TUI version)"
        )
        self.__version__ = "1.0.0"
        self.author = "(c) Henry Letellier"
        self.version = self.__version__
        self.question = question
        self.answer_type = answer_type
        self.screen = screen
        self.usr_answer = ""
        self.error_message = ""
        self.textbox_widget = None
        self.error_message_widget = None
        self.user_has_decided_to_quit = False
        self.run_status = self.success

        self.asciimatics_overlay = AsciiMaticsOverlayMain(Event, screen)
        self.frame_node = FrameNodes()
        self.ask_question_answer_processing = ask_question_answer_processing

        # Define a layout with three columns
        self.layout = WIG.Layout([100], fill_frame=True)
        self.add_layout(self.layout)
        self.layout_buttons = WIG.Layout([25, 25, 25, 25], fill_frame=False)
        self.add_layout(self.layout_buttons)
        self.place_content_on_screen()
        self.fix()

    def _recalculate_screen_height(self, screen_height: int, usr_screen_height: int, usr_screen_offset: int) -> int:
        """ Recalculate the screen size """
        default_screen_height = screen_height
        if usr_screen_height > 0 and usr_screen_height < default_screen_height:
            screen_height = usr_screen_height
        if usr_screen_offset > 0 and usr_screen_offset < default_screen_height:
            screen_height += usr_screen_offset
        return screen_height

    def _recalculate_screen_width(self, screen_width: int, usr_screen_width: int, usr_screen_offset: int) -> int:
        """ Recalculate the screen width """
        default_screen_width = screen_width
        if usr_screen_width > 0 and usr_screen_width < default_screen_width:
            screen_width = usr_screen_width
        if usr_screen_offset > 0 and usr_screen_offset < default_screen_width:
            screen_width += usr_screen_offset
        return screen_width

    def place_content_on_screen(self) -> None:
        """ Place the required assets on the screen for the user to interact """
        self.textbox_widget = self.add_textbox(
            height=5,
            label=self.question,
            name="usr_input",
            as_string=True,
            line_wrap=True,
            on_change=self._reset_error_message,
            readonly=False
        )
        self.error_message_widget = self.add_label(
            text=self.error_message,
            height=2,
            align=self.label_center,
            name="error_message"
        )
        self.layout.add_widget(self.textbox_widget, 0)
        self.layout.add_widget(self.error_message_widget, 0)
        self.layout_buttons.add_widget(
            self.add_button(
                text="Submit",
                on_click=self._submit,
                name=None
            ),
            1
        )
        self.layout_buttons.add_widget(
            self.add_button(
                text="Cancel",
                on_click=self._exit,
                name=None
            ),
            2
        )

    def _reset_error_message(self) -> None:
        """ Reset the error message """
        self.error_message = ""
        self.apply_text_to_display(
            self.error_message_widget, self.error_message)

    def _check_usr_input(self) -> Union[str, int, float, bool]:
        """ Check the input provided by the user """
        usr_input = self.get_widget_value(self.textbox_widget)
        self.usr_answer = self.ask_question_answer_processing.test_input(
            usr_input, self.answer_type, is_tui=True)
        if isinstance(self.usr_answer, list) is True:
            self.apply_text_to_display(
                self.error_message_widget,
                self.usr_answer[1]
            )
            self.error_message = self.usr_answer[1]
            self.run_status = self.error
        else:
            self._reset_error_message()
            self.run_status = self.success
            return self.usr_answer

    def _submit(self) -> str:
        """ Submit the answer """
        self._check_usr_input()
        if isinstance(self.usr_answer, list) is True:
            self.usr_answer = self.usr_answer[0]
        self._exit()

    def _exit(self) -> None:
        """ Exit the Scene """
        self.usr_answer = ""
        self.user_has_decided_to_quit = True


class AskQuestionTUI:
    """ An advanced function that contains boiling to gain time when asking a question """

    def __init__(self, screen: SC, human_type: dict = {}, illegal_characters_nb: str = "", screen_width: int = -1, screen_height: int = -1, screen_offset_x: int = 0, screen_offset_y: int = 0, tui_enabled: bool = True) -> None:
        """ The globals for the class """
        self.__version__ = "1.0.0"
        self.human_type = human_type
        self.illegal_characters_nb = illegal_characters_nb
        self.author = "(c) Henry Letellier"
        self.version = self.__version__
        self.usr_answer = ""
        self.answer_was_found = True
        self.answer_was_not_found = False
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen_offset_x = screen_offset_x
        self.screen_offset_y = screen_offset_y
        self.user_has_decided_to_quit = False
        if tui_enabled is None:
            self.tui_enabled = True
        else:
            self.tui_enabled = tui_enabled
        self.ask_question_tui_management = None
        self.ask_question_answer_processing = AskQuestionAnswerProcessing(
            human_type=human_type,
            illegal_characters_nb=illegal_characters_nb
        )

    def ask_question_tty(self, question: str, answer_type: str) -> Union[str, int, float, bool]:
        """ Ask a question and continue asking until type met """
        answer_found = False
        usr_answer = ""
        self.usr_answer = ""
        while answer_found is False:
            usr_answer = input(str(question))
            answer_found = self.ask_question_answer_processing.test_input(
                usr_answer,
                answer_type,
                is_tui=False
            )
            if isinstance(answer_found, list) is True:
                answer_found = False
        self.usr_answer = self.ask_question_answer_processing.usr_answer
        return self.usr_answer

    def ask_question_tui(self, question: str, answer_type: str) -> Union[str, int, float, bool]:
        """ Display a graphical interface to ask the question """
        aqtuim = AskQuestionTUIManagement(
            screen=self.screen,
            ask_question_answer_processing=self.ask_question_answer_processing,
            question=question,
            answer_type=answer_type,
            screen_width=self.screen_width,
            screen_height=self.screen_height,
            screen_offset_x=self.screen_offset_x,
            screen_offset_y=self.screen_offset_y
        )
        self.usr_answer = aqtuim.usr_answer
        self.user_has_decided_to_quit = aqtuim.user_has_decided_to_quit
        return self.usr_answer

    def ask_question(self, question: str, answer_type: str, tui_enabled: bool = None) -> Union[str, int, float, bool]:
        """ Display a graphical or non-graphical question based on the input """
        if tui_enabled is None:
            tui_enabled = self.tui_enabled
        if tui_enabled is True:
            return self.ask_question_tui(question, answer_type)
        return self.ask_question_tty(question, answer_type)

    def pause(self, pause_message: str = "Press enter to continue...") -> None:
        """ Act like the windows batch pause function """
        empty = ""
        pause_response = input(pause_message)
        empty += pause_response


if __name__ == "__main__":
    AQI = AskQuestionTUI(dict(), "")
    answer = AQI.ask_question("How old are you?", "uint")
    ADD_S = ""
    if answer > 1:
        ADD_S = "s"
    print(f"You are {answer} year{ADD_S} old")
    answer = AQI.ask_question("Enter a ufloat:", "ufloat")
    print(f"You entered {answer}")
    AQI.pause()
