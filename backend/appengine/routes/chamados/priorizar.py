# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaebusiness.business import CommandExecutionException
from gaepermission.decorator import login_not_required
from tekton import router
from gaecookie.decorator import no_csrf
from chamado_app import chamado_facade
from routes import chamados
from tekton.gae.middleware.redirect import RedirectResponse
from datetime import datetime,timedelta

@login_not_required
@no_csrf
def index(chamado_id):
    chamado = chamado_facade.get_chamado_cmd(chamado_id)()
    chamado_form = chamado_facade.chamado_form()
    item_dicionario = chamado_form.fill_with_model(chamado)
    postergar_id_ordem_anterior(int(item_dicionario['id_ordem']))
    print ('Itens atuais')
    print (item_dicionario)
    item_dicionario['id_ordem'] = int(item_dicionario['id_ordem']) - 1
    item_dicionario['start_date'] = '10/01/2015 08:00'
    
    data_final = ObterDataPrevisao(item_dicionario['tempo_dev'], item_dicionario['start_date'])
    
    item_dicionario['end_date'] = data_final
    save(chamado_id, **item_dicionario)    
      
    #context = {'save_path': router.to_path(save, chamado_id), 'chamado': chamado_form.fill_with_model(chamado)}
    #return TemplateResponse(context, 'chamados/chamado_form.html')
    return RedirectResponse(router.to_path(chamados))

@login_not_required
@no_csrf
def save(chamado_id, **chamado_properties):
    cmd = chamado_facade.update_chamado_cmd(chamado_id, **chamado_properties)
    try:
        cmd()
    except CommandExecutionException:
        context = {'errors': cmd.errors, 'chamado': chamado_properties}

        return TemplateResponse(context, 'chamados/chamado_form.html')
    return RedirectResponse(router.to_path(chamados))

def postergar_id_ordem_anterior(id_ordem):
    cmd_id_ordem = chamado_facade.get_chamado_where_id_ordem(id_ordem - 1)
    chamados_where_id = cmd_id_ordem()
    print ('priorizado:')    
    for chamado in chamados_where_id:    
        print (chamado) 
        chamado_form = chamado_facade.chamado_form()
        item_dicionario = chamado_form.fill_with_model(chamado)    
        
        item_dicionario['id_ordem'] = int(item_dicionario['id_ordem']) + 1
        item_dicionario['start_date'] = '10/01/2010'
        item_dicionario['end_date'] = '10/01/2010'
        save(item_dicionario['id'], **item_dicionario)    

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