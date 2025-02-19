import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";

    //static props = ['title', 'content']
    // ^ props validation

    static props = {
        title: String,
        slots: Object
    };
    // ^ props validation with type

    setup() {
        this.state = useState({isOpen: Boolean});
        this.state.isOpen = true;
    }

    toggle(){
        this.state.isOpen = !this.state.isOpen;
    }
}