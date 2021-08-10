import sublime_plugin
import textwrap


class binViewerCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        region = self.view.sel()[0]
        str_num = self.view.substr(region)

        if self.isDec(str_num):
            num = int(str_num)
        elif self.isHex(str_num):
            num = int(str_num, 16)
        else:
            return

        bin_num = self.convertToBin(num)
        content = '_'.join(textwrap.wrap(bin_num, width=8))
        self.view.show_popup(content, location=-1, on_navigate=print, max_width=400)

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

        if count_bits > 32:
            num_of_bits = 64
        elif count_bits > 16:
            num_of_bits = 32
        elif count_bits > 8:
            num_of_bits = 16

        return num_of_bits


0xdeadbeef