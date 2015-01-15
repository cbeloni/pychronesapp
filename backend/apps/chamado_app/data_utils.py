# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from gaepermission.decorator import login_not_required
from tekton import router
from gaecookie.decorator import no_csrf
from tekton.gae.middleware.redirect import RedirectResponse
from datetime import datetime,timedelta

def ObterDataPrevisao (tempo_de_desenvolvimento,data):
        #data = '28-10-2014 08:30'
        if len(data) > 16: 
            data = data[4:]
        dia_semana_extenso = {6: 'Dom ', 0: 'Seg ', 1: 'Ter ', 2:'Qua ', 3: 'Qui ', 4:'Sex ', 5: 'Sáb '}
        data_incial = datetime.strptime(data, '%d-%m-%Y %H:%M')
        data_formatada = datetime.strptime(data, '%d-%m-%Y %H:%M')

        hora_diferenca = data_formatada.hour - 8

        if hora_diferenca != 0:
            hora_diferenca *= -1
            data_formatada = data_formatada + timedelta(hours = hora_diferenca)

        tempo = int(tempo_de_desenvolvimento)

        horas = tempo % 8
        #print ("horas: " + str(horas))

        dias = tempo / 8
        #print ("dias: " + str(dias))

        data_days = data_formatada + timedelta(days = dias)
        data_final = data_days + timedelta(hours = horas)

        #adiciona novamente as horas subtraidas para o cálculo de dias e horas
        if hora_diferenca != 0:
            hora_diferenca *= -1
            data_final = data_final + timedelta(hours = hora_diferenca)

        #verifica se o horário de almoço será adicionado somente para o dia corrente
        if ((data_final.hour >= 12 and data_final.hour <= 13) or (data_incial.day != data_final.day and data_final.hour >= 12)):
            data_final = data_final + timedelta(hours = 1)

        #Caso após adicionar a diferença de horas o valor ultrapassar o horário comercial é adicionado mais um dia e inclída as horas da
        #diferença
        if  data_final.hour >= 18:
            hora_diferenca = data_final.hour - 17
            data_final = data_final + timedelta(days = 1)
            dias += 1
            data_final = data_final + timedelta(hours = - data_final.hour)
            data_final = data_final + timedelta(hours = 8 + hora_diferenca)

        # para cada dia de desenvolvimento verifica se existe sábado (dia_semana = 5)
        for i in range(0,dias):
            data_formatada = data_formatada + timedelta(days = 1)
            dia_semana = data_formatada.weekday()
            # se dia da semana for sábado adiciona dois dias a data final
            if (dia_semana == 5):
                data_final = data_final + timedelta(days = 2)
                data_formatada = data_formatada + timedelta(days = 2)

        dia_semana = data_final.weekday()        
        data_final_texto = dia_semana_extenso[dia_semana] + data_final.strftime('%d-%m-%Y %H:%M')
        #print (data_final.strftime('%d-%m-%Y %H:%M'))
        return data_final_texto