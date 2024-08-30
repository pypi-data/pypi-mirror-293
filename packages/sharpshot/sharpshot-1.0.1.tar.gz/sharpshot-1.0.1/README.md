## 精准测试
![SharpShot](https://github.com/openutx/sharpshot/blob/main/images/logo100x100.png)
### SharpShot 
一个专注于精准测试的工具，旨在提供一套强大而灵活的工具集，帮助开发人员和测试人员进行精细化、全面化的测试。该工具集结合了高效的测试技术和先进的分析功能，使用户能够快速、准确地识别和解决软件系统中的问题。

### 介绍

分析 java 项目的两次 git 提交差异对项目的影响，精准定位受影响的接口 并生成调用链数据。

### 实现效果
![效果图](https://github.com/openutx/sharpshot/blob/main/images/img.png)

### 原理
1. 通过代码改动定位代码影响，并不断遍历受影响的类和方法直至找到最上层的controller层
2. 通过javalang语法解析获取每个Java文件的import class extends implements declarators methods 等信息
3. 通过unidiff 解析git diff信息（diff file, added_line_num, removed_lin_num)
4. 然后根据文件增删的代码行去判断影响了哪些类和方法，不断遍历受影响的类和方法直至找到最上层的controller层
5. 分析出两次commit id之间代码改动所带来的影响，输出受影响的接口 并生成调用链路图。

### 环境部署
>要求python >= 3.9
    
```shell
pip install sharpshot
```
### 使用说明
1. 首先获取 gitlab 的 access_token
>https://git.openutx.com/-/profile/personal_access_tokens
2. 运行
```shell
sharpshot pr=https://git.openutx.com/utx/utx-im/-/merge_requests/370 username=utxuser access_token=xxxx
```
>pr 为 merge request 的地址，username 为 gitlab 用户名，access_token 为 gitlab 的 access_token
