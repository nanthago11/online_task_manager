import webapp2

from handlers import *

app = webapp2.WSGIApplication([("/", LandingPage), ("/loginvalidate", LoginValidate),
                               ("/createtaskboard", CreatTaskboard), ("/createtaskboardsubmit", CreateTaskboardSubmit),
                               ("/userdashboard", UserDashBoard), ("/viewcreatedtaskboard", ViewCreatedTaskboard),
                               ("/viewcreatedtbdata", ViewCreatedTBData),
                               ("/addnewtasktotaskboard", AddnewTaskToTaskboard),
                               ("/completetask", CompleteTask), ("/deletetask", DeleteTask),
                               ("/deletetaskboard", DeleteTaskboard), ("/viewmembertaskboard", ViewMemberTaskboard),
                               ("/addmembertotaskboard", AddMemberToTaskboard)],
                              debug=True)
