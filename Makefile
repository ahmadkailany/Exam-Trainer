# **************************************************************************** #
#                                                                              #
#   Exam Trainer v1.0.0 - made by Ahmad Kailany for 42 Students                #
#                                                                              #
#   make            install (first time) + start the examshell                 #
#   make grademe    grade your current exercise                                #
#   make help       all the commands                                           #
#                                                                              #
# **************************************************************************** #

NAME     := Exam Trainer
VERSION  := 1.0.0
VENV     := .venv
REQ      := requirements.txt
STAMP    := $(VENV)/.installed

ifeq ($(OS),Windows_NT)
    PYTHON  ?= python
    VENV_PY := $(VENV)/Scripts/python.exe
else
    PYTHON  ?= python3
    VENV_PY := $(VENV)/bin/python
endif

# The examshell itself never needs the venv bootstrap when started from here.
RUN := $(VENV_PY) examshell.py

# Portable helpers (work with sh or cmd.exe as the make shell)
RMTREE = $(PYTHON) -c "import shutil,sys; [shutil.rmtree(p, ignore_errors=True) for p in sys.argv[1:]]"
RMPYC  = $(PYTHON) -c "import os,shutil; [shutil.rmtree(os.path.join(r,'__pycache__')) for r,d,f in os.walk('.') if '__pycache__' in d and '.venv' not in r]"
RMFILE = $(PYTHON) -c "import os,sys; [os.remove(p) for p in sys.argv[1:] if os.path.isfile(p)]"

.DEFAULT_GOAL := run
.PHONY: all run install grademe status subject version clean fclean re help

all: run

## run        : install if needed, then start the examshell (default)
run: $(STAMP)
	@$(RUN)

## install    : create .venv and install the requirements
install: $(STAMP)
	@echo "[$(NAME)] ready - run: make"

$(STAMP): $(REQ)
	@echo "[$(NAME)] creating virtual environment in $(VENV) ..."
	@$(PYTHON) -m venv $(VENV)
	@echo "[$(NAME)] installing dependencies ..."
	@$(VENV_PY) -m pip install --disable-pip-version-check -q -r $(REQ)
	@$(VENV_PY) -c "open(r'$(STAMP)', 'w').close()"
	@echo "[$(NAME)] installation complete"

## grademe    : grade the current exercise (from any terminal)
grademe: $(STAMP)
	@$(RUN) grademe

## status     : level, score, timer and history of the current exam
status: $(STAMP)
	@$(RUN) status

## subject    : print the current subject
subject: $(STAMP)
	@$(RUN) subject

## version    : print the version
version:
	@echo "$(NAME) v$(VERSION) - made by Ahmad Kailany for 42 Students"

## clean      : remove traces, the subject copy and Python caches
clean:
	@$(RMTREE) traces subject
	@$(RMPYC)
	@echo "[$(NAME)] cleaned"

## fclean     : clean + remove the venv and the saved exam progress (keeps grademe/)
fclean: clean
	@$(RMTREE) $(VENV)
	@$(RMFILE) .exam_state.json
	@echo "[$(NAME)] venv and progress removed"

## re         : fclean + install
re: fclean install

## help       : show this help
help:
	@echo "$(NAME) v$(VERSION) - made by Ahmad Kailany for 42 Students"
	@echo ""
	@echo "  make            install (first time) and start the examshell"
	@echo "  make install    create .venv and install the requirements"
	@echo "  make grademe    grade your current exercise"
	@echo "  make status     level, score, timer and history"
	@echo "  make subject    print the current subject"
	@echo "  make clean      remove traces, subject copy, caches"
	@echo "  make fclean     clean + remove .venv and saved progress"
	@echo "  make re         fclean + install"
	@echo "  make version    print the version"
