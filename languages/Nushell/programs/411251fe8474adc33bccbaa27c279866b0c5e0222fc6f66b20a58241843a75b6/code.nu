def monitor_containers [] {
    loop {
        clear
        print $'(ansi green)Docker Container Status Monitor(ansi reset)'
        docker ps | from ssv -a | sort-by 'CONTAINER ID'
        sleep 2sec
    }
}

def docker-stats [] {
    docker stats --no-stream | from ssv | sort-by 'Container ID' | update Memory {
        get Memory | str replace '.+?/(.+)' '$1'
    } | move Memory --after 'Container ID'
}