# -*- coding: utf-8 -*-
from chamado_app import organizar_id_ordem,data_utils, chamado_facade  # @UnresolvedImport


def retorna_chamado_properties_alterado(ultimo_id_ordem,chamado_properties):
    """
    Command to save Chamado entity
    :param chamado_properties: a dict of properties to save on model
    :return: a Command that save Chamado, validating and localizing properties received as strings
    """
    chamado_properties['id_ordem'] = int(ultimo_id_ordem)

    if ultimo_id_ordem != '1':
        item_dicionario_anterior = organizar_id_ordem.retorna_dicionario_por_id_item(chamado_properties['id_ordem']-1)
        chamado_properties['start_date'] = item_dicionario_anterior['end_date']
    chamado_properties['end_date'] = data_utils.ObterDataPrevisao(chamado_properties['tempo_dev'],chamado_properties['start_date'])
    return chamado_properties

def refresh_por_id_ordem(id_ordem):
    """    
    """
    print (id_ordem)
    item_dicionario = organizar_id_ordem.retorna_dicionario_por_id_item(id_ordem)

    if int(item_dicionario['id_ordem']) != 1:
        item_dicionario = retorna_chamado_properties_alterado(item_dicionario['id_ordem'],item_dicionario)
    else:
        item_dicionario['end_date'] = data_utils.ObterDataPrevisao(item_dicionario['tempo_dev'],item_dicionario['start_date'])
                
    cmd = chamado_facade.update_chamado_cmd(item_dicionario['id'], **item_dicionario)
    try:
        cmd()        
    except :
        pass
    
    #return True 

def atualiza_datas_futuras(id_ordem,len_chamados):
    while id_ordem <= int(len_chamados):
        try:          
            refresh_por_id_ordem(str(id_ordem))
        except:
            pass   
        id_ordem += 1