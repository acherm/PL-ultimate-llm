#!/usr/bin/env nextflow

params.msg = 'Hello world!'

process sayHello {
    
    input:
    val msg from params.msg
 
    output:
    stdout
 
    """
    echo '$msg'
    """
}

sayHello()