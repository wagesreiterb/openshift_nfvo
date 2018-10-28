#!/usr/bin/env bash

curl -X PUT -H 'Content-Type: multipart/form-data' \
    -F 'file=@/home/que/Bernhard/NFV/tosca_examples/myCSAR.zip' \
    http://127.0.0.1:8000/vnfpkgm/v1/vnf_packages/7/package_content/
