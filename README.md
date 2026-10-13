# FIAP CP05 - Pipeline DevSecOps Completo

Aplicação estática interativa para o Checkpoint 05 de DevSecOps and Cloud Computing (Engenharia de Software, FIAP). O workflow **Security Pipeline** verifica segredos no histórico, código JavaScript e vulnerabilidades na imagem construída pelo Dockerfile. O painel da aplicação permite marcar etapas de estudo no navegador; esse progresso local não representa o resultado do CI.

**Equipe:** Enzo Vazquez Sartorelli (RM94818), Guilherme Brazioli (RM98237), Pedro Oliveira Valotto (RM551445), Nicolas Nogueira Boni (RM551965) e Kaue Pastori Teixeira (RM98501).

## Tecnologias

- HTML, CSS e JavaScript sem dependências de produção.
- Nginx sem privilégios, servido na porta 8080 do contêiner.
- GitHub Actions, Gitleaks 8.30.0, Semgrep 1.140.0 e Trivy Action v0.36.0.

## Estrutura

```text
.
├── .github/workflows/security.yml  # 3 jobs de segurança
├── .gitleaks.toml                   # regras padrão + token fictício do CP05
├── .semgrep/eval.yml                # regra local de demonstração
├── Dockerfile / .dockerignore
├── nginx.conf
├── index.html / styles.css / app.js
├── evidencias/                      # estado das evidências externas
└── CP05_DevSecOps_Relatorio.pdf
```

## Executar localmente

Para testar os arquivos sem contêiner: `python -m http.server 8080` e abrir `http://localhost:8080/`. Para usar o contêiner, com Docker instalado e em execução:

```bash
docker build -t fiap-cp05:latest .
docker run --rm -p 8080:8080 fiap-cp05:latest
```

A imagem Nginx sem privilégios usa a porta interna 8080. O exemplo usual `-p 8080:80` não se aplica aqui. A aplicação deve responder em `http://localhost:8080/`.

## Jobs do pipeline

O workflow roda em `push` e `pull_request` e contém exatamente três jobs:

| Job | O que verifica | Condição de falha |
| --- | --- | --- |
| `gitleaks` | Histórico completo da branch após `fetch-depth: 0`; regras padrão e token fictício CP05 | Segredo detectado; saída 1 |
| `semgrep` | JavaScript com regra local `.semgrep/eval.yml` | Chamada de `eval(...)`; `--error` |
| `trivy` | Imagem `fiap-cp05:${{ github.sha }}` construída no próprio job | CVE de severidade `CRITICAL`; saída 1 |

O Trivy mostra uma tabela com todas as severidades nos logs, gera um JSON como artefato e executa uma última verificação que bloqueia somente `CRITICAL`. A regra local do Semgrep foi criada para demonstrar a detecção exigida no CP05. A configuração do Gitleaks estende as regras padrão e acrescenta uma assinatura exclusiva do token fictício usado no teste.

O job `trivy` também inicia o contêiner no runner e verifica uma resposta HTTP 200 em `127.0.0.1:8080` antes da análise da imagem.

## Reproduzir as sabotagens

As branches `prova/gitleaks` e `prova/semgrep` contêm commits isolados, criados a partir de `main`, e já estão publicadas no GitHub. **Não faça merge dessas branches.** Os exemplos são fictícios e não incluem credenciais reais.

```bash
git switch prova/gitleaks
gitleaks git . --config .gitleaks.toml --log-opts="HEAD" --redact --verbose --exit-code 1
# Esperado: RuleID fiap-cp05-fake-token, saída 1.

git switch prova/semgrep
semgrep scan --config .semgrep/eval.yml --error --metrics=off .
# Esperado: fiap-cp05-no-eval em app.js, saída 1.

git switch main
```

Para validar o Trivy no CI, abra o [run aprovado da main](https://github.com/efsartorelli/CP05-DEVOPS/actions/runs/38462913681). Confira o build, a execução HTTP do contêiner, a tabela de CVEs, o artefato JSON e a etapa final de bloqueio. CVEs `LOW`, `MEDIUM` ou `HIGH` são exibidos, mas não bloqueiam por esta política; `CRITICAL` bloqueia. Uma execução sem `CRITICAL` não prova ausência de todas as vulnerabilidades.

## Evidências e relatório

As capturas autênticas do GitHub Actions, os logs baixados dos jobs e o JSON do Trivy estão descritos em [evidencias/README.md](evidencias/README.md). As capturas são das páginas de resumo dos runs; os logs preservam os achados detalhados porque a página pública exige login para exibi-los.

O relatório completo está em [CP05_DevSecOps_Relatorio.pdf](CP05_DevSecOps_Relatorio.pdf). Repositório: [efsartorelli/CP05-DEVOPS](https://github.com/efsartorelli/CP05-DEVOPS).

## Resultados reais do GitHub Actions

| Branch e run | Gitleaks | Semgrep | Trivy |
| --- | --- | --- | --- |
| [`main` · 38462913681](https://github.com/efsartorelli/CP05-DEVOPS/actions/runs/38462913681) | Passou | Passou | Passou; build e HTTP 200; 1 CVE `MEDIUM`, 0 `CRITICAL` |
| [`prova/gitleaks` · 38461907382](https://github.com/efsartorelli/CP05-DEVOPS/actions/runs/38461907382) | Falhou; 1 token fictício | Passou | Passou |
| [`prova/semgrep` · 38461915387](https://github.com/efsartorelli/CP05-DEVOPS/actions/runs/38461915387) | Passou | Falhou; 1 uso de `eval` | Passou |
| [`pull_request` · 38464011096](https://github.com/efsartorelli/CP05-DEVOPS/actions/runs/38464011096) | Passou | Falhou; 1 uso de `eval` | Passou |

O achado Trivy foi `CVE-2026-85091` no pacote zlib 1.3.2-r0, classificado como `MEDIUM`; a correção indicada no relatório é 1.3.2-r1. A política crítica não bloqueou o job.

O [PR de teste #1](https://github.com/efsartorelli/CP05-DEVOPS/pull/1) comprovou o gatilho `pull_request`. Ele foi fechado sem merge depois da execução. Após a publicação das evidências, a [main voltou a passar nos três jobs](https://github.com/efsartorelli/CP05-DEVOPS/actions/runs/38463925230).

## Referências técnicas

- [Gitleaks](https://github.com/gitleaks/gitleaks)
- [Semgrep CLI](https://semgrep.dev/docs/cli-reference)
- [Trivy Action](https://github.com/aquasecurity/trivy-action)
- [Nginx sem privilégios](https://github.com/nginx/docker-nginx-unprivileged)
