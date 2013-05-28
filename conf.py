import ConfigParser

class ecConfig:
   #configuracion
   def __init__(self):
      self.config = ConfigParser.RawConfigParser()
      self.config.read('ecomm.cfg')

   def read_configuration(self):
      self.conf_params = {'elx_host': self.config.get('general', 'host'), \
                     'http_user': self.config.get('general', 'username'), \
                     'http_pass': self.config.get('general', 'password'), \
                     'sip_user': self.config.get('sip', 'username'), \
                     'sip_pass': self.config.get('sip', 'password') }

   def write_configuration(self, new_conf_params):
      if new_conf_params['elx_host']:
         self.config.set('general', 'host', str(new_conf_params['elx_host'].get()))
         print "updating parameter general.elx_host with value " + str(new_conf_params['elx_host'].get())
      if new_conf_params['http_user']:
         self.config.set('general', 'username', str(new_conf_params['http_user'].get()))
         print "updating parameter general.http_user with value " + str(new_conf_params['http_user'].get())
      if new_conf_params['http_pass']:
         self.config.set('general', 'password', str(new_conf_params['http_pass'].get()))
         print "updating parameter general.http_pass with value " + str(new_conf_params['http_pass'].get())
      if new_conf_params['sip_user']:
         self.config.set('sip', 'username', str(new_conf_params['sip_user'].get()))
         print "updating parameter sip.username with value " + str(new_conf_params['sip_user'].get())
      if new_conf_params['sip_pass']:
         self.config.set('sip', 'password', str(new_conf_params['sip_pass'].get()))
         print "updating parameter sip.password with value " + str(new_conf_params['sip_pass'].get())

      f = open("ecomm.cfg", "w")      
      self.config.write(f)
      f.close() 


   def get_configuration(self):
      self.read_configuration()
      return self.conf_params
