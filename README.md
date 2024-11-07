docker network create mainNetwork

docker run --name cars_rent_db \
    -p 6432:5432 \
    -e POSTGRES_USER=admin \
    -e POSTGRES_PASSWORD=yZRGqu7j115@ \
    -e POSTGRES_DB=cars_rent \
    --network=mainNetwork \
    --volume pg-cars-rent-data:/var/lib/postgresql/data \
    -d postgres:16

docker run --name cars_rent_cache \
    -p 7379:6379 \
    --network mainNetwork \
    -d redis:7.4

docker run --name cars_rent_back `
    -p 7777:8000 `
    --network mainNetwork `
    car_rent_image

docker run --name cars_rent_celery_worker `
    --network mainNetwork `
    car_rent_image `
    celery --app=app.tasks.celery_app:celery_instance worker -l INFO

docker run --name cars_rent_celery_beat `
    --network mainNetwork `
    car_rent_image `
    celery --app=app.tasks.celery_app:celery_instance beat -l INFO