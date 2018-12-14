# LearnPythonGDAL
Learn Python And GDAL!
>考虑到机器学习及人工智能相关算法在Python3.x版本上支持更好，因此在图纸智能识别和设计项目中，使用了Python3.7。目前业界比较通用的做法是使用GDAL这个开源库来对建筑图纸的数据读写及处理。然而对于GDAL的支持大多使用Python2.7.x的版本，Python3.x的资料相对较少。
# 一、Python3.x的安装
从[Python官网](https://www.python.org/ "Python官网")下载适合你电脑的版本，然后进行安装。安装完成之后打开Python3.7 
# 二、Python3.x下GDAL的配置
Python下配置GDAL实际上可以分两大部分：  

- 一部分是“Core”的配置。Core是GDAL的公有DLL库，所有语言都会调用这些DLL实现功能。  
- 另一部分是“Binding”的配置。Binding则相当于是这些库的Python打包接口，以便Python可以调用。  

在Python下配置GDAL主要有两种办法：一种是下载源码进行编译；另一种是使用第三方的编译包，比如[gisinternals](https://www.gisinternals.com)所提供的安装包  
### 1、通过源码编译配置python环境
- “Core”的配置  

将编译生成的DLL文件所在目录添加至环境变量Path。同时，添加GDAL_DATA环境变量，如下图  
![Alt text](https://github.com/joyerf/LearnPythonGDAL/blob/master/asset/gdal_data_env.png)  

- “Binding”的配置  

<kbd>Win+R</kbd>，并输入cmd，操作如下：  
CD至定位到swig\python目录后，以此输入下面两个命令  

    python setup.py build  
    python setup.py install
    
执行完上述命令后，会在python的site-packages目录看到多了gdal和ogr的文件以及一个osgeo的文件夹。
### 2、使用第三方安装包配置
第三方安装包可以使用<http://www.gisinternals.com/>提供的安装包安装和whl文件安装。
#### 2.1、安装包安装
根据自己的电脑环境选择合适的安装包。  
首先，在<https://www.gisinternals.com/release.php>页面根据Visual Studio版本和电脑位数选择。如[release-1911-x64-gdal-2-3-2-mapserver-7-2-1](https://www.gisinternals.com/query.html?content=filelist&file=release-1911-x64-gdal-2-3-2-mapserver-7-2-1.zip)，表示MSVC 2017和x64。  
其次，选择后会跳转到一个页面，选择下载对应的Core安装包和Binding安装包(对应Python的版本)。比如[gdal-203-1911-x64-core.msi](http://download.gisinternals.com/sdk/downloads/release-1911-x64-gdal-2-3-2-mapserver-7-2-1/gdal-203-1911-x64-core.msi)和[GDAL-2.3.2.win-amd64-py3.7.msi](http://download.gisinternals.com/sdk/downloads/release-1911-x64-gdal-2-3-2-mapserver-7-2-1/GDAL-2.3.2.win-amd64-py3.7.msi)
最后，依次安装Core安装包和Binding安装包。
完成后打开Python的包目录，可以发现已经多了如下文件，这就是我们在Python下调用GDAL需要用到的文件了。  
![Alt text](https://github.com/joyerf/LearnPythonGDAL/blob/master/asset/gdal_dir.png)  
#### 2.2、pip安装whl文件
1. 从<https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal>网站，根据python版本下载相应的GDAL安装文件。  
比如Python3.7下载[GDAL‑2.3.2‑cp37‑cp37m‑win\_amd64.whl](https://download.lfd.uci.edu/pythonlibs/h2ufg7oq/GDAL-2.3.2-cp37-cp37m-win_amd64.whl)    
2. 下载完成后，打开命令提示符输入下面命令，即可安装GDAL。  
````
    pip install GDAL‑2.3.2‑cp37‑cp37m‑win_amd64.whl
````
#### Anaconda安装gdal
使用 Anaconda 管理 Python 的包非常方便，大部分的 Python 包都可以通过 Anaconda 进行安装，GDAL也不例外。可以采用如下命令进行安装：
````
    conda install gdal 
````
### 3、检验是否安装成功
![Alt text](https://github.com/joyerf/LearnPythonGDAL/blob/master/asset/gadl_version.png)  