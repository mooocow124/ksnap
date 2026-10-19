from microdot import Microdot # our server library, yipee!

app = Microdot()

@app.route('/')
async def index(request):
    return 'Hello, world!'

app.run(host="127.0.0.1", port=80)