# Estado das evidências do GitHub Actions

As capturas `01-gitleaks.png`, `02-semgrep.png` e `03-trivy.png` ainda **não existem**. Esta pasta não contém capturas simuladas.

Em 13/10/2026, o diretório local não tinha remoto GitHub configurado, `gh` não estava instalado e não havia Docker disponível no terminal. Portanto, nenhuma execução do GitHub Actions ou imagem construída foi confirmada. As URLs dos runs e os CVEs da imagem do projeto estão pendentes.

Resultados locais confirmados:

| Etapa | Resultado local | Limite da evidência |
| --- | --- | --- |
| Gitleaks na branch `prova/gitleaks` | 1 achado `fiap-cp05-fake-token`, saída 1 | Não é captura do GitHub Actions |
| Semgrep na branch `prova/semgrep` | 1 achado `fiap-cp05-no-eval` em `app.js`, saída 1 | Não é captura do GitHub Actions |
| Trivy | Imagem-base remota: 1 CVE `MEDIUM`, 0 `CRITICAL`; saída 0 na política crítica | A imagem do projeto não foi construída |

Logs autênticos dos testes locais: [gitleaks-local.txt](gitleaks-local.txt), [semgrep-local.txt](semgrep-local.txt) e [trivy-base-local.txt](trivy-base-local.txt). O último arquivo analisa somente a imagem-base remota `nginxinc/nginx-unprivileged:stable-alpine`, digest `sha256:56b8272e43a0525f67aed68d1e0794a712d10e3e45a563e118e9a77c817e6f86`. Em 13/10/2026, o achado foi `CVE-2026-85091`, severidade `MEDIUM`, pacote `zlib` 1.3.2-r0, corrigido em 1.3.2-r1. O resultado não pode ser transferido automaticamente para uma imagem construída em outro momento.

Para completar a entrega, configure o remoto, publique `main` e as duas branches de prova sem mesclá-las, abra as execuções do workflow **Security Pipeline** e capture a página de cada job com repositório, usuário, data, status e mensagem da ferramenta visíveis. Guarde as imagens sob os nomes acima e atualize o relatório com as URLs reais e o resultado do Trivy.
