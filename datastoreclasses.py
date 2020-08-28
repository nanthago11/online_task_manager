from google.appengine.ext import ndb


class User(ndb.Model):
    uid = ndb.IntegerProperty()
    uname = ndb.StringProperty()
    upassword = ndb.StringProperty()


class Taskboard(ndb.Model):
    tbid = ndb.IntegerProperty()
    tbcreator = ndb.IntegerProperty()
    tbname = ndb.StringProperty()
    createddate=ndb.DateProperty()


class MemberUser(ndb.Model):
    tbid = ndb.IntegerProperty()
    uid = ndb.IntegerProperty()


class Task(ndb.Model):
    tid = ndb.IntegerProperty()
    tname = ndb.StringProperty()
    tdue = ndb.StringProperty()
    tcompleted = ndb.StringProperty()
    tbid = ndb.IntegerProperty()
    tbstatus = ndb.StringProperty()
    assignedto = ndb.IntegerProperty()
