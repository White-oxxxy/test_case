DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .dev.env
APP = docker_compose/app.yaml
INFRA = docker_compose/infra.yaml
MONITORING = docker_compose/monitoring.yaml

.PHONY: app
app:
	${DC} -f ${APP} ${ENV} up --build -d

.PHONY: app-down
app-down:
	${DC} -f ${APP} ${ENV} down

.PHONY: infra
infra:
	${DC} -f ${INFRA} ${ENV} up --build -d

.PHONY: infra-down
infra-down:
    ${DC} -f ${INFRA} ${ENV} down

.PHONY: monitoring
monitoring:
    ${DC} -f ${MONITORING} ${ENV} up --build -d

.PHONY: monitoring-down
monitoring-down:
    ${DC} -f ${MONITORING} ${ENV} down