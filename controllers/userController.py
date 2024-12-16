import customtkinter as ctk
import tkinter.messagebox as messagebox
from utils.database import getAllUsers, deleteUser, addUser, updateUser
from utils.logging import logInfo, logError
from utils.helpers import centralizeWindowRelative
from settings import FONT_TITLE, FONT_NORMAL


class UserController(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        # Título
        self.labelTitle = ctk.CTkLabel(
            self, text="Gerenciamento de Usuários", font=FONT_TITLE
        )
        self.labelTitle.pack(pady=10)

        # Frame para Tabela
        self.userTable = ctk.CTkFrame(self)
        self.userTable.pack(pady=10, fill="x")

        # Botão para Adicionar Usuário
        self.addButton = ctk.CTkButton(
            self, text="Adicionar Usuário", command=self.addNewUser
        )
        self.addButton.pack(pady=5, padx=10)

        # Atualiza a grade com os usuários
        self.refreshTable()

    def refreshTable(self):
        """Atualiza a tabela de usuários."""
        for widget in self.userTable.winfo_children():
            widget.destroy()

        # Cabeçalho
        headers = ["Usuário", "Permissão", "Ações"]
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(
                self.userTable, text=header, font=FONT_NORMAL, padx=10, pady=5
            )
            label.grid(row=0, column=col, sticky="nsew")

        # Ajuste de colunas para expandir igualmente
        for col in range(3):
            self.userTable.grid_columnconfigure(col, weight=1)

        # Dados dos Usuários
        users = getAllUsers()  # Consulta os dados do banco, sem incluir o master
        for row, user in enumerate(users, start=1):
            ctk.CTkLabel(self.userTable, text=user["user"], font=FONT_NORMAL).grid(
                row=row, column=0, sticky="nsew", padx=5, pady=2
            )
            ctk.CTkLabel(self.userTable, text=user["role"], font=FONT_NORMAL).grid(
                row=row, column=1, sticky="nsew", padx=5, pady=2
            )

            # Botões de ação
            editButton = ctk.CTkButton(
                self.userTable,
                text="Editar",
                command=lambda u=user: self.editUser(u),
                width=80,
            )
            editButton.grid(row=row, column=2, sticky="w", padx=5, pady=2)

            deleteButton = ctk.CTkButton(
                self.userTable,
                text="Excluir",
                command=lambda u=user: self.deleteUser(u),
                width=80,
            )
            deleteButton.grid(row=row, column=2, sticky="e", padx=5, pady=2)

    def addNewUser(self):
        """Abre uma janela modal para adicionar um novo usuário."""
        # Janela modal
        self.addUserWindow = ctk.CTkToplevel(self)
        self.addUserWindow.title("Adicionar Usuário")
        centralizeWindowRelative(self, self.addUserWindow, 400, 300)
        self.addUserWindow.transient(self)
        self.addUserWindow.grab_set()

        # Título
        ctk.CTkLabel(self.addUserWindow, text="Novo Usuário", font=FONT_TITLE).pack(
            pady=10
        )

        # Entrada de Usuário
        ctk.CTkLabel(self.addUserWindow, text="Usuário:", font=FONT_NORMAL).pack()
        entryUser = ctk.CTkEntry(
            self.addUserWindow, placeholder_text="Digite o nome do usuário"
        )
        entryUser.pack(pady=5)

        # Entrada de Senha
        ctk.CTkLabel(self.addUserWindow, text="Senha:", font=FONT_NORMAL).pack()
        entryPassword = ctk.CTkEntry(
            self.addUserWindow, placeholder_text="Digite a senha", show="*"
        )
        entryPassword.pack(pady=5)

        # Role
        ctk.CTkLabel(self.addUserWindow, text="Permissão:", font=FONT_NORMAL).pack()
        comboRole = ctk.CTkComboBox(self.addUserWindow, values=["adm", "op"])
        comboRole.set("op")
        comboRole.pack(pady=5)

        # Botão Salvar
        ctk.CTkButton(
            self.addUserWindow,
            text="Salvar",
            command=lambda: self.saveNewUser(
                entryUser.get(), entryPassword.get(), comboRole.get()
            ),
        ).pack(pady=10)

    def saveNewUser(self, username, password, role):
        """Salva o novo usuário no banco de dados após validação."""
        # Validação de campos obrigatórios
        if not username.strip():
            messagebox.showerror("Erro", "O nome do usuário não pode estar vazio!")
            logError("Tentativa de adicionar usuário falhou: nome do usuário vazio.")
            return

        if not password.strip():
            messagebox.showerror("Erro", "A senha não pode estar vazia!")
            logError("Tentativa de adicionar usuário falhou: senha vazia.")
            return

        try:
            # Salva o novo usuário no banco
            addUser(username, password, role)
            logInfo(
                f"Novo usuário '{username}' adicionado com sucesso com papel '{role}'."
            )
            messagebox.showinfo(
                "Sucesso", f"Usuário '{username}' adicionado com sucesso!"
            )
            self.refreshTable()  # Atualiza a tabela
            self.addUserWindow.destroy()  # Fecha a janela modal
        except Exception as e:
            logError(f"Erro ao adicionar usuário '{username}': {e}")
            messagebox.showerror("Erro", f"Não foi possível adicionar o usuário: {e}")

    def editUser(self, user):
        """Abre uma janela modal para alterar a senha e o papel do usuário."""
        self.editUserWindow = ctk.CTkToplevel(self)
        self.editUserWindow.title(f"Editar Usuário - {user['user']}")
        centralizeWindowRelative(self, self.editUserWindow, 400, 300)
        self.editUserWindow.transient(self)
        self.editUserWindow.grab_set()

        # Título
        ctk.CTkLabel(
            self.editUserWindow,
            text=f"Editar Usuário '{user['user']}'",
            font=FONT_TITLE,
        ).pack(pady=10)

        # Nova Senha
        ctk.CTkLabel(self.editUserWindow, text="Nova Senha:", font=FONT_NORMAL).pack()
        entryPassword = ctk.CTkEntry(
            self.editUserWindow, placeholder_text="Digite a nova senha", show="*"
        )
        entryPassword.pack(pady=5)

        # Confirmação de Senha
        ctk.CTkLabel(
            self.editUserWindow, text="Confirme a Nova Senha:", font=FONT_NORMAL
        ).pack()
        entryConfirmPassword = ctk.CTkEntry(
            self.editUserWindow, placeholder_text="Confirme a nova senha", show="*"
        )
        entryConfirmPassword.pack(pady=5)

        # Alterar Role
        ctk.CTkLabel(self.editUserWindow, text="Permissão:", font=FONT_NORMAL).pack()
        comboRole = ctk.CTkComboBox(self.editUserWindow, values=["adm", "op"])
        comboRole.set(user["role"])
        comboRole.pack(pady=5)

        # Botão Salvar
        ctk.CTkButton(
            self.editUserWindow,
            text="Salvar",
            command=lambda: self.saveUserChanges(
                user["user"],
                entryPassword.get(),
                entryConfirmPassword.get(),
                comboRole.get(),
            ),
        ).pack(pady=10)

    def saveUserChanges(self, username, password, confirmPassword, role):
        """Salva as alterações feitas no usuário."""
        if password and password != confirmPassword:
            messagebox.showerror("Erro", "As senhas não coincidem!")
            logError(f"Erro ao editar usuário '{username}': senhas não coincidem.")
            return

        try:
            # Chama o banco de dados para atualizar
            updateUser(
                username, new_password=password if password else None, new_role=role
            )
            logInfo(
                f"Usuário '{username}' atualizado com sucesso: role='{role}', senha={'alterada' if password else 'não alterada'}."
            )
            messagebox.showinfo(
                "Sucesso", f"Usuário '{username}' atualizado com sucesso!"
            )
            self.refreshTable()  # Atualiza a tabela
            self.editUserWindow.destroy()  # Fecha a janela modal
        except Exception as e:
            logError(f"Erro ao atualizar usuário '{username}': {e}")
            messagebox.showerror("Erro", f"Não foi possível atualizar o usuário: {e}")

    def deleteUser(self, user):
        """Exclui um usuário após confirmação, exceto o logado."""
        # Obtém o nome do usuário logado (ajustar com a lógica correta do login)
        from utils.helpers import getCurrentUser

        currentUser = getCurrentUser()

        if user["user"] == currentUser:
            messagebox.showerror(
                "Erro", "Você não pode excluir o usuário atualmente logado!"
            )
            logError(f"Tentativa de exclusão do usuário logado: {currentUser}.")
            return

        confirm = messagebox.askyesno(
            "Confirmação", f"Tem certeza que deseja excluir o usuário '{user['user']}'?"
        )
        if confirm:
            try:
                deleteUser(
                    user["user"]
                )  # Chama a função do banco para excluir o usuário
                logInfo(f"Usuário '{user['user']}' excluído com sucesso.")
                messagebox.showinfo(
                    "Sucesso", f"Usuário '{user['user']}' foi excluído com sucesso."
                )
                self.refreshTable()  # Atualiza a tabela após exclusão
            except Exception as e:
                logError(f"Erro ao excluir usuário '{user['user']}': {e}")
                messagebox.showerror("Erro", f"Não foi possível excluir o usuário: {e}")
