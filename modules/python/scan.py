from typing import Union
from urllib.parse import urlparse
from logging import getLogger
from core.libs import Http
from requests.models import Response
from yaml import safe_load
from secrets import token_bytes
from base64 import b64encode
import difflib
import re
import validators

PATH_PYTHON_MODULE = 'modules/python/'


class Scan:
    def __init__(self, opts: dict, http: Http, path: str = PATH_PYTHON_MODULE):
        self.opts = opts
        self.http = http
        self.path = path
        self.log = getLogger('scant3r')

    def open_yaml_file(self, file_name: str, add_path: bool):
        try:
            path = file_name
            if add_path is True:
                path = f'{self.path}{file_name}'
            return safe_load(open(path, 'r'))
        except Exception as e:
            self.log.error(e)
            return None

    def send_request(self,
                     method: str,
                     url: str,
                     second_url: Union[str, None] = None,
                     remove_content_type: bool = True,
                     body: Union[dict, None] = None) -> Response:

        if method == 'GET':
            return self.http.send(method, url, remove_content_type=remove_content_type)

        if second_url is not None:
            if body is not None:
                return self.http.send(method,
                                      second_url.split('?')[0],
                                      body=body,
                                      remove_content_type=remove_content_type)

            return self.http.send(method,
                                  second_url.split('?')[0],
                                  body=urlparse(url).query,
                                  remove_content_type=remove_content_type)

        if body is not None:
            return self.http.send(method,
                                  url.split('?')[0],
                                  body=body,
                                  remove_content_type=remove_content_type)

        return self.http.send(method,
                              url.split('?')[0],
                              body=urlparse(url).query,
                              remove_content_type=remove_content_type)

    def send_upload_file_request(self, url: str, files: dict, data: dict):
        return self.http.send(method='POST',
                              url=url,
                              body=data,
                              files=files,
                              remove_content_type=True)

    def transform_path_to_module_import(self, path: str) -> str:
        path = path.replace('/', '.').replace('\\', '.').strip()
        if path[-3:] == ".py":
            path = path[:-3]
        return path

    # simple function for out-of-band host
    def oob_host(self, key: str = None) -> dict:
        if key:  # for get resutls of host
            req = self.http.custom(url='https://odiss.eu:1337/events',
                                   headers={"Authorization": f"Secret {key}"})
            return req.json()['events'][0]
        else:  # for generate a new host
            key = b64encode(token_bytes(32)).decode()
            req = self.http.custom(url='https://odiss.eu:1337/events',
                                   headers={"Authorization": f"Secret {key}"})

            return {'host': req.json()['id'] + '.odiss.eu', 'key': key}

    # In some module if we have a # in the url it's doesn't work
    # Clean the url
    def transform_url(self, url: str) -> str:
        parse_url = urlparse(url)
        new_url = f'{parse_url.scheme}://{parse_url.netloc}{parse_url.path}'

        if parse_url.query:
            new_url += f'?{parse_url.query}'

        return new_url

    def get_lists_form(self, html_content: str) -> list:
        forms = []

        html_content = self.remove_comment_from_html(html_content)
        matches = re.findall(r'(?i)(?s)<form.*?</form.*?>', html_content)
        for match in matches:
            form = {
                "action": self.extract_action_from_html_form(match),
                "method": self.extract_method_from_html_form(match),
                "inputs": self.extract_inputs_from_html_form(match),
            }
            forms.append(form)

        return forms

    def remove_comment_from_html(self, html_content: str) -> str:
        """Remove comment from HTML

        Args:
            html_content (str): Html content with comments

        Returns:
            str: Html content without comments
        """
        return re.sub(r'(?s)<!--.*?-->', '', html_content)

    def extract_action_from_html_form(self, form_content: str) -> str:
        """Extract action from the html form.
        If action not url return the url of the web page

        Args:
            form_content (str): the html content of the form

        Returns:
            str: Action
        """
        action = re.search(r'(?i)action=[\'"](.*?)[\'"]', form_content)
        if action.group(1) not in ['#', '', '.']:
            return action.group(1)
        return self.opts['url']

    def extract_method_from_html_form(self, form_content: str) -> str:
        """Extract method from the html form.
        If no method return GET

        Args:
            form_content (str): The html content of the form

        Returns:
            str: the method
        """
        method = re.search(r'(?i)method=[\'"](.*?)[\'"]', form_content)
        if method:
            return method.group(1).upper()
        return 'GET'

    def extract_inputs_from_html_form(self, form_content: str) -> list:
        """Create a list of dict with all input information

        Args:
            form_content (str): The html content of the form

        Returns:
            list: List of dict information inputs
        """
        list_dict_inputs_information = []
        inputs = re.findall(r'(?i)(?s)<input.*?>', form_content)
        for input in inputs:
            dict_input_information = self.extract_input_informations(input)
            if dict_input_information:
                list_dict_inputs_information.append(dict_input_information)

        return list_dict_inputs_information

    def extract_input_informations(self, input_html: str) -> dict:
        """Create a dict with all input information

        Args:
            input_html (str): The html content of one input

        Returns:
            dict: Dict with input information
        """
        dict_input = {}

        input_name = re.search(r'(?i)name=[\'"](.*?)[\'"]', input_html)

        if input_name:
            input_type = re.search(r'(?i)type=[\'"](.*?)[\'"]', input_html)
            input_value = re.search(r'(?i)value=[\'"](.*?)[\'"]', input_html)

            input_name = input_name.group(1)

            if input_type:
                input_type = input_type.group(1)
            else:
                input_type = ""

            if input_value:
                input_value = input_value.group(1)
            else:
                input_value = ""

            if input_type.lower() == "submit" and input_value == "":
                input_value = "Submit Query"

            dict_input = {
                "name": input_name,
                "type": input_type,
                "value": input_value
            }

        return dict_input

    def create_dict_data(self, inputs: list) -> dict:
        """Create a dict with data from input with default value

        Args:
            inputs (list): list of dict input information

        Returns:
            dict: all the data informations
        """
        dict_data = {}

        for input in inputs:
            dict_data[input['name']] = input['value']

        return dict_data

    def is_url_correct(self, url: str) -> bool:
        """Check if a url is correct

        Args:
            url (str)

        Returns:
            bool: True if correct / False incorrect
        """
        if type(url) is not str:
            return False
        if validators.url(url):
            return True

        return False

    def find_difference_between_two_html_file(self, content_1, content_2) -> str:
        text_to_find = ""
        output_list = [li for li in difflib.ndiff(content_1, content_2) if li[0] != ' ']
        for character in output_list:
            if character[0:2] == "+ ":
                text_to_find = f"{text_to_find}{character[2:]}"

        return text_to_find
