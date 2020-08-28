import webapp2
import os
from google.appengine.ext.webapp import template
from google.appengine.ext import ndb
from helperfunctions import *


class LandingPage(webapp2.RequestHandler):
    def get(self):
        page = os.path.join(os.path.dirname(__file__), 'pages/index.html')
        pagevalues = {}
        self.response.out.write(template.render(page, pagevalues))


class LoginValidate(webapp2.RequestHandler):
    def post(self):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        user = checkUserCredentials(username, password)
        if user is None:
            page = os.path.join(os.path.dirname(__file__), 'pages/index.html')
            pagevalues = {'msg': 'Username/Password Do not Match.'}
            self.response.out.write(template.render(page, pagevalues))
            return
        else:
            page = os.path.join(os.path.dirname(__file__), 'pages/userdashboard.html')
            pagevalues = {'user': user}
            self.response.out.write(template.render(page, pagevalues))
            return


class CreatTaskboard(webapp2.RequestHandler):
    def get(self):
        uid = int(self.request.get('uid'))
        if checkUserExits(uid):
            user = getUserDetails(uid)
            page = os.path.join(os.path.dirname(__file__), 'pages/createtaskboard.html')
            pagevalues = {'user': user}
            self.response.out.write(template.render(page, pagevalues))
        else:
            page = os.path.join(os.path.dirname(__file__), 'pages/error.html')
            self.response.out.write(template.render(page, {}))


class CreateTaskboardSubmit(webapp2.RequestHandler):
    def get(self):
        uid = int(self.request.get('uid'))
        if checkUserExits(uid):
            user = getUserDetails(uid)
            if createNewTaskboard(self.request.get('tbname'), user):
                page = os.path.join(os.path.dirname(__file__), 'pages/createtaskboardsuccess.html')
                pagevalues = {'user': user}
                self.response.out.write(template.render(page, pagevalues))
                return
            else:
                page = os.path.join(os.path.dirname(__file__), 'pages/createtaskboard.html')
                pagevalues = {'user': user, 'msg': 'Error :Taskboard exits with the name.'}
                self.response.out.write(template.render(page, pagevalues))
        else:
            page = os.path.join(os.path.dirname(__file__), 'pages/error.html')
            self.response.out.write(template.render(page, {}))


class UserDashBoard(webapp2.RequestHandler):
    def get(self):
        uid = int(self.request.get('uid'))
        if checkUserExits(uid):
            user = getUserDetails(uid)
            page = os.path.join(os.path.dirname(__file__), 'pages/userdashboard.html')
            pagevalues = {'user': user}
            self.response.out.write(template.render(page, pagevalues))
        else:
            page = os.path.join(os.path.dirname(__file__), 'pages/error.html')
            self.response.out.write(template.render(page, {}))


class ViewCreatedTaskboard(webapp2.RequestHandler):
    def get(self):
        uid = int(self.request.get('uid'))
        if checkUserExits(uid):
            user = getUserDetails(uid)
            createdtaskboard = getallcreatedtaskboards(user)

            pagevalues = {'user': user, 'usercreatedtb': createdtaskboard}
            page = os.path.join(os.path.dirname(__file__), 'pages/viewcreatedtaskboard.html')
            self.response.out.write(template.render(page, pagevalues))
        else:
            page = os.path.join(os.path.dirname(__file__), 'pages/error.html')
            self.response.out.write(template.render(page, {}))


class ViewCreatedTBData(webapp2.RequestHandler):
    def get(self):
        uid = int(self.request.get('uid'))
        if checkUserExits(uid):
            user = getUserDetails(uid)
            taskboadDetails = getTaskboardDetails(int(self.request.get("tb")))
            taskboardTasks = getTaskboardTasks(taskboadDetails.tbid)
            pagevalues = {'user': user, 'taskboard': taskboadDetails, 'tasks': taskboardTasks}
            page = os.path.join(os.path.dirname(__file__), 'pages/viewtaskboarddata.html')
            self.response.out.write(template.render(page, pagevalues))
        else:
            page = os.path.join(os.path.dirname(__file__), 'pages/error.html')
            self.response.out.write(template.render(page, {}))


class AddnewTaskToTaskboard(webapp2.RequestHandler):
    def get(self):
        uid = int(self.request.get('uid'))
        if checkUserExits(uid):
            user = getUserDetails(uid)
            taskboadDetails = getTaskboardDetails(int(self.request.get("tbid")))
            if addNewTAskToTaskBoard(self.request.get('tname'), self.request.get('tdue'), taskboadDetails):
                taskboardTasks = getTaskboardTasks(taskboadDetails.tbid)
                pagevalues = {'user': user, 'taskboard': taskboadDetails, 'tasks': taskboardTasks}
                page = os.path.join(os.path.dirname(__file__), 'pages/viewtaskboarddata.html')
                self.response.out.write(template.render(page, pagevalues))
                return
            else:
                taskboardTasks = getTaskboardTasks(taskboadDetails.tbid)
                pagevalues = {'user': user, 'taskboard': taskboadDetails, 'tasks': taskboardTasks,
                              "msg": 'Task Already Exists'}
                page = os.path.join(os.path.dirname(__file__), 'pages/viewtaskboarddata.html')
                self.response.out.write(template.render(page, pagevalues))
                return


        else:
            page = os.path.join(os.path.dirname(__file__), 'pages/error.html')
            self.response.out.write(template.render(page, {}))


class CompleteTask(webapp2.RequestHandler):
    def get(self):
        uid = int(self.request.get('uid'))
        if checkUserExits(uid):
            user = getUserDetails(uid)
            task = self.request.get("taskid")
            completeTask(int(task))
            taskboadDetails = getTaskboardDetails(int(self.request.get("tbid")))
            taskboardTasks = getTaskboardTasks(taskboadDetails.tbid)
            pagevalues = {'user': user, 'taskboard': taskboadDetails, 'tasks': taskboardTasks, 'msg': 'Task Deleted'}
            page = os.path.join(os.path.dirname(__file__), 'pages/viewtaskboarddata.html')
            self.response.out.write(template.render(page, pagevalues))
        else:
            page = os.path.join(os.path.dirname(__file__), 'pages/error.html')
            self.response.out.write(template.render(page, {}))


class DeleteTask(webapp2.RequestHandler):
    def get(self):
        uid = int(self.request.get('uid'))
        if checkUserExits(uid):
            user = getUserDetails(uid)
            task = self.request.get("taskid")
            deleteTask(int(task))
            taskboadDetails = getTaskboardDetails(int(self.request.get("tbid")))
            taskboardTasks = getTaskboardTasks(taskboadDetails.tbid)
            pagevalues = {'user': user, 'taskboard': taskboadDetails, 'tasks': taskboardTasks, 'msg': 'Task Deleted'}
            page = os.path.join(os.path.dirname(__file__), 'pages/viewtaskboarddata.html')
            self.response.out.write(template.render(page, pagevalues))
        else:
            page = os.path.join(os.path.dirname(__file__), 'pages/error.html')
            self.response.out.write(template.render(page, {}))


class DeleteTaskboard(webapp2.RequestHandler):
    def get(self):
        uid = int(self.request.get('uid'))
        if checkUserExits(uid):
            user = getUserDetails(uid)
            deleteTaskboard(int(self.request.get('tbid')))
            createdtaskboard = getallcreatedtaskboards(user)

            pagevalues = {'user': user, 'usercreatedtb': createdtaskboard}
            page = os.path.join(os.path.dirname(__file__), 'pages/viewcreatedtaskboard.html')
            self.response.out.write(template.render(page, pagevalues))
        else:
            page = os.path.join(os.path.dirname(__file__), 'pages/error.html')
            self.response.out.write(template.render(page, {}))


class ViewMemberTaskboard(webapp2.RequestHandler):
    def get(self):
        uid = int(self.request.get('uid'))
        if checkUserExits(uid):
            user = getUserDetails(uid)
            createdtaskboard = getallmembertaskboards(user)

            pagevalues = {'user': user, 'usercreatedtb': createdtaskboard}
            page = os.path.join(os.path.dirname(__file__), 'pages/viewmembertaskboard.html')
            self.response.out.write(template.render(page, pagevalues))
        else:
            page = os.path.join(os.path.dirname(__file__), 'pages/error.html')
            self.response.out.write(template.render(page, {}))


class AddMemberToTaskboard(webapp2.RequestHandler):
    def get(self):
        uid = int(self.request.get('uid'))
        if checkUserExits(uid):
            user = getUserDetails(uid)
            taskboadDetails = getTaskboardDetails(int(self.request.get("tbid")))
            if createMember(taskboadDetails.tbid, user.uid):
                taskboardTasks = getTaskboardTasks(taskboadDetails.tbid)
                members = getMembers(taskboadDetails)
                pagevalues = {'user': user, 'taskboard': taskboadDetails, 'tasks': taskboardTasks, 'members': members}
                page = os.path.join(os.path.dirname(__file__), 'pages/viewtaskboarddata.html')
                self.response.out.write(template.render(page, pagevalues))
                return
            else:
                taskboardTasks = getTaskboardTasks(taskboadDetails.tbid)
                members = getMembers(taskboadDetails)
                pagevalues = {'user': user, 'taskboard': taskboadDetails, 'tasks': taskboardTasks,
                              "memmsg": 'Cannot Add Duplicate Member', 'members': members}
                page = os.path.join(os.path.dirname(__file__), 'pages/viewtaskboarddata.html')
                self.response.out.write(template.render(page, pagevalues))
                return


        else:
            page = os.path.join(os.path.dirname(__file__), 'pages/error.html')
            self.response.out.write(template.render(page, {}))
