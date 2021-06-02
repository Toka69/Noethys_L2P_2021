#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
#------------------------------------------------------------------------
# Application :    Noethys, gestion multi-activit�s
# Site internet :  www.noethys.com
# Auteur:          Ivan LUCAS
# Copyright:       (c) 2010-18 Ivan LUCAS
# Licence:         Licence GNU GPL
#------------------------------------------------------------------------


import Chemins
from Utils import UTILS_Adaptations
from Utils.UTILS_Traduction import _
import wx
import GestionDB
import datetime
from Ctrl import CTRL_Assistant_base as Assistant
from Dlg.DLG_Ouvertures import Track_tarif, Track_ligne


# ----------------------------------------
# GENERATION DE SORTIES FAMILIALES
# ----------------------------------------


class Page_introduction(Assistant.Page):
    def __init__(self, parent):
        Assistant.Page.__init__(self, parent)
        self.Ajouter_question(titre=_(u"Bienvenue dans l'assistant de g�n�ration d'une activit� de type sorties familiales."))
        self.Ajouter_question(titre=_(u"Cliquez sur le bouton Suite pour commencer la saisie des donn�es..."))

    def Suite(self):
        return Page_generalites



class Page_generalites(Assistant.Page):
    def __init__(self, parent):
        Assistant.Page.__init__(self, parent)
        self.Ajouter_rubrique(titre=_(u"G�n�ralit�s"))
        self.Ajouter_question(code="nom", titre=_(u"Quel est le nom de l'activit� ?"), commentaire=_(u"Exemple : 'Sorties familiales'"), ctrl=Assistant.CTRL_Texte, obligatoire=True)
        self.Ajouter_question(code="groupes_activites", titre=_(u"Cochez les groupes d'activit�s associ�s � cette activit� :"), commentaire=_(u"Les groupes d'activit�s permettent une s�lection plus rapide dans certaines fen�tres de Noethys."), ctrl=Assistant.CTRL_Groupes_activite)

    def Suite(self):
        return Page_responsable


class Page_responsable(Assistant.Page_responsable):
    def __init__(self, parent):
        Assistant.Page_responsable.__init__(self, parent)

    def Suite(self):
        return Page_renseignements


class Page_renseignements(Assistant.Page_renseignements):
    def __init__(self, parent):
        Assistant.Page_renseignements.__init__(self, parent)

    def Suite(self):
        return Page_conclusion



class Page_conclusion(Assistant.Page):
    def __init__(self, parent):
        Assistant.Page.__init__(self, parent)
        self.Ajouter_question(titre=_(u"F�licitations, vous avez termin� de param�trer votre activit� !"))
        self.Ajouter_question(titre=_(u"Cliquez maintenant sur le bouton Valider pour g�n�rer cette activit�."))

        texte = _(u"""<IMG SRC="%s">
        Apr�s la g�n�ration de l'activit�, vous devrez aller dans le param�trage de l'activit� > Onglet Calendrier
        pour param�trer les sorties. Celles-ci doivent �tre enregistr�es en tant qu'�v�nements dans Noethys. 
        Pour saisir votre premi�re sortie depuis le calendrier des ouvertures, cliquez sur la case de la date souhait�e 
        pour ouvrir l'unit� de consommation 'Sortie' puis cliquez sur le '+' de la case pour saisir une ou plusieurs sorties.
        """) % Chemins.GetStaticPath("Images/16x16/Astuce.png")
        self.Ajouter_question(ctrl=Assistant.CTRL_Html, texte=texte, size=(-1, 50))

        # Pour la cr�ation du groupe unique
        self.parent.dict_valeurs["has_groupes"] = False

    def Suite(self):
        DB = GestionDB.DB()
        self.parent.Sauvegarde_standard(DB)
        IDactivite = self.parent.dict_valeurs["IDactivite"]

        # Unit�s de consommation
        listeIDunite = []
        listeDonnees = [
            ("IDactivite", IDactivite),
            ("nom", _(u"Sortie")),
            ("abrege", _(u"SORTIE")),
            ("type", "Evenement"),
            ("date_debut", "1977-01-01"),
            ("date_fin", "2999-01-01"),
            ("repas", 0),
            ("ordre", 1)
            ]
        IDunite = DB.ReqInsert("unites", listeDonnees)
        listeIDunite.append(IDunite)

        # Unit� de remplissage
        listeIDuniteRemplissage = []
        listeDonnees = [
            ("IDactivite", IDactivite),
            ("nom", _(u"Sortie")),
            ("abrege", _(u"SORTIE")),
            ("seuil_alerte", 5),
            ("date_debut", "1977-01-01"),
            ("date_fin", "2999-01-01"),
            ("afficher_page_accueil", 1),
            ("afficher_grille_conso", 1),
            ("ordre", 1),
            ]
        IDunite_remplissage = DB.ReqInsert("unites_remplissage", listeDonnees)
        listeIDuniteRemplissage.append(IDunite_remplissage)

        listeDonnees = [("IDunite_remplissage", IDunite_remplissage), ("IDunite", IDunite),]
        DB.ReqInsert("unites_remplissage_unites", listeDonnees)

        # Nom de tarif
        listeDonnees = [("IDactivite", IDactivite), ("nom", _(u"Sortie"))]
        IDnom_tarif = DB.ReqInsert("noms_tarifs", listeDonnees)

        # Cat�gories de tarifs
        listeCategoriesEtTarifs = []

        # Cat�gorie unique
        listeDonnees = [("IDactivite", IDactivite), ("nom", _(u"Cat�gorie unique"))]
        IDcategorie_tarif = DB.ReqInsert("categories_tarifs", listeDonnees)
        track_tarif = Track_tarif()
        listeCategoriesEtTarifs.append((IDcategorie_tarif, track_tarif))

        # Tarifs
        listeTarifs = []
        for IDcategorie_tarif, track_tarif in listeCategoriesEtTarifs :
            track_tarif.MAJ({
                "IDactivite": IDactivite,
                "IDnom_tarif": IDnom_tarif,
                "type": "JOURN",
                "date_debut" : "%d-01-01" % datetime.date.today().year,
                "categories_tarifs" : str(IDcategorie_tarif),
                "methode" : "montant_evenement",
                "etats" : "reservation;present;absenti",
                "label_prestation" : "nom_tarif",
                "combi_tarifs" : [{"type": "JOURN", "unites": [IDunite,]},],
                "lignes" : [Track_ligne({"code" : "montant_evenement", "num_ligne" : 0, "tranche" : "1"})],
                })
            listeTarifs.append(track_tarif)

        self.parent.Sauvegarde_tarifs(DB, listeTarifs)

        DB.Close()

        # Fermeture
        self.parent.Quitter()
        return False



class Dialog(Assistant.Dialog):
    def __init__(self, parent):
        Assistant.Dialog.__init__(self, parent, page_introduction=Page_introduction)



if __name__ == "__main__":
    app = wx.App(0)
    #wx.InitAllImageHandlers()
    dialog_1 = Dialog(None)
    app.SetTopWindow(dialog_1)
    dialog_1.ShowModal()
    app.MainLoop()
