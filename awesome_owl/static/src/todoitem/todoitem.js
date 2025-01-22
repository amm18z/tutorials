import { Component, useState } from "@odoo/owl";

export class TodoItem extends Component {
    static template = "awesome_owl.todoitem";

    static props = {
        todo: { id: Number, description: String, isCompleted: Boolean }
    };
}