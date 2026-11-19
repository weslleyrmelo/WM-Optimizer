import ctypes
import sys
import threading
import customtkinter as ctk
from tkinter import messagebox
from backend import (
    executar_limpeza_geral,
    otimizar_windows_gamer,
    restaurar_padrao_windows,
)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def eh_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def pedir_admin():
    if getattr(sys, "frozen", False):
        # Quando já estiver rodando como .exe
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, "", None, 1)
    else:
        # Quando estiver rodando pelo VS Code (.py)
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, f'"{__file__}"', None, 1
        )

class AppOtimizador(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("WM Optimizer - Limpeza & Performance")
        self.geometry("500x610")
        self.resizable(False, False)

        # Card principal arredondado
        self.card = ctk.CTkFrame(self, corner_radius=16, fg_color="#1e1e24")
        self.card.pack(fill="both", expand=True, padx=20, pady=20)

        # Cabeçalho
        self.lbl_titulo = ctk.CTkLabel(
            self.card,
            text="⚡ OTIMIZADOR WINDOWS",
            font=ctk.CTkFont(family="Segoe UI", size=20, weight="bold"),
            text_color="#ffffff",
        )
        self.lbl_titulo.pack(pady=(22, 4))

        self.lbl_subtitulo = ctk.CTkLabel(
            self.card,
            text="Limpeza profunda de cache e ajustes para máxima performance",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#9ca3af",
        )
        self.lbl_subtitulo.pack(pady=(0, 18))

        # Botão 1: Limpeza
        self.btn_limpar = ctk.CTkButton(
            self.card,
            text="🧹  Limpar Arquivos Temporários & Cache",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            height=42,
            corner_radius=10,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            command=self.acao_limpar,
        )
        self.btn_limpar.pack(fill="x", padx=28, pady=6)

        # Botão 2: Otimização Gamer
        self.btn_otimizar = ctk.CTkButton(
            self.card,
            text="🚀  Ativar Modo Gamer & Desempenho Máximo",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            height=42,
            corner_radius=10,
            fg_color="#16a34a",
            hover_color="#15803d",
            command=self.acao_otimizar,
        )
        self.btn_otimizar.pack(fill="x", padx=28, pady=6)

        # Botão 3: Restaurar Padrão
        self.btn_restaurar = ctk.CTkButton(
            self.card,
            text="↩️  Restaurar Padrão do Windows",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            height=42,
            corner_radius=10,
            fg_color="#374151",
            hover_color="#4b5563",
            command=self.acao_restaurar,
        )
        self.btn_restaurar.pack(fill="x", padx=28, pady=6)

        # Barra de progresso animada
        self.progresso = ctk.CTkProgressBar(
            self.card,
            mode="indeterminate",
            height=6,
            corner_radius=3,
            progress_color="#38bdf8",
        )
        self.progresso.pack(fill="x", padx=28, pady=(16, 6))
        self.progresso.set(0)

        # Status dinâmico
        self.lbl_status = ctk.CTkLabel(
            self.card,
            text="● Pronto para executar (Modo Administrador)",
            font=ctk.CTkFont(family="Segoe UI", size=11),
            text_color="#38bdf8",
        )
        self.lbl_status.pack(pady=(0, 8))

        # Caixa de Log / Relatório de Atividades
        self.caixa_log = ctk.CTkTextbox(
            self.card,
            height=155,
            corner_radius=10,
            fg_color="#121216",
            text_color="#d1d5db",
            font=ctk.CTkFont(family="Consolas", size=11),
            border_width=1,
            border_color="#2e2e38",
        )
        self.caixa_log.pack(fill="x", padx=28, pady=(4, 12))
        self.escrever_log("Aguardando comando...\nSelecione uma opção acima para iniciar.")

        # Rodapé / Assinatura
        self.lbl_credito = ctk.CTkLabel(
            self.card,
            text="Desenvolvido por Weslley Melo",
            font=ctk.CTkFont(family="Segoe UI", size=11, weight="bold"),
            text_color="#6b7280",
        )
        self.lbl_credito.pack(side="bottom", pady=(0, 12))

    def limpar_log(self):
        self.caixa_log.configure(state="normal")
        self.caixa_log.delete("1.0", "end")
        self.caixa_log.configure(state="disabled")

    def escrever_log(self, mensagem):
        self.caixa_log.configure(state="normal")
        self.caixa_log.insert("end", mensagem + "\n")
        self.caixa_log.see("end")
        self.caixa_log.configure(state="disabled")

    def log_seguro(self, mensagem):
        self.after(0, lambda: self.escrever_log(mensagem))

    def iniciar_carregamento(self, texto, titulo_log):
        self.btn_limpar.configure(state="disabled")
        self.btn_otimizar.configure(state="disabled")
        self.btn_restaurar.configure(state="disabled")
        self.lbl_status.configure(text=texto, text_color="#facc15")
        self.limpar_log()
        self.escrever_log(f"--- {titulo_log} ---")
        self.progresso.start()

    def finalizar_carregamento(self, status_texto, resumo_log):
        self.progresso.stop()
        self.progresso.set(1)
        self.lbl_status.configure(text=status_texto, text_color="#4ade80")
        self.escrever_log("----------------------------------------")
        self.escrever_log(resumo_log)
        self.btn_limpar.configure(state="normal")
        self.btn_otimizar.configure(state="normal")
        self.btn_restaurar.configure(state="normal")

    def acao_limpar(self):
        self.iniciar_carregamento("⏳ Limpando pastas temporárias e caches...", "INICIANDO FAXINA DO SISTEMA")

        def tarefa():
            total = executar_limpeza_geral(log_callback=self.log_seguro)
            self.after(
                0,
                lambda: self.finalizar_carregamento(
                    f"✔ Faxina concluída! {total} itens removidos.",
                    f"CONCLUÍDO: {total} arquivos/pastas removidos no total.",
                ),
            )

        threading.Thread(target=tarefa, daemon=True).start()

    def acao_otimizar(self):
        self.iniciar_carregamento("⏳ Aplicando ajustes de registro e energia...", "ATIVANDO MODO GAMER")

        def tarefa():
            otimizar_windows_gamer(log_callback=self.log_seguro)
            self.after(
                0,
                lambda: self.finalizar_carregamento(
                    "✔ Modo Gamer & Desempenho Máximo ativados!",
                    "CONCLUÍDO: Todas as otimizações foram aplicadas.",
                ),
            )

        threading.Thread(target=tarefa, daemon=True).start()

    def acao_restaurar(self):
        confirmar = messagebox.askyesno(
            "Restaurar Padrão",
            "Deseja voltar a telemetria, a Xbox Game Bar, as prioridades e o plano de energia (Equilibrado) para o padrão original do Windows?",
        )
        if not confirmar:
            return

        self.iniciar_carregamento("⏳ Restaurando configurações originais...", "RESTAURANDO PADRÃO DO WINDOWS")

        def tarefa():
            restaurar_padrao_windows(log_callback=self.log_seguro)
            self.after(
                0,
                lambda: self.finalizar_carregamento(
                    "✔ Configurações padrão restauradas!",
                    "CONCLUÍDO: Windows restaurado ao padrão original.",
                ),
            )

        threading.Thread(target=tarefa, daemon=True).start()

if __name__ == "__main__":
    if not eh_admin():
        pedir_admin()
        sys.exit()

    app = AppOtimizador()
    app.mainloop()