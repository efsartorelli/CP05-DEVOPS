# Evidências autênticas do GitHub Actions

Repositório: [efsartorelli/CP05-DEVOPS](https://github.com/efsartorelli/CP05-DEVOPS). Todas as execuções abaixo ocorreram em 13/10/2026. As branches de sabotagem permanecem isoladas da `main`.

| Prova | Captura do run | Log integral do job | Execução |
| --- | --- | --- | --- |
| Gitleaks | [01-gitleaks.png](01-gitleaks.png) | [01-gitleaks-github.txt](01-gitleaks-github.txt) | [run 38461907382](https://github.com/efsartorelli/CP05-DEVOPS/actions/runs/38461907382) |
| Semgrep | [02-semgrep.png](02-semgrep.png) | [02-semgrep-github.txt](02-semgrep-github.txt) | [run 38461915387](https://github.com/efsartorelli/CP05-DEVOPS/actions/runs/38461915387) |
| Trivy | [03-trivy.png](03-trivy.png) | [03-trivy-github.txt](03-trivy-github.txt) | [run 38462913681](https://github.com/efsartorelli/CP05-DEVOPS/actions/runs/38462913681) |

As imagens são capturas diretas das páginas de resumo do GitHub Actions. Elas mostram repositório, usuário, workflow, branch e status dos jobs. A visualização pública pede login para abrir o texto dos logs. Os arquivos `.txt` foram baixados da API autenticada do GitHub, sem alterar as mensagens das ferramentas, e trazem os detalhes que justificam cada status. Nenhum print ou resultado foi simulado.

## Resultados verificados

- **Gitleaks:** o job da branch `prova/gitleaks` falhou com `RuleID: fiap-cp05-fake-token`, `leaks found: 1` e saída 1. O valor foi redigido pela ferramenta. [Job direto](https://github.com/efsartorelli/CP05-DEVOPS/actions/runs/38461907382/job/115518951676).
- **Semgrep:** o job da branch `prova/semgrep` falhou com `semgrep.fiap-cp05-no-eval`, `Findings: 1 (1 blocking)` e saída 1. [Job direto](https://github.com/efsartorelli/CP05-DEVOPS/actions/runs/38461915387/job/115518978001).
- **Trivy:** no run da `main`, o runner construiu `fiap-cp05:f074f1da9053a1a97aa7682e18f725942dfa72fc`, iniciou o contêiner e obteve HTTP 200. A análise da imagem construída encontrou 1 `MEDIUM` e 0 `CRITICAL`, logo a política de bloqueio crítico passou. [Job direto](https://github.com/efsartorelli/CP05-DEVOPS/actions/runs/38462913681/job/115522410054).

O CVE da imagem construída é `CVE-2026-85091` em zlib 1.3.2-r0, com atualização indicada para 1.3.2-r1. O relatório completo da execução está em [03-trivy-github-report.json](03-trivy-github-report.json) e no [artefato do run](https://github.com/efsartorelli/CP05-DEVOPS/actions/runs/38462913681/artifacts/11847630669). A presença de uma CVE `MEDIUM` foi mantida no relatório, sem exclusões para produzir um resultado artificialmente limpo.

Também estão preservados os logs dos ensaios locais: [gitleaks-local.txt](gitleaks-local.txt), [semgrep-local.txt](semgrep-local.txt) e [trivy-base-local.txt](trivy-base-local.txt). O último é uma análise separada da imagem-base remota, anterior ao build no GitHub.
