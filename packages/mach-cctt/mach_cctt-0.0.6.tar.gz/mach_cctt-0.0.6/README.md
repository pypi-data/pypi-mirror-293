# Cross Chain Trade Test

Test automated trades between multiple chains on Mach.

## Overview

Test automated trades on Mach. Specify a start chain and symbol, and a policy determining how the destination token will be chosen (randomize, randomize chain and fix symbol). In each trade, the test wallet's entire balance of the source token will be sold for the destination token, and then the destination token because the new source token for the next trade. This continues until the script is killed by the user.

## Files

- `run_script.py`: Main script to execute trades.
- `script_tx_handler.py`: Helper functions for building and sending transactions.
- `main.py`: Argument parsing and entrypoint
- `config.py`: Constants storing configuration data and URLs
- `requirements.txt`: List of dependencies.

## Usage

1. Install

    ```bash
    python -m pip install mach-cctt
    ```

1. Usage

    ```bash
    cctt --help
    ```

## Development

### Setup

1. **Clone the repository**

    ```bash
    git clone https://github.com/tristeroresearch/cross-chain-trade-test.git
    cd cross-chain-trade-test
    ```

1. **Create and activate a virtual environment**

    Using `venv`:

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

    Or using `pyenv`:

    ```bash
    pyenv virtualenv 3.12.5 cctt
    pyenv activate
    ```

1. **Install dependencies**

    ```bash
    make init
    ```

#### Upload to Test PyPI

```bash
make build upload-test
```

#### Upload to PyPI

```bash
make build upload
```

#### Install Single-File Executable

```bash
make install
```

This produces an executable called `cctt` under the `dist/` directory. In theory this executable can be copied and run on any system with the same architecture and OS.

## TODO

- Use type 2 (EIP 1559) txs
- Resolve duplication between transfers.py and transactions.py
- Logging
- Better way of sharing private key between modules
  - Place in config.py
  - Initialize in main.py
  - In each module that depends on it, at the top of the file run `assert config.initialized`
- Use Quote class from backend and deserialize with pydantic
- Unit tests
