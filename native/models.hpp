#pragma once
#include <vector>
#include <string>
#include <libdivecomputer/device.h>


struct Sample {
    int time_ms;
    float depth_m;
    float temp_c;

    struct {
        int type;
        float depth_m;
        int time_ms;
        int tts;
    } deco_ceiling;

    struct {
        int tank_id;
        float pressure_bar;
    } tank;
};

struct Dive {
    std::vector<Sample> samples;
    std::string fingerprint;
};

struct UserData {
    dc_device_t *device;
    std::vector<Dive> dives;
};
