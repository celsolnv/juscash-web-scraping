from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configuração do WebDriver
# Certifique-se de que o ChromeDriver esteja instalado e acessível no seu PATH.
driver = webdriver.Chrome()

try:
    # Acessar o site do DJE
    driver.get("https://dje.tjsp.jus.br/cdje/index.do")

    # Esperar até que os elementos estejam disponíveis
    wait = WebDriverWait(driver, 10)
    driver.execute_script("document.querySelector('#dtInicioString').value = '13/11/2024';")
    driver.execute_script("document.querySelector('#dtFimString').value = '13/11/2024';")
    driver.execute_script(""" document.querySelector('[name="dadosConsulta.cdCaderno"]').value = '12'""")
    driver.execute_script("""document.querySelector('#procura').value = '"RPV" e "pagamento pelo INSS"'""")

    # Clicar no botão "Pesquisar"
    pesquisar_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][value='Pesquisar']")))
    pesquisar_button.click()

    # Esperar um pouco para visualizar os resultados antes de fechar o navegador
    time.sleep(5)
    
    # Verificar se há resultados
    resultados = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table#resultadoConsulta tbody tr")))
    if resultados:
      

finally:
    # Fechar o navegador
    driver.quit()