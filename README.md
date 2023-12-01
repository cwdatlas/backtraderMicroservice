backtraderMicroservice
This includes a microservice that is intended to be pared with the midas web app (one of my other projects). it can produce proformance data on past stock data given an algorithm (included in the app)

Dependencies:
Podman or Docker:
download and install podman or docker. These two container engines have almost identical commands, so change the word podman to docker in my commands if you are using docker. I am using podman, so that is what I would recomend to have the best results. 
Podman:
Official Instructions for Mac and Windows: https://podman.io/docs/installation

Docker: 
Install on MAC: https://docs.docker.com/desktop/install/mac-install/
Windows: https://docs.docker.com/desktop/install/windows-install/
Linux: https://docs.docker.com/desktop/install/linux-install/

I recomend to use postman to send requests to the microservice. Here is an example of the body of a post to this app.
localhost:5000/optimize
{
    "start_date": "2010-01-01",
    "end_date": "2010-03-01",
    "stock_ticker": "UEC",
    "algorithm": "EmaSmaCross",
    "commission": ".01",
    "stake": "100",
    "start_sma": "20",
    "end_sma": "40",
    "start_ema": "20",
    "end_ema": "40"

}
You can also use curl if you would like. 

After podman or docker is installed, use the commands in your terminal after the podman engine is running(use the container engine's name that you are using in the command:
podman pull madatlas/midasbacktrader:1.0

After you have the container, you can use this command to launch it. 
podman run --detach --name midas-backtrader -p 5000:8080 midasbacktrader:1.0

Its running now, so you can send it requests. have fun!


