1. git clone  
2. cd debate   
3. python3 -m venv .venv  
4. . .venv/bin/activate  
5. pip install -r requirements.txt  
6. pip install numpy==1.22

---
on mac  
brew update  
brew install ffmpeg  
soundfile error!!!

https://github.com/ohmtech-rdi/eurorack-blocks/issues/444

brew install libsndfile
brew list libsndfile

manual cp : /opt/homebrew/Cellar/libsndfile/1.2.2/lib --> .venv/lib/python3.10/site-packages/_soundfile_data
