#!/usr/bin/env python3
from modules.scant3r_maker import Module,colors,thetime
def data(): # The all data of module
	data = {
	'name': 'Dumper',
	'description':'''
Dump Everything in website (img , links , js , etc ..)
	''',
	'date':'6-3-2020',
	'license':'GPL',
	'authors':[
	'Khaled Nassar'],
	'emails':[
	'knassar702@gmail.com'],
	'list_support': True,
	'options':[
	'url',
	'threads',
	'timeout'
	]
	}
	return data
class script:
	def __init__(self):
		pass
	def run(self,options):
		import requests
		from bs4 import BeautifulSoup
		f = options['file']
		for url in f:
			if url.startswith('http://') or url.startswith('https://'):
				pass
			else:
				url = f'http://{url}'
			print(f"{colors().info} [ {url.strip()} ]")
			base_url = url.strip()
			try:
				r = requests.get(base_url,verify=False,timeout=options['timeout'])
				soup = BeautifulSoup(r.text)
				l = {
				'img':'src',
				'script':'src',
				'link':'href',
				'a':'href',
				'input':'name',
				}
				for tag,ty in l.items():
					print(f'\n\n{colors().red}+={colors().yellow}------{base_url}--[{tag}]----------{colors().red}=+{colors().end}')
					for src in soup.find_all(tag):
						try:
							print(src[ty])
						except:
							continue
				print(f'{colors().red}#{colors().yellow}----------------------{colors().red}#{colors().end}')
			except:
				pass
