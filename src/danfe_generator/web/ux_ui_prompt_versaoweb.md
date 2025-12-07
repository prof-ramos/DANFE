# 📋 Versão Web - Gerador de NF-e e DANFE

## Visão Geral

A Versão Web do DANFE Generator oferecerá uma **funcionalidade completa de criação de NF-e**, permitindo que o usuário preencha todos os campos fiscais através de uma interface intuitiva e gere tanto o **XML da NF-e** quanto o **PDF do DANFE** em uma única operação.

---

## 🎯 Objetivo Principal

Permitir que usuários sem conhecimento técnico de XML possam:

1. **Criar NF-e do zero** preenchendo formulários estruturados
2. **Gerar XML válido** no padrão NF-e 4.00 do Portal Fiscal
3. **Gerar PDF do DANFE** automaticamente a partir do XML criado
4. **Incluir protocolo de autorização** (`protNFe`) quando aplicável

---

## 🖥️ Estrutura da Interface

### Abas/Seções do Formulário

A interface será organizada em **seções colapsáveis** seguindo a estrutura do XML:

| Seção | Bloco XML | Campos Principais |
|-------|-----------|-------------------|
| **1. Identificação** | `<ide>` | UF, Natureza Operação, Série, Número, Data/Hora, Tipo NF-e, Finalidade |
| **2. Emitente** | `<emit>` | CNPJ, Razão Social, Nome Fantasia, Endereço, IE, CRT |
| **3. Destinatário** | `<dest>` | CNPJ/CPF, Nome, Endereço, Indicador IE, IE |
| **4. Produtos/Serviços** | `<det>` | Tabela dinâmica com múltiplos itens (código, descrição, NCM, CFOP, valores) |
| **5. Impostos** | `<imposto>` | ICMS, PIS, COFINS por item (calculados automaticamente) |
| **6. Totais** | `<total>` | Calculados automaticamente com base nos itens |
| **7. Transporte** | `<transp>` | Modalidade frete, Transportadora, Volumes |
| **8. Cobrança** | `<cobr>` | Fatura, Duplicatas (opcional) |
| **9. Pagamento** | `<pag>` | Forma de pagamento, Valor, Troco |
| **10. Informações Adicionais** | `<infAdic>` | Informações fiscais e complementares |
| **11. Protocolo SEFAZ** | `<protNFe>` | Checkbox para incluir, campos do protocolo |

---

## 🔄 Fluxo do Usuário (User Flow)

```
┌─────────────────────────────────────────────────────────────────────┐
│                         FLUXO DE CRIAÇÃO                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. INÍCIO                                                          │
│     └── Usuário clica em "Criar Nova NF-e"                          │
│                                                                     │
│  2. PREENCHIMENTO                                                   │
│     ├── Preenche dados do Emitente (ou carrega perfil salvo)        │
│     ├── Preenche dados do Destinatário                              │
│     ├── Adiciona Produtos/Serviços (tabela dinâmica)                │
│     │   └── Sistema calcula impostos automaticamente                │
│     ├── Configura Transporte (opcional)                             │
│     ├── Configura Cobrança/Pagamento                                │
│     └── Adiciona Informações Complementares                         │
│                                                                     │
│  3. PROTOCOLO (OPCIONAL)                                            │
│     ├── [  ] Incluir protocolo de autorização (protNFe)             │
│     │   ├── Se SIM: Preenche campos do protocolo                    │
│     │   │   ├── Número do Protocolo                                 │
│     │   │   ├── Data/Hora Recebimento                               │
│     │   │   └── Status (100 = Autorizada)                           │
│     │   └── Se NÃO: XML gerado sem protocolo                        │
│     │                                                               │
│  4. VALIDAÇÃO                                                       │
│     ├── Sistema valida campos obrigatórios                          │
│     ├── Sistema valida formatos (CNPJ, datas, valores)              │
│     └── Sistema calcula dígito verificador da chave                 │
│                                                                     │
│  5. GERAÇÃO                                                         │
│     ├── Usuário clica em "◆ GERAR NF-e"                             │
│     └── Sistema gera:                                               │
│         ├── 📄 XML da NF-e (nfe_CHAVE.xml)                          │
│         └── 📑 PDF do DANFE (nfe_CHAVE.pdf)                         │
│                                                                     │
│  6. DOWNLOAD                                                        │
│     ├── Botão "⬇ Baixar XML"                                        │
│     ├── Botão "⬇ Baixar PDF"                                        │
│     └── Botão "⬇ Baixar Ambos (ZIP)"                                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📝 Campos por Seção

### 1. Identificação (`<ide>`)

| Campo | Tag XML | Tipo | Obrigatório | Descrição |
|-------|---------|------|-------------|-----------|
| UF Emitente | `<cUF>` | Select | ✅ | Dropdown com estados (código IBGE) |
| Natureza Operação | `<natOp>` | Text | ✅ | Ex: "VENDA DE MERCADORIA" |
| Modelo | `<mod>` | Fixed | ✅ | Sempre "55" (NF-e) |
| Série | `<serie>` | Number | ✅ | Série da NF-e |
| Número | `<nNF>` | Number | ✅ | Número da NF-e |
| Data/Hora Emissão | `<dhEmi>` | DateTime | ✅ | Picker com timezone |
| Tipo Operação | `<tpNF>` | Select | ✅ | 0=Entrada, 1=Saída |
| Destino Operação | `<idDest>` | Select | ✅ | 1=Interna, 2=Interestadual, 3=Exterior |
| Município FG | `<cMunFG>` | Select | ✅ | Autocomplete com código IBGE |
| Tipo Impressão | `<tpImp>` | Select | ✅ | 1=Retrato (padrão) |
| Tipo Emissão | `<tpEmis>` | Select | ✅ | 1=Normal (padrão) |
| Ambiente | `<tpAmb>` | Select | ✅ | 1=Produção, 2=Homologação |
| Finalidade | `<finNFe>` | Select | ✅ | 1=Normal, 2=Complementar, 3=Ajuste, 4=Devolução |
| Consumidor Final | `<indFinal>` | Toggle | ✅ | 0=Não, 1=Sim |
| Presença Comprador | `<indPres>` | Select | ✅ | 1=Presencial, 2=Internet, etc. |

### 2. Emitente (`<emit>`)

| Campo | Tag XML | Tipo | Obrigatório | Validação |
|-------|---------|------|-------------|-----------|
| CNPJ | `<CNPJ>` | Mask | ✅ | Validar dígitos CNPJ |
| Razão Social | `<xNome>` | Text | ✅ | Max 60 caracteres |
| Nome Fantasia | `<xFant>` | Text | ❌ | Max 60 caracteres |
| Logradouro | `<xLgr>` | Text | ✅ | - |
| Número | `<nro>` | Text | ✅ | - |
| Complemento | `<xCpl>` | Text | ❌ | - |
| Bairro | `<xBairro>` | Text | ✅ | - |
| Município | `<cMun>`/`<xMun>` | Autocomplete | ✅ | IBGE |
| UF | `<UF>` | Select | ✅ | - |
| CEP | `<CEP>` | Mask | ✅ | 8 dígitos |
| Telefone | `<fone>` | Mask | ❌ | - |
| IE | `<IE>` | Text | ✅ | Validar por UF |
| CRT | `<CRT>` | Select | ✅ | 1=SN, 2=SN Excesso, 3=Normal |

### 3. Produtos (`<det>` → Tabela Dinâmica)

**Interface**: Tabela editável com botões "Adicionar Item" e "Remover Item"

| Coluna | Tag XML | Tipo | Descrição |
|--------|---------|------|-----------|
| # | `nItem` | Auto | Sequencial automático |
| Código | `<cProd>` | Text | Código interno |
| EAN | `<cEAN>` | Text/Select | Código de barras ou "SEM GTIN" |
| Descrição | `<xProd>` | Text | Descrição do produto |
| NCM | `<NCM>` | Autocomplete | 8 dígitos com busca |
| CFOP | `<CFOP>` | Autocomplete | Com descrição |
| Unidade | `<uCom>` | Select | UN, KG, CX, PCT, etc. |
| Quantidade | `<qCom>` | Number | 4 casas decimais |
| Valor Unitário | `<vUnCom>` | Currency | 4 casas decimais |
| Valor Total | `<vProd>` | Calculated | Auto: qCom × vUnCom |
| BC ICMS | `<vBC>` | Currency | = vProd (padrão) |
| Alíq. ICMS | `<pICMS>` | Percent | Baseado na UF |
| Valor ICMS | `<vICMS>` | Calculated | Auto: vBC × pICMS |

---

## ⚙️ Funcionalidades Especiais

### Cálculos Automáticos

```python
# Ao alterar qualquer item:
vProd = qCom × vUnCom              # Valor do produto
vBC = vProd                        # Base de cálculo (padrão)
vICMS = vBC × (pICMS / 100)        # Valor ICMS
vPIS = vBC × (pPIS / 100)          # Valor PIS
vCOFINS = vBC × (pCOFINS / 100)    # Valor COFINS

# Totais (recalculados em tempo real):
vBC_total = Σ(vBC de todos os itens)
vICMS_total = Σ(vICMS)
vPIS_total = Σ(vPIS)
vCOFINS_total = Σ(vCOFINS)
vProd_total = Σ(vProd)
vNF = vProd_total + vFrete + vSeg + vOutro - vDesc
```

### Chave de Acesso

Gerada automaticamente com base nos campos preenchidos:

```
CHAVE = cUF + AAMM + CNPJ + mod + serie + nNF + tpEmis + cNF + cDV
        (2)   (4)   (14)   (2)   (3)    (9)    (1)     (8)   (1)

Exemplo: 35231212345678000195550010000000021000000028
```

### Checkbox "Incluir Protocolo"

```
[ ] Incluir protocolo de autorização (protNFe)

    Se marcado, exibe campos:
    ┌─────────────────────────────────────────────────┐
    │ Número do Protocolo:  [________________]        │
    │ Data Recebimento:     [____/____/____ __:__]    │
    │ Código Status:        [100 - Autorizada    ▼]   │
    │ Versão Aplicativo:    [________________]        │
    └─────────────────────────────────────────────────┘
```

---

## 📤 Saída (Output)

Ao clicar em **"◆ GERAR NF-e"**, o sistema produz:

### 1. Arquivo XML

```
nfe_35231212345678000195550010000000021000000028.xml
```

- Estrutura válida conforme layout NF-e 4.00
- Encoding UTF-8
- Namespace correto do Portal Fiscal
- Com ou sem `<protNFe>` dependendo da opção

### 2. Arquivo PDF (DANFE)

```
nfe_35231212345678000195550010000000021000000028.pdf
```

- Gerado automaticamente usando o brazilfiscalreport
- Aplica configurações de cores/margens/logo da sidebar

### Opções de Download

| Botão | Ação |
|-------|------|
| ⬇ **Baixar XML** | Download apenas do XML |
| ⬇ **Baixar PDF** | Download apenas do DANFE |
| ⬇ **Baixar Ambos** | Download de ZIP contendo XML + PDF |

---

## 🎨 Design UX/UI

### Princípios

1. **Progressão Visual**: Seções colapsáveis que expandem conforme preenchimento
2. **Feedback Imediato**: Validação em tempo real com ícones ✅ ❌
3. **Cálculos Live**: Totais atualizados instantaneamente
4. **Prevenção de Erros**: Máscaras de entrada, autocomplete, validações
5. **Economia de Tempo**: Perfis salvos de emitente, histórico de destinatários

### Componentes Sugeridos

| Componente | Uso |
|------------|-----|
| **Accordion** | Seções colapsáveis (ide, emit, dest, det...) |
| **DataTable** | Tabela de produtos com edição inline |
| **Stepper** | Indicador de progresso do preenchimento |
| **Toast** | Notificações de sucesso/erro |
| **Modal** | Confirmação antes de gerar |
| **Autocomplete** | NCM, CFOP, Municípios |

### Estados da Interface

```
┌─────────────────────────────────────────────────────────────────────┐
│  ESTADO INICIAL                                                     │
│  └── Formulário vazio, botão "GERAR" desabilitado                   │
│                                                                     │
│  ESTADO EM PREENCHIMENTO                                            │
│  └── Campos sendo preenchidos, validação em tempo real              │
│  └── Indicador de progresso: "3 de 10 seções completas"             │
│                                                                     │
│  ESTADO VALIDADO                                                    │
│  └── Todos os campos obrigatórios OK                                │
│  └── Botão "GERAR" habilitado com destaque                          │
│                                                                     │
│  ESTADO GERANDO                                                     │
│  └── Spinner/Progress bar                                           │
│  └── "Gerando XML... Gerando PDF..."                                │
│                                                                     │
│  ESTADO CONCLUÍDO                                                   │
│  └── Preview do DANFE (opcional)                                    │
│  └── Botões de download disponíveis                                 │
│  └── "Nova NF-e" para reiniciar                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔗 Referências Técnicas

- [XML_TAGS_REFERENCE.md](../../docs/XML_TAGS_REFERENCE.md) - Documentação completa das tags
- [XML_STRUCTURE.md](../../docs/XML_STRUCTURE.md) - Estrutura do XML
- [Portal NF-e](https://www.nfe.fazenda.gov.br/) - Documentação oficial
- [Manual de Orientação do Contribuinte](https://www.nfe.fazenda.gov.br/portal/listaConteudo.aspx?tipoConteudo=BMPFMBoln3w=)

---

## 📋 Checklist de Implementação

- [ ] Criar componente de formulário com seções colapsáveis
- [ ] Implementar tabela dinâmica de produtos
- [ ] Adicionar cálculos automáticos de impostos
- [ ] Implementar geração da chave de acesso
- [ ] Criar validações de campos (CNPJ, datas, valores)
- [ ] Adicionar autocomplete para NCM e CFOP
- [ ] Implementar checkbox de protocolo com campos condicionais
- [ ] Criar gerador de XML com template
- [ ] Integrar com DANFEGenerator para PDF
- [ ] Adicionar opções de download (XML, PDF, ZIP)
- [ ] Implementar salvamento de perfis de emitente
- [ ] Adicionar histórico de destinatários

---

**DANFE Generator** - Especificação UX/UI da Versão Web
