# Django web server, backend, fronted, db hands on

---
django 3.2.10, 

db = postgresql 12.10

---

## Docker command

---
```
docker-compose build # build docker image
docker-compose up # run docker container
docker-compose exec web python manage.py migrate # migrate posgresql container

docker-compose exec web python manage.py createsuperuser # create superuser for django
```

db port : 5432 (you can find in ```.env.dev```)

---
## Set site

---
visit 127.0.0.1:8000/admin/sites/site/
Domain name : example.com -> 127.0.0.1:8000