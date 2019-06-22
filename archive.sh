docker-compose up --build
cp ./resize_operation.py ./deploy/dist/resize_operation.py
cd ./deploy/dist && zip -r9 ../../upload.zip ./* -x .gitignore
