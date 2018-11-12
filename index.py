from flask import Flask, redirect , url_for, render_template, abort, request
app = Flask(__name__)
@app.route('/')
def root():
    return render_template('index.html')

if __name__=="__main__":
    app.run(host='localhost', debug=True)
