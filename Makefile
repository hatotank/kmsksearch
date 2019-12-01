NAME=kmsksearch

run:
	docker-compose build
	docker-compose up -d

start:
	docker start ${NAME}_uwsgi_1 ${NAME}_nginx_1 ${NAME}_groonga_1 

stop:
	docker stop ${NAME}_uwsgi_1 ${NAME}_nginx_1 ${NAME}_groonga_1

stoprm:
	docker stop ${NAME}_uwsgi_1 ${NAME}_nginx_1 ${NAME}_groonga_1
	docker rm ${NAME}_uwsgi_1 ${NAME}_nginx_1 ${NAME}_groonga_1
