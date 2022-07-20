################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
CC_SRCS += \
../src/Converter.cc \
../src/Converter2D-3D.cc \
../src/Initializer.cc \
../src/InputReader.cc \
../src/KeyFrame.cc \
../src/Map.cc \
../src/MapManager.cc \
../src/MapPoint.cc \
../src/Optimizer.cc \
../src/OutputWriter.cc 

CPP_SRCS += \
../src/main.cpp 

CC_DEPS += \
./src/Converter.d \
./src/Converter2D-3D.d \
./src/Initializer.d \
./src/InputReader.d \
./src/KeyFrame.d \
./src/Map.d \
./src/MapManager.d \
./src/MapPoint.d \
./src/Optimizer.d \
./src/OutputWriter.d 

CPP_DEPS += \
./src/main.d 

OBJS += \
./src/Converter.o \
./src/Converter2D-3D.o \
./src/Initializer.o \
./src/InputReader.o \
./src/KeyFrame.o \
./src/Map.o \
./src/MapManager.o \
./src/MapPoint.o \
./src/Optimizer.o \
./src/OutputWriter.o \
./src/main.o 


# Each subdirectory must supply rules for building sources it contributes
src/%.o: ../src/%.cc src/subdir.mk
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -I/home/user/eclipse-workspace/Triangulacion/include -I/home/user/eclipse-workspace/Triangulacion/include/Thirdparty/g2o/lib -I/usr/include/eigen3 -I/usr/include/opencv4 -I/usr/lib/x86_64-linux-gnu -O2 -g -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '

src/%.o: ../src/%.cpp src/subdir.mk
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C++ Compiler'
	g++ -I/home/user/eclipse-workspace/Triangulacion/include -I/home/user/eclipse-workspace/Triangulacion/include/Thirdparty/g2o/lib -I/usr/include/eigen3 -I/usr/include/opencv4 -I/usr/lib/x86_64-linux-gnu -O2 -g -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


clean: clean-src

clean-src:
	-$(RM) ./src/Converter.d ./src/Converter.o ./src/Converter2D-3D.d ./src/Converter2D-3D.o ./src/Initializer.d ./src/Initializer.o ./src/InputReader.d ./src/InputReader.o ./src/KeyFrame.d ./src/KeyFrame.o ./src/Map.d ./src/Map.o ./src/MapManager.d ./src/MapManager.o ./src/MapPoint.d ./src/MapPoint.o ./src/Optimizer.d ./src/Optimizer.o ./src/OutputWriter.d ./src/OutputWriter.o ./src/main.d ./src/main.o

.PHONY: clean-src

