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
def index(ultimo_id_ordem):
    return TemplateResponse({'save_path': router.to_path(save, ultimo_id_ordem)}, 'chamados/chamado_form.html')

@login_not_required
@no_csrf
def save(ultimo_id_ordem,**chamado_properties):
    cmd = chamado_facade.save_chamado_id_cmd(ultimo_id_ordem,**chamado_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors,
                   'chamado': chamado_properties}

        return TemplateResponse(context, 'chamados/chamado_form.html')
    return RedirectResponse(router.to_path(chamados))

