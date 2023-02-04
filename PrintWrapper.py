from escpos.printer import Usb


class PrintManager:
    def __init__(self, vendor_id, product_id):
        """This function is the constructor for the PrintManager class.
           It takes two parameters, vendor_id and product_id, and creates a Usb object with them."""
        self.p = Usb(vendor_id, product_id)

    def println(self, text, cut=False):
        """This function prints a line of text and optionally cuts the paper after it.
           It takes two parameters, text and cut.
           If cut is set to True, it will cut the paper after printing the line."""
        self.p.text(text + "\n")
        if cut:
            self.p.cut()

    def printb(self, text, cut=False):
        """This function prints a line of text in bold and optionally cuts the paper after it.
           It takes two parameters, text and cut.
           If cut is set to True, it will cut the paper after printing the line."""
        self.p.set(text_type="B")
        self.p.text(text + "\n")
        self.p.set(text_type="normal")
        if cut:
            self.p.cut()

    def printbu(self, text, cut=False):
        """This function prints a line of text in bold and underlined and optionally cuts the paper after it.
           It takes two parameters, text and cut.
           If cut is set to True, it will cut the paper after printing the line."""
        self.p.set(text_type="BU")
        self.p.text(text + "\n")
        self.p.set(text_type="normal")
        if cut:
            self.p.cut()

    def qr(self, text, cut=False):
        """This function prints a QR code and optionally cuts the paper after it.
           It takes two parameters, text and cut.
           If cut is set to True, it will cut the paper after printing the QR code."""
        self.p.qr(text)
        if cut:
            self.p.cut()

    def pdocument(self, document):
        """This function prints a document with some formatting.
           It takes a single parameter, document, which is a string containing the text of the document.
           It will print the document, with # lines printed in bold and underlined, ## lines printed in bold,
           and --- lines printed as a line of 42 dashes."""

        for line in document.splitlines():
            if line:
                if line.startswith('# '):
                    self.printbu(line.replace("# ", ""))
                elif line.startswith('## '):
                    self.printb(line.replace("## ", ""))
                elif line.startswith('---'):
                    self.println("-" * 42)
                elif line.startswith('*'):
                    self.println(" " * 4 + line.replace("*", "-"))
                else:
                    self.p.text(f"{line}\n")

            else:
                self.p.text(' '*42)

        self.p.cut()

    def part(self, document):
        """This function prints a document with some formatting.
           It takes a single parameter, document, which is a string containing the text of the document.
           It will print the document, with lines that are longer than 42 characters split into multiple lines with 42 characters per line."""
        for line in document.splitlines():
            if line:
                if len (line) > 42:
                    self.p.text(line[:42])
                    self.p.text('\n')
                else:
                    self.p.text(line.ljust(42)[:42])

                self.p.text(line)
            else:
                self.p.text(' '*42)
        self.p.cut()
