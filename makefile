create:
	docker build -t lapelarating:1.0 .

deli:
	docker rmi lapelarating:1.0


runapp:
	docker run -d \
    -p 8000:8000 \
    --network web \
    --env-file .env \
    --name lapela-container \
  	lapelarating:1.0

rundb:
	docker run -d   --name postgres-db \
    --network web \
    -p 6432:5432 \
    -e POSTGRES_PASSWORD=postgre \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_DB=rating \
    --volume pg_rating_data:/var/lib/postgresql/data \
    postgres:17

logs:
	docker logs lapela-container

current:
	docker exec lapela-container alembic current

migrate:
	docker exec lapela-container alembic upgrade head


delapp:
	docker rm -f lapela-container

deldb:
	docker rm -f postgres-db



