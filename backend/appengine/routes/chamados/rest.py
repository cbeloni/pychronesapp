# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaebusiness.business import CommandExecutionException
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from tekton.gae.middleware.json_middleware import JsonResponse
from chamado_app import chamado_facade # @UnresolvedImport

@login_not_required
@no_csrf
def index():
    cmd = chamado_facade.list_chamados_cmd()
    chamado_list = cmd()
    chamado_form=chamado_facade.chamado_form()
    chamado_dcts = [chamado_form.fill_with_model(m) for m in chamado_list]
    return JsonResponse(chamado_dcts)

@login_not_required
@no_csrf
def new(_resp, **chamado_properties):
    cmd = chamado_facade.save_chamado_cmd(**chamado_properties)
    return _save_or_update_json_response(cmd, _resp)

@login_not_required
@no_csrf
def edit(_resp, chamado_id, **chamado_properties):
    cmd = chamado_facade.update_chamado_cmd(chamado_id, **chamado_properties)
    return _save_or_update_json_response(cmd, _resp)

@login_not_required
@no_csrf
def delete(chamado_id):
    chamado_facade.delete_chamado_cmd(chamado_id)()

@login_not_required
@no_csrf
def _save_or_update_json_response(cmd, _resp):
    try:
        chamado = cmd()
    except CommandExecutionException:
        _resp.status_code = 400
        return JsonResponse({'errors': cmd.errors})
    chamado_form=chamado_facade.chamado_form()
    return JsonResponse(chamado_form.fill_with_model(chamado))

