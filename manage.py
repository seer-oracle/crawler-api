# -*- coding: utf-8 -*-


# File: manage.py
"""
   Description:
        -
        -
"""
from gevent import monkey

monkey.patch_all()

from src import create_app
from flask_script import Manager
from src.services.price import get_price_socket
import asyncio
import threading

app = create_app()
manager = Manager(app)

def ws_worker():
    print("worker")
    loop = asyncio.new_event_loop()
    loop.run_until_complete(get_price_socket())
    loop.close()

threading.Thread(target=ws_worker, daemon=True).start()


@manager.command
def run():
    """Run in local machine."""
    # TODO set debug to False
    app.run(host='0.0.0.0', port="5004", debug=False)

manager.add_option('-c', '--config',
                   dest="config",
                   required=False,
                   help="config file")

if __name__ == "__main__":
    manager.run()