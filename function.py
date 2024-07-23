from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import pandas as pd
import urllib
import streamlit as st
import html
import re
from datetime import date


def DataScraper(username, password):
    navegador = webdriver.Chrome()
    navegador.get("https://accounts.tiny.com.br/realms/tiny/protocol/openid-connect/auth?client_id=tiny-webapp&redirect_uri=https://erp.tiny.com.br/login&scope=openid&response_type=code")

    time.sleep(2)

    username_input = navegador.find_element(By.XPATH,
            '/html/body/div/div[2]/div/div/react-login/div/div/div[1]/div[1]/div[1]/form/div[1]/div/input')
    password_input = navegador.find_element(By.XPATH,
            '/html/body/div/div[2]/div/div/react-login/div/div/div[1]/div[1]/div[1]/form/div[2]/div/input')

    username_input.send_keys(username)
    password_input.send_keys(password)

    navegador.find_element(By.XPATH,
            '/html/body/div/div[2]/div/div/react-login/div/div/div[1]/div[1]/div[1]/form/div[3]/button').click()

    time.sleep(3)


    if (navegador.find_element(By.XPATH, '//*[@id="bs-modal-ui-popup"]/div/div')) != 0:
        navegador.find_element(By.XPATH,
                               '//*[@id="bs-modal-ui-popup"]/div/div/div/div[3]/button[1]').click()
        time.sleep(3)
    else:
        time.sleep(3)

    st.success("Login realizado com sucesso!")


    navegador.get('https://erp.tiny.com.br/vendas#list')

    st.success("Acesso aos Pedidos de Venda")

    time.sleep(3)


    # RETIRAR TODOS OS FILTROS
    try:
        navegador.find_element(By.XPATH,
                                   '/html/body/div[6]/div/div[3]/div[1]/div[3]/ul/li[4]/a').click()
    except:
        time.sleep(1)

    # FILTRAR TRANSPORTADORA

    #CLICAR NO FILTRO GEARL
    navegador.find_element(By.XPATH,
                           '//*[@id="page-wrapper"]/div[3]/div[1]/div[3]/ul/li[3]/a').click()
    # CLICAR NO FILTRO DA TRANSPORTADORA
    navegador.find_element(By.XPATH,
                           '//*[@id="idFormaEnvioPsq"]').click()
    # CLICAR NA FM TRANSPORTES
    navegador.find_element(By.XPATH,
                           '//*[@id="idFormaEnvioPsq"]/option[138]').click()
    # CLICAR EM APLICAR FILTRO
    navegador.find_element(By.XPATH,
                           '//*[@id="page-wrapper"]/div[3]/div[1]/div[3]/ul/li[3]/div/div[9]/button[1]').click()

    st.success("Filtro aplicado")
    time.sleep(1)

    # PEDIDOS EM PREPARAÇÃO
    navegador.find_element(By.XPATH,
                               '/html/body/div[6]/div/div[3]/div[1]/div[5]/div[2]/ul/li[4]/a').click()

    st.success("Acesso ao Preparando Envio")
    time.sleep(1)

    # Encontrar a tabela - ajuste o seletor conforme necessário
    table = navegador.find_element(By.XPATH,
                                   '/html/body/div[6]/div/div[3]/div[2]/div[2]/div/div[1]/form/table')
    row_ids = []
    for tr in table.find_elements(By.XPATH, './/tr'):
        row_id = tr.get_attribute('id')
        if row_id:  # Adicionar apenas se o ID não for None ou vazio
            row_ids.append(row_id)

    st.markdown(row_ids)
    data_list = []
    total_pedidos = len(row_ids)
    count = 0
    for id in row_ids:
        # Navegar para a página específica com o ID atual
        navegador.get(f'https://erp.tiny.com.br/vendas#edit/{id}')
        time.sleep(2)

        navegador.find_element(By.XPATH,
                               '//*[@id="vendaForm"]/div[1]/div[2]/div[1]/div[2]/button[1]').click()

        time.sleep(2)
        # Capturar os dados conforme necessário
        pedido = navegador.find_element(By.XPATH, '//*[@id="vendaForm"]/div[1]/div[1]/div[2]/p').text
        contato = navegador.find_element(By.XPATH, '//*[@id="vendaForm"]/div[1]/div[2]/div[1]/div[1]/p').text
        cpf = navegador.find_element(By.XPATH, '//*[@id="td_cnpj"]/div[1]/p').text

        try:
            endereco = navegador.find_element(By.XPATH, '//*[@id="novoContato"]/div[3]/p').text
        except:
            endereco = 'ERRO'

        try:
            num_casa = navegador.find_element(By.XPATH, '//*[@id="novoContato"]/div[4]/div[2]/p').text
        except:
            num_casa = 'ERRO'

        try:
            compl_casa = navegador.find_element(By.XPATH, '//*[@id="novoContato"]/div[4]/div[3]/p').text
        except:
            compl_casa = 'ERRO'

        try:
            bairro = navegador.find_element(By.XPATH, '//*[@id="novoContato"]/div[4]/div[1]/p').text
        except:
            bairro = 'ERRO'

        try:
            cep = navegador.find_element(By.XPATH, '//*[@id="td_cep"]/div/p').text
        except:
            cep = 'ERRO'

        try:
            cidade = navegador.find_element(By.XPATH, '//*[@id="td_municipio"]/p').text
        except:
            cidade = 'ERRO'

        try:
            estado = navegador.find_element(By.XPATH, '//*[@id="td_uf"]/p').text
        except:
            estado = 'ERRO'

        valor = navegador.find_element(By.XPATH, '//*[@id="vendaForm"]/div[5]/div[2]/div[4]/div/p').text
        quant = navegador.find_element(By.XPATH, '//*[@id="vendaForm"]/div[9]/div/div/div[3]/div[8]/p').text


        try:
            email = navegador.find_element(By.XPATH, '//*[@id="novoContato"]/div[5]/div[3]/p').text
        except:
            email = 'ERRO'

        try:
            celular = navegador.find_element(By.XPATH, '//*[@id="novoContato"]/div[5]/div[2]/p').text
        except:
            celular = 'ERRO'

        count = count+1

        cpf_limpo = re.sub(r'\D', '', cpf)
        cep_limpo = re.sub(r'\D', '', cep)
        celular_limpo = re.sub(r'\D', '', celular)

        valor_ = valor.replace('R$', '').strip()
        valor_limpo_ = valor_.replace(',', '.')
        valor_limpo = float(valor_limpo_)

        # Armazenar os dados capturados na lista
        data_list.append({
            'DESTINATARIO': html.unescape(contato),
            'CPF / CNPJ': str(f'*{cpf_limpo}'),
            'IE': "",
            'LOGRADOURO': html.unescape(endereco),
            'NUMERO': num_casa,
            'COMPLEMENTO': compl_casa,
            'BAIRRO': html.unescape(bairro),
            'CEP': str(f'*{cep_limpo}'),
            'CIDADE': html.unescape(cidade),
            'ESTADO': estado,
            'VALOR': int(valor_limpo),
            'DECLARADO DESCRICAO PRODUTO / NATUREZA': "",
            'QTD VOLUEMS': quant,
            'NUMERO PEDIDO': pedido,
            'E - MAIL DESTINATARIO': email,
            'NUMERO NF': pedido,
            'TELEFONE': celular_limpo,
        })
        st.success(f'{count}/{total_pedidos} - Dados Coletados')

    # Criar DataFrame a partir da lista de dados capturados
    df = pd.DataFrame(data_list)


    # Fechar o WebDriver após coletar todos os dados
    navegador.quit()
    st.success("Extração dos dados completa!")


    return df