import math
import sublime
import sublime_plugin
import textwrap


def copy(view, text):
    sublime.set_clipboard(text)
    view.hide_popup()


class binViewerCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        output = ""
        for region in self.view.sel():
            str_num = self.view.substr(region)

            if self.isDec(str_num):
                num = int(str_num)
            elif self.isHex(str_num):
                num = int(str_num, 16)
            else:
                continue

            bin_num = self.convertToBin(num)
            content = '_'.join(textwrap.wrap(bin_num, width=8))
            output += "<li>%s = %s <a href='%s'>Copy</a> </li>\n" % (str_num, content, content)

        if output == "":
            return

        html = """
            <body>
                <style>
                    ul {
                        margin: 0;
                    }

                    a {
                        font-family: system;
                        font-size: 1.05rem;
                    }
                </style>

                <ul>
                    %s
                </ul>
            </body>
        """ % output
        self.view.show_popup(html, max_width=512, on_navigate=lambda x: copy(self.view, x))

    def isDec(self, number):
        try:
            int(number)
            return True
        except ValueError:
            return False

    def isHex(self, number):
        try:
            int(number, 16)
            return True
        except ValueError:
            return False

    def convertToBin(self, number):
        num_of_bits = self.bitsCount(number)

        if number < 0:
            number = int(hex(number & (2**num_of_bits - 1)), 16)

        return bin(number)[2:].zfill(num_of_bits)

    def bitsCount(self, number):
        count_bits = number.bit_length()
        num_of_bits = 8

        if count_bits > 8:
            num_of_bits = 2 ** math.ceil(math.log2(count_bits))

        return num_of_bits
