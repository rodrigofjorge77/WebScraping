import time
import selenium
from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
import psycopg2

def separar_string(s):
    for i, char in enumerate(s):
        if char.isdigit():
            return s[:i], s[i:]
    return s, ''  # Caso não haja números na string


# Função para inserir ou atualizar os dados na tabela
def inserir_ou_atualizar_dados(conexao, data, valor1, valor2, valor3):
    try:
        cursor = conexao.cursor()

        # Comando SQL para inserir ou atualizar os dados
        sql = f"""
        INSERT INTO dev.wheaterforecast (dateprev, perchuva, tempmin, tempmax)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (dateprev)
        DO UPDATE SET
            perchuva = EXCLUDED.perchuva,
            tempmin = EXCLUDED.tempmin,
            tempmax = EXCLUDED.tempmax;
        """

        # Executar o comando com os valores
        cursor.execute(sql, (data, valor1, valor2, valor3))
        
        # Confirmar a transação
        conexao.commit()

        print("Inserção ou atualização realizada com sucesso.")

    except Exception as e:
        print(f"Erro ao inserir ou atualizar dados: {e}")
        conexao.rollback()  # Reverter em caso de erro

    finally:
        cursor.close()


driver = webdriver.Chrome()

driver.get("https://www.cptec.inpe.br/previsao-tempo/sp/olimpia")

soup = BeautifulSoup(driver.page_source, 'html.parser')

driver.quit()

tickets = soup.find_all('div', attrs = {'class': 'col-md-2 text-center align-middle boletins'})

line = 0

ls_dataExtenso = []
ls_data        = []
ls_prevChuva   = []
ls_tempMinima  = []
ls_tempMaxima  = []

for ticket in tickets:
    dado = ticket.text.split('\n')
    #print(dado[1], dado[4], dado[10], dado[13])
    
    dataExtenso, data = separar_string(dado[1])
        
    ls_data.append(data)
    ls_prevChuva.append(dado[4].strip().replace('%',''))
    ls_tempMinima.append(dado[10].strip().replace('°',''))
    ls_tempMaxima.append(dado[13].strip().replace('°',''))
    
    line += 1

dicData = {}

i = 0

for dia in ls_data:
    #print(dia)
    
    if i == 0:
        dicData = {str(datetime.now().year) + "-" + dia[3:5] + "-" + dia[:2] : [ ls_prevChuva[i], ls_tempMinima[i], ls_tempMaxima[i]  ] }
    else:
        dicData.update( {str(datetime.now().year) + "-" + dia[3:5] + "-" + dia[:2] : [ ls_prevChuva[i], ls_tempMinima[i], ls_tempMaxima[i]  ] } )
    
    i += 1

try:
    # Conectar ao banco de dados PostgreSQL
    conexao = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="senha",
        host="172.27.213.163",
        port="5433"
    )
    
    for chave, valor in dicData.items() :
        data     = chave
        valor1   = valor[0]
        valor2   = valor[1]
        valor3   = valor[2]
        
        inserir_ou_atualizar_dados(conexao, data, valor1, valor2, valor3)
        

except Exception as e:
    print(f"Erro ao conectar ao banco de dados: {e}")

finally:
    if conexao:
        conexao.close()  # Fechar a conexão