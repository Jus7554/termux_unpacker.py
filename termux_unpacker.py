
import os
import sys
import subprocess
import time

class TermuxUnpacker:
    def __init__(self):
        self.tools_dir = os.path.join(os.path.expanduser("~"), "termux_unpacker_tools")
        self.output_dir = os.path.join(os.path.expanduser("~"), "termux_unpacker_output")
        self.setup_environment()

    def setup_environment(self):
        """إعداد المجلدات اللازمة"""
        os.makedirs(self.tools_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        print("\033[1;32m[+] تم إعداد بيئة العمل: مجلد الأدوات في {} ومجلد الإخراج في {}\033[0m".format(self.tools_dir, self.output_dir))

    def run_command(self, command, description, check_output=False):
        """تنفيذ أوامر النظام مع عرض الوصف والتحقق من الأخطاء"""
        print(f"\033[1;34m[*] {description}...\033[0m")
        try:
            process = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
            if check_output:
                print(process.stdout)
            return process.stdout
        except subprocess.CalledProcessError as e:
            print(f"\033[1;31m[!] خطأ أثناء {description}:\033[0m")
            print(f"\033[1;31m{e.stderr}\033[0m")
            return None
        except FileNotFoundError:
            print(f"\033[1;31m[!] الأمر '{command.split()[0]}' غير موجود. يرجى التأكد من تثبيته.\033[0m")
            return None

    def install_dependencies(self):
        """تثبيت المتطلبات الأساسية في Termux"""
        print("\033[1;33m[*] جاري تثبيت المتطلبات الأساسية. قد يستغرق هذا بعض الوقت...\033[0m")
        commands = [
            "pkg update -y && pkg upgrade -y",
            "pkg install python nodejs openjdk-17 wget curl git -y",
            "pip install frida-tools frida-dexdump"
        ]
        for cmd in commands:
            if self.run_command(cmd, f"تثبيت {cmd.split()[0]} أو حزمة ذات صلة") is None:
                print("\033[1;31m[!] فشل تثبيت بعض المتطلبات. يرجى التحقق من الاتصال بالإنترنت والمحاولة مرة أخرى.\033[0m")
                return False
        print("\033[1;32m[+] تم تثبيت جميع المتطلبات بنجاح.\033[0m")
        return True

    def unpack_with_frida(self, package_name):
        """استخدام frida-dexdump لفك التشفير من الذاكرة"""
        print(f"\033[1;34m[*] بدء فك التشفير للتطبيق: {package_name} باستخدام Frida-DexDump\033[0m")
        print("\033[1;33m[!] تأكد من تشغيل التطبيق المستهدف على هاتفك أولاً.\033[0m")
        print("\033[1;33m[!] قد تحتاج إلى تشغيل 'frida-server' يدويًا على جهازك إذا لم يتم اكتشافه تلقائيًا.\033[0m")
        
        # محاولة تشغيل frida-server إذا لم يكن يعمل (لأجهزة الروت أو إذا كان frida-gadget محقونًا)
        # هذا الجزء يحتاج إلى تعديل ليتناسب مع بيئة Termux بدون روت بشكل كامل (Frida Gadget)
        # حالياً، يفترض أن frida-server يعمل أو أن frida-gadget تم حقنه يدوياً.
        
        cmd = f"frida-dexdump -U -f {package_name} -d -o {self.output_dir}/{package_name}"
        if self.run_command(cmd, "تشغيل frida-dexdump", check_output=True) is not None:
            print(f"\033[1;32m[+] تم استخراج ملفات DEX إلى: {self.output_dir}/{package_name}\033[0m")
        else:
            print("\033[1;31m[!] فشل فك التشفير باستخدام Frida-DexDump. يرجى التحقق من تشغيل التطبيق و Frida-server/gadget.\033[0m")

    def unpack_360_jiagu(self, apk_path):
        """منطق فك حماية 360/Jiagu (يتطلب أدوات إضافية أو سكربتات مخصصة)"""
        print("\033[1;33m[*] وظيفة فك حماية 360/Jiagu قيد التطوير. حالياً، يرجى استخدام خيار Frida-DexDump.\033[0m")
        print("\033[1;33m[!] فك حماية 360/Jiagu يتطلب عادةً أدوات متخصصة مثل Jiagu Unpacker أو تحليل يدوي.\033[0m")
        print("\033[1;33m[!] يمكنك محاولة استخدام Frida-DexDump إذا كانت الحماية تعتمد على فك التشفير في الذاكرة.\033[0m")
        # هنا يمكن دمج سكربتات بايثون خارجية لفك حماية 360 مثل SafaSafari/jiagu_unpacker
        # ولكن هذا يتطلب تحميل السكربتات وتجهيز بيئتها بشكل منفصل.

    def unpack_dpt_shell(self, apk_path):
        """منطق فك حماية Dpt-Shell (يتطلب أداة dpt.jar)"""
        print("\033[1;33m[*] وظيفة فك حماية Dpt-Shell قيد التطوير. حالياً، يرجى استخدام خيار Frida-DexDump.\033[0m")
        print("\033[1;33m[!] فك حماية Dpt-Shell يتطلب أداة dpt.jar الرسمية أو تحليل يدوي.\033[0m")
        print("\033[1;33m[!] يمكنك محاولة استخدام Frida-DexDump إذا كانت الحماية تعتمد على فك التشفير في الذاكرة.\033[0m")
        # هنا يمكن دمج أداة dpt.jar إذا كانت متوفرة وتم تحميلها في مجلد tools
        # مثال: java -jar {self.tools_dir}/dpt.jar -f {apk_path} --dump-code -o {self.output_dir}

    def check_protection(self, apk_path):
        """فحص نوع الحماية الموجودة في ملف APK (فحص مبدئي)"""
        print(f"\033[1;34m[*] فحص الحماية لـ {apk_path}...\033[0m")
        if not os.path.exists(apk_path):
            print("\033[1;31m[!] ملف APK غير موجود في المسار المحدد.\033[0m")
            return

        try:
            # استخدام apktool لفك التفكيك الجزئي والبحث عن مؤشرات الحماية
            temp_dir = os.path.join(self.output_dir, "temp_apk_analysis")
            self.run_command(f"apktool d -f {apk_path} -o {temp_dir}", "تفكيك APK لتحليل الحماية")

            protection_found = []

            # مؤشرات 360/Jiagu
            if os.path.exists(os.path.join(temp_dir, "lib", "armeabi-v7a", "libjiagu.so")) or \
               os.path.exists(os.path.join(temp_dir, "lib", "arm64-v8a", "libjiagu.so")):
                protection_found.append("360/Jiagu Protection")
            
            # مؤشرات Dpt-Shell (قد تختلف حسب الإصدار)
            if os.path.exists(os.path.join(temp_dir, "lib", "armeabi-v7a", "libdpt.so")) or \
               os.path.exists(os.path.join(temp_dir, "lib", "arm64-v8a", "libdpt.so")):
                protection_found.append("Dpt-Shell Protection")

            # مؤشرات حماية ARM (عامة وقد تتداخل)
            # يمكن البحث عن ملفات DEX مشفرة أو كلاسات معينة
            # هذا الفحص يحتاج إلى تحليل أعمق لملفات smali أو DEX
            # كمثال مبدئي، سنعتبر وجود ملفات .so مشفرة مؤشراً
            if not protection_found and (os.path.exists(os.path.join(temp_dir, "lib")) and any(fname.endswith('.so') for root, dirs, files in os.walk(os.path.join(temp_dir, "lib")) for fname in files)):
                 protection_found.append("Generic Native/ARM Protection (further analysis needed)")

            if protection_found:
                print(f"\033[1;32m[+] تم العثور على الحمايات التالية: {', '.join(protection_found)}\033[0m")
            else:
                print("\033[1;33m[!] لم يتم العثور على مؤشرات حماية معروفة بشكل مباشر. قد يكون التطبيق غير محمي أو يستخدم حماية غير مكتشفة.\033[0m")

        except Exception as e:
            print(f"\033[1;31m[!] حدث خطأ أثناء تحليل APK: {e}\033[0m")
        finally:
            # تنظيف الملفات المؤقتة
            self.run_command(f"rm -rf {temp_dir}", "تنظيف الملفات المؤقتة")

    def menu(self):
        print("""
    \033[1;36m====================================
      Termux Unpacker (No Root)
    ====================================\033[0m
    \033[1;33m[!] يرجى التأكد من تثبيت جميع المتطلبات قبل البدء (الخيار 1)\033[0m

    1. \033[1;34mتثبيت/تحديث المتطلبات (Dependencies)\033[0m
    2. \033[1;34mفك تشفير تطبيق (Frida-DexDump) - عام لمعظم الحمايات\033[0m
    3. \033[1;34mفك حماية 360/Jiagu (قيد التطوير - استخدم 2 حالياً)\033[0m
    4. \033[1;34mفك حماية Dpt-Shell (قيد التطوير - استخدم 2 حالياً)\033[0m
    5. \033[1;34mفحص حماية ملف APK (يتطلب Apktool)\033[0m
    6. \033[1;31mخروج\033[0m
    \033[1;36m====================================\033[0m
        """)
        choice = input("\033[1;32m[?] اختر عملية: \033[0m")
        if choice == '1':
            self.install_dependencies()
        elif choice == '2':
            pkg = input("\033[1;32m[?] أدخل اسم حزمة التطبيق (مثال: com.example.app): \033[0m")
            self.unpack_with_frida(pkg)
        elif choice == '3':
            apk_path = input("\033[1;32m[?] أدخل المسار الكامل لملف APK: \033[0m")
            self.unpack_360_jiagu(apk_path)
        elif choice == '4':
            apk_path = input("\033[1;32m[?] أدخل المسار الكامل لملف APK: \033[0m")
            self.unpack_dpt_shell(apk_path)
        elif choice == '5':
            apk_path = input("\033[1;32m[?] أدخل المسار الكامل لملف APK: \033[0m")
            self.check_protection(apk_path)
        elif choice == '6':
            print("\033[1;32m[+] شكراً لاستخدامك Termux Unpacker. إلى اللقاء!\033[0m")
            sys.exit()
        else:
            print("\033[1;31m[!] خيار غير صالح. يرجى الاختيار من 1 إلى 6.\033[0m")

if __name__ == "__main__":
    unpacker = TermuxUnpacker()
    while True:
        unpacker.menu()
