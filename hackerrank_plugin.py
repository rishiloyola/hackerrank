import sublime, sublime_plugin

lang = {'py':'python', 'java':'java', 'c':'c', 'cpp':'cpp'}

class HackerRank():
	def __init__(self, problem, lang, code):
		self.problem = problem
		self.code = code
		self.lang = lang
		self.url = 'https://www.hackerrank.com/rest/contests/master/challenges/%s/compile_tests'%problem
		self.submissionId = None

	def run():


class RunCommand(sublime_plugin.TextCommand):

	def getFileExtension(self):
		filePath = self.view.file_name()	
		if filePath == None:
			return None, None
		fileName = filePath.split('/')[-1]
		extension = fileName.split('.')[1]
		fName = fileName.split('.')[0]
		language = lang[extension]
		return language, fileName

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
