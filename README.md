# Octree
Generator siatek prostopadłościennych z wykorzystaniem drzewa ósemkowego

## Jak to działa?
### Konfiguracja środowiska
```
$ git clone https://github.com/monika-osiak/octree.git
$ cd octree
$ pip install virtualenv
$ virtualenv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```
### Przykład z kostką
```
(venv) $ python main.py --config config/cube.ini
```
### Przykład z donutem
```
(venv) $ python main.py --config config/element.ini
```
### Przykład z liskiem
```
(venv) $ python main.py --config config/fox.ini
```
