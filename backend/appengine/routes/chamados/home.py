# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse  # @UnresolvedImport
from gaepermission.decorator import login_not_required
from tekton import router
from gaecookie.decorator import no_csrf
from chamado_app import chamado_facade, data_utils,organizar_id_ordem,prepara_save  # @UnresolvedImport
from routes.chamados import new, edit  # @UnresolvedImport
from tekton.gae.middleware.redirect import RedirectResponse
from time import sleep

@login_not_required
@no_csrf
def index():    
    cmd = chamado_facade.list_chamados_cmd()
    chamados = cmd()
    
    for i in range(1,len(chamados)):
        prepara_save.refresh_por_id_ordem(i)
        
    edit_path = router.to_path(edit)
    delete_path = router.to_path(delete)
    priorizar_path = router.to_path(priorizar)
    postergar_path = router.to_path(postergar)
    chamado_form = chamado_facade.chamado_form()

    def localize_chamado(chamado):
        chamado_dct = chamado_form.fill_with_model(chamado)
        chamado_dct['edit_path'] = router.to_path(edit_path, chamado_dct['id'])
        chamado_dct['delete_path'] = router.to_path(delete_path, chamado_dct['id'], chamado_dct['id_ordem'])
        chamado_dct['priorizar_path'] = router.to_path(priorizar_path, chamado_dct['id'], len(chamados))
        chamado_dct['postergar_path'] = router.to_path(postergar_path, chamado_dct['id'], len(chamados))
        return chamado_dct

    localized_chamados = [localize_chamado(chamado) for chamado in chamados]
    context = {'chamados': localized_chamados,
               'new_path': router.to_path(new,len(localized_chamados)),
               'len_chamados': len(localized_chamados)}
    return TemplateResponse(context, 'chamados/chamado_home.html')

@login_not_required
@no_csrf
def delete(chamado_id,id_ordem_atual):
    controle_while = True
    id_ordem = int(id_ordem_atual)
    while controle_while:
        id_ordem += 1        
        if organizar_id_ordem.retorna_len_por_id_item(id_ordem) == 1:              
            #item_dicionario = organizar_id_ordem.retorna_dicionario_por_id_item(id_ordem)
            item_dicionario_menos_um = organizar_id_ordem.diminuir_um_para_id_ordem_del(id_ordem)
            organizar_id_ordem.save(item_dicionario_menos_um['id'],**item_dicionario_menos_um)
        else:
            controle_while = False  
    
            
    chamado_facade.delete_chamado_cmd(chamado_id)()    
    sleep(0.1)
    return RedirectResponse(router.to_path(index))

@login_not_required
@no_csrf
def priorizar(chamado_id,len_chamados):
    chamado = chamado_facade.get_chamado_cmd(chamado_id)()
    chamado_form = chamado_facade.chamado_form()
    item_dicionario = chamado_form.fill_with_model(chamado)
    item_dicionario_mais_um = organizar_id_ordem.acrescentar_um_para_id_ordem(int(item_dicionario['id_ordem']) - 1)
    item_dicionario_menos_um = organizar_id_ordem.diminuir_um_para_id_ordem(int(item_dicionario['id_ordem']))
    organizar_id_ordem.save(item_dicionario_mais_um['id'],**item_dicionario_mais_um)
    organizar_id_ordem.save(item_dicionario_menos_um['id'],**item_dicionario_menos_um)                          
    #prepara_save.refresh_por_id_ordem(item_dicionario['id_ordem'])
    sleep(0.1)
    prepara_save.atualiza_datas_futuras(int(item_dicionario['id_ordem'])-1,len_chamados)
    
    return RedirectResponse(router.to_path(index))

@login_not_required
@no_csrf
def postergar(chamado_id,len_chamados):
    chamado = chamado_facade.get_chamado_cmd(chamado_id)()
    chamado_form = chamado_facade.chamado_form()
    item_dicionario = chamado_form.fill_with_model(chamado)
    item_dicionario_mais_um = organizar_id_ordem.acrescentar_um_para_id_ordem(int(item_dicionario['id_ordem']))
    item_dicionario_menos_um = organizar_id_ordem.diminuir_um_para_id_ordem(int(item_dicionario['id_ordem']) + 1)
    organizar_id_ordem.save(item_dicionario_mais_um['id'],**item_dicionario_mais_um)
    organizar_id_ordem.save(item_dicionario_menos_um['id'],**item_dicionario_menos_um)                          

    sleep(0.1)
    prepara_save.atualiza_datas_futuras(int(item_dicionario['id_ordem'])-1,len_chamados)
    return RedirectResponse(router.to_path(index))