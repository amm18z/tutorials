import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todoitem";

    static props = {
        todo: { id: Number, description: String, isCompleted: Boolean },
        toggleState: Function,
        removeProp: Function,
    };

    onChange(){
        this.props.toggleState(this.props.todo.id)
    }

    onClick(){
        this.props.removeProp(this.props.todo.id) // calling the function bound to removeProp (binding occurred in todolist.xml)
    }
}