include .env.docker

# ============================================
# CONFIGURATION
# ============================================
IMAGE_NAME = lapelarating:1.3.5
APP_CONTAINER = lapela-container
DB_CONTAINER = postgres-db
PG_NAME = $(DB_NAME)
PG_USER = $(DB_USER)
NETWORK = web
DOMAIN = lapelarating.ru

# ============================================
# DOCKER COMMANDS
# ============================================

# Создать образ приложения
create:
	docker build -t $(IMAGE_NAME) .

# Удалить образ приложения
deli:
	docker rmi $(IMAGE_NAME)

# Запустить приложение с Traefik
runapp:
	docker run -d \
    --network $(NETWORK) \
    --restart unless-stopped \
    --env-file .env.docker \
    --name $(APP_CONTAINER) \
    --label "traefik.enable=true" \
    --label "traefik.http.routers.$(APP_CONTAINER).rule=Host(\`$(DOMAIN)\`)" \
    --label "traefik.http.routers.$(APP_CONTAINER).entrypoints=websecure" \
    --label "traefik.http.routers.$(APP_CONTAINER).tls.certresolver=letsencrypt" \
    --label "traefik.http.routers.$(APP_CONTAINER).service=$(APP_CONTAINER)-service" \
    --label "traefik.http.services.$(APP_CONTAINER)-service.loadbalancer.server.port=8000" \
    --label "traefik.http.routers.$(APP_CONTAINER)-api.rule=Host(\`$(DOMAIN)\`) && PathPrefix(\`/api\`)" \
    --label "traefik.http.routers.$(APP_CONTAINER)-api.entrypoints=websecure" \
    --label "traefik.http.routers.$(APP_CONTAINER)-api.tls.certresolver=letsencrypt" \
  	$(IMAGE_NAME)

# Запустить базу данных
rundb:
	docker run -d \
    --name $(DB_CONTAINER) \
    --network $(NETWORK) \
    --restart unless-stopped \
    --env-file .env.docker \
    --volume pg_rating_data:/var/lib/postgresql/data \
    postgres:17

backup:
	docker exec -t $(DB_CONTAINER) pg_dump -U $(PG_USER) $(PG_NAME) > \
	~/sites/lapelarating/backups/$(PG_NAME)_$$(date +%Y%m%d_%H%M%S).sql


# Показать логи приложения
logs:
	docker logs $(APP_CONTAINER)

# Проверить текущую миграцию
current:
	docker exec $(APP_CONTAINER) alembic current

# Выполнить миграции
migrate:
	docker exec $(APP_CONTAINER) alembic upgrade head

# Удалить приложение
delapp:
	docker rm -f $(APP_CONTAINER)


# ============================================
# TRAEFIK COMMANDS
# ============================================

# Запустить Traefik
runtraefik:
	cd ~/traefik/ && docker compose -f docker-compose.yml up -d

# Остановить Traefik
stoptraefik:
	cd ~/traefik/ && docker compose -f docker-compose.yml down

# Перезапустить Traefik
restarttraefik: stoptraefik runtraefik

# Показать логи Traefik
logstraefik:
	docker logs traefik


# ============================================
# TESTS
# ============================================

all_test:
	pytest -v -s

unit_test:
	pytest test/unit_test/ -v

integration_test:
	pytest test/integration_test/ -v



# ============================================
# UTILITY COMMANDS
# ============================================

# Проверить контейнеры
ps:
	docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Проверить сеть
networks:
	docker network inspect $(NETWORK)

# Проверить SSL сертификат
checkssl:
	@echo "Проверка SSL для $(DOMAIN)..."
	@echo | openssl s_client -connect $(DOMAIN):443 -servername $(DOMAIN) 2>/dev/null | openssl x509 -noout -dates || echo "SSL не настроен"


# Показать help
help:
	@echo "Доступные команды:"
	@echo ""
	@echo "=== Основные команды ==="
	@echo "make create        - Собрать образ приложения"
	@echo "make runapp        - Запустить приложение с Traefik"
	@echo "make rundb         - Запустить PostgreSQL"
	@echo "make runall        - Запустить всё"
	@echo ""
	@echo "=== Traefik ==="
	@echo "make runtraefik    - Запустить Traefik"
	@echo "make stoptraefik   - Остановить Traefik"
	@echo "make logstraefik   - Показать логи Traefik"
	@echo "make restarttraefik   - Перезапустить Traefik"
	@echo ""
	@echo "=== Утилиты ==="
	@echo "make ps            - Показать контейнеры"
	@echo "make logs          - Показать логи приложения"
	@echo "make migrate       - Выполнить миграции БД"
	@echo "make checkssl      - Проверить SSL сертификат"

# ============================================
# CUSTOMER PREVIEW MODE
# ============================================
CUSTOMER_CONTAINER = lapela-customer
CUSTOMER_DB = lapelarating_customer

# Собрать preview образ
build-preview:
	docker build -t lapelarating:preview .

copy-db:
	docker exec $(DB_CONTAINER) psql -U $(DB_USER) -d postgres -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '$(DB_NAME)';"
	docker exec $(DB_CONTAINER) psql -U $(DB_USER) -d postgres -c "DROP DATABASE IF EXISTS $(CUSTOMER_DB);"
	docker exec $(DB_CONTAINER) psql -U $(DB_USER) -d postgres -c "CREATE DATABASE $(CUSTOMER_DB) WITH TEMPLATE $(DB_NAME);"
	@echo "✅ Копия БД $(CUSTOMER_DB) создана"

run-customer:
	docker run -d \
		--name $(CUSTOMER_CONTAINER) \
		--network $(NETWORK) \
		--restart unless-stopped \
		--env-file .env.customer \
		--label "traefik.enable=true" \
		--label "traefik.http.routers.$(CUSTOMER_CONTAINER).rule=Host(\`preview.$(DOMAIN)\`)" \
		--label "traefik.http.routers.$(CUSTOMER_CONTAINER).entrypoints=websecure" \
		--label "traefik.http.routers.$(CUSTOMER_CONTAINER).tls.certresolver=letsencrypt" \
		--label "traefik.http.services.$(CUSTOMER_CONTAINER).loadbalancer.server.port=8000" \
		lapelarating:preview
	@echo "✅ Контейнер $(CUSTOMER_CONTAINER) запущен"

stop-customer:
	docker rm -f $(CUSTOMER_CONTAINER) 2>/dev/null || true

preview: copy-db run-customer
	@echo "========================================="
	@echo "✅ Preview версия запущена:"
	@echo "   https://preview.$(DOMAIN)"
	@echo "   База: $(CUSTOMER_DB)"
	@echo "========================================="

# Обновить код без пересоздания БД
update-preview: build-preview stop-customer run-customer
	docker exec $(CUSTOMER_CONTAINER) alembic upgrade head
	@echo "========================================="
	@echo "✅ Код обновлён, БД осталась прежней"
	@echo "   https://preview.$(DOMAIN)"
	@echo "========================================="