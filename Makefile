#!make

include .env
COMPOSE = docker compose

build:
	${COMPOSE} build

start:
	${COMPOSE} start

stop:
	${COMPOSE} stop

up:
	${COMPOSE} up --build -d

down:
	${COMPOSE} down

restart:
	${COMPOSE} down
	${COMPOSE} up -d