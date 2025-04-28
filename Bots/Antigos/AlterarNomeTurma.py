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
senhaUsuario.send_keys('Offinexp.4') 

entrarUsuario = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/sso-root/lex-login-page/sso-login-layout/div/div[2]/form/lex-button/button')))   
entrarUsuario.click() 

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

deuErro = []
semTurma = []
nomeAtualizado = []
#indices = [5, 6, 8, 10, 11, 15, 19, 20, 23, 28, 29, 30, 31, 32, 36, 37, 40, 41, 53, 54, 63, 66, 71, 76, 79, 87, 89, 94, 96, 97, 99, 101, 107, 110, 111, 120, 125, 128, 129, 135, 137, 138, 139, 140, 141, 142, 143, 144, 150, 151, 153, 154, 156, 161, 162, 165, 166, 175, 186, 200, 202, 204, 207, 208, 213, 214, 216, 219, 220, 221, 227, 232, 233]

if elementos_filtrados:
    
    for indice in range(5,len(elementos_filtrados)):
        time.sleep(1)
        
    #for indice in range(6):
        
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
            
            menuTurmas = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/nav/div/ul/li[3]/a")))
            menuTurmas.click()

            clicarFiltroAno = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/seb-root/div[3]/div/seb-class/seb-table-class/div/div/seb-table-filtro-class/form/div/div[5]/ng-select')))
            clicarFiltroAno.click()

            clicarFiltroTodos = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-class/seb-table-class/div/div/seb-table-filtro-class/form/div/div[5]/ng-select/ng-dropdown-panel/div/div[2]/div[2]/span")))
            clicarFiltroTodos.click()

            #inserir o nome da turma academica
            inserirNomeTurma = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/seb-root/div[3]/div/seb-class/seb-table-class/div/div/seb-table-filtro-class/form/div/div[3]/input')))
            inserirNomeTurma.send_keys("Suporte LEX 2025")

            inserirNomeTurma.send_keys(Keys.ENTER)
            time.sleep(2)
            inserirNomeTurma.send_keys(Keys.ENTER)
            time.sleep(2)
        
            turma_pesquisada = WebDriverWait(driver, 5).until(EC._element_if_visible((By.XPATH, '/html/body/seb-root/div[3]/div/seb-class/seb-table-class/div/div/seb-lex-table/div[2]/div[2]/div[2]')))

            
            if turma_pesquisada:
                
                turma_pesquisada = True
                
                clicarTurma = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > seb-root > div.page-wrapper > div > seb-class > seb-table-class > div > div > seb-lex-table > div.lex-table.mt-2 > div.lex-table-content > div:nth-child(2)")))
                time.sleep(2)
                clicarTurma.click()
                
                time.sleep(2)
                
                atualizar_Turma =  WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[2]/div[2]/div[2]/input')))
                atualizar_Turma.send_keys(Keys.CONTROL + 'a')
                atualizar_Turma.send_keys(Keys.DELETE)
                atualizar_Turma.send_keys("Suporte LEX 2025")
                
                time.sleep(2)
                
                salvarTurma = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/seb-buttons-form-completion/div/button[2]')))
                salvarTurma.click()
                
                time.sleep(5)
                
                print(f"[{indice}] Nome da Turma atualizado Escola: {nomeEscola}")
                nomeAtualizado.append(indice)

                # Switch to the first tab
                driver.close()
                first_tab = driver.window_handles[0]
                driver.switch_to.window(first_tab)     
                            
                                
            else:
                
                turma_pesquisada = False
                                
                print(f"[{indice}] Não tem turma na Escola: {nomeEscola}")
                semTurma.append(indice)

                driver.close()
                first_tab = driver.window_handles[0]
                driver.switch_to.window(first_tab) 

        except Exception as error:
            print(f"[{indice}] Deu erro na Escola: {nomeEscola}")
            print(indice)
            print(error)
            deuErro.append(indice)
            
            if len(driver.window_handles) > 1:
                driver.close()
                first_tab = driver.window_handles[0]
                driver.switch_to.window(first_tab)  
        
print(deuErro)
print(semTurma)
print(nomeAtualizado)