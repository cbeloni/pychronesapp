# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from gaegraph.business_base import NodeSearch, DeleteNode
from chamado_app.chamado_commands import ListChamadoCommand, SaveChamadoCommand, UpdateChamadoCommand, ChamadoForm, ObtemUltimoIdOrdem


def save_chamado_cmd(**chamado_properties):
    """
    Command to save Chamado entity
    :param chamado_properties: a dict of properties to save on model
    :return: a Command that save Chamado, validating and localizing properties received as strings
    """
    return SaveChamadoCommand(**chamado_properties)

def save_chamado_id_cmd(ultimo_id_ordem,**chamado_properties):
    """
    Command to save Chamado entity
    :param chamado_properties: a dict of properties to save on model
    :return: a Command that save Chamado, validating and localizing properties received as strings
    """
    chamado_properties['id_ordem'] = int(ultimo_id_ordem)
    return SaveChamadoCommand(**chamado_properties)

def update_chamado_cmd(chamado_id, **chamado_properties):
    """
    Command to update Chamado entity with id equals 'chamado_id'
    :param chamado_properties: a dict of properties to update model
    :return: a Command that update Chamado, validating and localizing properties received as strings
    """
    
    return UpdateChamadoCommand(chamado_id, **chamado_properties)


def list_chamados_cmd():
    """
    Command to list Chamado entities ordered by their creation dates
    :return: a Command proceed the db operations when executed
    """
    return ListChamadoCommand()


def chamado_form(**kwargs):
    """
    Function to get Chamado's detail form.
    :param kwargs: form properties
    :return: Form
    """
    return ChamadoForm(**kwargs)


def get_chamado_cmd(chamado_id):
    """
    Find chamado by her id
    :param chamado_id: the chamado id
    :return: Command
    """
    return NodeSearch(chamado_id)

def delete_chamado_cmd(chamado_id):
    """
    Construct a command to delete a Chamado
    :param chamado_id: chamado's id
    :return: Command
    """
    return DeleteNode(chamado_id)

def obtem_ultimo_id_ordem():
    """
    Construct a command to delete a Chamado
    :param chamado_id: chamado's id
    :return: Command
    """
    return ObtemUltimoIdOrdem()

