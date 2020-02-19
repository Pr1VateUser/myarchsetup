#/bin/bash
systemctl enable dhcpcd
systemctl start dhcpcd
sleep 10
useradd -m user 
echo -e "user ALL=(ALL) ALL" >> /etc/sudoers
sed -i "/\[multilib\]/,/Include/"'s/^#//' /etc/pacman.conf
pacman -Syuu xorg-server xorg-xinit plasma sddm plasma konsole ntfs-3g dolphin nano --noconfirm
systemctl enable sddm
passwd user
systemctl start sddm
