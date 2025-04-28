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

#login

driver.get("https://lex.education/")

perfilUsuario = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="user-portal-profile"]/lex-card/div/a[3]/div/div[2]/h3')))
perfilUsuario.click()

loginUsuario = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'/html/body/sso-root/lex-login-page/sso-login-layout/div/div[2]/form/div[1]/sso-mat-input/mat-form-field/div/div[1]/div[2]/input')))
loginUsuario.send_keys('fernanda.vieira@dnx.tec.br')

senhaUsuario = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'/html/body/sso-root/lex-login-page/sso-login-layout/div/div[2]/form/div[1]/sso-mat-password-input/mat-form-field/div/div[1]/div[2]/input')))
senhaUsuario.send_keys('Maple@2024') 

entrarUsuario = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/sso-root/lex-login-page/sso-login-layout/div/div[2]/form/lex-button/button')))   
entrarUsuario.click() 

time.sleep(5)

complementarCadastro = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div[2]/div/mat-dialog-container/sso-registration-complement-dialog/div/div[2]/lex-button[2]/button')))
complementarCadastro.click()

#Escolas
elementos_div = driver.find_elements(By.CSS_SELECTOR,"div.cards-container__info")

# Filtrar elementos que contêm o texto "Maple Bear"
elementos_filtrados = []

for elemento in elementos_div:
    titulo_elemento = elemento.find_element(By.CSS_SELECTOR, "h3")
    texto_titulo = titulo_elemento.text
       
    # Verificar se o texto "Maple Bear" está presente no título
    if "maple bear" in texto_titulo.lower():
        elementos_filtrados.append(elemento)

turmaExiste = []
turma_nao_existe = []
errosEscolas = []

#indices =  [3,10,11,12,13]

if elementos_filtrados:
    
    for indice in range(1,len(elementos_filtrados)):
        
    #for indice in indices:
        time.sleep(1)
        
        titulo_elemento = elementos_filtrados[indice].find_element(By.CSS_SELECTOR, "h3")
        nomeEscola = titulo_elemento.text
       
        try:
            try:
                elementos_filtrados[indice].click()
            except StaleElementReferenceException:
                print("Erro")
                # # Se ocorrer StaleElementReferenceException, recarregue o elemento e tente clicar novamente
                # WebDriverWait(driver, 10).until(EC.staleness_of(elementos_filtrados[indice]))
                # primeiro_elemento = driver.find_elements(By.CSS_SELECTOR, "div.cards-container__info")[indice]
                # primeiro_elemento.click()
                # time.sleep(5)
                
            time.sleep(5) #otimizar
            cadAdministrador = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '/html/body/sso-root/lex-user-portal-page/lex-backdrop/div/div/main/section[2]/lex-card/div/a[1]/div')))
            cadAdministrador.click()

            aba_atual = driver.window_handles[-1]
            driver.switch_to.window(aba_atual)                   

            time.sleep(1)

            try:
                # Wait for the element to be clickable
                menuUsuarios = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/usuarios']")))
                # Click on the element
                menuUsuarios.click()
            except StaleElementReferenceException:
                # If the element is stale, find it again and retry
                menuUsuarios = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/usuarios']")))
                menuUsuarios.click()

            filtrarNome = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '/html/body/seb-root/div[3]/div/seb-usuario/div/seb-list-table-usuario/div/seb-list-filter-user/form/div[1]/div[1]/input')))
            filtrarNome.send_keys('Jessika Queiroz')
            time.sleep(2)
            filtrarNome.send_keys(Keys.ENTER)
            time.sleep(2)
            filtrarNome.send_keys(Keys.ENTER)
            
            time.sleep(2)

            registro_existe = False

            try:
                #verifica se existe
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.no-data")))
                registro_existe = True
             
            except TimeoutException:
                
                pass
                
            if registro_existe:
                    # confere se existe perfil coordenador 
                    # coordenadorAdicionado = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, '/html/body/seb-root/div[3]/div/seb-edit-user/form/div[2]/section[2]/seb-form-table-component/div/div/table/tbody/tr[2]/td[2]/span')))
                    # print('Perfil Coordenador já existe', nomeEscola)
                entrarCadastro = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-usuario/div/seb-list-table-usuario/div/seb-lex-table/div[2]/div[2]/div")))
                entrarCadastro.click()
                    #confere se existe turma acadêmica
                existe_turma = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, '/html/body/seb-root/div[3]/div/seb-edit-user/form/div[2]/section[4]/seb-form-table-component/div/div/table/tbody/tr[2]/td[2]/span')))
                print("A turma existe no cadastro: ", nomeEscola)
                turmaExiste.append(indice)        
                print(indice)
                # Se a exceção não for acionada, definir a variável para True
                registro_existe = True

            else:

                if registro_existe == False:
                    print('Não existe registro')    
                    turma_nao_existe.append(indice)
                    print(turma_nao_existe)       
                                            
                # Switch to the first tab
                driver.close()
                first_tab = driver.window_handles[0]
                driver.switch_to.window(first_tab)                        
            
        except Exception as error:
            print("Deu erro na escola: ", nomeEscola)
            print(indice)
            errosEscolas.append(indice)
            if len(driver.window_handles) > 1:
                driver.close()
            first_tab = driver.window_handles[0]
            driver.switch_to.window(first_tab)  
            
# print("Lista não cadastrados: ")
# print(naoCadastrados)
print('Lista de Sem registro: ')
print(turma_nao_existe)

print("Lista erros: ")
print(errosEscolas)