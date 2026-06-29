# 到梦空间登录脚本

到梦空间 App 登录加密分析与 Frida Hook 脚本集合。

## 项目结构

```
.
├── hook.js          # 合并版 Frida Hook 脚本（反调试绕过+密钥获取+签名Hook）
├── 密钥hook.js      # 密钥获取专用 Hook 脚本
├── 签名hook.js      # 签名生成专用 Hook 脚本
├── login.py         # Python 登录模拟脚本
├── 登录请求.py       # 登录请求测试脚本
└── 登录分析.md       # 加密流程分析文档
```

## 功能说明

### Frida Hook 脚本

1. **反调试绕过**：Hook `ptrace`、`read`（TracerPid）、`libnesec.so` 反调试线程
2. **密钥获取**：Hook `NativeUtil` 类获取 RSA 公钥模块、指数、AES IV
3. **签名分析**：Hook 签名生成方法，打印输入参数和签名结果

### Python 脚本

1. **login.py**：完整实现登录加密流程（RSA+AES+签名）
2. **登录请求.py**：直接发送登录请求测试

## 使用方法

### Frida Hook

```bash
frida -U -f com.jingcai.apps.qualitydev -l hook.js --no-pause
```

### Python 登录

```bash
pip install rsa pycryptodome requests
python login.py
```

## 加密流程

1. 参数排序（TreeMap）
2. 生成签名（SHA-512 → 取位 → MD5）
3. 生成随机 AES 密钥（16位）
4. RSA 加密随机密钥
5. AES-CBC 加密参数
6. 拼接加密数据 + 加密密钥 → Base64