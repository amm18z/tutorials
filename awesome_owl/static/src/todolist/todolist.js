import { Component, useState } from "@odoo/owl";
import { TodoItem } from "../todoitem/todoitem";

export class TodoList extends Component {
    static template = "awesome_owl.todolist";


    static components = {TodoItem };

    setup() {
        this.todos = useState( [{ id: 1, description: "buy milk", isCompleted: false }, 
                                { id: 2, description: "buy bread", isCompleted: false }, 
                                { id: 3, description: "buy eggs", isCompleted: false }] );
    }
}