#!/usr/bin/env bash

curl -X POST "http://172.20.0.3:8000/vnfpkgm/v1/vnf_packages/" \
    -H  "accept: application/json" \
    -H  "Content-Type: application/json"\
    -H  "X-CSRFToken: CVePEZabbidmzZN2m4KExdbOHLsFPLRMTi7tuNWzAeGe7pShUF4wcD5DEtR90kzy"\
    -d "{   \"vnfdId\": \"8\",    \
            \"vnfProvider\": \"bbb\",    \
            \"vnfProductName\": \"myProduct\",    \
            \"vnfSoftwareVersion\": \"1.9\",    \
            \"vnfdVersion\": \"1.0\",    \
            \"checksum\": \"123\",    \
            \"onboardingState\": \"CREATED\",    \
            \"operationalState\": \"DISABLED\",    \
            \"usageState\": \"NOT_IN_USE\"  \
        }"
echo