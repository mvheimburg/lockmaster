#!/bin/sh

python3 -m grpc_tools.protoc -I. --python_out=app/doormanager/src --grpc_python_out=app/doormanager/src protos/doormanager.proto
# python3 -m grpc_tools.protoc -I. --python_out=app/doormanager_test/src --grpc_python_out=app/doormanager_test/src protos/doormanager.proto
# sudo protoc -I. protos/doormanager.proto --dart_out=grpc:app/web/doorcontrol/protos
protoc -I protos/ doormanager.proto plugin=protoc-gen-dart=$HOME/snap/flutter/common/flutter/.pub-cache/bin/protoc-gen-dart --dart_out=grpc:app/web/doorcontrol/protos

