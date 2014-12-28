# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from gaegraph.model import Node
from gaeforms.ndb import property


class Chamado(Node):
    name = ndb.StringProperty(required=True)
    empresa = ndb.StringProperty(required=True)
    price = property.SimpleCurrency(required=True)
    start_date = ndb.DateProperty(required=True)
    id_ordem = ndb.IntegerProperty(required=True)
    
    
    @classmethod
    def query_by_id_ordem(cls):
        resultado = cls.query(cls.id_ordem > 0).order(cls.id_ordem)
        print ("resultado")
        print (resultado.fetch())
        return cls.query(cls.id_ordem > 0).order(cls.id_ordem)
    
    @classmethod
    def query_ultimo_id_ordem(cls):
        return cls.query(cls.id_ordem > 3).order(-cls.id_ordem)
        #return '4'



