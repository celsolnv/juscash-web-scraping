from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
from helper import extract_info
from api import send_to_api
import fitz  # PyMuPDF

def main():
    driver = webdriver.Chrome()
    base_url = "https://dje.tjsp.jus.br"
    home_url = f"{base_url}/cdje/index.do"
    try:
        driver.get(home_url)
        wait = WebDriverWait(driver, 10)
        driver.execute_script("document.querySelector('#dtInicioString').value = '13/11/2024';")
        driver.execute_script("document.querySelector('#dtFimString').value = '13/11/2024';")
        driver.execute_script("document.querySelector('[name=\"dadosConsulta.cdCaderno\"]').value = '12'")
        driver.execute_script( """ document.querySelector('#procura').value = '"RPV" e "pagamento pelo INSS"' """)

        search_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][value='Pesquisar']")))
        search_button.click()

        time.sleep(2)

        results = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".fundocinza1")))
        if not results:
            return "No results found."
        rows = driver.find_elements(By.CLASS_NAME, "fundocinza1")
        print(f"Found {len(rows)} results.")
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
            print(f"Downloading {pdf_link}")
            response = requests.get(pdf_link)
            doc = fitz.open(stream=response.content, filetype="pdf")
            full_text = ""
            for page in doc:
                full_text += page.get_text()
            info = extract_info(full_text)
            print(info)
            result_to_send.append(info)
        print(result_to_send)
        # send_to_api(result_to_send)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
