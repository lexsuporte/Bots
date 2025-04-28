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
loginUsuario.send_keys('jaqueline.floriano@dnx.tec.br')

senhaUsuario = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'/html/body/sso-root/lex-login-page/sso-login-layout/div/div[2]/form/div[1]/sso-mat-password-input/mat-form-field/div/div[1]/div[2]/input')))
senhaUsuario.send_keys('04031996Jf@') 

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
naoEnturmados = []
enturmados = []
indices = [6, 7, 8, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24, 25, 26, 27, 29, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 44, 45, 47, 49, 50, 51, 54, 55, 59, 60, 63, 66, 67, 69, 73, 78, 79, 80, 81, 82, 83, 84, 85, 87, 88, 89, 91, 93, 94, 96, 100, 103, 105, 109, 111, 116, 117, 118, 121, 122, 123, 124, 125, 126, 130, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 148, 151, 152, 153, 154, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252]
[5, 8, 9, 10, 12, 23, 26, 28, 30, 31, 38, 43, 46, 48, 50, 52, 56, 57, 58, 61, 62, 64, 65, 68, 70, 71, 72, 74, 75, 76, 77, 83, 86, 90, 92, 95, 97, 98, 99, 101, 102, 104, 106, 107, 108, 110, 112, 113, 114, 115, 119, 120, 122, 127, 128, 129, 131, 147, 149, 150, 152, 155, 159]


if elementos_filtrados:
    
    for indice in indices: #range(5,len(elementos_filtrados)):
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
                
            time.sleep(10) #otimizar
            cadAdministrador = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, '/html/body/sso-root/lex-user-portal-page/lex-backdrop/div/div/main/section[2]/lex-card/div/a[1]/div')))
            cadAdministrador.click()

            aba_atual = driver.window_handles[-1]
            driver.switch_to.window(aba_atual)                   
            
            menuTurmas = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/nav/div/ul/li[3]/a")))
            menuTurmas.click()

            clicarFiltroAno = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/seb-root/div[3]/div/seb-class/seb-table-class/div/div/seb-table-filtro-class/form/div/div[6]/ng-select/div/div')))
            clicarFiltroAno.click()

            clicarFiltroTodos = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-class/seb-table-class/div/div/seb-table-filtro-class/form/div/div[6]/ng-select/ng-dropdown-panel/div/div[2]/div[1]")))
            clicarFiltroTodos.click()

            #inserir o nome da turma academica
            inserirNomeTurma = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/seb-root/div[3]/div/seb-class/seb-table-class/div/div/seb-table-filtro-class/form/div/div[3]/input')))
            inserirNomeTurma.send_keys("Suporte LEX 2025")

            inserirNomeTurma.send_keys(Keys.ENTER)
            time.sleep(1)
            inserirNomeTurma.send_keys(Keys.ENTER)

            turma_pesquisada = False
            time.sleep(1)

            try:
                
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > seb-root > div.page-wrapper > div > seb-class > seb-table-class > div > div > seb-lex-table > div.lex-table.mt-2 > div.lex-table-content > div > div:nth-child(5) > div > span.table-text")))
                turma_pesquisada = True
                
            except TimeoutException:
               
                turma_pesquisada = False

            if turma_pesquisada == True:
                
                turmas = driver.find_elements(By.CSS_SELECTOR,".lex-table-row")
                turmas = turmas[1:]

                for turma in turmas:
                
                    clicarTurma = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > seb-root > div.page-wrapper > div > seb-class > seb-table-class > div > div > seb-lex-table > div.lex-table.mt-2 > div.lex-table-content > div > div:nth-child(5) > div > span.table-text")))
                    clicarTurma.click()
                    
                    buscar_nome = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[7]/div[4]/div/div/input')))
                    buscar_nome.click()
                    buscar_nome.send_keys('joao.freitas@mbcentral.com.br')
                    time.sleep(1)
                    buscar_nome.send_keys(Keys.ENTER)
                    time.sleep(1)

                    nome_usuario_nenhum = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[7]/div[5]/div/seb-form-table-class/div/div[3]')))
                    time.sleep(1)
                    print(nome_usuario_nenhum)
                    nome_usuario_nenhum = True
                    
                    time.sleep(1)
                    if nome_usuario_nenhum == True:
                        
                        inserirNomeUsuario = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[7]/div[2]/div[1]/ng-select/div/div/div[2]/input')))
                        time.sleep(1)
                        
                        inserirNomeUsuario.send_keys('joao.freitas@mbcentral.com.br')
                        time.sleep(2)

                        inserirNomeUsuario.send_keys(Keys.ENTER)
                        time.sleep(0.3)
                        
                        inserirNomeUsuario.send_keys(Keys.ENTER)
                        time.sleep(0.1)
                        
                        inserirNomeUsuario.send_keys(Keys.ENTER)
                        time.sleep(0.1)
                        
                        selecionarPerfilTurma = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[7]/div[2]/div[2]/ng-select/div/div/div[2]/input")))
                        selecionarPerfilTurma.click()

                        time.sleep(1)
                        
                        selecionarPerfilCoordenador = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[7]/div[2]/div[2]/ng-select/ng-dropdown-panel/div/div[2]/div[5]")))
                        selecionarPerfilCoordenador.click()
                        
                        clicarAdicionarUsuario = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,'/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[7]/div[2]/div[3]/button/i')))
                        clicarAdicionarUsuario.click()
                        
                        time.sleep(4)
                        
                        salvarTurma = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/seb-buttons-form-completion/div/button[2]')))
                        salvarTurma.click()
                        
                        time.sleep(10)
                        
                        print("Cadastro na turma realizado ", nomeEscola)
                        time.sleep(10)
                            
                        
                        enturmados.append(indice)
                    
                    else:
                        print('Usuário já está na turma: ', nomeEscola)
                        click_cancelar = WebDriverWait(driver, 10). until(EC.element_to_be_clickable((By.XPATH, '/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/seb-buttons-form-completion/div/button[1]')))
                        click_cancelar.click()
                    

                # Switch to the first tab
                driver.close()
                first_tab = driver.window_handles[0]
                driver.switch_to.window(first_tab)                        
                
            else:
                print("Não tem está turma na: ", nomeEscola)
                naoEnturmados.append(indice)
                turma_pesquisada = False
                
                
                driver.close()
                first_tab = driver.window_handles[0]
                driver.switch_to.window(first_tab)   
                
        except Exception as error:
            
            print("Deu erro na escola: ", nomeEscola)
            print(indice)
            print(error)
            deuErro.append(indice)
            if len(driver.window_handles) > 1:
                driver.close()
            first_tab = driver.window_handles[0]
            driver.switch_to.window(first_tab)  
            
print(naoEnturmados)
print(deuErro)
print(enturmados)
