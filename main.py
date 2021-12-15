#!/usr/bin/env python3
#┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
#┃IUTv2 Server Core b0001                ┃
#┃> coded with <3 by 0x7df, 2021         ┃
#┃> licensed under MIT License           ┃
#┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
#
from dotenv import load_dotenv
from quart import Quart, redirect, render_template
from quart_auth import AuthManager, current_user, logout_user
from quart_rate_limiter import RateLimiter, rate_limit

import asyncio, uvloop

from hypercorn.asyncio import serve
from hypercorn.config import Config

from datetime import datetime, timedelta
import secrets
import time
import os
#

os.chdir("/root/iutools.ru")
load_dotenv()

app = Quart(
	__name__,
	static_url_path='',
	static_folder  ='static',
	template_folder='html'
)

app.secret_key = os.getenv('app_key')
app.config["QUART_AUTH_COOKIE_NAME"] = 'fumo'
app.config["QUART_AUTH_DURATION"   ] = 24 * 60 * 60
app.config["QUART_AUTH_SALT"       ] = os.getenv('auth_key')
app.config["TEMPLATES_AUTO_RELOAD" ] = True

AuthManager(app)
RateLimiter(app)

from ext.auth import auth
from ext.home import home

@app.route('/', methods=["GET","POST"])
@rate_limit(256, timedelta(hours=12))
async def router():
	if (await current_user.is_authenticated) == False:
		return await auth()
	else:
		return await home()

@app.route('/d', methods=["GET"])
@rate_limit(16, timedelta(hours=12))
async def donate():
	if (await current_user.is_authenticated) == True:
		return redirect(
			f'https://oplata.qiwi.com/create?publicKey=48e7qUxn9T7RyYE1MVZswX1FRSbE6iyCj2gCRwwF3Dnh5XrasNTx3BGPiMsyXQFNKQhvukniQG8RTVhYm3iPwNMchpfi4NV1yp7Msu65dNspwyyCtMnLz8wRiEh8a67RZvYtNcdXqewJ56d9qTNukyesaaTcjryqbSpCqigU9xPZcZeVmeA7mHLF64VCZ&comment=Донат+на+развитие+IUTools+:)&lifetime={(datetime.now()+timedelta(minutes=15)).strftime("%Y-%m-%dT%H%M")}&successUrl=https%3A%2F%2Fiutools.ru'
		)
	else:
		return redirect('/')

@app.route('/l', methods=['GET'])
@rate_limit(256, timedelta(hours=12))
async def logout():
	logout_user()
	return redirect('/')

@app.errorhandler(Exception)
async def exception_handler(error):
	code = getattr(error, "code", 500)

	if code == 429:
		return await render_template('error.html', code="429", desc="too many requests")

	if code == 500:
		return await render_template('error.html', code="500", desc="internal server error")

	return redirect('/')

if __name__ == '__main__':
	uvloop.install()

	asyncio.run(
    serve(app, Config().from_toml('hypercorn.toml'))
	)
