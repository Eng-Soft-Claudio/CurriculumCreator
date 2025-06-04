# ----- IMPORTAÇÕES -----
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.units import inch
from reportlab.lib import colors
import os

# ----- CLASSE PRINCIPAL DA APLICAÇÃO -----
class ResumeBuilderApp:
    """
    Uma aplicação GUI para construir currículos otimizados para ATS.
    Permite ao usuário inserir informações pessoais, resumo, experiência,
    educação e habilidades, e então gerar um arquivo PDF.
    """

    def __init__(self, master):
        """
        Inicializa a aplicação ResumeBuilderApp.

        Args:
            master (tk.Tk): A janela raiz do Tkinter.
        """
        self.master = master
        master.title("Construtor de Currículo ATS-Friendly")
        master.geometry("800x700") 

        # Estilos para ReportLab
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()

        # Variáveis para armazenar os dados do currículo
        self.data = {
            "nome_completo": tk.StringVar(),
            "email": tk.StringVar(),
            "telefone": tk.StringVar(),
            "linkedin": tk.StringVar(), 
            "resumo": tk.StringVar(),
            "experiencias": [], 
            "educacao": [],   
            "habilidades": tk.StringVar() 
        }

        # Configuração da interface gráfica
        self._create_widgets()

    def setup_custom_styles(self):
        """Configura estilos personalizados para o PDF."""
        self.styles.add(ParagraphStyle(name='NomeCandidato',
                                        fontName='Helvetica-Bold',
                                        fontSize=18,
                                        leading=22,
                                        alignment=TA_CENTER,
                                        spaceAfter=6))
        self.styles.add(ParagraphStyle(name='ContatoInfo',
                                        fontName='Helvetica',
                                        fontSize=10,
                                        leading=12,
                                        alignment=TA_CENTER,
                                        spaceAfter=12))
        self.styles.add(ParagraphStyle(name='SecaoTitulo',
                                        fontName='Helvetica-Bold',
                                        fontSize=14,
                                        leading=18,
                                        spaceBefore=12,
                                        spaceAfter=6))
        self.styles.add(ParagraphStyle(name='SubTitulo',
                                        fontName='Helvetica-Bold',
                                        fontSize=11,
                                        leading=14,
                                        spaceAfter=2))
        self.styles.add(ParagraphStyle(name='Detalhes', 
                                        fontName='Helvetica-Oblique',
                                        fontSize=10,
                                        leading=12,
                                        spaceAfter=2))
        self.styles.add(ParagraphStyle(name='CorpoTexto',
                                        fontName='Helvetica',
                                        fontSize=10,
                                        leading=12,
                                        bulletIndent=18, 
                                        leftIndent=18, 
                                        spaceAfter=6))
        self.styles.add(ParagraphStyle(name='BulletPoints',
                                    parent=self.styles['CorpoTexto'],
                                    bulletIndent=20,
                                    leftIndent=20,
                                    spaceBefore=0,
                                    spaceAfter=2))

    # ----- CRIAÇÃO DE WIDGETS DA UI -----
    def _create_widgets(self):
        """Cria e organiza os widgets na interface gráfica."""
        main_frame = ttk.Frame(self.master, padding="10")
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Notebook para seções
        notebook = ttk.Notebook(main_frame)
        notebook.pack(expand=True, fill=tk.BOTH, pady=10)

        # Abas
        self.personal_info_container, self.personal_info_frame = self._create_scrollable_frame(notebook, "Informações Pessoais")
        self.summary_container, self.summary_frame = self._create_scrollable_frame(notebook, "Resumo")
        self.experience_container, self.experience_frame = self._create_scrollable_frame(notebook, "Experiência")
        self.education_container, self.education_frame = self._create_scrollable_frame(notebook, "Educação")
        self.skills_container, self.skills_frame = self._create_scrollable_frame(notebook, "Habilidades")

        notebook.add(self.personal_info_container, text="Informações Pessoais")
        notebook.add(self.summary_container, text="Resumo")
        notebook.add(self.experience_container, text="Experiência")
        notebook.add(self.education_container, text="Educação")
        notebook.add(self.skills_container, text="Habilidades")

        self._populate_personal_info_frame()
        self._populate_summary_frame()
        self._populate_experience_frame() 
        self._populate_education_frame()  
        self._populate_skills_frame()

        # Botão Gerar PDF
        generate_button = ttk.Button(main_frame, text="Gerar PDF", command=self._generate_pdf)
        generate_button.pack(pady=20)

    def _create_scrollable_frame(self, parent, title):
        """Cria um frame com scrollbar dentro de um container (como um Notebook)."""
        # Frame container para o canvas e scrollbar
        container = ttk.Frame(parent)
        container.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        return container, scrollable_frame

    # ----- SEÇÃO: INFORMAÇÕES PESSOAIS -----
    def _populate_personal_info_frame(self):
        """Popula o frame de informações pessoais com campos de entrada."""
        frame = self.personal_info_frame
        ttk.Label(frame, text="Nome Completo:", font=('Arial', 11)).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(frame, textvariable=self.data["nome_completo"], width=50).grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        ttk.Label(frame, text="Email:", font=('Arial', 11)).grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(frame, textvariable=self.data["email"], width=50).grid(row=1, column=1, padx=5, pady=5, sticky=tk.EW)

        ttk.Label(frame, text="Telefone:", font=('Arial', 11)).grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(frame, textvariable=self.data["telefone"], width=50).grid(row=2, column=1, padx=5, pady=5, sticky=tk.EW)

        ttk.Label(frame, text="LinkedIn (URL completa, opcional):", font=('Arial', 11)).grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(frame, textvariable=self.data["linkedin"], width=50).grid(row=3, column=1, padx=5, pady=5, sticky=tk.EW)
        
        frame.columnconfigure(1, weight=1) 

    # ----- SEÇÃO: RESUMO -----
    def _populate_summary_frame(self):
        """Popula o frame de resumo com um campo de texto."""
        frame = self.summary_frame
        ttk.Label(frame, text="Resumo Profissional / Objetivo:", font=('Arial', 11)).pack(padx=5, pady=5, anchor=tk.W)
        self.summary_text = tk.Text(frame, height=8, width=70, wrap=tk.WORD, font=('Arial', 10))
        self.summary_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

    # ----- SEÇÃO: EXPERIÊNCIA PROFISSIONAL -----
    def _populate_experience_frame(self):
        """Popula o frame de experiência profissional."""
        self.experience_entries_frame = ttk.Frame(self.experience_frame)
        self.experience_entries_frame.pack(fill=tk.X)
        self._add_experience_entry() 

        add_button = ttk.Button(self.experience_frame, text="Adicionar Outra Experiência", command=self._add_experience_entry)
        add_button.pack(pady=10)

    def _remove_experience_entry(self, entry_data):
        """Remove uma entrada de experiência da interface e dos dados."""
        entry_data["frame"].destroy()
        self.data["experiencias"].remove(entry_data)

    def _add_experience_entry(self, is_first=False):
        """Adiciona um novo conjunto de campos para uma experiência profissional."""
        entry_frame = ttk.Labelframe(self.experience_entries_frame, text=f"Experiência #{len(self.data['experiencias']) + 1}", padding="10")
        entry_frame.pack(fill=tk.X, padx=5, pady=5)

        entry_data = {
            "cargo": tk.StringVar(),
            "empresa": tk.StringVar(),
            "local": tk.StringVar(), 
            "data_inicio": tk.StringVar(),
            "data_fim": tk.StringVar(), 
            "descricao": None,
            "frame": entry_frame
        }

        ttk.Label(entry_frame, text="Cargo:").grid(row=0, column=0, sticky=tk.W, padx=2, pady=2)
        ttk.Entry(entry_frame, textvariable=entry_data["cargo"], width=40).grid(row=0, column=1, sticky=tk.EW, padx=2, pady=2)

        ttk.Label(entry_frame, text="Empresa:").grid(row=1, column=0, sticky=tk.W, padx=2, pady=2)
        ttk.Entry(entry_frame, textvariable=entry_data["empresa"], width=40).grid(row=1, column=1, sticky=tk.EW, padx=2, pady=2)

        ttk.Label(entry_frame, text="Local (Cidade, Estado):").grid(row=2, column=0, sticky=tk.W, padx=2, pady=2)
        ttk.Entry(entry_frame, textvariable=entry_data["local"], width=40).grid(row=2, column=1, sticky=tk.EW, padx=2, pady=2)

        ttk.Label(entry_frame, text="Data Início (Mês/Ano):").grid(row=3, column=0, sticky=tk.W, padx=2, pady=2)
        ttk.Entry(entry_frame, textvariable=entry_data["data_inicio"], width=15).grid(row=3, column=1, sticky=tk.W, padx=2, pady=2)

        ttk.Label(entry_frame, text="Data Fim (Mês/Ano ou 'Atual'):").grid(row=4, column=0, sticky=tk.W, padx=2, pady=2)
        ttk.Entry(entry_frame, textvariable=entry_data["data_fim"], width=15).grid(row=4, column=1, sticky=tk.W, padx=2, pady=2)
        
        ttk.Label(entry_frame, text="Descrição (use '-' para bullet points):").grid(row=5, column=0, sticky=tk.NW, padx=2, pady=2)
        desc_text = tk.Text(entry_frame, height=6, width=50, wrap=tk.WORD, font=('Arial', 10))
        desc_text.grid(row=5, column=1, sticky=tk.EW, padx=2, pady=2)
        entry_data["descricao"] = desc_text 

        delete_button = ttk.Button(entry_frame, text="Excluir", command=lambda: self._remove_experience_entry(entry_data))
        delete_button.grid(row=6, column=1, sticky=tk.E, padx=2, pady=5)

        entry_frame.columnconfigure(1, weight=1)
        self.data["experiencias"].append(entry_data)

    # ----- SEÇÃO: EDUCAÇÃO -----
    def _populate_education_frame(self):
        """Popula o frame de educação."""
        self.education_entries_frame = ttk.Frame(self.education_container)
        self.education_entries_frame.pack(fill=tk.X)
        self._add_education_entry() 

        add_button = ttk.Button(self.education_container, text="Adicionar Outra Formação", command=self._add_education_entry)
        add_button.pack(pady=10)

    def _remove_education_entry(self, entry_data):
        """Remove uma entrada de educação da interface e dos dados."""
        entry_data["frame"].destroy()
        self.data["educacao"].remove(entry_data)
        
    def _add_education_entry(self):
        """Adiciona um novo conjunto de campos para uma formação educacional."""
        entry_frame = ttk.Labelframe(self.education_entries_frame, text=f"Formação #{len(self.data['educacao']) + 1}", padding="10")
        entry_frame.pack(fill=tk.X, padx=5, pady=5)

        entry_data = {
            "curso": tk.StringVar(),
            "instituicao": tk.StringVar(),
            "local_edu": tk.StringVar(), 
            "data_conclusao": tk.StringVar(),
            "detalhes_edu": None,
            "frame": entry_frame
        }

        ttk.Label(entry_frame, text="Curso/Grau:").grid(row=0, column=0, sticky=tk.W, padx=2, pady=2)
        ttk.Entry(entry_frame, textvariable=entry_data["curso"], width=40).grid(row=0, column=1, sticky=tk.EW, padx=2, pady=2)

        ttk.Label(entry_frame, text="Instituição:").grid(row=1, column=0, sticky=tk.W, padx=2, pady=2)
        ttk.Entry(entry_frame, textvariable=entry_data["instituicao"], width=40).grid(row=1, column=1, sticky=tk.EW, padx=2, pady=2)
        
        ttk.Label(entry_frame, text="Local (Cidade, Estado):").grid(row=2, column=0, sticky=tk.W, padx=2, pady=2)
        ttk.Entry(entry_frame, textvariable=entry_data["local_edu"], width=40).grid(row=2, column=1, sticky=tk.EW, padx=2, pady=2)

        ttk.Label(entry_frame, text="Data de Conclusão (Mês/Ano):").grid(row=3, column=0, sticky=tk.W, padx=2, pady=2)
        ttk.Entry(entry_frame, textvariable=entry_data["data_conclusao"], width=15).grid(row=3, column=1, sticky=tk.W, padx=2, pady=2)

        ttk.Label(entry_frame, text="Detalhes (Honras, GPA, etc. Opcional):").grid(row=4, column=0, sticky=tk.NW, padx=2, pady=2)
        det_text = tk.Text(entry_frame, height=3, width=50, wrap=tk.WORD, font=('Arial', 10))
        det_text.grid(row=4, column=1, sticky=tk.EW, padx=2, pady=2)
        entry_data["detalhes_edu"] = det_text

        delete_button = ttk.Button(entry_frame, text="Excluir", command=lambda: self._remove_education_entry(entry_data))
        delete_button.grid(row=5, column=1, sticky=tk.E, padx=2, pady=5)

        entry_frame.columnconfigure(1, weight=1)
        self.data["educacao"].append(entry_data)

    # ----- SEÇÃO: HABILIDADES -----
    def _populate_skills_frame(self):
        """Popula o frame de habilidades com um campo de texto."""
        frame = self.skills_frame
        ttk.Label(frame, text="Habilidades (separadas por vírgula):", font=('Arial', 11)).pack(padx=5, pady=5, anchor=tk.W)
        self.skills_text = tk.Text(frame, height=5, width=70, wrap=tk.WORD, font=('Arial', 10))
        self.skills_text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

    # ----- LÓGICA DE GERAÇÃO DO PDF -----
    def _get_data_from_ui(self):
        """Coleta os dados dos widgets da UI e armazena em self.data."""

        # Resumo
        self.data["resumo"] = self.summary_text.get("1.0", tk.END).strip()

        for i, exp_entry_ui in enumerate(self.data["experiencias"]):
            exp_entry_ui["descricao_text"] = exp_entry_ui["descricao"].get("1.0", tk.END).strip()


        # Educação 
        for i, edu_entry_ui in enumerate(self.data["educacao"]):
            edu_entry_ui["detalhes_edu_text"] = edu_entry_ui["detalhes_edu"].get("1.0", tk.END).strip()

        # Habilidades
        self.data["habilidades"] = self.skills_text.get("1.0", tk.END).strip()

    def _generate_pdf(self):
        """Gera o currículo em formato PDF."""
        self._get_data_from_ui() 

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Salvar Currículo Como..."
        )
        if not file_path:
            return 

        try:
            doc = SimpleDocTemplate(file_path, pagesize=letter,
                                    rightMargin=0.75*inch, leftMargin=0.75*inch,
                                    topMargin=0.75*inch, bottomMargin=0.75*inch)
            story = []

            # --- Nome e Contato ---
            if self.data["nome_completo"].get():
                story.append(Paragraph(self.data["nome_completo"].get().upper(), self.styles['NomeCandidato']))
            
            contact_info = []
            if self.data["email"].get(): contact_info.append(self.data["email"].get())
            if self.data["telefone"].get(): contact_info.append(self.data["telefone"].get())
            if self.data["linkedin"].get(): contact_info.append(self.data["linkedin"].get())
            if contact_info:
                story.append(Paragraph(" | ".join(contact_info), self.styles['ContatoInfo']))
            story.append(Spacer(1, 0.1*inch))

            # --- Resumo ---
            if self.data["resumo"]:
                story.append(Paragraph("RESUMO PROFISSIONAL", self.styles['SecaoTitulo']))
                story.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey, spaceBefore=1, spaceAfter=1, hAlign='LEFT', vAlign='BOTTOM', lineCap='round'))
                story.append(Paragraph(self.data["resumo"], self.styles['CorpoTexto']))
                story.append(Spacer(1, 0.1*inch))

            # --- Experiência ---
            if any(exp["cargo"].get() or exp["empresa"].get() for exp in self.data["experiencias"]):
                story.append(Paragraph("EXPERIÊNCIA PROFISSIONAL", self.styles['SecaoTitulo']))
                story.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey, spaceBefore=1, spaceAfter=1))
                for exp in self.data["experiencias"]:
                    if not (exp["cargo"].get() or exp["empresa"].get()): continue 

                    story.append(Paragraph(exp["cargo"].get().upper(), self.styles['SubTitulo']))
                    
                    empresa_local_data = []
                    if exp["empresa"].get(): empresa_local_data.append(exp["empresa"].get())
                    if exp["local"].get(): empresa_local_data.append(exp["local"].get())
                    if exp["data_inicio"].get() or exp["data_fim"].get():
                        datas = f"{exp['data_inicio'].get()} - {exp['data_fim'].get()}"
                        empresa_local_data.append(datas)
                    
                    if empresa_local_data:
                        story.append(Paragraph(" | ".join(empresa_local_data), self.styles['Detalhes']))

                    # Descrição com bullet points
                    desc_text = exp["descricao_text"]
                    if desc_text:
                        responsibilities = desc_text.split('\n')
                        for resp in responsibilities:
                            resp = resp.strip()
                            if resp.startswith("-"):
                                resp = resp[1:].strip()
                                story.append(Paragraph(resp, self.styles['BulletPoints'], bulletText='•'))
                            elif resp: 
                                story.append(Paragraph(resp, self.styles['CorpoTexto']))
                    story.append(Spacer(1, 0.1*inch))

            # --- Educação ---
            if any(edu["curso"].get() or edu["instituicao"].get() for edu in self.data["educacao"]):
                story.append(Paragraph("FORMAÇÃO ACADÊMICA", self.styles['SecaoTitulo']))
                story.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey, spaceBefore=1, spaceAfter=1))
                for edu in self.data["educacao"]:
                    if not (edu["curso"].get() or edu["instituicao"].get()): continue

                    story.append(Paragraph(edu["curso"].get().upper(), self.styles['SubTitulo']))
                    
                    instituicao_local_data = []
                    if edu["instituicao"].get(): instituicao_local_data.append(edu["instituicao"].get())
                    if edu["local_edu"].get(): instituicao_local_data.append(edu["local_edu"].get())
                    if edu["data_conclusao"].get(): instituicao_local_data.append(edu["data_conclusao"].get())
                    
                    if instituicao_local_data:
                        story.append(Paragraph(" | ".join(instituicao_local_data), self.styles['Detalhes']))
                    
                    detalhes_edu_text = edu["detalhes_edu_text"]
                    if detalhes_edu_text:
                        story.append(Paragraph(detalhes_edu_text, self.styles['CorpoTexto']))
                    story.append(Spacer(1, 0.1*inch))

            # --- Habilidades ---
            if self.data["habilidades"]:
                story.append(Paragraph("HABILIDADES", self.styles['SecaoTitulo']))
                story.append(HRFlowable(width="100%", thickness=0.5, color=colors.grey, spaceBefore=1, spaceAfter=1))
                habilidades_list = [s.strip() for s in self.data["habilidades"].replace(',', '\n').split('\n') if s.strip()]
                if habilidades_list:
                    for habilidade in habilidades_list:
                         story.append(Paragraph(habilidade, self.styles['BulletPoints'], bulletText='•'))
                story.append(Spacer(1, 0.1*inch))

            doc.build(story)
            messagebox.showinfo("Sucesso", f"Currículo salvo em:\n{file_path}")

        except Exception as e:
            messagebox.showerror("Erro ao Gerar PDF", f"Ocorreu um erro: {e}\nVerifique os dados e tente novamente.")
            print(f"Erro detalhado: {e}") 

# ----- INICIALIZAÇÃO DA APLICAÇÃO -----
if __name__ == "__main__":
    root = tk.Tk()
    app = ResumeBuilderApp(root)
    root.mainloop()