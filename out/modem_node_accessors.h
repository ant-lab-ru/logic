#pragma once

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

// version
uint8_t modem_write_version_bootloader(modem_node_t* self);
uint8_t modem_read_version_bootloader(modem_node_t* self);

uint8_t modem_write_version_test_field(modem_node_t* self);
uint8_t modem_read_version_test_field(modem_node_t* self);

// nandfs
uint8_t modem_write_nandfs_total_files(modem_node_t* self);
uint8_t modem_read_nandfs_total_files(modem_node_t* self);

uint8_t modem_write_nandfs_next_name(modem_node_t* self);
uint8_t modem_read_nandfs_next_name(modem_node_t* self);

uint8_t modem_write_nandfs_erase_nand(modem_node_t* self);
uint8_t modem_read_nandfs_erase_nand(modem_node_t* self);

// fs
uint8_t modem_write_fs_total_files(modem_node_t* self);
uint8_t modem_read_fs_total_files(modem_node_t* self);

uint8_t modem_write_fs_next_name(modem_node_t* self);
uint8_t modem_read_fs_next_name(modem_node_t* self);

uint8_t modem_write_fs_erase_nand(modem_node_t* self);
uint8_t modem_read_fs_erase_nand(modem_node_t* self);

// memfs
uint8_t modem_write_memfs_value(modem_node_t* self);
uint8_t modem_read_memfs_value(modem_node_t* self);

#ifdef __cplusplus
}
#endif
