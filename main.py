from website import create_app
from flask import Flask, render_template

def run_app():
    app = create_app()
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=5000, debug="True")


if __name__ == "__main__":
    #app.run(debug=True)
    run_app()
