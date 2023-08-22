# read xml from stdin
# find all request nodes that do not have a response child
# issue request to api
# attach as a child the response to its request node
# output xml to stdout

import sys
import re
from lxml import etree

from Context import Context 
from pictures.StubPictureMaker import StubPictureMaker
from text.StubTextMaker import StubTextMaker


def context_configure(context:Context):
    # if your module needs to be configured, you can do it here
    # eventually we will have a config file and/or command line args
    #
    # WARNING: DO NOT CHECKIN YOUR API KEYS / SECRETS
    #
    context.config['story_maker_port'] = 8080
    context.config['make_text_attempts'] = 3
    

def state_setup(context:Context):
    # for now we hardcode function bindings
    context.state['picture_maker'] = StubPictureMaker(context)
    context.state['text_maker'] = StubTextMaker(context)


def address_requests(context, input_file, output_file): # manager thread
    tree = etree.parse(input_xml)
    request_nodes = tree.xpath("//request")
    for request_node in request_nodes:
        process_request(context,request_node)
    tree.write(output_file, pretty_print=True)


def process_request(context, request_node):  # worker thread
    request_type = request_node.get("type")
    match request_type:
        case "make_text":
            attempts_left = context.config['make_text_attempts']
            while(True):
                positive_prompt_text = request_node.find('positive_prompt_text').text
                response_text = ({"positive_prompt_text": positive_prompt_text})
                response_string_xml = extract_xml(response_text)
                if valid_xml(response_string_xml):
                    break
                attempts_left -= 1
                if attempts_left <= 0:
                    raise Exception("Unable to generate valid xml response")
        case _:
            raise Exception(f"Unknown request type: {request_type}")

def extract_xml(input_string):
    match = re.search(r'<scene .*?</scene>', input_string, re.DOTALL)
    if match:
        return match.group()
    else:
        raise Exception("No xml found in input string")
    
def valid_xml(input_file):
    try:
        input_tree = etree.parse(input_file)
        expressions = [
            # not sure what to put here yet
        ]
        for expr in expressions:
            if not input_tree.xpath(expr):
                return (False, None)
        return (True, input_tree)
    except etree.XMLSyntaxError:
        return (False, input_tree)

if __name__ == "__main__":
    context = Context() 
    context_configure(context)
    state_setup(context)
    input_xml = 'story/_generated/p00311_response_simulate.xml'
    address_requests(context, input_xml, "/dev/stdout")
    