import sublime, sublime_plugin
import urllib2, httplib, urllib
import json as JSON
import time

basicUrl = 'https://www.hackerrank.com/rest/contests/'

lang = {'py':'python', 'java':'java', 'c':'c', 'cpp':'cpp'}

class HackerRank():
	def __init__(self, problem, lang, code):
		self.problem = problem
		self.code = code
		self.lang = lang
		self.url = 'https://www.hackerrank.com/rest/contests/master/challenges/%s/compile_tests'%problem
		self.submissionId = None

	def getCredentials(self):
   		from os.path import expanduser
   	  	import os
	  	home = expanduser("~")+'/'

	  	try:
	  		f = open(home+'account.txt', 'r')
	  	except IOError:
	  		return None, None, None
	  	text = f.readlines()
	  	return True, text[0], text[1]
	
	def getParams(self, username, password):
	  authController = urllib2.HTTPBasicAuthHandler()
	  authController.add_password( realm=None, uri=basicUrl, user=username, passwd=password)
	  opener = urllib2.build_opener(authController)
	  urllib2.install_opener(opener)
	  return

	def run(self):
		status, username, password = self.getCredentials()
		if not status:
   	  		print "[Error] : Enter your username & password in home/account.txt' \n\n"
   	  		return
   	  	'''self.getParams(username.strip('\n'), password.strip('\n'))'''
   	  	try:
   	  		jsonRequest = {"code":self.code,"language":self.lang,"customtestcase":'false'}
   	  		sock = urllib2.Request(self.url, urllib.urlencode(jsonRequest))
	 		resp = urllib2.urlopen(sock)
	  		header = JSON.loads(resp.read())
	  		print header
	  		codeId = header['model']['id']
	  		url = self.url+'/'+str(codeId)+'?_'
	  		print url
	  		sock = urllib2.Request(url)
	  		jsonResponse = 'NULL'
	  		i = 0
	  		while i < 4:
	  			resp = urllib2.urlopen(sock)
	  			jsonResponse = JSON.loads(resp.read())
	  			print jsonResponse
	  			if jsonResponse['status']:
	  				if len(jsonResponse['model']['testcase_message']) is not 0:
	  					break
	  				else:
	  					time.sleep(1)
	  					if i > 8:
	  						print "\n\nCONNECTION TIMED OUT\n\n"
	  						return
	  			i += 1
	  		self.printOutput(codeId, jsonResponse)
	  	except (urllib2.HTTPError) as (e):
			print "Something went wrong. Check the problem slug"
		except (urllib2.URLError) as (e):
			print "Something went wrong buddy, try again"
	
	def printOutput(self, codeId, jsonResponse):
		print "\n"+'SUBMISSION ID:', str(codeId)+"\n"
		print "[Output] : "
		print jsonResponse


class RunCommand(sublime_plugin.TextCommand):

	def getFileExtension(self):
		filePath = self.view.file_name()	
		if filePath == None:
			return None, None
		fileName = filePath.split('/')[-1]
		extension = fileName.split('.')[1]
		fName = fileName.split('.')[0]
		language = lang[extension]
		return language, fName

	def getFileCode(self):
		content = self.view.substr(sublime.Region(0, self.view.size()))
		return content

	def run(self, edit):
		print "Process started"
		extension, fileName = self.getFileExtension()
		code = self.getFileCode()
		if extension == None:
			print "[Error] : Please save the file"
			return
		hackerrankObj = HackerRank(fileName, extension, code)
		hackerrankObj.run()
		return
