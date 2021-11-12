def senha():
    password = 'apm'
    digitacao = input('Digite a senha do sistema:')
    if password == digitacao:
        def escola():
            return render_template('escola.html')
    else:
        def retorno():
            return render_template('index.html')