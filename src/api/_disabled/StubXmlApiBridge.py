import sys
import re
from lxml import etree

from common.Context import Context 
from pictures.StubPictureMaker import StubPictureMaker
from text.DelayedTextMaker import DelayedTextMaker
from text.StubTextMaker import StubTextMaker

def context_configure(context:Context):
    context.config['story_maker_port'] = 8080
    context.config['make_text_attempts'] = 3

def state_setup(context:Context):
    # for now we hardcode function bindings
    context.state['picture_maker'] = StubPictureMaker(context)
    context.state['text_maker'] = StubTextMaker(context)

def address_requests(context, input_file, output_file): # manager thread
    tree = etree.parse(input_file)
    request_nodes = tree.xpath("//request")
    for request_node in request_nodes:
        response_node = process_request(context, request_node)
        request_parent = request_node.getparent()
        request_parent.replace(request_node, response_node)
    tree.write(output_file, pretty_print=True)


def process_request(context, request_node):  # worker thread
    request_type = request_node.get("type")
    match request_type:
        case "make_text":
            attempts_left = context.config['make_text_attempts']
            while(True):
                positive_prompt_text = request_node.find('positive_prompt_text').text
                prompt_dict = ({"positive_prompt_text": positive_prompt_text})
                print(f"calling make_text()... attempts left {attempts_left}",file=sys.stderr)
                response_string= context.state['text_maker'].make_text(prompt_dict)
                response_string_xml = extract_xml(response_string)
                if valid_xml(response_string_xml):
                    break
                attempts_left -= 1
                if attempts_left <= 0:
                    raise Exception("Ran out of attempts to generate valid xml response")
                
            return etree.fromstring(response_string_xml)
        case _:
            raise Exception(f"Unknown request type: {request_type}")

def extract_xml(input_string):
    match = re.search(r'<scene .*?</scene>', input_string, re.DOTALL)
    if match:
        return match.group()
    else:
        raise Exception("No xml found in input string")
    
def valid_xml(input_string):
    try:
        input_tree = etree.fromstring(input_string)
        expressions = [
                "/scene/@name",
                "/scene/@act",
                "/scene/@part",
                "/scene/@branch_count",
                "/scene/@index",
                # "/scene/@key", # TODO: enable once there is key gen
                "/scene/setting",
                "/scene/introduction",
                "/scene/dialogue",
                "/scene/illustration",
                "/scene/illustration_title",
                "/scene/sound",
                "/scene/music",
        ]
        for expr in expressions:
            if not input_tree.xpath(expr):
                return False
        return True
    except etree.XMLSyntaxError:
        return False

if __name__ == "__main__":
    context = Context() 
    context_configure(context)
    state_setup(context)
    address_requests(context, "/dev/stdin", "/dev/stdout")
    