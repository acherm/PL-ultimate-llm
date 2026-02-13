# Build and test a project

default:
    just --list

# Build the project
build:
    echo "Building project..."
    mkdir -p build
    cc -o build/program src/main.c

# Run tests
test: build
    echo "Running tests..."
    ./build/program --test
    echo "All tests passed!"

# Clean build artifacts
clean:
    rm -rf build

# Install dependencies
install-deps:
    echo "Installing dependencies..."
    apt-get update && apt-get install -y build-essential

# Run the application
run: build
    ./build/program

# Format code
fmt:
    clang-format -i src/*.c src/*.h
