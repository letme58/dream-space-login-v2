// 合并版 Frida Hook 脚本 - 绕过反调试检测、获取密钥并Hook签名生成
// 运行命令: frida -U -f com.jingcai.apps.qualitydev -l hook.js --no-pause

console.log("=== 开始绕过 libnesec.so 反调试检测 ===");

function hook_dlopen() {
    const targetLibrary = "libnesec.so";
    var baseAddress = null;

    Interceptor.attach(Module.findExportByName(null, "android_dlopen_ext"), {
        onEnter: function (args) {
            var libraryPath = args[0].readCString();
            if (libraryPath && libraryPath.includes(targetLibrary)) {
                console.log("[+] Loading " + targetLibrary + " from: " + libraryPath);
                this.isTargetLib = true;
            }
        },
        onLeave: function (retval) {
            if (this.isTargetLib) {
                console.log("[+] " + targetLibrary + " loaded, handle: " + retval);
                baseAddress = Module.findBaseAddress(targetLibrary);
                console.log("[+] Base address of " + targetLibrary + " is: " + baseAddress);
                bypass_anti_debug(baseAddress);
                this.isTargetLib = false;
            }
        }
    });
}

function bypass_anti_debug(baseAddress) {
    Interceptor.attach(Module.findExportByName("libc.so", "pthread_create"), {
        onEnter: function (args) {
            var thread_start_routine = args[2];
            var offset = thread_start_routine.sub(baseAddress);
            
            if (offset.toString() === "0x103bdaa4") {
                console.warn("[!] Anti-debugging thread detected at offset: " + offset);
                Interceptor.replace(thread_start_routine, new NativeCallback(function () {
                    console.log("[+] Anti-debugging thread at " + offset + " neutralized.");
                    return ptr(0);
                }, 'pointer', []));
            }
        },
        onLeave: function (retval) {}
    });
}

hook_dlopen();

try {
    Interceptor.attach(Module.findExportByName(null, 'ptrace'), {
        onEnter: function (args) {
            args[0] = ptr(-1);
        },
        onLeave: function (retval) {
            retval.replace(0);
        }
    });
    console.log("[*] 成功 Hook ptrace");
} catch (e) {
    console.log("[!] 未找到 ptrace: " + e.message);
}

try {
    var tracerPidBypassed = false;
    Interceptor.attach(Module.findExportByName(null, 'read'), {
        onEnter: function (args) {
            this.fd = args[0].toInt32();
            this.buf = args[1];
            this.count = args[2].toInt32();
        },
        onLeave: function (retval) {
            if (retval > 0 && !tracerPidBypassed) {
                try {
                    const data = Memory.readUtf8String(this.buf, retval.toInt32());
                    if (data.includes("TracerPid:")) {
                        const patched = data.replace(/TracerPid:\s*\d+/, "TracerPid:\t0");
                        Memory.writeUtf8String(this.buf, patched);
                        console.log("[*] 绕过 TracerPid 检测");
                        tracerPidBypassed = true;
                    }
                } catch (e) {
                }
            }
        }
    });
    console.log("[*] 成功 Hook read");
} catch (e) {
    console.log("[!] 未找到 read: " + e.message);
}

Java.perform(function() {
    console.log("=== 到梦空间登录密钥 Hook 开始 ===");
    
    var NativeUtil = Java.use("com.jingcai.apps.qualitydev.utils.NativeUtil");
    
    NativeUtil.getNetSignModuleKey.implementation = function(context) {
        var result = this.getNetSignModuleKey(context);
        console.log("[RSA 公钥模块] " + result);
        return result;
    };
    
    NativeUtil.getNetSignExponent.implementation = function(context) {
        var result = this.getNetSignExponent(context);
        console.log("[RSA 公钥指数] " + result);
        return result;
    };
    
    NativeUtil.getNetSignReIV.implementation = function(context) {
        var result = this.getNetSignReIV(context);
        console.log("[AES 加密 IV] " + result);
        return result;
    };
    
    NativeUtil.getNetSignPlIV.implementation = function(context) {
        var result = this.getNetSignPlIV(context);
        console.log("[AES 解密 IV] " + result);
        return result;
    };
    
    console.log("=== 到梦空间登录密钥 Hook 完成 ===");
    
    console.log("[+] 开始执行签名生成Hook...");
    var SignUtil = Java.use("com.jingcai.apps.qualitydev.common.encrypt.i");
    
    SignUtil.d.implementation = function(map) {
        console.log("=== 签名生成开始 ===");
        
        console.log("输入参数:");
        try {
            var entrySet = map.entrySet();
            var iterator = entrySet.iterator();
            while (iterator.hasNext()) {
                var entry = iterator.next();
                try {
                    var key = entry.getKey();
                    var value = entry.getValue();
                    console.log("  " + key + ": " + value);
                } catch (e) {
                    console.log("  [Error] 无法获取键值: " + e.message);
                }
            }
        } catch (e) {
            console.log("  [Error] 遍历映射时出错: " + e.message);
        }
        
        var result = this.d(map);
        
        console.log("签名结果: " + result);
        
        console.log("=== 签名生成结束 ===\n");
        return result;
    };
    
    try {
        var context = Java.use("android.app.Application").getApplicationContext();
        console.log("[+] 尝试主动获取密钥信息...");
        NativeUtil.getNetSignModuleKey(context);
        NativeUtil.getNetSignExponent(context);
        NativeUtil.getNetSignReIV(context);
        NativeUtil.getNetSignPlIV(context);
    } catch (e) {
        console.log("[!] 主动获取密钥失败: " + e.message);
        console.log("[!] 密钥信息将在应用需要时自动打印");
    }
    
    console.log("[+] 所有Hook已加载完成！");
    console.log("请打开到梦空间应用，密钥和签名信息将自动打印");
});