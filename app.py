import tkinter as tk
from tkinter import ttk, messagebox
import logging
from dolphin_automator import DolphinAutomator

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Interface de Automação")
        self.dolphin_automator = DolphinAutomator()
        self.setup_ui()

    def setup_ui(self):
        # Frame para a lista de perfis
        self.frame_profiles = ttk.Frame(self.root)
        self.frame_profiles.pack(padx=10, pady=10)

        self.label = ttk.Label(self.frame_profiles, text="Selecione os perfis para automatizar:")
        self.label.pack()

        # Lista de perfis
        self.profile_listbox = tk.Listbox(self.frame_profiles, height=10, width=50, selectmode=tk.MULTIPLE)
        self.profile_listbox.pack()

        self.start_button = ttk.Button(self.frame_profiles, text="Iniciar Automação", command=self.start_automation)
        self.start_button.pack(pady=10)

        # Carregar perfis
        self.load_profiles()

    def load_profiles(self):
        try:
            profiles = self.dolphin_automator.get_profiles()
            if profiles:
                self.profile_listbox.delete(0, tk.END)  # Limpa a lista antes de carregar novos perfis
                for profile in profiles:
                    profile_id = profile['id']
                    profile_name = profile['name']
                    self.profile_listbox.insert(tk.END, (profile_id, profile_name))
            else:
                self.profile_listbox.insert(tk.END, "Nenhum perfil encontrado.")
        except RuntimeError as e:
            messagebox.showerror("Erro", str(e))

    def start_automation(self):
        selected = self.profile_listbox.curselection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione pelo menos um perfil para iniciar a automação.")
            return

        # Desabilita o botão para evitar múltiplos cliques
        self.start_button.config(state=tk.DISABLED)
        self.root.update()  # Atualiza a interface para refletir a desativação do botão
        
        try:
            for index in selected:
                profile_id, profile_name = self.profile_listbox.get(index)
                logging.info(f"Iniciando automação do perfil {profile_name} ({profile_id})")
                self.dolphin_automator.automate_profile(profile_id, profile_name)
                # Removido: messagebox.showinfo("Concluído", f"Automação do perfil {profile_name} concluída com sucesso.")
        except Exception as e:
            logging.error(f"Erro ao automatizar os perfis: {e}")
            messagebox.showerror("Erro", f"Erro ao automatizar os perfis: {e}")
        finally:
            # Reabilita o botão após a automação
            self.start_button.config(state=tk.NORMAL)