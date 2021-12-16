from quart import request, render_template, redirect
from quart_auth import AuthUser, current_user, login_user
import requests, secrets
import os

async def auth():
	if request.method == 'POST':
		r = requests.post('https://www.google.com/recaptcha/api/siteverify', data={
			"secret"   : os.getenv('re_key'),
			"response" : (await request.form)["g-recaptcha-response"]
		})

		if r.json()["success"]:
			login_user(
				AuthUser(secrets.token_urlsafe(16)), True # generate uid and save session
			)

			return redirect('/')

	return await render_template('auth.html')

