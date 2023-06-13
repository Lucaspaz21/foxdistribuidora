import os
import secrets
from flask import render_template, url_for, request, flash, redirect
from foxdistribuidora.forms import FormDadosTrabalheConosco, FormContato
from foxdistribuidora import app
import smtplib
import email.message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#para enviar email com anexo
from email.mime.base import MIMEBase
from email import encoders
import os
from werkzeug.utils import secure_filename

@app.route("/")
def home():
    return render_template('home.html')


def salvar_pdf(arquivo_pdf, nome_completo, codigo):
    if arquivo_pdf:
        nome_arquivo = secure_filename(nome_completo + codigo + '.pdf')
        caminho_completo = os.path.join(app.root_path, 'static/curriculo', nome_arquivo)
        try:
            arquivo_pdf.save(caminho_completo)
            print(f"PDF salvo com sucesso: {caminho_completo}")
            return nome_arquivo
        except Exception as e:
            print(f"Erro ao salvar o PDF: {str(e)}")
            return None
    return None


def email_contato(nome_de_contato, empresa, cnpj, e_mail, telefone, mensagem):
    nomecontato, empresa, cnpj, e_mail, telefone, mensagem = nome_de_contato, empresa, cnpj, e_mail, telefone, mensagem
    corpo_email = corpo_email = f'''
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f2f2f2;
                padding: 20px;
            }}
            
            h1 {{
                color: #333;
            }}
            
            p {{
                color: #666;
                margin-bottom: 10px;
            }}
            
            b {{
                color: #000;
            }}
            
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: #fff;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }}
            
            .container h1 {{
                font-size: 24px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Contato de <b>{nomecontato}</b></h1>  
            <br>
            <p>Empresa: <b>{empresa}</b></p>
            <p>CNPJ: <b>{cnpj}</b></p>
            <p>E-mail: <b>{e_mail}</b></p>
            <p>Telefone: <b>{telefone}</b></p>
            <p>Mensagem:</p>
            <p><b>{mensagem}</b></p>
        </div>
    </body>
    </html>
    '''

    msg = email.message.Message()
    msg['Subject'] = f"E-mail de contato "
    msg['From'] = 'lspaz2125@gmail.com'
    msg['To'] = 'lucas.paz12@gmail.com'
    password = 'yfwaprhmwprrnfcd'
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    # Login Credentials for sending the mail
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('Email enviado')


def email_curriculo(caminho, nomecompleto, telefone, email):
    # 1 - startar o servidor SMTP

     host = "smtp.gmail.com"
    port = "587"
    login = "lspaz2125@gmail.com"
    senha = "yfwaprhmwprrnfcd"

    # conectando no servidor
    server = smtplib.SMTP(host, port)

    server.ehlo()
    server.starttls()

    # fazendo login
    server.login(login, senha)

    # 2 - construuir o email tipo MINE

    corpo = "Contato via Site" \
            f"\nNome completo: {nomecompleto}" \
            f"\nTelefone: {telefone}" \
            f"\nE-mail: {email}" \
            f"\n\nSegue Anexo"

    corpo_email = f'''
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f2f2f2;
                    padding: 20px;
                }}

                h1 {{
                    color: #333;
                }}

                p {{
                    color: #666;
                    margin-bottom: 10px;
                }}

                b {{
                    color: #000;
                }}

                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 5px;
                    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                }}

                .container h1 {{
                    font-size: 24px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Curriculo de <b>{nomecompleto}</b></h1>  
                <br>
                <p>E-mail: <b>{email}</b></p>
                <p>Telefone: <b>{telefone}</b></p>
            </div>
        </body>
        </html>
        '''

    email_msg = MIMEMultipart()
    email_msg['From'] = login
    email_msg['To'] = login
    email_msg['Subject'] = "Contato - Trabalhe Conosco"
    email_msg.attach(MIMEText(corpo_email, 'html'))

    # pegando anexo

    # abrimos o arquivo em modo leitura e binary
    arquivo = caminho
    attchment = open(arquivo, 'rb')

    # lemos o arquivo no modo binario e jogamos codificado em base 64(que é o que o email precisa)
    att = MIMEBase('application', 'octet-stream')
    att.set_payload(attchment.read())
    encoders.encode_base64(att)

    # adicioanamos o cabecalho no tipo anexo de email
    att.add_header('Content-Disposition', f'attachment; filename=catalogo.pdf')
    # fechamos o arquivo
    attchment.close()

    # colocamos o anexo no corpo do email
    email_msg.attach(att)

    # 3 - enviar o email tipo MINE no sercidor SMTP

    server.sendmail(email_msg['From'], email_msg['To'], email_msg.as_string())

    server.quit()

@app.route("/trabalheconosco", methods=['GET', 'POST'])
def trabalheconosco():
    form_trabalheconosco = FormDadosTrabalheConosco()
    form_contato = FormContato()

    if request.method == 'POST':
        print("Entrou no POST")
        if 'botao_contato' in request.form:
            if form_contato.validate():
                print("Formulário de contato válido")
                flash('Mensagem enviada com sucesso', 'alert-success')
                email_contato(nome_de_contato=form_contato.nome.data, empresa=form_contato.empresa.data,
                              cnpj=form_contato.cnpj.data, e_mail=form_contato.email_contato.data,
                              telefone=form_contato.telefone_contato.data, mensagem=form_contato.mensagem.data)
                return redirect(url_for('home'))
            else:
                print("Formulário de contato inválido")
        elif 'botao_confirmar' in request.form:
            if form_trabalheconosco.validate():
                print("Formulário de trabalheconosco válido")
                arquivo_pdf = form_trabalheconosco.curriculo.data
                nome_completo = form_trabalheconosco.nomecompleto.data
                telefone = form_trabalheconosco.telefone.data
                email = form_trabalheconosco.email.data
                codigo = codigo = secrets.token_hex(6)
                nome_arquivo = salvar_pdf(arquivo_pdf, nome_completo, codigo)
                caminho_arquivo = f"foxdistribuidora/static/curriculo/{nome_arquivo}"
                if caminho_arquivo:
                    email_curriculo(caminho_arquivo, nome_completo, telefone, email)
                flash('Currículo enviado com sucesso', 'alert-success')
                return redirect(url_for('home'))
            else:
                print("Formulário de trabalheconosco inválido")

    return render_template('trabalheconosco.html', form_trabalheconosco=form_trabalheconosco, form_contato=form_contato)



@app.route("/sobre")
def sobre():
    return render_template('sobre.html')





