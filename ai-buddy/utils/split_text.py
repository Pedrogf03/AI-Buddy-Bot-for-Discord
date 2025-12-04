def split_text(texto, limite=1900):
    fragmentos = []
    while len(texto) > limite:
        corte = texto.rfind('\n', 0, limite)
        
        if corte == -1:
            corte = texto.rfind('. ', 0, limite)
        
        if corte == -1:
            corte = texto.rfind(' ', 0, limite)
        
        if corte == -1:
            corte = limite

        punto_corte = corte + 1 if texto[corte] in ['.', '\n'] else corte
        
        fragmentos.append(texto[:punto_corte])
        texto = texto[punto_corte:].strip()

    fragmentos.append(texto)
    return fragmentos