import sys
import re
from lxml import etree

from common.Context import Context
from pictures.FastLocalSdPictureMaker import FastLocalSdPictureMaker
from pictures.LocalSdPictureMaker import LocalSdPictureMaker 
from pictures.StubPictureMaker import StubPictureMaker
from text.CachingTextMaker import CachingTextMaker
from text.DelayedTextMaker import DelayedTextMaker
from text.Gpt35TextMaker import Gpt35TextMaker
from text.Gpt4t8kTextMaker import Gpt4t8kTextMaker
from text.StubTextMaker import StubTextMaker

def context_configure(context:Context):
    # context.config['story_maker_port'] = 8080
    # context.config['make_text_attempts'] = 3
    pass    

def state_setup(context:Context):
    # for now we hardcode bindings
    context.state['picture_maker'] = StubPictureMaker(context)
    context.state['picture_maker'] = FastLocalSdPictureMaker(context)
    # context.state['picture_maker'] = LocalSdPictureMaker(context)
    # context.state['text_maker'] = CachingTextMaker(Gpt35TextMaker(context))
    # context.state['text_maker'] = CachingTextMaker(Gpt4t8kTextMaker(context))
    pass

def address_requests(context, input_file, output_file): # manager thread
    tree = etree.parse(input_file)
    request_nodes = tree.xpath("//request")
    for request_node in request_nodes:
        try:
            response_node = process_request(context, request_node)
        except Exception as e:
            error_node = etree.fromstring(f"<error><![CDATA[{e}]]></error>")
            request_node.append(error_node)
            continue
        request_parent = request_node.getparent()
        request_parent.replace(request_node, response_node)
    tree.write(output_file, pretty_print=True)

def children_to_string(node):
    return " ".join([etree.tostring(child, encoding='unicode') for child in node])

def process_request(context, request_node):
    request_type = request_node.get("type")

    prompt_dict = {
        "positive_prompt_text" : request_node.find('positive_prompt_text').text,
        "negative_prompt_text" : request_node.find('negative_prompt_text').text,
        "style_prompt_text" : request_node.find('style_prompt_text').text,
        "rq_id" : request_node.find("rq").attrib['id'],
    }
    
    match request_type:
        case "make_picture":
                response_string = context.state['picture_maker'].make_picture(prompt_dict)
                return etree.fromstring("<url>" + response_string + "</url>")
        case _:
            raise Exception(f"unsupported request_type: {request_type}")

if __name__ == "__main__":
    context = Context() 
    context_configure(context)
    state_setup(context)
    address_requests(context, "/dev/stdin", "/dev/stdout")
    