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
def index(ultimo_id_ordem):
    if ultimo_id_ordem != '1':
        return TemplateResponse({'save_path': router.to_path(save, ultimo_id_ordem)}, 'chamados/chamado_form_sem_id.html')
    else:
        return TemplateResponse({'save_path': router.to_path(save, ultimo_id_ordem)}, 'chamados/chamado_form_inicial.html')

@login_not_required
@no_csrf
def save(ultimo_id_ordem,**chamado_properties):
    if ultimo_id_ordem != '1':
        chamado_properties = prepara_save.retorna_chamado_properties_alterado(ultimo_id_ordem,chamado_properties)
    else:
        chamado_properties['end_date'] = data_utils.ObterDataPrevisao(chamado_properties['tempo_dev'],chamado_properties['start_date'])
    chamado_properties['id_ordem'] = ultimo_id_ordem
    cmd = chamado_facade.save_chamado_id_cmd(ultimo_id_ordem,**chamado_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors,
                   'chamado': chamado_properties}

        return TemplateResponse(context, 'chamados/chamado_form_inicial.html')
    return RedirectResponse(router.to_path(chamados))

