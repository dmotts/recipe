import logging
import requests
from flask import render_template, send_file, jsonify
from pathlib import Path
from config import Config

logger = logging.getLogger(__name__)

class PDFGenerator:
    """
    PDFGenerator is responsible for converting HTML content to a PDF using the PDF.co API.
    It reads external CSS, injects it into the HTML, and generates a PDF.

    Attributes:
        api_key (str): The API key for PDF.co.
        css_path (str): The file path to the external CSS file.
    """

    def __init__(self):
        """
        Initializes the PDFGenerator with configuration values.
        """
        self.api_key = Config.API_KEY
        self.css_path = Config.CSS_PATH
        logger.info("PDFGenerator initialized with API key and CSS path.")

    def inject_css(self, html_content):
        """
        Injects CSS styles from the external stylesheet into the provided HTML content.

        Args:
            html_content (str): The HTML content as a string.

        Returns:
            str: The HTML content with embedded CSS.
        """
        logger.debug("Injecting CSS into HTML content.")
        css_content = self.read_css()
        head_end_index = html_content.find('</head>')
        if head_end_index == -1:
            logger.error("Invalid HTML content: Missing </head> tag.")
            raise ValueError("Invalid HTML content: Missing </head> tag.")

        # Inject CSS before the closing head tag
        html_with_css = html_content[:head_end_index] + f"<style>{css_content}</style>" + html_content[head_end_index:]
        logger.debug("CSS successfully injected into HTML.")
        return html_with_css

    def read_css(self):
        """
        Reads the CSS content from the file specified by css_path.

        Returns:
            str: The contents of the CSS file.
        """
        logger.debug(f"Reading CSS from {self.css_path}.")
        try:
            with open(self.css_path, 'r') as css_file:
                css_content = css_file.read()
                logger.debug("CSS file read successfully.")
                return css_content
        except FileNotFoundError:
            logger.error(f"CSS file not found: {self.css_path}")
            raise FileNotFoundError(f"CSS file not found: {self.css_path}")

    def generate_pdf(self, html_template, output_filename):
        """
        Generates a PDF from the HTML template by injecting CSS and converting it using PDF.co.

        Args:
            html_template (str): The name of the HTML template file.
            output_filename (str): The name of the output PDF file.

        Returns:
            Response: Flask response object containing the PDF file.
        """
        if not Config.ENABLE_PDF_DOWNLOAD:
            logger.warning("PDF download is disabled by configuration.")
            return jsonify({"error": "PDF download is disabled"}), 403

        logger.info(f"Generating PDF for template: {html_template}")
        try:
            html_content = self.get_html(html_template)
            html_with_css = self.inject_css(html_content)
            pdf_content = self.convert_html_to_pdf(html_with_css)
            logger.info("PDF generation successful.")
            return self.save_pdf(pdf_content, output_filename)
        except Exception as e:
            logger.error(f"Failed to generate PDF: {str(e)}")
            return jsonify({"error": "Failed to generate PDF"}), 500

    def get_html(self, template_name):
        """
        Renders the HTML template using Flask's render_template function.

        Args:
            template_name (str): The name of the HTML template file.

        Returns:
            str: Rendered HTML content.
        """
        logger.debug(f"Rendering HTML template: {template_name}")
        try:
            html_content = render_template(template_name)
            logger.debug("HTML template rendered successfully.")
            return html_content
        except Exception as e:
            logger.error(f"Failed to render HTML template: {str(e)}")
            raise

    def convert_html_to_pdf(self, html_content):
        """
        Converts HTML content to PDF using the PDF.co API.

        Args:
            html_content (str): The HTML content with embedded CSS.

        Returns:
            bytes: The binary content of the generated PDF.
        """
        logger.debug("Converting HTML to PDF using PDF.co API.")
        url = "https://api.pdf.co/v1/pdf/convert/from/html"
        headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "html": html_content,
            "name": "output.pdf"
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            pdf_url = response.json().get("url")
            logger.debug("PDF generated successfully, retrieving content.")
            return requests.get(pdf_url).content
        else:
            logger.error(f"Failed to generate PDF: {response.text}")
            raise RuntimeError(f"Failed to generate PDF: {response.text}")

    def save_pdf(self, pdf_content, output_filename):
        """
        Saves the PDF content to a file and returns a Flask response for download.

        Args:
            pdf_content (bytes): The binary content of the PDF.
            output_filename (str): The name of the output PDF file.

        Returns:
            Response: Flask response object containing the PDF file.
        """
        output_path = Path(output_filename)
        output_path.write_bytes(pdf_content)
        logger.info(f"PDF saved to {output_filename}.")
        return send_file(output_path, as_attachment=True, download_name=output_filename)
