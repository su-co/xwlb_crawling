#!/bin/bash

unset all_proxy && unset ALL_PROXY
export all_proxy=""
kill $(ps -ef | grep java | awk '{print $2}')
kill $(ps -ef | grep top | awk '{print $2}')
