mkdir -p build
cd build
cmake ..
cmake --build .
sudo cmake --build . --target install