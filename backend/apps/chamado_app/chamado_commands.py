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
                Chamado.start_date,
                Chamado.id_ordem,
                Chamado.end_date,
                Chamado.tipo,
                Chamado.status,
                Chamado.responsavel,
                Chamado.chamado,
                Chamado.tempo_dev]
                    

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

class ListChamadoWhereIdOrdem(ModelSearchCommand):
    def __init__(self,id_ordem):
#        print (id_ordem)
        super(ListChamadoWhereIdOrdem, self).__init__(Chamado.query_by_where_id_ordem(id_ordem))        

