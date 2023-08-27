import hashlib
import sys
import os
import re
import traceback
import boto3
from lxml import etree

from common.ContextAware import ContextAware 

class S3RqApiBridge(ContextAware):

    def __init__(self, queue_path:str="_queue", bucket_name:str='aipif-2023'):
        self._queue_path = queue_path
        self._bucket_name = bucket_name
        self._s3_client = boto3.client('s3')

    def _queue_filepath(self, hash_value: str) -> str:
        return self._queue_path + "/" +  hash_value

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
        request_key = filepath + "-req.xml"
        # response_fp = filepath + "-res.xml"
        response_node =  etree.fromstring(f'<rq id="{rq_id}"/>')
        request_node.append(response_node)
        request_str = etree.tostring(request_node, encoding='unicode', pretty_print=True)    
        s3_request_body = "<queue>\n" + request_str + "\n</queue>\n"
        self._s3_client.put_object(Bucket=self._bucket_name, Key=request_key, Body=s3_request_body)

        return response_node

if __name__ == "__main__":
    S3RqApiBridge().address_requests("/dev/stdin", "/dev/stdout")
    

