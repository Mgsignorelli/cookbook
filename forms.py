from wtforms import Form, BooleanField, StringField, PasswordField, validators, FieldList, FormField, \
    SelectMultipleField


class Select2FormField(SelectMultipleField):
    def pre_validate(self, form):
        pass

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = ",".join(valuelist)
        else:
            self.data = ""


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('password_confirm', message='Passwords must match')
    ])
    password_confirm = PasswordField('Repeat Password')


class RecipeCreateForm(Form):
    title = StringField('Title', [validators.Length(min=4, max=25)])
    categories = Select2FormField('Category', [validators.DataRequired()])
    method = StringField('Method', [validators.Length(min=6)])
    ingredients = Select2FormField('Ingredient', [validators.DataRequired()])


class RecipeEditForm(Form):
    title = StringField('Title', [validators.Length(min=4, max=25)])
    categories = Select2FormField('Category', [validators.DataRequired()])
    method = StringField('Method', [validators.Length(min=6)])
    ingredients = Select2FormField('Ingredient', [validators.DataRequired()])
