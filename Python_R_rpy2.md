# 配置
1. 安装R
######可以去网上搜索安装包直接安装。将R的路径放到系统环境，就可以在cmd中输入R来检验R安装是否成功。
![系统环境](https://upload-images.jianshu.io/upload_images/8605744-42a6a1aeac391864.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

2. 安装rpy2
######作者直接pip install rpy2出错
- 如果安装了anoconda或者miniconda，可以使用conda install rpy2直接安装rpy2（会自动选择合适的rpy2版本）。
- 如果直接安装的python，可以去网上下载rpy2的安装包离线安装。
3. 配置
######为了让python识别到R的安装地址，需要配置两个路径。
- R_HOME；R_USER
![系统变量](https://upload-images.jianshu.io/upload_images/8605744-ad24693219f5d10f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
- 建议：设置好以后重启一下
4. notebook的使用
######在配置好以后就可以直接在python中调用R了，例如：
```
from rpy2.robjects import r as Rcode
from rpy2.robjects.packages import importr as Rrequire
Rrequire('ggplot2') # 导入R包
print(Rcode("pi")) # 运行R语句
# [1] 3.141593
```
######但是这么用有一些不方便，R很多时候需要一步步地运行来看变量或数据集的变化，此外Python调用的R与直接用R写代码时会有些许不同。使用notebook来解决这个问题，anoconda集成了notebook，以下的操作都在anoconda环境下的notebook中运行的。
(如果只是调用R中的几个函数，以下可忽略)
![python调用R](https://upload-images.jianshu.io/upload_images/8605744-b3db8c87eb91d8cb.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
######上图实现的过程中需要注意以下几点：
- -i表示input，有时候还会用到-o，表示output。
-  注意在这里R中的library用不了，用require。
- 直接运行load_ext rpy2.ipython大概率会因为缺少一些包出错，**缺什么补什么**。
- %%R指的是调用%R，直接%R调用不了ggplot2。
######以下再给出一个调用R的例子，注意这里调用的%R调用的是R的基础包
![python调用R](https://upload-images.jianshu.io/upload_images/8605744-8b96028e96791df6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
###### 附1：
- notebook中的语法提示，cmd中安装nbextensions，代码如下（以下代码在anoconda环境下可以运行）：
```
pip install jupyter_contrib_nbextensions
jupyter contrib nbextension install --user
pip install --user jupyter_nbextensions_configurator
jupyter nbextensions_configurator enable --user
```
- 重启后在nbextensions中勾选Hinterland

###### 附2：
- R运行python可参考R的包reticulate，作者用不上，没有进一步研究。
