from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
from helper import extract_info
from api import send_to_api
import json
import fitz  

def main():
    driver = webdriver.Chrome()
    base_url = "https://dje.tjsp.jus.br"
    home_url = f"{base_url}/cdje/index.do"
    published_at= "2024-11-13"  # This is the date we are interested in
    date = "13/11/2024"  # This is the date we are interested in
    try:
        driver.get(home_url)
        print(f'Iniciando a busca por publicações do dia {published_at}')
        wait = WebDriverWait(driver, 10)
        driver.execute_script(f"document.querySelector('#dtInicioString').value = '{date}';")
        driver.execute_script(f"document.querySelector('#dtFimString').value = '{date}';")

        driver.execute_script("document.querySelector('[name=\"dadosConsulta.cdCaderno\"]').value = '12'")
        driver.execute_script( """ document.querySelector('#procura').value = '"RPV" e "pagamento pelo INSS"' """)

        print("Esperando o carregamento da página...")
        search_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][value='Pesquisar']")))
        search_button.click()
        print("Aguardando os resultados...")

        time.sleep(2)

        results = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".fundocinza1")))
        if not results:
            return "No results found."
        print(f"Encontradas {len(results)} publicações.")
        rows = driver.find_elements(By.CLASS_NAME, "fundocinza1")
        extracted_data = []
        for row in rows:
            pdf_link = row.find_element(By.XPATH, ".//a[contains(@title, 'Visualizar')]")
            publication_date = pdf_link.text.split(' - ')[0]  # Extracts the date from the link text
            publication_details = row.find_element(By.CLASS_NAME,
                                                   "ementaClass2").text  # Extracts the publication content
            link = base_url + pdf_link.get_attribute('onclick').split("'")[1].replace("consultaSimples.do", "getPaginaDoDiario.do")
            extracted_data.append({
                'date': publication_date,
                'details': publication_details,
                'pdf_link': link
            })
        result_to_send = []
        for publication in extracted_data:
            pdf_link = publication['pdf_link']
            response = requests.get(pdf_link)
            doc = fitz.open(stream=response.content, filetype="pdf")
            full_text = ""
            for page in doc:
                full_text += page.get_text()
            info = extract_info(full_text, published_at)
            result_to_send.append(info)
        # with open("result.json", "w", encoding="utf-8") as f:
        #     json.dump(result_to_send, f, ensure_ascii=False, indent=2)
        send_to_api(result_to_send)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
