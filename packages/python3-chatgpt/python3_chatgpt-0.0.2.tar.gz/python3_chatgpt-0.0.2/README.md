# chatgpt
## 安装
```bash
pip3 install python3-chatgpt
```

## 用法
```python
from chatgpt.chatgpt import ChatGPT

chatgpt=ChatGPT(api_key="xxx",base_url="https:/xxx.com")
rs=chatgpt.ask("你是谁")
print(rs)
```