# read xml from stdin
# find all request nodes that do not have a response child
# issue request to api
# attach as a child the response to its request node
# output xml to stdout

import sys
from lxml import etree

from Context import Context # ! don't know why it can't import when in /story !
from pictures.StubPictureMaker import StubPictureMaker

context = Context() # empty since no configuration is needed for StubPictureMaker

picture_maker = StubPictureMaker(context)

def address_requests(input_file, output_file):
    tree = etree.parse(input_xml)
    request_nodes = tree.xpath("//request[not(response)]")
    
    for request_node in request_nodes:
        request_type = request_node.get("type")
        match request_type:
            case "make_picture":
                positive_prompt_text = request_node.find('arg[@type="positive_prompt_text"]').text
                print(f"positive_prompt_text: {positive_prompt_text}")
                response = picture_maker.make_picture({"positive_prompt_text": positive_prompt_text})
                response_node = etree.SubElement(request_node, "response")
                response_node.text = response
                break
            case _:
                raise Exception(f"Unknown request type: {request_type}")
    tree.write(output_file, pretty_print=True)


if __name__ == "__main__":
    # input_xml = sys.stdin.read()
    input_xml = sys.argv[1]
    # input_xml = "story/seeds/flat_structure.xml"
    address_requests(input_xml, "/dev/stdout")
    