import customtkinter as ctk
from tkinter import ttk
from datetime import datetime
from utils.database import getAllBingos, getCardStats
from utils.helpers import centralizeWindowRelative
from utils.logging import logInfo, logError
from settings import FONT_TITLE, FONT_NORMAL
import json

class SelectBingoController(ctk.CTkToplevel):
    def __init__(self, parent, callback, displayArea):
        super().__init__(parent)
        self.callback = callback
        self.displayArea = displayArea
        self.title("Selecionar Bingo")
        centralizeWindowRelative(parent, self, 600, 400)  # Centraliza o modal
        self.transient(parent)
        self.grab_set()

        self.bingos = []
        self.showPastBingos = ctk.BooleanVar(value=True)

        self.createWidgets()
        self.loadBingos()


    def createWidgets(self):
        # Título
        titleLabel = ctk.CTkLabel(self, text="Selecione um Bingo", font=FONT_TITLE)
        titleLabel.pack(pady=10)

        # Checkbox para esconder bingos passados
        self.hidePastCheck = ctk.CTkCheckBox(
            self, text="Ocultar Bingos com Data Passada", variable=self.showPastBingos,
            command=self.filterBingos
        )
        self.hidePastCheck.pack(pady=5)

        # Frame da Tabela
        self.tableFrame = ctk.CTkFrame(self)
        self.tableFrame.pack(fill="both", expand=True, padx=10, pady=10)

        # Treeview para Tabela
        self.bingoTable = ttk.Treeview(self.tableFrame, columns=("name", "date"), show="headings")
        self.bingoTable.heading("name", text="Nome")
        self.bingoTable.heading("date", text="Data")
        self.bingoTable.pack(fill="both", expand=True)

        # Botão de Selecionar
        selectButton = ctk.CTkButton(self, text="Selecionar", command=self.selectBingo)
        selectButton.pack(pady=10)

    def loadBingos(self):
        try:
            self.bingos = getAllBingos()
            logInfo("Bingos carregados com sucesso.")
            self.filterBingos()
        except Exception as e:
            logError(f"Erro ao carregar bingos: {e}")

    def filterBingos(self):
        # Limpa a tabela
        for row in self.bingoTable.get_children():
            self.bingoTable.delete(row)

        # Aplica o filtro
        hidePast = not self.showPastBingos.get()
        now = datetime.now()

        for bingo in self.bingos:
            bingoDate = datetime.strptime(bingo["date"], "%d-%m-%Y %H:%M")
            if hidePast and bingoDate < now:
                continue
            self.bingoTable.insert("", "end", values=(bingo["name"], bingo["date"]))

        logInfo(f"Filtro aplicado: Ocultar Bingos Passados = {hidePast}")

    def selectBingo(self):
        selectedItem = self.bingoTable.selection()
        if selectedItem:
            bingoName = self.bingoTable.item(selectedItem, "values")[0]
            self.callback(bingoName)  # Atualiza o nome do bingo no MainView

            # Busca todos os bingos para passar à função
            bingos = self.bingos  # A lista de bingos já carregada no controlador
            SelectBingoController.displayBingoDetails(self.displayArea, bingoName, bingos)  # Exibe os detalhes
            self.destroy()
        else:
            logError("Nenhum bingo selecionado.")



    @staticmethod
    def displayBingoDetails(displayArea, bingoName, bingos):
        """Exibe os detalhes do bingo na área principal."""
        selectedBingo = next((b for b in bingos if b["name"] == bingoName), None)
        if not selectedBingo:
            logError(f"Detalhes do bingo '{bingoName}' não encontrados.")
            return

        from utils.database import getCardStats
        total_cartelas, lote_atual = getCardStats(selectedBingo['id'])

        # Limpa a área principal
        for widget in displayArea.winfo_children():
            widget.destroy()

        # Frame Principal Dividido
        mainFrame = ctk.CTkFrame(displayArea, corner_radius=10)
        mainFrame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        ctk.CTkLabel(mainFrame, text="Detalhes do Bingo", font=FONT_TITLE).pack(padx=10, pady=10)

        # Informações Principais
        infoFrame = ctk.CTkFrame(mainFrame, corner_radius=10)
        infoFrame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(infoFrame, text=f"Nome: {selectedBingo['name']}", font=FONT_NORMAL).pack(anchor="w", padx=10, pady=5)
        ctk.CTkLabel(infoFrame, text=f"Data: {selectedBingo['date']}", font=FONT_NORMAL).pack(anchor="w", padx=10, pady=5)
        ctk.CTkLabel(infoFrame, text=f"Valor da Cartela: R$ {selectedBingo['cartela_value']:.2f}", font=FONT_NORMAL).pack(anchor="w", padx=10, pady=5)
        ctk.CTkLabel(infoFrame, text=f"Responsáveis: {selectedBingo['responsaveis']}", font=FONT_NORMAL).pack(anchor="w", padx=10, pady=5)
        ctk.CTkLabel(infoFrame, text=f"Total de Cartelas: {total_cartelas}", font=FONT_NORMAL).pack(anchor="w", padx=10, pady=5)
        ctk.CTkLabel(infoFrame, text=f"Lote Atual: {lote_atual:02d}", font=FONT_NORMAL).pack(anchor="w", padx=10, pady=5)

        # Frame Prêmios
        prizesFrame = ctk.CTkFrame(mainFrame, corner_radius=10)
        prizesFrame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(prizesFrame, text="Prêmios:", font=FONT_NORMAL).pack(pady=5)
        prizes = json.loads(selectedBingo['prizes'])
        for idx, prize in enumerate(prizes, start=1):
            ctk.CTkLabel(prizesFrame, text=f"{idx}. {prize['premio']} - {prize['condicao']}", font=FONT_NORMAL).pack(anchor="w", padx=20, pady=2)
