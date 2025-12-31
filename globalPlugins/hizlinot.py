# -*- coding: utf-8 -*-
import os
import datetime
import globalPluginHandler
import scriptHandler
import gui
import wx
import ui
import speech
import webbrowser
import addonHandler

addonHandler.initTranslation()

class NoteDialog(wx.Dialog):
	def __init__(self, parent, title):
		super().__init__(parent, title=title, size=(450, 350))
		panel = wx.Panel(self)
		vbox = wx.BoxSizer(wx.VERTICAL)
		lbl = wx.StaticText(panel, label=_("Enter your note:"))
		vbox.Add(lbl, 0, wx.ALL | wx.EXPAND, 10)
		self.textCtrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
		vbox.Add(self.textCtrl, 1, wx.ALL | wx.EXPAND, 10)
		btnSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.okBtn = wx.Button(panel, wx.ID_OK, label=_("OK"))
		self.cancelBtn = wx.Button(panel, wx.ID_CANCEL, label=_("Close"))
		self.donateBtn = wx.Button(panel, label=_("Donate"))
		btnSizer.Add(self.okBtn, 0, wx.ALL, 5)
		btnSizer.Add(self.cancelBtn, 0, wx.ALL, 5)
		btnSizer.Add(self.donateBtn, 0, wx.ALL, 5)
		vbox.Add(btnSizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
		panel.SetSizer(vbox)
		self.okBtn.SetDefault()
		self.donateBtn.Bind(wx.EVT_BUTTON, self.onDonate)

	def onDonate(self, event):
		webbrowser.open("https://www.paytr.com/link/N2IAQKm")

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super().__init__()

	@scriptHandler.script(description=_("Take a quick note"), category=_("Quick Note"))
	def script_takeQuickNote(self, gesture):
		wx.CallAfter(self.showNoteDialog)

	def showNoteDialog(self):
		desktop = os.path.join(os.path.expanduser('~'), 'Desktop')
		filePath = os.path.join(desktop, "Notes.txt")
		dlg = NoteDialog(gui.mainFrame, _("Quick Note Taker v5.0 - Volkan Ozdemir Software Services"))
		speech.speakMessage(_("Please enter your note"))
		if dlg.ShowModal() == wx.ID_OK:
			note = dlg.textCtrl.GetValue().strip()
			if note:
				now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
				with open(filePath, "a", encoding="utf-8") as f:
					f.write(f"\n--- {now} ---\n{note}\n------------------\n")
				ui.message(_("Note saved to desktop."))
		dlg.Destroy()