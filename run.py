from flask import Flask
from flask import render_template
from flask_wtf import Form
from flask_wtf.file import FileField
from wtforms import StringField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileRequired
from werkzeug import secure_filename
from flask import abort
from flask_wtf import RecaptchaField

app = Flask(__name__)

app.config['SECRET_KEY'] = 'very strong secret key'
app.config['RECAPTCHA_USE_SSL'] = True
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LdQyAoTAAAAAKYDQbvdFFvnWMZwpOj-IIOEtYYX'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LdQyAoTAAAAAMNDDF4VbxK4PyqjnCk1TZ2vpnbP'

class MyForm(Form):
  user_name = StringField('user_name', validators=[DataRequired(), Length(3, 5)])
  user_file = FileField('user_file', validators=[DataRequired(), FileRequired()])
  recaptcha = RecaptchaField()

@app.route('/', methods=['GET', 'POST'])
def index():
    form = MyForm()
    if form.validate_on_submit():
        filename = secure_filename(form.user_file.data.filename)
        if not filename:
            return abort(404)
        form.user_file.data.save('./' + filename)
        return '<html><body>Form data validated</body></html>'
    return render_template('index.html', form=form)

if __name__ == '__main__':
   app.run(debug=True)
