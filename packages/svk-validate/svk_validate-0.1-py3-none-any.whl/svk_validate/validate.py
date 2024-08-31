from saxonche import PySaxonProcessor
from lxml import etree
import tempfile
from pathlib import Path
import os
from datetime import datetime

class ErmsValidator:

    # ERMS-SVK versions:
    ERMS_SVK_ARENDE_1 = "ERMS-SVK-ARENDE-1.0"

    # Namespaces applied:
    ERMS_NAMESPACE = "https://DILCIS.eu/XML/ERMS"
    ERMS = "{%s}" % ERMS_NAMESPACE
    SVK_NAMESPACE = "https://xml.svenskakyrkan.se/ERMS-SVK-ARENDE"
    SVK = "{%s}" % SVK_NAMESPACE

    # Class properties
    xml_file = None
    xml_tree = None
    erms_element = None
    erms_svk_version = None
    erms_schema_files = None
    erms_svk_schema_files = None
    app_path = os.path.dirname(__file__)

    def __init__(self, path_to_xml_file: str):

        self.xml_file = Path(path_to_xml_file)

        if not self.xml_file.is_file():
            raise Exception(f"'{path_to_xml_file}' is not a file.")

        try:
            self.xml_tree = etree.parse(self.xml_file)
        except etree.XMLSyntaxError:
            raise Exception(f"'{path_to_xml_file}' is not a valid XML-file.")

        self.erms_element = self.xml_tree.getroot()
        self.erms_svk_version = self.erms_element.find(".//" + self.SVK + "ermsSvkArende").get("schemaVersion")

        if not self.erms_svk_version:
            raise Exception(f"'{path_to_xml_file}' has no information about  the version of the ERMS-SVK document.")



        if self.erms_svk_version == self.ERMS_SVK_ARENDE_1:
            erms_dir = Path(self.app_path, "schemata", "erms-3-0-0")

            self.erms_schema_files = {
                "xsd": Path(erms_dir).joinpath("ERMS_v3.xsd"),
                "sch": str(Path(erms_dir).joinpath("erms_v3.sch")),
                "sch_compiled": str(Path(erms_dir).joinpath("erms_v3_sch_compiled.xsl")),
            }

            erms_svk_dir = Path(self.app_path, "schemata", "erms-svk-1-0")
            self.erms_svk_schema_files = {
                "xsd": str(Path(erms_svk_dir).joinpath("ERMS-SVK-ARENDE.xsd")),
                "xsd_element": str(Path(erms_svk_dir).joinpath("ERMS-SVK-element.xsd")),
                "sch": str(Path(erms_svk_dir).joinpath("ERMS-SVK-ARENDE.sch")),
                "sch_compiled": str(Path(erms_svk_dir).joinpath("erms_svk_1_0_sch_compiled.xsl")),
            }
        else:
            raise Exception(f"There are no schema files for version '{self.erms_svk_version}'")

    def xml_validate(self, schema="erms"):
        if schema == "erms":
            xmlschema_doc = etree.parse(self.erms_schema_files['xsd'])

        elif schema == "erms-svk-arende":
            xmlschema_doc = etree.parse(self.erms_svk_schema_files['xsd'])

        else:
            raise Exception(f"'{schema}' is not a valid argument.")

        xmlschema = etree.XMLSchema(xmlschema_doc)
        xmlschema.validate(self.xml_tree)
        log = xmlschema.error_log
        if len(log) > 0:
            message = f"Line {log[0].line}: {log[0].message}"
            return {"is_valid": False, "message": message}
        else:
            return {"is_valid": True, "message": "Document is valid"}


    def schematron_validate(self):

        schematron_xls = str(Path(self.app_path, "schxslt-1.10/2.0/pipeline-for-svrl.xsl"))

        with PySaxonProcessor(license=False) as proc:

            erms_output_file = tempfile.NamedTemporaryFile(suffix=".xml")
            erms_svk_output_file = tempfile.NamedTemporaryFile(suffix=".xml")

            xslt30_processor = proc.new_xslt30_processor()
            xslt30_processor.set_cwd(".")

            # Compile ERMS-standard
            xslt30_processor.transform_to_file(source_file=self.erms_schema_files['sch'],
                                               stylesheet_file=schematron_xls,
                                               output_file=self.erms_schema_files['sch_compiled'])

            # Get ERMS-standard result
            xslt30_processor.transform_to_file(source_file=str(self.xml_file),
                                               stylesheet_file=self.erms_schema_files['sch_compiled'],
                                               output_file=erms_output_file.name)

            # Compile ERMS-SVK
            xslt30_processor.transform_to_file(source_file=self.erms_svk_schema_files['sch'],
                                               stylesheet_file=schematron_xls,
                                               output_file=self.erms_svk_schema_files['sch_compiled'])

            # Get ERMS-SVK result
            xslt30_processor.transform_to_file(source_file=str(self.xml_file),
                                               stylesheet_file=self.erms_svk_schema_files['sch_compiled'],
                                               output_file=erms_svk_output_file.name)

        tree = etree.parse(erms_output_file.name)
        root = tree.getroot()
        supressed_rules = [ elm.get("context") for elm in root.iterfind(".//{http://purl.oclc.org/dsdl/svrl}suppressed-rule") ]
        validation_errors = [{"location": elm.get("location"), "test": elm.get("test"), "text": elm[0].text}
                             for elm in root.iterfind(".//{http://purl.oclc.org/dsdl/svrl}failed-assert")]
        erms = {"supressed_rules": supressed_rules, "validation_errors": validation_errors}

        tree = etree.parse(erms_svk_output_file.name)
        root = tree.getroot()
        supressed_rules = [elm.get("context") for elm in
                           root.iterfind(".//{http://purl.oclc.org/dsdl/svrl}suppressed-rule")]
        validation_errors = [{"location": elm.get("location"), "test": elm.get("test"), "text": elm[0].text}
                             for elm in root.iterfind(".//{http://purl.oclc.org/dsdl/svrl}failed-assert")]
        erms_svk = {"supressed_rules": supressed_rules, "validation_errors": validation_errors}

        if erms['validation_errors'] or erms_svk['validation_errors']:
            is_valid = False
        else:
            is_valid = True

        return {"is_valid": is_valid, "erms": erms, "erms_svk": erms_svk}

    def validate(self, logfile):
        erms_log = self.xml_validate("erms")
        erms_svk_log = self.xml_validate("erms-svk-arende")
        sch_log = self.schematron_validate()

        log_file = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")

        if logfile:
            with open(log_file, 'w') as f:
                f.write(erms_log["message"] + "\n")
                f.write(erms_svk_log["message"] + "\n")
                for entry in sch_log["erms"]["validation_errors"]:
                    f.write(entry["text"] + "\n")
                for entry in sch_log["erms_svk"]["validation_errors"]:
                    f.write(entry["text"] + "\n")

        print(f"Validating {self.xml_file}:")
        print(f"Is valid ERMS: {erms_log['is_valid']}")
        print(f"Is valid ERMS-SVK: {erms_svk_log['is_valid']}")
        print(f"Schematron is valid: {sch_log['is_valid']}")

# val = ErmsValidator("../xml-files/erms_07.xml")
# val.validate()