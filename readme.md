### URL Shortening Service 


*Note: Run Docker engine before running the following commands:*

###### Docker commands

###### Week 1 
```
docker build -t url-shortener .
docker run -p 5000:5000 url-shortener
```

###### Week 2
```
./minikube-cleanup.sh
./minikube-deploy.sh
```

- To test the api calls
```python3 test.py``` in a different terminal.


###### Week 3

```
./minikube-cleanup.sh
./minikube-deploy.sh
```

- For stress testing:
    run `hey -n 1000 -c 50 $url`
(the url is where the program is running on.)
