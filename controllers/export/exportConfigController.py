import customtkinter as ctk
from tkinter import StringVar, IntVar, messagebox
from utils.helpers import centralizeWindowRelative

class ExportConfigController(ctk.CTkToplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.title("Configurar Exportação de Cartelas")
        centralizeWindowRelative(parent, self, 400, 350)
        self.transient(parent)
        self.grab_set()

        self.callback = callback  # Função para retornar as configurações
        self.exportType = StringVar(value="Excel")
        self.cardsPerPage = IntVar(value=6)
        self.pageOrientation = StringVar(value="Retrato")

        self.createWidgets()

    def createWidgets(self):
        """Cria os widgets do modal de exportação."""
        ctk.CTkLabel(self, text="Escolha o Tipo de Exportação:", font=("Arial", 14)).pack(pady=10)

        # Tipo de Exportação
        exportFrame = ctk.CTkFrame(self)
        exportFrame.pack(padx=20, pady=5, fill="x")
        ctk.CTkRadioButton(exportFrame, text="Excel", variable=self.exportType, value="Excel", command=self.togglePdfOptions).pack(anchor="w", padx=5)
        ctk.CTkRadioButton(exportFrame, text="PDF", variable=self.exportType, value="PDF", command=self.togglePdfOptions).pack(anchor="w", padx=5)

        # Configurações para PDF
        self.pdfFrame = ctk.CTkFrame(self)
        self.pdfFrame.pack(padx=20, pady=10, fill="x")

        self.cardsPerPageLabel = ctk.CTkLabel(self.pdfFrame, text="Cartelas por Página:")
        self.cardsPerPageLabel.grid(row=0, column=0, sticky="w", pady=5)
        self.cardsPerPageEntry = ctk.CTkEntry(self.pdfFrame, textvariable=self.cardsPerPage)
        self.cardsPerPageEntry.grid(row=0, column=1, padx=5)

        self.pageOrientationLabel = ctk.CTkLabel(self.pdfFrame, text="Orientação da Página:")
        self.pageOrientationLabel.grid(row=1, column=0, sticky="w", pady=5)
        self.pageOrientationMenu = ctk.CTkOptionMenu(self.pdfFrame, variable=self.pageOrientation, values=["Retrato", "Paisagem"])
        self.pageOrientationMenu.grid(row=1, column=1, padx=5)

        # Botões
        buttonFrame = ctk.CTkFrame(self)
        buttonFrame.pack(pady=20)

        ctk.CTkButton(buttonFrame, text="Confirmar", command=self.confirmConfig).pack(side="left", padx=10)
        ctk.CTkButton(buttonFrame, text="Cancelar", command=self.destroy).pack(side="right", padx=10)

        # Inicialmente oculta as opções PDF se necessário
        self.togglePdfOptions()

    def togglePdfOptions(self):
        """Mostra ou esconde as opções de PDF com base no tipo selecionado."""
        if self.exportType.get() == "PDF":
            self.pdfFrame.pack(padx=20, pady=10, fill="x")
        else:
            self.pdfFrame.pack_forget()

    def confirmConfig(self):
        """Retorna as configurações selecionadas."""
        exportType = self.exportType.get()
        cardsPerPage = self.cardsPerPage.get()
        pageOrientation = self.pageOrientation.get()

        if exportType == "PDF" and cardsPerPage <= 0:
            messagebox.showerror("Erro", "O número de cartelas por página deve ser maior que zero.")
            return

        # Retorna as configurações ao callback
        self.callback({
            "exportType": exportType,
            "cardsPerPage": cardsPerPage,
            "pageOrientation": pageOrientation
        })
        self.destroy()
