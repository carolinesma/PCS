# Huffman Distribution Matching

## Passo a passo para instalação e uso

### 1. Clone o repositório

```bash
git clone git@github.com:carolinesma/PCS.git
cd PCS
```

### 2. Instale o submódulo Huffman_DM

```bash
git submodule add git@github.com:andrademicael/Huffman_DM.git
# Ou, se já existe como submódulo, apenas inicialize e atualize:
git submodule update --init --recursive
```

### 3. Instale o pacote em modo editável

Recomenda-se o uso de um ambiente virtual (venv, conda, etc).

```bash
pip install -e .
```

