import asyncio
import sympy
import tornado.web
import tornado.escape


class MainHandler(tornado.web.RequestHandler):

    def get(self) -> None:
        self.render("MainPage.html")

    def post(self) -> None:
        command = self.get_argument('command')
        number = self.get_argument('num')
        self.redirect("/result/" + command + "&" + number)


class GetData (tornado.web.RequestHandler):

    def get(self, result: str) -> None:
        data = result.split("&")
        if data[0] == 'fib':
            self.write(str(self.fibonacci(int(data[1]))))
        else:
            self.write(str(self.primary_nums(int(data[1]))))

    def fibonacci(self, n: int) -> int:
        fib1 = fib2 = 1
        n -= 2
        while n > 0:
            fib1, fib2 = fib2, fib1 + fib2
            n -= 1
        return fib2

    def primary_nums(self, n: int) -> int:
        print(type(sympy.prime(n)))
        return sympy.prime(n)


def make_app() -> tornado.web.Application:
    return tornado.web.Application([
        (r"/", MainHandler),
        (r'/result/([^/]+)', GetData)
    ])


async def main() -> None:
    app = make_app()
    app.listen(8888)
    shutdown_event = asyncio.Event()
    await shutdown_event.wait()


if __name__ == "__main__":
    asyncio.run(main())
