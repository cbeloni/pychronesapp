# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from gaepermission.decorator import login_not_required
from tekton import router
from gaecookie.decorator import no_csrf
from chamado_app import chamado_facade,data_utils
from tekton.gae.middleware.redirect import RedirectResponse
from datetime import datetime,timedelta


@login_not_required
@no_csrf
def save(chamado_id, **chamado_properties):
    cmd = chamado_facade.update_chamado_cmd(chamado_id, **chamado_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors, 'chamado': chamado_properties}

        return False
    return True

def acrescentar_um_para_id_ordem(id_ordem):  
    """
        Parâmetro: id_ordem, função obtem id_ordem e salva com o valor + 1
    """ 
    item_dicionario = retorna_dicionario_por_id_item(id_ordem)  
    item_dicionario_anterior = retorna_dicionario_por_id_item(id_ordem - 1)
    item_dicionario['id_ordem'] = int(item_dicionario['id_ordem']) + 1
    item_dicionario['start_date'] = item_dicionario_anterior['end_date']
    item_dicionario['end_date'] = data_utils.ObterDataPrevisao(item_dicionario['tempo_dev'], item_dicionario['start_date'])
    save(item_dicionario['id'], **item_dicionario)    

def diminuir_um_para_id_ordem(id_ordem):  
    """
        Parâmetro: id_ordem, função obtem id_ordem e salva com o valor - 1
    """ 
    item_dicionario = retorna_dicionario_por_id_item(id_ordem)
    item_dicionario_anterior = retorna_dicionario_por_id_item(id_ordem - 1)    
    item_dicionario['id_ordem'] = int(item_dicionario['id_ordem']) - 1
    item_dicionario['start_date'] = item_dicionario_anterior['end_date']
    item_dicionario['end_date'] = data_utils.ObterDataPrevisao(item_dicionario['tempo_dev'], item_dicionario['start_date'])
    save(item_dicionario['id'], **item_dicionario)    

def retorna_dicionario_por_id_item(id_ordem):
    cmd_id_ordem = chamado_facade.get_chamado_where_id_ordem(id_ordem)
    chamados_where_id = cmd_id_ordem()
    for i in chamados_where_id:    
        chamado =  i        
    chamado_form = chamado_facade.chamado_form()
    return chamado_form.fill_with_model(chamado)  