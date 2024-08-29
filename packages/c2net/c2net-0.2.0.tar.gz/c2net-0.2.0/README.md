# C2NET-BETA

> PYPI package for c2net-beta

# 使用说明安装

- 虎鲸平台提供使用代码，数据集，模型示例

## 安装

*适配python3.6及以上版本*

> PYPI package for C2NET-BETA。

```bash
pip3 install -U c2net
或
pip3 install c2net==版本号 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 云脑资源初始化与上传，获取路径示例：

```
#导入包
from c2net.context import prepare, upload_output

#初始化导入数据集和预训练模型到容器内
c2net_context = prepare()

#获取代码路径, 数据集路径，预训练模型路径，输出路径
code_path = c2net_context.code_path
dataset_path = c2net_context.dataset_path
pretrain_model_path = c2net_context.pretrain_model_path
you_must_save_here = c2net_context.output_path

#回传结果到c2net
upload_output()
```

## 在启智平台上的[使用示例](https://openi.pcl.ac.cn/OpenIOSSG/OpenI_Cloudbrain_Example)
