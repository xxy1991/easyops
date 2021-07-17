#!/usr/bin/env bash
# netboot.sh by xxy1991

CFG_URI='https://cfg.ori.fyi'

BOOT_PATH='/boot/new'
MIRROR='http://mirrors.163.com'
BASE_URI='main/installer-amd64/current/images/netboot'
NETBOOTFILE='netboot.tar.gz'
GRUB40='/etc/grub.d/40_custom'
DGRUB='/etc/default/grub'

# netboot_download(str os, str version)
netboot_download() {
    wget -Nq "${MIRROR}/${1}/dists/${2}/${BASE_URI}/${NETBOOTFILE}"
    tar -zxf ${NETBOOTFILE}
}

# netboot_grub(str os)
netboot_grub() {
    grep 'New Install' ${GRUB40} >&/dev/null
    if [ $? -eq 1 ]; then
        wget -qO - "${CFG_URI}/boot/msdos-${1}.cfg" | cat - >>${GRUB40}
    fi
    sed -i '/^GRUB_DEFAULT=/c\GRUB_DEFAULT="New Install"' ${DGRUB}
    sed -i '/^GRUB_TIMEOUT=/c\GRUB_TIMEOUT=1' ${DGRUB}
    sed -i '/^GRUB_HIDDEN_TIMEOUT=/d' ${DGRUB}
    update-grub
}

# netboot_grub(str os)
netboot_preseed() {
    wget -qO preseed.cfg "${CFG_URI}/boot/preseed-${2}.cfg"
    initrd_file="${1}-installer/amd64/initrd"
    gunzip "${initrd_file}.gz"
    echo preseed.cfg | cpio -H newc -o -A -F "${initrd_file}"
    gzip "${initrd_file}"
}

rm -rf ${BOOT_PATH}/*
if [ ! -d ${BOOT_PATH} ]; then mkdir ${BOOT_PATH}; fi
cd ${BOOT_PATH}

if [ -n "$1" ]; then
    case $1 in
    debian)
        netboot_download 'debian' 'buster'
        netboot_grub 'debian'
        netboot_preseed 'debian' $2
        reboot
        ;;
    ubuntu)
        netboot_download 'ubuntu' 'focal'
        netboot_grub 'ubuntu'
        netboot_preseed 'ubuntu' $2
        reboot
        ;;
    manual-debian)
        netboot_download 'debian' 'buster'
        netboot_grub 'debian'
        ;;
    manual-ubuntu)
        netboot_download 'ubuntu' 'focal'
        netboot_grub 'ubuntu'
        ;;
    *)
        echo 'error:no target!'
        ;;
    esac
fi
