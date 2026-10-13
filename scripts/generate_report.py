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
    HRFlowable, Image, KeepTogether, PageBreak, Paragraph, Preformatted,
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
styles.add(ParagraphStyle(name="WhiteTeamCP", fontName="ArialCP", fontSize=10.5, leading=16, textColor=colors.white))
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


def screenshot(name):
    path = ROOT / "evidencias" / name
    image = Image(str(path), width=166 * mm, height=121 * mm)
    image.hAlign = "CENTER"
    return image


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
    title="FIAP - CP05: Pipeline DevSecOps Completo", author="Enzo Vazquez Sartorelli, Guilherme Brazioli, Pedro Oliveira Valotto, Nicolas Nogueira Boni, Kaue Pastori Teixeira",
)
story = []

# Capa
story += [Spacer(1, 50 * mm), tag("Engenharia de Software / DevSecOps and Cloud Computing"),
          p("FIAP - CP05<br/>Pipeline DevSecOps<br/>Completo", "WhiteTitleCP"), Spacer(1, 11 * mm),
          p("Gitleaks · Semgrep · Trivy", "WhiteBodyCP"), Spacer(1, 29 * mm),
          p("Checkpoint 05  |  13 de outubro de 2026", "WhiteBodyCP"),
          p("Equipe — cinco integrantes", "WhiteBodyCP"),
          p("Enzo Vazquez Sartorelli — RM94818<br/>"
            "Guilherme Brazioli — RM98237<br/>"
            "Pedro Oliveira Valotto — RM551445<br/>"
            "Nicolas Nogueira Boni — RM551965<br/>"
            "Kaue Pastori Teixeira — RM98501", "WhiteTeamCP"),
          p("Repositório: <link href='https://github.com/efsartorelli/CP05-DEVOPS' color='#FFFFFF'>github.com/efsartorelli/CP05-DEVOPS</link>", "WhiteBodyCP"),
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
          p("A aplicação respondeu por HTTP local, o JavaScript passou na verificação de sintaxe e o YAML passou no actionlint. No run 38462913681 da main, os três jobs passaram; a imagem foi construída e o contêiner respondeu HTTP 200. Os runs isolados falharam respectivamente no Gitleaks e no Semgrep. Um PR de teste também acionou os três jobs e foi fechado sem merge."),
          PageBreak()]

# Gitleaks
story += [tag("02 / Primeira barreira"), p("Gitleaks: segredos no histórico", "SectionTitleCP"),
          p("O Gitleaks 8.30.0 procura credenciais em commits. O job usa <b>fetch-depth: 0</b>, estende as regras padrão e acrescenta uma assinatura para o token fictício da prova. A branch <b>prova/gitleaks</b> contém o commit isolado c68a4d5, sem merge na main."),
          p("No run 38461907382, o job Gitleaks falhou em 13/10/2026 às 20:19 UTC. O log autêntico mostra <b>RuleID fiap-cp05-fake-token</b>, <b>leaks found: 1</b> e <b>exit code 1</b>. O valor foi redigido. Isso confirma uma falha esperada de segurança. Segredos reais expostos exigiriam revogação ou rotação, mesmo após remover o arquivo em novo commit."),
          screenshot("01-gitleaks.png"),
          box("Trecho do log do GitHub Actions", "RuleID: fiap-cp05-fake-token  |  leaks found: 1  |  Process completed with exit code 1."),
          p("Captura autêntica do run no GitHub Actions. O detalhe da regra está em evidencias/01-gitleaks-github.txt. URL: github.com/efsartorelli/CP05-DEVOPS/actions/runs/38461907382", "SmallCP"),
          PageBreak()]

# Semgrep
story += [tag("03 / Segunda barreira"), p("Semgrep: análise estática", "SectionTitleCP"),
          p("O Semgrep 1.140.0 analisa JavaScript. A regra local <b>fiap-cp05-no-eval</b>, criada para esta demonstração, identifica <b>eval(...)</b>; a opção <b>--error</b> torna o achado bloqueante. A branch <b>prova/semgrep</b> recebeu o exemplo abaixo, que não é executado:"),
          Preformatted("function exemploInseguro(entrada) { return eval(entrada); }", styles["CodeCP"]),
          p("No run 38461915387, o job Semgrep falhou em 13/10/2026 às 20:19 UTC com <b>1 finding (1 blocking)</b>, regra <b>semgrep.fiap-cp05-no-eval</b> em app.js e <b>exit code 1</b>. A main passou sem achados. eval interpreta texto como código JavaScript e pode executar entrada influenciada por terceiros."),
          screenshot("02-semgrep.png"),
          box("Trecho do log do GitHub Actions", "semgrep.fiap-cp05-no-eval  |  Findings: 1 (1 blocking)  |  Process completed with exit code 1."),
          p("Captura autêntica do run no GitHub Actions. O achado detalhado está em evidencias/02-semgrep-github.txt. URL: github.com/efsartorelli/CP05-DEVOPS/actions/runs/38461915387", "SmallCP"),
          PageBreak()]

# Trivy
story += [tag("04 / Terceira barreira"), p("Trivy: vulnerabilidades da imagem", "SectionTitleCP"),
          p("O job construiu <b>fiap-cp05:f074f1da9053a1a97aa7682e18f725942dfa72fc</b> a partir do Dockerfile e confirmou resposta HTTP 200 na porta 8080 do contêiner. O Trivy examinou a imagem construída, publicou um JSON como artefato, exibiu a tabela nos logs e aplicou a política de bloqueio para <b>CRITICAL</b>."),
          p("No run 38462913681, a tabela apresentou <b>1 CVE MEDIUM</b> e <b>0 CRITICAL</b>: <b>CVE-2026-85091</b> no pacote zlib 1.3.2-r0, com correção indicada em 1.3.2-r1. O job passou porque MEDIUM está abaixo do limite definido. Isso não significa ausência de vulnerabilidades; o pacote deve ser reavaliado em atualização segura da imagem-base."),
          screenshot("03-trivy.png"),
          box("Trecho do log do GitHub Actions", "Total: 1 (MEDIUM: 1, CRITICAL: 0)  |  zlib  |  CVE-2026-85091  |  Aplicação respondeu HTTP 200 dentro do contêiner."),
          p("Captura autêntica do run na main. Tabela e build: evidencias/03-trivy-github.txt; relatório completo: evidencias/03-trivy-github-report.json. URL: github.com/efsartorelli/CP05-DEVOPS/actions/runs/38462913681", "SmallCP"),
          PageBreak()]

# Conclusão e repositório
story += [tag("05 / Encerramento"), p("Conclusão", "SectionTitleCP"),
          p("As três ferramentas protegem etapas diferentes: Gitleaks examina exposição de credenciais no histórico; Semgrep identifica um padrão de código inseguro; Trivy relaciona pacotes da imagem a CVEs. O pipeline executou os três jobs na main com sucesso e bloqueou as duas sabotagens em branches isoladas. O Trivy registrou uma CVE MEDIUM na imagem construída e manteve o job aprovado pela política que bloqueia CRITICAL."),
          p("Repositório e execuções", "SectionTitleCP"),
          p("Repositório: <link href='https://github.com/efsartorelli/CP05-DEVOPS' color='#E91860'>https://github.com/efsartorelli/CP05-DEVOPS</link>", "BodyCP"),
          p("Gitleaks (falha esperada): <link href='https://github.com/efsartorelli/CP05-DEVOPS/actions/runs/38461907382' color='#E91860'>https://github.com/efsartorelli/CP05-DEVOPS/actions/runs/38461907382</link>", "SmallCP"),
          p("Semgrep (falha esperada): <link href='https://github.com/efsartorelli/CP05-DEVOPS/actions/runs/38461915387' color='#E91860'>https://github.com/efsartorelli/CP05-DEVOPS/actions/runs/38461915387</link>", "SmallCP"),
          p("Trivy e main (sucesso): <link href='https://github.com/efsartorelli/CP05-DEVOPS/actions/runs/38462913681' color='#E91860'>https://github.com/efsartorelli/CP05-DEVOPS/actions/runs/38462913681</link>", "SmallCP"),
          p("pull_request (teste, PR #1 fechado): <link href='https://github.com/efsartorelli/CP05-DEVOPS/actions/runs/38464011096' color='#E91860'>https://github.com/efsartorelli/CP05-DEVOPS/actions/runs/38464011096</link>", "SmallCP"),
          p("Commits das provas: prova/gitleaks em c68a4d5; prova/semgrep em 0225a55. Ambas as branches permanecem isoladas da main.", "SmallCP"),
          Spacer(1, 8 * mm),
          box("Integridade das evidências", "As três imagens são capturas diretas das páginas dos runs no GitHub Actions. A visualização pública pede login para mostrar logs; por isso os logs autênticos foram baixados pela API autenticada e preservados ao lado das imagens. Os arquivos de sabotagem nunca foram mesclados à main."),
          Spacer(1, 8 * mm),
          HRFlowable(color=LINE, width="100%"), Spacer(1, 6 * mm),
          p("Fontes técnicas", "SubTitleCP"),
          p("Gitleaks: github.com/gitleaks/gitleaks<br/>Semgrep CLI: semgrep.dev/docs/cli-reference<br/>Trivy Action: github.com/aquasecurity/trivy-action<br/>Nginx sem privilégios: github.com/nginx/docker-nginx-unprivileged", "SmallCP")]

doc.build(story, onFirstPage=page_header, onLaterPages=page_header)
print(OUTPUT)
