# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaegraph.model import Node

class Chamado(Node):
    empresa = ndb.StringProperty(required=True)
    start_date = ndb.StringProperty()
    id_ordem = ndb.IntegerProperty(required=True)
    end_date = ndb.StringProperty()
    tipo = ndb.StringProperty()
    status = ndb.StringProperty()
    responsavel = ndb.StringProperty()
    chamado = ndb.StringProperty(required=True)
    tempo_dev = ndb.IntegerProperty(required=True)    
    
    @classmethod
    def query_by_id_ordem(cls):    
        return cls.query().order(cls.id_ordem)

    @classmethod
    def query_by_id_ordem_desc(cls):    
        return cls.query().order(-cls.id_ordem)
    
    @classmethod
    def query_ultimo_id_ordem(cls):
        return cls.query().order(-cls.id_ordem)

    @classmethod
    def query_by_where_id_ordem(cls,id_ordem):  
        return cls.query(ndb.GenericProperty('id_ordem') == int(id_ordem)).order(cls.id_ordem)


