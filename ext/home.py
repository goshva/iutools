from quart import request, render_template, redirect
from quart_auth import current_user
from ext.db import search
import re

async def home():
	if request.method=='POST':
		if "interneturok.ru/school/lesson" in str((await request.form)["lesson_url"]): # check if link contains iu shit
			try: # ill fix it someday...
				id = re.search( # search first digit in link (lesson id)
					"\\d+",
					str((await request.form)["lesson_url"])
				).group()
			except: # set id to 0 if no digit found
				id = 0


			return await render_template(
				'home.html', result=[
					["video_library", "Разборы"   , search(id, "parsing")], # search yt videos for lesson
					["task"         , "Тесты"     , search(id, "twork"  )], # search ykl tworks for lesson
					["article"      , "Письменное", search(id, "paper"  )]  # search paperworkls for lesson
				]
			)

	return await render_template('home.html')
