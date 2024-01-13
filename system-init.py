import os
import subprocess

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        raise Exception(f"command failed: {stderr.decode().strip()}")
    return stdout.decode().strip()

def run_command_interactive(command):
    subprocess.run(command, shell=True)

def install_yay():
    print("installing yay")
    run_command_interactive("git clone https://aur.archlinux.org/yay.git")
    os.chdir("yay")
    run_command_interactive("makepkg -si")
    os.chdir("..")
    run_command("rm -rf yay")
    print("yay installed successfully")

def install_blackarch():
    print("installing BlackArch")
    run_command("curl -O https://blackarch.org/strap.sh")
    run_command("chmod +x strap.sh")
    run_command_interactive("sudo ./strap.sh")
    run_command("rm strap.sh")
    print("BlackArch installed successfully.")


def install_packages(category, packages):
    response = input(f"do you want to install {category} packages? (yes/no): ").lower()
    if response.startswith('y'):
        for package in packages:
            print(f"installing {package}...")
            run_command_interactive(f"yay -S {package}")
    elif response.startswith('n'):
        print(f"skipping installation of {category} packages")
            
def clone_and_copy_repo():
    print("cloning your gitlab repository...")
    run_command("git clone https://gitlab.com/insidesources/archlinux.git")
    os.chdir("archlinux")
    print("copying files to the home directory")
    run_command_interactive("sudo cp -ri . ~/")
    
def change_default_shell():
    print("changing the default shell to ZSH")
    run_command_interactive("chsh -s /usr/bin/zsh")

def main():
    try:
        install_yay()
        install_blackarch()

        #package lists
        core_packages = ["linux-zen-headers", "feh", "firefox", "bitwarden", "alacritty", "kvantum", "qt5ct", "qt6ct", "ttf-nerd-fonts-symbols-mono",
                        "noto-fonts-emoji", "arc-gtk-theme", "arc-icon-theme", "discord", "betterdiscord-installer-bin", "brave-bin", "debtap", "dunst", "easyeffects",
                        "glances", "mc", "google-chrome", "gotop", "ledger-live-bin", "lxappearance", "lynx", "mysql-workbench", "neofetch",
                        "neovim", "nitrogen", "noisetorch", "notepadqq", "notion-app-enhanced", "nvidia-settings", "nvtop", "obs-studio", "obsidian", "onlyoffice-bin",
                        "openrgb", "openvpn", "pavucontrol", "picom", "postman-bin", "powershell-bin", "protonmail-bridge-bin", "protonvpn", "proxychains-ng", "qbittorrent",
                        "qflipper", "qtile-extras", "qutebrowser", "rofi", "rofi-power-menu-git", "rpi-imager", "scrot", "solaar", "spicetify-cli", "spotify",
                        "streamdeck-ui", "tailscale", "teamviewer", "telegram-desktop", "termius", "thunderbird", "tmux", "tor", "torbrowser-launcher", "tradingview",
                        "unicode-character-database", "unicode-emoji", "visual-studio-code-bin", "vlc", "vmware-workstation", "weechat", "xorg-xrandr", "xreader", "zerotier-one", "zoom",
                        "zsh", "man"]
        
        cybersecurity_tools = ["dnsrecon", "exploitdb", "hydra", "metasploit", "ngrok", "nmap", "phonesploit", "punter", "recon-ng", "set",
                        "sublist3r", "thefatrat", "theharvester", "wireshark-qt", "wpscan"]
        
        games = ["steam", "lutris", "curseforge", "strongbox", "proton-ge-custom-bin"]

        install_packages("core packages", core_packages)
        install_packages("cybersecurity tools", cybersecurity_tools)
        install_packages("games", games)
        
        clone_and_copy_repo()
        
        change_default_shell()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
