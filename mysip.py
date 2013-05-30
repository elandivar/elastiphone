import pjsua as pj
import _pjsua
import threading
import sqlite3 as sqlite
from myglobs import *

def sip_registration(lib, conf_params):
   global acc, common_objects
   lib.init(log_cfg = pj.LogConfig(level=1, callback=log_cb))

   transport = lib.create_transport(pj.TransportType.UDP, pj.TransportConfig(0))
   lib.start()

   acc = lib.create_account(pj.AccountConfig(conf_params['elx_host'], conf_params['sip_user'], conf_params['sip_pass']))

   acc_cb = MyAccountCallback(acc)
   acc.set_callback(acc_cb)
   acc_cb.wait()

def sip_unregistration(lib):
   global acc
   # Shutdown the library
   transport = None
   acc.delete()
   acc = None
   lib.destroy()
   lib = None

def answer_current_call():
   global common_objects
   if not common_objects['current_call']:
      print "There is no call"
   thread_desc = 1
   _pjsua.thread_register("mysipcall", thread_desc)
   common_objects['current_call'].answer(200)

def hangup_current_call():
   global common_objects
   if not common_objects['current_call']:
      print "There is no call"
   common_objects['current_call'].hangup()

def log_cb(level, str, len):
   print str,

# Function to make call
def make_call(uri):
   global acc
   try:
      print "Making call to", uri
      return acc.make_call(uri, cb=MyCallCallback())
   except pj.Error, e:
      print "Exception: " + str(e)
      return None

def callcontact(num_to_call):
   #global lib, conf_params, url_call, http, current_call
   global lib, common_objects
   #Call through the Elastix REST resource
   #url_num_to_call = url_call + str(num_to_call.get())
   #response, content = http.request(url_num_to_call, 'GET', body='', headers={'content-type':'text/plain'})
   #Call through SIP
   #lck = lib.auto_lock()
   thread_desc = 0
   _pjsua.thread_register("gui", thread_desc)
   ci_list = _pjsua.enum_codecs()
   #codecs experiment
   codec_info = []
   for ci in ci_list:
      print(ci.codec_id),
      cp = _pjsua.codec_get_param(ci.codec_id)
      #print(dump(cp.info))

   conf_params = common_objects['myconf'].get_configuration()

   call_uri = 'sip:' + str(num_to_call.get()) + '@' + conf_params['elx_host']
   common_objects['current_call'] = make_call(call_uri)
   #del lck

class MyAccountCallback(pj.AccountCallback):
   sem = None

   def __init__(self, account):
      pj.AccountCallback.__init__(self, account)

   def on_reg_state(self):
      global common_objects
      if self.sem:
         if self.account.info().reg_status == 200:
            common_objects['myView'].set_status_text(self.account.info().reg_reason)
         else:
            common_objects['myView'].set_status_text(self.account.info().reg_reason)

         if self.account.info().reg_status >= 200:
            self.sem.release()

   def on_reg_started(self):
      global common_objects
      common_objects['myView'].set_status_text("Registering...") 

   def wait(self):
      self.sem = threading.Semaphore(0)
      self.sem.acquire()

   def on_incoming_call(self, call):
      global common_objects
      if common_objects['current_call']:
         #print("Parece que hay una llamada activa")
         call.answer(486, "Busy")
         return

      common_objects['myView'].set_status_text("Incomming Call") 

      #print "Incoming call from ", call.info().remote_uri
      common_objects['myView'].open_incomming_call_window(call.info().remote_uri)

      common_objects['current_call'] = call

      call_cb = MyCallCallback(common_objects['current_call'])
      common_objects['current_call'].set_callback(call_cb)

      # Ringing
      common_objects['current_call'].answer(180)

# Callback to receive events from Call
class MyCallCallback(pj.CallCallback):

   def __init__(self, call=None):
      pj.CallCallback.__init__(self, call)

   # Notification when call state has changed
   def on_state(self):
      global common_objects
      
      print "Call with", self.call.info().remote_uri,
      print "is", self.call.info().state_text,
      print "last code =", self.call.info().last_code,
      print "(" + self.call.info().last_reason + ")"

      if self.call.info().state == pj.CallState.DISCONNECTED:
         # Here i will record the call history
         print "................"
         print "LOCAL URI", self.call.info().uri
         print "LOCAL CONTACT", self.call.info().contact
         print "REMOTE URI", self.call.info().remote_uri
         print "REMOTE CONTACT", self.call.info().remote_contact
         print "SIP CALL ID", self.call.info().sip_call_id
         print "STATE", self.call.info().state
         print "STATE TEXT", self.call.info().state_text
         print "LAST CODE", self.call.info().last_code
         print "LAST REASON", self.call.info().last_reason
         print "MEDIA STATE", self.call.info().media_state
         print "MEDIA DIR", self.call.info().media_dir
         print "CONF SLOT", self.call.info().conf_slot
         print "CALL TIME", self.call.info().call_time
         print "TOTAL TIME", self.call.info().total_time
         print "................"
         
         con=None
         try:
            con = sqlite.connect('/Users/egar/Documents/Repos/elastiphone/db/history.db')
            cur = con.cursor()
            buf = "INSERT INTO call_info (id, local_uri, local_contact, remote_uri, remote_contact, sip_call_id, state, state_text, last_code, last_reason, media_state, media_dir, conf_slot, call_time, total_time) values (NULL,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (self.call.info().uri, self.call.info().contact, self.call.info().remote_uri, self.call.info().remote_contact, self.call.info().sip_call_id, self.call.info().state, self.call.info().state_text, self.call.info().last_code, self.call.info().last_reason, self.call.info().media_state, self.call.info().media_dir, self.call.info().conf_slot, self.call.info().call_time, self.call.info().total_time)

            cur.execute(buf)
            con.commit()
            print buf
            
         except lite.Error, e:
            print "Error %s:" % e.args[0]
    
         finally:
            if con:
               con.close()
                  
         common_objects['current_call'] = None
         if common_objects['myView'].wwindow_current_call:
            common_objects['myView'].wwindow_current_call.destroy()

   # Notification when call's media state has changed.
   def on_media_state(self):
      if self.call.info().media_state == pj.MediaState.ACTIVE:
         # Connect the call to sound device
         call_slot = self.call.info().conf_slot
         pj.Lib.instance().conf_connect(call_slot, 0)
         pj.Lib.instance().conf_connect(0, call_slot)
         print "Media is now active"
      else:
         print "Media is inactive"
