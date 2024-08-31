PYTHON = python

FILE = account.json
PASSWORD = abc
SOURCE = arbitrum-USDC
# Wallet to withdraw funds to
WALLET = 0xAAE1887BDed35e9fcC2f0bb6229DE479b91FD00c

INSTALL_DIR = dist

# Set to any non-empty value to turn on performance profiling
PROFILE =
PROFILE_OUTPUT = perf.out

# Don't touch these
PROFILE_ARGS = $(if $(PROFILE),cProfile -o $(PROFILE_OUTPUT),)
EXEC = ${PYTHON} -m ${PROFILE_ARGS} src.mach_cctt

.PHONY: init
init: pyproject.toml
	${PYTHON} -m pip install -e .

.PHONY: help
help:
	${EXEC} \
		--help

.PHONY: generate
generate:
	${EXEC} \
		generate \
		--file ${FILE} \
		--password ${PASSWORD}

.PHONY: import
import:
	${EXEC} \
		import \
		--file ${FILE} \
		--password ${PASSWORD} \
		--private-key ${PRIVATE_KEY}

.PHONY: decrypt
decrypt: ${FILE}
	${EXEC} \
		decrypt \
		--file ${FILE} \
		--password ${PASSWORD}

.PHONY: run
run: ${FILE}
	${EXEC} \
		run \
		--file ${FILE} \
		--password ${PASSWORD} \
		--source ${SOURCE}

.PHONY: withdraw
withdraw: ${FILE}
	${EXEC} \
		withdraw \
		--file ${FILE} \
		--password ${PASSWORD} \
		--wallet ${WALLET}

.PHONY: build
build:
	${PYTHON} -m build

.PHONY: upload-test
upload-test:
	${PYTHON} -m twine upload --repository testpypi dist/*

.PHONY: upload
upload:
	${PYTHON} -m twine upload dist/*

# Single file executable installation
.PHONY: install
install:
	mkdir -p ${INSTALL_DIR}
	pyinstaller \
		main.py \
		--onefile  \
		--distpath ${INSTALL_DIR} \
		-n cctt

.PHONY: perf
perf:
	${PYTHON} -m pstats ${PROFILE_OUTPUT}

.PHONY: clean
clean:
	rm -rf ${INSTALL_DIR}/cctt build/ cctt.spec ${PROFILE_OUTPUT}
