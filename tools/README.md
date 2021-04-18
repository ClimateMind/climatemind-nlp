# Deploying instances of Prodigy
This assumes you have a Dockerfile ready to go with data configured

0. Configure `prodigy.json` & ensure DB resources are allocated
1. `docker build -t <tag_name> <dockerfile>`
2. Test & run the image locally
3. Push the image to the container registery `docker push -t <tag_name>`
4. Create the Azure WebApp instance & have it pull the image from the container registery
5. Go to your Azure WebApp -> Settings -> Configuration -> Application Settings -> New Application Settings. Add a new variable Name: `WEBSITES_PORT` with Value set to whatever port Prodigy is on
