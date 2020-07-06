#ifndef SHM_READER_H
#define SHM_READER_H

#include <stdlib.h>

#define DEFAULT_BUFFER      204800

#define EXPORT __attribute__((visibility("default")))
#define IMPORT

class ShmReader {
    private:
        int mShmKey;
    public:
        ShmReader(unsigned int key);
        ~ShmReader();

        int nx;
        int ny;
        int datasize;
        u_int8_t *numpy_buffer;

        int read_data();
};

extern "C" {

void* create_shm_reader(int key);
void  release_shm_reader(void* shm_reader);
void*  read_data(void* shm_reader);
}

#endif //SHM_READER_H
