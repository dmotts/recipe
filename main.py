from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def recipe():
    return render_template('recipe.html')

if __name__ == '__main__':
    app.run(debug=True)
