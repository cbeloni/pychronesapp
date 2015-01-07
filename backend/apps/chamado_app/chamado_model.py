# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb,db
from gaegraph.model import Node
from gaeforms.ndb import property


class Chamado(Node):
    empresa = ndb.StringProperty(required=True)
    start_date = ndb.DateProperty()
    id_ordem = ndb.IntegerProperty(required=True)
    end_date = ndb.DateProperty()
    tipo = ndb.StringProperty(required=True)
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




