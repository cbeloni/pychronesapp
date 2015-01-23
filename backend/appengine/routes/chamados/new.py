# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse # @UnresolvedImport
from gaebusiness.business import CommandExecutionException
from gaepermission.decorator import login_not_required
from tekton import router
from gaecookie.decorator import no_csrf
from chamado_app import chamado_facade,prepara_save,data_utils # @UnresolvedImport
from routes import chamados # @UnresolvedImport
from tekton.gae.middleware.redirect import RedirectResponse


@login_not_required
@no_csrf
def index(len_chamados):
    id_ordem_atual = int(len_chamados) + 1
    id_ordem = {'id_ordem' : id_ordem_atual}
    context = {'save_path': router.to_path(save,id_ordem_atual), 'len_chamados': len_chamados, 'chamado': id_ordem}
    return TemplateResponse(context, 'chamados/chamado_form.html')

@login_not_required
@no_csrf
def save(id_ordem_atual,**chamado_properties):
    if id_ordem_atual != '1':
        chamado_properties = prepara_save.retorna_chamado_properties_alterado(id_ordem_atual,chamado_properties)
    else:
        chamado_properties['end_date'] = data_utils.ObterDataPrevisao(chamado_properties['tempo_dev'],chamado_properties['start_date'])
    chamado_properties['id_ordem'] = id_ordem_atual
    chamado_properties['start_date'] = chamado_properties['start_date'].strip()
    cmd = chamado_facade.save_chamado_id_cmd(id_ordem_atual,**chamado_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors,
                   'chamado': chamado_properties}

        return TemplateResponse(context, 'chamados/chamado_form.html')
    return RedirectResponse(router.to_path(chamados))

