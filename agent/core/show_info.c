#include "core.h"

#include <errno.h>
#include <inttypes.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>

int main(int argc, char **argv) {
    struct core_info info;
    if (argc == 2 && strcmp(argv[1], "--check-null") == 0) {
        int err = core_get_info(NULL);
        printf("NULL: %d (%s)\n", err, strerror(err));
        return err == EINVAL ? 0 : 1;
    }
    int err = core_get_info(&info);
    if (err) {
        fprintf(stderr, "core_get_info: %s\n", strerror(err));
        return 1;
    }
    printf("sizeof: %zu, offsets: %zu %zu %zu %zu\n", sizeof info,
           offsetof(struct core_info, pid), offsetof(struct core_info, cpus),
           offsetof(struct core_info, page_size), offsetof(struct core_info, host));
    printf("pid: %" PRId64 "\ncpus: %" PRId32 "\npage_size: %" PRId32 "\nhost: %s\n",
           info.pid, info.cpus, info.page_size, info.host);
    return 0;
}
