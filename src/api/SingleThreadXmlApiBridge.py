import sys
import re
import traceback
from lxml import etree

from common.Context import Context
from pictures.StubPictureMaker import StubPictureMaker
from text.CachingTextMaker import CachingTextMaker
from text.DelayedTextMaker import DelayedTextMaker
from text.Gpt35TextMaker import Gpt35TextMaker
from text.Gpt4t8kTextMaker import Gpt4t8kTextMaker
from text.StubTextMaker import StubTextMaker

def context_configure(context:Context):
    # context.config['story_maker_port'] = 8080
    context.config['make_text_attempts'] = 3

def state_setup(context:Context):
    # for now we hardcode function bindings
    # context.state['picture_maker'] = StubPictureMaker(context)
    # context.state['text_maker'] = StubTextMaker(context)
    # context.state['picture_maker'] = StubPictureMaker(context)
    context.state['text_maker'] = CachingTextMaker(Gpt35TextMaker(context))
    # context.state['text_maker'] = CachingTextMaker(Gpt4t8kTextMaker(context))

def address_requests(context, input_file, output_file): # manager thread
    tree = etree.parse(input_file)
    request_nodes = tree.xpath("//request")
    for request_node in request_nodes:
        try:
            response_node = process_request(context, request_node)
        except Exception as e:
            error_message = str(e)
            stack_trace = traceback.format_exc()  # Get the formatted stack trace as a string
            error_node = etree.fromstring(f"<error><![CDATA[{error_message}\n\n{stack_trace}]]></error>")
            request_node.append(error_node)
            continue
        request_parent = request_node.getparent()
        request_parent.replace(request_node, response_node)
    tree.write(output_file, pretty_print=True)

def children_to_string(node):
    return " ".join([etree.tostring(child, encoding='unicode') for child in node])

def process_request(context, request_node):  # worker thread
    request_type = request_node.get("type")
    match request_type:
        case "make_text":
            attempts_left = context.config['make_text_attempts']
            response_string = ""
            while(True):
                attempts_left -= 1
                if attempts_left < 0:
                    raise Exception(f"process_request(): Ran out of attempts to get valid xml response. Last response_string: {response_string}")
                positive_prompt_text = request_node.find('positive_prompt_text').text
                positive_prompt_text += " " + children_to_string(request_node.find('positive_prompt_text'))
                positive_prompt_text = re.sub(r'\s+|\n', ' ', positive_prompt_text)
                prompt_dict = ({"positive_prompt_text": positive_prompt_text + " "*attempts_left })
                # print(f"\n\nprompt_dict:{prompt_dict}",file=sys.stderr)
                response_string= context.state['text_maker'].make_text(prompt_dict)
                # print(f"\n\nresponse_string:{response_string}",file=sys.stderr)
                try:
                    response_string_xml = extract_xml(response_string)
                    if valid_xml(response_string_xml):
                        break
                except Exception as e:
                    continue

            return etree.fromstring(response_string_xml)
        case _:
            raise Exception(f"unsupported request_type: {request_type}")

def extract_xml(input_string):
    match = re.search(r'<scene .*?</scene>', input_string, re.DOTALL)
    if match:
        return match.group()
    else:
        raise Exception(f"\nextract_xml() failed to find XML in:\n{input_string}\n")

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
                # "/scene/setting",
                "/scene/introduction",
                "count(/scene/dialogue)=1",
                "/scene/illustration",
                # "/scene/illustration_title",
                "/scene/sound",
                "/scene/music"
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
