#include "core.h"

#include <errno.h>
#include <limits.h>
#include <string.h>
#include <unistd.h>

static int read_system_value(int key, int32_t *out) {
    errno = 0;
    long value = sysconf(key);
    if (value <= 0)
        return errno ? errno : EINVAL;
    if (value > INT32_MAX)
        return EOVERFLOW;
    *out = (int32_t)value;
    return 0;
}

int core_get_info(struct core_info *out) {
    if (out == NULL)
        return EINVAL;

    struct core_info info = {0};
    info.pid = getpid();
    int err = read_system_value(_SC_NPROCESSORS_ONLN, &info.cpus);
    if (err)
        return err;
    err = read_system_value(_SC_PAGESIZE, &info.page_size);
    if (err)
        return err;
    if (gethostname(info.host, sizeof info.host) != 0)
        return errno;
    if (memchr(info.host, '\0', sizeof info.host) == NULL)
        return ENAMETOOLONG;

    *out = info;
    return 0;
}
