import pratlang

while True:
		text = input('pratlang ')
		result, error = pratlang.start(text)

		if error: print(error.as_string())
		else: print(result)
