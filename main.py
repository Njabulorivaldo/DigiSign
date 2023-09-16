from website import create_app
from flask import Flask, render_template

def run_app():
    app = create_app()
    app.run(debug=True)


#@app.route('/')
#def home():
#    return render_template('index.html')


if __name__ == "__main__":
    #app.run(debug=True)
    run_app()