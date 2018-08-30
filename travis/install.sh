if [[ "$TRAVIS_OS_NAME" == "osx" ]]; then
    brew install libusb
    wget -nv -O riscv-toolchain.tar.gz https://bintray.com/platformio/dl-packages/download_file?file_path=toolchain-riscv-pulp-darwin_x86_64-1.70101.180706.tar.gz
else
    wget -nv -O riscv-toolchain.tar.gz https://bintray.com/platformio/dl-packages/download_file?file_path=toolchain-riscv-pulp-linux_x86_64-1.70101.180703.tar.gz
fi

mkdir riscv-toolchain && tar xvf riscv-toolchain.tar.gz -C riscv-toolchain
export PATH=`pwd`/riscv-toolchain/bin:$PATH