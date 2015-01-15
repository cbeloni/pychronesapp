# -*- coding: utf-8 -*-
from chamado_app import organizar_id_ordem,data_utils

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