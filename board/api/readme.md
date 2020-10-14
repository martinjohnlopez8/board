Setup

1. Must have docker setup in PC
2. change into project directory where the dockerfile resides
3. docker-compose build to build the service to run the docker-compose.yml
4. docker-compose up   to run the service
5. You can now access the api using http://localhost:8000

API Endpoints 
/api/register/
/api/login/
/api/follow/
/api/unfollow/
/api/profile/
/api/profile/update/
/api/ban/
/api/unban/
/api/lock-unlock/thread/
/api/create/board/
/api/create/thread/
/api/create/post/
/api/boards/
/api/post/:user_id/
/api/get/gravatar/