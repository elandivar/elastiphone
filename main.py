# ----------------------------------------------------------------------+
# Elastix Communicator 0.1
# Copyright (c) 2012 Edgar Landivar
# ----------------------------------------------------------------------+
# The contents of this files are subject to a propietary commercial
# license.
# ----------------------------------------------------------------------+
# Contact the Developer if you want to use or distribute this program.
# Authorized use or distribution is prohibited.
# ----------------------------------------------------------------------+

import sys
import json
import httplib2 #installed manually
from Tkinter import *
import ttk
import pjsua as pj
import _pjsua
import threading
# My Libraries 
import winx
import conf
import mysip as mysip
import restc
from myglobs import *
import splash

common_objects['current_call'] = None

root = Tk()
root.title("Elastix Communicator")
#ttk.Style().configure("TLabel", background="yellow")
#ttk.Style().configure("B.TFrame", background="yellow")
#s.configure('EComm.TFrame', background='yellow')
#s.theme_use('clam')
root.geometry('450x600-20+20')
root.minsize(width=450, height=600)

#img_bground = PhotoImage(file='splash.gif')
#root = Label(root1, image=img_bground)
#root.pack(side='top', fill='both', expand='yes')


#Load Configuration
common_objects['myconf'] = conf.ecConfig()
conf_params = common_objects['myconf'].get_configuration()
#TODO: HTTPS Not supported at this time
url_ext   = 'http://' + conf_params['elx_host'] + '/rest.php/address_book/SyncContacts/full'
url_int   = 'http://' + conf_params['elx_host'] + '/rest.php/address_book/ContactList/internal'
url_call  = 'http://' + conf_params['elx_host'] + '/rest.php/pbxadmin/Call/'

common_objects['myView'] = winx.Winx(root)

def dump(obj):
   for attr in dir(obj):
      print "obj.%s = %s" % (attr, getattr(obj, attr))

class MyThread(threading.Thread):

   def run (self):
      #global current_call, acc
      global common_objects, acc
      lib = pj.Lib()

      try:
         # SIP Registration
         mysip.sip_registration(lib, conf_params)

      except pj.Error, e:
         print "Exception: " + str(e)
         lib.destroy()
         lib = None

with splash.SplashScreen(root, 'images/splash.gif', 3):
   # The menu bar
   common_objects['myView'].draw_menu_bar()
   # The bar at the upside position that allows the user to place calls
   common_objects['myView'].draw_main_header()
   calltext_widget = common_objects['myView'].get_calltext_widget()

   #Connection to HOST
   http = httplib2.Http()
   http.add_credentials(conf_params['http_user'], conf_params['http_pass'])
   data = restc.get_rest_data(http, url_ext, url_int)

   wnotebook_main = ttk.Notebook(root)
   wmf1 = ttk.Frame(wnotebook_main)
   wmf2 = ttk.Frame(wnotebook_main)
   wmf3 = ttk.Frame(wnotebook_main)
   wnotebook_main.add(wmf1, text='Contacts')
   wnotebook_main.add(wmf2, text='Events')
   wnotebook_main.add(wmf3, text='History')
   img_tab_contacts = PhotoImage(file='images/contacts.gif')
   wnotebook_main.tab(0, image=img_tab_contacts, text='Contacts', compound='left')
   img_tab_calendar = PhotoImage(file='images/calendar.gif')
   wnotebook_main.tab(1, image=img_tab_calendar, text='Events', compound='left')
   img_tab_history = PhotoImage(file='images/clock.gif')
   wnotebook_main.tab(2, image=img_tab_history, text='History', compound='left')
   wnotebook_main.grid(row=2, column=0, sticky=W+E+N+S)

   common_objects['myView'].draw_search_contacts_bar(wmf1, data)
   common_objects['myView'].draw_treeview_contacts(data, wmf1)
   common_objects['myView'].draw_contact_management_bar(wmf1)

   root.columnconfigure(0, weight=1)
   root.rowconfigure(0, weight=0)
   root.rowconfigure(1, weight=0)
   root.rowconfigure(2, weight=1)
   wmf1.columnconfigure(0, weight=1)
   wmf1.columnconfigure(1, weight=0)
   wmf1.rowconfigure(0, weight=0)
   wmf1.rowconfigure(1, weight=1)

MyThread().start()
root.mainloop()
