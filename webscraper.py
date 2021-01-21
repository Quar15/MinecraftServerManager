import requests
from bs4 import BeautifulSoup


def get_versions():
    URL = 'http://files.minecraftforge.net/maven/net/minecraftforge/forge/index_1.1.html'

    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'}

    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')


    forge_links = []
    mc_versions = []
    for url in soup.find_all("a"):
        link = url.get('href')
        if link and "/maven/net/minecraftforge/forge/index" in link:
            mc_ver = link[38:-5]
            mc_versions.append(mc_ver)
            forge_link = "http://files.minecraftforge.net" + link
            forge_links.append(forge_link)

    return forge_links, mc_versions


def get_forge_version_from_url(url):

    if url != None:

        headers = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'}
        page = requests.get(url, headers=headers)

        soup = BeautifulSoup(page.content, 'html.parser')

        forge_ver = soup.find("small").text
        if forge_ver:
            forge_ver = forge_ver.replace(" ", "")
            return forge_ver

    return None


def get_forge_link(mc_ver, forge_links):

    for forge_link in forge_links:
        mc_ver_in_link = forge_link[69:-5]
        if mc_ver == mc_ver_in_link:
            print("@INFO: Found forge download link")
            print(forge_link)
            return forge_link

    print("@ERROR: Forge link not found")
    return None

if __name__ == "__main__":
    print("@INFO: Run main.py to use Minecraft Server Manager")