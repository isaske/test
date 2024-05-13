from flask import Flask
from threading import Thread
from highrise.__main__ import *
import time
from global_variables import *
from F_guard_carg import *


class WebServer():

  def __init__(self):
    self.app = Flask(__name__)

    @self.app.route('/')
    def index() -> str:
      return "✅MINIMIZA LA APP, Y VUELVE AL HR✅"

  def run(self) -> None:
    self.app.run(host='0.0.0.0', port=8080)

  def keep_alive(self):
    t = Thread(target=self.run)
    t.start()


class RunBot():

  bot_token = "2fd15dd284ce5693b5820e6321efa7f877a04e19548712a584069eab9027a83f"
  bot_file = "main"
  bot_class = "Bot"

  def __init__(self) -> None:
    self.variables = cargar_variables()
    self.room_id = self.variables['room_idSave']
    self.definitions = [
        BotDefinition(
            getattr(import_module(self.bot_file), self.bot_class)(),
            self.room_id, self.bot_token)
    ]  # More BotDefinition classes can be added to the definitions list

  def run_loop(self) -> None:
    while True:
      try:
        self.variables = cargar_variables()
        self.room_id = self.variables['room_idSave']
        self.definitions[0].room_id = self.room_id
        arun(main(self.definitions))
      except Exception as e:
        print("Error: ", e)
        time.sleep(4)


if __name__ == "__main__":
  WebServer().keep_alive()

  RunBot().run_loop()
