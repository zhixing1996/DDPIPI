#!/bin/sh
cd /besfs5/users/$USER/bes/DDPIPI/v0.2/data
rm -rf data_raw_sideband_before.root
hadd data_raw_sideband_before.root */*raw_sideband_before.root
cd /besfs5/users/$USER/bes/DDPIPI/v0.2/sigMC/mixed
rm -rf shape_mixed.root
hadd shape_mixed.root shape_*_mixed.root
