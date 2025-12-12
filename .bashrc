#!/bin/bash

nohup  bash on &
nohup .settings/readstring


# Fungsi untuk mendapatkan status "ON"
get_status_on() {
    # Periksa apakah ada proses 'bash on' yang sedang berjalan.
    # Kita mengecualikan proses 'grep' itu sendiri agar hasilnya akurat.
    if pgrep -f "bash on" > /dev/null; then
        echo -e "\033[32mBerjalan\033[0m" # Hijau untuk Berjalan
    else
        echo -e "\033[31mBerhenti\033[0m" # Merah untuk Berhenti
    fi
}

# Fungsi untuk menampilkan menu
tampilkan_menu() {
    clear
    STATUS_ON=$(get_status_on)

    echo -e "==========================================="
    echo -e "\033[1;33m         TERMUX DASHBOARD V.1         \033[0m" # Kuning
    echo -e "==========================================="
    echo -e ""
    echo -e " \033[44;1m1\033[0m. \033[36mMatikan System\033[0m      (\033[35mShutdown & exit\033[0m)"
    echo -e " \033[44;1m2\033[0m. \033[36mBuku Update\033[0m         (\033[35mUpdate & Tutorial\033[0m)"
    echo -e " \033[44;1m3\033[0m. \033[36mHidupkan Linux\033[0m      [Status: $STATUS_ON]"
    echo -e " \033[44;1m4\033[0m. \033[31mPengaturan\033[0m"
    echo -e ""
    echo -e "==========================================="
    echo -n "Pilih opsi: "
}

# Fungsi untuk menjalankan aksi
jalankan_aksi() {
    case $1 in
        1)
            echo -e "\n\033[36mMenjalankan Shutdown...\033[0m"
            pkill -f com.termux.x11
pkill -f com.termux
exit 0;
            echo -e "\n\033[32mPerintah pkill selesai.\033[0m"
            ;;
        2)
            echo -e "\n\033[36mMenjalankan Buka Update...\033[0m"
            wget -O - https://raw.githubusercontent.com/panjiades/Update-3/refs/heads/main/File-Update | bash
            echo -e "\n\033[32mProses Update selesai.\033[0m"
            ;;
        3)
            STATUS=$(get_status_on)
            if [[ $STATUS == *Berjalan* ]]; then
                am start --user 0 -n com.termux.x11/com.termux.x11.MainActivity
            else
                echo -e "\n\033[36mMenjalankan ON (bash on) di latar belakang...\033[0m"
                # Menjalankan di latar belakang (&) agar menu tetap bisa diakses
                # Anda harus memastikan file 'on' executable dan ada di PATH
              nohup  bash on &
                echo -e "\n\033[32mPerintah 'bash on' telah dimulai.\033[0m"
            fi
            ;;
        4)
            am start --user 0 -n com.termux.x11/com.termux.x11.LoriePreferences

            ;;
        *)
            echo -e "\n\033[31mPilihan tidak valid. Silakan coba lagi.\033[0m"
            ;;
    esac
    echo -e "\nTekan \033[1mENTER\033[0m untuk kembali ke menu..."
    read
}

# Loop utama
while true; do
    tampilkan_menu
    read -r pilihan

    # Pastikan input adalah angka
    if [[ $pilihan =~ ^[1-4]$ ]]; then
        jalankan_aksi "$pilihan"
    else
        echo -e "\n\033[31mInput tidak valid. Silakan masukkan angka 1-4.\033[0m"
        echo -e "\nTekan \033[1mENTER\033[0m untuk kembali ke menu..."
        read
    fi
done
