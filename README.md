# Web Scraping DJE-SP - RPV/INSS

Automação para coletar e extrair publicações de RPV/INSS no DJE-SP (Diário da Justiça Eletrônico de São Paulo).

## 🛠 Tecnologias utilizadas

- Python 3
- Selenium
- PyMuPDF (`fitz`)
- Requests

## 📦 Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/web-scraping.git
   cd web-scraping
   ```

2. Crie e ative o ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   # venv\Scripts\activate    # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuração

Edite a variável `date` no início do arquivo `scraper.py` para definir o dia da consulta.

```python
date = "13/11/2024"
```

## ▶️ Execução

Para rodar o scraper, execute:

```bash
python3 scraper.py
```

O script irá:

- Acessar o site do DJE-SP
- Filtrar publicações com os termos “RPV” e “pagamento pelo INSS”
- Baixar e extrair texto dos PDFs
- Estruturar os dados e enviá-los automaticamente para a API REST

## 📄 Saída

Os dados extraídos são enviados para a API backend como JSON, contendo:
- Número do processo
- Autor(a)
- Advogado(a)
- Valores (principal, juros, honorários)
- Texto completo da publicação
- Status inicial: `new`

---

> Esse projeto faz parte de um sistema maior com backend em Node.js e frontend em React.
