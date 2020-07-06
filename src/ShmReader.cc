#include <ShmReader.hh>

ShmReader::ShmReader(unsigned int key) : mShmKey(key),
                                nx(100),
                                ny(100),
                                datasize(3),
                                numpy_buffer(NULL)


{
}


ShmReader::~ShmReader(){
    free(numpy_buffer);
}

int ShmReader::read_data() {
    int buffer_size = nx*ny*datasize;
    if (!numpy_buffer){
        numpy_buffer = (u_int8_t *) malloc(buffer_size);
    }

    for(int i=0; i < buffer_size ; i++){
       numpy_buffer[i] = (u_int8_t)1.0;
    }
    return 1;
}


//C definitions
void* create_shm_reader(int key){
    return new ShmReader(key);
}

void  release_shm_reader(void* shm_reader) {
    delete static_cast<ShmReader*>(shm_reader);
}

void*  read_data(void* shm_reader) {
    static_cast<ShmReader*>(shm_reader)->read_data();
    return static_cast<ShmReader*>(shm_reader)->numpy_buffer;
}



