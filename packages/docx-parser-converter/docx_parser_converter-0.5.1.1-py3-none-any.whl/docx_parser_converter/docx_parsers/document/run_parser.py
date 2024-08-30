from lxml import etree
from typing import List
from docx_parser_converter.docx_parsers.helpers.common_helpers import extract_element, NAMESPACE_URI
from docx_parser_converter.docx_parsers.models.paragraph_models import Run, RunContent, TextContent, TabContent
from docx_parser_converter.docx_parsers.models.styles_models import RunStyleProperties
from docx_parser_converter.docx_parsers.styles.run_properties_parser import RunPropertiesParser

class RunParser:
    """
    A parser for extracting run elements from the DOCX document structure.

    This class handles the extraction of run properties and contents within a 
    run element, converting them into a structured Run object for further 
    processing or conversion to other formats like HTML.
    """

    def parse(self, r: etree.Element) -> Run:
        """
        Parses a run from the given XML element.

        Args:
            r (etree.Element): The run XML element.

        Returns:
            Run: The parsed run.

        Example:
            The following is an example of a run element in a document.xml file:

            .. code-block:: xml

                <w:r>
                    <w:rPr>
                        <w:b/>
                        <w:color w:val="FF0000"/>
                    </w:rPr>
                    <w:t>Example text</w:t>
                </w:r>
        """
        rPr = extract_element(r, ".//w:rPr")
        run_properties = RunPropertiesParser().parse(rPr) if rPr else RunStyleProperties()
        contents = self.extract_run_contents(r)
        return Run(contents=contents, properties=run_properties)

    def extract_run_contents(self, r: etree.Element) -> List[RunContent]:
        """
        Extracts run contents from the given run XML element.

        Args:
            r (etree.Element): The run XML element.

        Returns:
            List[RunContent]: The list of extracted run contents.

        Example:
            The following is an example of run contents in a document.xml file:

            .. code-block:: xml

                <w:r>
                    <w:tab/>
                    <w:t>Example text</w:t>
                </w:r>
        """
        contents = []
        for elem in r:
            if elem.tag == f"{{{NAMESPACE_URI}}}tab":
                contents.append(RunContent(run=TabContent()))
            elif elem.tag == f"{{{NAMESPACE_URI}}}t":
                contents.append(RunContent(run=TextContent(text=elem.text)))
        return contents
