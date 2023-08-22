# read xml from stdin
# find all request nodes that do not have a response child
# issue request to api
# attach as a child the response to its request node
# output xml to stdout

import sys
import re
from lxml import etree

from common.Context import Context 
from pictures.StubPictureMaker import StubPictureMaker
from text.StubTextMaker import StubTextMaker

context = Context() # empty since no configuration is needed for StubPictureMaker

picture_maker = StubPictureMaker(context)
text_maker = StubTextMaker(context)

def address_requests(input_file, output_file):
    tree = etree.parse(input_xml)
    request_nodes = tree.xpath("//request")
    
    for request_node in request_nodes:
        request_type = request_node.get("type")
        match request_type:
            case "make_text":
                positive_prompt_text = request_node.find('positive_prompt_text').text
                print(f"positive_prompt_text: {positive_prompt_text}")
                response = text_maker.make_text({"positive_prompt_text": positive_prompt_text})
                extract_xml(response)
                break
            case _:
                raise Exception(f"Unknown request type: {request_type}")
    tree.write(output_file, pretty_print=True)


def extract_xml(input_file, output_file):
    with open(input_file, "r") as f:
        content = f.read()
    match = re.search(r'\<\?xml version="1\.0" encoding="UTF-8"\?\>\s*<root>.*?</root>', content, re.DOTALL)
    if match:
        xml_content = match.group()
        with open(output_file, "w") as f:
            f.write(xml_content)
    else:
        raise Exception("No xml found in input file")
    
def valid_xml(input_file):
    try:
        input_tree = etree.parse(input_file)
        expressions = [
            # not sure what to put here yet
        ]
        for expr in expressions:
            if not input_tree.xpath(expr):
                return False
        return True
    except etree.XMLSyntaxError:
        return False

if __name__ == "__main__":
    # input_xml = sys.stdin.read()
    input_xml = 'story/_generated/p00311_response_simulate.xml'
    # input_xml = "story/seeds/flat_structure.xml"
    # address_requests(input_xml, "/dev/stdout")
    address_requests(input_xml, "/dev/stdout")
    