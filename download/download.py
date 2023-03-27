#! /bin/env/python

import requests

def downloads(url):
	get_response = requests.get(url)
	file_name = url.split("/")[-1]
	with open(file_name, "wb") as out_file:
		out_file.write(get_response.content)
	
downloads('https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_960_720.jpg')
