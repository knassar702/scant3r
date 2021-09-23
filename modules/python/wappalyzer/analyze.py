from modules import Scan
from core.libs import Http
from Wappalyzer import Wappalyzer, WebPage


class Analyze(Scan):
    def __init__(self, opts: dict, http: Http):
        super().__init__(opts, http)

    def start(self):
        return self.parse_result_wappalyzer(self.wappalyzer())

    def wappalyzer(self) -> dict:
        """Analyse the website and give the version on composant

        Args:
            url (str): url to analyse

        Raises:
            ValueError: Invalid url

        Returns:
            dict: The result of analyse
        """
        if not self.is_url_correct(self.opts['url']):
            raise ValueError('The url is invalid')

        webpage = WebPage.new_from_url(self.opts['url'])
        wappalyzer = Wappalyzer.latest()
        return wappalyzer.analyze_with_versions_and_categories(webpage)

    def parse_result_wappalyzer(self, result_wappalyzer: dict) -> list:
        """Parse the dict of wappalyser

        Args:
            result_wappalyzer (dict): the dict from wappalyzer function

        Raises:
            TypeError: if the arg is not a dict

        Returns:
            list: list with a dict foreach service
        """
        if type(result_wappalyzer) is not dict:
            raise TypeError('The result of wappalyzer is not a dict')

        list_result = []
        for key in result_wappalyzer.keys():
            correct_dict = {}
            correct_dict['service'] = str(key).lower()

            correct_dict['categories'] = ""
            if "categories" in result_wappalyzer[key] and result_wappalyzer[key]['categories']:
                correct_dict['categories'] = result_wappalyzer[key]['categories'][0]

            correct_dict['versions'] = ""
            if "versions" in result_wappalyzer[key] and result_wappalyzer[key]['versions']:
                correct_dict['versions'] = result_wappalyzer[key]['versions'][0]

            list_result.append(correct_dict)

        return list_result
