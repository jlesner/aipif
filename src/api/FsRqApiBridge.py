import hashlib
import sys
import os
import re
import traceback
from lxml import etree

from common.ContextAware import ContextAware 

class FsRqApiBridge(ContextAware):

    def __init__(self, queue_dir: str = '_queue'):
        self.queue_dir = queue_dir
        if not os.path.exists(self.queue_dir):
            os.makedirs(self.queue_dir)

    def _queue_filepath(self, hash_value: str) -> str:
        return os.path.join(self.queue_dir, hash_value)

    def address_requests(self, input_file, output_file):
        tree = etree.parse(input_file)
        for request_node in tree.xpath("//request"):
            try:
                response_node = self._process_request(request_node)
            except Exception as e:
                error_message = str(e)
                stack_trace = traceback.format_exc()  # Get the formatted stack trace as a string
                error_node = etree.fromstring(f"<error><![CDATA[{error_message}\n\n{stack_trace}]]></error>")
                request_node.append(error_node)
                continue
            request_parent = request_node.getparent()
            request_parent.replace(request_node, response_node)
        tree.write(output_file, pretty_print=True)

    def _process_request(self, request_node):
        request_type = request_node.get("type")
        request_str = etree.tostring(request_node, encoding='unicode', pretty_print=True)
        request_hash = hashlib.sha256(request_str.encode()).hexdigest()
        rq_id = request_hash[:8]
        
        filepath = self._queue_filepath(request_type + "-" + rq_id)
        request_fp = filepath + "-req.xml"
        # response_fp = filepath + "-res.xml"
        response_node =  etree.fromstring(f'<rq id="{rq_id}"/>')

        with open(request_fp, 'w') as file:
            request_node.append(response_node)
            request_str = etree.tostring(request_node, encoding='unicode', pretty_print=True)    
            file.write("<queue>\n" + request_str + "</queue>\n")

        return response_node

if __name__ == "__main__":
    FsRqApiBridge().address_requests("/dev/stdin", "/dev/stdout")
    