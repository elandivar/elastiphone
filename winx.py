from Tkinter import *
import ttk
import mysip
from myglobs import *

global num_to_call
# No se me ocurrio otro nombre :)
class Winx:

   def __init__(self, parent_win):
      self.data = []
      self.parent_win = parent_win

   def get_calltext_widget(self):
      return self.calltext_widget

   def set_status_text(self, text):
      self.status_text.set("VoIP Account Status: " + text)

   def open_incomming_call_window(self, incomming_call_uri):
      self.wwindow_call = Toplevel(self.parent_win, padx=10, pady=10)

      wlabel_call_confirm = Label(self.wwindow_call, text="Incomming call from " + incomming_call_uri)
      wlabel_call_confirm.grid(row=0, column=0, columnspan=2, sticky=W)

      # Accept button
      wbutton_accept = ttk.Button(self.wwindow_call, text="Answer", command=self.answer_call_callback)
      wbutton_accept.grid(row=1, column=0, sticky=E)
      # hangup button
      wbutton_reject = ttk.Button(self.wwindow_call, text="Reject")
      wbutton_reject.grid(row=1, column=1, sticky=W)

   def answer_call_callback(self):
      self.wwindow_call.destroy()
      mysip.answer_current_call()
      self.draw_current_call_window()

   def call_call_callback(self, num_to_call):
      global common_objects
      if not common_objects['current_call']:
         mysip.callcontact(num_to_call)
         self.draw_current_call_window()

   def draw_main_header(self):
      global wtext_num_to_call, img_dialpad
      # status bar
      wframe_status = Frame(self.parent_win, background="#89AFDA", padx=17)
      #wframe_status['padding'] = (17, 5, 17, 5)
      #wframe_status['style'] = "B.TFrame"
      wframe_status.grid(row=0, column=0, columnspan=2, sticky=W+E+N)
      # status label. By default it shows 'Unregistered'
      self.status_text = StringVar()
      wlabel_status = Label(wframe_status, textvariable=self.status_text, background="#89AFDA")
      wlabel_status.grid(row=0, column=0, sticky=W)
      self.status_text.set("VoIP Account Status: Unregistered")

      # call bar
      wframe_callbar = ttk.Frame(self.parent_win, height=45)
      wframe_callbar['padding'] = (17, 6, 17, 0)
      wframe_callbar.grid(row=1, column=0, columnspan=2, sticky=W+E+N)

      # phone number to call Entry
      num_to_call = StringVar()
      wtext_num_to_call = ttk.Entry(wframe_callbar, textvariable=num_to_call)
      wtext_num_to_call.grid(row=0, column=0, sticky=W+E)

      self.calltext_widget = wtext_num_to_call
      # dialpad button
      img_dialpad = PhotoImage(file="images/pad.gif")
      wbutton_dialpad = Button(wframe_callbar, bg="#333", image=img_dialpad, height=26, width=26, borderwidth=0, padx=0, pady=0)
      wbutton_dialpad.grid(row=0, column=1, sticky=W+E)
      # call button
      #buttonf = ttk.Button(wframe_callbar, text="Call", command=(lambda: self.callback_call(num_to_call)))
      buttonf = ttk.Button(wframe_callbar, text="Call", command=(lambda: self.call_call_callback(num_to_call)))
      buttonf.grid(row=0, column=2, sticky=W+E)
      # hangup button
      #self.wbutton_hangup = ttk.Button(wframe_callbar, text="Hangup")
      #self.wbutton_hangup.grid(row=0, column=2, sticky=E)
      #self.wbutton_hangup.config(state=DISABLED)

      wframe_callbar.columnconfigure(0, weight=1)
      wframe_callbar.columnconfigure(1, weight=0)
      wframe_callbar.columnconfigure(2, weight=0)

   def draw_config_window(self):
      global username, password, host, sip_username, sip_password, common_objects

      # Configuration instance   
      elements = common_objects['myconf'].get_configuration()

      wwindow_conf = Toplevel(self.parent_win)
      wwindow_conf.title('Configuration')
      wwindow_conf.resizable(width=FALSE, height=FALSE)
      wnotebook = ttk.Notebook(wwindow_conf)
      wf1 = ttk.Frame(wnotebook, padding="20 20 20 20")
      wf2 = ttk.Frame(wnotebook, padding="20 20 20 20")
      wnotebook.add(wf1, text='Elastix Account')
      wnotebook.add(wf2, text='SIP Account')

      #Textfield Host
      wlabel_host = ttk.Label(wf1, text='Elastix Host: ')
      wlabel_host.grid(column=0, row=0, sticky=E)
      host = StringVar()
      wtext_host = ttk.Entry(wf1, textvariable=host)
      wtext_host.grid(column=1, row=0)
      if elements['elx_host']:
         wtext_host.delete(0, END)
         wtext_host.insert(0, elements['elx_host'])
      #Textfield Username
      wlabel_username = ttk.Label(wf1, text='Elastix Username: ')
      wlabel_username.grid(column=0, row=1, sticky=E)
      username = StringVar()
      wtext_username = ttk.Entry(wf1, textvariable=username)
      wtext_username.grid(column=1, row=1)
      if elements['http_user']:
         wtext_username.delete(0, END)
         wtext_username.insert(0, elements['http_user'])
      #Textfield Password
      wlabel_password = ttk.Label(wf1, text='Password: ')
      wlabel_password.grid(column=0, row=2, sticky=E)
      password = StringVar()
      wtext_password = ttk.Entry(wf1, textvariable=password, show="*")
      wtext_password.grid(column=1, row=2)
      if elements['http_pass']:
         wtext_password.delete(0, END)
         wtext_password.insert(0, elements['http_pass'])
      #Button
      wbutton_update_config = ttk.Button(wf1, text="Update Configuration", command=self.cb_update_configuration)
      wbutton_update_config.grid(column=1, row=3)

      #Textfield Username SIP
      wlabel_sip_username = ttk.Label(wf2, text='SIP Username: ')
      wlabel_sip_username.grid(column=0, row=0, sticky=E)
      sip_username = StringVar()
      wtext_sip_username = ttk.Entry(wf2, textvariable=sip_username)
      wtext_sip_username.grid(column=1, row=0)
      if elements['sip_user']:
         wtext_sip_username.delete(0, END)
         wtext_sip_username.insert(0, elements['sip_user'])
      #Textfield Password SIP
      wlabel_sip_password = ttk.Label(wf2, text='SIP Password: ')
      wlabel_sip_password.grid(column=0, row=1, sticky=E)
      sip_password = StringVar()
      wtext_sip_password = ttk.Entry(wf2, textvariable=sip_password, show="*")
      wtext_sip_password.grid(column=1, row=1)
      if elements['sip_pass']:
         wtext_sip_password.delete(0, END)
         wtext_sip_password.insert(0, elements['sip_pass'])
      #Button
      wbutton_update_sip_config = ttk.Button(wf2, text="Update Configuration", command=self.cb_update_configuration)
      wbutton_update_sip_config.grid(column=1, row=2)

      wnotebook.pack()

   def cb_update_configuration(self):
      global username, password, host, sip_username, sip_password, common_objects
      newconfig = {'http_user': username, 'http_pass': password, 'elx_host': host, 'sip_user': sip_username, 'sip_pass': sip_password}
      common_objects['myconf'].write_configuration(newconfig)
      common_objects['myconf'].read_configuration()

   def draw_menu_bar(self):
      menubar = Menu(self.parent_win)
 
      filemenu = Menu(menubar, tearoff=0)
      filemenu.add_command(label="Preferences...", command=self.draw_config_window)
      filemenu.add_separator()
      filemenu.add_command(label="Exit", command=self.parent_win.quit)
      menubar.add_cascade(label="File", menu=filemenu)
   
      helpmenu = Menu(menubar, tearoff=0)
      helpmenu.add_command(label="Help Index", command=self.cb_about_window)
      helpmenu.add_command(label="About...", command=self.cb_about_window)
      menubar.add_cascade(label="Help", menu=helpmenu)
   
      self.parent_win.config(menu=menubar)

   def cb_about_window(self):
      print("Ventana de About")

   def draw_treeview_contacts(self, data, wmf1):

      #self.tree = ttk.Treeview(wmf1, columns=('email', 'phone'), selectmode="browse")
      self.tree = ttk.Treeview(wmf1, columns=('phone'), selectmode="browse")
      #self.tree.heading('email', text='Email')
      self.tree.heading('phone', text='Phone')

      self.populate_treeview_contacts(data)

      self.tree.grid(row=1, column=0, sticky=W+E+S+N)
      self.tree.bind("<ButtonRelease-1>", self.update_call_button)

      s = Scrollbar(wmf1, orient=VERTICAL, command=self.tree.yview)
      s.grid(row=1, column=1, sticky=N+S+E)
      self.tree['yscrollcommand'] = s.set

   def update_treeview_contacts(self, data):
      self.tree.delete('list_shared_contacts')
      self.tree.delete('list_private_contacts')
      self.tree.delete('list_internals')
      self.populate_treeview_contacts(data)

   def populate_treeview_contacts(self, data):
      
      self.tree.insert('', 'end', 'list_shared_contacts', text='Shared Contacts', tags=('category'))
      self.tree.insert('', 'end', 'list_private_contacts', text='Private Contacts', tags=('category'))
      self.tree.insert('', 'end', 'list_internals', text='Internos', tags=('category'))

      self.tree.tag_configure('category', background='gray87')    

      for i in data['contacts']:
         if i['status']=='isPrivate':
            node = 'list_private_contacts'
         else:
            node = 'list_shared_contacts'

         itemid = self.tree.insert(node, 'end', text=i['name'])
         #self.tree.set(itemid, 'email', i['email'])
         self.tree.set(itemid, 'phone', i['phone'])

      for i in data['extensions']:
         itemid = self.tree.insert('list_internals', 'end', text=i['name'])
         #self.tree.set(itemid, 'email', i['email'])
         self.tree.set(itemid, 'phone', i['phone'])

   def expand_treeview_contacts(self):
      self.tree.item('list_shared_contacts', open=TRUE)
      self.tree.item('list_private_contacts', open=TRUE)
      self.tree.item('list_internals', open=TRUE)

   def update_call_button(self, event):
      contacts_selected = event.widget.selection()
      for i in contacts_selected:
         last_contact = i
      if last_contact:
         last_contact_values = event.widget.item(last_contact)
         print(last_contact_values)
         if last_contact_values['values']:
            print(last_contact_values)
            #last_contact_phone = str(last_contact_values['values'][1])
            last_contact_phone = str(last_contact_values['values'][0])
            self.calltext_widget.delete(0, END)
            self.calltext_widget.insert(0, last_contact_phone)
            #buttonf.config(state=NORMAL, text='Call')

   def draw_search_contacts_bar(self, wmf1, data):
      global str_contact
      wframe_search = ttk.Frame(wmf1, height=35)
      wframe_search.grid(row=0, column=0, columnspan=2, sticky=W+E)

      str_contact = StringVar()
      wtext_search = ttk.Entry(wframe_search, textvariable=str_contact)
      wtext_search.grid(row=0, column=0, sticky=W+E)
      buttonf2 = ttk.Button(wframe_search, text="Search", command=(lambda: self.filtered_treeview_contacts(data, wtext_search)))
      buttonf2.grid(row=0, column=1, sticky=E)
      buttonf3 = ttk.Button(wframe_search, text="Clear")
      buttonf3.grid(row=0, column=2, sticky=E)
      wframe_search.columnconfigure(0, weight=1)
      wframe_search.columnconfigure(1, weight=0)
      wframe_search.columnconfigure(2, weight=0)

   def draw_contact_management_bar(self, wmf1):
      global img_add_contact, img_del_contact, img_sync_contact
      wframe_contact_manag = ttk.Frame(wmf1, height=35)
      wframe_contact_manag.grid(row=2, column=0, columnspan=2, sticky=W+E)

      img_add_contact = PhotoImage(file="images/add.gif")
      img_del_contact = PhotoImage(file="images/del.gif")
      img_sync_contact = PhotoImage(file="images/sync.gif")
      #iconw = img_add_contact.width() + 2
      #iconh = img_add_contact.height() + 2
      iconw=26
      iconh=26

      wbutton_add_contact = Button(wframe_contact_manag, image=img_add_contact, height=iconh, width=iconw, borderwidth=0, padx=0, pady=0)
      wbutton_add_contact.grid(row=0, column=0, sticky=W)

      wbutton_del_contact = Button(wframe_contact_manag, image=img_del_contact, height=iconh, width=iconw, borderwidth=0, padx=0, pady=0)
      wbutton_del_contact.grid(row=0, column=1, sticky=W)

      wbutton_sync_contact = Button(wframe_contact_manag, image=img_sync_contact, height=iconh, width=iconw, borderwidth=0, padx=0, pady=0)
      wbutton_sync_contact.grid(row=0, column=3, sticky=W)

      wframe_contact_manag.columnconfigure(0, weight=0)
      wframe_contact_manag.columnconfigure(1, weight=0)
      wframe_contact_manag.columnconfigure(2, weight=0)

   def filtered_treeview_contacts(self, data, wtext_search):
      #print(data)
      data_filtered = {}
      data_contacts = []
      data_extensions = []
      for i in data['contacts']:
         if str(wtext_search.get()).lower() in i['name'].lower() or str(wtext_search.get()).lower() in i['phone'].lower():
            data_contacts.append(i)

      for i in data['extensions']:
         if str(wtext_search.get()).lower() in i['name'].lower() or str(wtext_search.get()).lower() in i['phone'].lower():
            data_extensions.append(i)

      data_filtered = {'contacts': data_contacts, 'extensions': data_extensions}
      self.update_treeview_contacts(data_filtered)
      self.expand_treeview_contacts()

   def draw_current_call_window(self):
      global common_objects, img_hangup, img_mute

      self.wwindow_current_call = Toplevel(self.parent_win, padx=10, pady=10, background="#999999")
      self.wwindow_current_call.title("Current call")
      self.wwindow_current_call.resizable(width=FALSE, height=FALSE)
      self.wwindow_current_call.geometry('220x170')

      if common_objects['current_call']:
         call_remote_uri = common_objects['current_call'].info().remote_uri
      else:
         call_remote_uri = "Unknown"

      wlabel_current_call = Label(self.wwindow_current_call, background='#999999', wraplength=180, text="In call with " + call_remote_uri)
      wlabel_current_call.grid(row=0, column=0, columnspan=2, sticky=W+E)

      # hangup button
      img_hangup = PhotoImage(file="images/hangup.gif")
      wbutton_hangup = Button(self.wwindow_current_call, background='#999999', highlightthickness=0, highlightbackground='#999999', relief='flat', padx=0, pady=0, bd=0, width=44, height=44, text="Hangup", image=img_hangup, command=self.hangup_call_callback)
      wbutton_hangup.grid(row=1, column=0, sticky=E)
      # mute button
      img_mute = PhotoImage(file="images/mute.gif")
      wbutton_mute = Button(self.wwindow_current_call, background='#999999', highlightthickness=0, highlightbackground='#999999', padx=0, pady=0, bd=0, width=44, height=44, text="Mute", image=img_mute)
      wbutton_mute.grid(row=1, column=1, sticky=W)

      self.wwindow_current_call.rowconfigure(0, weight=1)
      self.wwindow_current_call.rowconfigure(1, weight=0)

   def hangup_call_callback(self):
      mysip.hangup_current_call()
      self.wwindow_current_call.destroy()
