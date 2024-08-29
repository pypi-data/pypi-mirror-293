import unittest
from src.py_cep_search import cepsearch
from unittest.mock import patch, MagicMock
from pathlib import Path

class CepSearchTests(unittest.TestCase):

    def setUp(self) -> None:

        relative_path = 'mock_data_address.html'
        dir = Path(__file__).parent
        absolute_path = dir.joinpath(relative_path)
        with open(absolute_path, "r") as file:
            self.html_address = file.read()

        relative_path = 'mock_data_cep.html'
        dir = Path(__file__).parent
        absolute_path = dir.joinpath(relative_path)
        with open(absolute_path, "r") as file:
            self.html_cep = file.read()


    @patch('requests.post')
    def test_get_address_by_cep(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status = 200

        mock_response.read.return_value = self.html_cep
        mock_response.text = self.html_cep

        mock_requests.return_value = mock_response

        obj = cepsearch.CepSearch()
        address = obj.get_address_by_cep("69918-120")
        self.assertIsNotNone(address)
        self.assertEqual(address["rua"], "Rua Frei Caneca")


    def test_get_address_by_cep_error(self):
        obj = cepsearch.CepSearch()
        self.assertRaises(ValueError, obj.get_address_by_cep, "")

    
    @patch('requests.post')
    def test_get_cep_by_address(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status = 200

        mock_response.read.return_value = self.html_address
        mock_response.text = self.html_address

        mock_requests.return_value = mock_response

        obj = cepsearch.CepSearch()
        ceps = obj.get_cep_by_address("Rua Frei Caneca")
        self.assertIsNotNone(ceps)
        self.assertEqual(50, len(ceps))

    
    def test_get_cep_by_address_error(self):
        obj = cepsearch.CepSearch()
        self.assertRaises(ValueError, obj.get_cep_by_address, "")

    

    if __name__ == '__main__':
        unittest.main(argv=['first-arg-is-ignored'], exit=False)