from tornado.testing import AsyncHTTPTestCase
import tornado
from src import main


class Testing(AsyncHTTPTestCase):

    def get_app(self) -> tornado.web.Application:
        return main.make_app()

    def test_page(self) -> None:
        response = self.fetch('/result/primeNum&3')
        assert response.body == b'5'
