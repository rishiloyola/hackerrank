import sublime, sublime_plugin
import urllib2, httplib, urllib
import json as JSON
import time
import Cookie
import base64

basicUrl = 'https://www.hackerrank.com/rest/contests/'

lang = {'py':'python', 'java':'java', 'c':'c', 'cpp':'cpp'}

class CustomBasicAuthHandler(urllib2.HTTPBasicAuthHandler):
	def http_request(self, req):
		url = req.get_full_url()
		realm = None
		user, pw = self.passwd.find_user_password(realm, url)
		if pw:
			raw = "%s:%s" % (user, pw)
			auth = 'Basic %s' % base64.b64encode(raw).strip()
			req.add_unredirected_header(self.auth_header, auth)
		return req

	https_request = http_request

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
   	  		self.cookie = "hackerrank_mixpanel_token=" + "676b366b-3e5a-4307-8a63-1e305a22d5e0" +";"+ "_hackerrank_session=" + "BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTUxMDFiOGVkNzg1YjQ3YzU3ZTU3ODhmMmRhYWFjYjA3BjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUdDVTU4SXJQZEFoVTFPdkdyczA2ZVdiQ1RpK0R6Nm1iWGpCWEw3cUh4bXM9BjsARg%3D%3D--c9e2e544456a5de3ea27a200da56e6817fda4d21"+";"
   	  		jsonRequest = {'code':self.code,'language':self.lang,'customtestcase':'false'}
   	  		sock = urllib2.Request(self.url,urllib.urlencode(jsonRequest))
   	  		sock.add_header('Cookie', self.cookie)
   	  		httpResponse = urllib2.urlopen(sock)
   	  		print "Submitting on %s"%self.url
   	  		response = JSON.loads(httpResponse.read())

	  		while  self.submitted == False and count<5:
				count = count + 1
				if response['status']:
					header = httpResponse.info()
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
			print "Something went wrong. Check the file name"
		except (urllib2.URLError) as (e):
			print "Something went wrong buddy, try again"
	
	def printOutput(self, jsonResponse):
		if jsonResponse['status']:
			model = jsonResponse['model']
			total = len(model['testcase_message'])
			success = 0
			print "[OUTPUT]"
			for i in range(0, len(model['testcase_message'])):
				if model['testcase_message'][i] == 'Success':
					success = success + 1
			print "Total Testcases: %d, Passed: %d"% (total, success)
			for i in range(0, len(model['testcase_message'])):
				print "Testcase #%d: %s"%(i+1, model['testcase_message'][i])
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

	def getCredentials(self):
   	  	from os.path import expanduser
   	  	import os
	  	home = expanduser("~")+'/'
	  	try:
	  		f = open(home+'account.txt', 'r')
	  	except IOError:
	  		return None, None, None
	  	lines = f.readlines()
	  	return lines[0], lines[1]
	  	
	def getParams(self, username, password):
	  	auth_handler = CustomBasicAuthHandler()
	  	auth_handler.add_password( realm=None, uri=basicUrl, user=username, passwd=password)
	  	opener = urllib2.build_opener(auth_handler)
	  	urllib2.install_opener(opener)
	  	return
  	
	def getFileCode(self):
		content = self.view.substr(sublime.Region(0, self.view.size()))
		return content

	def run(self, edit):
		print "Process started"
		username, password = self.getCredentials()
		self.getParams(username.strip('\n'), password.strip('\n'))
		extension, fileName = self.getFileExtension()
		code = self.getFileCode()
		if extension == None:
			print "[Error] : Please save the file"
			return
		hackerrankObj = HackerRank(fileName, extension, code)
		hackerrankObj.run()
		return
