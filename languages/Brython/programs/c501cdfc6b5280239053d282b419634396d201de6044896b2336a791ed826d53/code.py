from browser import document, html

def add_todo(event):
    """Add a new todo item to the list"""
    todo_input = document["todo-input"]
    todo_text = todo_input.value.strip()
    
    if todo_text:
        # Create new list item
        todo_item = html.LI()
        todo_item.text = todo_text
        
        # Create delete button
        delete_btn = html.BUTTON("Delete")
        delete_btn.bind("click", lambda e: todo_item.remove())
        
        todo_item <= delete_btn
        document["todo-list"] <= todo_item
        
        # Clear input
        todo_input.value = ""

# Bind the add button
document["add-btn"].bind("click", add_todo)
