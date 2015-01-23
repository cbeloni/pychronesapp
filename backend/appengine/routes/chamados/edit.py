# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse # @UnresolvedImport
from gaebusiness.business import CommandExecutionException
from gaepermission.decorator import login_not_required
from tekton import router
from gaecookie.decorator import no_csrf
from chamado_app import chamado_facade,prepara_save,data_utils   # @UnresolvedImport
from routes import chamados # @UnresolvedImport
from tekton.gae.middleware.redirect import RedirectResponse


@login_not_required
@no_csrf
def index(chamado_id):
    chamado = chamado_facade.get_chamado_cmd(chamado_id)()
    chamado_form = chamado_facade.chamado_form()
    item_properties = chamado_form.fill_with_model(chamado)
    
    if (item_properties['id_ordem'] == '1'):
        item_ordem = '0'
    else:
        item_ordem = item_properties['id_ordem']
    
    #verifica total de itens
    cmd = chamado_facade.list_chamados_cmd()
    chamados = cmd()
    
    context = {'save_path': router.to_path(save, chamado_id, len(chamados)), 'chamado': item_properties, 'len_chamados' : item_ordem}
    #print (type(chamado_form.fill_with_model(chamado)))
    return TemplateResponse(context, 'chamados/chamado_form.html')

@login_not_required
@no_csrf
def save(chamado_id,len_chamados, **chamado_properties):
    id_ordem_atual = str(chamado_properties['id_ordem'])
    if int(id_ordem_atual) > 1:
        chamado_properties = prepara_save.retorna_chamado_properties_alterado(id_ordem_atual,chamado_properties)
    else:
        chamado_properties['end_date'] = data_utils.ObterDataPrevisao(chamado_properties['tempo_dev'],chamado_properties['start_date'])
    chamado_properties['start_date'] = chamado_properties['start_date'].strip()
    cmd = chamado_facade.update_chamado_cmd(chamado_id, **chamado_properties)
    try:
        cmd()        
        
        if int(chamado_properties['id_ordem']) > 1:
            id_ordem_inicial = int(chamado_properties['id_ordem']) - 1
        else:
            id_ordem_inicial = int(chamado_properties['id_ordem'])
        prepara_save.atualiza_datas_futuras(id_ordem_inicial,len_chamados)
    except CommandExecutionException:
        context = {'errors': cmd.errors, 'chamado': chamado_properties}

        return TemplateResponse(context, 'chamados/chamado_form.html')
    return RedirectResponse(router.to_path(chamados))

