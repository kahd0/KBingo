from tkcalendar import Calendar
from tkinter import ttk, messagebox
from tkinter.simpledialog import askstring
import customtkinter as ctk
import json  # Import necessário para trabalhar com JSON
from utils.database import addBingo, getAllBingos, deleteBingo, updateBingo
from settings import FONT_TITLE, FONT_NORMAL
from utils.helpers import centralizeWindowRelative
from utils.logging import logInfo, logError



class BingoController(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.labelTitle = ctk.CTkLabel(self, text="Gerenciamento de Bingos", font=FONT_TITLE)
        self.labelTitle.pack(pady=10)

        # Tabela de Bingos
        self.bingoTable = ctk.CTkFrame(self)  # Frame que vai conter a tabela
        self.bingoTable.pack(fill="both", expand=True, padx=10, pady=5)

        # Botão Adicionar Bingo
        self.addButton = ctk.CTkButton(self, text="Adicionar Bingo", command=self.openAddBingoModal)
        self.addButton.pack(pady=10)

        # Carrega a tabela inicialmente
        self.refreshTable()

    def openBingoModal(self, title, bingo=None):
        """Cria uma modal para adicionar ou editar um bingo."""
        modal = ctk.CTkToplevel(self)
        modal.title(title)
        centralizeWindowRelative(self, modal, 700, 600)
        modal.transient(self)
        modal.grab_set()

        # Frame Principal
        mainFrame = ctk.CTkFrame(modal)
        mainFrame.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame Esquerdo - Campos do Bingo
        leftFrame = ctk.CTkFrame(mainFrame)
        leftFrame.pack(side="left", fill="y", expand=True, padx=(0, 5))

        # Nome do Bingo
        ctk.CTkLabel(leftFrame, text="Nome do Bingo:", font=FONT_NORMAL).pack(anchor="w")
        nameEntry = ctk.CTkEntry(leftFrame, placeholder_text="Nome do Bingo")
        nameEntry.pack(fill="x", pady=2)
        if bingo:
            nameEntry.insert(0, bingo["name"])

        # Data e Hora
        dateTimeFrame = ctk.CTkFrame(leftFrame)
        dateTimeFrame.pack(fill="x", pady=5)

        ctk.CTkLabel(dateTimeFrame, text="Data do Bingo:", font=FONT_NORMAL).grid(row=0, column=0, sticky="w", padx=5)
        calendar = Calendar(dateTimeFrame, date_pattern="dd-mm-yyyy", locale="pt_BR")
        calendar.grid(row=1, column=0, padx=5, pady=2)
        if bingo:
            calendar.selection_set(bingo["date"].split(" ")[0])

        ctk.CTkLabel(dateTimeFrame, text="Horário (HH:MM):", font=FONT_NORMAL).grid(row=0, column=1, sticky="w", padx=5)
        timeCombo = ttk.Combobox(dateTimeFrame, values=[f"{h:02}:{m:02}" for h in range(24) for m in (0, 30)])
        timeCombo.grid(row=1, column=1, padx=5)
        if bingo:
            timeCombo.set(bingo["date"].split(" ")[1])
        else:
            timeCombo.set("20:00")

        # Valor da Cartela
        ctk.CTkLabel(leftFrame, text="Valor da Cartela (R$):", font=FONT_NORMAL).pack(anchor="w", pady=5)
        valueEntry = ctk.CTkEntry(leftFrame, placeholder_text="Exemplo: 10.00")
        valueEntry.pack(fill="x", pady=2)
        if bingo:
            valueEntry.insert(0, f"{bingo['cartela_value']:.2f}")

        # Responsáveis
        ctk.CTkLabel(leftFrame, text="Responsáveis:", font=FONT_NORMAL).pack(anchor="w", pady=5)
        responsaveisEntry = ctk.CTkTextbox(leftFrame, height=60)
        responsaveisEntry.pack(fill="both", expand=True, pady=2)
        if bingo:
            responsaveisEntry.insert("1.0", bingo["responsaveis"])

        # Frame Direito - Prêmios
        rightFrame = ctk.CTkFrame(mainFrame)
        rightFrame.pack(side="right", fill="y", expand=True, padx=(5, 0))

        ctk.CTkLabel(rightFrame, text="Prêmios:", font=FONT_NORMAL).pack(anchor="w")

        self.prizeList = json.loads(bingo["prizes"]) if bingo and bingo["prizes"] else []
        self.prizeListFrame = ctk.CTkFrame(rightFrame)
        self.prizeListFrame.pack(fill="both", expand=True, pady=5)
        self.updatePrizeList()

        # Botões de Gerenciamento de Prêmios
        buttonsFrame = ctk.CTkFrame(rightFrame)
        buttonsFrame.pack(fill="x", pady=5)

        ctk.CTkButton(buttonsFrame, text="Adicionar Prêmio", command=self.addPrize).pack(side="left", padx=2)
        ctk.CTkButton(buttonsFrame, text="Remover Prêmio", command=self.removePrize).pack(side="left", padx=2)

        # Botão Salvar
        return {
            "modal": modal,
            "nameEntry": nameEntry,
            "calendar": calendar,
            "timeCombo": timeCombo,
            "valueEntry": valueEntry,
            "responsaveisEntry": responsaveisEntry
        }

    def openAddBingoModal(self):
        """Abre a modal para adicionar um novo bingo."""
        fields = self.openBingoModal("Adicionar Bingo")

        def saveNewBingo():
            """Salva o novo bingo."""
            name = fields["nameEntry"].get().strip()
            date = fields["calendar"].get_date()
            time = fields["timeCombo"].get()
            cartelaValue = fields["valueEntry"].get().strip().replace(",", ".")
            responsaveis = fields["responsaveisEntry"].get("1.0", "end").strip()

            if not all([name, date, time, cartelaValue, responsaveis, self.prizeList]):
                logError("Erro: Todos os campos são obrigatórios!")
                messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
                return

            addBingo(name, f"{date} {time}", float(cartelaValue), responsaveis, self.prizeList)
            self.refreshTable()
            fields["modal"].destroy()

        ctk.CTkButton(fields["modal"], text="Salvar Bingo", command=saveNewBingo).pack(pady=10)

    def saveBingo(self):
        """Salva o bingo no banco de dados."""
        name = self.bingoNameEntry.get().strip()
        date = self.calendar.get_date()
        time = self.timeCombo.get()
        cartelaValue = self.cartelaValueEntry.get().strip().replace(",", ".")  # Trata vírgula no valor
        responsaveis = self.responsaveisText.get("1.0", "end").strip()
        premios = self.prizeList  # Lista de prêmios

        if not all([name, date, time, cartelaValue, responsaveis, premios]):
            ctk.CTkLabel(self.bingoModal, text="Erro: Todos os campos são obrigatórios!", text_color="red").pack()
            return

        try:
            # Concatena data e hora
            dateTime = f"{date} {time}"

            # Salva no banco de dados
            addBingo(name, dateTime, float(cartelaValue), responsaveis, premios)
            logInfo(f"Bingo '{name}' salvo com sucesso.")

            # Atualiza a tabela de bingos
            self.refreshTable()

            # Fecha a janela modal
            self.bingoModal.destroy()
        except ValueError as ve:
            logError(f"Erro no valor da cartela: {ve}")
            ctk.CTkLabel(self.bingoModal, text="Erro: Valor da cartela inválido!", text_color="red").pack()
        except Exception as e:
            logError(f"Erro ao salvar o bingo '{name}': {e}")
            ctk.CTkLabel(self.bingoModal, text=f"Erro: {e}", text_color="red").pack()

    def addPrize(self):
        """Abre uma janela modal para adicionar um prêmio com dois campos."""
        self.prizeModal = ctk.CTkToplevel(self)
        self.prizeModal.title("Adicionar Prêmio")
        centralizeWindowRelative(self, self.prizeModal, 400, 200)
        self.prizeModal.transient(self)
        self.prizeModal.grab_set()

        # Frame Principal
        modalFrame = ctk.CTkFrame(self.prizeModal)
        modalFrame.pack(fill="both", expand=True, padx=10, pady=10)

        # Campo de Descrição do Prêmio
        ctk.CTkLabel(modalFrame, text="Descrição do Prêmio:", font=FONT_NORMAL).pack(anchor="w", pady=2)
        self.premioEntry = ctk.CTkEntry(modalFrame, placeholder_text="Exemplo: R$ 500,00")
        self.premioEntry.pack(fill="x", pady=5)

        # Campo de Condição de Vitória
        ctk.CTkLabel(modalFrame, text="Condição de Vitória:", font=FONT_NORMAL).pack(anchor="w", pady=2)
        self.condicaoEntry = ctk.CTkEntry(modalFrame, placeholder_text="Exemplo: 5 pedras")
        self.condicaoEntry.pack(fill="x", pady=5)

        # Botão Salvar
        ctk.CTkButton(modalFrame, text="Salvar", command=self.savePrize).pack(pady=10)

    def savePrize(self):
        """Salva o prêmio preenchido na modal."""
        premio = self.premioEntry.get().strip()
        condicao = self.condicaoEntry.get().strip()

        if premio and condicao:
            self.prizeList.append({"premio": premio, "condicao": condicao})
            self.updatePrizeList()
            self.prizeModal.destroy()
        else:
            ctk.CTkMessagebox.show_error("Erro", "Preencha todos os campos!")

    def removePrize(self):
        """Remove o último prêmio da lista."""
        if self.prizeList:
            self.prizeList.pop()
            self.updatePrizeList()

    def updatePrizeList(self):
        """Atualiza a exibição da lista de prêmios."""
        for widget in self.prizeListFrame.winfo_children():
            widget.destroy()

        for idx, prize in enumerate(self.prizeList, start=1):
            label = ctk.CTkLabel(
                self.prizeListFrame, text=f"{idx}. {prize['premio']} - {prize['condicao']}", font=FONT_NORMAL
            )
            label.pack(anchor="w", padx=5, pady=2)

    def refreshTable(self):
        """Atualiza a tabela de bingos na interface."""
        # Limpa os widgets existentes
        for widget in self.bingoTable.winfo_children():
            widget.destroy()

        # Cabeçalho da tabela
        headers = ["Nome", "Data", "Valor Cartela", "Responsáveis", "Ações"]
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(self.bingoTable, text=header, font=FONT_NORMAL, padx=10, pady=5)
            label.grid(row=0, column=col, sticky="nsew")

        # Configura expansão das colunas
        for col in range(len(headers)):
            self.bingoTable.grid_columnconfigure(col, weight=1)

        # Obtém os dados do banco
        bingos = getAllBingos()  # Deve retornar uma lista de dicionários

        # Exibe os dados na tabela
        for row, bingo in enumerate(bingos, start=1):
            ctk.CTkLabel(self.bingoTable, text=bingo["name"], font=FONT_NORMAL).grid(row=row, column=0, sticky="nsew", padx=5, pady=2)
            ctk.CTkLabel(self.bingoTable, text=bingo["date"], font=FONT_NORMAL).grid(row=row, column=1, sticky="nsew", padx=5, pady=2)
            ctk.CTkLabel(self.bingoTable, text=f"R$ {bingo['cartela_value']:.2f}", font=FONT_NORMAL).grid(row=row, column=2, sticky="nsew", padx=5, pady=2)
            ctk.CTkLabel(self.bingoTable, text=bingo["responsaveis"], font=FONT_NORMAL).grid(row=row, column=3, sticky="nsew", padx=5, pady=2)

            # Botões de Ação
            actionFrame = ctk.CTkFrame(self.bingoTable)
            actionFrame.grid(row=row, column=4, sticky="nsew", padx=5, pady=2)

            editButton = ctk.CTkButton(actionFrame, text="Editar", width=80, command=lambda b=bingo: self.openEditBingo(b))
            editButton.pack(side="left", padx=2)

            deleteButton = ctk.CTkButton(actionFrame, text="Excluir", width=80, command=lambda b=bingo: self.confirmDeleteBingo(b))
            deleteButton.pack(side="right", padx=2)

    def confirmDeleteBingo(self, bingo):
        """Confirma e exclui um bingo do banco de dados."""
        confirm = messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir o bingo '{bingo['name']}'?")
        if confirm:
            try:
                deleteBingo(bingo["id"])  # Chama a função do banco
                self.refreshTable()  # Atualiza a tabela
                logInfo(f"Bingo '{bingo['name']}' excluído com sucesso.")
            except Exception as e:
                logError(f"Erro ao excluir bingo: {e}")
                messagebox.showerror("Erro", f"Não foi possível excluir o bingo: {e}")

    def openEditBingo(self, bingo):
        """Abre a modal para editar um bingo existente."""
        fields = self.openBingoModal("Editar Bingo", bingo)

        def saveEditedBingo():
            """Salva as alterações no bingo."""
            name = fields["nameEntry"].get().strip()
            date = fields["calendar"].get_date()
            time = fields["timeCombo"].get()
            cartelaValue = fields["valueEntry"].get().strip().replace(",", ".")
            responsaveis = fields["responsaveisEntry"].get("1.0", "end").strip()

            if not all([name, date, time, cartelaValue, responsaveis]):
                logError("Erro: Todos os campos são obrigatórios!")
                return

            updateBingo(bingo["id"], name, f"{date} {time}", float(cartelaValue), responsaveis)
            self.refreshTable()
            fields["modal"].destroy()

        ctk.CTkButton(fields["modal"], text="Salvar Alterações", command=saveEditedBingo).pack(pady=10)

    def saveEditedBingo(self, bingoId, nameEntry, calendar, timeEntry, valueEntry, responsaveisEntry):
        """Salva as alterações do bingo editado no banco de dados."""
        name = nameEntry.get().strip()
        date = calendar.get_date()
        time = timeEntry.get().strip()
        cartelaValue = valueEntry.get().strip().replace(",", ".")
        responsaveis = responsaveisEntry.get("1.0", "end").strip()

        if not all([name, date, time, cartelaValue, responsaveis]):
            logError("Erro: Todos os campos são obrigatórios!")
            messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
            return

        try:
            # Atualiza o banco de dados
            updateBingo(bingoId, name, f"{date} {time}", float(cartelaValue), responsaveis)
            logInfo(f"Bingo '{name}' atualizado com sucesso.")

            # Atualiza a tabela e fecha a modal
            self.refreshTable()
            self.editModal.destroy()
        except Exception as e:
            logError(f"Erro ao salvar o bingo: {e}")
