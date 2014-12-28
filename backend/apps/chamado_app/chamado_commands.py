# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.gaeutil import SaveCommand, ModelSearchCommand,SingleModelSearchCommand
from gaeforms.ndb.form import ModelForm
from gaegraph.business_base import UpdateNode
from chamado_app.chamado_model import Chamado



class ChamadoSaveForm(ModelForm):
    """
    Form used to save and update Chamado
    """
    _model_class = Chamado
    _include = [Chamado.empresa, 
                Chamado.price, 
                Chamado.start_date, 
                Chamado.name,
                Chamado.id_ordem]

class ChamadoForm(ModelForm):
    """
    Form used to expose Chamado's properties for list or json
    """
    _model_class = Chamado

class SaveChamadoCommand(SaveCommand):
    _model_form_class = ChamadoSaveForm

class UpdateChamadoCommand(UpdateNode):
    _model_form_class = ChamadoSaveForm

class ListChamadoCommand(ModelSearchCommand):
    def __init__(self):
        super(ListChamadoCommand, self).__init__(Chamado.query_by_id_ordem())

class ObtemUltimoIdOrdem(ModelSearchCommand):
    def __init__(self):
        super(ObtemUltimoIdOrdem, self).__init__(Chamado.query_ultimo_id_ordem())        

