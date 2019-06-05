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
	topic = request.form.get("topic")
	summary = '<h1>{}</h1>'.format(topic)
	if topic:
		try:
			summary = summary + wikipedia.summary(str(topic))
		except wikipedia.exceptions.DisambiguationError as e:
			summary = "<h2>There is an ambiguty!!</h2> <h3>Please enter from the following options:</h3> <br>" + "<br> ".join(e.options[:20])
		except wikipedia.exceptions.PageError:
			summary = "<h3 style='color:red'>No Page found!! <br> Please try another query</h3> <br>"
	else:
		summary = "<h3 style='color:red'>Empty query!!!</h3>"
	return render_template("summary.html",summary = summary)

@app.errorhandler(404)
def not_found_error(error):
    return (render_template('error.html',code = "404"), 404)

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return (render_template('error.html',code = "500"), 500)



if __name__ == "__main__":
	app.run(use_reloader = True)
