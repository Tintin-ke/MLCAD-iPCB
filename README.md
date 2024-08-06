# MLCAD-iPCB
for artifact evaluation
## Deployment environment steps

```
pip install PyQt5
pip install opencv-python
pip install PyQt-Fluent-Widgets -i https://pypi.org/simple/
pip install pandas
conda install paddlepaddle==2.4.0 --channel https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/Paddle/
pip install "paddleocr>=2.0.1"
pip install Polygon3 -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install lanms-neo
pip install paddlex -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install filelock
pip install xlrd
pip install protobuf==3.19.0
pip install Levenshtein
```

## Using requirements.txt to import the environment, you can try
```
pip install -r requirements.txt
```
or
```
conda install --yes --file requirements.txt 
```

## Using environment.yaml to import the environment, you can try
```
conda env create -f environment.yaml
```

## Direct download of environment
There may be various problems when installing the environment, so I packed my local environment and put it on OneDrive. If there are problems during installation, you can download the compressed package directly from OneDrive.
Unzip the environment package into a new folder and configure the python interpreter as "python.exe" in the folder in PyCharm.
The OneDrive website is as follows:
https://1drv.ms/u/s!Ash-dyUui6GwkFas0cbdtAnjJ5BU?e=VxWlw7

## Directory structure description
    ├── README.md           // Help documentation
    
    ├── function             // Folder to store functions
    
    ├── image             // Folder for input images
    
    ├── new_ui            // ui file
    
    ├── PaddleOCR            
    
    │   ├── output     // trained text detection model
    
    │   └── __init__.py
    
    ├── PaddleX            // trained Text Orientation Classifier model
    
    ├── result            // Folder to save results
    
    └── Schematic_design                // Draw schematic

The platform for running the code is pycharm

Run the demo.py file under new_ui
