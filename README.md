# GinPlum
[![Build Status](https://app.travis-ci.com/lzqlzzq/GinPlum.svg?branch=main)](https://app.travis-ci.com/lzqlzzq/GinPlum) [![GitHub version](https://badge.fury.io/gh/lzqlzzq%2FGinPlum.svg)](https://badge.fury.io/gh/lzqlzzq%2FGinPlum) [![Coverage Status](https://coveralls.io/repos/github/lzqlzzq/GinPlum/badge.svg?branch=main)](https://coveralls.io/github/lzqlzzq/GinPlum?branch=main)

## 简介
GinPlum（译作“金瓶梅”）是一个轻量化的python的RESTful风格WEB后端框架，用于阿里云函数计算的HTTP函数。
GinPlum对HTTP函数提供的wsgi根据HTTP协议做了一些封装，便于开发RESTful风格的WEB后端服务。

> Gin Plum May是我在2021年5月调制出的一种鸡尾酒，彼时我恰好开始编码这个项目，其调制方法是：金酒与酸梅汤3:2混合，酌情加砂糖，加冰搅拌，用柯林杯盛装，投入小串乌梅装饰，并用盐镶边。

## 特点
- 轻量化：整个代码包大小不到10kb，避免函数计算代码包体积超限；
- 零依赖：没有引用任何的第三方库，避免依赖问题；
- 功能齐全：对函数提供的wsgi做了封装，可方便地使用请求中的信息与构造应答，让开发者专注于业务代码；
- 用法接近Flask：路由等用法与Flask相似，几乎完全支持Flask风格的stub code，从Flask迁移也较为容易。

## 运行环境
- 阿里云函数计算
- python 3.6
- http函数
- http触发器设在*index.handler()*上

## 安装
无需安装，开箱即用，只需将代码包上传到函数中即可。

## 使用
参照[api.py](https://github.com/lzqlzzq/GinPlum/blob/main/api.py)的示例代码，并添加、实现业务接口。

## 文件结构
.  
|----.travis.yml -------> travis-ci的配置文件，用于测试代码，**使用时可删除**  
|----api.py -------> 业务api代码，包含模板代码，应在这个模块内实现所有业务功能  
|----ginPlum.py -------> ginPlum主模块的代码  
|----index.py -------> 包含函数计算的触发器，用于接受wsgi传来的请求信息  
|----README.md -------> 说明文档，即这个文件，**使用时可删除**  
|----requestEntity.py -------> 请求处理模块，将wsgi传过来的请求进行结构化处理以便使用  
|----responseEntity.py -------> 应答处理模块，便于构建应答  
|----test.py -------> 测试代码，**使用时可删除**  
|----LICENSE -------> 许可协议，**使用时可删除**  
|----.gitignore -------> git忽略文件，**使用时可删除**  

## 许可协议
[MIT](https://github.com/lzqlzzq/GinPlum/blob/main/README.md)

## 更多信息
[阿里云函数计算官方文档：Python HTTP函数](https://help.aliyun.com/document_detail/74756.html)
