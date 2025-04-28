from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time
import codecs

def login(driver):

    TIMEOUT_LOGIN = 20

    driver.get("https://lex.education/")

    perfilUsuario = WebDriverWait(driver, TIMEOUT_LOGIN).until(EC.presence_of_element_located((By.XPATH, '//*[@id="user-portal-profile"]/lex-card/div/a[3]/div/div[2]/h3')))
    perfilUsuario.click()

    loginUsuario = WebDriverWait(driver, TIMEOUT_LOGIN).until(EC.presence_of_element_located((By.XPATH,'/html/body/sso-root/lex-login-page/sso-login-layout/div/div[2]/form/div[1]/sso-mat-input/mat-form-field/div/div[1]/div[2]/input')))
    loginUsuario.send_keys('jaqueline.floriano@dnx.tec.br')

    senhaUsuario = WebDriverWait(driver,TIMEOUT_LOGIN).until(EC.presence_of_element_located((By.XPATH,'/html/body/sso-root/lex-login-page/sso-login-layout/div/div[2]/form/div[1]/sso-mat-password-input/mat-form-field/div/div[1]/div[2]/input')))
    senhaUsuario.send_keys('04031996Jf@') 

    entrarUsuario = WebDriverWait(driver, TIMEOUT_LOGIN).until(EC.presence_of_element_located((By.XPATH, '/html/body/sso-root/lex-login-page/sso-login-layout/div/div[2]/form/lex-button/button')))   
    entrarUsuario.click()

def dismissCompletarCadastr(driver):

    TIMEOUT_HOMEPAGE = 30

    complementarCadastro = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div[2]/div/mat-dialog-container/sso-registration-complement-dialog/div/div[2]/lex-button[2]/button')))
    complementarCadastro.click()

def pegarEscolas(driver):

    TIMEOUT_HOMEPAGE = 30

    # Encontrar os cards antes, para não dar erro
    WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.CSS_SELECTOR,"div.cards-container__info")))

    cardsEscolas = driver.find_elements(By.CSS_SELECTOR,"div.cards-container__info")

    cardsEscolas = cardsEscolas[91:240] # Remove a escola Mapple bear demonstração e o card "Administrador"

    return cardsEscolas

def pegarCursos2025(driver, cardsEscolas, arquivo):

    with codecs.open(arquivo, "a","utf-8") as file:
        file.write(f"\n\nNova execução\n\n")

    TIMEOUT_HOMEPAGE = 30

    cardsEscolas = cardsEscolas[1:-1] # Remove a escola Mapple bear demonstração e o card "Administrador"

    for escola in cardsEscolas:
        nomeEscola = (escola.find_element(By.CSS_SELECTOR, "h3")).text
        
        # Clica no card da escola
        escola.click()

        time.sleep(3)   # Delay necessário

        # Espera enconrar o card Administrador e clica
        cardAdministrador = WebDriverWait(driver,TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, '/html/body/sso-root/lex-user-portal-page/lex-backdrop/div/div/main/section[2]/lex-card/div/a[1]/div')))
        h3_element = cardAdministrador.find_element(By.XPATH, ".//h3")
        
        if h3_element.text != "Administrador":
            print(f"{nomeEscola}, Sem acesso ao painel Administrador")
            with codecs.open(arquivo, "a","utf-8") as file:
                file.write(f"{nomeEscola}, Sem acesso ao painel Administrador\n")
            continue    # Pular o codigo abaixo, pois a escola não possui o card administrador

        cardAdministrador.click()

        time.sleep(2)

        novaAba = driver.window_handles[-1]
        driver.switch_to.window(novaAba)

        
        time.sleep(1)   # Delay necessário
          
        menuCursos = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "//li[a[@href='/cursos']]"))) 
        menuCursos.click()

        time.sleep(1)

        # Clicar no filtro de escola
        filtroEscola= WebDriverWait(driver,TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="filterCourseId"]/div/div/div[3]/input')))
        filtroEscola.click()

        time.sleep(1)

        try:
            
            # Pega as unidades
            unidades = driver.find_elements(By.XPATH, "//span[contains(@class, 'ng-option-label')]")

            if len(unidades) > 1:

                for unidade in unidades:
                    if unidade.text == nomeEscola:  # verifica se o card bate com a unidade
                        unidade.click()
                        break
            else:
                print("Escola com apenas uma unidade: ", nomeEscola)
        except:
            print("******Exception: Escola com apenas uma unidade: ", nomeEscola)
            
        # Clicar no filtro
        filtroAno= WebDriverWait(driver,TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, '/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/div/div/div[3]/input')))
        filtroAno.click()

        # Selecionar o ano 2025
        selecionarAno = WebDriverWait(driver,TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, '/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/ng-dropdown-panel/div/div[2]/div[2]')))
        selecionarAno.click()

        # Clicar no botão Filtrar
        clicarFiltrar = WebDriverWait(driver,TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, '/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[6]/button')))
        clicarFiltrar.click()

        time.sleep(2)

        listaCursos = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.lex-table-row')))

        if len(listaCursos) == 1:
            print(f"{nomeEscola}, Nenhum")
            with codecs.open(arquivo, "a","utf-8") as file:
                file.write(f"{nomeEscola}, Nenhum\n")
            
        else:
            
            # Remover o header da tabela
            listaCursos = listaCursos[1:]
            listaCursosStr = []

            for curso in listaCursos:
                                    
                #Encontre todas as colunas dentro da linha atual
                colunas = curso.find_elements(By.CSS_SELECTOR, '.table-text')
                nomeCurso = colunas[0].get_attribute('title')
                listaCursosStr.append(nomeCurso)

            print(f"{nomeEscola}, {listaCursosStr}")
            with codecs.open(arquivo, "a","utf-8") as file:
                file.write(f"{nomeEscola}, {listaCursosStr}\n")

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)

def pegarCNPJ(driver, cardsEscolas, arquivo):

    with codecs.open(arquivo, "a","utf-8") as file:
        file.write(f"\n\nNova execução\n\n")

    TIMEOUT_HOMEPAGE = 30

    cardsEscolas = cardsEscolas[1:-1] # Remove a escola Mapple bear demonstração e o card "Administrador"

    for escola in cardsEscolas:
        nomeEscola = (escola.find_element(By.CSS_SELECTOR, "h3")).text
        
        # Clica no card da escola
        escola.click()

        time.sleep(3)   # Delay necessário

        # Espera enconrar o card Administrador e clica
        cardAdministrador = WebDriverWait(driver,TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, '/html/body/sso-root/lex-user-portal-page/lex-backdrop/div/div/main/section[2]/lex-card/div/a[1]/div')))
        h3_element = cardAdministrador.find_element(By.XPATH, ".//h3")
        
        if h3_element.text != "Administrador":
            print(f"{nomeEscola}, Sem acesso ao painel Administrador")
            with codecs.open(arquivo, "a","utf-8") as file:
                file.write(f"{nomeEscola}, Sem acesso ao painel Administrador\n")
            continue    # Pular o codigo abaixo, pois a escola não possui o card administrador

        cardAdministrador.click()

        time.sleep(2)

        novaAba = driver.window_handles[-1]
        driver.switch_to.window(novaAba)

        time.sleep(1)   # Delay necessário
        
        listaUnidades = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.lex-table-row')))
        
        while len(listaUnidades) == 1:
            time.sleep(1)
            listaUnidades = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.lex-table-row')))
        
        listaUnidades = listaUnidades[1:]
                
        for unidade in listaUnidades:
            colunas = unidade.find_elements(By.CSS_SELECTOR, '.lex-table-column')
            
            nomeFantasia = colunas[2].text
            cnpj = colunas[4].text
            
            if nomeFantasia == nomeEscola:
                print(nomeFantasia," ", cnpj)
                with codecs.open(arquivo, "a","utf-8") as file:
                    file.write(f"{nomeEscola},{cnpj}\n")
        
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)

def cadastrarCursos(driver, cardsEscolas,arquivo):
    
    
    with codecs.open(arquivo, "a","utf-8") as file:
        file.write(f"\n\nNova execução\n\n")

    TIMEOUT_HOMEPAGE = 50

    cardsEscolas = cardsEscolas[1:240] # Remove a escola Mapple bear demonstração e o card "Administrador"
    
    time.sleep(1)

    for escola in cardsEscolas:
        nomeEscola = (escola.find_element(By.CSS_SELECTOR, "h3")).text
        
        # Clica no card da escola
        escola.click()

        time.sleep(3)   # Delay necessário

        # Espera enconrar o card Administrador e clica
        cardAdministrador = WebDriverWait(driver,TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, '/html/body/sso-root/lex-user-portal-page/lex-backdrop/div/div/main/section[2]/lex-card/div/a[1]/div')))
        h3_element = cardAdministrador.find_element(By.XPATH, ".//h3")
        
        if h3_element.text != "Administrador":
            print(f"{nomeEscola}, Sem acesso ao painel Administrador")
            with codecs.open(arquivo, "a","utf-8") as file:
                file.write(f"{nomeEscola}, Sem acesso ao painel Administrador\n")
            continue    # Pular o codigo abaixo, pois a escola não possui o card administrador

        cardAdministrador.click()

        time.sleep(2)

        novaAba = driver.window_handles[-1]
        driver.switch_to.window(novaAba)

        time.sleep(1)   # Delay necessário
          
        menuCursos = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "//li[a[@href='/cursos']]"))) 
        menuCursos.click()
        
        filtrarCodigo = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[2]/input"))) 
        filtrarCodigo.send_keys("MBBC25")
        
        clicarFiltrar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[6]/button"))) 
        clicarFiltrar.click()

        time.sleep(2)
        
        listaCursos = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.lex-table-row')))

        time.sleep(2)
        
        if len(listaCursos) == 2:
            print(f"{nomeEscola}, O MBBC25 já existe")
            
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1) 
            
        else:           
             

            time.sleep(1)
            
            criarCurso = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/seb-titlebar/div/div/div[2]/div/lex-button[3]/button/span")))
            criarCurso.click()
            
            time.sleep(1)
            
            unidades_1 = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-course/form/div/seb-identification/form/div[2]/div[1]/div[1]/ng-select/div/div/div[2]/input")))
            unidades_1.click()
            
            try:
                
                # Pega as unidades
                unidades = driver.find_elements(By.XPATH, "//span[contains(@class, 'ng-option-label')]")
                            
                if len(unidades) > 1:

                    for unidade in unidades:
                        if unidade.text == nomeEscola:  # verifica se o card bate com a unidade
                            unidade.click()
                            break
                else:
                    unidades[0].click()
                    print("Escola com apenas uma unidade: ", nomeEscola)
            except:
                print("******Exception: Escola com apenas uma unidade: ", nomeEscola)
            
            #Seleciona o Segmento do Curso
            time.sleep(1)
            segmentoCurso = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-course/form/div/seb-identification/form/div[2]/div[1]/div[2]/ng-select/div/div/div[2]/input")))
            segmentoCurso.click()
            
            time.sleep(1)
            earlyCurso =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-course/form/div/seb-identification/form/div[2]/div[1]/div[2]/ng-select/ng-dropdown-panel/div/div[2]/div[1]")))
            earlyCurso.click()
            
            #Seleciona a série
            time.sleep(1)
            serieCurso =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-course/form/div/seb-identification/form/div[2]/div[1]/div[3]/ng-select/div/div/div[2]/input")))
            serieCurso.send_keys("Bear Care 3")
            serieCurso.send_keys(Keys.ENTER)
            
            #Seleciona o Ano
            time.sleep(1)
            anoLetivo = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-course/form/div/seb-identification/form/div[2]/div[1]/div[4]/ng-select/div/div")))
            anoLetivo.click()
            
            time.sleep(1)
            ano2025 = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-course/form/div/seb-identification/form/div[2]/div[1]/div[4]/ng-select/ng-dropdown-panel/div/div[2]/div[2]")))
            ano2025.click()
            
            #inserir código
            time.sleep(1)
            codigoCurso = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-course/form/div/seb-identification/form/div[2]/div[2]/div[1]/input")))
            codigoCurso.send_keys("MBBC25")
            
            #inserir nome da turma
            time.sleep(1)
            nomeCurso = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-course/form/div/seb-identification/form/div[2]/div[2]/div[2]/input")))
            nomeCurso.send_keys("BEAR CARE 2025")
            
            #salvar curso
            time.sleep(1)
            salvarCurso = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-course/form/div/seb-buttons-form-completion/div/button[2]/div")))
            salvarCurso.click()
                
            print(f"{nomeEscola}, Criado o Curso MBBC25 ")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1) 

def inativarUsuario(driver,cardsEscolas,arquivo):
    
    with codecs.open(arquivo, "a","utf-8") as file:
        file.write(f"\n\nNova execução\n\n")

    TIMEOUT_HOMEPAGE = 50

    cardsEscolas = cardsEscolas[91:240] # Remove a escola Mapple bear demonstração e o card "Administrador"
    
    time.sleep(1)

    for escola in cardsEscolas:
        nomeEscola = (escola.find_element(By.CSS_SELECTOR, "h3")).text
        
        # Clica no card da escola
        escola.click()

        time.sleep(3)   # Delay necessário

        # Espera enconrar o card Administrador e clica
        cardAdministrador = WebDriverWait(driver,TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, '/html/body/sso-root/lex-user-portal-page/lex-backdrop/div/div/main/section[2]/lex-card/div/a[1]/div')))
        h3_element = cardAdministrador.find_element(By.XPATH, ".//h3")
        
        if h3_element.text != "Administrador":
            print(f"{nomeEscola}, Sem acesso ao painel Administrador")
            with codecs.open(arquivo, "a","utf-8") as file:
                file.write(f"{nomeEscola}, Sem acesso ao painel Administrador\n")
            continue    # Pular o codigo abaixo, pois a escola não possui o card administrador

        cardAdministrador.click()

        time.sleep(2)

        novaAba = driver.window_handles[-1]
        driver.switch_to.window(novaAba)

        time.sleep(2)   # Delay necessário
          
        menuUsuario = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/nav/div/ul/li[5]/a"))) 
        menuUsuario.click()

        usuariosInativar = ( "451.662.058-80" , "397.194.908-88", "400.520.268-33") #falta o luiz "451.662.058-80" , "397.194.908-88", "400.520.268-33", "329.729.308-00"
        
        for usuarios in usuariosInativar:
                
            inputCPF = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-usuario/div/seb-list-table-usuario/div/seb-list-filter-user/form/div[1]/div[1]/input"))) 
            inputCPF.send_keys(Keys.CONTROL + "A")
            inputCPF.send_keys(Keys.DELETE)
            time.sleep(1) 
            
            inputCPF.send_keys(usuarios)
            time.sleep(2)
            inputCPF.send_keys(Keys.ENTER)
            
            time.sleep(3)

            usuario_existe = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.lex-table-row')))
            
            time.sleep(3)
        
            if len(usuario_existe) == 2:
                
                time.sleep(2)
                
                cadastroUsuario = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-usuario/div/seb-list-table-usuario/div/seb-lex-table/div[2]/div[2]/div")))         
                cadastroUsuario.click()
                
                time.sleep(5)
                
                usuarioAtivo = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-user/form/div[1]/label/span"))) 
                usuarioAtivo.click()

                notificacaoInativar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-user/seb-modal-warning/div/div/div/div[3]/button[2]"))) 
                time.sleep(1)
                notificacaoInativar.click()

                salvar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-user/form/div[2]/section[7]/div/seb-buttons-form-completion/div/button[2]/div/span"))) 
                salvar.click()
                
                time.sleep(10)
                
                print(f"{nomeEscola}, Usuário inativado ")

            
            else:  
                
                time.sleep(2)
                    
                print(f"{nomeEscola}, Usuário não existe")
                inputCPF.send_keys(Keys.CONTROL + "A")
                inputCPF.send_keys(Keys.DELETE)
                
                time.sleep(2)
                
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1) 


if __name__ == "__main__":

    driver = webdriver.Chrome()

    login(driver)
    dismissCompletarCadastr(driver)
    cardsEscolas = pegarEscolas(driver)
    #pegarCursos2025(driver,cardsEscolas,"cursos2025.txt")
    #pegarCNPJ(driver, cardsEscolas, "cnpjs2025.txt")
    #cadastrarCursos(driver, cardsEscolas, "cursosBC25.txt")
    inativarUsuario(driver, cardsEscolas, "usuariosInativo.txt")

    