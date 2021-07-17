#!/usr/bin/env bash
# created by xxy1991

BOOT_PATH='/boot/new'

BASE_URI='main/installer-amd64/current/images/netboot'
BASE_URI2='main/installer-amd64/current/legacy-images/netboot'
NETBOOTFILE='netboot.tar.gz'

GRUB40='/etc/grub.d/40_custom'
DGRUB='/etc/default/grub'

# netboot_download(str mirror, str os, str ver_code)
netboot_download() {
    rm -rf "${BOOT_PATH:?}/"*
    if [ ! -d ${BOOT_PATH} ]; then mkdir ${BOOT_PATH}; fi
    cd "${BOOT_PATH}" || exit

    if [ "${3}" = "focal" ]; then
        wget -Nq "${1}/${2}/dists/${3}/${BASE_URI2}/${NETBOOTFILE}" &&
            tar -zxf "${NETBOOTFILE}"
    else
        wget -Nq "${1}/${2}/dists/${3}/${BASE_URI}/${NETBOOTFILE}" &&
            tar -zxf "${NETBOOTFILE}"
    fi
}

# netboot_grub(str cfg_path)
netboot_grub() {
    grep 'New Install' "${GRUB40}" >&/dev/null
    if [ $? -eq 1 ]; then
        cat "$1" >>"${GRUB40}"
    fi
    sed -i '/^GRUB_DEFAULT=/c\GRUB_DEFAULT="New Install"' "${DGRUB}"
    sed -i '/^GRUB_TIMEOUT=/c\GRUB_TIMEOUT=1' "${DGRUB}"
    sed -i '/^GRUB_HIDDEN_TIMEOUT=/d' "${DGRUB}"
    update-grub
}

# netboot_preseed(str os, str cfg_path)
netboot_preseed() {
    cd "${BOOT_PATH}" || exit
    cp "$2" ./preseed.cfg
    initrd_file="${1}-installer/amd64/initrd"
    gunzip "${initrd_file}.gz"
    echo preseed.cfg | cpio -H newc -o -A -F "${initrd_file}"
    gzip "${initrd_file}"
}

# netboot_attach(str os, str file_path, str base_path)
netboot_attach() {
    cd "${BOOT_PATH}" || exit
    attach_file="${2}"
    base_path="${3}"
    initrd_file="${1}-installer/amd64/initrd"
    gunzip "${initrd_file}.gz"
    if [ -f "${base_path}/${attach_file}" ]; then
        cd "${base_path}" || exit
        ls "${attach_file}" | cpio -H newc -o -A -F "${BOOT_PATH}/${initrd_file}"
        cd "${BOOT_PATH}"
    elif [ -d "${base_path}/${attach_file}" ]; then
        cd "${base_path}" || exit
        find "${attach_file}" -depth -print0 | cpio --null -H newc -o -A -F "${BOOT_PATH}/${initrd_file}"
        cd "${BOOT_PATH}"
    else
        echo "attach file exception: ${base_path}/${attach_file}"
    fi
    gzip "${initrd_file}"
}

"$@"
