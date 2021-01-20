from psutil import virtual_memory
import os
import json
import urllib3
import shutil
import webscraper as ws

FORGE_LINKS, MC_VERSIONS = ws.get_versions()

class Server:
    def __init__(self, name, mc_version=None, ram_to_use="4"):
        self.name = name
        self.mc_ver = mc_version
        self.forge_ver = self.check_forge_version()
        self.ram_to_use = ram_to_use
        self.manager_file = "MinecraftServerManager" + self.name + ".json"


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
                raise Exception("@ERROR: Server name already exists")

            self.download_server_files()
            self.edit_config("Message of the Day")


    def initialize_server(self):
        try:
            server_file_path = "forge-{forge_ver}.jar".format(forge_ver=self.forge_ver)
            run_server_cmd = "java -Xmx8G -Xms1G -jar {server_file} nogui".format(server_file = server_file_path)
            os.mkdir("mods")
            wait_for_mods_txt = ">> Waiting to add mods in {path} [Enter]: ".format(path=os.path.dirname(os.path.abspath(server_file_path)))
            input(wait_for_mods_txt)
            print("@INFO: Server is running")
            os.system(run_server_cmd)
        except:
            print("@WARNING: Failed to run", server_file_path)


    def check_forge_version(self):
        print("@INFO: Looking for forge version")
        forge_ver = ws.get_forge_version_from_url(ws.get_forge_link(self.mc_ver, FORGE_LINKS))
        return forge_ver


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
            server_installer_file = self.forge_ver + ".jar"
            server_file_path = "./data/servers/" + self.name + "/" + server_installer_file
            shutil.copy(forge_file_path, server_file_path)
            install_forge_cmd = "java -jar " + self.forge_ver + ".jar" + " --installServer"
            os.chdir("./data/servers/" + self.name)
            os.system(install_forge_cmd)

            print("@INFO: Deleting installation files")
            os.remove(server_installer_file)
            os.remove(server_installer_file + ".log")
            return True
        return False


    def edit_config(self, motd, online_mode="false", difficulty="hard"):
        server_config_files_path = "./data/servers/" + self.name + "/"
        with open(server_config_files_path + "eula.txt", "w+") as f:
            f.write("eula=true")
        with open(server_config_files_path + "server.properties", "w+") as f:
            properties_txt = "motd=" + motd + "\nonline-mode=" + online_mode + "\ndifficulty=" + difficulty
            f.write(properties_txt)
        print("@INFO: Server configuration finished")


    def try_to_kill_server(self):
        print("@INFO: Trying to kill (safely) server process")


def convert_to_mb(bytes):
    return bytes//1024


def input_mc_version():
    
    while True:
        mc_version_txt = input(">> Select Minecraft Version (leave empty to use latest): ")
        
        mc_ver = None
        if mc_version_txt in MC_VERSIONS:
            mc_ver = mc_version_txt
        else:
            print("@ERROR: Minecraft", mc_version_txt, "not found")
            mc_version_txt = MC_VERSIONS[0]
            mc_ver = mc_version_txt
        print("@INFO: Minecraft", mc_version_txt, "selected.")
        confirm_text = input(">> Install? [Y/n]: ")
        if confirm_text.lower() == "y" or confirm_text == "":
            break

    return mc_ver

def initialize_app():

    try:
        os.mkdir("./data")
        os.mkdir("./data/forge_installers")
        os.mkdir("./data/servers")
    except OSError:
        pass

    print("@INFO: Minecraft Server Manager initialized")


def main():
    initialize_app()

    mc_ver = input_mc_version()

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