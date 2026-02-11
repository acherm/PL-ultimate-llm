Window_Width  :: 1280;
Window_Height :: 720;

main :: () {
    window := create_window(Window_Width, Window_Height, "Basic Window");
    
    while !window.should_close {
        update_window_events();
        
        render_context := window.render_context;
        clear_render_target(0.15, 0.15, 0.15, 1);
        swap_buffers(window);
    }
}