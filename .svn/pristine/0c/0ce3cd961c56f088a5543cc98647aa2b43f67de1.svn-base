#! /bin/bash

# 打印错误
error() {
    echo $(red [错误]) "$@"
    exit 1
}

# 打印警告
warn() {
    echo $(yellow [警告]) "$@"
}

# 打印信息
echo2() {
    echo $(green [操作]) "$@"
}

yellow() {
	echo -e "\033[1;43m$1\033[0m"
}

red() {
	echo -e "\033[1;41m$1\033[0m"
}

green() {
	echo -e "\033[1;42m$1\033[0m"
}