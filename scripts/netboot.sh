#!/usr/bin/env bash
# created by xxy1991

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

test(){
    echo "abc"
}

"$@"
