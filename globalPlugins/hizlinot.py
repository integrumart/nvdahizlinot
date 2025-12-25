import os
import datetime
import globalPluginHandler
import scriptHandler
import gui
import wx
import ui
import speech
import webbrowser

class NoteDialog(wx.Dialog):
	def __init__(self, parent, title):
		super(NoteDialog, self).__init__(parent, title=title, size=(450, 350))
		panel = wx.Panel(self)
		vbox = wx.BoxSizer(wx.VERTICAL)
		
		lbl = wx.StaticText(panel, label="Notunuzu giriniz:")
		vbox.Add(lbl, 0, wx.ALL | wx.EXPAND, 10)
		
		self.textCtrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
		vbox.Add(self.textCtrl, 1, wx.ALL | wx.EXPAND, 10)
		
		btnSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.okBtn = wx.Button(panel, wx.ID_OK, label="Tamam")
		self.cancelBtn = wx.Button(panel, wx.ID_CANCEL, label="İptal")
		self.donateBtn = wx.Button(panel, label="Bağış Yap")
		
		btnSizer.Add(self.okBtn, 0, wx.ALL, 5)
		btnSizer.Add(self.cancelBtn, 0, wx.ALL, 5)
		btnSizer.Add(self.donateBtn, 0, wx.ALL, 5)
		
		vbox.Add(btnSizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
		panel.SetSizer(vbox)
		self.okBtn.SetDefault()
		self.donateBtn.Bind(wx.EVT_BUTTON, self.onDonate)

	def onDonate(self, event):
		# PayTR Linki - Otomatik dil algılama
		webbrowser.open("https://www.paytr.com/link/N2IAQKm")

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	@scriptHandler.script(
		description="Hızlı Not Al",
		gesture="kb:NVDA+shift+n"
	)
	def script_takeQuickNote(self, gesture):
		wx.CallAfter(self.showNoteDialog)

	def showNoteDialog(self):
		desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
		filePath = os.path.join(desktop, "Notlarim.txt")
		
		dlg = NoteDialog(gui.mainFrame, "Volkan Özdemir Yazılım Hizmetleri")
		speech.speakMessage("Lütfen notunuzu giriniz")
		
		if dlg.ShowModal() == wx.ID_OK:
			note = dlg.textCtrl.GetValue()
			if note:
				now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
				try:
					with open(filePath, "a", encoding="utf-8") as f:
						f.write(f"\n--- {now} ---\n{note}\n------------------\n")
					
					bilgi = "Not masaüstüne kaydedildi."
					ui.message(bilgi)
					speech.speakMessage(bilgi)
				except Exception as e:
					ui.message(str(e))
		dlg.Destroy()