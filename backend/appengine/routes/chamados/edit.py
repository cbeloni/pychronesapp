# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from gaepermission.decorator import login_not_required
from tekton import router
from gaecookie.decorator import no_csrf
from chamado_app import chamado_facade,prepara_save,data_utils
from routes import chamados
from tekton.gae.middleware.redirect import RedirectResponse


@login_not_required
@no_csrf
def index(chamado_id):
    chamado = chamado_facade.get_chamado_cmd(chamado_id)()
    chamado_form = chamado_facade.chamado_form()
    chamado_properties = chamado_form.fill_with_model(chamado)
    context = {'save_path': router.to_path(save, chamado_id), 'chamado': chamado_form.fill_with_model(chamado)}
        
    if chamado_properties['id_ordem'] != '1':
        return TemplateResponse(context, 'chamados/chamado_form.html')
    else:
        return TemplateResponse(context, 'chamados/chamado_form_inicial.html')
    
@login_not_required
@no_csrf
def save(chamado_id, **chamado_properties):
    if chamado_properties['id_ordem'] != '1':
        chamado_properties = prepara_save.retorna_chamado_properties_alterado(chamado_properties['id_ordem'],chamado_properties)
    else:
        chamado_properties['end_date'] = data_utils.ObterDataPrevisao(chamado_properties['tempo_dev'],chamado_properties['start_date'])
    cmd = chamado_facade.update_chamado_cmd(chamado_id, **chamado_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors, 'chamado': chamado_properties}

        return TemplateResponse(context, 'chamados/chamado_form.html')
    return RedirectResponse(router.to_path(chamados))

