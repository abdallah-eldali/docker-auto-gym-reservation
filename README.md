## Explanation

This web-bot uses Selenium to automatically reserve a spot at the gym in Richcraft's Recreational Complex in Kanata once registration opens.

The script is packaged by in a Docker image by installing the necessary browser drivers for Selenium to function, as well as a list of Python module dependencies `requirement.txt`, and later be pushed to a private Docker repository to later be executed on an Azure virtual machine.

Once the gym spot is reserverd (or an error occurs), the script will store all of the information in a log file in the VM using Docker's Volume to store persistent data outside of the container. The script will also send a message through Whatsapp using the Twilio API.

**This script is no longer functional, as the registration website doesn't exist anymore.**

## Things I would've liked to add:

The next step for this project would've been to add a CI/CD pipeline (I was between using GitHub's Actiona pipeline or Jenkins), so that it automated the deployment of the container to the remote VM instead of doing it manually, tasks like:
* Creating the Docker image every time I added a new change
* Having to push said image to DockerHub
* Having to login into the VM (through SSH) and manually pull the image and create a container for it

These steps could've been easly automated through a pipeline. I also had experience writing pipeline scripts through my internships as DevOps