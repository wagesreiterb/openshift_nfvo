#!/usr/bin/env bash

curl -X PUT -H 'Content-Type: multipart/form-data' \
    -F 'file=@/home/que/Bernhard/NFV/tosca_examples/myCSAR.zip' \
    http://127.20.0.3:8000/vnfpkgm/v1/vnf_packages/8/package_content/
