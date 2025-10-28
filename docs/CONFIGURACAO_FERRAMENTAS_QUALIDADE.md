# 🔧 **CONFIGURAÇÃO DE FERRAMENTAS DE QUALIDADE**

## 📋 **VISÃO GERAL**

Este arquivo configura todas as ferramentas de qualidade de código para o projeto CoinBalance, garantindo consistência e padronização em todo o desenvolvimento.

---

## 🎨 **FORMATAÇÃO DE CÓDIGO**

### **Black - Formatação Automática**
```toml
# pyproject.toml
[tool.black]
line-length = 88
target-version = ['py311']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''
```

### **isort - Organização de Imports**
```toml
# pyproject.toml
[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88
known_first_party = ["src"]
known_third_party = ["fastapi", "pydantic", "sqlalchemy"]
sections = ["FUTURE", "STDLIB", "THIRDPARTY", "FIRSTPARTY", "LOCALFOLDER"]
```

---

## 🔍 **ANÁLISE DE CÓDIGO**

### **Flake8 - Linting**
```ini
# setup.cfg
[flake8]
max-line-length = 88
extend-ignore = E203, W503, E501
exclude = 
    .git,
    __pycache__,
    .venv,
    venv,
    .eggs,
    *.egg,
    build,
    dist,
    .mypy_cache,
    .pytest_cache
per-file-ignores =
    __init__.py:F401
max-complexity = 10
```

### **MyPy - Verificação de Tipos**
```ini
# mypy.ini
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_incomplete_defs = True
check_untyped_defs = True
disallow_untyped_decorators = True
no_implicit_optional = True
warn_redundant_casts = True
warn_unused_ignores = True
warn_no_return = True
warn_unreachable = True
strict_equality = True

# Ignore missing imports for external libraries
[[mypy.fastapi.*]]
ignore_missing_imports = True

[[mypy.pydantic.*]]
ignore_missing_imports = True

[[mypy.sqlalchemy.*]]
ignore_missing_imports = True
```

### **Pylint - Análise Avançada**
```ini
# pylintrc
[MASTER]
load-plugins=pylint_django

[MESSAGES CONTROL]
disable=
    missing-docstring,
    too-few-public-methods,
    too-many-arguments,
    too-many-locals,
    too-many-branches,
    too-many-statements,
    duplicate-code,
    import-error,
    no-member,
    not-callable,
    no-name-in-module,
    used-before-assignment,
    broad-except,
    bare-except,
    unused-argument,
    redefined-outer-name,
    unused-variable,
    global-statement,
    consider-using-f-string,
    line-too-long,
    missing-module-docstring,
    missing-class-docstring,
    missing-function-docstring

[FORMAT]
max-line-length=88
indent-string='    '

[DESIGN]
max-args=10
max-locals=20
max-returns=6
max-branches=15
max-statements=60
max-parents=10
max-attributes=15
max-public-methods=25
max-bool-expr=5

[SIMILARITIES]
min-similarity-lines=4
ignore-comments=yes
ignore-docstrings=yes
ignore-imports=no
```

---

## 🔒 **ANÁLISE DE SEGURANÇA**

### **Bandit - Segurança**
```ini
# bandit.yaml
exclude_dirs:
  - tests
  - test
  - .venv
  - venv
  - .git

skips:
  - B101  # assert_used
  - B601  # shell_injection_subprocess

tests:
  - B201
  - B301
  - B302
  - B303
  - B304
  - B305
  - B306
  - B307
  - B308
  - B309
  - B310
  - B311
  - B312
  - B313
  - B314
  - B315
  - B316
  - B317
  - B318
  - B319
  - B320
  - B321
  - B322
  - B323
  - B324
  - B325
  - B501
  - B502
  - B503
  - B504
  - B505
  - B506
  - B507
  - B508
  - B509
  - B510
  - B511
  - B512
  - B513
  - B514
  - B515
  - B516
  - B517
  - B518
  - B519
  - B520
  - B521
  - B522
  - B523
  - B524
  - B525
  - B526
  - B527
  - B528
  - B529
  - B530
  - B531
  - B532
  - B533
  - B534
  - B535
  - B536
  - B537
  - B538
  - B539
  - B540
  - B541
  - B542
  - B543
  - B544
  - B545
  - B546
  - B547
  - B548
  - B549
  - B550
  - B551
  - B552
  - B553
  - B554
  - B555
  - B556
  - B557
  - B558
  - B559
  - B560
  - B561
  - B562
  - B563
  - B564
  - B565
  - B566
  - B567
  - B568
  - B569
  - B570
  - B571
  - B572
  - B573
  - B574
  - B575
  - B576
  - B577
  - B578
  - B579
  - B580
  - B581
  - B582
  - B583
  - B584
  - B585
  - B586
  - B587
  - B588
  - B589
  - B590
  - B591
  - B592
  - B593
  - B594
  - B595
  - B596
  - B597
  - B598
  - B599
  - B600
  - B602
  - B603
  - B604
  - B605
  - B606
  - B607
  - B608
  - B609
  - B610
  - B611
  - B612
  - B613
  - B614
  - B615
  - B616
  - B617
  - B618
  - B619
  - B620
  - B621
  - B622
  - B623
  - B624
  - B625
  - B626
  - B627
  - B628
  - B629
  - B630
  - B631
  - B632
  - B633
  - B634
  - B635
  - B636
  - B637
  - B638
  - B639
  - B640
  - B641
  - B642
  - B643
  - B644
  - B645
  - B646
  - B647
  - B648
  - B649
  - B650
  - B651
  - B652
  - B653
  - B654
  - B655
  - B656
  - B657
  - B658
  - B659
  - B660
  - B661
  - B662
  - B663
  - B664
  - B665
  - B666
  - B667
  - B668
  - B669
  - B670
  - B671
  - B672
  - B673
  - B674
  - B675
  - B676
  - B677
  - B678
  - B679
  - B680
  - B681
  - B682
  - B683
  - B684
  - B685
  - B686
  - B687
  - B688
  - B689
  - B690
  - B691
  - B692
  - B693
  - B694
  - B695
  - B696
  - B697
  - B698
  - B699
  - B700
  - B701
  - B702
  - B703
  - B704
  - B705
  - B706
  - B707
  - B708
  - B709
  - B710
  - B711
  - B712
  - B713
  - B714
  - B715
  - B716
  - B717
  - B718
  - B719
  - B720
  - B721
  - B722
  - B723
  - B724
  - B725
  - B726
  - B727
  - B728
  - B729
  - B730
  - B731
  - B732
  - B733
  - B734
  - B735
  - B736
  - B737
  - B738
  - B739
  - B740
  - B741
  - B742
  - B743
  - B744
  - B745
  - B746
  - B747
  - B748
  - B749
  - B750
  - B751
  - B752
  - B753
  - B754
  - B755
  - B756
  - B757
  - B758
  - B759
  - B760
  - B761
  - B762
  - B763
  - B764
  - B765
  - B766
  - B767
  - B768
  - B769
  - B770
  - B771
  - B772
  - B773
  - B774
  - B775
  - B776
  - B777
  - B778
  - B779
  - B780
  - B781
  - B782
  - B783
  - B784
  - B785
  - B786
  - B787
  - B788
  - B789
  - B790
  - B791
  - B792
  - B793
  - B794
  - B795
  - B796
  - B797
  - B798
  - B799
  - B800
  - B801
  - B802
  - B803
  - B804
  - B805
  - B806
  - B807
  - B808
  - B809
  - B810
  - B811
  - B812
  - B813
  - B814
  - B815
  - B816
  - B817
  - B818
  - B819
  - B820
  - B821
  - B822
  - B823
  - B824
  - B825
  - B826
  - B827
  - B828
  - B829
  - B830
  - B831
  - B832
  - B833
  - B834
  - B835
  - B836
  - B837
  - B838
  - B839
  - B840
  - B841
  - B842
  - B843
  - B844
  - B845
  - B846
  - B847
  - B848
  - B849
  - B850
  - B851
  - B852
  - B853
  - B854
  - B855
  - B856
  - B857
  - B858
  - B859
  - B860
  - B861
  - B862
  - B863
  - B864
  - B865
  - B866
  - B867
  - B868
  - B869
  - B870
  - B871
  - B872
  - B873
  - B874
  - B875
  - B876
  - B877
  - B878
  - B879
  - B880
  - B881
  - B882
  - B883
  - B884
  - B885
  - B886
  - B887
  - B888
  - B889
  - B890
  - B891
  - B892
  - B893
  - B894
  - B895
  - B896
  - B897
  - B898
  - B899
  - B900
  - B901
  - B902
  - B903
  - B904
  - B905
  - B906
  - B907
  - B908
  - B909
  - B910
  - B911
  - B912
  - B913
  - B914
  - B915
  - B916
  - B917
  - B918
  - B919
  - B920
  - B921
  - B922
  - B923
  - B924
  - B925
  - B926
  - B927
  - B928
  - B929
  - B930
  - B931
  - B932
  - B933
  - B934
  - B935
  - B936
  - B937
  - B938
  - B939
  - B940
  - B941
  - B942
  - B943
  - B944
  - B945
  - B946
  - B947
  - B948
  - B949
  - B950
  - B951
  - B952
  - B953
  - B954
  - B955
  - B956
  - B957
  - B958
  - B959
  - B960
  - B961
  - B962
  - B963
  - B964
  - B965
  - B966
  - B967
  - B968
  - B969
  - B970
  - B971
  - B972
  - B973
  - B974
  - B975
  - B976
  - B977
  - B978
  - B979
  - B980
  - B981
  - B982
  - B983
  - B984
  - B985
  - B986
  - B987
  - B988
  - B989
  - B990
  - B991
  - B992
  - B993
  - B994
  - B995
  - B996
  - B997
  - B998
  - B999
```

### **Safety - Vulnerabilidades de Dependências**
```ini
# safety.ini
[SAFETY]
output = json
full_report = true
short_report = true
```

---

## 📊 **ANÁLISE DE COMPLEXIDADE**

### **Radon - Análise de Complexidade**
```ini
# radon.ini
[radon]
min = 'B'
max = 'F'
no_assert = true
show_complexity = true
show_duplicates = true
show_errors = true
```

### **Xenon - Monitoramento de Complexidade**
```ini
# xenon.ini
[xenon]
max_absolute = 'B'
max_modules = 'A'
max_average = 'A'
```

---

## 🧪 **CONFIGURAÇÃO DE TESTES**

### **Pytest - Framework de Testes**
```ini
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --strict-markers
    --strict-config
    --cov=src
    --cov-report=term-missing
    --cov-report=html
    --cov-report=xml
    --cov-fail-under=95
    --junitxml=test-results.xml
    --maxfail=10
    --tb=short
markers =
    unit: Unit tests
    integration: Integration tests
    performance: Performance tests
    enterprise: Enterprise system tests
    slow: Slow running tests
    security: Security tests
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
```

### **Coverage - Cobertura de Código**
```ini
# .coveragerc
[run]
source = src
omit = 
    */tests/*
    */test/*
    */venv/*
    */.venv/*
    */migrations/*
    */__pycache__/*
    */settings/*
    */manage.py
    */wsgi.py
    */asgi.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    if self.debug:
    if settings.DEBUG
    raise AssertionError
    raise NotImplementedError
    if 0:
    if __name__ == .__main__.:
    class .*\bProtocol\):
    @(abc\.)?abstractmethod

[html]
directory = htmlcov
title = CoinBalance Test Coverage Report
```

---

## 🔧 **PRE-COMMIT HOOKS**

### **Pre-commit Configuration**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: check-json
      - id: check-toml
      - id: check-xml
      - id: debug-statements
      - id: check-docstring-first

  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=88, --extend-ignore=E203,W503]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
        args: [--ignore-missing-imports]

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: [-r, src/, -f, json, -o, bandit-report.json]
        exclude: ^tests/

  - repo: https://github.com/Lucas-C/pre-commit-hooks-safety
    rev: v1.3.2
    hooks:
      - id: python-safety-dependencies-check
        args: [--full-report]

  - repo: https://github.com/pycqa/pylint
    rev: v2.17.5
    hooks:
      - id: pylint
        args: [--rcfile=.pylintrc]
        exclude: ^tests/

  - repo: https://github.com/asottile/pyupgrade
    rev: v3.9.0
    hooks:
      - id: pyupgrade
        args: [--py311-plus]

  - repo: https://github.com/hadialqattan/pycln
    rev: v2.1.3
    hooks:
      - id: pycln
        args: [--config=pyproject.toml]
```

---

## 📈 **MÉTRICAS E RELATÓRIOS**

### **SonarQube - Análise de Qualidade**
```properties
# sonar-project.properties
sonar.projectKey=coinbalance
sonar.projectName=CoinBalance Blockchain
sonar.projectVersion=3.0.0
sonar.sources=src
sonar.tests=tests
sonar.python.coverage.reportPaths=coverage.xml
sonar.python.xunit.reportPath=test-results.xml
sonar.python.bandit.reportPaths=bandit-report.json
sonar.python.pylint.reportPaths=pylint-report.txt
sonar.coverage.exclusions=**/tests/**,**/test/**,**/migrations/**
sonar.qualitygate.wait=true
```

---

## 🚀 **COMANDOS DE QUALIDADE**

### **Scripts de Qualidade**
```bash
#!/bin/bash
# scripts/quality-check.sh

echo "🔍 Executando verificações de qualidade..."

# Formatação
echo "📝 Verificando formatação..."
black --check src/ tests/
isort --check-only src/ tests/

# Linting
echo "🔍 Executando linting..."
flake8 src/ tests/
pylint src/

# Verificação de tipos
echo "🔍 Verificando tipos..."
mypy src/

# Análise de segurança
echo "🔒 Executando análise de segurança..."
bandit -r src/
safety check

# Análise de complexidade
echo "📊 Analisando complexidade..."
radon cc src/ -a
xenon --max-absolute B --max-modules A --max-average A src/

# Testes
echo "🧪 Executando testes..."
pytest tests/ --cov=src --cov-report=html --cov-report=xml

echo "✅ Verificações de qualidade concluídas!"
```

### **Scripts de Correção**
```bash
#!/bin/bash
# scripts/quality-fix.sh

echo "🔧 Aplicando correções de qualidade..."

# Formatação automática
echo "📝 Aplicando formatação..."
black src/ tests/
isort src/ tests/

# Remoção de imports não utilizados
echo "🧹 Removendo imports não utilizados..."
pycln src/ --all

# Upgrade de sintaxe Python
echo "⬆️ Atualizando sintaxe Python..."
pyupgrade --py311-plus src/**/*.py

echo "✅ Correções aplicadas!"
```

---

## 📋 **CHECKLIST DE QUALIDADE**

### **Checklist Diário**
- [ ] Código formatado com Black
- [ ] Imports organizados com isort
- [ ] Linting sem erros (Flake8)
- [ ] Verificação de tipos (MyPy)
- [ ] Testes unitários passando
- [ ] Cobertura de testes > 95%

### **Checklist Semanal**
- [ ] Análise de segurança (Bandit)
- [ ] Verificação de dependências (Safety)
- [ ] Análise de complexidade (Radon/Xenon)
- [ ] Testes de integração
- [ ] Testes de performance
- [ ] Revisão de código

### **Checklist Mensal**
- [ ] Auditoria de segurança completa
- [ ] Análise de débito técnico
- [ ] Revisão de arquitetura
- [ ] Atualização de dependências
- [ ] Treinamento da equipe
- [ ] Melhoria de processos

---

## 🎯 **CONCLUSÃO**

Esta configuração garante que todas as ferramentas de qualidade estejam devidamente configuradas e integradas ao processo de desenvolvimento, mantendo os mais altos padrões de qualidade de código em todo o projeto CoinBalance.

**Status**: ✅ Configuração completa e pronta para uso
**Próximos Passos**: Execução dos scripts de qualidade e integração ao pipeline CI/CD
