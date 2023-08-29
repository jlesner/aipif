import sys
import re
import time
import random
import threading
from lxml import etree

from common.Context import Context
from common.BoundedBuffer import BoundedBuffer
from pictures.StubPictureMaker import StubPictureMaker
from text.CachingTextMaker import CachingTextMaker
from text.DelayedTextMaker import DelayedTextMaker
from text.Gpt35TextMaker import Gpt35TextMaker
from text.StubTextMaker import StubTextMaker


class Task:
    def __init__(self, request_node=None):
        self.request_node = request_node
        self.response_node = None


def context_configure(context:Context):
    # if your module needs to be configured, you can do it here
    # eventually we will have a config file and/or command line args
    #
    # WARNING: DO NOT CHECKIN YOUR API KEYS / SECRETS
    #
    context.config['story_maker_port'] = 8080
    context.config['num_workers'] = 8
    context.config['sentinel'] = "STOP"
    context.config['make_text_attempts'] = 4


def state_setup(context:Context):
    # for now we hardcode function bindings
    context.state['todo_tasks'] = BoundedBuffer(128)
    context.state['done_tasks'] = BoundedBuffer(128)

    # context.state['picture_maker'] = StubPictureMaker(context)
    context.state['text_maker'] = CachingTextMaker(Gpt35TextMaker(context))


def address_requests(context, input_file, output_file): # manager thread
    tree = etree.parse(input_file)
    request_nodes = tree.xpath("//request")
    for request_node in request_nodes:
        task = Task(request_node)
        context.state['todo_tasks'].add(task)
        print(f"Manager producing {task.request_node.get('type')}",file=sys.stderr)
        time.sleep(random.random())
    print(f"Manager gathering done tasks! {len(request_nodes)} tasks",file=sys.stderr)
    context.state['todo_tasks'].add(context.config['sentinel'])
    while(True):
        if context.state['done_tasks'].count == len(request_nodes):
            break
        # print(f"Manager waiting for done tasks! {context.state['done_tasks'].size()} tasks",file=sys.stderr)
        time.sleep(0.1)
    print("Manager building new xml tree",file=sys.stderr)
    while context.state['done_tasks'].count > 0:
        item = context.state['done_tasks'].remove()
        request_node = item.request_node
        response_node = item.response_node
        request_parent = request_node.getparent()
        request_parent.replace(request_node, response_node)

    tree.write(output_file, pretty_print=True)

def children_to_string(node):
    return " ".join([etree.tostring(child, encoding='unicode') for child in node])

def process_request(context, id):  # worker thread
    while True:
        item = context.state['todo_tasks'].remove()
        if item == context.config['sentinel']:
            context.state['todo_tasks'].add(item)
            print(f"Worker {id} received termination signal",file=sys.stderr)
            break
        else:
            request_node = item.request_node
            request_type = request_node.get("type")
            try:
                match request_type:
                    case "make_text":
                        attempts_left = context.config['make_text_attempts']
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
                                time.sleep(random.random()*2)
                            except Exception as e:
                                continue

                        item.response_node = etree.fromstring(response_string_xml)
                        context.state['done_tasks'].add(item)
                    case _:
                        raise Exception(f"unsupported request_type: {request_type}")
            except Exception as e:
                print(f"Worker {id} encountered error: {e}",file=sys.stderr)
                item.response_node = etree.fromstring(f"<error>{e}</error>")
                context.state['done_tasks'].add(item)
                continue

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
    manager_thread = threading.Thread(target=address_requests, args=(context,"/dev/stdin","/dev/stdout"))
    manager_thread.start()

    worker_threads = []
    for i in range(context.config['num_workers']):
        worker_thread = threading.Thread(target=process_request, args=(context,i))
        worker_thread.start()
        worker_threads.append(worker_thread)

    for worker_thread in worker_threads:
        worker_thread.join()

    manager_thread.join()