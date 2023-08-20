from xml.dom import minidom
import sys

def format_xml(input_xml):
    doc = minidom.parseString(input_xml)
    formatted_xml = doc.toprettyxml(indent="    ")
    return formatted_xml

if __name__ == "__main__":
    input_xml = sys.stdin.read()
    formatted_xml = format_xml(input_xml)
    sys.stdout.write(formatted_xml)
