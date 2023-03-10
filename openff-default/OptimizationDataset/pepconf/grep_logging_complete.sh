#!/bin/bash

grep -v "INCOMPLETE" logging.log | grep -v "INVALID" | grep "COMPLETE" | grep "INFO" > logging_complete.log