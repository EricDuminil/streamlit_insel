#######################################################################
#                            Main targets                             #
#######################################################################

## Simple example tasks for StreamLit + INSEL

help:     ## Show this help.
	@egrep -h '(\s##\s|^##\s)' $(MAKEFILE_LIST) | egrep -v '^--' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[32m  %-35s\033[0m %s\n", $$1, $$2}'

build:   ## Build containers.
	@echo "${green}Create app${no_color}"
	docker compose build

up: ## Start containers.
	@echo "${green}Start container${no_color}"
	docker compose up --detach

watch: up ## Start containers and watch any change. Convenient for development.
	@echo "${green}Start and watch container${no_color}"
	docker compose watch --no-up

down:   ## Stop containers and discard them.
	@echo "${green}Stop container${no_color}"
	docker compose down

shell: ## Start shell.
	@echo "${green}Start shell interactive console${no_color}"
	docker compose run --rm web bash

status: ## Show current status.
	@docker compose ps --all | \
		sed "s/\b\(exited\)\b/${orange}\U\1\E${no_color}/gi" | \
		sed "s/\b\(up\)\b/${green}\U\1\E${no_color}/gi" | \
		sed "s/\b\(healthy\)\b/${green}\U\1\E${no_color}/gi" | \
		sed "s/\b\(unhealthy\)\b/${orange}\U\1\E${no_color}/gi" | tee /tmp/status
	@(grep -qi "UP" /tmp/status && echo "${green}UP!${no_color}") || echo "${red}DOWN!${no_color}"

logs: ## Show logs
	@echo "${green}Show logs${no_color}"
	docker compose logs --follow

update: ## Update images
	@echo "${orange}Update images${no_color}"
	git pull


green=`tput setaf 2`
orange=`tput setaf 9`
red=`tput setaf 1`
no_color=`tput sgr0`
