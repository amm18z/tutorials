import { Component, useState } from "@odoo/owl";
import { TodoItem } from "./todoitem";
import { useAutofocus } from "../utils.js";

export class TodoList extends Component {
    static template = "awesome_owl.todolist";

    static components = {TodoItem };

    setup() {
        // this.todos = useState( [{ id: 1, description: "buy milk", isCompleted: false }, 
        //                         { id: 2, description: "buy bread", isCompleted: true }, 
        //                         { id: 3, description: "buy eggs", isCompleted: false }] );

        this.todos = useState([]);
        this.nextId = 0;
        useAutofocus("input");
    }

    /* ^ How does OWL/the interpreter/whatever is relevant here know that todos is an array of TodoItem objects? */

    /* Answer: in this file, it doesn't. In todolist.js, todos is just an array of plain javascript objects.
               the real type reconciliation, if you could call it that, happens in todolist.xml, when it tries to render  via:
                <t t-foreach="todos" t-as="todo" t-key="todo.id">
                    <TodoItem todo="todo"/>
                </t> 

                which is possible because of this line:
                    static components = {TodoItem };
                in this file.
    */

    addTodo(ev) {
        if (ev.keyCode === 13 && ev.target.value != "") {
            this.todos.push({
                id: this.nextId++,
                description: ev.target.value,
                isCompleted: false
            });
            ev.target.value = "";
        }
    }

    toggleTodo(todoId) 
    {
        const todo = this.todos.find((todo) => todo.id === todoId);
        if (todo) {
            todo.isCompleted = !todo.isCompleted
        }
    }

    removeTodo(todoId) 
    {
        const index = this.todos.findIndex((elem) => elem.id === todoId);
        if (index >= 0) {
            // remove the element at index from list
            this.todos.splice(index, 1);
        }
    }
}