from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class FormDadosTrabalheConosco(FlaskForm):
    nomecompleto = StringField('Nome Completo', validators=[DataRequired(), Length(5, 30)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    telefone = StringField('Telefone - (DDD) 99999-9999', validators=[DataRequired(), Length(10, 16)])
    curriculo = FileField('Currículo em PDF', validators=[FileAllowed(['pdf'], 'Apenas arquivos PDF são permitidos.')])
    botao_confirmar = SubmitField('Enviar Currículo')

class FormContato(FlaskForm):
    nome = StringField('Nome Completo', validators=[DataRequired(), Length(5, 30)])
    empresa = StringField('Nome da empresa', validators=[DataRequired()])
    cnpj = StringField('CNPJ - XX.XXX.XXX/XXXX-XX', validators=[DataRequired(), Length(14, 18)])
    email_contato = StringField('E-mail', validators=[DataRequired(), Email()])
    telefone_contato = StringField('Telefone (DDD) 99999-9999', validators=[DataRequired(), Length(10, 16)])
    mensagem = StringField('Mensagem', validators=[DataRequired(), Length(15, 300)])
    botao_contato = SubmitField('Mensagem')





