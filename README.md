# ICBC IWork Computer Vision  

### How to set this up on a local computer  
git clone from `https://github.com/iwork-cs319/iwork-cv.git`
`cd iwork-cv`  
`pip install -r requirements.txt`  
## Installing Tesseract
**On a MAC**  
`brew install tesseract`  
**UBUNTU**  
`sudo apt update sudo apt install tesseract-ocr`  
## Installing Redis
**On a MAC**  
`brew install redis`  
**UBUNTU**  
`sudo apt-get install redis-server`  

### How to run on a local computer  
in the folder, run `python app.py`. This will boot up the backend.  
Then open a seperate tab in the terminal, and type `python worker.py`.  
The worker is needed to handle the tasks that take longer than 30 seconds.  

### How to run on Heroku
Heroku requires the following buildpacks  
1. https://github.com/heroku/heroku-buildpack-apt (APT has been deprecated and is no longer needed)
2. heroku/python
3. https://github.com/bayareacoder/heroku-buildpack-tesseract
The third buildpack handles installing tesseract version 4.1  
  
It also requires the Redis-To-Go Dyno  
  
Everything else is setup within the folder, so you just have to connect to the folder to a Heroku app and push. To do this, follow the instructions here!  
https://devcenter.heroku.com/articles/git
