# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from gaepermission.decorator import login_not_required
from tekton import router
from gaecookie.decorator import no_csrf
from chamado_app import chamado_facade
from routes import chamados
from tekton.gae.middleware.redirect import RedirectResponse


@login_not_required
@no_csrf
def index(chamado_id):
    chamado = chamado_facade.get_chamado_cmd(chamado_id)()
    chamado_form = chamado_facade.chamado_form()
    item_dicionario = chamado_form.fill_with_model(chamado)
    postergar_id_ordem_anterior(int(item_dicionario['id_ordem']))
    print ('Itens atuais')
    print (item_dicionario)
    item_dicionario['id_ordem'] = int(item_dicionario['id_ordem']) + 1
    item_dicionario['start_date'] = '10/01/2015 08:00'
    item_dicionario['end_date'] = '10/01/2015 08:00'
    save(chamado_id, **item_dicionario)    
      
    #context = {'save_path': router.to_path(save, chamado_id), 'chamado': chamado_form.fill_with_model(chamado)}
    #return TemplateResponse(context, 'chamados/chamado_form.html')
    return RedirectResponse(router.to_path(chamados))

@login_not_required
@no_csrf
def save(chamado_id, **chamado_properties):
    cmd = chamado_facade.update_chamado_cmd(chamado_id, **chamado_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors, 'chamado': chamado_properties}

        return TemplateResponse(context, 'chamados/chamado_form.html')
    return RedirectResponse(router.to_path(chamados))

def postergar_id_ordem_anterior(id_ordem):
    cmd_id_ordem = chamado_facade.get_chamado_where_id_ordem(id_ordem + 1)
    chamados_where_id = cmd_id_ordem()
    print ('priorizado:')    
    for chamado in chamados_where_id:    
        print (chamado) 
        chamado_form = chamado_facade.chamado_form()
        item_dicionario = chamado_form.fill_with_model(chamado)    
        
        item_dicionario['id_ordem'] = int(item_dicionario['id_ordem']) - 1
        item_dicionario['start_date'] = '10/01/2010'
        item_dicionario['end_date'] = '10/01/2010'
        save(item_dicionario['id'], **item_dicionario)    

