from microblog import create_app

app = create_app("microblog")
app.run(debug=True)