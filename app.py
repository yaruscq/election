# app.py


from electionPkg import create_app

app = create_app()
app.run(debug=True)