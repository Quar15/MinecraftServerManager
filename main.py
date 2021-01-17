from psutil import virtual_memory
import os
import json
import urllib3
import shutil

class Server:
    def __init__(self, name, mc_version=None, ram_to_use="4"):
        self.name = name
        if mc_version == None:
            self.mc_ver = self.check_latest_mc_version()
        else:
            self.mc_ver = mc_version
        self.forge_ver = self.check_forge_version()
        self.ram_to_use = ram_to_use
        self.manager_file = "MinecraftServerManager" + self.mc_ver + ".json"


    def __repr__(self):
        return "<Server>( Minecraft Version: {mc_ver} | Forge Version: {forge_ver} | Mods Path: {mods_path} | Config Path: {config_path} | RAM To Use: {ram_to_use} | Manager File: {manager_file}".format(mc_ver=self.mc_ver, forge_ver=self.forge_ver, mods_path=self.mods_path, config_path=self.config_path, ram_to_use=self.ram_to_use, manager_file=self.manager_file)
    
    
    def __str__(self):
        return "<Server>( Minecraft Version: {mc_ver} | Forge Version: {forge_ver} | Mods Path: {mods_path} | Config Path: {config_path} | RAM To Use: {ram_to_use} | Manager File: {manager_file}".format(mc_ver=self.mc_ver, forge_ver=self.forge_ver, mods_path=self.mods_path, config_path=self.config_path, ram_to_use=self.ram_to_use, manager_file=self.manager_file)
    
    
    def serialize(self):
        return {"mc_ver": self.mc_ver, "forge_ver": self.forge_ver, "mods_path": self.mods_path, "config_path": self.config_path, "ram_to_use": self.ram_to_use}


    def initialize_me(self):
        json_data = self.check_if_server_exists()
        if json_data == None:
            server_files_folder_path = "./data/servers/" + self.name
            if not os.path.isdir(server_files_folder_path):
                os.mkdir(server_files_folder_path)
            else:
                raise Exception("Server name already exists")

            self.download_server_files()
            self.edit_config("Message of the Day")


    def initialize_server(self):
        print("@INFO: Server is running")


    def check_forge_version(self):
        return "1.16.4-35.1.37"


    def download_forge(self, force=False):
        forge_file_path = './data/forge_installers/' + self.forge_ver + '.jar'
        if not os.path.isfile(forge_file_path) or force:
            http = urllib3.PoolManager()
            url = "https://files.minecraftforge.net/maven/net/minecraftforge/forge/{forge_ver}/forge-{forge_ver}-installer.jar".format(forge_ver=self.forge_ver)
            try:
                r = http.request('GET', url)
                with open(forge_file_path, "wb") as f:
                    f.write(r.data)
            except:
                print("@ERROR: Failed to download forge")
                print("URL:", url)
                return False
            return True


    def check_latest_mc_version(self):
        # @TODO: find most recent Minecraft version
        return "1.16.4"


    def check_if_server_exists(self):
        manager_file_path = "./data/" + self.manager_file
        print(manager_file_path)
        if os.path.isfile(manager_file_path):
            print("@INFO: Found server for that Minecraft version")
            if input(">> Overwrite old server? [y/N]: ").lower() != "y":
                try:
                    with open(manager_file_path, "r") as f:
                        return json.load(f)
                except:
                    print("@ERROR: Failed to load Minecraft Server Manager configuration file")
            else:
                print("@INFO: Overwriting data")
        return None


    def download_server_files(self):
        if self.download_forge():
            return True
        return False


    def install_server_files(self):
        if self.forge_ver != None:
            forge_file_path = "./data/forge_installers/" + self.forge_ver + ".jar"
            server_file_path = "./data/servers/" + self.name + "/" + self.forge_ver + ".jar"
            shutil.copy(forge_file_path, server_file_path)
            install_forge_cmd = "java -jar " + self.forge_ver + ".jar" + " --installServer"
            os.chdir("./data/servers/" + self.name)
            os.system(install_forge_cmd)
            os.chdir("...")
        return True


    def edit_config(self, motd, online_mode="false", difficulty="hard"):
        server_config_files_path = "./data/servers/" + self.name + "/"
        with open(server_config_files_path + "eula.txt", "w+") as f:
            f.write("eula=true")
        with open(server_config_files_path + "server.properties", "w+") as f:
            properties_txt = "motd=" + motd + "\nonline_mode=" + online_mode + "\ndifficulty=" + difficulty
            f.write(properties_txt)
        print("@INFO: Server configuration finished")


    def try_to_kill_server(self):
        print("@INFO: Trying to kill (safely) server process")


def convert_to_mb(bytes):
    return bytes//1024


def main():
    print("@INFO: Minecraft Server Manager initialized")

    mc_version_txt = input(">> Select Minecraft Version (leave empty to use latest): ")
    if mc_version_txt:
        # @TODO: add checking formatting
        mc_ver = mc_version_txt
    else:
        mc_ver = None

    serv_name = ""
    while len(serv_name) < 1:
        serv_name = input(">> Name your new server: ")

    mem = virtual_memory()
    server = Server(serv_name, mc_ver, convert_to_mb(mem.total//2))
    
    print("@INFO: Selected Minecraft version:", server.mc_ver)
    server.initialize_me()
    server.download_server_files()
    server.install_server_files()
    server.initialize_server()


if __name__ == "__main__":
    main()