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

naoCadastrados = []
errosEscolas = []

indices =   [
    44, 71, 205, 92, 121, 122, 129, 132, 133, 135, 
    141, 144, 157, 158, 166, 169, 34, 35, 179, 182, 
    185, 186, 188, 191, 193, 201, 207, 211, 212, 213, 
    214, 215, 222, 223, 239, 241, 244
]

if elementos_filtrados:
    
    for indice in indeces: #range(1,len(elementos_filtrados)):
        
   # for indice in indices:
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

            filtrarNome = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/seb-root/div[3]/div/seb-usuario/div/seb-list-table-usuario/div/seb-list-filter-user/form/div[1]/div[1]/input')))
            filtrarNome.send_keys('Jessika Queiroz')
            filtrarNome.send_keys(Keys.ENTER)
            time.sleep(0.5)
            filtrarNome.send_keys(Keys.ENTER)
            
            meu_registro = False

            try:
                # Esperar até que o elemento esteja presente na página
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.no-data")))
                WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, '/html/body/seb-root/div[3]/div/seb-edit-user/form/div[2]/section[4]/seb-form-table-component/div/div/div/div')))

                # Se a exceção não for acionada, definir a variável para True
                nenhum_registro = True

            except TimeoutException:
                nenhum_registro = False

            if meu_registro == True:
                
                entrarCadastro = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-usuario/div/seb-list-table-usuario/div/seb-lex-table/div[2]/div[2]/div")))
                entrarCadastro.click()
            
                CoordenadorAdicionado = WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, '/html/body/seb-root/div[3]/div/seb-edit-user/form/div[2]/section[2]/seb-form-table-component/div/div/table/tbody/tr[2]/td[2]/span')))
                print('Perfil Coordenador já existe', nomeEscola)
                                    
            else:
                print("Não tem perfil coordenador")
            
            turmaExiste = False
                              
            try:
                    
                WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, '/html/body/seb-root/div[3]/div/seb-edit-user/form/div[2]/section[4]/seb-form-table-component/div/div/div/div')))
                turmaExiste = True
                
            except TimeoutException:
                turmaExiste = False            
            
            if turmaExiste == True:
                print('A turma Existe!')
            else:
                print('Turma não existe')
                                               
                # Switch to the first tab
                driver.close()
                first_tab = driver.window_handles[0]
                driver.switch_to.window(first_tab)                        
          # except ValueError as err: 
    #     print(err)
        except Exception as error:
            print("Deu erro na escola: ", nomeEscola)
            print(indice)
            errosEscolas.append(indice)
            if len(driver.window_handles) > 1:
                driver.close()
            first_tab = driver.window_handles[0]
            driver.switch_to.window(first_tab)   
                
else:
    
    print("Não está cadastrado Escola: ", nomeEscola)
    print(indice)
    driver.close()
    first_tab = driver.window_handles[0]
    driver.switch_to.window(first_tab)  
    

            
print("Lista não cadastrados: ")
print(naoCadastrados)

print("Lista erros: ")
print(errosEscolas)