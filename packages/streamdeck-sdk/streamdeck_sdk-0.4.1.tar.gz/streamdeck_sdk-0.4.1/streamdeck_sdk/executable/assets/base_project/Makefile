PLUGIN_NAME=com.bestdeveloper.mytestplugin.sdPlugin
PLUGIN_DIR_PATH=$(PLUGIN_NAME)
PLUGIN_CODE_DIR_PATH=$(PLUGIN_DIR_PATH)/code
PLUGIN_CODE_VENV_DIR_PATH=$(PLUGIN_CODE_DIR_PATH)/venv
PLUGIN_LOGS_DIR_PATH=${PLUGIN_DIR_PATH}/logs
REQUIREMENTS_PATH=$(PLUGIN_DIR_PATH)/code/requirements.txt

PATH_TO_VENV=./venv
PATH_TO_VENV_ACTIVATE=$(PATH_TO_VENV)/bin/activate

_create_venv_in_project_root:
	# Создать виртуальное окружение в корне проекта
	python3 -m venv "$(PATH_TO_VENV)"

install_requirements_in_venv:
	# Установить зависимости из requirements.txt в venv, находящийся вне кода плагина
	source "$(PATH_TO_VENV_ACTIVATE)" && \
    python3 -m pip install --upgrade pip  && \
    python3 -m pip install -r "$(REQUIREMENTS_PATH)"

init: _create_venv_in_project_root install_requirements_in_venv
	# Создать виртуальное окружение в корне проекта и установить зависимости.

upgrade_requirements:
	# Обновить зависимости на основе requirements.txt
	source "$(PATH_TO_VENV_ACTIVATE)" && \
	pip install -r "$(REQUIREMENTS_PATH)" --upgrade

freeze_requirements_to_plugin:
	# Выгрузить установленные зависимости в requirements.txt
	source "$(PATH_TO_VENV_ACTIVATE)" && \
	pip freeze > "$(REQUIREMENTS_PATH)"

_clean_pycache:
	# Очистить кэш python
	./clean_pycache.sh

_distribution_tool_automate:
	# Собирать проект в текущую директорию
	./DistributionTool -b -i "$(PLUGIN_DIR_PATH)" -o .

_rm_code_venv:
	# Очистить venv плагина
	rm -rf "$(PLUGIN_CODE_VENV_DIR_PATH)"

_rm_logs_dir:
	# Очистить папку с логами
	rm -rf "$(PLUGIN_LOGS_DIR_PATH)"

export_plugin: _rm_code_venv _rm_logs_dir _clean_pycache _distribution_tool_automate
	# Очистить плагин от мусора и собрать дистрибутив плагина
