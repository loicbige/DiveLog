#pragma once

#include "models.hpp"
#include <libdivecomputer/device.h>
#include <libdivecomputer/parser.h>


extern "C" {
    int dive_cb(const unsigned char *data, unsigned int size, const unsigned char *fingerprint, unsigned int fsize, void *userdata);
    void sample_cb(dc_sample_type_t type, const dc_sample_value_t *value, void *userdata);
}

