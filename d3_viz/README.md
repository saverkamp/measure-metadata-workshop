These folders are the source material for the examples we will be using today. 

To make them work you need to run a mini-webserver on your system to server the files to your web browser.

Luckily python has one built in!

Try (for python 2.7)
```
  cd measure-metadata-workshop/d3_viz
  python -m SimpleHTTPServer 8000
```

Or (for python 3+)
```
  cd measure-metadata-workshop/d3_viz
  python3 -m http.server
```

And then visit [http://localhost:8000/](http://localhost:8000/) in your web browser.
