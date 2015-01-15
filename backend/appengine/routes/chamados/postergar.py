# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from gaepermission.decorator import login_not_required
from tekton import router
from gaecookie.decorator import no_csrf
from chamado_app import chamado_facade,organizar_id_ordem
from routes import chamados
from tekton.gae.middleware.redirect import RedirectResponse

@login_not_required
@no_csrf
def index(chamado_id):
    chamado = chamado_facade.get_chamado_cmd(chamado_id)()
    chamado_form = chamado_facade.chamado_form()
    item_dicionario = chamado_form.fill_with_model(chamado)
    organizar_id_ordem.acrescentar_um_para_id_ordem(int(item_dicionario['id_ordem']))
    organizar_id_ordem.diminuir_um_para_id_ordem(int(item_dicionario['id_ordem']) + 1)  
        
    return RedirectResponse(router.to_path(chamados))