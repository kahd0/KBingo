import openpyxl
from openpyxl.styles import Font, Alignment
from tkinter import filedialog, messagebox
from utils.database import getAllCards, getBingoById
from utils.logging import logInfo, logError
import datetime

class ExportExcelController:
    def __init__(self, bingo_id):
        self.bingo_id = bingo_id

    def export(self):
        """Inicia o processo de exportação das cartelas para Excel."""
        try:
            # Busca todas as cartelas do bingo selecionado
            cards = getAllCards(self.bingo_id)
            if not cards:
                messagebox.showwarning("Aviso", "Nenhuma cartela encontrada para exportação.")
                return

            # Busca informações do bingo para formar o nome do arquivo
            bingo = getBingoById(self.bingo_id)
            bingo_name = bingo["name"].replace(" ", "_")
            bingo_date = datetime.datetime.strptime(bingo["date"].split()[0], "%d-%m-%Y").strftime("%Y%m%d")
            suggested_name = f"Cartelas_{bingo_name}_{bingo_date}.xlsx"

            # Solicita o local para salvar o arquivo com nome sugerido
            filePath = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")],
                initialfile=suggested_name,
                title="Salvar Cartelas em Excel"
            )
            if not filePath:
                return  # Usuário cancelou

            # Gera o arquivo Excel
            self.createExcelFile(filePath, cards)
            messagebox.showinfo("Sucesso", f"Cartelas exportadas com sucesso!\nArquivo salvo em: {filePath}")
            logInfo(f"Cartelas exportadas para Excel: {filePath}")
        except Exception as e:
            logError(f"Erro ao exportar cartelas para Excel: {e}")
            messagebox.showerror("Erro", f"Não foi possível exportar as cartelas.\n{e}")

    def createExcelFile(self, filePath, cards):
        """Cria o arquivo Excel com os dados das cartelas."""
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = "Cartelas"

        # Configura o cabeçalho
        sheet["A1"] = "Número"
        sheet["B1"] = "Pedras"
        headerFont = Font(bold=True)
        for col in ["A1", "B1"]:
            sheet[col].font = headerFont
            sheet[col].alignment = Alignment(horizontal="center")

        # Preenche os dados das cartelas
        for idx, card in enumerate(cards, start=2):
            sheet[f"A{idx}"] = card["numero_cartela"]
            sheet[f"B{idx}"] = ", ".join(map(str, card["numeros"]))

        # Ajusta largura das colunas
        sheet.column_dimensions["A"].width = 15
        sheet.column_dimensions["B"].width = 50

        # Salva o arquivo
        workbook.save(filePath)
