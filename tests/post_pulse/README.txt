# -*- coding: utf-8 -*-
"""
PPPAT - Post Pulse test
"""
# modules python nécessaires
import pywed as pw
import numpy as np
import matplotlib.pyplot as plt
from pppat.libpulse.check_result import CheckResult as Result
from pppat.libpulse.utils import is_online, wait_cursor, post_pulse_test
import logging  # pour ajouter des informations au log de PPPPAT
logger = logging.getLogger(__name__)

"""
Un test 'post-pulse', doit être défini comme un objet Python ('class'), 
héritant de l'objet 'Result'. L'objet 'Result' possède les attributs 'code' et 
'text' qui décrivent le résultat du test. In-fine, c'est ces attributs qu'il 
faut définir dans un test post-pulse. La définition de ces attributs doit être 
faite dans la méthode test(). 
La méthode plot() sert à illustrer le test (si besoin)
IMPORTANT: 
le nom de la classe doit débuter par 'check_' pour être listé dans PPPAT
"""
class check_my_super_post_test_de_fou(Result):
    """
    Ici une description du test. C'est toujours sympa.
    """
    
    # Constructeur de la classe. A laisser.
    def __init__(self):
        Result.__init__(self)  # Result() constructor. Do not remove.
        
        # nom du test. À modifier
        self.name = 'Breve description du test'
        
        # Est-ce un test à réaliser par défaut ? True/False. À modifier.
        self.default = False

    # méthode de test. À laisser et compléter.
    @post_pulse_test  # Do not remove
    def test(self, pulse_nb):
        """
        Plasma disruption Post-test
        """
        
        # Ici réaliser le test. 
        
        
        # le plus important : définir le code et texte de l'erreur du test:
        if une_condition:
            self.code = self.ERROR
            self.text = 'message erreur'
        elif une_autre_condition:
            self.code = self.WARNING
            self.text = 'message warning'
        else:
            self.code = self.OK
            self.text = 'message OK'

    # La méthode suivante sert à tracer des choses utiles. À modifier.
    @post_pulse_test  # Do not remove
    def plot(self, pulse_nb):
        """
        Post-test display
        """
         
        fig, ax = plt.subplots()
        # ax.plot( a_completer)
        plt.show()



