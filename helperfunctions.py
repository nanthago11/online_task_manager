from datastoreclasses import *
import logging
import time
from datetime import date


def checkUserExits(username):
    allusers = User.query().fetch()
    if len(allusers) > 0:
        for user in allusers:
            if user.uname == username:
                return True
    return False


def checkUserExits(uid):
    allusers = User.query().fetch()
    if len(allusers) > 0:
        for user in allusers:
            if user.uid == uid:
                return True
    return False


def getNewId():
    return int(round(time.time()))


def createNewUser(username, password):
    newUser = User()
    newUser.uname = username
    newUser.uid = getNewId()
    newUser.upassword = password
    newUser.put()
    return newUser


def checkUserCredentials(username, password):
    if not checkUserExits(username):
        newuser = createNewUser(username, password)
        return newuser
    allUsers = User.query().fetch()
    for user in allUsers:
        logging.info("User validated")
        if user.uname == username and password == user.upassword:
            return user
    logging.info("User not found")


def getUserDetails(uid):
    for user in User.query().fetch():
        if user.uid == uid:
            return user


def createNewTaskboard(tbname, user):
    for tb in Taskboard.query().fetch():
        if tb.tbname == tbname:
            return False
    newTb = Taskboard()
    newTb.tbid = getNewId()
    newTb.tbname = tbname
    newTb.tbcreator = user.uid
    newTb.createddate = date.today()
    newTb.put()
    createMember(newTb.tbid, user.uid)
    return True


def createMember(tbid, userid):
    member = MemberUser()
    member.tbid = tbid
    member.uid = userid
    for mem in MemberUser.query().fetch():
        if mem.tbid == tbid and mem.uid == userid:
            return False
    member.put()
    return True


def getallcreatedtaskboards(user):
    tbs = []
    for tb in Taskboard.query().fetch():
        if tb.tbcreator == user.uid:
            tbs.append(tb)
    return tbs


def getTaskboardDetails(tbid):
    for tb in Taskboard.query().fetch():
        if tb.tbid == tbid:
            return tb

    return None


def getTaskboardTasks(tbid):
    tasks = []
    taskboard = getTaskboardDetails(tbid)
    for task in Task.query().fetch():
        if task.tbid == taskboard.tbid:
            tasks.append(task)
    return tasks


def addNewTAskToTaskBoard(tname, tdue, tb):
    task = Task()
    task.tid = getNewId()
    task.tname = tname
    task.tdue = tdue
    task.tbid = tb.tbid
    task.tcompleted = '_'
    task.tbstatus = 'In Progress'
    for temp in Task.query().fetch():
        if temp.tbid == tb.tbid:
            if temp.tname == tname:
                logging.info("Here")
                return False
    task.put()
    return True


def deleteTask(task):
    for temp in Task.query().fetch():
        if temp.tid == task:
            temp.key.delete()


def completeTask(task):
    for temp in Task.query().fetch():
        if temp.tid == task:
            temp.tbstatus = 'Completed'
            temp.tcompleted = str(date.today())
            temp.put()


def deleteTaskboard(tbid):
    for mem in MemberUser.query().fetch():
        if mem.tbid == tbid:
            mem.key.delete()
    for task in Task.query().fetch():
        if task.tbid == tbid:
            task.key.delete()
    for taskb in Taskboard.query().fetch():
        if taskb.tbid == tbid:
            taskb.key.delete()
            return


def getallmembertaskboards(user):
    listoftbid = []
    for mem in MemberUser.query().fetch():
        if mem.uid == user.uid:
            listoftbid.append(mem.tbid)
    return getTaskboardFromTbidList(listoftbid)


def getTaskboardFromTbidList(listoftbid):
    taskboardlist = []
    for tbid in listoftbid:
        for tb in Taskboard.query().fetch():
            if tbid == tb.tbid:
                taskboardlist.append(tb)
    return taskboardlist


def getMembers(taskboadDetails):
    memberids = []
    for mem in MemberUser.query().fetch():
        if mem.tbid == taskboadDetails.tbid:
            memberids.append(mem.uid)
    memberUsersDetails = []
    for uid in memberids:
        memberUsersDetails.append(getUserDetails(uid))
    return memberUsersDetails
