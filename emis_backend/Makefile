# Использовать bash с опцией pipefail 
# pipefail - фейлит выполнение пайпа, если команда выполнилась с ошибкой
SHELL=/bin/bash -o pipefail

# Если переменная CI_JOB_ID не определена 
ifeq ($(CI_JOB_ID),)
    # присваиваем значение local
    CI_JOB_ID := local
endif

# Экспортируем переменную окружения
export COMPOSE_PROJECT_NAME = $(CI_JOB_ID)-testrail

# Останавливаем и удаляем контейнеры, сеть, volumes
docker-down:
	docker-compose down

# Предварительно выполняем docker-down (опционально)
docker-up: docker-down
    # Забираем последние образы из docker-registry
	# docker-compose -f docker-compose.yml pull
    # Запускаем окружение
    # force-recreate - принудительное пересоздание контейнеров
    # renew-anon-volumes - не использовать volumes предыдущих контейнеров
	# docker-compose -f docker-compose.yml up --force-recreate --renew-anon-volumes -d
	docker-compose up -d
    # Ну и, на всякий случай, вывести что там у нас в принципе запущено на машинке
	docker ps

# Коллектим логи сервисов
docker-logs:
	mkdir -p ./logs
	docker logs $${COMPOSE_PROJECT_NAME}_web_1       >& logs/testrail-web.log       || true
	docker logs $${COMPOSE_PROJECT_NAME}_fpm_1       >& logs/testrail-fpm.log       || true
	docker logs $${COMPOSE_PROJECT_NAME}_migration_1 >& logs/testrail-migration.log || true
	docker logs $${COMPOSE_PROJECT_NAME}_db_1        >& logs/testrail-mysql.log     || true

# Очистка раннера
docker-clean:
	@echo Останавливаем все testrail-контейнеры
	docker kill $$(docker ps --filter=name=testrail -q) || true
	@echo Очистка докер контейнеров
	docker rm -f $$(docker ps -a -f --filter=name=testrail status=exited -q) || true
	@echo Очистка dangling образов
	docker rmi -f $$(docker images -f "dangling=true" -q) || true
	@echo Очистка testrail образов
	docker rmi -f $$(docker images --filter=reference='registry.gitlab.com/touchbit/image/testrail/*' -q) || true
	@echo Очистка всех неиспользуемых volume
	docker volume rm -f $$(docker volume ls -q) || true
	@echo Очистка всех testrail сетей
	docker network rm $(docker network ls --filter=name=testrail -q) || true
	docker ps