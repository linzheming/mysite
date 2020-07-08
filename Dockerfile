# 建立 python3.7 环境
FROM python:3.7

# 镜像作者
MAINTAINER LZM

# 设置 python 环境变量
ENV PYTHONUNBUFFERED 1

# 设置pypi源头为国内源
COPY pip.conf /root/.pip/pip.conf

# 在容器内/var/www/html/下创建 mysite2 文件夹
RUN mkdir -p /var/www/html/mysite

# 设置容器内工作目录
WORKDIR /var/www/html/mysite

# 将当前目录文件拷贝一份到工作目录中（. 表示当前目录）
ADD . /var/www/html/mysite

# 利用 pip 安装依赖
RUN pip install -r requirements.txt


# 设置start.sh文件可执行权限
RUN chmod +x ./start.sh
