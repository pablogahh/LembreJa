import time
import database as db
from datetime import datetime


def verificar_alarmes_loop(app, recarregar_callback):
    from tkinter import messagebox

    while True:
        # Espera 5 segundos antes da próxima checagem
        time.sleep(5)

        try:
            agora = datetime.now()
            data_atual = agora.strftime("%d/%m/%Y")
            horario_atual = agora.strftime("%H:%M")

            alarmes = db.carregar_alarmes()
            alteracao = False

            for alarme in alarmes:
                if (
                    alarme["data"] == data_atual
                    and alarme["horario"] == horario_atual
                    and not alarme.get("disparado", False)
                ):
                    alarme["disparado"] = True
                    alteracao = True

                    # 1. Avisa a tela principal para abrir o Alerta
                    app.after(
                        0,
                        lambda tit=alarme["titulo"]: messagebox.showinfo(
                            "🔔 Alarme!", f"Hora de: {tit}"
                        ),
                    )

                    # 2. Só recarrega a interface aqui dentro do IF, após o disparo!
                    app.after(200, recarregar_callback)

                    # Lógica de arquivamento (roda em background)
                    def processar_limpeza(id_al=alarme["id"]):
                        lista = db.carregar_alarmes()
                        for item in lista:
                            if item["id"] == id_al:
                                db.arquivar_no_historico(item)
                                break
                        db.salvar_alarmes([i for i in lista if i["id"] != id_al])
                        app.after(0, recarregar_callback)

                    app.after(10000, processar_limpeza)

            if alteracao:
                db.salvar_alarmes(alarmes)

        except Exception as e:
            print(f"Erro no motor: {e}")
