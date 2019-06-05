from flask import Flask,request,render_template
import wikipedia
app = Flask(__name__)

@app.route("/", methods =['POST', 'GET'])
def index():
	if request.method == 'GET':
		return render_template("index.html")
	elif request.method == 'POST':
		return handle_query()

def handle_query():
	summary = '<h1>The summary is: </h1>'
	topic = request.form.get("topic")
	if topic:
		try:
			summary = summary + wikipedia.summary(str(topic))
		except wikipedia.exceptions.DisambiguationError as e:
			summary = "<h2>There is an ambiguiy!!</h2> <br> <h3>Please enter from the following options:</h3> <br>" + "<br> ".join(e.options[:20])
		except wikipedia.exceptions.PageError:
			summary = "<h2>No Page found!!</h2> <br> <h3>Please try another query</h3> <br>"
	else:
		summary = "<h1>Empty query!!!</h1>"
	return render_template("summary.html",summary = summary)


@app.route('/login', methods =['POST', 'GET'])
def login():
	if request.method == 'GET':
		return render_template("login.html")
	else:
		user, password = request.form.get("user"),request.form.get("pass")
		print(user,password)
		return "success"
@app.errorhandler(404)
def not_found_error(error):
    return (render_template('404.html'), 404)

#Error handler for 500
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return (render_template('500.html'), 500)



if __name__ == "__main__":
	app.run(use_reloader = True)
