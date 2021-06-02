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


# ----------------------------------------
# GENERATION D'UNE CANTINE SCOLAIRE
# ----------------------------------------


class Page_introduction(Assistant.Page):
    def __init__(self, parent):
        Assistant.Page.__init__(self, parent)
        self.Ajouter_question(titre=_(u"Bienvenue dans l'assistant de g�n�ration d'une activit� de type cantine scolaire"))
        self.Ajouter_question(titre=_(u"Cliquez sur le bouton Suite pour commencer la saisie des donn�es..."))

    def Suite(self):
        return Page_generalites



class Page_generalites(Assistant.Page):
    def __init__(self, parent):
        Assistant.Page.__init__(self, parent)
        self.Ajouter_rubrique(titre=_(u"G�n�ralit�s"))
        if "nom" not in self.parent.dict_valeurs:
            self.parent.dict_valeurs["nom"] = _(u"Cantine")
        self.Ajouter_question(code="nom", titre=_(u"Quel est le nom de la cantine ?"), commentaire=_(u"Exemple : 'Cantine scolaire'"), ctrl=Assistant.CTRL_Texte, obligatoire=False)
        self.Ajouter_question(code="groupes_activites", titre=_(u"Cochez les groupes d'activit�s associ�s � cette activit� :"), commentaire=_(u"Les groupes d'activit�s permettent une s�lection plus rapide dans certaines fen�tres de Noethys."), ctrl=Assistant.CTRL_Groupes_activite)

    def Suite(self):
        return Page_responsable


class Page_responsable(Assistant.Page_responsable):
    def __init__(self, parent):
        Assistant.Page_responsable.__init__(self, parent)

    def Suite(self):
        return Page_groupes



class Page_groupes(Assistant.Page):
    def __init__(self, parent):
        Assistant.Page.__init__(self, parent)
        self.Ajouter_rubrique(titre=_(u"Services"))
        self.Ajouter_question(code="has_groupes", titre=_(u"Le temps de cantine est-il constitu� de plusieurs services ?"), commentaire=_(u"Exemple : Service 1 et Service 2"), ctrl=Assistant.CTRL_Oui_non, defaut=False)

    def Suite(self):
        if self.parent.dict_valeurs["has_groupes"] == True :
            return Page_groupes_nombre
        else :
            return Page_renseignements


class Page_groupes_nombre(Assistant.Page):
    def __init__(self, parent):
        Assistant.Page.__init__(self, parent)
        self.Ajouter_rubrique(titre=_(u"Services"))
        self.Ajouter_question(code="nbre_groupes", titre=_(u"Quel est le nombre de services ?"), commentaire=None, ctrl=Assistant.CTRL_Nombre, obligatoire=True)

    def Suite(self):
        return Page_groupes_liste


class Page_groupes_liste(Assistant.Page):
    def __init__(self, parent):
        Assistant.Page.__init__(self, parent)
        self.Ajouter_rubrique(titre=_(u"Services"))
        for index in range(1, self.parent.dict_valeurs["nbre_groupes"]+1) :
            code = "nom_groupe#%d" % index
            if code not in self.parent.dict_valeurs:
                self.parent.dict_valeurs[code] = _(u"Service %d") % index
            self.Ajouter_question(code=code, titre=_(u"Quel est le nom du service n�%d ?") % index, commentaire=None, ctrl=Assistant.CTRL_Texte, obligatoire=True)

    def Suite(self):
        return Page_renseignements


class Page_renseignements(Assistant.Page_renseignements):
    def __init__(self, parent):
        Assistant.Page_renseignements.__init__(self, parent)

    def Suite(self):
        return Page_categories_tarifs


class Page_categories_tarifs(Assistant.Page):
    def __init__(self, parent):
        Assistant.Page.__init__(self, parent)
        self.Ajouter_rubrique(titre=_(u"Tarifs"))
        self.Ajouter_question(code="has_categories_tarifs", titre=_(u"Avez-vous plusieurs cat�gories de tarifs ?"), commentaire=_(u"On retrouve par exemple souvent 'Commune' et 'Hors commune'."), ctrl=Assistant.CTRL_Oui_non, defaut=False)

    def Suite(self):
        if self.parent.dict_valeurs["has_categories_tarifs"] == True :
            return Page_categories_tarifs_nombre
        else :
            return Page_tarifs


class Page_categories_tarifs_nombre(Assistant.Page):
    def __init__(self, parent):
        Assistant.Page.__init__(self, parent)
        self.Ajouter_rubrique(titre=_(u"Tarifs"))
        self.Ajouter_question(code="nbre_categories_tarifs", titre=_(u"Quel est le nombre de cat�gories de tarifs ?"), commentaire=None, ctrl=Assistant.CTRL_Nombre, obligatoire=True)

    def Suite(self):
        if self.parent.dict_valeurs["nbre_categories_tarifs"] < 2 :
            dlg = wx.MessageDialog(self, _(u"Le nombre de cat�gories doit �tre sup�rieur � 1 !\n\nSinon s�lectionnez Non � la question pr�c�dente."), _(u"Erreur de saisie"), wx.OK | wx.ICON_EXCLAMATION)
            dlg.ShowModal()
            dlg.Destroy()
            return False

        return Page_tarifs


class Page_tarifs(Assistant.Page):
    def __init__(self, parent):
        Assistant.Page.__init__(self, parent)

        # Si une seule cat�gorie de tarif
        if self.parent.dict_valeurs["has_categories_tarifs"] == False :
            self.Ajouter_rubrique(titre=_(u"Tarif"))
            self.Ajouter_question(code="tarif", titre=_(u"Quel est le tarif � appliquer pour le repas ?"), commentaire=_(u"S�lectionnez une m�thode puis saisissez les param�tres demand�s."), ctrl=Assistant.CTRL_Tarif)
        # Si plusieurs cat�gories de tarifs
        else :
            for index in range(1, self.parent.dict_valeurs["nbre_categories_tarifs"]+1):
                self.Ajouter_rubrique(titre=_(u"Tarif n�%d") % index)
                self.Ajouter_question(code="nom_categorie_tarif#%d" % index, titre=_(u"Quel est le nom de la cat�gorie de tarifs n�%d ?") % index, commentaire=_(u"Exemples : 'Commune' ou 'Hors commune'."), ctrl=Assistant.CTRL_Texte, obligatoire=False)
                self.Ajouter_question(code="tarif#%d" % index, titre=_(u"Quel est le tarif � appliquer � la cat�gorie n�%d ?") % index, commentaire=_(u"S�lectionnez une m�thode puis saisissez les param�tres demand�s."), ctrl=Assistant.CTRL_Tarif)

    def Suite(self):
        return Page_conclusion


class Page_conclusion(Assistant.Page):
    def __init__(self, parent):
        Assistant.Page.__init__(self, parent)
        self.Ajouter_question(titre=_(u"F�licitations, vous avez termin� de param�trer votre activit� !"))
        self.Ajouter_question(titre=_(u"Cliquez maintenant sur le bouton Valider pour g�n�rer cette activit�."))

        texte = _(u"""<IMG SRC="%s">
        Apr�s la g�n�ration de l'activit�, vous devrez aller dans le param�trage de l'activit� > Onglet Calendrier
        pour param�trer les dates d'ouverture. Cliquez simplement dans les cases pour ouvrir les dates souhait�es.
        """) % Chemins.GetStaticPath("Images/16x16/Astuce.png")
        self.Ajouter_question(ctrl=Assistant.CTRL_Html, texte=texte, size=(-1, 50))

    def Suite(self):
        DB = GestionDB.DB()
        self.parent.Sauvegarde_standard(DB)
        IDactivite = self.parent.dict_valeurs["IDactivite"]


        # Unit�s de consommation
        listeIDunite = []
        listeDonnees = [
            ("IDactivite", IDactivite),
            ("nom", _(u"Repas")),
            ("abrege", _(u"R")),
            ("type", "Unitaire"),
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
            ("nom", _(u"Repas")),
            ("abrege", _(u"R")),
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
        nom_tarif = self.parent.dict_valeurs["nom"]
        listeDonnees = [("IDactivite", IDactivite), ("nom", _(u"Repas"))]
        IDnom_tarif = DB.ReqInsert("noms_tarifs", listeDonnees)

        # Cat�gories de tarifs
        listeCategoriesEtTarifs = []

        # Si cat�gorie unique
        if self.parent.dict_valeurs["has_categories_tarifs"] == False :
            listeDonnees = [("IDactivite", IDactivite), ("nom", _(u"Cat�gorie unique"))]
            IDcategorie_tarif = DB.ReqInsert("categories_tarifs", listeDonnees)
            track_tarif = self.parent.dict_valeurs["tarif"]
            listeCategoriesEtTarifs.append((IDcategorie_tarif, track_tarif))

        # Si plusieurs cat�gories
        if self.parent.dict_valeurs["has_categories_tarifs"] == True :
            nbre_categories_tarifs = self.parent.dict_valeurs["nbre_categories_tarifs"]
            for index in range(1, nbre_categories_tarifs+1):
                nom_categorie_tarif = self.parent.dict_valeurs["nom_categorie_tarif#%d" % index]
                listeDonnees = [("IDactivite", IDactivite), ("nom", nom_categorie_tarif)]
                IDcategorie_tarif = DB.ReqInsert("categories_tarifs", listeDonnees)
                track_tarif = self.parent.dict_valeurs["tarif#%d" % index]
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
                "etats" : "reservation;present;absenti",
                "label_prestation" : "nom_tarif",
                "combi_tarifs" : [{"type": "JOURN", "unites": [IDunite,]},],
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
