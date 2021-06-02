#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
#-----------------------------------------------------------
# Application :    Noethys, gestion multi-activit�s
# Site internet :  www.noethys.com
# Auteur:           Ivan LUCAS
# Copyright:       (c) 2010-12 Ivan LUCAS
# Licence:         Licence GNU GPL
#-----------------------------------------------------------


DICT_FETES = {

    (1, 1) : u"Maria",
    (2, 1) : u"Basile",
    (3, 1) : u"Genevi�ve;Ginette",
    (4, 1) : u"Eddie;Eddy;Odilon",
    (5, 1) : u"Am�lien;�douard;�milienne",
    (6, 1) : u"Melaine;Tiphaine",
    (7, 1) : u"C�dric;Lucienne;Raymond;Virginie",
    (8, 1) : u"Lucien;Peggy",
    (9, 1) : u"Alexia;Alicia;Alix;Allison",
    (10, 1) : u"Guillaume;Guillemette;William",
    (11, 1) : u"Paulin",
    (12, 1) : u"Arcadie;Tania;Tatiana",
    (13, 1) : u"Hilaire;Yvette",
    (14, 1) : u"Nina",
    (15, 1) : u"Amalric;Amaury;Rachel;Rachelle;R�mi",
    (16, 1) : u"Marceau;Marcel;Marcello;Priscilla",
    (17, 1) : u"Anthony;Antonio;Roselyne",
    (18, 1) : u"Gwendal",
    (19, 1) : u"Mario;Marius",
    (20, 1) : u"Bastien;Fabien;Fabienne;S�bastien",
    (21, 1) : u"Agn�s",
    (22, 1) : u"Vincent",
    (23, 1) : u"Barnard",
    (24, 1) : u"Fr. de Sales;Paco;Soizic",
    (25, 1) : u"Apollos;Conv. St Paul",
    (26, 1) : u"Alb�ric;Paula;Pauline;Timoth�e",
    (27, 1) : u"Ang�le;Ang�lina;Ang�line;Ang�lique",
    (28, 1) : u"Th. d'Aquin",
    (29, 1) : u"Gildas",
    (30, 1) : u"Bathilde;Jacinthe;Martina;Martine",
    (31, 1) : u"Marcelle;Nikita",
    (1, 2) : u"Ella;Ellie",
    (2, 2) : u"Pr�sentation;Th�ophane",
    (3, 2) : u"Blaise;Oscar",
    (4, 2) : u"B�r�nice;Gilberto;Vanessa;V�ronica;V�ronique",
    (5, 2) : u"Agatha;Agathe",
    (6, 2) : u"Amand;Amanda;Doris;Doroth�e;Gaston",
    (7, 2) : u"Dorian;Doriane;Eug�nie",
    (8, 2) : u"Jackie;Jacky;Jacqueline",
    (9, 2) : u"Apolline",
    (10, 2) : u"Arnaud",
    (11, 2) : u"ND Lourdes",
    (12, 2) : u"Eulalie;F�licienne;F�lix",
    (13, 2) : u"B�atrice;Jordan;Lauriane",
    (14, 2) : u"Tino;Valentin",
    (15, 2) : u"Claude",
    (16, 2) : u"Julienne;Lucille;Pam�la",
    (17, 2) : u"Alexane;Alexis",
    (18, 2) : u"Bernadette;Flavien;Nadine",
    (19, 2) : u"Gabin",
    (20, 2) : u"Aim�e",
    (21, 2) : u"Dinan",
    (22, 2) : u"Isabelle",
    (23, 2) : u"Lazare",
    (24, 2) : u"Modeste",
    (25, 2) : u"Rom�o",
    (26, 2) : u"Nestor",
    (27, 2) : u"Honorine",
    (28, 2) : u"Antoinette;Romain;Romane",
    (29, 2) : u"Auguste",
    (1, 3) : u"Albin;Aubin;Dave",
    (2, 3) : u"Jaouen;Jo�vin",
    (3, 3) : u"Gu�nol�;Gw�nola",
    (4, 3) : u"Casimir;Casper;Humbert",
    (5, 3) : u"Olive;Olivia;Virgile",
    (6, 3) : u"Colette;Nicole;Nicoletta",
    (7, 3) : u"F�licit�",
    (8, 3) : u"Jean de D.",
    (9, 3) : u"Fanchon;Francesca;Fran�oise",
    (10, 3) : u"Anastasia;Vivien;Vivienne",
    (11, 3) : u"Rosine",
    (12, 3) : u"Elph�ge;Justine;Maximilien;Maximilienne;Pol",
    (13, 3) : u"Rodrigue",
    (14, 3) : u"Mathilde;Maud;Maude",
    (15, 3) : u"Louisa;Louise",
    (16, 3) : u"B�n�dicte",
    (17, 3) : u"Patrice;Patricia;Patrick",
    (18, 3) : u"Cyril;Cyrille;Salvatore",
    (19, 3) : u"Jos�;Jos�e;Joseph;Jos�phine;Josiane;Josianne",
    (20, 3) : u"Alessandra;Herbert",
    (21, 3) : u"Axel;Cl�mence",
    (22, 3) : u"L�a;Le�la;L��la;Lila",
    (23, 3) : u"R�becca;Victorien",
    (24, 3) : u"Kathy;Katia;Katie;Kristell",
    (25, 3) : u"Humbert",
    (26, 3) : u"Annonciation",
    (27, 3) : u"Habib",
    (28, 3) : u"Gontran",
    (29, 3) : u"Gladys;Gwladys",
    (30, 3) : u"Am�d�;Am�d�e",
    (31, 3) : u"Ben;Benjamin",
    (1, 4) : u"Hugues;Val�ry",
    (2, 4) : u"Sandra;Sandrine",
    (3, 4) : u"Marie-France;Ricardo;Richard",
    (4, 4) : u"Isidore;Maya",
    (5, 4) : u"Ir�ne",
    (6, 4) : u"Marcellin",
    (7, 4) : u"J.B. de la S.",
    (8, 4) : u"Constance;Julie",
    (9, 4) : u"Gauthier;Gautier",
    (10, 4) : u"Fulbert",
    (11, 4) : u"Stan;Stanislas",
    (12, 4) : u"Jules;Julio",
    (13, 4) : u"Ida",
    (14, 4) : u"Maxime",
    (15, 4) : u"Paterne",
    (16, 4) : u"Beno�t-Joseph",
    (17, 4) : u"Anicet",
    (18, 4) : u"Greta;Parfait",
    (19, 4) : u"Emma;Werner",
    (20, 4) : u"Giraud;Odette",
    (21, 4) : u"Anselme;Selma",
    (22, 4) : u"Alexandra;Alexandre",
    (23, 4) : u"Georges;Georgia;Jordi;Youri",
    (24, 4) : u"Fid�le",
    (25, 4) : u"Marc;Markus",
    (26, 4) : u"Alda;Alida",
    (27, 4) : u"Zita",
    (28, 4) : u"Louis-Marie;Val�rie",
    (29, 4) : u"Cathy;Hugo;Kate;Katherine;Kathleen",
    (30, 4) : u"Archibald;Robert;Roberte",
    (1, 5) : u"Brieuc;J�r�mie;Tamara",
    (2, 5) : u"Antonin;Boris;Zo�",
    (3, 5) : u"Alex;Filip;Philippe",
    (4, 5) : u"Florian;Sylvain;Sylvaine",
    (5, 5) : u"Ange;Judith",
    (6, 5) : u"Prudence",
    (7, 5) : u"Flavie;Gis�le",
    (8, 5) : u"D�sir�;D�sir�e;Jeannine;Jenny",
    (9, 5) : u"Isa�e;Pac�me",
    (10, 5) : u"Simone;Solange",
    (11, 5) : u"Estelle;Stella",
    (12, 5) : u"Achille",
    (13, 5) : u"Ma�l;Ma�la;Ma�lle;Rolande",
    (14, 5) : u"Mathias;Matthias",
    (15, 5) : u"Denise;Victorin",
    (16, 5) : u"Honor�",
    (17, 5) : u"Pascal;Pascale;Pascaline",
    (18, 5) : u"Cora;Coralie;Corinne;�ric;�rica",
    (19, 5) : u"C�lestin;Erwan;Yves;Yvon;Yvonne",
    (20, 5) : u"Bernardin;Roxane",
    (21, 5) : u"Constantin",
    (22, 5) : u"�mile;Julia;Rita",
    (23, 5) : u"Didier",
    (24, 5) : u"Donatien",
    (25, 5) : u"Sofia;Sophia;Sophie",
    (26, 5) : u"B�ranger;B�reng�re",
    (27, 5) : u"Hildevert",
    (28, 5) : u"Germain",
    (29, 5) : u"Aymar;Aymard;Maximin",
    (30, 5) : u"Ferdinand;Jeanine;Jeanne;Johanna;Loraine",
    (31, 5) : u"Pernelle;Perrine",
    (1, 6) : u"Justin;Ronan",
    (2, 6) : u"Blandine",
    (3, 6) : u"K�vin",
    (4, 6) : u"Clothilde;Clotilde",
    (5, 6) : u"Boniface;Igor",
    (6, 6) : u"Claudia;Claudie;Claudine;Norbert",
    (7, 6) : u"Gilbert;Ma�t�;Marie-Th�r�se",
    (8, 6) : u"Armand;Mars;M�dard;M�d�ric",
    (9, 6) : u"Diana;Diane;F�licien",
    (10, 6) : u"Gloria;Landry",
    (11, 6) : u"Barnab�;Yolande",
    (12, 6) : u"Guy",
    (13, 6) : u"Antoine de P.",
    (14, 6) : u"Candice;�lis�e",
    (15, 6) : u"Germaine",
    (16, 6) : u"Argan;Aur�lien;R�gis",
    (17, 6) : u"Herv�",
    (18, 6) : u"Cassandra;Cassandre",
    (19, 6) : u"Gervais;Micheline;Romuald",
    (20, 6) : u"Silv�re",
    (21, 6) : u"Gina;Lo�s;Rodolphe;Rudy",
    (22, 6) : u"Alban;Albane;Aubaine",
    (23, 6) : u"Audrey",
    (24, 6) : u"Baptiste;Ivan;Jean;Jean-Baptiste;Yann;Yannick;Yoann;Yvan",
    (25, 6) : u"�l�onore;Nora;Salomon",
    (26, 6) : u"Anthelme;Olympe",
    (27, 6) : u"Fernand;Fernande",
    (28, 6) : u"Ir�n�e",
    (29, 6) : u"Esm�ralda;Judy;Pablo;Paul;Peter;Pierre;Pierrick",
    (30, 6) : u"Adolphe;Martial",
    (1, 7) : u"Aaron;Esther;Goulven;Servane;Thierry",
    (2, 7) : u"Martinien",
    (3, 7) : u"Anatole;Thomas;Tom",
    (4, 7) : u"Florent;Lilian;Lillianne",
    (5, 7) : u"Antoine;Tonio;Tony",
    (6, 7) : u"Mariette;Nolwenn",
    (7, 7) : u"Raoul",
    (8, 7) : u"Edgar;Thibault",
    (9, 7) : u"Amandine;Hermine;Marianne",
    (10, 7) : u"Ulrich",
    (11, 7) : u"Beno�t;Olga",
    (12, 7) : u"Olivier",
    (13, 7) : u"Enrique;Harry;Henry;Jo�l;Jo�lle",
    (14, 7) : u"Camille",
    (15, 7) : u"Donald;Vladimir",
    (16, 7) : u"Carmen;Elvire",
    (17, 7) : u"Carole;Caroline;Charline;Charlotte;Marcelline;Victoria",
    (18, 7) : u"Freddy;Fr�d�ric;Fr�d�rique;Frida",
    (19, 7) : u"Ars�ne",
    (20, 7) : u"�liane;�lie;Marina;Marine;Marjorie",
    (21, 7) : u"Victor",
    (22, 7) : u"Madeleine;Magalie;Maggy",
    (23, 7) : u"Appolinaire;Brigitte",
    (24, 7) : u"Christelle;Christine;John;S�gol�ne",
    (25, 7) : u"Christopher;Jacques;James;Jimmy;Valentine",
    (26, 7) : u"Ana�s;Anna;Annabelle;Anna�lle;Anne;Annick;Annie;Anouk;Joachim",
    (27, 7) : u"Nathalie;Viktor",
    (28, 7) : u"Cristina",
    (29, 7) : u"B�atrix;Marthe",
    (30, 7) : u"Juliette",
    (31, 7) : u"Ignace;Ignacio",
    (1, 8) : u"Alphonse;Esp�rance",
    (2, 8) : u"Julien",
    (3, 8) : u"Lydia;Lydiane;Lydie",
    (4, 8) : u"Jean-Marie;Vianney",
    (5, 8) : u"Abel;Ab�lia",
    (6, 8) : u"Marl�ne;Octavien",
    (7, 8) : u"Ga�tan;Ga�tane",
    (8, 8) : u"Cyriaque;Dominique",
    (9, 8) : u"Amour",
    (10, 8) : u"Laura;Laure;Laurence;Laurent;Laurie",
    (11, 8) : u"Claire;Clara;Suzanne",
    (12, 8) : u"Clarisse",
    (13, 8) : u"Hippolyte;Samantha",
    (14, 8) : u"Arnold;�vrard",
    (15, 8) : u"Manon;Marie;Marielle;Marion;Maryse;Murielle;Myriam",
    (16, 8) : u"Armel;Armelle",
    (17, 8) : u"Hyacinthe",
    (18, 8) : u"H�l�na;H�l�ne;Laetitia;La�titia;L�na;Nelly",
    (19, 8) : u"Eudes;Myl�ne",
    (20, 8) : u"Bernard;Philibert;Sammy;Samuel",
    (21, 8) : u"Christophe;No�mie",
    (22, 8) : u"Fabrice",
    (23, 8) : u"�glantine;Rose;Rozenn",
    (24, 8) : u"Barth�l�my;Emily;Nathan;Nathana�lle",
    (25, 8) : u"Lo�c;Louis;Ludivine;Ludovic",
    (26, 8) : u"C�sar;Natacha",
    (27, 8) : u"Monica;Monique",
    (28, 8) : u"Augustin;Augustine;Hermance;Linda",
    (29, 8) : u"Sabine;Sabrina",
    (30, 8) : u"Fiacre;Sacha",
    (31, 8) : u"Aristide",
    (1, 9) : u"Gilles;Josu�",
    (2, 9) : u"Ingrid",
    (3, 9) : u"Greg;Gr�gory",
    (4, 9) : u"Iris;Marin;Rosalie",
    (5, 9) : u"Bertrand;Ra�ssa",
    (6, 9) : u"Donatienne;�va;�velyne",
    (7, 9) : u"R�gine;Reine",
    (8, 9) : u"Adrian;Adriane;Adrianna;Adrien",
    (9, 9) : u"Alain;Alan;Omer",
    (10, 9) : u"Aubert;In�s",
    (11, 9) : u"Daphn�e;Vinciane",
    (12, 9) : u"Apollinaire",
    (13, 9) : u"Aim�;Amy",
    (14, 9) : u"Materne;Sainte Croix",
    (15, 9) : u"Dolor�s;Lola;Lolita;Roland",
    (16, 9) : u"Abondance;Cyprien;�dith",
    (17, 9) : u"Lambert;R�nald;Renaud",
    (18, 9) : u"Marilyne;Nad�ge;Nadia;Sonia;V�ra",
    (19, 9) : u"Am�lie;�milie;Gabriel",
    (20, 9) : u"Eustache;Kim",
    (21, 9) : u"D�borah;Mathieu;Matteo",
    (22, 9) : u"Maurice",
    (23, 9) : u"Constant",
    (24, 9) : u"Andoche;Th�cle",
    (25, 9) : u"Hermann",
    (26, 9) : u"C�me;Damien",
    (27, 9) : u"Vincent de P.",
    (28, 9) : u"Venceslas",
    (29, 9) : u"Michel;Mich�le;Micka�l;Rapha�l;Rapha�lle",
    (30, 9) : u"J�r�me",
    (1, 10) : u"Ariel;Arielle;Uriel;Urielle",
    (2, 10) : u"L�ger",
    (3, 10) : u"Blanche;G�rard",
    (4, 10) : u"Auriane;France;Francine;Francis;Franck;Fran�ois;Oriane",
    (5, 10) : u"Fleur;Cerise;Hortense;Jasmine;Myrtille;Violaine",
    (6, 10) : u"Bruno",
    (7, 10) : u"Gustave;Serge",
    (8, 10) : u"P�lagie",
    (9, 10) : u"Denis;Sarah;Sibille",
    (10, 10) : u"Elric;Ghislain;Ghislaine",
    (11, 10) : u"Firmin",
    (12, 10) : u"Fred;S�raphine;Wilfried",
    (13, 10) : u"G�raud",
    (14, 10) : u"C�leste;�nora;Gwendoline",
    (15, 10) : u"Aur�lia;Aur�lie;Th�r�se",
    (16, 10) : u"Edwige;Ga�la;Ga�lla",
    (17, 10) : u"Solenne;Soline",
    (18, 10) : u"Luc;Lucas;Morgan;Morgane",
    (19, 10) : u"Ren�;Ren�e",
    (20, 10) : u"Adeline;Aline",
    (21, 10) : u"C�line;Ursula",
    (22, 10) : u"�lodie;Salom�",
    (23, 10) : u"Jean de Cap.",
    (24, 10) : u"Evrard;Florentin;Magloire",
    (25, 10) : u"Cr�pin;Daria;Doria",
    (26, 10) : u"Dimitri;�variste",
    (27, 10) : u"Emeline;�meline",
    (28, 10) : u"Jude;Mona;Simon",
    (29, 10) : u"Narcisse",
    (30, 10) : u"Heidi",
    (31, 10) : u"Quentin;Wolfgang",
    (1, 11) : u"Harold;Mathurin;Toussaint",
    (2, 11) : u"D�funts",
    (3, 11) : u"Gw�na�l;Gw�na�lle;Hubert",
    (4, 11) : u"Aymeric;Charles;Charlie;�meric;Jessica;Jessy",
    (5, 11) : u"�lisa;�lise;�lizabeth;Sylvia;Sylvianne;Sylvie",
    (6, 11) : u"Berthille;Bertille;L�o;L�onard",
    (7, 11) : u"Carine;Ernest;Ernestine;Karen;Karine",
    (8, 11) : u"Geoffrey;Geoffroy",
    (9, 11) : u"Dora;Sybil;Th�o;Th�odore",
    (10, 11) : u"L�on;Lionel;No�",
    (11, 11) : u"Martin;V�rane",
    (12, 11) : u"Christian;Cristian;Tristan",
    (13, 11) : u"Brice;Di�go;Killian",
    (14, 11) : u"Sidoine;Sidonie",
    (15, 11) : u"Albert;Arthur;L�opold;Malo",
    (16, 11) : u"Margaret;Margaux;Margot;Marguerite;Omar",
    (17, 11) : u"�lisabeth;Elsa;Leslie;Lily;Lisa;Lise",
    (18, 11) : u"Aude",
    (19, 11) : u"Tanguy",
    (20, 11) : u"Edm�e;Edmond;Octave",
    (21, 11) : u"G�lase;Pr�s. Marie",
    (22, 11) : u"C�cile;C�cilia;C�lia;Sheila",
    (23, 11) : u"Cl�ment;Cl�mentine;F�licia",
    (24, 11) : u"Augusta;Flora;Flore",
    (25, 11) : u"Cathel;Catherine;Katel",
    (26, 11) : u"Conrad;Delphine",
    (27, 11) : u"Astrid;S�verin;S�verine",
    (28, 11) : u"Jacq. de M.",
    (29, 11) : u"Saturnin",
    (30, 11) : u"Andr�;Andr�a;Andr�e",
    (1, 12) : u"�lo�se;Florence;Natalie",
    (2, 12) : u"Vivian;Viviane",
    (3, 12) : u"Fran�ois-Xavier;Xavier",
    (4, 12) : u"Ada;Barbara",
    (5, 12) : u"G�rald;G�raldine",
    (6, 12) : u"Colin;Nicolas",
    (7, 12) : u"Ambre;Ambroise",
    (8, 12) : u"Elfi;Im. Concept.",
    (9, 12) : u"P. Fourier",
    (10, 12) : u"Romaric",
    (11, 12) : u"Daniel;Daniela;Dani�le;Danny",
    (12, 12) : u"Chantal;Chantale;Corentin",
    (13, 12) : u"Aurore;Jocelyne;Josselin;Luce;Lucie",
    (14, 12) : u"Odile",
    (15, 12) : u"Christiane;Christianne;Ninon",
    (16, 12) : u"Ad�la�de;Alice;Aliz�e",
    (17, 12) : u"Ga�l;Ga�lle;Judica�l;Tessa",
    (18, 12) : u"Briac;Gatien;Robin",
    (19, 12) : u"Urbain",
    (20, 12) : u"Abraham;Isaac;Jacob;Th�ophile",
    (21, 12) : u"Pierre Can.",
    (22, 12) : u"Fra. Xavi�re;Xavi�re",
    (23, 12) : u"Armand",
    (24, 12) : u"Ad�le",
    (25, 12) : u"Emanuel;Emmanuel;Emmanuelle;Manuel;No�l;No�lle",
    (26, 12) : u"Esteban;�tienne;Fannie;Fanny;St�phane;St�phanie",
    (27, 12) : u"Jean",
    (28, 12) : u"Gaspard;Innocent",
    (29, 12) : u"David",
    (30, 12) : u"Roger",
    (31, 12) : u"M�lanie;Melina;Sylvestre",
    
}



DICT_CELEBRATIONS = {

    (21, 2) : u"la journ�e internationale de la langue maternelle",
    (8, 3) : u"la journ�e internationale de la Femme",
    (20, 3) : u"la journ�e internationale de la Francophonie",
    (21, 3) : u"la journ�e internationale pour l'�limination de la discrimination raciale",
    (22, 3) : u"la journ�e mondiale de l'eau",
    (23, 3) : u"la journ�e m�t�orologique mondiale",
    (27, 3) : u"la journ�e mondiale du th��tre",
    (7, 4) : u"la journ�e mondiale de la sant�",
    (23, 4) : u"la journ�e mondiale du livre et du droit d'auteur",
    (26, 4) : u"la journ�e mondiale de la propri�t� intellectuelle",
    (29, 4) : u"la journ�e Internationale de la Danse",
    (3, 5) : u"la journ�e mondiale de la libert� de la presse",
    (9, 5) : u"la journ�e de l'Europe",
    (15, 5) : u"la journ�e internationale des familles",
    (17, 5) : u"la journ�e mondiale des t�l�communications",
    (18, 5) : u"la journ�e internationale des mus�es",
    (21, 5) : u"la journ�e mondiale de la diversit� culturelle pour le dialogue et le developpement",
    (22, 5) : u"la journ�e internationale de la biodiversit�",
    (28, 5) : u"la journ�e internationale d'action pour la sant� des femmes",
    (31, 5) : u"la journ�e mondiale sans tabac",
    (5, 6) : u"la journ�e mondiale de l'environnement",
    (8, 6) : u"la journ�e mondiale des oc�ans",
    (17, 6) : u"la journ�e mondiale de la lutte contre la d�sertification et la s�cheresse",
    (11, 7) : u"la journ�e mondiale de la population",
    (12, 8) : u"la journ�e internationale de la jeunesse",
    (8, 9) : u"la journ�e internationale de l'alphab�tisation",
    (16, 9) : u"la journ�e internationale de la protection de la couche d'ozone",
    (21, 9) : u"la journ�e internationale de la paix",
    (22, 9) : u"la journ�e internationale sans voitures",
    (26, 9) : u"la journ�e mondiale du c�ur",
    (27, 9) : u"la journ�e Internationale de mobilisation contre la guerre et les occupations",
    (1, 10) : u"la journ�e internationale pour les personnes �g�es",
    (5, 10) : u"la journ�e internationale des enseignants du monde",
    (8, 10) : u"la journ�e internationale de la pr�vention des catastrophes naturelles",
    (9, 10) : u"la journ�e mondiale de la poste",
    (10, 10) : u"la journ�e internationale de la musique",
    (16, 10) : u"la journ�e mondiale de l'alimentation",
    (17, 10) : u"la journ�e internationale pour l'�limination de la pauvret�",
    (24, 10) : u"la journ�e mondiale d'information sur le d�veloppement",
    (16, 11) : u"la journ�e internationale pour la tol�rance",
    (20, 11) : u"la journ�e internationale des Droits de l'Enfant",
    (21, 11) : u"la journ�e internationale de la t�l�vision",
    (1, 12) : u"la journ�e mondiale contre le SIDA",
    (5, 12) : u"la journ�e internationale des volontaires pour le d�veloppement �conomique et social",
    (7, 12) : u"la journ�e de l'aviation civile internationale",
    (10, 12) : u"la journ�e internationale des droits de l'homme",
    (11, 12) : u"la journ�e internationale de la montagne",
    (29, 12 ) : u"Journ�e internationale de la diversit� biologique",
    (1, 1) : u"Le Nouvel An",
    (5, 1) : u"l'Epiphanie",
    (2, 2) : u"La chandeleur",
    (14, 2) : u"la Saint Valentin",
    (1, 5) : u"la f�te du travail",
    (31, 10) : u"la f�te d'Halloween",
    (25, 12) : u"la f�te de No�l",

}
