import os
import time

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from .database import connect_and_get_word_list


def generate_pdf(word_list: list, output_path: str | os.PathLike,
                 page_size=A4, font="Helvetica-Oblique", font_size: int = 14, max_lines: int = 45):
    """
    generates pdf with list of words in word_list
    :param word_list: list of words to be printed in pdf
    :param output_path: path to output
    :param page_size: size of pdf page
    :param font: font of text
    :param font_size: size of text
    :param max_lines: maximum no of words in single page
    :return:
    """
    start_time = time.time()
    c = canvas.Canvas(output_path, pagesize=page_size)

    current_line = 0
    max_lines_per_page = max_lines

    text_object = c.beginText(50, 800)
    text_object.setFont(font, font_size)

    for word in word_list:

        text_object.textLine(word)
        current_line += 1
        if current_line >= max_lines_per_page:
            c.drawText(text_object)
            c.showPage()
            text_object = c.beginText(50, 800)
            text_object.setFont(font, 14)
            current_line = 0

    c.drawText(text_object)
    c.showPage()
    c.save()
    end_time = time.time()
    generated_time = end_time - start_time

    # Calculate file size
    file_size = os.path.getsize(output_path) / (1024)

    print("PDF file generated successfully.")
    print(f"File size: {file_size:.2f} KB")
    print(f"Generated time: {generated_time:.2f} seconds")


def apply_pdf_pipeline(database_config, pdf_config):
    """
    Creates pdf of words from word list fetched from database
    :param database_config: configuration for database
    :param pdf_config: configuration for pdf
    :return:
    """
    db_name = database_config['database_name']
    table_name = database_config['table_name']

    output_path = pdf_config["output_path"]
    font = pdf_config["font"]
    font_size = float(pdf_config["font_size"])
    max_lines = int(pdf_config["max_lines"])

    word_list = connect_and_get_word_list(db_name, table_name)
    generate_pdf(word_list, output_path, font=font, font_size=font_size, max_lines=max_lines)
