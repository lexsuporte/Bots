from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
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

    TIMEOUT_HOMEPAGE = 31

    complementarCadastro = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/div[2]/div/mat-dialog-container/sso-registration-complement-dialog/div/div[2]/lex-button[2]/button')))
    complementarCadastro.click()

def pegarEscolas(driver):

    TIMEOUT_HOMEPAGE = 31

    # Encontrar os cards antes, para não dar erro
    WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.CSS_SELECTOR,"div.cards-container__info")))

    cardsEscolas = driver.find_elements(By.CSS_SELECTOR,"div.cards-container__info")

    cardsEscolas = cardsEscolas [0:-1] # Remove a escola Mapple bear demonstração e o card "Administrador"

    return cardsEscolas

def pegarCursos2025(driver, cardsEscolas, arquivo):

    with codecs.open(arquivo, "a","utf-8") as file:
        file.write(f"\n\nNova execução\n\n")

    TIMEOUT_HOMEPAGE = 30

    cardsEscolas = cardsEscolas[43:-1] # Remove a escola Mapple bear demonstração e o card "Administrador"

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

    cardsEscolas = cardsEscolas[26:-1] # Remove a escola Mapple bear demonstração e o card "Administrador"

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
        
        listaUnidades = listaUnidades[1:10]
                
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

def cadastrarTurmas(driver, cardsEscolas, arquivo):
    
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

        time.sleep(5)

        novaAba = driver.window_handles[-1]
        driver.switch_to.window(novaAba)

        if driver.current_url == "about:blank":
            print("Página inválida detectada ('about:blank'). Fechando a aba.")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])    
            time.sleep(1)   # Delay necessário
          
        menuTurmas = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/nav/div/ul/li[3]/a"))) 
        menuTurmas.click()

        time.sleep(1)
        
        UnidadesEscolher = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until( EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-class/seb-table-class/div/div/seb-table-filtro-class/form/div/div[1]/ng-select/div/div/div[2]/input")))
        UnidadesEscolher.click()
        
        unidades = driver.find_elements(By.XPATH, "//div[@class='ng-dropdown-panel-items scroll-host']//div[@class='ng-option']")

        if unidades:
            for unidade in unidades:
                if unidade.text == nomeEscola:
                    unidade.click()
                    break
                else:
                    print(f"Escola {nomeEscola} com apenas uma unidade ou sem unidades disponíveis.")
                    
        codigoTurma = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-class/seb-table-class/div/div/seb-table-filtro-class/form/div/div[2]/input")))
        codigoTurma.send_keys("SUPORTE2025")
        
        filtrarCodigo = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-class/seb-table-class/div/div/seb-table-filtro-class/form/div/div[7]/button")))
        filtrarCodigo.click()
        
        time.sleep(3)
        
        turmaExiste = driver.find_elements(By.XPATH, "//span[@class='table-text' and text()='SUPORTE LEX 2025']")
                
        if turmaExiste:
            print("Turma já existe na Escola:", nomeEscola)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)
        
        else:
            criarTurma = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-class/seb-titlebar/div/div/div[2]/div/lex-button/button")))
            criarTurma.click()
            
            time.sleep(1)
            
            UnidadesTeste = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until( EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[1]/ng-select/div")))
            UnidadesTeste.click()
            
            unidades = driver.find_elements(By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[1]/ng-select/ng-dropdown-panel/div/div[2]/div")

            if unidades:
                for unidade in unidades:
                    if unidade.text == nomeEscola:
                        unidade.click()
                        break
                    else:
                        print(f"Escola {nomeEscola} com apenas uma unidade ou sem unidades disponíveis.")
            
            #Ano curso
            ano2025 = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[2]/ng-select/div/div/div[3]/input")))
            ano2025.click()
            
            clicarAno2025 = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "//html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[2]/ng-select/ng-dropdown-panel/div/div[2]/div[2]")))
            clicarAno2025.click()

            #Seleciona a séria
            serieCurso =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[3]/ng-select/div/div/div[2]/input")))
            serieCurso.send_keys("Year 1 2025")
            
            try:
    
                #serieElementary = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[3]/ng-select/ng-dropdown-panel/div/div[2]/div[8]")))
                #serieElementary.click
                time.sleep(1)
                year1 = driver.find_elements(By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[3]/ng-select/ng-dropdown-panel/div/div[2]/div/span")
                
                if year1:
                
                    #serieElementary = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[3]/ng-select/ng-dropdown-panel/div/div[2]/div[8]")))
                    #serieCurso.send_keys("YEAR 1")
                    serieCurso.send_keys(Keys.ENTER)
                    print("adicionado Y1", nomeEscola)
                
                else:
                    time.sleep(1)
                    serieSK = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[3]/ng-select/div/div/div[2]/input")))
                    serieSK.click()
                    serieSK.send_keys(Keys.CONTROL, "A")
                    serieSK.send_keys(Keys.DELETE)
                    serieSK.click()
                    serieSK.send_keys("SENIOR KINDERGARTEN 2025")
                    serieSK.send_keys(Keys.ENTER)
                    print("Adicionado SK", nomeEscola)
            except:
                print("A unidade não possui SK ou Year 1:", nomeEscola) 
                serieCurso.click()
                clicar1Item =   WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[3]/ng-select")))      
                clicar1Item.click()
                
                
                
            #Inserir código
            inserirCodigo = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[2]/div[1]/input")))
            inserirCodigo.send_keys("SUPORTE2025")
            
            #inserir nome da turma
            inserirNomeTurma = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[2]/div[2]/input")))
            inserirNomeTurma.send_keys("SUPORTE LEX 2025")
            '''
            timeLexToddle = ["jaqueline.floriano@dnx.tec.br", "jessika.queiroz@dnx.tec.br", "fernanda.vieira@dnx.tec.br", "fernanda.inacio@dnx.tec.br", "julioc.santos@maplebear.com.br", "toddle@maplebear.com.br"] 
            
            for pessoa in timeLexToddle:
                
                time.sleep(1)
                
                try:
                    
                    if pessoa:
                        time.sleep(1)
                        inserirUsuariosTurma = 3(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[7]/div[2]/div[1]/ng-select/div/div/div[2]/input")))
                        inserirUsuariosTurma.click()
                        inserirUsuariosTurma.send_keys(pessoa)
                        inserirUsuariosTurma.send_keys(Keys.ENTER)
                        inserirUsuariosTurma.send_keys(Keys.ENTER)
                        
                        print("Usuário:", pessoa, "adicionado a turma!")
                        
                        selecionarPerfil = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, '/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[7]/div[2]/div[2]/ng-select')))
                        selecionarPerfil.click()

                        selecionarPerfilCoordenador = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[7]/div[2]/div[2]/ng-select/ng-dropdown-panel/div/div[2]/div[5]/span")))
                        selecionarPerfilCoordenador.click()
                        
                        time.sleep(1)
                        
                        adicionarUsuarios = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[7]/div[2]/div[3]/button")))
                        adicionarUsuarios.click()
                        
                        WebDriverWait(driver, 5).until(EC.staleness_of(inserirUsuariosTurma))
                        continue
                    
                    else:
                        print(f"Erro ao adicionar o usuário {pessoa}")
                    
                        
                except:
                    continue
                
            time.sleep(5)
            '''
            
            clicarSalvar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/seb-buttons-form-completion/div/button[2]/div")))
            clicarSalvar.click()
            
            time.sleep(5)
            print(nomeEscola, ": Criado Turma Suporte LEX 2025")
            
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)
                                
def verificarTurmas(driver, cardsEscolas, arquivo):
    
    with codecs.open(arquivo, "a","utf-8") as file:
        file.write(f"\n\nNova execução\n\n")
    
    TIMEOUT_HOMEPAGE = 30

    cardsEscolas = cardsEscolas[69:-1] # Remove a escola Mapple bear demonstração e o card "Administrador"


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

        time.sleep(5)

        novaAba = driver.window_handles[-1]
        driver.switch_to.window(novaAba)

        if driver.current_url == "about:blank":
            print("Página inválida detectada ('about:blank'). Fechando a aba.")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])    
            time.sleep(1)   # Delay necessário
        
        time.sleep(2)
          
        menuTurmas = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/nav/div/ul/li[3]/a"))) 
        menuTurmas.click()

        time.sleep(1)
        
        UnidadesEscolher = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until( EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-class/seb-table-class/div/div/seb-table-filtro-class/form/div/div[1]/ng-select/div/div/div[2]/input")))
        UnidadesEscolher.click()
        
        unidades = driver.find_elements(By.XPATH, "//div[@class='ng-dropdown-panel-items scroll-host']//div[@class='ng-option']")

        if unidades:
            for unidade in unidades:
                if unidade.text == nomeEscola:
                    unidade.click()
                    break
                else:
                    print(f"Escola {nomeEscola} com apenas uma unidade ou sem unidades disponíveis.")
                    
        codigoTurma = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-class/seb-table-class/div/div/seb-table-filtro-class/form/div/div[2]/input")))
        codigoTurma.send_keys("SUPORTE2025")
        
        filtrarCodigo = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-class/seb-table-class/div/div/seb-table-filtro-class/form/div/div[7]/button")))
        filtrarCodigo.click()
        
        turmaExiste = driver.find_elements(By.XPATH, "//span[@class='table-text' and text()='SUPORTE LEX 2025']")
                
        if turmaExiste:
            print("Turma já existe na Escola:", nomeEscola)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)
        
        else:
            print("Turma não cadastrada:", nomeEscola)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)
            
def posicoesEscolas(driver):
    
    
    

    TIMEOUT_HOMEPAGE = 30

    # Espera até que os elementos estejam presentes
    WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.cards-container__info"))
    )

    # Localiza os cards
    cardsEscolas = driver.find_elements(By.CSS_SELECTOR, "div.cards-container__info")

    # Remove itens indesejados
    cardsEscolas = cardsEscolas[1:-1]  
   
    # Itera e captura os nomes
    for index, escola in enumerate(cardsEscolas, start=1):  
        nomeEscola = escola.find_element(By.CSS_SELECTOR, "h3").text  
        print(f"{index} - {nomeEscola}")  
def adicionarUsuariosTurmas(driver, cardsEscolas,arquivo):
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

        time.sleep(5)

        novaAba = driver.window_handles[-1]
        driver.switch_to.window(novaAba)

        if driver.current_url == "about:blank":
            print("Página inválida detectada ('about:blank'). Fechando a aba.")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])    
            time.sleep(1)   # Delay necessário
          
        menuTurmas = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/nav/div/ul/li[3]/a"))) 
        menuTurmas.click()

        time.sleep(1)
        
        UnidadesEscolher = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until( EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-class/seb-table-class/div/div/seb-table-filtro-class/form/div/div[1]/ng-select/div/div/div[2]/input")))
        UnidadesEscolher.click()
        
        unidades = driver.find_elements(By.XPATH, "//div[@class='ng-dropdown-panel-items scroll-host']//div[@class='ng-option']")

        if unidades:
            for unidade in unidades:
                if unidade.text == nomeEscola:
                    unidade.click()
                    break
                else:
                    print(f"Escola {nomeEscola} com apenas uma unidade ou sem unidades disponíveis.")
                    
        codigoTurma = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-class/seb-table-class/div/div/seb-table-filtro-class/form/div/div[2]/input")))
        codigoTurma.send_keys("SUPORTE2025")
        
        filtrarCodigo = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-class/seb-table-class/div/div/seb-table-filtro-class/form/div/div[7]/button")))
        filtrarCodigo.click()
        
        time.sleep(3)
        
        turmaExiste = driver.find_elements(By.XPATH, "//span[@class='table-text' and text()='SUPORTE LEX 2025']")
        time.sleep(3)
        
        if turmaExiste:
            print("Turma já existe na Escola:", nomeEscola)
            time.sleep(2)
            clicarTurma = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > seb-root > div.page-wrapper > div > seb-class > seb-table-class > div > div > seb-lex-table > div.lex-table.mt-2 > div.lex-table-content > div")))
            clicarTurma.click()
            
            time.sleep(1)
            
            
            timeLexToddle = ["jaqueline.floriano@dnx.tec.br", "jessika.queiroz@dnx.tec.br", "fernanda.vieira@dnx.tec.br", "fernanda.inacio@dnx.tec.br", "julioc.santos@maplebear.com.br", "toddle@maplebear.com.br"] 
                       # timeLexToddle = ["jaqueline.floriano@dnx.tec.br", "fernanda.vieira@dnx.tec.br"] 
            
            for pessoa in timeLexToddle:
                
                try:
                    
                    if pessoa:
                        time.sleep(2)
                        inserirUsuariosTurma = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, '/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[7]/div[2]/div[1]/ng-select/div/div/div[2]/input')))
                        inserirUsuariosTurma.click()
                        inserirUsuariosTurma.send_keys(pessoa)
                        inserirUsuariosTurma.send_keys(Keys.ENTER)
                        inserirUsuariosTurma.send_keys(Keys.ENTER)
                        
                        time.sleep(1)
                        
                        selecionarPerfil = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, '/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[7]/div[2]/div[2]/ng-select/div/div/div[2]/input')))
                        selecionarPerfil.click()
                        #selecionarPerfil.send_keys("Coordenador")

                        selecionarPerfilCoordenador = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[7]/div[2]/div[2]/ng-select/ng-dropdown-panel/div/div[2]/div[5]")))
                        selecionarPerfilCoordenador.click()
                        
                        time.sleep(1)
                        
                        adicionarUsuarios = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[7]/div[2]/div[3]/button")))
                        adicionarUsuarios.click()
                        
                        print("Usuário:", pessoa, "adicionado a turma!")
                        
                        WebDriverWait(driver, 5).until(EC.staleness_of(inserirUsuariosTurma))
                        continue
                    
                    else:
                        print(f"Erro ao adicionar o usuário {pessoa}")
                    
                        
                except:
                    continue
                
            
            clicarSalvar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/seb-buttons-form-completion/div/button[2]")))
            clicarSalvar.click()
            
            time.sleep(5)
            print(nomeEscola, ": Criado Turma Suporte LEX 2025")
            
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)

        
        else:
            print("Turma não existe na Escola:", nomeEscola)  
            
            criarTurma = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-class/seb-titlebar/div/div/div[2]/div/lex-button/button")))
            criarTurma.click()
            
            time.sleep(1)
            
            UnidadesTeste = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until( EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[1]/ng-select/div")))
            UnidadesTeste.click()
            
            unidades = driver.find_elements(By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[1]/ng-select/ng-dropdown-panel/div/div[2]/div")

            if unidades:
                for unidade in unidades:
                    if unidade.text == nomeEscola:
                        unidade.click()
                        break
                    else:
                        print(f"Escola {nomeEscola} com apenas uma unidade ou sem unidades disponíveis.")
            
            #Ano curso
            ano2025 = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[2]/ng-select/div/div/div[3]/input")))
            ano2025.click()
            
            clicarAno2025 = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "//html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[2]/ng-select/ng-dropdown-panel/div/div[2]/div[2]")))
            clicarAno2025.click()

            #Seleciona a séria
            serieCurso =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[3]/ng-select/div/div/div[2]/input")))
            serieCurso.send_keys("Year 1 2025")
            
            try:
    
                #serieElementary = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[3]/ng-select/ng-dropdown-panel/div/div[2]/div[8]")))
                #serieElementary.click
                time.sleep(1)
                year1 = driver.find_elements(By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[3]/ng-select/ng-dropdown-panel/div/div[2]/div/span")
                
                if year1:
                
                    #serieElementary = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[3]/ng-select/ng-dropdown-panel/div/div[2]/div[8]")))
                    #serieCurso.send_keys("YEAR 1")
                    serieCurso.send_keys(Keys.ENTER)
                    print("adicionado Y1", nomeEscola)
                
                else:
                    time.sleep(1)
                    serieSK = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[3]/ng-select/div/div/div[2]/input")))
                    serieSK.click()
                    serieSK.send_keys(Keys.CONTROL, "A")
                    serieSK.send_keys(Keys.DELETE)
                    serieSK.click()
                    serieSK.send_keys("SENIOR KINDERGARTEN 2025")
                    serieSK.send_keys(Keys.ENTER)
                    print("Adicionado SK", nomeEscola)
            except:
                print("A unidade não possui SK ou Year 1:", nomeEscola) 
                serieCurso.click()
                clicar1Item =   WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[3]/ng-select")))      
                clicar1Item.click()
                
                
                
            #Inserir código
            inserirCodigo = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[2]/div[1]/input")))
            inserirCodigo.send_keys("SUPORTE2025")
            
            #inserir nome da turma
            inserirNomeTurma = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[2]/div[2]/input")))
            inserirNomeTurma.send_keys("SUPORTE LEX 2025")
            
            clicarSalvar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/seb-buttons-form-completion/div/button[2]/div")))
            clicarSalvar.click()
            
            time.sleep(5)
            print(nomeEscola, ": Criado Turma Suporte LEX 2025")
            
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)
                                          
def cadastrarProdutos(driver, cardsEscolas, arquivo):
    
        with codecs.open(arquivo, "a","utf-8") as file:
            file.write(f"\n\nNova execução\n\n")
    
        TIMEOUT_HOMEPAGE = 30

        cardsEscolas = cardsEscolas[160:-1] # Remove a escola Mapple bear demonstração e o card "Administrador"

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

            time.sleep(5)

            novaAba = driver.window_handles[-1]
            driver.switch_to.window(novaAba)

            if driver.current_url == "about:blank":
                print("Página inválida detectada ('about:blank'). Fechando a aba.")
                driver.close()
                driver.switch_to.window(driver.window_handles[0])    
                time.sleep(1)   # Delay necessário
            
            menuCursos = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/nav/div/ul/li[2]/a"))) 
            menuCursos.click()

            time.sleep(3)

            UnidadesEscolher = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until( EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[1]/ng-select/div/div/div[3]")))
            UnidadesEscolher.click()
            
            unidades = driver.find_elements(By.XPATH, "//ng-dropdown-panel[@role='listbox']//span[@class='ng-option-label']")

            if unidades:
                for unidade in unidades:
                    if unidade.text == nomeEscola:
                        unidade.click()
                        break
                    else:
                        print(f"Escola {nomeEscola} com apenas uma unidade ou sem unidades disponíveis.")
        
            filtrarAno = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/div/div/div[3]")))
            filtrarAno.click()
            
            time.sleep(2)
            
            filtrar2025 =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/ng-dropdown-panel/div/div[2]/div[2]")))
            filtrar2025.click()
            
            time.sleep(2)
            
            clicarFiltrar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[6]/button")))
            clicarFiltrar.click()
            
            time.sleep(5)
            
            clicarFiltrar.click()
            
            time.sleep(5)
            
            listaCursos = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.lex-table-row')))
            
            quantidade_cursos = int(len(listaCursos))
            
            for i in range(1, quantidade_cursos):
            
                time.sleep(2)
                
                print(f"Valor de quantidade_cursos na iteração {i}: {quantidade_cursos} {type(quantidade_cursos)}")

                listaCursos = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.lex-table-row')))

                curso = listaCursos[i]
                print(f"Clicando no curso {i}: {curso.text}")
                texto_do_curso = curso.text
                curso.click()

                adicionarProduto = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[2]/div/button")))
                adicionarProduto.click()
                
                time.sleep(2)
                
                if "YEAR" in texto_do_curso:
                
                    buscarProduto = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/div[1]/div[1]/div/input")))
                    # buscarProduto.send_keys("SLM+ / Toddle - Colaboradores")

                    # time.sleep(2)
                    
                    # clicarAcao = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/seb-lex-table/div[2]/div[2]/div/div[4]/div/button")))
                    # clicarAcao.click()
                    
                    # time.sleep(2)
                    
                    # buscarProduto.click()
                    # buscarProduto.send_keys(Keys.CONTROL, "A")
                    # buscarProduto.send_keys(Keys.DELETE)
                    buscarProduto.send_keys("SLM+ / Toddle - Família e Alunos")
                    
                    # time.sleep(2)
                    
                    # clicarAcao2 = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#modalAddLicense > div > div > div.modal-body > seb-lex-table > div.lex-table.mt-2 > div.lex-table-content > div > div:nth-child(4) > div > button")))
                    # clicarAcao2.click()
                    # time.sleep(2)
                    
                    # buscarProduto.click()
                    # buscarProduto.send_keys(Keys.CONTROL, "A")
                    # buscarProduto.send_keys(Keys.DELETE)
                    # buscarProduto.send_keys("ÁRVORE - MAPLE BEAR")
                    
                else: 
                    buscarProduto = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/div[1]/div[1]/div/input")))
                    # buscarProduto.send_keys("SLM+ / Toddle - Colaboradores - Early")
                    
                    # clicarAcao = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/seb-lex-table/div[2]/div[2]/div/div[4]/div/button")))
                    # clicarAcao.click()
                    
                    # buscarProduto.click()
                    # buscarProduto.send_keys(Keys.CONTROL, "A")
                    # buscarProduto.send_keys(Keys.DELETE)
                    buscarProduto.send_keys("SLM+ / Toddle - Família e Alunos - Early")

                    time.sleep(2)
                try:
                    nomeProduto = driver.find_elements(By.CSS_SELECTOR, "#modalAddLicense > div > div > div.modal-body > seb-lex-table > div.lex-table.mt-2 > div.lex-table-content")
                    time.sleep(3)
                    
                    if nomeProduto[0].text == "Nenhum registro!":
                        
                        btnCancelarProduto = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/div[3]/button[1]")))
                        btnCancelarProduto.click()
                        
                        time.sleep(2)
                        
                        btnCancelar =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > seb-root > div.page-wrapper > div > seb-edit-course > div > seb-buttons-form-completion > div > button.btn.btn-light-cancel.button-cancel")))
                        btnCancelar.click()
                        
                        time.sleep(5)
                        
                        UnidadesEscolher = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until( EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[1]/ng-select/div/div/div[3]")))
                        UnidadesEscolher.click()
                        
                        unidades = driver.find_elements(By.XPATH, "//ng-dropdown-panel[@role='listbox']//span[@class='ng-option-label']")

                        if unidades:
                            for unidade in unidades:
                                if unidade.text == nomeEscola:
                                    unidade.click()
                                    break
                                else:
                                    print(f"Escola {nomeEscola} com apenas uma unidade ou sem unidades disponíveis.")
                        
            
                        filtrarAno = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/div/div/div[3]")))
                        filtrarAno.click()
                        
                        filtrar2025 =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/ng-dropdown-panel/div/div[2]/div[2]")))
                        filtrar2025.click()
                        
                        clicarFiltrar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[6]/button")))
                        clicarFiltrar.click()
                        
                        print(f"Valor de quantidade_cursos na iteração {i}: {quantidade_cursos} {type(quantidade_cursos)}")
                        
                        time.sleep(5)
                    else:
                        clicarAcao = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/seb-lex-table/div[2]/div[2]/div/div[4]/div/button")))
                        clicarAcao.click()

                        time.sleep(5)
                
                        clicarAdicionar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/div[3]/button[2]")))
                        clicarAdicionar.click()
                        
                        time.sleep(5)
                                                    
                                                    
                        salvarCurso = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-buttons-form-completion/div/button[2]")))
                        salvarCurso.click()
                    
                        time.sleep(5)
                        
                        print("Adicionado Toddle no", texto_do_curso, nomeEscola)
                        UnidadesEscolher = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until( EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[1]/ng-select/div/div/div[3]")))
                        UnidadesEscolher.click()
                        
                        time.sleep(3)
                    
                        unidades = driver.find_elements(By.XPATH, "//ng-dropdown-panel[@role='listbox']//span[@class='ng-option-label']")

                        if unidades:
                            for unidade in unidades:
                                if unidade.text == nomeEscola:
                                    unidade.click()
                                    break
                                else:
                                    print(f"Escola {nomeEscola} com apenas uma unidade ou sem unidades disponíveis.")
                            
                        filtrarAno = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/div/div/div[3]")))
                        filtrarAno.click()
                        
                        filtrar2025 =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/ng-dropdown-panel/div/div[2]/div[2]")))
                        filtrar2025.click()
                        
                        clicarFiltrar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[6]/button")))
                        clicarFiltrar.click()
                                            
                        time.sleep(3)
                
                except:
                    print("Erro na escola", nomeEscola)
                    
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)
                
        
        '''   
                time.sleep(2)
                try:
                    
                    listaProdutos = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.lex-table-row')))
                    
                    for produto in listaProdutos:
                        
                    
                    if texto_produto == 'SLM+ / Toddle':
                        time.sleep(2)
                        
                        btnCancelar =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > seb-root > div.page-wrapper > div > seb-edit-course > div > seb-buttons-form-completion > div > button.btn.btn-light-cancel.button-cancel")))
                        btnCancelar.click()
                        
                        time.sleep(5)
                        
                        UnidadesEscolher = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until( EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[1]/ng-select/div/div/div[3]")))
                        UnidadesEscolher.click()
                        
                        unidades = driver.find_elements(By.XPATH, "//ng-dropdown-panel[@role='listbox']//span[@class='ng-option-label']")

                        if unidades:
                            for unidade in unidades:
                                if unidade.text == nomeEscola:
                                    unidade.click()
                                    break
                                else:
                                    print(f"Escola {nomeEscola} com apenas uma unidade ou sem unidades disponíveis.")
                        
                        time.sleep(4)
                        
                        filtrarAno = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/div/div/div[3]")))
                        filtrarAno.click()
                        
                        filtrar2025 =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/ng-dropdown-panel/div/div[2]/div[2]")))
                        filtrar2025.click()
                        
                        clicarFiltrar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[6]/button")))
                        clicarFiltrar.click()
                        
                        time.sleep(5)
                
                        clicarFiltrar.click()
                        
                        print(f"Valor de quantidade_cursos na iteração {i}: {quantidade_cursos} {type(quantidade_cursos)}")
                        
                        time.sleep(5)
                    
                    else:
                    
                        time.sleep(5)
                        
                        adicionarProduto = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[2]/div/button")))
                        adicionarProduto.click()
                        
                        time.sleep(5)
                        
                        if "YEAR" in texto_do_curso:
                        
                            buscarProduto = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/div[1]/div[1]/div/input")))
                            buscarProduto.send_keys("SLM+ / Toddle - Colaboradores")

                            time.sleep(2)
                            
                            clicarAcao = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/seb-lex-table/div[2]/div[2]/div/div[4]/div/button")))
                            clicarAcao.click()
                            
                            buscarProduto.click()
                            buscarProduto.send_keys(Keys.CONTROL, "A")
                            buscarProduto.send_keys(Keys.DELETE)
                            buscarProduto.send_keys("ÁRVORE - MAPLE BEAR")
                            
                        else: 
                            buscarProduto = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/div[1]/div[1]/div/input")))
                            buscarProduto.send_keys("SLM+ / Toddle - Colaboradores - Early")

                            time.sleep(2)
                        
                        clicarAcao = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/seb-lex-table/div[2]/div[2]/div/div[4]/div/button")))
                        clicarAcao.click()

                        time.sleep(5)
                        
                        clicarAdicionar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/div[3]/button[2]")))
                        clicarAdicionar.click()
                        
                        time.sleep(10)
                        
                        salvarCurso = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-buttons-form-completion/div/button[2]")))
                        salvarCurso.click()
                        
                        time.sleep(10)
                        
                        print("Adicionado Toddle no", texto_do_curso, nomeEscola)
                        UnidadesEscolher = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until( EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[1]/ng-select/div/div/div[3]")))
                        UnidadesEscolher.click()
                        
                        time.sleep(10)
                        
                        unidades = driver.find_elements(By.XPATH, "//ng-dropdown-panel[@role='listbox']//span[@class='ng-option-label']")

                        if unidades:
                            for unidade in unidades:
                                if unidade.text == nomeEscola:
                                    unidade.click()
                                    break
                                else:
                                    print(f"Escola {nomeEscola} com apenas uma unidade ou sem unidades disponíveis.")
                    
                        filtrarAno = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/div/div/div[3]")))
                        filtrarAno.click()
                        
                        filtrar2025 =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/ng-dropdown-panel/div/div[2]/div[2]")))
                        filtrar2025.click()
                        
                        clicarFiltrar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[6]/button")))
                        clicarFiltrar.click()
                        
                        time.sleep(1)
                
                        clicarFiltrar.click()
                                    
                        time.sleep(3)
                except:
                    print("Erro na escola", nomeEscola)
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(1)
                '''
               
def cadastrarProdutosArvore(driver, cardsEscolas, arquivo):
    
        with codecs.open(arquivo, "a","utf-8") as file:
            file.write(f"\n\nNova execução\n\n")
    
        TIMEOUT_HOMEPAGE = 30

        cardsEscolas = cardsEscolas[110:-1] # Remove a escola Mapple bear demonstração e o card "Administrador"

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

            if driver.current_url == "about:blank":
                print("Página inválida detectada ('about:blank'). Fechando a aba.")
                driver.close()
                driver.switch_to.window(driver.window_handles[0])    
                time.sleep(1)   # Delay necessário
            
            menuCursos = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/nav/div/ul/li[2]/a"))) 
            menuCursos.click()

            time.sleep(3)

            UnidadesEscolher = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until( EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[1]/ng-select/div/div/div[3]")))
            UnidadesEscolher.click()
            
            unidades = driver.find_elements(By.XPATH, "//ng-dropdown-panel[@role='listbox']//span[@class='ng-option-label']")

            if unidades:
                for unidade in unidades:
                    if unidade.text == nomeEscola:
                        unidade.click()
                        break
                    else:
                        print(f"Escola {nomeEscola} com apenas uma unidade ou sem unidades disponíveis.")
        
            filtrarAno = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/div/div/div[3]")))
            filtrarAno.click()
                        
            filtrar2025 =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/ng-dropdown-panel/div/div[2]/div[2]")))
            filtrar2025.click()
                        
            clicarFiltrar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[6]/button")))
            clicarFiltrar.click()
            
            time.sleep(5)
            
            clicarFiltrar.click()
            
            time.sleep(5)
            
            listaCursos = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.lex-table-row')))
            
            quantidade_cursos = int(len(listaCursos))
            
            for i in range(1, quantidade_cursos):
            
                time.sleep(2)
                
                print(f"Valor de quantidade_cursos na iteração {i}: {quantidade_cursos} {type(quantidade_cursos)}")

                listaCursos = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.lex-table-row')))

                curso = listaCursos[i]
                print(f"Clicando no curso {i}: {curso.text}")
                texto_do_curso = curso.text
                curso.click()

                adicionarProduto = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[2]/div/button")))
                adicionarProduto.click()
                
                time.sleep(2)
                
                if "YEAR" in texto_do_curso:
                
                    buscarProduto = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/div[1]/div[1]/div/input")))                    
                    buscarProduto.click()
                    buscarProduto.send_keys(Keys.CONTROL, "A")
                    buscarProduto.send_keys(Keys.DELETE)
                    buscarProduto.send_keys("ÁRVORE - MAPLE BEAR")
                    
                else: 
                    btnCancelarProduto = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/div[3]/button[1]")))
                    btnCancelarProduto.click()
                    
                    time.sleep(1)
                        
                    btnCancelar =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > seb-root > div.page-wrapper > div > seb-edit-course > div > seb-buttons-form-completion > div > button.btn.btn-light-cancel.button-cancel")))
                    btnCancelar.click()
                    
                    time.sleep(5)
                    
                    UnidadesEscolher = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until( EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[1]/ng-select/div/div/div[3]")))
                    UnidadesEscolher.click()
                    
                    unidades = driver.find_elements(By.XPATH, "//ng-dropdown-panel[@role='listbox']//span[@class='ng-option-label']")

                    if unidades:
                        for unidade in unidades:
                            if unidade.text == nomeEscola:
                                unidade.click()
                                break
                            else:
                                print(f"Escola {nomeEscola} com apenas uma unidade ou sem unidades disponíveis.")
                    
        
                    filtrarAno = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/div/div/div[3]")))
                    filtrarAno.click()
                    
                    filtrar2025 =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/ng-dropdown-panel/div/div[2]/div[2]")))
                    filtrar2025.click()
                    
                    clicarFiltrar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[6]/button")))
                    clicarFiltrar.click()
                    
                    print(f"Valor de quantidade_cursos na iteração {i}: {quantidade_cursos} {type(quantidade_cursos)}")
                    
                    time.sleep(2)
                try:
                    nomeProduto = driver.find_elements(By.CSS_SELECTOR, "#modalAddLicense > div > div > div.modal-body > seb-lex-table > div.lex-table.mt-2 > div.lex-table-content")
                    time.sleep(1)
                    
                    if nomeProduto[0].text == "Nenhum registro!":
                        
                        btnCancelarProduto = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/div[3]/button[1]")))
                        btnCancelarProduto.click()
                        
                        time.sleep(2)
                        
                        btnCancelar =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > seb-root > div.page-wrapper > div > seb-edit-course > div > seb-buttons-form-completion > div > button.btn.btn-light-cancel.button-cancel")))
                        btnCancelar.click()
                        
                        time.sleep(3)
                        
                        UnidadesEscolher = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until( EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[1]/ng-select/div/div/div[3]")))
                        UnidadesEscolher.click()
                        
                        unidades = driver.find_elements(By.XPATH, "//ng-dropdown-panel[@role='listbox']//span[@class='ng-option-label']")

                        if unidades:
                            for unidade in unidades:
                                if unidade.text == nomeEscola:
                                    unidade.click()
                                    break
                                else:
                                    print(f"Escola {nomeEscola} com apenas uma unidade ou sem unidades disponíveis.")
                        
            
                        filtrarAno = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/div/div/div[3]")))
                        filtrarAno.click()
                        
                        filtrar2025 =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/ng-dropdown-panel/div/div[2]/div[2]")))
                        filtrar2025.click()
                        
                        clicarFiltrar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[6]/button")))
                        clicarFiltrar.click()
                        
                        print(f"Valor de quantidade_cursos na iteração {i}: {quantidade_cursos} {type(quantidade_cursos)}")
                        
                        time.sleep(5)
                    else:
                        clicarAcao = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/seb-lex-table/div[2]/div[2]/div/div[4]/div/button")))
                        clicarAcao.click()

                        time.sleep(1)
                
                        clicarAdicionar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/div[3]/button[2]")))
                        clicarAdicionar.click()
                        
                        time.sleep(1)
                                                    
                                                    
                        salvarCurso = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-buttons-form-completion/div/button[2]")))
                        salvarCurso.click()
                    
                        time.sleep(3)
                        
                        print("Adicionado Toddle no", texto_do_curso, nomeEscola)
                        UnidadesEscolher = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until( EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[1]/ng-select/div/div/div[3]")))
                        UnidadesEscolher.click()
                        
                        time.sleep(2)
                    
                        unidades = driver.find_elements(By.XPATH, "//ng-dropdown-panel[@role='listbox']//span[@class='ng-option-label']")

                        if unidades:
                            for unidade in unidades:
                                if unidade.text == nomeEscola:
                                    unidade.click()
                                    break
                                else:
                                    print(f"Escola {nomeEscola} com apenas uma unidade ou sem unidades disponíveis.")
                            
                        filtrarAno = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/div/div/div[3]")))
                        filtrarAno.click()
                        
                        filtrar2025 =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/ng-dropdown-panel/div/div[2]/div[2]")))
                        filtrar2025.click()
                        
                        clicarFiltrar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[6]/button")))
                        clicarFiltrar.click()
                                            
                        time.sleep(2)
                
                except:
                    print("Erro na escola", nomeEscola)
                    
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)

def fazerTudoTurma(driver, cardsEscolas,arquivo):
    with codecs.open(arquivo, "a","utf-8") as file:
        file.write(f"\n\nNova execução\n\n")
    
    TIMEOUT_HOMEPAGE = 30

    cardsEscolas = cardsEscolas[240:-1] # Remove a escola Mapple bear demonstração e o card "Administrador"


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

        time.sleep(5)

        novaAba = driver.window_handles[-1]
        driver.switch_to.window(novaAba)

        if driver.current_url == "about:blank":
            print("Página inválida detectada ('about:blank'). Fechando a aba.")
            driver.close()
            driver.switch_to.window(driver.window_handles[0])    
            time.sleep(1)   # Delay necessário
          
        menuTurmas = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/nav/div/ul/li[3]/a"))) 
        menuTurmas.click()

        time.sleep(1)
        
        UnidadesEscolher = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until( EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-class/seb-table-class/div/div/seb-table-filtro-class/form/div/div[1]/ng-select/div/div/div[2]/input")))
        UnidadesEscolher.click()
        
        unidades = driver.find_elements(By.XPATH, "//div[@class='ng-dropdown-panel-items scroll-host']//div[@class='ng-option']")

        if unidades:
            for unidade in unidades:
                if unidade.text == nomeEscola:
                    unidade.click()
                    break
                else:
                    print(f"Escola {nomeEscola} com apenas uma unidade ou sem unidades disponíveis.")
                    
        codigoTurma = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-class/seb-table-class/div/div/seb-table-filtro-class/form/div/div[2]/input")))
        codigoTurma.send_keys("SUPORTE2025")
        
        filtrarCodigo = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-class/seb-table-class/div/div/seb-table-filtro-class/form/div/div[7]/button")))
        filtrarCodigo.click()
        
        time.sleep(3)
        
        turmaExiste = driver.find_elements(By.XPATH, "//span[@class='table-text' and text()='SUPORTE LEX 2025']")
        time.sleep(3)
        
        if turmaExiste:
            print("Turma já existe na Escola:", nomeEscola)
            time.sleep(2)
            clicarTurma = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > seb-root > div.page-wrapper > div > seb-class > seb-table-class > div > div > seb-lex-table > div.lex-table.mt-2 > div.lex-table-content > div")))
            clicarTurma.click()
            
            time.sleep(1)
            
            apagarCurso = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > seb-root > div.page-wrapper > div > seb-edit-class > form > div.page-content.fade-in-up > div:nth-child(2) > div:nth-child(1) > div:nth-child(3) > ng-select > div > div > div.ng-input > input[type=text]")))
            time.sleep(1)
            apagarCurso.click()
            time.sleep(1)
            apagarCurso.send_keys(Keys.BACKSPACE)
            
            time.sleep(1)
            
            btnSemCursoEntendi =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/seb-modal-warning[8]/div/div/div/div[3]/button")))
            btnSemCursoEntendi.click()
            
            #Ano curso
            ano2025 = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[2]/div[1]/div[2]/ng-select/div/div/div[3]/input")))
            ano2025.send_keys("2025")
            ano2025.send_keys(Keys.ENTER)
            
            #Preenche Segmento e Série
            
            try:
                
                segmentoElementary = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[2]/div[1]/div[4]/ng-select/div/div/div[2]/input")))
                segmentoElementary.click
                segmentoElementary.send_keys("Elementary")
                
                time.sleep(1)
                
                serieElementary1 = driver.find_elements(By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[2]/div[1]/div[4]/ng-select/ng-dropdown-panel/div/div[2]/div")
                
                if serieElementary1:
                    
                    time.sleep(1)
                    segmentoElementary.send_keys(Keys.ENTER)
                    time.sleep(2)
                    serieEntendi = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/seb-modal-warning[4]/div/div/div/div[3]/button")))
                    serieEntendi.click()
                    time.sleep(2)
                    
                    seriecurso1 = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[2]/div[1]/div[5]/ng-select/div/div/div[2]/input")))
                    time.sleep(2)
                    #seriecurso1 = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[2]/div[1]/div[5]/ng-select/div/div/div[2]")))
                    #seriecurso1.click()
                    seriecurso1.send_keys("Year 01")
                    time.sleep(2)
                    seriecurso1.send_keys(Keys.ENTER)
                    
                    serieEntendiCurso = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/seb-modal-warning[5]/div/div/div/div[3]/button")))
                    time.sleep(5)
                    serieEntendiCurso.click()
                    time.sleep(2)
                    print("Adicionado Year 1", nomeEscola)
                    
                    # serieCurso = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[2]/div[1]/div[5]/ng-select/div/div/div[2]")))
                    # serieCurso.send_keys("Year 01")
                    # serieCurso.send_keys(Keys.ENTER)

                
                else:
                    time.sleep(1)
                    segmentoElementary.send_keys(Keys.CONTROL,"A")
                    segmentoElementary.send_keys(Keys.DELETE)
                    segmentoElementary.send_keys("Early")
                    segmentoElementary.send_keys(Keys.ENTER)
                    
                    serieSK = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[5]/ng-select/div/div/div[2]/input")))
                    serieSK.send_keys("SENIOR KINDERGARTEN")
                    serieSK.send_keys(Keys.ENTER)
                    print("Adicionado SK", nomeEscola)
                    
                    
            except:
                print("Deu erro na escola", nomeEscola, cardsEscolas) 
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(1)
                
            
            btnAddProduto =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[4]/div/button")))
            btnAddProduto.click()
            
            produtos = ["SLM+ / Toddle - Família e Alunos", "SLM+ / Toddle - Colaboradores", "ÁRVORE - MAPLE BEAR","Plataforma de Excelência Maple Bear"]
            
            for produto in produtos:
            
                buscarProdutoTurma =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/div/div/div/div[2]/div[1]/div[1]/div/input")))
                buscarProdutoTurma.send_keys(produto)
                
                btnAddProdutoBuscar =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/div/div/div/div[2]/table/tbody/tr/td[4]/button")))
                btnAddProdutoBuscar.click()
                
                buscarProdutoTurma.click()
                buscarProdutoTurma.send_keys(Keys.CONTROL,"A")
                buscarProdutoTurma.send_keys(Keys.DELETE)
                
                print("Adicionado produto: ", produto)
                
                time.sleep(1)
            
            btnAdicionarTodosProdutos =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/div/div/div/div[3]/button[2]")))
            btnAdicionarTodosProdutos.click()
            
            time.sleep(3)
                
            timeLexToddle = ["jaqueline.floriano@dnx.tec.br", "jessika.queiroz@dnx.tec.br", "fernanda.vieira@dnx.tec.br", "fernanda.inacio@dnx.tec.br", "julioc.santos@maplebear.com.br", "toddle@maplebear.com.br"] 
            
            for pessoa in timeLexToddle:
                
                try:
                    
                    if pessoa:
                        time.sleep(2)
                        inserirUsuariosTurma = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, '/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[7]/div[2]/div[1]/ng-select/div/div/div[2]/input')))
                        inserirUsuariosTurma.click()
                        inserirUsuariosTurma.send_keys(pessoa)
                        time.sleep(2)
                        inserirUsuariosTurma.send_keys(Keys.ENTER)
                        inserirUsuariosTurma.send_keys(Keys.ENTER)
                        
                        time.sleep(1)
                        
                        selecionarPerfil = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, '/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[7]/div[2]/div[2]/ng-select/div/div/div[2]/input')))
                        selecionarPerfil.click()
                        #selecionarPerfil.send_keys("Coordenador")

                        selecionarPerfilCoordenador = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[7]/div[2]/div[2]/ng-select/ng-dropdown-panel/div/div[2]/div[5]")))
                        selecionarPerfilCoordenador.click()
                        
                        time.sleep(1)
                        
                        adicionarUsuarios = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[7]/div[2]/div[3]/button")))
                        adicionarUsuarios.click()
                        
                        print("Usuário:", pessoa, "adicionado a turma!")
                        
                        WebDriverWait(driver, 5).until(EC.staleness_of(inserirUsuariosTurma))
                        continue
                    
                    else:
                        print(f"Erro ao adicionar o usuário {pessoa}")
                    
                        
                except:
                    continue
                
            
            clicarSalvar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/seb-buttons-form-completion/div/button[2]")))
            clicarSalvar.click()
            
            time.sleep(5)
            print(nomeEscola, ": Criado Turma Suporte LEX 2025")
            
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)

        
        else:
            print("Turma não existe na Escola:", nomeEscola)  
            
            criarTurma = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-class/seb-titlebar/div/div/div[2]/div/lex-button/button")))
            criarTurma.click()
            
            time.sleep(1)
            
            UnidadesTeste = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until( EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[1]/ng-select/div")))
            UnidadesTeste.click()
            
            unidades = driver.find_elements(By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[1]/ng-select/ng-dropdown-panel/div/div[2]/div")

            if unidades:
                for unidade in unidades:
                    if unidade.text == nomeEscola:
                        unidade.click()
                        break
                    else:
                        print(f"Escola {nomeEscola} com apenas uma unidade ou sem unidades disponíveis.")
            
            #Ano curso
            ano2025 = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[2]/div[1]/div[2]/ng-select/div/div/div[3]/input")))
            ano2025.send_keys("2025")
            ano2025.send_keys(Keys.ENTER)
                
            #Inserir código
            inserirCodigo = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[2]/div[1]/input")))
            inserirCodigo.send_keys("SUPORTE2025")
            
            #inserir nome da turma
            inserirNomeTurma = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[2]/div[2]/input")))
            inserirNomeTurma.send_keys("SUPORTE LEX 2025")

            try:
                
                segmentoElementary = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[2]/div[1]/div[4]/ng-select/div/div/div[2]/input")))
                segmentoElementary.click
                segmentoElementary.send_keys("Elementary")
                
                time.sleep(1)
                
                serieElementary1 = driver.find_elements(By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[2]/div[1]/div[4]/ng-select/ng-dropdown-panel/div/div[2]/div")
                
                if serieElementary1:
                
                    segmentoElementary.send_keys(Keys.ENTER)
                    serieEntendi = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/seb-modal-warning[4]/div/div/div/div[3]/button")))
                    serieEntendi.click()
                    
                    seriecurso1 = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[2]/div[1]/div[5]/ng-select/div/div/div[2]/input")))
                   
                    #seriecurso1 = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[2]/div[1]/div[5]/ng-select/div/div/div[2]")))
                    #seriecurso1.click()
                    seriecurso1.send_keys("Year 01")
                    seriecurso1.send_keys(Keys.ENTER)
                    
                    # serieCurso = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[2]/div[1]/div[5]/ng-select/div/div/div[2]")))
                    # serieCurso.send_keys("Year 01")
                    # serieCurso.send_keys(Keys.ENTER)
                    
                    serieEntendiCurso = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/seb-modal-warning[4]/div/div/div/div[3]/button")))
                    time.sleep(2)
                    serieEntendiCurso.click()
                    
                    btnAddProduto =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[4]/div/button")))
                    btnAddProduto.click()
                    
                    produtos = ["SLM+ / Toddle - Família e Alunos", "SLM+ / Toddle - Colaboradores", "ÁRVORE - MAPLE BEAR","Plataforma de Excelência Maple Bear"]
                    
                    try:
                        for produto in produtos:
                        
                            buscarProdutoTurma =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/div/div/div/div[2]/div[1]/div[1]/div/input")))
                            buscarProdutoTurma.send_keys(produto)
                            
                            btnAddProdutoBuscar =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/div/div/div/div[2]/table/tbody/tr/td[4]/button")))
                            btnAddProdutoBuscar.click()
                            
                            buscarProdutoTurma.click()
                            
                            print("Adicionado produto: ", produto)
                            
                            time.sleep(1)
                        
                            btnAddProduto =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[4]/div/button")))
                            btnAddProduto.click()
                    except (TimeoutException) as e:
                        print(f"Não foi possível adicionar o produto: {produto}. Erro: {e}")
                
                else:
                    time.sleep(1)
                    segmentoElementary.send_keys(Keys.CONTROL,"A")
                    segmentoElementary.send_keys(Keys.DELETE)
                    segmentoElementary.send_keys("Early")
                    segmentoElementary.send_keys(Keys.ENTER)
                    
                    serieSK = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[5]/ng-select/div/div/div[2]/input")))
                    serieSK.send_keys("SENIOR KINDERGARTEN")
                    serieSK.send_keys(Keys.ENTER)
                    print("Adicionado SK", nomeEscola)
                    
                    btnAddProduto =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[4]/div/button")))
                    btnAddProduto.click()
                    
                    produtos = ["SLM+ / Toddle - Colaboradores - Early", "SLM+ / Toddle - Família e Alunos - Early","Plataforma de Excelência Maple Bear"]
                    
                    try:
                    
                        for produto in produtos:
                        
                            buscarProdutoTurma =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/div/div/div/div[2]/div[1]/div[1]/div/input")))
                            buscarProdutoTurma.send_keys(produto)
                            
                            btnAddProdutoBuscar =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/div/div/div/div[2]/table/tbody/tr/td[4]/button")))
                            btnAddProdutoBuscar.click()
                            
                            buscarProdutoTurma.click()
                            
                            print("Adicionado produto: ", produto)
                        
                            btnAddProduto =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[4]/div/button")))
                            btnAddProduto.click()
                            
                    except (TimeoutException) as e:
                        print(f"Não foi possível adicionar o produto: {produto}. Erro: {e}") 
                        
                time.sleep(1)
                
            except:
                print("A unidade não possui SK ou Year 1:", nomeEscola) 
                clicar1Item =   WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/div[2]/div[1]/div[3]/ng-select")))      
                clicar1Item.click()
            
                btnAddProduto =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[4]/div/button")))
                btnAddProduto.click()
                       
            time.sleep(3)
                
            timeLexToddle = ["jaqueline.floriano@dnx.tec.br", "jessika.queiroz@dnx.tec.br", "fernanda.vieira@dnx.tec.br", "fernanda.inacio@dnx.tec.br", "julioc.santos@maplebear.com.br", "toddle@maplebear.com.br"] 
            
            for pessoa in timeLexToddle:
                
                try:
                    
                    if pessoa:
                        time.sleep(2)
                        inserirUsuariosTurma = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, '/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[7]/div[2]/div[1]/ng-select/div/div/div[2]/input')))
                        inserirUsuariosTurma.click()
                        inserirUsuariosTurma.send_keys(pessoa)
                        inserirUsuariosTurma.send_keys(Keys.ENTER)
                        inserirUsuariosTurma.send_keys(Keys.ENTER)
                        
                        time.sleep(1)
                        
                        selecionarPerfil = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, '/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[7]/div[2]/div[2]/ng-select/div/div/div[2]/input')))
                        selecionarPerfil.click()
                        #selecionarPerfil.send_keys("Coordenador")

                        selecionarPerfilCoordenador = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[7]/div[2]/div[2]/ng-select/ng-dropdown-panel/div/div[2]/div[5]")))
                        selecionarPerfilCoordenador.click()
                        
                        time.sleep(1)
                        
                        adicionarUsuarios = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-class/form/div[2]/div[7]/div[2]/div[3]/button")))
                        adicionarUsuarios.click()
                        
                        print("Usuário:", pessoa, "adicionado a turma!")
                        
                        WebDriverWait(driver, 5).until(EC.staleness_of(inserirUsuariosTurma))
                        continue
                    
                    else:
                        print(f"Erro ao adicionar o usuário {pessoa}")
                    
                        
                except:
                    continue
            
            time.sleep(1)
            
            clicarSalvar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-new-class/form/div[2]/seb-buttons-form-completion/div/button[2]/div")))
            time.sleep(1)
            clicarSalvar.click()
            
            time.sleep(5)
            print(nomeEscola, ": Turma Atualizada para 2025")
            
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)
                              
def cadastrarProdutosTodos(driver, cardsEscolas, arquivo):
    
    with codecs.open(arquivo, "a","utf-8") as file:
            file.write(f"\n\nNova execução\n\n")
    
    TIMEOUT_HOMEPAGE = 30

    cardsEscolas = cardsEscolas[180:-1] # Remove a escola Mapple bear demonstração e o card "Administrador"

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
            
            time.sleep(10)

            cardAdministrador.click()

            time.sleep(5)

            novaAba = driver.window_handles[-1]
            driver.switch_to.window(novaAba)
            
            if driver.current_url == "about:blank":
                print("Página inválida detectada ('about:blank'). Fechando a aba.")
                driver.close()  # Fecha a aba inválida

                # Verifica se ainda existem outras abas abertas
                if driver.window_handles:
                    driver.switch_to.window(driver.window_handles[0])  # Troca para a aba inicial
                    time.sleep(1)  # Pequeno delay para garantir que o foco mude corretamente

            # if driver.current_url == "about:blank":
            #     print("Página inválida detectada ('about:blank'). Fechando a aba.")
            #     driver.close()
            #     driver.switch_to.window(driver.window_handles[0])    
            #     time.sleep(1)   # Delay necessário
            
            menuCursos = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/nav/div/ul/li[2]/a"))) 
            menuCursos.click()

            time.sleep(3)

            UnidadesEscolher = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until( EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[1]/ng-select/div/div/div[3]")))
            UnidadesEscolher.click()
            
            unidades = driver.find_elements(By.XPATH, "//ng-dropdown-panel[@role='listbox']//span[@class='ng-option-label']")

            if unidades:
                for unidade in unidades:
                    if unidade.text == nomeEscola:
                        unidade.click()
                        break
                    else:
                        print(f"Escola {nomeEscola} com apenas uma unidade ou sem unidades disponíveis.")
        
            inserirYear = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[3]/input")))
            inserirYear.send_keys("YEAR")

            
            filtrarAno = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/div/div/div[3]/input")))
            filtrarAno.send_keys("2025")
            filtrarAno.send_keys(Keys.ENTER)
            
            time.sleep(2)
            filtrarAno.send_keys(Keys.ENTER)

            time.sleep(2)
            
            clicarFiltrar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[6]/button")))
            clicarFiltrar.click()
            
            time.sleep(5)  
            clicarFiltrar.click()    
              
            listaCursos = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.lex-table-row')))
            
            quantidade_cursos = int(len(listaCursos))
            
            for i in range(1, quantidade_cursos):
            
                time.sleep(2)
                
                print(f"Valor de quantidade_cursos na iteração {i}: {quantidade_cursos} {type(quantidade_cursos)}")

                listaCursos = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.lex-table-row')))

                curso = listaCursos[i]
                print(f"Clicando no curso {i}: {curso.text}")
                texto_do_curso = curso.text
                texto_normalizado = texto_do_curso.replace("\n", " ").strip()
                curso.click()

                adicionarProduto = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[2]/div/button")))
                adicionarProduto.click()
                
                time.sleep(3)
                
                cursosPearson = ["YEAR 1 2025", "YEAR 2 2025", "YEAR 3 2025", "YEAR 4 2025","YEAR 5 2025","YEAR 6 2025","YEAR 7 2025","YEAR 8 2025", "YEAR 9 2025"]
                cursosHighSchool = ["YEAR 10 2025", "YEAR 11 2025", "YEAR 12 2025"]
                
                if any(curso in texto_normalizado for curso in cursosPearson):
                    
                    time.sleep(2)
            
                    #Produto Pearson
                    buscarProduto = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/div[1]/div[1]/div/input")))
                    buscarProduto.send_keys("Pearson Resources")
                    
                    time.sleep(2)
                
                else: 
                    if any(curso in texto_normalizado for curso in cursosHighSchool):
                        time.sleep(2)
                        #Futureme
                        buscarProduto = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/div[1]/div[1]/div/input")))
                        buscarProduto.send_keys("FutureMe")
                        
                        nomeProduto = driver.find_elements(By.CSS_SELECTOR, "#modalAddLicense > div > div > div.modal-body > seb-lex-table > div.lex-table.mt-2 > div.lex-table-content")
                        time.sleep(3)
                    
                        if nomeProduto[0].text == "Nenhum registro!":
                            print("Futurme não localizado na escola",nomeEscola)
                            
                            #University Connection
                            buscarProduto = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/div[1]/div[1]/div/input")))
                            buscarProduto.send_keys("University Connection")
                            
                            nomeProduto = driver.find_elements(By.CSS_SELECTOR, "#modalAddLicense > div > div > div.modal-body > seb-lex-table > div.lex-table.mt-2 > div.lex-table-content")
                            time.sleep(3)
                            
                            if nomeProduto[0].text == "Nenhum registro!":
                                print("Não localizado University Connection", nomeEscola)
                                
                                btnCancelarProduto = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/div[3]/button[1]")))
                                btnCancelarProduto.click()
                                
                                time.sleep(2)
                                
                                btnCancelar =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > seb-root > div.page-wrapper > div > seb-edit-course > div > seb-buttons-form-completion > div > button.btn.btn-light-cancel.button-cancel")))
                                btnCancelar.click()
                                
                                time.sleep(5)
                                
                                UnidadesEscolher = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until( EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[1]/ng-select/div/div/div[3]")))
                                UnidadesEscolher.click()
                                
                                unidades = driver.find_elements(By.XPATH, "//ng-dropdown-panel[@role='listbox']//span[@class='ng-option-label']")

                                if unidades:
                                    for unidade in unidades:
                                        if unidade.text == nomeEscola:
                                            unidade.click()
                                            break
                                        else:
                                            print(f"Escola {nomeEscola} com apenas uma unidade ou sem unidades disponíveis.")
                                
                                
                                inserirYear = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[3]/input")))
                                inserirYear.send_keys("YEAR")
                    
                                filtrarAno = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/div/div/div[3]")))
                                filtrarAno.click()
                                
                                filtrar2025 =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/ng-dropdown-panel/div/div[2]/div[2]")))
                                filtrar2025.click()
                                
                                clicarFiltrar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[6]/button")))
                                clicarFiltrar.click()
                                
                                print(f"Valor de quantidade_cursos na iteração {i}: {quantidade_cursos} {type(quantidade_cursos)}")
                                
                                time.sleep(5)
                            
                            print("Adicionado University Connection", nomeEscola)
                            clicarAcao = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/seb-lex-table/div[2]/div[2]/div/div[4]/div/button")))
                            clicarAcao.click()
                                
                        clicarAcao = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/seb-lex-table/div[2]/div[2]/div/div[4]/div/button")))
                        clicarAcao.click()
                        
                        #University Connection
                        buscarProduto = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/div[1]/div[1]/div/input")))
                        buscarProduto.send_keys("University Connection")
                        
                        clicarAcao = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/seb-lex-table/div[2]/div[2]/div/div[4]/div/button")))
                        clicarAcao.click()
                        
                        time.sleep(2)
                         
                try:
                    nomeProduto = driver.find_elements(By.CSS_SELECTOR, "#modalAddLicense > div > div > div.modal-body > seb-lex-table > div.lex-table.mt-2 > div.lex-table-content")
                    time.sleep(3)
                    
                    if nomeProduto[0].text == "Nenhum registro!":
                        
                        btnCancelarProduto = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/div[3]/button[1]")))
                        btnCancelarProduto.click()
                        
                        time.sleep(2)
                        
                        btnCancelar =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "body > seb-root > div.page-wrapper > div > seb-edit-course > div > seb-buttons-form-completion > div > button.btn.btn-light-cancel.button-cancel")))
                        btnCancelar.click()
                        
                        time.sleep(5)
                        
                        UnidadesEscolher = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until( EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[1]/ng-select/div/div/div[3]")))
                        UnidadesEscolher.click()
                        
                        unidades = driver.find_elements(By.XPATH, "//ng-dropdown-panel[@role='listbox']//span[@class='ng-option-label']")

                        if unidades:
                            for unidade in unidades:
                                if unidade.text == nomeEscola:
                                    unidade.click()
                                    break
                                else:
                                    print(f"Escola {nomeEscola} com apenas uma unidade ou sem unidades disponíveis.")
                        
                        inserirYear = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[3]/input")))
                        inserirYear.send_keys("YEAR")    
                                
                        filtrarAno = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/div/div/div[3]")))
                        filtrarAno.click()
                        
                        filtrar2025 =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/ng-dropdown-panel/div/div[2]/div[2]")))
                        filtrar2025.click()
                        
                        clicarFiltrar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[6]/button")))
                        clicarFiltrar.click()
                        
                        time.sleep(2)
                        clicarFiltrar.click()
                        print(f"Valor de quantidade_cursos na iteração {i}: {quantidade_cursos} {type(quantidade_cursos)}")
                        
                        time.sleep(5)
                    else:
                        # clicarAcao = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/seb-lex-table/div[2]/div[2]/div/div[4]/div/button")))
                        # clicarAcao.click()

                        # time.sleep(5)
                        
                        clicarAcao = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/seb-lex-table/div[2]/div[2]/div/div[4]/div/button")))
                        clicarAcao.click()
                
                        clicarAdicionar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-products-edit-course/div[3]/div/div/div[2]/div[3]/button[2]")))
                        clicarAdicionar.click()
                        
                        time.sleep(5)
                                                                       
                        salvarCurso = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-edit-course/div/seb-buttons-form-completion/div/button[2]")))
                        salvarCurso.click()
                    
                        time.sleep(10)
                        
                        print("Adicionado Produto no", texto_do_curso, nomeEscola)
                        UnidadesEscolher = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until( EC.presence_of_element_located((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[1]/ng-select/div/div/div[3]")))
                        UnidadesEscolher.click()
                        
                        time.sleep(3)
                    
                        unidades = driver.find_elements(By.XPATH, "//ng-dropdown-panel[@role='listbox']//span[@class='ng-option-label']")

                        if unidades:
                            for unidade in unidades:
                                if unidade.text == nomeEscola:
                                    unidade.click()
                                    break
                                else:
                                    print(f"Escola {nomeEscola} com apenas uma unidade ou sem unidades disponíveis.")
                            
                        inserirYear = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[3]/input")))
                        inserirYear.send_keys("YEAR")                           
                        
                        filtrarAno = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/div/div/div[3]")))
                        filtrarAno.click()
                        
                        filtrar2025 =  WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[5]/ng-select/ng-dropdown-panel/div/div[2]/div[2]")))
                        filtrar2025.click()
                        
                        clicarFiltrar = WebDriverWait(driver, TIMEOUT_HOMEPAGE).until(EC.element_to_be_clickable((By.XPATH, "/html/body/seb-root/div[3]/div/seb-courses/div/seb-table-course/seb-table-filter-course/form/div/div[6]/button")))
                        clicarFiltrar.click()
                                            
                        time.sleep(3)
                
                except:
                    print("Erro na escola", nomeEscola)
                    
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)

    if len(driver.window_handles) > 1:
        driver.close()
        first_tab = driver.window_handles[0]
        driver.switch_to.window(first_tab)  
            
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

        usuariosInativar = ( "451.662.058-80" , "397.194.908-88", "400.520.268-33") #falta o luiz "451.662.058-80" , "397.194.908-88", "400.520.268-33", "329.729.308-00")
        
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
    posicoesEscolas(driver) #verifica a posiçao das escolas



    #cadastrarProdutosTodos(driver,cardsEscolas,"cursosBC25.txt")
    #fazerTudoTurma(driver,cardsEscolas,"cursosBC25.txt")
    #adicionarUsuariosTurmas(driver, cardsEscolas, "cursosBC25.txt")
    #cadastrarTurmas(driver, cardsEscolas, "cursosBC25.txt") #cadastra turmas
    #cadastrarProdutos(driver, cardsEscolas, "cursosBC25.txt")
    #cadastrarProdutosArvore(driver, cardsEscolas, "cursosBC25.txt")
    #posicoesEscolas(driver) #verifica a posiçao das escolas
    #verificarTurmas(driver, cardsEscolas,"cursos2025.txt" )
    #pegarCursos2025(driver,cardsEscolas,"cursos2025.txt")
    #pegarCNPJ(driver, cardsEscolas, "cnpjs2025.txt")

    
    
