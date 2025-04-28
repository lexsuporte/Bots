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

time.sleep(1)

perfilUsuario = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/sso-root/sso-login-profile/div/sso-login-layout/div/div[2]/section/lex-card/div/a[3]/div')))
time.sleep(2)
perfilUsuario.click()

loginUsuario = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'/html/body/sso-root/lex-login-page/sso-login-layout/div/div[2]/form/div[1]/sso-mat-input/mat-form-field/div/div[1]/div[2]/input')))
loginUsuario.send_keys('fernanda.vieira@dnx.tec.br')

senhaUsuario = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'/html/body/sso-root/lex-login-page/sso-login-layout/div/div[2]/form/div[1]/sso-mat-password-input/mat-form-field/div/div[1]/div[2]/input')))
senhaUsuario.send_keys('Offinexp.4') 

entrarUsuario = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/sso-root/lex-login-page/sso-login-layout/div/div[2]/form/lex-button/button')))   
entrarUsuario.click() 

complementarCadastro = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/div[2]/div/mat-dialog-container/sso-registration-complement-dialog/div/div[2]/lex-button[2]/button')))
complementarCadastro.click()

#Escolas
# elementos_div = driver.find_elements(By.CSS_SELECTOR,"body > sso-root > lex-user-portal-page > lex-backdrop > div > div > main > section.user-portal-page__content__section.user-portal-page__content__schools > lex-card > div")
elementos_div = driver.find_elements(By.CSS_SELECTOR,"div.cards-container__info")


# Filtrar elementos que contêm o texto "Maple Bear"
elementos_filtrados = []

for elemento in elementos_div:
    titulo_elemento = elemento.find_element(By.XPATH, "/html/body/sso-root/lex-user-portal-page/lex-backdrop/div/div/main/section[1]/lex-card/div/a[1]/div")
    texto_titulo = titulo_elemento.text
       
    # Verificar se o texto "Maple Bear" está presente no título
    if "maple bear" in texto_titulo.lower():
        elementos_filtrados.append(elemento)

adicionadoCord =[]
naoCadastrados = []
errosEscolas = []

indices =  [51, 82, 84, 114, 115, 147, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237]

if elementos_filtrados:
    
    for indice in range(1,len(elementos_filtrados)):
        
    #for indice in indices:
        time.sleep(5)
        
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

            filtrarNome = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/seb-root/div[3]/div/seb-usuario/div/seb-list-table-usuario/div/seb-list-filter-user/form/div[1]/div[1]/input')))
            filtrarNome.send_keys('95417781860')
            filtrarNome.send_keys(Keys.ENTER)
            time.sleep(0.5)
            filtrarNome.send_keys(Keys.ENTER)
            
            textoNenhumRegistro = False # inicializacao (pode er qualquer coisa)

            try:
                # Esperar até que o elemento esteja presente na página
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.no-data")))
                
                textoNenhumRegistro = True # -> Significa que não existem cadastros

            except TimeoutException:
                textoNenhumRegistro = False # Significa que existe algum cadastro
            
            # textoNenhumRegistro for falso, significa que encontrou alguem, assumimos que é a pessoa
            # textoNenhumRegistro for true, significa que nao encontrou a pessoa
            
            if textoNenhumRegistro == False: # Se existe cadastro, vamos colocar o perfil
                
                entrarCadastro = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-usuario/div/seb-list-table-usuario/div/seb-lex-table/div[2]/div[2]/div/div[6]/div/span")))
                entrarCadastro.click()
                
                CoordenadorAdicionado = False
                
                try:
                
                    WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/seb-root/div[3]/div/seb-edit-user/form/div[2]/section[2]/seb-form-table-component/div/div/table/tbody/tr[2]/td[2]/span')))
                    time.sleep(1)
                    CoordenadorAdicionado = True
                                        
                except TimeoutException:
                    CoordenadorAdicionado = False
                
                if CoordenadorAdicionado == False:
                    
                    colocarPerfilCoordenador = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/seb-root/div[3]/div/seb-edit-user/form/div[2]/section[2]/div[2]/div[1]/ng-select/div/div/div[2]/input')))
                    colocarPerfilCoordenador.click()
                    
                    time.sleep(1)

                    selecionarPerfilCoordenador = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/seb-root/div[3]/div/seb-edit-user/form/div[2]/section[2]/div[2]/div[1]/ng-select/ng-dropdown-panel/div/div[2]/div[4]/span')))
                    selecionarPerfilCoordenador.click()

                    time.sleep(1)
                    
                    clicarVincularPerfil = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, '/html/body/seb-root/div[3]/div/seb-edit-user/form/div[2]/section[2]/div[2]/div[2]/button')))
                    clicarVincularPerfil.click()
                    
                    print("Adicionado Perfil Coordenador", nomeEscola)
                    adicionadoCord.append(indice)
                    print(indice)
                    
                    driver.close()
                    first_tab = driver.window_handles[0]
                    driver.switch_to.window(first_tab)
                else:
                    print(f"[{indice}] Ja cadastrado como coordenadorna Escola: {nomeEscola}")
                    driver.close()
                    first_tab = driver.window_handles[0]
                    driver.switch_to.window(first_tab)        
            else:
                
                print(f"[{indice}] Não está cadastrado Escola: {nomeEscola}")
                driver.close()
                first_tab = driver.window_handles[0]
                driver.switch_to.window(first_tab)  
            
        #print erro
        except Exception as error:
            
            print(f"[{indice}] Deu erro na escola: {nomeEscola}")
            errosEscolas.append(indice)
            
            if len(driver.window_handles) > 1:
                driver.close()
            first_tab = driver.window_handles[0]
            driver.switch_to.window(first_tab)  
            
print("Lista não cadastrados: ")
print(naoCadastrados)

print("Lista erros: ")
print(errosEscolas)