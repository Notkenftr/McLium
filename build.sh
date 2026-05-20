rm -rf ./build/
cmake -S . -B build
cmake --build build -j

while [ ! -f ./build/aoko.so ]; do
    sleep 0.1
done

sleep 1

mv ./build/aoko.so ~/PycharmProjects/test/