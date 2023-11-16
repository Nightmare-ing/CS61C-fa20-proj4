cmake_minimum_required(VERSION 3.10.2)

project(Numc
        VERSION 1.0.0
        LANGUAGES C)

set(CMAKE_C_FLAGS "-g -Wall -std=c99 -fopenmp -mavx -mfma -pthread")
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -fopenmp")

# Set CUnit Library
find_library(CUNIT_LIBRARY cunit)

# Set Python libraries
find_package(Python3 REQUIRED COMPONENTS Development)

# add executable
add_executable(test mat_test.c matrix.c numc.c)
add_executable(dumbpy dumbmatrix.c dumbpy.c)

# modify compile and link options
# target_compile_options(test PRIVATE "${CFLAGS}")
# target_link_options(test PRIVATE ${LDFLAGS})

# include libraries
target_include_directories(test PRIVATE
        "./"
        ${Python3_INCLUDE_DIRS})
target_link_libraries(test PRIVATE
        ${CUNIT_LIBRARY}
        ${Python3_LIBRARIES})

target_include_directories(dumbpy PRIVATE
        "./"
        ${Python3_INCLUDE_DIRS})
target_link_libraries(dumbpy PRIVATE
        ${CUNIT_LIBRARY}
        ${Python3_LIBRARIES})

