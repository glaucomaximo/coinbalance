# Contribuindo para CoinBalance (CBL)

Agradecemos seu interesse em contribuir! Este documento descreve o fluxo de contribuições, padrões de código, como abrir issues e PRs, e as expectativas para revisão.

Sumário rápido
- Como contribuir: issues, PRs, correções rápidas
- Código: formato, testes e CI
- Fluxo de branches e mensagens de commit
- Processo de revisão e merge
- Contato e código de conduta

1. Antes de começar
- Verifique issues abertas para evitar duplicação.
- Se for um trabalho maior (nova feature, refatoração), abra uma issue descrevendo a proposta antes de iniciar o PR.
- Adote o branch naming padrão: `feat/<desc>`, `fix/<desc>`, `chore/<desc>`, `docs/<desc>`, `ci/<desc>`, `refactor/<desc>`.

2. Ambiente de desenvolvimento
- Python: suporte para X.Y (documentar versão final em README)
- Recomendamos isolamento com venv/virtualenv/poetry.
- Instalação:
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt

3. Formatação e lint
- Código Python: use Black e isort. Recomendamos:
  - black .
  - isort .
- Lint: flake8 (configurar regras no `.flake8`).
- Antes de abrir PR, rode:
  - black .
  - isort .
  - pytest tests/ --maxfail=1 --disable-warnings -q

4. Testes
- Todo PR que altera lógica deve incluir testes unitários/integração.
- Testes devem rodar localmente com `pytest`.
- Objetivo mínimo de cobertura para componentes core: 70% (meta, não bloqueio inicial).

5. Commit messages
- Use o formato convencional (tipo: escopo — mensagem) preferencialmente:
  - feat(wallet): adiciona suporte a hd paths
  - fix(rpc): corrige parsing de txs
  - docs(readme): atualiza quickstart
- Mensagens em inglês ou português claras são aceitas — prefira inglês para mudanças públicas maiores.

6. Pull Requests
- Crie PRs contra o branch `master` (ou o branch que o maintainer indicar).
- PR deve incluir:
  - Título claro: tipo: escopo — resumo
  - Descrição com contexto e o que foi alterado
  - Checklist (preencha):
    - [ ] Testes adicionados/atualizados
    - [ ] Documentação atualizada (README/API)
    - [ ] Lint/format OK
    - [ ] Pipeline CI passou
- Coloque `Fixes #<issue>` se o PR fechar uma issue.

7. Labels e revisão
- Mantenedores irão etiquetar (bug, enhancement, documentation, help wanted, good first issue).
- PRs com alterações críticas (consenso, cripto, smart contracts) exigem revisão por, no mínimo, 2 mantenedores.
- PRs de docs e correções menores podem ser mesclados com 1 aprovação.

8. Segurança
- Para reporte de vulnerabilidade, envie email para security@coinbalance.example (ou use o canal privado indicado).
- Não publique vulnerabilidades em issues públicas até haver mitigação/patch.

9. Pull request templates e issues
- Use os templates disponibilizados em `.github/ISSUE_TEMPLATE` e `.github/PULL_REQUEST_TEMPLATE.md`.

10. Código de Conduta
- Todos os contribuidores devem respeitar o Código de Conduta do projeto (arquivo CODE_OF_CONDUCT.md).
- Comportamento hostil/abusivo não será tolerado.

11. Contribuições de terceiros
- Ao contribuir, você concorda que suas contribuições poderão ser licenciadas sob MIT (licença do projeto).
- Para contribuições maiores, o time pode solicitar um CLA (Contributor License Agreement).

12. Suporte
- Para dúvidas, abra uma issue com a tag `question` ou contate os mantenedores no perfil do repositório.

Obrigado por contribuir!