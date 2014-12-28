# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaepermission.decorator import login_not_required
from tekton import router
from gaecookie.decorator import no_csrf
from chamado_app import chamado_facade
from routes.chamados import new, edit, rest
from tekton.gae.middleware.redirect import RedirectResponse


@login_not_required
@no_csrf
def index():
    cmd = chamado_facade.list_chamados_cmd()
    chamados = cmd()
    edit_path = router.to_path(edit)
    delete_path = router.to_path(delete)
    mensagem_path = router.to_path(mostra_mensagem)
    chamado_form = chamado_facade.chamado_form()
    
    def localize_chamado(chamado):
        chamado_dct = chamado_form.fill_with_model(chamado)    
        chamado_dct['edit_path'] = router.to_path(edit_path, chamado_dct['id'])
        chamado_dct['delete_path'] = router.to_path(delete_path, chamado_dct['id'])
        chamado_dct['mensagem_path'] = router.to_path(mensagem_path, chamado_dct['id'])
        return chamado_dct
    
    localized_chamados = [localize_chamado(chamado) for chamado in chamados]
       
    if localized_chamados:
        ultimo_id_ordem = (localized_chamados[-1])['id_ordem']
    else:
        ultimo_id_ordem = ''  
    
    context = {'chamados_localizados': localized_chamados,
               'new_path': router.to_path(new),
               'ultimo_id_ordem': str(ultimo_id_ordem)}
    return TemplateResponse(context, 'chamados/chamado_home.html')

@login_not_required
@no_csrf
def delete(chamado_id):
    chamado_facade.delete_chamado_cmd(chamado_id)()
    return RedirectResponse(router.to_path(index))

@login_not_required
@no_csrf
def mostra_mensagem(chamado_id):
    print ("Mostrei-me: %s" % chamado_id  )
    return RedirectResponse(router.to_path(index))
