from datetime import datetime


def aplicar_mascara_e_validar(entry, tipo):
    texto = "".join(filter(str.isdigit, entry.get()))

    if tipo == "data":
        texto = texto[:8]
        if len(texto) > 4:
            texto = f"{texto[:2]}/{texto[2:4]}/{texto[4:]}"
        elif len(texto) > 2:
            texto = f"{texto[:2]}/{texto[2:]}"
    elif tipo == "horario":
        texto = texto[:4]
        if len(texto) > 2:
            texto = f"{texto[:2]}:{texto[2:]}"

    entry.delete(0, "end")
    entry.insert(0, texto)

    if (tipo == "data" and len(texto) == 10) or (tipo == "horario" and len(texto) == 5):
        try:
            formato = "%d/%m/%Y" if tipo == "data" else "%H:%M"
            datetime.strptime(texto, formato)
            entry.configure(border_color="#2fa572")
        except ValueError:
            entry.configure(border_color="#c84343")
    else:
        entry.configure(border_color=["#979da2", "#565b5e"])
