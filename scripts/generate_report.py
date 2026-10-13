"""Gera o relatório factual do CP05. Não cria capturas ou resultados simulados."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable, KeepTogether, PageBreak, Paragraph, Preformatted,
    SimpleDocTemplate, Spacer, Table, TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "CP05_DevSecOps_Relatorio.pdf"
PINK = colors.HexColor("#E91860")
DARK = colors.HexColor("#161821")
GRAY = colors.HexColor("#5B6170")
LIGHT = colors.HexColor("#F4F5F8")
LINE = colors.HexColor("#DCE0E7")

font_dir = Path("C:/Windows/Fonts")
pdfmetrics.registerFont(TTFont("ArialCP", str(font_dir / "arial.ttf")))
pdfmetrics.registerFont(TTFont("ArialCP-Bold", str(font_dir / "arialbd.ttf")))
pdfmetrics.registerFontFamily("ArialCP", normal="ArialCP", bold="ArialCP-Bold")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="ReportTitle", fontName="ArialCP-Bold", fontSize=31, leading=37, textColor=DARK, spaceAfter=15))
styles.add(ParagraphStyle(name="SectionTitleCP", fontName="ArialCP-Bold", fontSize=18, leading=23, textColor=DARK, spaceBefore=12, spaceAfter=13))
styles.add(ParagraphStyle(name="SubTitleCP", fontName="ArialCP-Bold", fontSize=10.5, leading=15, textColor=DARK, spaceBefore=12, spaceAfter=6))
styles.add(ParagraphStyle(name="BodyCP", fontName="ArialCP", fontSize=9.4, leading=15, textColor=DARK, spaceAfter=10))
styles.add(ParagraphStyle(name="SmallCP", fontName="ArialCP", fontSize=8.4, leading=12.5, textColor=GRAY, spaceAfter=7))
styles.add(ParagraphStyle(name="LabelCP", fontName="ArialCP-Bold", fontSize=8, leading=11, textColor=PINK, spaceAfter=8))
styles.add(ParagraphStyle(name="WhiteTitleCP", fontName="ArialCP-Bold", fontSize=33, leading=40, textColor=colors.white))
styles.add(ParagraphStyle(name="WhiteBodyCP", fontName="ArialCP", fontSize=12, leading=19, textColor=colors.white))
styles.add(ParagraphStyle(name="CellCP", fontName="ArialCP", fontSize=8, leading=12, textColor=DARK))
styles.add(ParagraphStyle(name="CellBoldCP", fontName="ArialCP-Bold", fontSize=8, leading=12, textColor=DARK))
styles.add(ParagraphStyle(name="CodeCP", fontName="Courier", fontSize=8.2, leading=12, textColor=DARK))


def p(text, style="BodyCP"):
    return Paragraph(text, styles[style])


def tag(text):
    return p(text.upper(), "LabelCP")


def box(title, body, bg=LIGHT):
    data = [[p(title, "SubTitleCP")], [p(body, "SmallCP")]]
    table = Table(data, colWidths=[166 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), .5, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 10),
    ]))
    return table


def page_header(canvas, doc):
    canvas.saveState()
    w, h = A4
    if doc.page == 1:
        canvas.setFillColor(DARK)
        canvas.rect(0, 0, w, h, fill=1, stroke=0)
        canvas.setFillColor(PINK)
        canvas.rect(0, h - 17 * mm, w, 17 * mm, fill=1, stroke=0)
        canvas.setFont("ArialCP-Bold", 11)
        canvas.setFillColor(colors.white)
        canvas.drawString(22 * mm, h - 11 * mm, "FIAP / CHECKPOINT 05")
        canvas.setStrokeColor(PINK)
        canvas.setLineWidth(3)
        canvas.line(22 * mm, 62 * mm, 188 * mm, 62 * mm)
    else:
        canvas.setStrokeColor(LINE)
        canvas.line(22 * mm, h - 17 * mm, 188 * mm, h - 17 * mm)
        canvas.setFont("ArialCP-Bold", 8)
        canvas.setFillColor(PINK)
        canvas.drawString(22 * mm, h - 13 * mm, "FIAP  /  CP05")
        canvas.setFont("ArialCP", 8)
        canvas.setFillColor(GRAY)
        canvas.drawRightString(188 * mm, h - 13 * mm, "PIPELINE DEVSECOPS COMPLETO")
        canvas.line(22 * mm, 18 * mm, 188 * mm, 18 * mm)
        canvas.drawString(22 * mm, 12 * mm, "Engenharia de Software · DevSecOps and Cloud Computing")
        canvas.drawRightString(188 * mm, 12 * mm, f"{doc.page:02d}")
    canvas.restoreState()


doc = SimpleDocTemplate(
    str(OUTPUT), pagesize=A4, rightMargin=22 * mm, leftMargin=22 * mm,
    topMargin=24 * mm, bottomMargin=25 * mm,
    title="FIAP - CP05: Pipeline DevSecOps Completo", author="Enzo Sartorelli",
)
story = []

# Capa
story += [Spacer(1, 50 * mm), tag("Engenharia de Software / DevSecOps and Cloud Computing"),
          p("O Pipeline<br/>DevSecOps<br/>Completo", "WhiteTitleCP"), Spacer(1, 11 * mm),
          p("Gitleaks · Semgrep · Trivy", "WhiteBodyCP"), Spacer(1, 46 * mm),
          p("Checkpoint 05  |  13 de outubro de 2026", "WhiteBodyCP"),
          p("Aluno: Enzo Sartorelli  |  RM: ____________________", "WhiteBodyCP"),
          PageBreak()]

# Introdução e arquitetura
story += [tag("01 / Visão geral"), p("Introdução", "SectionTitleCP"),
          p("Este checkpoint integra verificações automáticas de segurança ao fluxo de integração contínua. Cada push e pull request aciona uma análise de segredos, uma análise estática de JavaScript e uma análise de vulnerabilidades da imagem Docker. Detectar problemas cedo reduz o risco de publicar credenciais, executar código não confiável e distribuir componentes vulneráveis."),
          p("Arquitetura do pipeline", "SectionTitleCP"),
          p("O arquivo <b>.github/workflows/security.yml</b> define três jobs independentes. O Gitleaks lê o histórico da branch após checkout completo; o Semgrep inspeciona o código-fonte com uma regra local; o Trivy constrói a imagem do Dockerfile e consulta bases de CVEs. Jobs independentes permitem ver qual barreira falhou sem confundir o tipo de problema."),
          box("push / pull request  →  gitleaks + semgrep + trivy", "Política: Gitleaks bloqueia segredos; Semgrep bloqueia eval; Trivy exibe todas as severidades e bloqueia CRITICAL."),
          Spacer(1, 8 * mm),
          p("Aplicação analisada", "SubTitleCP"),
          p("O repositório começou vazio. Foi criada uma aplicação HTML/CSS/JavaScript sem dependências de produção, servida por Nginx sem privilégios na porta interna 8080. O painel apresenta as três barreiras e uma lista local de estudo salva no navegador. O progresso da interface não representa o estado dos jobs."),
          p("Estado de validação", "SubTitleCP"),
          p("A aplicação respondeu por HTTP local e o JavaScript passou na verificação de sintaxe. O workflow YAML foi interpretado com os gatilhos e três jobs esperados. O ambiente não dispõe de Docker nem de remoto GitHub configurado; por isso o build, a execução do workflow no GitHub e as capturas exigidas seguem pendentes."),
          PageBreak()]

# Gitleaks
story += [tag("02 / Primeira barreira"), p("Gitleaks: segredos no histórico", "SectionTitleCP"),
          p("O Gitleaks procura credenciais expostas em commits. O job instala a versão 8.30.0, usa <b>fetch-depth: 0</b>, estende as regras padrão e acrescenta uma regra local que identifica apenas o formato fictício do teste. A execução usa saída 1 em caso de achado e redige o valor do segredo no log."),
          p("Sabotagem isolada", "SubTitleCP"),
          p("A branch <b>prova/gitleaks</b> recebeu um commit com um token inteiramente fictício no arquivo de teste. A análise local percorreu dois commits, encontrou um achado com <b>RuleID fiap-cp05-fake-token</b> e terminou com <b>código 1</b>. A branch main não contém o arquivo de sabotagem. O log autêntico está em <b>evidencias/gitleaks-local.txt</b>."),
          box("Resultado local confirmado", "1 achado · RuleID fiap-cp05-fake-token · saída 1 · commit c68a4d5. Trata-se de falha esperada de segurança, não de erro de configuração."),
          Spacer(1, 9 * mm),
          box("Captura do GitHub Actions: PENDENTE", "Não há execução remota confirmada. A captura 01-gitleaks.png deve ser obtida do job gitleaks após publicar a branch isolada. Nenhum print foi fabricado."),
          Spacer(1, 9 * mm),
          p("Por que importa", "SubTitleCP"),
          p("Segredos em commits podem continuar acessíveis mesmo após a remoção do arquivo em uma revisão posterior. A resposta a um segredo real seria revogá-lo ou rotacioná-lo e avaliar o histórico afetado. Este teste usa exclusivamente um valor fictício."),
          PageBreak()]

# Semgrep
story += [tag("03 / Segunda barreira"), p("Semgrep: análise estática", "SectionTitleCP"),
          p("O Semgrep 1.140.0 examina os arquivos JavaScript do repositório. A regra local <b>fiap-cp05-no-eval</b>, criada especificamente para a demonstração, identifica chamadas <b>eval(...)</b>. A opção <b>--error</b> faz um achado resultar em falha do job."),
          p("Exemplo inserido somente na branch prova/semgrep", "SubTitleCP"),
          Preformatted("function exemploInseguro(entrada) { return eval(entrada); }", styles["CodeCP"]),
          Spacer(1, 5 * mm),
          p("A função acima não é chamada na demonstração. A análise local apontou <b>1 finding</b> na linha 52 de app.js com a regra <b>semgrep.fiap-cp05-no-eval</b> e terminou com <b>código 1</b>. Na branch main, a mesma varredura terminou com zero achados e código 0. O log autêntico está em <b>evidencias/semgrep-local.txt</b>."),
          box("Resultado local confirmado", "1 achado bloqueante na branch de prova · saída 1 · commit 0225a55. O código vulnerável não foi incorporado à main."),
          Spacer(1, 9 * mm),
          box("Captura do GitHub Actions: PENDENTE", "A captura 02-semgrep.png precisa mostrar a falha real do job semgrep depois que a branch de prova for publicada."),
          Spacer(1, 9 * mm),
          p("Risco de eval", "SubTitleCP"),
          p("eval interpreta texto como código JavaScript. Quando a entrada pode ser influenciada por terceiros, a execução pode alterar o comportamento esperado da aplicação e permitir acesso indevido a dados ou funções do contexto."),
          PageBreak()]

# Trivy
story += [tag("04 / Terceira barreira"), p("Trivy: vulnerabilidades da imagem", "SectionTitleCP"),
          p("O job trivy constrói <b>fiap-cp05:${{ github.sha }}</b> a partir do Dockerfile do repositório. Depois gera um JSON como artefato, mostra uma tabela com todas as severidades nos logs e executa a política final que retorna código 1 somente se houver vulnerabilidades <b>CRITICAL</b>. Nenhuma vulnerabilidade é ignorada para limpar artificialmente o relatório."),
          p("Observação local da imagem-base", "SubTitleCP"),
          p("Como não havia Docker disponível, o Trivy 0.75.0 analisou diretamente a imagem-base remota <b>nginxinc/nginx-unprivileged:stable-alpine</b> em 13/10/2026. O digest observado foi <b>sha256:56b8272e43a0525f67aed68d1e0794a712d10e3e45a563e118e9a77c817e6f86</b>. Esse teste <b>não valida a imagem do projeto</b>, que ainda precisa ser construída."),
          box("Achado real da imagem-base", "CVE-2026-85091 · MEDIUM · zlib 1.3.2-r0 · correção indicada: 1.3.2-r1. Nenhuma CRITICAL foi encontrada nessa imagem-base; a verificação local com --severity CRITICAL --exit-code 1 retornou 0."),
          Spacer(1, 7 * mm),
          p("Interpretação", "SubTitleCP"),
          p("CVE é um identificador público de vulnerabilidade. A severidade MEDIUM indica risco abaixo do limite de bloqueio definido para o CP05, mas ainda deve ser acompanhada e corrigida quando uma atualização segura estiver disponível. A tag da imagem-base pode mudar; uma execução posterior pode apresentar outros resultados. O log local consta em <b>evidencias/trivy-base-local.txt</b>."),
          box("Captura e resultado da imagem construída: PENDENTES", "A captura 03-trivy.png, os CVEs da imagem do projeto e a confirmação do status do job dependem de build Docker e execução do GitHub Actions."),
          PageBreak()]

# Conclusão e repositório
story += [tag("05 / Encerramento"), p("Conclusão", "SectionTitleCP"),
          p("As três ferramentas protegem etapas diferentes: Gitleaks examina exposição de credenciais no histórico; Semgrep identifica um padrão de código inseguro; Trivy relaciona pacotes da imagem a CVEs. As sabotagens locais confirmaram o bloqueio do Gitleaks e do Semgrep. A varredura local do Trivy confirmou seu funcionamento contra a imagem-base, com um achado MEDIUM; a validação da imagem construída permanece pendente."),
          p("Repositório e execuções", "SectionTitleCP"),
          box("URL do GitHub: PENDENTE", "O diretório local ainda não possui remoto. Não há links de runs para registrar. Após a publicação, incluir aqui a URL do repositório e as URLs das três execuções usadas como evidência."),
          Spacer(1, 8 * mm),
          p("Pendências para a entrega integral", "SubTitleCP"),
          p("1. Construir e executar a imagem Docker do projeto.<br/>2. Publicar main e as duas branches de prova sem mesclá-las.<br/>3. Confirmar os três jobs no GitHub Actions, incluindo CVEs e política do Trivy.<br/>4. Capturar 01-gitleaks.png, 02-semgrep.png e 03-trivy.png a partir de runs reais.<br/>5. Acrescentar URLs, resultados remotos e imagens autênticas a este relatório."),
          Spacer(1, 8 * mm),
          HRFlowable(color=LINE, width="100%"), Spacer(1, 6 * mm),
          p("Fontes técnicas", "SubTitleCP"),
          p("Gitleaks: github.com/gitleaks/gitleaks<br/>Semgrep CLI: semgrep.dev/docs/cli-reference<br/>Trivy Action: github.com/aquasecurity/trivy-action<br/>Nginx sem privilégios: github.com/nginx/docker-nginx-unprivileged", "SmallCP")]

doc.build(story, onFirstPage=page_header, onLaterPages=page_header)
print(OUTPUT)
