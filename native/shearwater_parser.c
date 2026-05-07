#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <libdivecomputer/context.h>
#include <libdivecomputer/descriptor.h>
#include <libdivecomputer/device.h>
#include <libdivecomputer/parser.h>

typedef struct
{
    float temp_c;
    float depth_m;
    int time_ms;
    struct
    {
        int time_ms;
        float depth_m;
        int tts_ms;
        int type; // SAFETYSTOP/DECO/NDL
    } deco_ceiling;
    struct
    {
        int tank_id;
        float pressure_bar;
    } pressure;

} sample_t;

typedef struct
{
    int count;
    int capacity;
    sample_t current;
    sample_t *samples;
} DiveData_t;

static void sample_cb(dc_sample_type_t type, const dc_sample_value_t *value, void *userdata)
{

    DiveData_t *data = (DiveData_t *)userdata;

    sample_t *cur = &data->current;

    switch (type)
    {
    case DC_SAMPLE_TEMPERATURE:
        cur->temp_c = value->temperature;
        break;
    case DC_SAMPLE_DECO:
        cur->deco_ceiling.depth_m = value->deco.depth;
        cur->deco_ceiling.time_ms = value->deco.time;
        cur->deco_ceiling.tts_ms = value->deco.tts;
        cur->deco_ceiling.type = value->deco.type;
        break;
    case DC_SAMPLE_TIME:
        if (cur->time_ms != 0)
        {
            if (data->count >= data->capacity)
            {
                data->capacity *= 2;
                data->samples = realloc(data->samples, data->capacity * sizeof(sample_t));
            }

            data->samples[data->count] = data->current;
            data->count++;
            memset(&data->current, 0, sizeof(sample_t));
        }
        cur->time_ms = value->time;

        break;
    case DC_SAMPLE_DEPTH:
        cur->depth_m = value->depth;
        break;
    case DC_SAMPLE_PRESSURE:
        cur->pressure.tank_id = value->pressure.tank;
        cur->pressure.pressure_bar = value->pressure.value;
        break;

    default:
        break;
    }
}
