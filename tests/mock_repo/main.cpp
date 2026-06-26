#include "helper.h"

#ifdef DEBUG
class DebugLogger {
    void log(const char* msg) {}
};
#endif

#ifdef RELEASE
class OptimizedLogger {
    void log(const char* msg) {}
};
#endif

#ifdef _WIN32
class WindowsService {
    void runWin() {}
};
#else
class LinuxService {
    void runLinux() {}
};
#endif
