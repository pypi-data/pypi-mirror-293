import os
import subprocess
import tempfile
from typing import Optional

from .latex import recipe_to_latex, LatexOptions
from .models import Recipe


class PdfOptions:
    """
    Represents options for the PDF conversion process.

    Attributes:
        reproducible (bool): Whether to enforce reproducible builds by setting SOURCE_DATE_EPOCH.
        source_date_epoch (Optional[str]): The value for SOURCE_DATE_EPOCH to enforce reproducible builds. Defaults to "0".
    """

    def __init__(self, reproducible: bool = False, source_date_epoch: Optional[str] = "0"):
        self.reproducible = reproducible
        self.source_date_epoch = source_date_epoch


def recipe_to_pdf(recipe: Recipe, latex_options: Optional[LatexOptions] = None, pdf_options: Optional[PdfOptions] = None) -> bytes:
    """
    Converts a `Recipe` object to a PDF using LaTeX and returns the PDF content as bytes.

    Args:
        recipe (Recipe): The `Recipe` object to be converted to PDF.
        latex_options (Optional[LatexOptions]): The options to use for the LaTeX conversion process.
        pdf_options (Optional[PdfOptions]): The options to use for the PDF conversion process.

    Returns:
        bytes: The generated PDF content as bytes.
    """
    if pdf_options is None:
        pdf_options = PdfOptions()

    latex_content = recipe_to_latex(recipe, latex_options)
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file = os.path.join(temp_dir, 'recipe.tex')
        with open(temp_file, 'w') as f:
            f.write(latex_content)

        env = os.environ.copy()

        if pdf_options.reproducible:
            env["SOURCE_DATE_EPOCH"] = pdf_options.source_date_epoch
            env["FORCE_SOURCE_DATE"] = "1"
        
        subprocess_args = ["lualatex", "--shell-escape", temp_file, "-output-directory", temp_dir]
        subprocess.run(
            subprocess_args,
            cwd=temp_dir,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=env,
        )
        
        pdf_file = os.path.join(temp_dir, 'recipe.pdf')
        with open(pdf_file, 'rb') as f:
            return f.read()
