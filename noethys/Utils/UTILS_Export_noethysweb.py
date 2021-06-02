#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
#------------------------------------------------------------------------
# Application :    Noethys, gestion multi-activit�s
# Site internet :  www.noethys.com
# Auteur:          Ivan LUCAS
# Copyright:       (c) 2010-20 Ivan LUCAS
# Licence:         Licence GNU GPL
#------------------------------------------------------------------------

import Chemins
import wx
import six, os, copy, json, datetime, uuid, base64, re, shutil
import GestionDB
from Data.DATA_Tables import DB_DATA as DICT_CHAMPS
from PIL import Image
from Utils import UTILS_Fichiers, UTILS_Cryptage_fichier



def Rgb2hex(texte=""):
    """ Convertit une couleur RGB en HEX """
    try:
        r, g, b = [int(x) for x in texte[1:-1].split(",")]
        return "#{:02x}{:02x}{:02x}".format(r, g, b)
    except:
        return None


class Table():
    def __init__(self, parent=None, nom_table="",
                 nouveau_nom_table="",
                 exclure_champs=[],
                 nouveaux_noms_champs={},
                 dict_types_champs={},
                 nouveaux_champs=[],
                 champs_images=[]):
        self.parent = parent
        self.nom_table = nom_table
        self.nouveau_nom_table = nouveau_nom_table
        self.exclure_champs = exclure_champs
        self.nouveaux_noms_champs = nouveaux_noms_champs
        self.dict_types_champs = dict_types_champs
        self.nouveaux_champs = nouveaux_champs
        self.champs_images = champs_images

        # Recherche des donn�es
        self.liste_objets = self.Get_data()

    def Get_data(self):
        # Liste des champs
        listeChamps = []
        for nom, type_champ, info in DICT_CHAMPS[self.nom_table]:
            listeChamps.append(nom)

        # Lecture table
        req = "SELECT %s FROM %s;" % (", ".join(listeChamps), self.nom_table)
        self.parent.DB.ExecuterReq(req)
        liste_donnees = self.parent.DB.ResultatReq()
        liste_objets = []
        for objet in liste_donnees:
            dictTemp = {
                "pk": objet[0],
                "model": self.nouveau_nom_table,
                "fields": {},
            }
            dictData = copy.copy(dictTemp)
            for index, nom_champ in enumerate(listeChamps):
                valeur = objet[index]

                if nom_champ not in self.exclure_champs:

                    # Fonction personnalis�e
                    if hasattr(self, nom_champ):
                        valeur = getattr(self, nom_champ)(valeur=valeur)

                    # Changement du nom du champ
                    if nom_champ in self.nouveaux_noms_champs:
                        nom_champ = self.nouveaux_noms_champs[nom_champ]

                    # Changement du type de valeur
                    if nom_champ in self.dict_types_champs:
                        valeur = self.dict_types_champs[nom_champ](valeur)

                    # Si image
                    if valeur and nom_champ in self.champs_images:
                        rep_images = self.nom_table
                        rep_images_complet = os.path.join(self.parent.rep_medias, rep_images)

                        # Cr�ation du r�pertoire images
                        if not os.path.exists(rep_images_complet):
                            os.makedirs(rep_images_complet)

                        # Ouverture de l'image
                        image = Image.open(six.BytesIO(valeur))

                        # Cr�ation du nom du fichier image
                        nom_fichier_image = u"%s.%s" % (uuid.uuid4(), image.format.lower())

                        # Sauvegarde de l'image dans le r�pertoire
                        image.save(os.path.join(rep_images_complet, nom_fichier_image), format=image.format)
                        valeur = rep_images + "/" + nom_fichier_image

                    # M�morisation de la valeur
                    dictTemp["fields"][nom_champ.lower()] = valeur
                    dictData["fields"][nom_champ.lower()] = valeur

                dictData[nom_champ] = valeur

            # Si nouveaux champs
            for nom_champ in self.nouveaux_champs:
                valeur = None
                if hasattr(self, nom_champ):
                    valeur = getattr(self, nom_champ)(data=dictData)
                dictTemp["fields"][nom_champ.lower()] = valeur

            # M�morisation de l'objet
            liste_objets.append(dictTemp)

        return liste_objets

    def Get_objets(self):
        return self.liste_objets


class MyEncoder(json.JSONEncoder):
    def default(self, objet):
        # Si datetime.date
        if isinstance(objet, datetime.date):
            return six.text_type(objet)
        # Si datetime.datetime
        elif isinstance(objet, datetime.datetime):
            return six.text_type(objet)
        return json.JSONEncoder.default(self, objet)


class Export:
    def __init__(self, dlg=None, nom_fichier="", mdp=None):
        self.dlg = dlg
        self.nom_fichier = nom_fichier
        self.mdp = mdp
        self.liste_objets = []

        # Cr�ation du r�pertoire de travail
        self.rep = UTILS_Fichiers.GetRepTemp(fichier="noethysweb")
        if not os.path.exists(self.rep):
            os.makedirs(self.rep)

        # Cr�ation du r�pertoire medias
        self.rep_medias = os.path.join(self.rep, "media")
        if not os.path.exists(self.rep_medias):
            os.makedirs(self.rep_medias)

    def Ajouter(self, table=None):
        self.liste_objets.extend(table.Get_objets())

    def Finaliser(self):
        # Cr�ation du fichier json
        nom_fichier_json = os.path.join(self.rep, "core.json")
        with open(nom_fichier_json, 'w') as outfile:
            json.dump(self.liste_objets, outfile, cls=MyEncoder)

        # with io.open(self.nom_fichier, encoding='utf-8') as f:
        #     f.write(json.dumps(self.liste_objets, cls=MyEncoder, ensure_ascii=False))

        # Cr�ation du ZIP
        fichier_zip = shutil.make_archive(UTILS_Fichiers.GetRepTemp("exportweb"), 'zip', self.rep)

        # Crypte le fichier
        UTILS_Cryptage_fichier.CrypterFichier(fichier_zip, self.nom_fichier, self.mdp, ancienne_methode=False)

        # Nettoyage
        shutil.rmtree(self.rep)
        os.remove(fichier_zip)

        return True

class Export_all(Export):
    def __init__(self, *args, **kwds):
        Export.__init__(self, *args, **kwds)

        # Ouverture de la DB
        self.DB = GestionDB.DB()

        # R�cup�ration des comptes payeurs
        req = """SELECT IDcompte_payeur, IDfamille FROM comptes_payeurs;"""
        self.DB.ExecuterReq(req)
        self.dictComptesPayeurs = {}
        for IDcompte_payeur, IDfamille in self.DB.ResultatReq():
            self.dictComptesPayeurs[IDcompte_payeur] = IDfamille

        # Tables � exporter
        self.Ajouter(Table(self, nom_table="categories_medicales", nouveau_nom_table="core.CategorieMedicale"))

        self.Ajouter(Table(self, nom_table="categories_travail", nouveau_nom_table="core.CategorieTravail"))

        self.Ajouter(Table(self, nom_table="lots_factures", nouveau_nom_table="core.LotFactures"))

        self.Ajouter(Table(self, nom_table="lots_rappels", nouveau_nom_table="core.LotRappels"))

        self.Ajouter(Table(self, nom_table="factures_prefixes", nouveau_nom_table="core.PrefixeFacture"))

        self.Ajouter(Table(self, nom_table="factures_messages", nouveau_nom_table="core.MessageFacture"))

        self.Ajouter(Table(self, nom_table="comptes_bancaires", nouveau_nom_table="core.CompteBancaire", dict_types_champs={"defaut": bool}))

        self.Ajouter(Table(self, nom_table="modes_reglements", nouveau_nom_table="core.ModeReglement", champs_images=["image"]))

        self.Ajouter(Table(self, nom_table="emetteurs", nouveau_nom_table="core.Emetteur", nouveaux_noms_champs={"IDmode": "mode"}, champs_images=["image"]))

        self.Ajouter(Table(self, nom_table="medecins", nouveau_nom_table="core.Medecin"))

        self.Ajouter(Table(self, nom_table="niveaux_scolaires", nouveau_nom_table="core.NiveauScolaire"))

        self.Ajouter(Table(self, nom_table="organisateur", nouveau_nom_table="core.Organisateur", champs_images=["logo"]))

        self.Ajouter(Table(self, nom_table="regimes", nouveau_nom_table="core.Regime"))

        self.Ajouter(Table(self, nom_table="caisses", nouveau_nom_table="core.Caisse", nouveaux_noms_champs={"IDregime": "regime"}))

        self.Ajouter(Table(self, nom_table="types_pieces", nouveau_nom_table="core.TypePiece", dict_types_champs={"valide_rattachement": bool}))

        self.Ajouter(Table(self, nom_table="types_quotients", nouveau_nom_table="core.TypeQuotient"))

        self.Ajouter(Table(self, nom_table="vacances", nouveau_nom_table="core.Vacance"))

        self.Ajouter(Table(self, nom_table="jours_feries", nouveau_nom_table="core.Ferie"))

        self.Ajouter(Table(self, nom_table="secteurs", nouveau_nom_table="core.Secteur"))

        self.Ajouter(Table(self, nom_table="types_maladies", nouveau_nom_table="core.TypeMaladie"))

        self.Ajouter(Table(self, nom_table="types_sieste", nouveau_nom_table="core.TypeSieste"))

        self.Ajouter(Table(self, nom_table="types_vaccins", nouveau_nom_table="core.TypeVaccin"))

        self.Ajouter(Table_ecoles(self, nom_table="ecoles", nouveau_nom_table="core.Ecole"))

        self.Ajouter(Table_classes(self, nom_table="classes", nouveau_nom_table="core.Classe", nouveaux_noms_champs={"IDecole": "ecole"}))

        self.Ajouter(Table(self, nom_table="types_cotisations", nouveau_nom_table="core.TypeCotisation", dict_types_champs={"carte": bool, "defaut": bool}))

        self.Ajouter(Table(self, nom_table="unites_cotisations", nouveau_nom_table="core.UniteCotisation", nouveaux_noms_champs={"IDtype_cotisation": "type_cotisation"}, dict_types_champs={"defaut": bool}))

        self.Ajouter(Table(self, nom_table="messages_categories", nouveau_nom_table="core.MessageCategorie", dict_types_champs={"afficher_accueil": bool, "afficher_liste": bool}))

        self.Ajouter(Table(self, nom_table="listes_diffusion", nouveau_nom_table="core.ListeDiffusion"))

        self.Ajouter(Table(self, nom_table="restaurateurs", nouveau_nom_table="core.Restaurateur"))

        self.Ajouter(Table(self, nom_table="menus_categories", nouveau_nom_table="core.MenuCategorie"))

        self.Ajouter(Table(self, nom_table="menus_legendes", nouveau_nom_table="core.MenuLegende"))

        self.Ajouter(Table(self, nom_table="types_groupes_activites", nouveau_nom_table="core.TypeGroupeActivite"))

        self.Ajouter(Table(self, nom_table="factures_regies", nouveau_nom_table="core.FactureRegie", nouveaux_noms_champs={"IDcompte_bancaire": "compte_bancaire"}))

        self.Ajouter(Table_activites(self, nom_table="activites", nouveau_nom_table="core.Activite",
                           exclure_champs=["public", "psu_activation", "psu_unite_prevision", "psu_unite_presence", "psu_tarif_forfait", "psu_etiquette_rtt"],
                           dict_types_champs={"coords_org": bool, "logo_org": bool, "vaccins_obligatoires": bool, "portail_inscriptions_affichage": bool,
                                              "portail_reservations_affichage": bool, "portail_unites_multiples": bool, "inscriptions_multiples": bool},
                           nouveaux_champs=["pieces", "groupes_activites", "cotisations"], champs_images=["logo"]))

        self.Ajouter(Table(self, nom_table="responsables_activite", nouveau_nom_table="core.ResponsableActivite", nouveaux_noms_champs={"IDactivite": "activite"}, dict_types_champs={"defaut": bool}))

        self.Ajouter(Table(self, nom_table="agrements", nouveau_nom_table="core.Agrement", nouveaux_noms_champs={"IDactivite": "activite"}))

        self.Ajouter(Table(self, nom_table="groupes", nouveau_nom_table="core.Groupe", nouveaux_noms_champs={"IDactivite": "activite"}))

        self.Ajouter(Table_unites(self, nom_table="unites", nouveau_nom_table="core.Unite", nouveaux_noms_champs={"IDactivite": "activite", "IDrestaurateur": "restaurateur"},
                                  dict_types_champs={"heure_debut_fixe": bool, "heure_fin_fixe": bool, "repas": bool, "autogen_active": bool},
                                  nouveaux_champs=["groupes", "incompatibilites"]))

        self.Ajouter(Table_unites_remplissage(self, nom_table="unites_remplissage", nouveau_nom_table="core.UniteRemplissage", nouveaux_noms_champs={"IDactivite": "activite"},
                                  exclure_champs=["etiquettes"],
                                  dict_types_champs={"afficher_page_accueil": bool, "afficher_grille_conso": bool},
                                  nouveaux_champs=["unites"]))

        self.Ajouter(Table(self, nom_table="categories_tarifs", nouveau_nom_table="core.CategorieTarif", nouveaux_noms_champs={"IDactivite": "activite"}))

        self.Ajouter(Table(self, nom_table="noms_tarifs", nouveau_nom_table="core.NomTarif", nouveaux_noms_champs={"IDactivite": "activite"},
                           exclure_champs=["IDcategorie_tarif"]))

        self.Ajouter(Table_tarifs(self, nom_table="tarifs", nouveau_nom_table="core.Tarif", nouveaux_noms_champs={"IDactivite": "activite", "IDnom_tarif": "nom_tarif", "IDtype_quotient": "type_quotient"},
                                  exclure_champs=["IDcategorie_tarif", "condition_nbre_combi", "condition_periode", "condition_nbre_jours", "condition_conso_facturees", "condition_dates_continues", "etiquettes", "IDevenement", "IDproduit"],
                                  dict_types_champs={"forfait_saisie_manuelle": bool, "forfait_saisie_auto": bool, "forfait_suppression_auto": bool}))

        self.Ajouter(Table(self, nom_table="tarifs_lignes", nouveau_nom_table="core.TarifLigne", nouveaux_noms_champs={"IDactivite": "activite", "IDtarif": "tarif"},
                                  exclure_champs=["IDmodele"]))

        self.Ajouter(Table_combi_tarifs(self, nom_table="combi_tarifs", nouveau_nom_table="core.CombiTarif", nouveaux_noms_champs={"IDtarif": "tarif", "IDgroupe": "groupe"},
                                        nouveaux_champs=["unites"]))

        self.Ajouter(Table(self, nom_table="ouvertures", nouveau_nom_table="core.Ouverture", nouveaux_noms_champs={"IDactivite": "activite", "IDunite": "unite", "IDgroupe": "groupe"}))

        self.Ajouter(Table(self, nom_table="remplissage", nouveau_nom_table="core.Remplissage", nouveaux_noms_champs={"IDactivite": "activite", "IDunite_remplissage": "unite_remplissage", "IDgroupe": "groupe"}))

        self.Ajouter(Table_individus(self, nom_table="individus", nouveau_nom_table="core.Individu", nouveaux_noms_champs={"IDcivilite": "civilite", "IDnationalite": "idnationalite", "IDsecteur": "secteur", "IDcategorie_travail": "categorie_travail", "IDmedecin": "medecin", "IDtype_sieste": "type_sieste"},
                                     exclure_champs=["num_secu"], dict_types_champs={"deces": bool, "travail_tel_sms": bool, "tel_domicile_sms": bool, "tel_mobile_sms": bool},
                                     nouveaux_champs=["photo", "listes_diffusion"]))

        self.Ajouter(Table(self, nom_table="scolarite", nouveau_nom_table="core.Scolarite", nouveaux_noms_champs={"IDindividu": "individu", "IDecole": "ecole", "IDclasse": "classe", "IDniveau": "niveau"}))

        self.Ajouter(Table_familles(self, nom_table="familles", nouveau_nom_table="core.Famille",
                            nouveaux_noms_champs={"IDcaisse": "caisse", "code_comptable": "code_compta"},
                           exclure_champs=["IDcompte_payeur", "prelevement_activation", "prelevement_etab", "prelevement_guichet", "prelevement_numero", "prelevement_cle",
                                           "prelevement_banque", "prelevement_individu", "prelevement_nom", "prelevement_rue", "prelevement_cp", "prelevement_ville",
                                           "prelevement_cle_iban", "prelevement_iban", "prelevement_bic", "prelevement_reference_mandat", "prelevement_date_mandat", "prelevement_memo",
                                           "autre_adresse_facturation"],
                            nouveaux_champs=["email_factures_adresses", "email_recus_adresses", "email_depots_adresses"],
                           dict_types_champs={"autorisation_cafpro": bool, "internet_actif": bool}))

        self.Ajouter(Table(self, nom_table="evenements", nouveau_nom_table="core.Evenement", nouveaux_noms_champs={"IDactivite": "activite", "IDgroupe": "groupe", "IDunite": "unite"}))

        self.Ajouter(Table(self, nom_table="inscriptions",
                           nouveau_nom_table="core.Inscription",
                           nouveaux_noms_champs={"IDindividu": "individu", "IDfamille": "famille", "IDactivite": "activite", "IDgroupe": "groupe", "IDcategorie_tarif": "categorie_tarif",
                                                 "date_inscription": "date_debut", "date_desinscription": "date_fin"},
                           exclure_champs=["IDcompte_payeur", "parti"]))

        self.Ajouter(Table_consommations(self, nom_table="consommations",
                           nouveau_nom_table="core.Consommation",
                           nouveaux_noms_champs={"IDindividu": "individu", "IDinscription": "inscription", "IDactivite": "activite", "IDunite": "unite", "IDgroupe": "groupe", "IDcategorie_tarif": "categorie_tarif", "IDprestation": "prestation", "IDevenement": "evenement"},
                           exclure_champs=["verrouillage", "IDutilisateur", "IDcompte_payeur", "etiquettes"]))

        # Les m�mo ne sont plus compatibles car associ�s d�sormais � l'inscription
        # self.Ajouter(Table(self, nom_table="memo_journee",
        #                    nouveau_nom_table="core.MemoJournee",
        #                    nouveaux_noms_champs={"IDindividu": "individu"}))

        self.Ajouter(Table_problemes_sante(self, nom_table="problemes_sante",
                           nouveau_nom_table="core.ProblemeSante",
                           nouveaux_noms_champs={"IDindividu": "individu", "IDtype": "categorie"},
                            dict_types_champs={"traitement_medical": bool, "eviction": bool, "diffusion_listing_enfants": bool, "diffusion_listing_conso": bool, "diffusion_listing_repas": bool}))

        self.Ajouter(Table(self, nom_table="vaccins", nouveau_nom_table="core.Vaccin", nouveaux_noms_champs={"IDindividu": "individu", "IDtype_vaccin": "type_vaccin"}))

        self.Ajouter(Table(self, nom_table="messages", nouveau_nom_table="core.Message", nouveaux_noms_champs={"IDcategorie": "categorie", "IDindividu": "individu", "IDfamille": "famille"},
                           exclure_champs=["IDutilisateur"],
                           dict_types_champs={"afficher_accueil": bool, "afficher_liste": bool, "rappel": bool, "afficher_facture": bool, "rappel_famille": bool, "afficher_commande": bool}))

        self.Ajouter(Table(self, nom_table="rattachements", nouveau_nom_table="core.Rattachement", nouveaux_noms_champs={"IDindividu": "individu", "IDfamille": "famille", "IDcategorie": "categorie"},
                           dict_types_champs={"titulaire": bool}))

        self.Ajouter(Table(self, nom_table="pieces", nouveau_nom_table="core.Piece", nouveaux_noms_champs={"IDindividu": "individu", "IDfamille": "famille", "IDtype_piece": "type_piece"}))

        self.Ajouter(Table_factures(self, nom_table="factures", nouveau_nom_table="core.Facture", nouveaux_noms_champs={"IDfamille": "famille", "IDregie": "regie", "IDlot": "lot", "IDprefixe": "prefixe"},
                            exclure_champs=["IDcompte_payeur", "IDutilisateur", "etat", "mention1", "mention2", "mention3"],
                            nouveaux_champs=["famille"]))

        self.Ajouter(Table_prestations(self, nom_table="prestations", nouveau_nom_table="core.Prestation", nouveaux_noms_champs={"IDactivite": "activite", "IDtarif": "tarif", "IDfacture": "facture", "IDfamille": "famille",
                           "IDindividu": "individu", "IDcategorie_tarif": "categorie_tarif", "code_comptable": "code_compta"},
                           exclure_champs=["IDcompte_payeur", "forfait_date_debut", "forfait_date_fin", "reglement_frais", "IDcontrat", "IDdonnee"]))

        self.Ajouter(Table(self, nom_table="depots_cotisations", nouveau_nom_table="core.DepotCotisations", dict_types_champs={"verrouillage": bool}, nouveaux_noms_champs={"IDdepot_cotisation": "iddepot"})),

        self.Ajouter(Table_cotisations(self, nom_table="cotisations", nouveau_nom_table="core.Cotisation", nouveaux_noms_champs={"IDfamille": "famille", "IDindividu": "individu",
                                     "IDtype_cotisation": "type_cotisation", "IDunite_cotisation": "unite_cotisation", "IDdepot_cotisation": "depot_cotisation", "IDprestation": "prestation"},
                                      exclure_champs=["IDutilisateur"]))

        # self.Ajouter(Table_aides(self, nom_table="aides", nouveau_nom_table="core.Aide", nouveaux_noms_champs={"IDfamille": "famille", "IDactivite": "activite", "IDcaisse": "caisse"},
        #                          nouveaux_champs=["individus"]))

        # self.Ajouter(Table_combi_aides(self, nom_table="aides_combinaisons", nouveau_nom_table="core.CombiAide", nouveaux_noms_champs={"IDaide": "aide"},
        #                          exclure_champs=["IDaide_montant"], nouveaux_champs=["montant", "unites"]))

        self.Ajouter(Table(self, nom_table="quotients", nouveau_nom_table="core.Quotient", nouveaux_noms_champs={"IDfamille": "famille", "IDtype_quotient": "type_quotient"}))

        # self.Ajouter(Table(self, nom_table="deductions", nouveau_nom_table="core.Deduction", nouveaux_noms_champs={"IDprestation": "prestation", "IDfamille": "famille", "IDaide": "aide"},
        #                    exclure_champs=["IDcompte_payeur"],))

        self.Ajouter(Table_documents_modeles(self, nom_table="documents_modeles", nouveau_nom_table="core.ModeleDocument", exclure_champs=["IDdonnee", "supprimable", "observations"],
                                            nouveaux_noms_champs={"IDfond": "fond"}, dict_types_champs={"defaut": bool}, nouveaux_champs=["objets"]))

        self.Ajouter(Table_questions(self, nom_table="questionnaire_questions", nouveau_nom_table="core.QuestionnaireQuestion", exclure_champs=["defaut"],
                                            nouveaux_noms_champs={"IDcategorie": "categorie"}, dict_types_champs={"visible": bool}, nouveaux_champs=["choix"]))

        self.Ajouter(Table_reponses(self, nom_table="questionnaire_reponses", nouveau_nom_table="core.QuestionnaireReponse", exclure_champs=["type", "IDdonnee"],
                                            nouveaux_noms_champs={"IDquestion": "question", "IDindividu": "individu", "IDfamille": "famille"}))

        self.Ajouter(Table_payeurs(self, nom_table="payeurs", nouveau_nom_table="core.Payeur", exclure_champs=["IDcompte_payeur"],
                                        nouveaux_champs=["famille"]))

        self.Ajouter(Table(self, nom_table="depots", nouveau_nom_table="core.Depot", dict_types_champs={"verrouillage": bool},
                                    nouveaux_noms_champs={"IDcompte": "compte"})),

        self.Ajouter(Table_reglements(self, nom_table="reglements", nouveau_nom_table="core.Reglement",
                                            exclure_champs=["IDcompte_payeur", "IDprestation_frais", "IDutilisateur", "IDprelevement", "IDpiece"],
                                            nouveaux_noms_champs={"IDmode": "mode", "IDemetteur": "emetteur", "IDpayeur": "payeur", "IDcompte": "compte", "IDdepot": "depot"},
                                            nouveaux_champs=["famille"]))

        self.Ajouter(Table_ventilation(self, nom_table="ventilation", nouveau_nom_table="core.Ventilation",
                                            exclure_champs=["IDcompte_payeur"],
                                            nouveaux_noms_champs={"IDreglement": "reglement", "IDprestation": "prestation"},
                                            nouveaux_champs=["famille"]))

        self.Ajouter(Table_recus(self, nom_table="recus", nouveau_nom_table="core.Recu",
                                            exclure_champs=["IDutilisateur"],
                                            nouveaux_noms_champs={"IDfamille": "famille", "IDreglement": "reglement"}))

        self.Ajouter(Table(self, nom_table="attestations", nouveau_nom_table="core.Attestation",
                                            exclure_champs=["IDutilisateur"],
                                            nouveaux_noms_champs={"IDfamille": "famille"}))

        self.Ajouter(Table(self, nom_table="devis", nouveau_nom_table="core.Devis",
                                            exclure_champs=["IDutilisateur"],
                                            nouveaux_noms_champs={"IDfamille": "famille"}))

        self.Ajouter(Table_textes_rappels(self, nom_table="textes_rappels", nouveau_nom_table="core.ModeleRappel",
                                            exclure_champs=["texte_xml", "texte_pdf"],
                                            nouveaux_champs=["html"]))

        self.Ajouter(Table_rappels(self, nom_table="rappels", nouveau_nom_table="core.Rappel",
                                            exclure_champs=["IDutilisateur", "IDcompte_payeur"],
                                            nouveaux_noms_champs={"IDtexte": "modele", "IDlot": "lot"},
                                            nouveaux_champs=["famille"]))

        self.Ajouter(Table_modeles_emails(self, nom_table="modeles_emails", nouveau_nom_table="core.ModeleEmail",
                                            dict_types_champs={"defaut": bool},
                                            exclure_champs=["IDadresse", "texte_xml"],
                                            nouveaux_champs=["html"]))

        self.Ajouter(Table(self, nom_table="liens", nouveau_nom_table="core.Lien", dict_types_champs={"responsable": bool},
                                            nouveaux_noms_champs={"IDfamille": "famille", "IDindividu_sujet": "individu_sujet", "IDindividu_objet": "individu_objet",
                                                                  "IDtype_lien": "idtype_lien", "IDautorisation": "autorisation"})),

        self.Ajouter(Table(self, nom_table="adresses_mail", nouveau_nom_table="core.AdresseMail", dict_types_champs={"use_ssl": bool, "defaut": bool, "use_tls": bool},
                                            nouveaux_noms_champs={"smtp": "hote", "connexionssl": "use_ssl", "startTLS": "use_tls"},
                                            exclure_champs=["connexionAuthentifiee"])),

        self.Ajouter(Table(self, nom_table="contacts", nouveau_nom_table="core.Contact")),

        self.DB.Close()
        self.Finaliser()



class Table_ecoles(Table):
    def secteurs(self, valeur=None):
        """ Champ ManyToMany"""
        liste_secteurs = []
        if valeur:
            for IDsecteur in valeur.split(";"):
                liste_secteurs.append(int(IDsecteur))
        return liste_secteurs

class Table_classes(Table):
    def niveaux(self, valeur=None):
        """ Champ ManyToMany"""
        liste_niveaux = []
        if valeur:
            for IDniveau in valeur.split(";"):
                liste_niveaux.append(int(IDniveau))
        return liste_niveaux


class Table_activites(Table):
    def __init__(self, parent, **kwds):
        self.parent = parent

        # R�cup�ration des types de groupes d'activit�s
        req = """SELECT IDtype_groupe_activite, nom FROM types_groupes_activites;"""
        self.parent.DB.ExecuterReq(req)
        self.liste_types_groupes_activites = []
        for IDtype_groupe_activite, nom in self.parent.DB.ResultatReq():
            self.liste_types_groupes_activites.append(IDtype_groupe_activite)

        Table.__init__(self, parent, **kwds)

    def groupes_activites(self, data={}):
        """ Champ ManyToMany"""
        req = """SELECT IDtype_groupe_activite, IDactivite FROM groupes_activites WHERE IDactivite=%d;""" % data["pk"]
        self.parent.DB.ExecuterReq(req)
        return [IDtype_groupe_activite for IDtype_groupe_activite, IDactivite in self.parent.DB.ResultatReq() if IDtype_groupe_activite in self.liste_types_groupes_activites]

    def pieces(self, data={}):
        """ Champ ManyToMany"""
        req = """SELECT IDactivite, IDtype_piece FROM pieces_activites WHERE IDactivite=%d;""" % data["pk"]
        self.parent.DB.ExecuterReq(req)
        return [IDtype_piece for IDactivite, IDtype_piece in self.parent.DB.ResultatReq()]

    def cotisations(self, data={}):
        """ Champ ManyToMany"""
        req = """SELECT IDactivite, IDtype_cotisation FROM cotisations_activites WHERE IDactivite=%d;""" % data["pk"]
        self.parent.DB.ExecuterReq(req)
        return [IDtype_cotisation for IDactivite, IDtype_cotisation in self.parent.DB.ResultatReq()]

    def inscriptions_multiples(self, valeur=None):
        if valeur:
            return True
        return False


class Table_unites(Table):
    def groupes(self, data={}):
        """ Champ ManyToMany"""
        req = """SELECT IDunite, IDgroupe FROM unites_groupes WHERE IDunite=%d;""" % data["pk"]
        self.parent.DB.ExecuterReq(req)
        return [IDgroupe for IDunite, IDgroupe in self.parent.DB.ResultatReq()]

    def incompatibilites(self, data={}):
        """ Champ ManyToMany"""
        req = """SELECT IDunite, IDunite_incompatible FROM unites_incompat WHERE IDunite=%d;""" % data["pk"]
        self.parent.DB.ExecuterReq(req)
        return [IDunite_incompatible for IDunite, IDunite_incompatible in self.parent.DB.ResultatReq()]

class Table_unites_remplissage(Table):
    def unites(self, data={}):
        """ Champ ManyToMany"""
        req = """SELECT IDunite_remplissage, IDunite FROM unites_remplissage_unites WHERE IDunite=%d;""" % data["pk"]
        self.parent.DB.ExecuterReq(req)
        return [IDunite for IDunite_remplissage, IDunite in self.parent.DB.ResultatReq()]

class Table_tarifs(Table):
    def categories_tarifs(self, valeur=None):
        """ Champ ManyToMany"""
        liste_categories = []
        if valeur:
            for IDcategorie_tarif in valeur.split(";"):
                liste_categories.append(int(IDcategorie_tarif))
        return liste_categories

    def groupes(self, valeur=None):
        """ Champ ManyToMany"""
        liste_groupes = []
        if valeur:
            for IDgroupe in valeur.split(";"):
                liste_groupes.append(int(IDgroupe))
        return liste_groupes

    def cotisations(self, valeur=None):
        """ Champ ManyToMany"""
        liste_cotisations = []
        if valeur:
            for IDcotisation in valeur.split(";"):
                liste_cotisations.append(int(IDcotisation))
        return liste_cotisations

    def caisses(self, valeur=None):
        """ Champ ManyToMany"""
        liste_caisses = []
        if valeur:
            for IDcaisse in valeur.split(";"):
                liste_caisses.append(int(IDcaisse))
        return liste_caisses

    def etats(self, valeur=None):
        if valeur:
            valeur = valeur.replace(";", ",")
        return valeur


class Table_combi_tarifs(Table):
    def unites(self, data={}):
        """ Champ ManyToMany"""
        req = """SELECT IDcombi_tarif, IDunite FROM combi_tarifs_unites WHERE IDcombi_tarif=%d;""" % data["pk"]
        self.parent.DB.ExecuterReq(req)
        return [IDunite for IDcombi_tarif, IDunite in self.parent.DB.ResultatReq()]


class Table_familles(Table):
    def __init__(self, parent, **kwds):
        self.parent = parent

        # R�cup�ration des allocataires
        req = """SELECT IDindividu, nom FROM individus;"""
        self.parent.DB.ExecuterReq(req)
        self.liste_individus = []
        for IDindividu, nom in self.parent.DB.ResultatReq():
            self.liste_individus.append(IDindividu)

        Table.__init__(self, parent, **kwds)

    def allocataire(self, valeur=None):
        if valeur and valeur in self.liste_individus:
            return valeur
        return None

    def email_factures(self, valeur=None):
        if valeur:
            return True
        return False

    def email_recus(self, valeur=None):
        if valeur:
            return True
        return False

    def email_depots(self, valeur=None):
        if valeur:
            return True
        return False

    def email_factures_adresses(self, data={}):
        return data["email_factures"]

    def email_recus_adresses(self, data={}):
        return data["email_recus"]

    def email_depots_adresses(self, data={}):
        return data["email_depots"]




class Table_individus(Table):
    def __init__(self, parent, **kwds):
        self.parent = parent
        # Importation de toutes les photos
        DB_photos = GestionDB.DB(suffixe="PHOTOS")
        req = """SELECT IDindividu, photo FROM photos;"""
        DB_photos.ExecuterReq(req)
        listePhotos = DB_photos.ResultatReq()
        DB_photos.Close()
        self.dictPhotos = {}
        for IDindividu, photo in listePhotos:
            self.dictPhotos[IDindividu] = photo

        # Cr�ation du r�pertoire photos
        self.rep_images = "individus"
        self.rep_images_complet = os.path.join(self.parent.rep_medias, self.rep_images)

        # Cr�ation du r�pertoire images
        if not os.path.exists(self.rep_images_complet):
            os.makedirs(self.rep_images_complet)

        Table.__init__(self, parent, **kwds)

    def photo(self, data={}):
        IDindividu = data["pk"]
        if IDindividu in self.dictPhotos:
            image = Image.open(six.BytesIO(self.dictPhotos[IDindividu]))
            nom_fichier_image = u"%s.%s" % (uuid.uuid4(), image.format.lower())
            image.save(os.path.join(self.rep_images_complet, nom_fichier_image), format=image.format)
            valeur = os.path.join(self.rep_images, nom_fichier_image)
            return valeur
        return None

    def listes_diffusion(self, data={}):
        """ Champ ManyToMany"""
        req = """SELECT IDliste, IDindividu FROM abonnements WHERE IDindividu=%d;""" % data["pk"]
        self.parent.DB.ExecuterReq(req)
        return [IDliste for IDliste, IDindividu in self.parent.DB.ResultatReq()]


class Table_factures(Table):
    def famille(self, data={}):
        return self.parent.dictComptesPayeurs[data["IDcompte_payeur"]]



class Table_prestations(Table):
    def __init__(self, parent, **kwds):
        # Importe les factures
        req = """SELECT IDfacture, date_edition FROM factures;"""
        parent.DB.ExecuterReq(req)
        self.dictFactures = {}
        for IDfacture, date_edition in parent.DB.ResultatReq():
            self.dictFactures[IDfacture] = date_edition

        Table.__init__(self, parent, **kwds)

    def IDindividu(self, valeur=None):
        if valeur == 0:
            valeur = None
        return valeur

    def IDfacture(self, valeur=None):
        # V�rifie que la facture existe bien
        if valeur and valeur in self.dictFactures:
            return valeur
        return None

class Table_consommations(Table):
    def __init__(self, parent, **kwds):
        # Importe les prestations
        req = """SELECT IDprestation, date FROM prestations;"""
        parent.DB.ExecuterReq(req)
        self.dictPrestations = {}
        for IDprestation, date in parent.DB.ResultatReq():
            self.dictPrestations[IDprestation] = date

        Table.__init__(self, parent, **kwds)

    def IDprestation(self, valeur=None):
        # V�rifie que la prestation existe bien
        if valeur and valeur in self.dictPrestations:
            return valeur
        return None


class Table_cotisations(Table):
    def __init__(self, parent, **kwds):
        # Importe les prestations
        req = """SELECT IDprestation, date FROM prestations;"""
        parent.DB.ExecuterReq(req)
        self.dictPrestations = {}
        for IDprestation, date in parent.DB.ResultatReq():
            self.dictPrestations[IDprestation] = date

        Table.__init__(self, parent, **kwds)

    def activites(self, valeur=None):
        """ Champ ManyToMany"""
        liste_activites = []
        if valeur:
            for IDactivite in valeur.split(";"):
                liste_activites.append(int(IDactivite))
        return liste_activites

    def IDprestation(self, valeur=None):
        if valeur and valeur in self.dictPrestations:
            return valeur
        return None


class Table_problemes_sante(Table):
    def IDtype(self, valeur=None):
        if valeur == None:
            return 1
        return valeur


class Table_aides(Table):
    def individus(self, data={}):
        """ Champ ManyToMany"""
        req = """SELECT IDaide, IDindividu FROM aides_beneficiaires WHERE IDaide=%d;""" % data["pk"]
        self.parent.DB.ExecuterReq(req)
        return [IDindividu for IDaide, IDindividu in self.parent.DB.ResultatReq()]

class Table_combi_aides(Table):
    def __init__(self, parent, **kwds):
        self.parent = parent
        # Importation des montants
        req = """SELECT IDaide_combi, aides_montants.IDaide_montant, montant FROM aides_montants
        LEFT JOIN aides_combinaisons ON aides_combinaisons.IDaide_montant = aides_montants.IDaide_montant;"""
        self.parent.DB.ExecuterReq(req)
        self.dictMontants = {}
        for IDaide_combi, IDaide_montant, montant in self.parent.DB.ResultatReq():
            self.dictMontants[IDaide_combi] = montant
        # Importation des unit�s
        req = """SELECT IDaide_combi, IDunite FROM aides_combi_unites;"""
        self.parent.DB.ExecuterReq(req)
        self.dictUnites = {}
        for IDaide_combi, IDunite in self.parent.DB.ResultatReq():
            if IDaide_combi not in self.dictUnites:
                self.dictUnites[IDaide_combi] = []
            self.dictUnites[IDaide_combi].append(IDunite)
        Table.__init__(self, parent, **kwds)

    def montant(self, data={}):
        """ Champ ManyToMany"""
        IDaide_combi = data["pk"]
        if IDaide_combi in self.dictMontants:
            return self.dictMontants[IDaide_combi]
        return 0.0

    def unites(self, data={}):
        """ Champ ManyToMany"""
        IDaide_combi = data["pk"]
        if IDaide_combi in self.dictUnites:
            return self.dictUnites[IDaide_combi]
        return []



class Table_documents_modeles(Table):
    def __init__(self, parent, **kwds):
        self.parent = parent

        # Importation de tous les objets des mod�les
        listeChamps = []
        for nom, type_champ, info in DICT_CHAMPS["documents_objets"]:
            listeChamps.append(nom)
        req = "SELECT * FROM documents_objets ORDER BY ordre;"
        self.parent.DB.ExecuterReq(req)
        self.dict_objets = {}
        for objet in self.parent.DB.ResultatReq():
            dict_objet = {}
            for index in range(1, len(listeChamps)):
                nom_champ = listeChamps[index]
                dict_objet[nom_champ] = objet[index]
            if dict_objet["IDmodele"] not in self.dict_objets:
                self.dict_objets[dict_objet["IDmodele"]] = []
            self.dict_objets[dict_objet["IDmodele"]].append(dict_objet)

        Table.__init__(self, parent, **kwds)

    def IDfond(self, valeur=None):
        """ Changement de valeur par d�faut """
        if valeur == 0:
            valeur = None
        return valeur

    def objets(self, data={}):
        """ Cr�ation d'un champ suppl�mentaire """
        liste_objets = []
        IDmodele = data["pk"]
        if IDmodele in self.dict_objets:
            for dict_objet in self.dict_objets[IDmodele]:
                objet = None

                # Rectangle
                if dict_objet["categorie"] == "rectangle":
                    objet = json.loads("""{"type":"rect","version":"3.4.0","originX":"left","originY":"top","left":80,"top":123.5,"width":50,"height":50,"fill":"rgba(122,156,255,1)","stroke":"rgba(0,0,0,1)","strokeWidth":0,"strokeDashArray":null,"strokeLineCap":"butt","strokeDashOffset":0,"strokeLineJoin":"miter","strokeMiterLimit":4,"scaleX":1,"scaleY":1,"angle":0,"flipX":false,"flipY":false,"opacity":1,"shadow":null,"visible":true,"clipTo":null,"backgroundColor":"","fillRule":"nonzero","paintFirst":"fill","globalCompositeOperation":"source-over","transformMatrix":null,"skewX":0,"skewY":0,"rx":0,"ry":0,"nom":"Rectangle","categorie":"rectangle"}""")
                    objet = {
                        "type": "rect", "categorie": "rectangle", "nom": dict_objet["nom"],
                        "left": dict_objet["x"], "top": data["fields"]["hauteur"] - dict_objet["y"] - dict_objet["hauteur"], "width": dict_objet["largeur"], "height": dict_objet["hauteur"],
                        "fill": self.ConvertCouleur(dict_objet["coulRemplis"], transparent=dict_objet["largeur"] == 'Transparent'),
                        "strokeWidth": dict_objet["epaissTrait"], "stroke": self.ConvertCouleur(dict_objet["couleurTrait"]),
                        "strokeDashArray": self.ConvertTrait(dict_objet["styleTrait"]),
                    }

                # Cercle
                if dict_objet["categorie"] == "cercle":
                    objet = {
                        "type": "circle", "categorie": "cercle", "nom": dict_objet["nom"],
                        "left": dict_objet["x"], "top": data["fields"]["hauteur"] - dict_objet["y"] - dict_objet["hauteur"], "width": dict_objet["largeur"], "height": dict_objet["hauteur"],
                        "fill": self.ConvertCouleur(dict_objet["coulRemplis"], transparent=dict_objet["largeur"] == 'Transparent'),
                        "strokeWidth": dict_objet["epaissTrait"], "stroke": self.ConvertCouleur(dict_objet["couleurTrait"]),
                        "strokeDashArray": self.ConvertTrait(dict_objet["styleTrait"]),
                    }

                # Ligne
                if dict_objet["categorie"] == "ligne":
                    point1, point2 = dict_objet["points"][:-1].split(";")
                    x1, y1 = point1.split(",")
                    x2, y2 = point2.split(",")
                    top = data["fields"]["hauteur"] - dict_objet["y"]
                    objet = {
                        "type": "line", "categorie": "ligne", "nom": dict_objet["nom"],
                        "left": dict_objet["x"], "top": top, "width": float(x2) - float(x1), "height": top,
                        "fill": self.ConvertCouleur(dict_objet["coulRemplis"]),
                        "strokeWidth": dict_objet["epaissTrait"], "stroke": self.ConvertCouleur(dict_objet["couleurTrait"]),
                        "strokeDashArray": self.ConvertTrait(dict_objet["styleTrait"]),
                        "champ": dict_objet["champ"], "x1": float(x1), "y1": top, "x2": float(x2), "y2": top,
                    }

                # Texte
                if dict_objet["categorie"] == "bloc_texte":
                    top = data["fields"]["hauteur"] - dict_objet["y"]
                    objet = {
                        "type": "textbox", "categorie": "texte", "nom": dict_objet["nom"],
                        "fontFamily": "Arial", "fontSize": dict_objet["taillePolice"],
                        "left": dict_objet["x"], "top": top, "width": 500, "height": dict_objet["hauteur"],
                        "fill": self.ConvertCouleur(dict_objet["couleurTexte"]),
                        "text": dict_objet["texte"], "scaleX": 0.33, "scaleY": 0.33,
                    }

                # Image
                if dict_objet["categorie"] == "image" and dict_objet["typeImage"].startswith("fichier"):
                    image = Image.open(six.BytesIO(dict_objet["image"]))
                    taille_image = image.size
                    buffer = six.BytesIO()
                    image.save(buffer, format=image.format)
                    image64 = base64.b64encode(buffer.getvalue())

                    objet = json.loads("""{"type":"image","version":"3.4.0","originX":"left","originY":"top","left":41,"top":84.5,"width":128,"height":128,"fill":"rgb(0,0,0)","stroke":"rgba(0,0,0,0)","strokeWidth":0,"strokeDashArray":null,"strokeLineCap":"butt","strokeDashOffset":0,"strokeLineJoin":"miter","strokeMiterLimit":4,"scaleX":1,"scaleY":1,"angle":0,"flipX":false,"flipY":false,"opacity":1,"shadow":null,"visible":true,"clipTo":null,"backgroundColor":"","fillRule":"nonzero","paintFirst":"fill","globalCompositeOperation":"source-over","transformMatrix":null,"skewX":0,"skewY":0,"crossOrigin":"","cropX":0,"cropY":0,"nom":"Image","categorie":"image","src":"data:image/png;base64,X","filters":[]}""")
                    scaleY = 1.0 * dict_objet["hauteur"] / taille_image[1]
                    top = data["fields"]["hauteur"] - dict_objet["y"] - taille_image[1] * scaleY
                    objet.update({
                        "type": "image", "categorie": "logo", "nom": dict_objet["nom"],
                        "left": dict_objet["x"], "top": top, "width": taille_image[0], "height": taille_image[1],
                        "scaleX": scaleY, "scaleY": scaleY, "fill": self.ConvertCouleur(dict_objet["coulRemplis"]),
                        "strokeWidth": dict_objet["epaissTrait"], "stroke": self.ConvertCouleur(dict_objet["couleurTrait"]),
                        "strokeDashArray": self.ConvertTrait(dict_objet["styleTrait"]),
                        "src": "data:image/png;base64,%s" % image64
                    })

                # Photo individuelle
                if dict_objet["typeImage"] == "photo":
                    objet = json.loads("""{"type":"image","version":"3.4.0","originX":"left","originY":"top","left":3,"top":3,"width":128,"height":128,"fill":"rgb(0,0,0)","stroke":"rgba(0,0,0,0)","strokeWidth":0,"strokeDashArray":null,"strokeLineCap":"butt","strokeDashOffset":0,"strokeLineJoin":"miter","strokeMiterLimit":4,"scaleX":0.19,"scaleY":0.19,"angle":0,"flipX":false,"flipY":false,"opacity":1,"shadow":null,"visible":true,"clipTo":null,"backgroundColor":"","fillRule":"nonzero","paintFirst":"fill","globalCompositeOperation":"source-over","transformMatrix":null,"skewX":0,"skewY":0,"crossOrigin":"","cropX":0,"cropY":0,"nom":"Photo individuelle","categorie":"photo","src":"/static/images/femme.png","filters":[]}""")
                    scaleY = 1.0 * dict_objet["hauteur"] / 128
                    top = data["fields"]["hauteur"] - dict_objet["y"] - 128 * scaleY
                    objet.update({
                        "type": "image", "categorie": "photo", "nom": dict_objet["nom"],
                        "left": dict_objet["x"], "top": top, "width": 128, "height": 128,
                        "scaleX": scaleY, "scaleY": scaleY,
                        "fill": self.ConvertCouleur(dict_objet["coulRemplis"]),
                        "strokeWidth": dict_objet["epaissTrait"], "stroke": self.ConvertCouleur(dict_objet["couleurTrait"]),
                        "strokeDashArray": self.ConvertTrait(dict_objet["styleTrait"]),
                    })

                # Logo
                if dict_objet["typeImage"] == "logo":
                    req = "SELECT logo FROM organisateur WHERE IDorganisateur=1;"
                    self.parent.DB.ExecuterReq(req)
                    logo = self.parent.DB.ResultatReq()[0][0]
                    if logo != None:
                        io = six.BytesIO(logo)
                        if 'phoenix' in wx.PlatformInfo:
                            img = wx.Image(io, wx.BITMAP_TYPE_ANY)
                        else:
                            img = wx.ImageFromStream(io, wx.BITMAP_TYPE_ANY)
                        taille_logo = img.GetSize()

                        objet = json.loads("""{"type":"image","version":"3.4.0","originX":"left","originY":"top","left":11.49,"top":54.99,"width":500,"height":500,"fill":"rgb(0,0,0)","stroke":"rgba(0,0,0,0)","strokeWidth":0,"strokeDashArray":null,"strokeLineCap":"butt","strokeDashOffset":0,"strokeLineJoin":"miter","strokeMiterLimit":4,"scaleX":0.37,"scaleY":0.37,"angle":0,"flipX":false,"flipY":false,"opacity":1,"shadow":null,"visible":true,"clipTo":null,"backgroundColor":"","fillRule":"nonzero","paintFirst":"fill","globalCompositeOperation":"source-over","transformMatrix":null,"skewX":0,"skewY":0,"crossOrigin":"","cropX":0,"cropY":0,"nom":"Logo organisateur","categorie":"logo","src":"/media/organisateur/logo.png","filters":[]}""")
                        scaleY = 1.0 * dict_objet["hauteur"] / taille_logo[1]
                        top = data["fields"]["hauteur"] - dict_objet["y"] - taille_logo[1] * scaleY
                        objet.update({
                            "type": "image", "categorie": "logo", "nom": dict_objet["nom"],
                            "left": dict_objet["x"], "top": top, "width": taille_logo[0], "height": taille_logo[1],
                            "scaleX": scaleY, "scaleY": scaleY,
                            "fill": self.ConvertCouleur(dict_objet["coulRemplis"]),
                            "strokeWidth": dict_objet["epaissTrait"], "stroke": self.ConvertCouleur(dict_objet["couleurTrait"]),
                            "strokeDashArray": self.ConvertTrait(dict_objet["styleTrait"]),
                        })

                # Sp�cial
                if dict_objet["categorie"] == "special":
                    objet = {
                        "type": "rect", "categorie": "special", "nom": dict_objet["nom"],
                        "left": dict_objet["x"], "top": data["fields"]["hauteur"] - dict_objet["y"] - dict_objet["hauteur"], "width": dict_objet["largeur"], "height": dict_objet["hauteur"],
                        "fill": self.ConvertCouleur(dict_objet["coulRemplis"]),
                        "strokeWidth": dict_objet["epaissTrait"], "stroke": self.ConvertCouleur(dict_objet["couleurTrait"]),
                        "strokeDashArray": self.ConvertTrait(dict_objet["styleTrait"]),
                        "champ": dict_objet["champ"],
                    }

                # Barcode
                if dict_objet["categorie"] == "barcode":
                    objet = json.loads("""{"type":"image","version":"3.4.0","originX":"left","originY":"top","left":84.21,"top":145.03,"width":462,"height":139,"fill":"rgb(0,0,0)","stroke":"rgba(0,0,0,0)","strokeWidth":0,"strokeDashArray":null,"strokeLineCap":"butt","strokeDashOffset":0,"strokeLineJoin":"miter","strokeMiterLimit":4,"scaleX":0.09,"scaleY":0.05,"angle":0,"flipX":false,"flipY":false,"opacity":1,"shadow":null,"visible":true,"clipTo":null,"backgroundColor":"","fillRule":"nonzero","paintFirst":"fill","globalCompositeOperation":"source-over","transformMatrix":null,"skewX":0,"skewY":0,"crossOrigin":"","cropX":0,"cropY":0,"nom":"Code-barres ID de l'individu","categorie":"barcode","champ":"{CODEBARRES_ID_INDIVIDU}","cb_norme":"Extended39","cb_affiche_numero":false,"src":"/static/images/codebarres.png","filters":[]}""")
                    top = data["fields"]["hauteur"] - dict_objet["y"] - dict_objet["hauteur"]
                    objet.update({
                        "type": "image", "categorie": "barcode", "nom": dict_objet["nom"],
                        "left": dict_objet["x"], "top": top, "width": dict_objet["largeur"] / objet["scaleX"],
                        "height": dict_objet["hauteur"] / objet["scaleY"],
                        "champ": dict_objet["champ"],
                    })

                if objet:
                    liste_objets.append(objet)

        return """%s""" % json.dumps(liste_objets)

    def ConvertCouleur(self, couleur="(0, 0, 0)", transparent=False):
        try:
            couleur = couleur[1:-1].split(",")
            if transparent == True:
                alpha = 0
            else:
                alpha = 1
            return 'rgba(%d,%d,%d,%d)' % (int(couleur[0]), int(couleur[1]), int(couleur[2]), alpha)
        except:
            return couleur

    def ConvertTrait(self, style="Solid"):
        if style == "Solid": return None
        if style == "Dot": return [1,2]
        if style == "LongDash": return [6,3]
        if style == "ShortDash": return [3,6]
        if style == "DotDash": return [6,2,3]
        return None


class Table_questions(Table):
    def __init__(self, parent, **kwds):
        self.parent = parent

        # Importation de la table des choix
        req = "SELECT IDchoix, IDquestion, label FROM questionnaire_choix ORDER BY ordre;"
        self.parent.DB.ExecuterReq(req)
        self.dict_choix = {}
        for IDchoix, IDquestion, label in self.parent.DB.ResultatReq():
            if IDquestion not in self.dict_choix:
                self.dict_choix[IDquestion] = []
            self.dict_choix[IDquestion].append(label)

        # Importation de la table des cat�gories
        req = "SELECT IDcategorie, type, label FROM questionnaire_categories ORDER BY ordre;"
        self.parent.DB.ExecuterReq(req)
        self.dict_categories = {}
        for IDcategorie, type_question, label in self.parent.DB.ResultatReq():
            self.dict_categories[IDcategorie] = type_question

        Table.__init__(self, parent, **kwds)

    def IDcategorie(self, valeur=None):
        return self.dict_categories[valeur]

    def choix(self, data={}):
        if data["pk"] in self.dict_choix:
            return ";".join(self.dict_choix[data["pk"]])
        return None

    def options(self, valeur=None):
        return None

class Table_reponses(Table):
    def __init__(self, parent, **kwds):
        self.parent = parent

        # Importation de la table des choix
        req = "SELECT IDchoix, label FROM questionnaire_choix ORDER BY ordre;"
        self.parent.DB.ExecuterReq(req)
        self.dict_choix = {}
        for IDchoix, label in self.parent.DB.ResultatReq():
            self.dict_choix[IDchoix] = label

        Table.__init__(self, parent, **kwds)

    def reponse(self, valeur=None):
        liste_reponse = []
        if valeur and ";" in valeur:
            for IDchoix in valeur.split(";"):
                liste_reponse.append(self.dict_choix[int(IDchoix)])
            valeur = ";".join(liste_reponse)
        return valeur


class Table_payeurs(Table):
    def famille(self, data={}):
        return self.parent.dictComptesPayeurs[data["IDcompte_payeur"]]


class Table_reglements(Table):
    def __init__(self, parent, **kwds):
        self.parent = parent
        # Importation de la table des payeurs
        req = "SELECT IDpayeur, IDcompte_payeur FROM payeurs;"
        self.parent.DB.ExecuterReq(req)
        self.liste_payeurs = []
        for IDpayeur, IDcompte_payeur in self.parent.DB.ResultatReq():
            self.liste_payeurs.append(IDpayeur)

        Table.__init__(self, parent, **kwds)

    def famille(self, data={}):
        return self.parent.dictComptesPayeurs[data["IDcompte_payeur"]]

    def encaissement_attente(self, valeur=None):
        if valeur == None:
            return 0
        return valeur

    def IDpayeur(self, valeur=None):
        if valeur not in self.liste_payeurs:
            try:
                # Le payeur n'existe plus, on essaie de trouver un autre payeur de la m�me famille
                req = "SELECT IDreglement, IDcompte_payeur FROM reglements WHERE IDpayeur=%d;" % valeur
                self.parent.DB.ExecuterReq(req)
                IDreglement, IDcompte_payeur = self.parent.DB.ResultatReq()[0]
                req = "SELECT IDpayeur, IDcompte_payeur FROM payeurs WHERE IDcompte_payeur=%d;" % IDcompte_payeur
                self.parent.DB.ExecuterReq(req)
                IDpayeur, IDcompte_payeur = self.parent.DB.ResultatReq()[0]
                return IDpayeur
            except:
                pass
        return valeur



class Table_ventilation(Table):
    def famille(self, data={}):
        return self.parent.dictComptesPayeurs[data["IDcompte_payeur"]]


class Table_recus(Table):
    def __init__(self, parent, **kwds):
        self.parent = parent
        # Importation de la table des r�glements
        req = "SELECT IDreglement, IDcompte_payeur FROM reglements;"
        self.parent.DB.ExecuterReq(req)
        self.liste_reglements = []
        for IDreglement, IDcompte_payeur in self.parent.DB.ResultatReq():
            self.liste_reglements.append(IDreglement)

        Table.__init__(self, parent, **kwds)

    def IDreglement(self, valeur=None):
        if valeur not in self.liste_reglements:
            return None
        return valeur



class Table_textes_rappels(Table):
    def couleur(self, valeur=""):
        return Rgb2hex(valeur)

    def html(self, data={}):
        html = data["texte_pdf"]
        html = re.sub('<para.*?>', '<p>', html)
        html = html.replace("""</para>""", "</p>")
        return html


class Table_rappels(Table):
    def __init__(self, parent, **kwds):
        self.parent = parent
        # Importation de la table des lots de rappels
        req = "SELECT IDlot, nom FROM lots_rappels;"
        self.parent.DB.ExecuterReq(req)
        self.lots_rappels = []
        for IDlot, nom in self.parent.DB.ResultatReq():
            self.lots_rappels.append(IDlot)

        Table.__init__(self, parent, **kwds)

    def famille(self, data={}):
        return self.parent.dictComptesPayeurs[data["IDcompte_payeur"]]

    def IDlot(self, valeur=None):
        if valeur not in self.lots_rappels:
            return None
        return valeur


class Table_modeles_emails(Table):
    def html(self, data={}):
        texte_xml = data["texte_xml"]
        ctrl_editeur = self.parent.dlg.ctrl_editeur
        html = None
        if texte_xml:
            if six.PY3 and isinstance(texte_xml, str):
                texte_xml = texte_xml.encode("utf8")
            ctrl_editeur.SetXML(texte_xml)
            html = ctrl_editeur.GetHTML()[0]
            for balise in ("<html>", "</html>", "<head>", "</head>", "<body>", "</body>", "\r\n", "</font>"):
                html = html.replace(balise, "")
            html = re.sub('<font.*?>', '', html)
        return html

