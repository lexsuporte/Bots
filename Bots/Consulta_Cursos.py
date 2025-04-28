from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time

driver = webdriver.Chrome()

driver.get("https://lex.education/")

perfilUsuario = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="user-portal-profile"]/lex-card/div/a[3]/div/div[2]/h3')))
perfilUsuario.click()

loginUsuario = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'/html/body/sso-root/lex-login-page/sso-login-layout/div/div[2]/form/div[1]/sso-mat-input/mat-form-field/div/div[1]/div[2]/input')))
loginUsuario.send_keys('gabriela.santos@dnx.tec.br')

senhaUsuario = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'/html/body/sso-root/lex-login-page/sso-login-layout/div/div[2]/form/div[1]/sso-mat-password-input/mat-form-field/div/div[1]/div[2]/input')))
senhaUsuario.send_keys('Dnx@2024') 

entrarUsuario = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/sso-root/lex-login-page/sso-login-layout/div/div[2]/form/lex-button/button')))   
entrarUsuario.click() 

time.sleep(1)

complementarCadastro = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div[2]/div/mat-dialog-container/sso-registration-complement-dialog/div/div[2]/lex-button[2]/button')))
complementarCadastro.click()

time.sleep(10)

#Escolas
elementos_div = driver.find_elements(By.CSS_SELECTOR,"div.cards-container__info")

# Filtrar elementos que contêm o texto "Maple Bear"
elementos_filtrados = []
elementos_filtrados_nome_escola = []

for elemento in elementos_div:
    titulo_elemento = elemento.find_element(By.CSS_SELECTOR, "h3")
    texto_titulo = titulo_elemento.text
       
    # Verificar se o texto "Maple Bear" está presente no título
    if "maple bear" in texto_titulo.lower():
        elementos_filtrados.append(elemento)
        elementos_filtrados_nome_escola.append(texto_titulo)

#inserir o indice da escola aqui
indices = [23,28,20]

print(len(elementos_div))
print(len(elementos_filtrados))

if elementos_filtrados:
    
    time.sleep(2)
    for indice in indices: #range(1,len(elementos_filtrados)):
        time.sleep(2)
        
        # titulo_elemento = elementos_filtrados[indice].find_element(By.CSS_SELECTOR, "h3")
        # nomeEscola = titulo_elemento.text
        nomeEscola = elementos_filtrados_nome_escola[indice]
       
        try:
            try:
                elementos_filtrados[indice].click()
                print()
             
            except StaleElementReferenceException:
                print("Erro")
                
            time.sleep(5) #otimizar
            cadAdministrador = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '/html/body/sso-root/lex-user-portal-page/lex-backdrop/div/div/main/section[2]/lex-card/div/a[1]/div')))
            cadAdministrador.click()
                
            aba_atual = driver.window_handles[-1]
            driver.switch_to.window(aba_atual)     
        except StaleElementReferenceException:
            print('erro')    

        time.sleep(2)

        menuCursos = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/seb-root/div[3]/nav/div/ul/li[1]/a')))
        menuCursos.click()   

        #filtro para selecionar alunos

        filtroAno= WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/div/div/div[3]/input')))
        filtroAno.click()

        selecionarAno = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/ng-dropdown-panel/div/div[2]/div[2]')))
        selecionarAno.click()

        time.sleep(2)
        
        clicarFiltrar = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[6]/button')))
        clicarFiltrar.click()

        #filtro para selecionar a pendência de cadastro
        wait = WebDriverWait(driver, 10)
        table = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-lex-table/div[1]')))

        wait = WebDriverWait(driver, 40)  # Aumentei para 30 segundos

        try:
            # Localize a tabela pelo XPath fornecido
            # xpath_tabela = '/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-lex-table/div[1]/div[2]'
            # tabela = wait.until(EC.presence_of_element_located((By.XPATH, xpath_tabela)))

            WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.lex-table-row')))
            cursos = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.lex-table-row')))

            cursos = cursos[1:]
            
            if len(cursos) != 0:

                #Inicialize uma lista para armazenar os dados de cada coluna
                dados_colunas = []
                            
                for curso in cursos:
                                
                    #Encontre todas as colunas dentro da linha atual
                    colunas = curso.find_elements(By.CSS_SELECTOR, '.table-text')
                    
                    texto_str = colunas[0].get_attribute('title')
                    texto_str = texto_str.split("\n")[0]

                    dados_colunas.append(texto_str)

                # Exibir os dados da coluna
                print(f"{nomeEscola} Dados da coluna:", dados_colunas)

                                # Switch to the first tab
                driver.close()
                first_tab = driver.window_handles[0]
                driver.switch_to.window(first_tab)       

        except Exception as e:
            print(f"Erro ao extrair dados da coluna: {e}")