import sublime, sublime_plugin
import urllib2, httplib, urllib
import json as JSON
import time
import Cookie

basicUrl = 'https://www.hackerrank.com/rest/contests/'

lang = {'py':'python', 'java':'java', 'c':'c', 'cpp':'cpp'}

class HackerRank():
	def __init__(self, problem, lang, code):
		self.problem = problem
		self.code = code
		self.lang = lang
		self.url = 'https://www.hackerrank.com/rest/contests/master/challenges/%s/compile_tests'%problem
		self.submissionId = None
		self.submitted = False
		self.cookie = None

	def run(self):
		jsonResponse = 'NULL'
		count = 0
		i = 0

   	  	try:
   	  		jsonRequest = {'code':self.code,'language':self.lang,'customtestcase':'false'}
   	  		data = urllib.urlencode(jsonRequest)
   	  		httpResponse = urllib2.urlopen(self.url, data)
   	  		print "Requesting on %s"%self.url
   	  		response = JSON.loads(httpResponse.read())

	  		while  self.submitted == False and count<5:
				count = count + 1
				if response['status']:
					header = httpResponse.info()
					cookie = Cookie.SimpleCookie(header['Set-Cookie'])
					self.cookie = "hackerrank_mixpanel_token=" + cookie['hackerrank_mixpanel_token'].value +";"+ "_hackerrank_session=" + cookie['_hackerrank_session'].value + ";"
					if response['model']['id']:
						self.submissionId = response['model']['id']
						self.submitted = True
						print "Code is successfully Submitted."
						print "[SubmissionId] : %s"%self.submissionId
					else:
						print "Error occurred during code submission. Wait! and let me try again"
						time.sleep(1)
			if self.submitted == False:
				print "[Failed] : Could not submit your code, try again"

	  		url = self.url+'/'+str(self.submissionId)+'?_'
	  		sock = urllib2.Request(url)
			sock.add_header('Cookie', self.cookie)

	  		while i < 5:
	  			response = urllib2.urlopen(sock)
	  			jsonResponse = JSON.loads(response.read())
	  			print jsonResponse
	  			if jsonResponse['status']:
	  				if len(jsonResponse['model']) is not 0:
	  					break
	  				else:
	  					time.sleep(1)
	  					if i > 8:
	  						print "\n\nTIMED OUT TRY AGAIN\n\n"
	  						return
	  			i += 1
	  		self.printOutput(jsonResponse)
	  	except (urllib2.HTTPError) as (e):
			print "Something went wrong. Check the problem slug"
		except (urllib2.URLError) as (e):
			print "Something went wrong buddy, try again"
	
	def printOutput(jsonResponse):
		if jsonResponse['status']:
			print "[Output] : \n"
			print jsonResponse['testcase_message']
		else:
			print "Compilation Error"


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
