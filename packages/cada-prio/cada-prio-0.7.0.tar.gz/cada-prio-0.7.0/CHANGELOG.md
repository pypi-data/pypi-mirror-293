# Changelog

## [0.7.0](https://www.github.com/varfish-org/cada-prio/compare/v0.6.1...v0.7.0) (2024-08-29)


### Features

* command to dump OpenAPI schema ([#58](https://www.github.com/varfish-org/cada-prio/issues/58)) ([#59](https://www.github.com/varfish-org/cada-prio/issues/59)) ([317a767](https://www.github.com/varfish-org/cada-prio/commit/317a7674002543720084d4e5532db4cc7dc456e5))

### [0.6.1](https://www.github.com/bihealth/cada-prio/compare/v0.6.0...v0.6.1) (2023-11-16)


### Bug Fixes

* pinning python to 3.11 for build so we have setuptools ([#36](https://www.github.com/bihealth/cada-prio/issues/36)) ([54d4e8c](https://www.github.com/bihealth/cada-prio/commit/54d4e8c4be8bdd7ad6b9f839b22a798b5f527d27))

## [0.6.0](https://www.github.com/bihealth/cada-prio/compare/v0.5.0...v0.6.0) (2023-11-16)


### Features

* adding API prefix, OpenAPI and docs to REST server ([#35](https://www.github.com/bihealth/cada-prio/issues/35)) ([1a2f605](https://www.github.com/bihealth/cada-prio/commit/1a2f605bbaa28ed511b117efa04de256dcff149d))
* adding classic and current model ([#25](https://www.github.com/bihealth/cada-prio/issues/25)) ([44ddf24](https://www.github.com/bihealth/cada-prio/commit/44ddf24abf939eed8ad56b80cb1e90f60846a390))

## [0.5.0](https://www.github.com/bihealth/cada-prio/compare/v0.4.0...v0.5.0) (2023-09-18)


### Features

* adding "tune run-optuna" command ([#23](https://www.github.com/bihealth/cada-prio/issues/23)) ([6cc753b](https://www.github.com/bihealth/cada-prio/commit/6cc753b3b4f92aa75d961c3cf314e097d174ede0))
* re-useable implementation of "tune train-eval" ([#21](https://www.github.com/bihealth/cada-prio/issues/21)) ([c80c4bf](https://www.github.com/bihealth/cada-prio/commit/c80c4bf1d69ff83bcb84b949cf3383746580a12d))

## [0.4.0](https://www.github.com/bihealth/cada-prio/compare/v0.3.1...v0.4.0) (2023-09-14)


### Features

* adding dump-graph to cli ([#18](https://www.github.com/bihealth/cada-prio/issues/18)) ([3aace31](https://www.github.com/bihealth/cada-prio/commit/3aace31166ddbd4357ae32283b6514a21404e0ef))
* adding param-opt command with single parameter evaluation ([#20](https://www.github.com/bihealth/cada-prio/issues/20)) ([83141c6](https://www.github.com/bihealth/cada-prio/commit/83141c6c4afe6efffc51fcde1ebdc92b5b3d0fbf))
* allow running with legacy model/graph data ([#16](https://www.github.com/bihealth/cada-prio/issues/16)) ([9d3cc7c](https://www.github.com/bihealth/cada-prio/commit/9d3cc7cea6efeac82b41fe11dfc9527ab4fe2913))
* embedding parameters can be provided via CLI and contains seeds ([#19](https://www.github.com/bihealth/cada-prio/issues/19)) ([bbd5d86](https://www.github.com/bihealth/cada-prio/commit/bbd5d86e879db94240093c20145b1c4c45edc69e))

### [0.3.1](https://www.github.com/bihealth/cada-prio/compare/v0.3.0...v0.3.1) (2023-09-13)


### Bug Fixes

* add missing line endings to hgnc_info.jsonl ([#13](https://www.github.com/bihealth/cada-prio/issues/13)) ([aa14b9b](https://www.github.com/bihealth/cada-prio/commit/aa14b9b948a0e9512c57567de2acaa65e9b132bc))
* properly parsing comma-separated list on REST API ([#14](https://www.github.com/bihealth/cada-prio/issues/14)) ([97fdfee](https://www.github.com/bihealth/cada-prio/commit/97fdfeee118d2e4985ca71433617fd9c470d0b49))

## [0.3.0](https://www.github.com/bihealth/cada-prio/compare/v0.2.1...v0.3.0) (2023-09-11)


### Features

* also adding gene-to-phen edges from HPO ([#9](https://www.github.com/bihealth/cada-prio/issues/9)) ([d5a8337](https://www.github.com/bihealth/cada-prio/commit/d5a833774b1488fb7e1f0650692aab2c3f753144))

### [0.2.1](https://www.github.com/bihealth/cada-prio/compare/v0.2.0...v0.2.1) (2023-09-08)


### Bug Fixes

* removing spurious debug print statement ([#7](https://www.github.com/bihealth/cada-prio/issues/7)) ([98e7443](https://www.github.com/bihealth/cada-prio/commit/98e74433001872517a4904bbe85fd021cc4ad613))

## [0.2.0](https://www.github.com/bihealth/cada-prio/compare/v0.1.0...v0.2.0) (2023-09-08)


### Features

* gene to phenotype links file can be gziped ([#5](https://www.github.com/bihealth/cada-prio/issues/5)) ([66c48bf](https://www.github.com/bihealth/cada-prio/commit/66c48bf98c8bd73f8227c7cbd5687b4e74577ef8))

## 0.1.0 (2023-09-07)


### Features

* adding REST API server for prediction ([#4](https://www.github.com/bihealth/cada-prio/issues/4)) ([8bb7516](https://www.github.com/bihealth/cada-prio/commit/8bb75161097529932f371925fe860290098f0885))
* initial training implementation ([#1](https://www.github.com/bihealth/cada-prio/issues/1)) ([10d3a7c](https://www.github.com/bihealth/cada-prio/commit/10d3a7cb356b50a89fd8b1226ad66932dd5542f3))
* prioritization prediction with model ([#3](https://www.github.com/bihealth/cada-prio/issues/3)) ([48d504c](https://www.github.com/bihealth/cada-prio/commit/48d504c0bc373e1ae312773fa70a5a2e04d8dbed))
