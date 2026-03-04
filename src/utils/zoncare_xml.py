import xml.etree.ElementTree as ET


def parse_zoncare_xml(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    patient = root.find("patient")
    measure = root.find("measure")
    result = root.find("result")
    base = root.find("base")

    return {
        "base": {
            "device_id": base.findtext("device_id"),
            "time": base.findtext("time"),
        },
        "patient": {
            "external_id": patient.findtext("id"),
            "name": patient.findtext("name"),
            "age": patient.findtext("age"),
            "age_unit": patient.findtext("ageUnit"),
            "gender": patient.findtext("gender"),
            "department": patient.findtext("department"),
            "bed": patient.findtext("bedNo"),
            "weight": patient.findtext("weight"),
            "height": patient.findtext("height"),
        },
        "measures": {
            "hr": int(measure.findtext("hr", 0)),
        },
        "report": {
            "diagnosis": result.findtext("diagnosis"),
            "advicetext": result.findtext("advicetext"),
        }
    }