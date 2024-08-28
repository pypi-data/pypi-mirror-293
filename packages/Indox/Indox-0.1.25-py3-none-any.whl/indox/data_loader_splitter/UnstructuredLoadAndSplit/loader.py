import importlib
from loguru import logger
import sys

from indox.data_loaders.utils import convert_latex_to_md

# Set up logging
logger.remove()  # Remove the default logger
logger.add(sys.stdout,
           format="<green>{level}</green>: <level>{message}</level>",
           level="INFO")

logger.add(sys.stdout,
           format="<red>{level}</red>: <level>{message}</level>",
           level="ERROR")


def import_unstructured_partition(content_type):
    # Import appropriate partition function from the `unstructured` library
    module_name = f"unstructured.partition.{content_type}"
    module = importlib.import_module(module_name)
    partition_function_name = f"partition_{content_type}"
    prt = getattr(module, partition_function_name)
    return prt


def create_documents_unstructured(file_path):
    try:
        if file_path.lower().endswith(".pdf"):
            # Partition PDF with a high-resolution strategy
            from unstructured.partition.pdf import partition_pdf
            elements = partition_pdf(
                filename=file_path,
                strategy="hi_res",
                # infer_table_structure=True,
            )
            # Remove "References" and header elements
            reference_title = [
                el for el in elements
                if el.text == "References" and el.category == "Title"
            ][0]
            references_id = reference_title.id
            elements = [el for el in elements if el.metadata.parent_id != references_id]
            elements = [el for el in elements if el.category != "Header"]
        elif file_path.lower().endswith(".xlsx"):
            from unstructured.partition.xlsx import partition_xlsx
            elements_ = partition_xlsx(filename=file_path)
            elements = [el for el in elements_ if el.metadata.text_as_html is not None]
        elif file_path.lower().startswith("www") or file_path.lower().startswith("http"):
            from unstructured.partition.html import partition_html
            elements = partition_html(url=file_path)
        else:
            if file_path.lower().endswith(".tex"):
                file_path = convert_latex_to_md(latex_path=file_path)
            content_type = file_path.lower().split(".")[-1]
            if content_type == "txt":
                prt = import_unstructured_partition(content_type="text")
            else:
                prt = import_unstructured_partition(content_type=content_type)
            elements = prt(filename=file_path)
        return elements
    except AttributeError as ae:
        logger.error(f"Attribute error: {ae}")
        return ae
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return e
