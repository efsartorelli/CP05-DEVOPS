# FIAP CP05 - Pipeline DevSecOps Completo

Aplicação estática interativa para o Checkpoint 05 de DevSecOps and Cloud Computing (Engenharia de Software, FIAP). O workflow **Security Pipeline** verifica segredos no histórico, código JavaScript e vulnerabilidades na imagem construída pelo Dockerfile. O painel da aplicação permite marcar etapas de estudo no navegador; esse progresso local não representa o resultado do CI.

**Aluno:** Enzo Sartorelli (identificação disponível na configuração Git local; confirmar RM antes da entrega acadêmica).

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

## Reproduzir as sabotagens

As branches locais `prova/gitleaks` e `prova/semgrep` contêm commits isolados, criados a partir de `main`. **Não faça merge dessas branches.** Os exemplos são fictícios e não incluem credenciais reais. Quando o projeto estiver publicado no GitHub, envie essas branches separadamente para acionar o workflow.

```bash
git switch prova/gitleaks
gitleaks git . --config .gitleaks.toml --log-opts="HEAD" --redact --verbose --exit-code 1
# Esperado: RuleID fiap-cp05-fake-token, saída 1.

git switch prova/semgrep
semgrep scan --config .semgrep/eval.yml --error --metrics=off .
# Esperado: fiap-cp05-no-eval em app.js, saída 1.

git switch main
```

Para validar o Trivy no CI, publique `main` e abra o job `trivy` de uma execução. Confira a tabela de CVEs, o artefato JSON e a etapa final de bloqueio. CVEs `LOW`, `MEDIUM` ou `HIGH` são exibidos, mas não bloqueiam por esta política; `CRITICAL` bloqueia. Uma execução sem `CRITICAL` não prova ausência de todas as vulnerabilidades.

## Evidências e relatório

O estado da coleta está em [evidencias/README.md](evidencias/README.md). As capturas exigidas (`01-gitleaks.png`, `02-semgrep.png`, `03-trivy.png`) devem ser imagens autênticas do GitHub Actions. Os logs locais não substituem essas capturas.

O relatório está em [CP05_DevSecOps_Relatorio.pdf](CP05_DevSecOps_Relatorio.pdf). Sem remoto GitHub configurado, o relatório registra os testes locais efetivamente realizados e deixa explícitas as pendências de execução remota, Docker e screenshots.

## Referências técnicas

- [Gitleaks](https://github.com/gitleaks/gitleaks)
- [Semgrep CLI](https://semgrep.dev/docs/cli-reference)
- [Trivy Action](https://github.com/aquasecurity/trivy-action)
- [Nginx sem privilégios](https://github.com/nginx/docker-nginx-unprivileged)
