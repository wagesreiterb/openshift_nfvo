#!/usr/bin/env bash

sqlite3 -line /home/que/PycharmProjects/nfv/nfvo/db.sqlite3 'select * from api_vnfpkgmodel;'
sqlite3 -line /home/que/PycharmProjects/nfv/nfvo/db.sqlite3 'DELETE FROM api_vnfpkgmodel WHERE vnfPkgInfo_id = 7;'
sqlite3 -line /home/que/PycharmProjects/nfv/nfvo/db.sqlite3 'select * from api_vnfpkgmodel;'
