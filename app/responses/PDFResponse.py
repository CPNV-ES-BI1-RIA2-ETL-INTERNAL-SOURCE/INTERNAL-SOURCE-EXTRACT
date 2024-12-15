from pydantic import RootModel


class PDFResponse(RootModel[list]):
    pass