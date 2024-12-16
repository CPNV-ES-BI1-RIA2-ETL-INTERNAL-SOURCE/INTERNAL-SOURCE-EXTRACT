import subprocess
import tempfile


class OCRProcessor:
    def extract_text(self, pdf_data: str) -> str:
        try:
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=True) as temp_pdf:
                temp_pdf.write(pdf_data)
                temp_pdf.flush()

                result = subprocess.run(
                    ["pdftotext", "-layout", temp_pdf.name, "-"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=True,
                    text=True
                )
                return result.stdout.strip()  # Ensure no trailing spaces or empty lines in the output

        except subprocess.CalledProcessError as e:
            raise ValueError(f"Failed to extract text from PDF. Error: {e.stderr.strip()}")

        except FileNotFoundError:
            raise FileNotFoundError(
                "The 'pdftotext' tool is not installed or not found in your system's PATH. "
            )
