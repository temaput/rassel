from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import legal
from reportlab.lib.units import mm
from datetime import datetime


class CellBlockAbstract:
    x = 0
    y = 0
    x_shift = 0
    y_shift = 0
    template = ""
    font = ("Courier", 8)
    charSpace = 8.25
    maxSize = 9999

    def __init__(self, can, data):
        self.can = can
        self.data = data

    def prepare_text_object(self):
        self.t.setFont(*self.font)
        self.t.setCharSpace(self.charSpace)

    def set_text_origin(self):
        self.t.setTextOrigin(self.x*mm + self.x_shift,
                             self.y*mm + self.y_shift)

    def draw(self):
        self.t = self.can.beginText()
        self.prepare_text_object()
        self.set_text_origin()
        text = self.get_text()
        self.t.textLine(text)
        self.can.drawText(self.t)

    def get_data(self):
        return self.data

    def get_text(self):
        try:
            return self.template.format_map(self.get_data())[:self.maxSize]
        except (ValueError):
            return ""


class FreeBlockAbstract(CellBlockAbstract):
    charSpace = 1
    maxSize = 60


class PatientNameBlock(CellBlockAbstract):
    x = 36
    y = 39
    template = "{firstName:<18.16}{lastName:<18.15}{middleName:.1}"


class FirstRowBlock(CellBlockAbstract):
    x = 54.8
    y = 34.2

    def get_text(self):
        if self.data.get("sex", None) == "M":
            self.template = "{dob:%m %d %Y}    X        {socSec:.11}"
        else:
            self.template = "{dob:%m %d %Y}      X      {socSec:.11}"
        return super().get_text()

    def get_data(self):
        if "dob" in self.data:
            copy = self.data.copy()
            copy["dob"] = datetime.fromisoformat(copy["dob"])
            return copy
        else:
            return self.data


class AddressBlock(CellBlockAbstract):
    x = 36
    y = 44.5
    template = "{address:.33}"


class CityRow(CellBlockAbstract):
    x = 22
    y = 50
    template = "{city:<27.24}{state:<4.2}{zip:.10}"


class CellPhoneRow(CellBlockAbstract):
    x = 26.5
    y = 55
    template = "{mob:<14.10}{county:<15.11}{country:.10}"


class RaceRow(CellBlockAbstract):
    x = 36
    y = 60
    template = "{mob2:.10}"


class EmailRow(FreeBlockAbstract):
    x = 22
    y = 65
    maxSize = 80
    template = "{email}"


class GuardianRow(CellBlockAbstract):
    x = 36
    y = 76.5
    template = "{guardianLastName:<16.14}{guardianFirstName:<16.13}{guardianMiddleName:.1}"


class OccupationBlock(FreeBlockAbstract):
    x = 26.5
    y = 86
    template = "{occupation}"


class EmployerBlock(FreeBlockAbstract):
    x = 26.5
    y = 92
    template = "{employer}"


class EmployerAddressBlock(FreeBlockAbstract):
    x = 129.5
    y = 86
    template = "{employerAddress1}"


class EmployerAddressSecondBlock(FreeBlockAbstract):
    x = 129.5
    y = 92
    template = "{employerAddress2}"


class InsuranceCompanyBlock(FreeBlockAbstract):
    x = 40
    y = 115
    template = "{insuranceCompany}"


class InsuranceClaimsBlock(FreeBlockAbstract):
    x = 32.5
    y = 125
    template = "{claimsAddress}"


class InsuranceCityBlock(FreeBlockAbstract):
    maxSize = 80
    x = 29.5
    y = 132
    template = "{insuranceCity}"


class InsurancePhoneBlock(FreeBlockAbstract):
    maxSize = 80
    x = 22.5
    y = 139.5
    template = "{insurancePhone}"


class SubscriberNameBlock(FreeBlockAbstract):
    x = 139
    y = 115
    template = "{subscriberName}"


class SubscriberIDBlock(FreeBlockAbstract):
    x = 151.5
    y = 121
    template = "{subscriberID}"


class SubscriberGroupBlock(FreeBlockAbstract):
    x = 127
    y = 126.5
    template = "{subscriberGroup}"


class SubscriberDOBBlock(FreeBlockAbstract):
    x = 167.5
    y = 132.5
    maxSize = 40

    template = "{subscriberDOB:%m/%d/%Y}"

    def get_data(self):
        if "subscriberDOB" in self.data:
            copy = self.data.copy()
            copy["subscriberDOB"] = datetime.fromisoformat(copy["subscriberDOB"])
            return copy
        else:
            return self.data


class OptionBlockAbstract(CellBlockAbstract):
    optionsRegions = [(0, 0)]
    fname = "race"
    defaultOrigin = (0, 0)

    def get_origin_by_option(self):
        optionVal = self.get_data().get(self.fname, "")
        if isinstance(optionVal, int) and optionVal <= len(self.optionsRegions):
            return self.optionsRegions[optionVal-1]
        else:
            return self.defaultOrigin

    def set_text_origin(self):
        x, y = self.get_origin_by_option()
        self.t.setTextOrigin(x*mm + self.x_shift, y*mm + self.y_shift)

    def get_text(self):
        optionVal = self.get_data().get(self.fname, "")
        if isinstance(optionVal, int) and optionVal <= len(self.optionsRegions):
            return "x"
        else:
            return optionVal


class RaceOptionBlock(OptionBlockAbstract):
    optionsRegions = [(115.7, 59), (162, 59), (174.5, 59), (115.5, 63),
                      (163, 63), (175.5, 63), (193.5, 63), (115.5, 66.5)]
    fname = "race"


class EthnicityBlock(OptionBlockAbstract):
    optionsRegions = [(137, 70), (154, 70), (177.2, 70), (190, 70)]
    fname = "ethnicity"


class SubscriberRelationBlock(OptionBlockAbstract):
    optionsRegions = [(139.5, 140.5), (149.5, 140.5), (163.5, 140.5)]
    fname = "subscriberRelation"


class SubscriberRelationOtherBlock(FreeBlockAbstract):
    x = 175.5
    y = 140
    template = "{subscriberRelationOther}"


class Document:
    pageSize = legal

    blocks = [FirstRowBlock, PatientNameBlock, AddressBlock, CityRow,
              CellPhoneRow, RaceRow, EmailRow, GuardianRow, OccupationBlock, EmployerBlock,
              EmployerAddressBlock, EmployerAddressSecondBlock,
              InsuranceCompanyBlock, InsuranceClaimsBlock,
              InsuranceCityBlock, InsurancePhoneBlock,
              SubscriberNameBlock, SubscriberIDBlock, SubscriberGroupBlock,
              SubscriberDOBBlock,
              RaceOptionBlock, EthnicityBlock, SubscriberRelationBlock,
              SubscriberRelationOtherBlock




              ]

    def __init__(self, data, originalFile, destinationFile):
        self.packet = io.BytesIO()
        self.can = canvas.Canvas(self.packet, pagesize=legal, bottomup=0)
        self.data = data
        self.originalFile = originalFile
        self.destinationFile = destinationFile

    def draw_blocks(self):
        for b in self.blocks:
            b(self.can, self.data).draw()
        self.can.save()

    def finalize(self):
        print("finalizing...")
        new_pdf = PdfFileReader(self.packet)
        # read your existing PDF
        existing_pdf = PdfFileReader(self.originalFile)
        output = PdfFileWriter()

        # add the "watermark" (which is the new pdf) on the existing page
        page = existing_pdf.getPage(0)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)
        # finally, write "output" to a real file
        outputStream = self.destinationFile
        print("writing output...")
        output.write(outputStream)
        # outputStream.close()
