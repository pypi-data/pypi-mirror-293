from bs4 import BeautifulSoup
import requests
from .response_correios import ResponseCep

class CepSearch:

    def __init__(self):
        self.url_address = "https://www2.correios.com.br/sistemas/buscacep/resultadoBuscaEndereco.cfm"
        self.url_cep = "https://www2.correios.com.br/sistemas/buscacep/resultadoBuscaCepEndereco.cfm"


    def get_address_by_cep(self, cep) -> dict:
        """
        It returns ResponseCep as dict (rua, bairro, cidade, cep, uf)
        """
        if not cep.strip():
            raise ValueError("CEP is empty")
        
        form_data = { "CEP": cep }

        data = requests.post(self.url_address, data=form_data)

        soup_address = BeautifulSoup(data.text, features="html.parser")
        nodes = soup_address.find_all("td")
        
        rua = nodes[0].string.strip()
        bairro = nodes[1].string.strip()
        data_splitted = nodes[2].string.split("/")
        cidade = data_splitted[0].strip()
        uf = data_splitted[1].strip()
        
        result = ResponseCep(rua, bairro, cidade, cep, uf)

        return result.__dict__
    

    def get_cep_by_address(self, address) -> list:
        """
        It returns a list of ResponseCep(rua, bairro, cidade, cep, uf)
        """

        if not address.strip():
            raise ValueError("address is empty")
        
        form_data = { "relaxation": address, "tipoCEP": "ALL", "semelhante": "N" }

        data = requests.post(self.url_cep, data=form_data)
        hasNextPage = False
        list_addresses = []

        soup_cep = BeautifulSoup(data.text, features="html.parser")
        
        link = soup_cep.find_all("a")

        for x in link:
            for y in x.contents:
                if y == "[ Próxima ]":
                    hasNextPage = True

        nodes = soup_cep.find_all("td")

        for idx, i in enumerate(nodes):
            if idx % 4 == 0:
                rua = nodes[idx + 0].get_text().strip()
                bairro = nodes[idx + 1].get_text().strip()
                data_splitted = nodes[idx + 2].get_text().split("/")
                cidade = data_splitted[0].strip()
                uf = data_splitted[1].strip()
                cep = nodes[idx + 3].get_text().strip()
                resp_cep = ResponseCep(rua, bairro, cidade, cep, uf)
                list_addresses.append(resp_cep)

        if hasNextPage:
            self.__access_next_pages(list_addresses, address)

        return list_addresses
    
    
    def __access_next_pages(self, list_addresses, address, pag_ini = 51, pag_fim = 100):
        
        hasNextPage = False

        form_data = { "relaxation": address,
                     "exata":"5",
                      "tipoCEP": "ALL", 
                      "semelhante": "N",
                      "qtdrow": "50",
                      "pagIni": str(pag_ini),
                      "pagFim": str(pag_fim)
                        }

        data = requests.post(self.url_cep, data=form_data)
        soup_cep = BeautifulSoup(data.text, features="html.parser")
        
        link = soup_cep.find_all("a")

        if not hasNextPage:
            for x in link:
                for y in x.contents:
                    if y == "[ Próxima ]":
                        hasNextPage = True
                        pag_ini += 25
                        pag_fim += 25

        
        nodes = soup_cep.find_all("td")

        for idx, i in enumerate(nodes):
            if idx % 4 == 0:
                rua = nodes[idx + 0].get_text().strip()
                bairro = nodes[idx + 1].get_text().strip()
                data_splitted = nodes[idx + 2].get_text().split("/")
                cidade = data_splitted[0].strip()
                uf = data_splitted[1].strip()
                cep = nodes[idx + 3].get_text().strip()
                resp_cep = ResponseCep(rua, bairro, cidade, cep, uf)
                list_addresses.append(resp_cep)

        if hasNextPage:
            self.__access_next_pages(list_addresses, address, pag_ini, pag_fim)