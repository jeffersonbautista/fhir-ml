docker stop python_sepsis_ml;
docker rm python_sepsis_ml;
docker build -t "python_sepsis_ml" . ;
docker run -d -p 5656:5656  --name="python_sepsis_ml" python_sepsis_ml 
