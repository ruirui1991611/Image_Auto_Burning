# Image_Auto_Burning[image自动烧录]
说明:
我们的image是放在jenkins上的, jenkins是一个开源的、提供友好操作界面的持续集成(CI)工具, 主要用于持续, 自动的构建/测试软件项目, 监控外部任务的运行(参考:https://www.jianshu.com/p/5f671aca2b5a ), jenkins官网: https://www.jenkins.io/. 由于每次烧录都要先image单独下载到本地, 然后再通过特定的烧录工具将其固化至board上, 时间久了就会觉得麻烦, 故自己写了简单的python脚本(使用python是自己偷懒了, 通过shell使用wget, sed和awk也是完全可以做的), 将爬取和烧录放在一起.