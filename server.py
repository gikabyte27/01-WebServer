from flask import Flask, render_template, url_for

app = Flask(__name__)

posts = [
    {
        'author': 'Gika',
        'title': 'Prima postare',
        'content': 'Mesajul meu din prima postare',
        'date_posted': '19 Septembrie 2024'
    },
    {
        'author': 'John Doe',
        'title': 'A doua postare',
        'content': 'Mesajul meu din a doua postare',
        'date_posted': '20 Mai 2024'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About!')

if __name__ == '__main__':
    app.run(debug=True)