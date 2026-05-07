#include "callback.hpp"

#include <string>
#include <vector>

void sample_cb(dc_sample_type_t type, const dc_sample_value_t *value,
               void *userdata) {
    Dive *computerCallback = static_cast<Dive *>(userdata);

    static Sample cur = {};

    switch (type) {
        case DC_SAMPLE_DECO:
            if (value->deco.type == DC_DECO_NDL) {
                cur.deco_ceiling.time_ms = value->deco.time;
            } else {
                cur.deco_ceiling.type = value->deco.type;
                cur.deco_ceiling.time_ms = value->deco.time;
                cur.deco_ceiling.depth_m = value->deco.depth;
                cur.deco_ceiling.tts = value->deco.tts;
            }
            break;

        case DC_SAMPLE_DEPTH:
            cur.depth_m = value->depth;
            break;

        case DC_SAMPLE_TIME:
            if (cur.time_ms != 0) {
                computerCallback->samples.push_back(cur);
                cur = {};
            }
            cur.time_ms = value->time;
            break;
        case DC_SAMPLE_PRESSURE:
            cur.tank.tank_id = value->pressure.tank;
            cur.tank.pressure_bar = value->pressure.value;
            break;
        case DC_SAMPLE_TEMPERATURE:
            cur.temp_c = value->temperature;
            break;
        default:
            break;
    }
}

int dive_cb(const unsigned char *data, unsigned int size, const unsigned char *fingerprint, unsigned int fsize,
            void *userdata) {
    UserData *ud = static_cast<UserData *>(userdata);
    dc_device_t *device = ud->device;
    std::vector<Dive> *dives = &ud->dives;

    Dive dive;
    dive.fingerprint = std::string((char *) fingerprint, fsize);
    /*PARSER */

    dc_parser_t *parser = {0};
    if (dc_parser_new(&parser, device, data, size) != DC_STATUS_SUCCESS) exit(EXIT_FAILURE);
    if (dc_parser_samples_foreach(parser, sample_cb, &dive) != DC_STATUS_SUCCESS) exit(EXIT_FAILURE);

    dives->push_back(dive);
    if (dc_parser_destroy(parser) != DC_STATUS_SUCCESS) exit(EXIT_FAILURE);
    return 1;
}
