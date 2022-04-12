def comatoslash(text):
    if not '//' in text:
        l = list(str(text).split(','))
        text = ''
        for i in l:
            if i == '':
                text += ' ' + '//'
            else:
                text += i + '//'
        return text
    return text