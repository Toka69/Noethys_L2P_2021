#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
#------------------------------------------------------------------------
# Application :    Noethys, gestion multi-activit�s
# Site internet :  www.noethys.com
# Auteur:          Ivan LUCAS
# Copyright:       (c) 2010-17 Ivan LUCAS
# Licence:         Licence GNU GPL
#------------------------------------------------------------------------


import Chemins
from Utils import UTILS_Adaptations
from Utils.UTILS_Traduction import _
import wx
from Ctrl import CTRL_Bouton_image
import GestionDB
import datetime
from dateutil.relativedelta import relativedelta
from dateutil.easter import easter 


class MyDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, id=-1, style=wx.DEFAULT_DIALOG_STYLE)

        self.label_intro = wx.StaticText(self, -1, _(u"""Cette fonctionnalit� vous permet de g�n�rer automatiquement les jours f�ri�s variables\nd'une ou plusieurs ann�es selon des algorithmes de calcul int�gr�s. Saisissez une\nann�e de d�part, renseignez le nombre d'ann�es � g�n�rer puis cochez les f�ri�s � cr�er."""))

        self.label_nbre = wx.StaticText(self, -1, _(u"Nombre d'ann�es � g�n�rer :"))
        self.ctrl_nbre = wx.SpinCtrl(self, -1, u"", min=1, max=50)

        self.label_annee = wx.StaticText(self, -1, _(u"Depuis l'ann�e :"))
        self.ctrl_annee = wx.SpinCtrl(self, -1, u"", min=1970, max=2999)
        self.ctrl_annee.SetValue(datetime.date.today().year)

        self.label_jours = wx.StaticText(self, -1, _(u"Cochez les f�ri�s � g�n�rer :"))
        listeJours = [_(u"Lundi de P�ques"), _(u"Jeudi de l'ascension"), _(u"Lundi de Pentec�te")]
        self.ctrl_jours = wx.CheckListBox(self, -1, (-1, -1), wx.DefaultSize, listeJours)
        if 'phoenix' in wx.PlatformInfo:
            self.ctrl_jours.SetCheckedItems((0, 1, 2))
        else:
            self.ctrl_jours.SetChecked((0, 1, 2))
        self.ctrl_jours.SetMinSize((-1, 80))
        self.bouton_aide = CTRL_Bouton_image.CTRL(self, texte=_(u"Aide"), cheminImage="Images/32x32/Aide.png")
        self.bouton_ok = CTRL_Bouton_image.CTRL(self, texte=_(u"Ok"), cheminImage="Images/32x32/Valider.png")
        self.bouton_annuler = CTRL_Bouton_image.CTRL(self, texte=_(u"Annuler"), cheminImage="Images/32x32/Annuler.png")

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.OnBoutonAide, self.bouton_aide)
        self.Bind(wx.EVT_BUTTON, self.OnBoutonOk, self.bouton_ok)
        self.Bind(wx.EVT_BUTTON, self.OnBoutonAnnuler, self.bouton_annuler)

    def __set_properties(self):
        self.SetTitle(_(u"Saisie automatique des jours f�ri�s variables"))
        self.ctrl_nbre.SetToolTip(wx.ToolTip(_(u"Saisissez le nombre d'ann�es � g�n�rer")))
        self.ctrl_annee.SetToolTip(wx.ToolTip(_(u"Saisissez l'ann�e de d�part")))
        self.ctrl_jours.SetToolTip(wx.ToolTip(_(u"Cochez les jours f�ri�s � cr�er")))
        self.bouton_aide.SetToolTip(wx.ToolTip(_(u"Cliquez ici pour obtenir de l'aide")))
        self.bouton_ok.SetToolTip(wx.ToolTip(_(u"Cliquez ici pour cr�er les jours f�ri�s")))
        self.bouton_annuler.SetToolTip(wx.ToolTip(_(u"Cliquez ici pour annuler")))

    def __do_layout(self):
        grid_sizer_base = wx.FlexGridSizer(3, 1, 10, 0)
        grid_sizer_base.Add(self.label_intro, 0, wx.ALL, 10)

        grid_sizer_contenu = wx.FlexGridSizer(6, 1, 10, 10)

        grid_sizer_contenu.Add(self.label_nbre, 0, 0, 0)
        grid_sizer_contenu.Add(self.ctrl_nbre, 0, wx.EXPAND, 0)

        grid_sizer_contenu.Add(self.label_annee, 0, 0, 0)
        grid_sizer_contenu.Add(self.ctrl_annee, 0, wx.EXPAND, 0)

        grid_sizer_contenu.Add(self.label_jours, 0, 0, 0)
        grid_sizer_contenu.Add(self.ctrl_jours, 0, wx.EXPAND, 0)
        grid_sizer_contenu.AddGrowableCol(0)
        grid_sizer_base.Add(grid_sizer_contenu, 1, wx.LEFT|wx.RIGHT|wx.EXPAND, 10)

        # Boutons
        grid_sizer_boutons = wx.FlexGridSizer(1, 4, 10, 10)
        grid_sizer_boutons.Add(self.bouton_aide, 0, 0, 0)
        grid_sizer_boutons.Add((20, 20), 0, wx.EXPAND, 0)
        grid_sizer_boutons.Add(self.bouton_ok, 0, 0, 0)
        grid_sizer_boutons.Add(self.bouton_annuler, 0, 0, 0)
        grid_sizer_boutons.AddGrowableCol(1)
        grid_sizer_base.Add(grid_sizer_boutons, 1, wx.ALL|wx.EXPAND, 10)
        self.SetSizer(grid_sizer_base)
        grid_sizer_base.Fit(self)
        grid_sizer_base.AddGrowableCol(0)
        self.Layout()
        self.CenterOnScreen() 

    def OnBoutonAide(self, event):
        from Utils import UTILS_Aide
        UTILS_Aide.Aide("Joursfris")

    def OnBoutonAnnuler(self, event): 
        self.EndModal(wx.ID_CANCEL)

    def OnBoutonOk(self, event): 
        # R�cup�ration des ann�es
        annee_depart = self.ctrl_annee.GetValue()
        nbre_annees = self.ctrl_nbre.GetValue()

        # G�n�ration de la liste des ann�es :
        listeAnnees = range(annee_depart, annee_depart+nbre_annees)

        # R�cup�ration jours f�ri�s � cr�er
        listeCoches = []
        for index in range(0, self.ctrl_jours.GetCount()):
            if self.ctrl_jours.IsChecked(index):
                listeCoches.append(index)

        if len(listeCoches) == 0 :
            dlg = wx.MessageDialog(self, _(u"Vous devez obligatoirement cocher au moins un jour f�ri� � cr�er !"), _(u"Erreur"), wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            dlg.Destroy()
            return False
        
        # R�cup�ration des jours d�j� pr�sents dans la base de donn�es
        DB = GestionDB.DB() 
        req = """SELECT IDferie, nom, jour, mois, annee
        FROM jours_feries
        WHERE type='variable' ; """
        DB.ExecuterReq(req)
        listeDonnees = DB.ResultatReq()
        listeJoursExistants = []
        for IDferie, nom, jour, mois, annee in listeDonnees :
            try :
                listeJoursExistants.append(datetime.date(annee, mois, jour))
            except :
                pass
        
        def SauvegarderDate(nom="", date=None):
            if date not in listeJoursExistants :
                IDferie = DB.ReqInsert("jours_feries", [("type", "variable"), ("nom", nom), ("annee", date.year), ("mois", date.month), ("jour", date.day)])


        # Calcul des jours f�ri�s
        for annee in listeAnnees :
            
            # Dimanche de Paques
            dimanche_paques = easter(annee)
            
            # Lundi de P�ques
            lundi_paques = dimanche_paques + relativedelta(days=+1)
            if 0 in listeCoches : SauvegarderDate(_(u"Lundi de P�ques"), lundi_paques)
            
            # Ascension
            ascension = dimanche_paques + relativedelta(days=+39)
            if 1 in listeCoches : SauvegarderDate(_(u"Jeudi de l'Ascension"), ascension)

            # Pentecote
            pentecote = dimanche_paques + relativedelta(days=+50)
            if 2 in listeCoches : SauvegarderDate(_(u"Lundi de Pentec�te"), pentecote)
        
        DB.Close()
        
        # Fermeture
        self.EndModal(wx.ID_OK)

        



if __name__ == u"__main__":
    app = wx.App(0)
    dlg = MyDialog(None)
    dlg.ShowModal() 
    dlg.Destroy() 
    app.MainLoop()
