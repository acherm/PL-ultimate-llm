import {api} from '../api'

export tag ShowcaseCard < button
    prop item
    prop index

    def render
        <self[d:hflex ja:center]>
            <div.preview[pos:relative w:100% h:100% d:block]>
                <div.overlay[pos:absolute inset:0 bg:gray9.10 z:1]>
                <div.title[pos:absolute l:4 b:4 z:2 c:white fs:xl fw:600]> item.title
                <img[d:block w:100% h:100% object-fit:cover] src=api.url(item.image)>

    def enter
        let rect = getBoundingClientRect()
        let clone = <div.preview[pos:fixed z:100] style=rect>
        document.body.appendChild(clone)
        imba.commit do
            clone.style.borderRadius = '2rem'
            clone.style.width = '100%'
            clone.style.height = '100%'
            clone.style.top = 0
            clone.style.left = 0
        await 200ms
        imba.commit do
            clone.find('.overlay').style.opacity = 0
        await 200ms
        emit('show',item)
        await 100ms
        clone.remove()

    def ontap e
        enter()