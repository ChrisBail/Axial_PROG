#!/usr/bin/env bash

# Program made to convert William's ddfile into xyz time mag file

awk 'NF>5 {var = sprintf("%04d-%02d-%02dT%02d:%02d:%06.3f",$2,$3,$4,$5,$6,$7);print $9,$8,$10,var, $11}' $1
