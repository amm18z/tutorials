import { Component, useState } from "@odoo/owl";

export class Card extends Component {
    static template = "awesome_owl.card";

    //static props = ['title', 'content']
    // ^ props with no validation

    static props = {
        title: String,
        content: String
    };
    // ^ props with validation

    setup() {
        // this.state = useState({  });
        // not setting anything up yet really
    }

    
}