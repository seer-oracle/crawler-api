# -*- coding: utf-8 -*-
"""
   Description:
        -
        -
"""
import lib.enums.http as httpEnum


class ErrorCode(httpEnum.ErrorCode):
    ErrorFileRequire = 'ErrorFileRequire'
    ErrorFileTypeSupport = 'ErrorFileTypeSupport'
    ErrorS3Service = 'ErrorS3Service'
    ErrorLiveStreamTranscodeService = 'ErrorLiveStreamTranscodeService'


