#include <iostream>
#include <h5cpp/hdf5.hpp>
#include <vector>

using namespace hdf5;

int main() {
    file::File f = file::create("example.h5", file::AccessFlags::TRUNCATE);
    node::Group root = f.root();

    std::vector<int> data{0, 1, 2, 3, 4, 5};
    node::Dataset dataset(root, "data", datatype::create<std::vector<int>>(), dataspace::create(data));
    dataset.write(data);

    std::vector<int> saved_data(dataset.dataspace().size());
    dataset.read(saved_data);

    for(unsigned int i = 0; i < data.size(); ++i) {
        if(data[i] != saved_data[i]) {
            std::cout << data[i] << " != " << saved_data[i] << std::endl;
            return 1;
        }
    }

    return 0;
}
