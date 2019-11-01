import os
from intelhex import hex2bin
file_path = "D:\工作\python\download\static"
start = None
end = None
size = None
pad = None
header_data = [0x55, 0x00, 0x00, 0x20, 0x64, 0x00, 0x80, 0x46]
DEFAULT_STEP = 0x40
DEFAULT_TAIL = [0x20, ]
DEFAULT_READ_BIN_DATA_SIZE = 128
DEFAULT_BIN_FILE_TAIL = [0x51, 0x20]


def get_hex_file_name():
    # 获取文件名
    path = os.listdir(file_path)
    for file in path:
        if 'hex' in file:
            hex_file_name = file
            list = file.split('.')[:-1]
            file_name = '.'.join(list)
            bin_file_name = file_name + ".bin"
            # print("bin文件名称为:" + bin_file_name)
            return (hex_file_name, bin_file_name)
        else:
            print('no file_name')


def hex_to_bin():
    # hex文件转成bin文件
    hex_file_name, bin_file_name = get_hex_file_name()
    hex_file_path = os.path.join(file_path, hex_file_name)
    bin_file_path = os.path.join(file_path, bin_file_name)
    hex2bin(hex_file_path, bin_file_path, start, end, size, pad)
    return bin_file_path


def bin_add_agreement():
    #  bin文件加入协议信息
    bin_file_path = hex_to_bin()
    size_of_file = os.path.getsize(bin_file_path)   # bin文件大小
    count = size_of_file // 128      # 计算分块个数
    remainder = size_of_file % 128
    if remainder == 0:      # 正好整除的情况
        write_to_bin(count)

    else:                   # 不能整除的情况
        count = count + 1
        write_to_bin(count)


def write_to_bin(count):
    # bin文件写入具体数组内容
    bin_file_path = hex_to_bin()
    with open(file_path + '/new.bin', "wb+") as f:
        with open(bin_file_path, 'rb') as file:
            header_data_list = []

            # 1.写入 xx  xx 8个字节
            for i in range(count):
                if i != 0:
                    calc(header_data, DEFAULT_STEP)
                new_header_data = header_data[:]
                new_header_data[4] = 0x74
                header_data_list.append(new_header_data)

                # print('要写入的内容为:', header_data)
                f.write(bytearray(header_data))
                # 写入文件的代码
                file.seek(int(DEFAULT_READ_BIN_DATA_SIZE * i), 0)
                code = file.read(DEFAULT_READ_BIN_DATA_SIZE)
                f.write(code)
                f.write(bytearray(DEFAULT_TAIL))       # 写入0x20
            # 2.写入 0x74
            for i in range(len(header_data_list)):
                f.write(bytearray(header_data_list[i]))
                f.write(bytearray(DEFAULT_TAIL))
            # 3. 写入51 20
            f.write(bytearray(DEFAULT_BIN_FILE_TAIL))
    os.remove(bin_file_path)
    os.rename(file_path + '/new.bin', bin_file_path)


def calc(data, step):
    tmp = data[1] + step
    high = (tmp & 0xff00) >> 8
    low = tmp & 0xff
    if high > 0x00:
        data[2] = data[2] + high
        data[1] = low

    else:
        data[1] = low


if __name__ == '__main__':
    bin_add_agreement()

